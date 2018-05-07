
import os
import struct
import csv


def print_csv(data, path):
    # print("-- " + str(len(data.keys())) + " channels detected")

    for experimentName in data.keys():
        experiment = data[experimentName]

        experiment_infos = [[], [], [], []]
        experiment_data = []

        max_times_number = 0

        for sample in experiment:
            infos, times, data = sample

            max_times_number = max(max_times_number, len(times))

        for sample in experiment:

            infos, times, data = sample

            experiment_infos[2].append("Sample")
            experiment_infos[2].append(infos[0][2:-1])

            experiment_infos[3].append("Parameters")
            experiment_infos[3].append(infos[8][2:-1])

            experiment_infos[0].append("Time")
            experiment_infos[0].append("Intensity")

            experiment_infos[1].append("min")
            experiment_infos[1].append(infos[7][2:-1])

            for i in range(0, max_times_number):
                if len(experiment_data) <= i:
                    experiment_data.append([])

                if len(times) > i:
                    experiment_data[i].append(times[i] / 60000.0)
                    experiment_data[i].append(data[i])
                else:
                    experiment_data[i].append("")
                    experiment_data[i].append("")

        filename = str(experimentName[:-3]) + '.csv'
        exportname = os.path.join(path, filename)

        c = csv.writer(open(exportname, "w"))

        for info in experiment_infos:
            c.writerow(info)

        for line in experiment_data:
            c.writerow(line)


def read_ind_file(fname):

    with open(fname, 'rb') as f:

        if f.read(2) != b'\x02\x33':
            # print("Invalid file")
            return

        infos = []

        f.seek(0x18)
        sample = str(f.read(struct.unpack('>B', f.read(1))[0]))  # unsigned char
        infos.append(sample)

        f.seek(0x94)
        operator = str(f.read(struct.unpack('>B', f.read(1))[0]))  # unsigned char
        infos.append(operator)

        f.seek(0xB2)
        date = str(f.read(struct.unpack('>B', f.read(1))[0]))  # unsigned char
        infos.append(date)

        f.seek(0xD0)
        weird1 = str(f.read(struct.unpack('>B', f.read(1))[0]))  # unsigned char
        infos.append(weird1)

        f.seek(0xDA)
        weird2 = str(f.read(struct.unpack('>B', f.read(1))[0]))  # unsigned char
        infos.append(weird2)

        f.seek(0xE4)
        method = str(f.read(struct.unpack('>B', f.read(1))[0]))  # unsigned char
        infos.append(method)

        f.seek(0x195)
        version = str(f.read(struct.unpack('>B', f.read(1))[0]))  # unsigned char
        infos.append(version)

        f.seek(0x244)
        yUnits = str(f.read(struct.unpack('>B', f.read(1))[0]))  # unsigned char
        infos.append(yUnits)

        f.seek(0x254)
        detector = str(f.read(struct.unpack('>B', f.read(1))[0]))  # unsigned char
        infos.append(detector)

        f.seek(0x284)
        del_ab = struct.unpack('>d', f.read(8))[0]  # double

        f.seek(0x400)
        loc = 0
        data = []

        while True:
            f.read(1)  # Always 0x10 ?

            rec_len = struct.unpack('>B', f.read(1))[0]
            if rec_len == 0:
                break

            for _ in range(rec_len):
                inp = struct.unpack('>h', f.read(2))[0]  # short

                if inp == -32768:  # 0x8000
                    inp = struct.unpack('>i', f.read(4))[0]  # int
                    data.append(inp * del_ab)
                elif loc == 0:
                    data.append(inp * del_ab)
                else:
                    data.append(data[loc - 1] + inp * del_ab)

                loc += 1

        # Time points generation (x axis) / Temps de début et de fin en ms
        f.seek(0x11A)
        st_t = struct.unpack('>i', f.read(4))[0]
        en_t = struct.unpack('>i', f.read(4))[0]

        data_len = len(data)
        interval = (en_t - st_t) / data_len
        times = []
        loc2 = 0

        for _ in range(data_len):
            if len(times) == 0:
                times.append(st_t)
            else:
                times.append(times[loc2 - 1] + interval)

            loc2 += 1

    for i in range(len(infos)):
        infos[i] = infos[i].replace(',', ' -')  # Avoid commas in infos (replace them with -)

    return infos, times, data


class Decrypter:
    """
    This class was a bit of a mess. It was supposed to be in converter.py, and only be used
    after the module has created and started the Tk app/root.

    """
    def __init__(self, folder, delegate):

        experimentList = []

        #for root, subFolders, files in os.walk(os.getcwd()):
        for fRoot, subFolders, files in os.walk(folder):
            for fichier in files:
                if fichier[-2:] == '.B':
                    # New experiment
                    experimentList.append(fRoot)

        if len(experimentList) > 0:
            print("Processing " + str(len(experimentList)) + ' experiments')

            i = 0

            for experiment in experimentList:
                text = "Processing folder " + os.path.basename(experiment) + " - " + "{:.1f}".format(i / len(experimentList) * 100) + "% finished"
                delegate.statusText.config(text=text)
                delegate.instructionLabel.config(text="Please wait while we convert your files")
                # root.update()

                self.process_experiment(experiment)
                i += 1

            print("Done")
            delegate.statusText.config(text="All jobs finished")
            delegate.instructionLabel.config(text="Program ready for another conversion job")
        else:
            delegate.statusText.config(text="Nothing to convert")
            delegate.instructionLabel.config(text="Please select a folder containing HPLC 1100 Series data")
            #print("Nothing to process here :(")

    def process_experiment(self, path):
        fileList = {}
        #print("- Processing experiment " + os.path.basename(path))

        for fRoot, subFolders, files in os.walk(path):
            for fichier in files:
                if fichier[-3:] == '.ch':
                    fileName = os.path.join(fRoot, fichier)

                    if fichier in fileList.keys():
                        fileList[fichier].append(fileName)
                    else:
                        fileList[fichier] = [fileName]

        dataSet = {}

        for key in fileList.keys():

            subData = []

            for fileName in fileList[key]:
                infos, times, data = self.read_ind_file(fileName)
                subData.append((infos, times, data))

            dataSet[key] = subData

        self.print_csv(dataSet, path)

