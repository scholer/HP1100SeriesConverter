
Note: This fork was created to convert the project from a "pyinstaller app only" package 
to a proper distribution package that you can install with `pip` and use from python
in your normal data analysis workflows.

All credit for the original code goes to @TheTrueTom (github.com/TheTrueTom).


#HP 1100 Series Data Converter [![GitHub license](https://img.shields.io/dub/l/vibe-d.svg)](https://raw.githubusercontent.com/TheTrueTom/HP1100SeriesConverter/master/LICENCE) [![GitHub release](https://img.shields.io/github/release/TheTrueTom/HP1100SeriesConverter.svg)](https://github.com/TheTrueTom/HP1100SeriesConverter/releases/latest)

### Building Instructions for Windows

- Make sure you have pyinstaller on your system
- Navigate to the project's folder
- Run the following command: pyinstaller 1100SeriesConverter.spec

Alternatively you can download a binary from github

### Operating Instructions

- Select a folder
- Click convert !

### Remarks

- The program will walk the entire subtree looking for HP Chemstation data and create corresponding csv files.
- One file per detector channel is created, each files regroups all samples.
- CSV can be directly imported into Origin or Excel

## License

HP1100SeriesConverter is released under the [MIT License](LICENSE.md).

HP1100SeriesConverter is not associated in any way to HP or Agilent.
