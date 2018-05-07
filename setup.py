# from distutils.core import setup
from setuptools import setup, find_packages
import os


# Get the long description from the README file:
PROJECT_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(PROJECT_ROOT_DIR, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except IOError:
    long_description = None


# Distribution build and release:
#   python setup.py sdist
#   python setup.py bdist_wheel
#   twine upload dist/*
# Note: Make sure to use `pip -v` when pip-installing, so you can check what is being installed.
setup(
    name='hp1100-hplc',
    version='0.1.0dev1',
    packages=find_packages(),  # List all packages (directories) to include in the source dist.
    url='https://github.com/scholer/HP1100SeriesConverter',
    license='MIT License',
    author='Rasmus Scholer Sorensen',
    author_email='rasmusscholer@gmail.com',
    description='HP1100SeriesConverter. Extraction and conversion of HPLC data from the HP/Agilent 1100-series HPLC.',
    long_description=long_description,
    keywords=['HPLC', 'HP', 'Agilent', '1100', 'data', 'data-conversion', 'data-extraction'],
    entry_points={
        # 'console_scripts': [
        #     'todoist-action-cli=actionista.todoist.action_cli:action_cli',
        #     'actionista-todoist=actionista.todoist.action_cli:action_cli',  # New alias
        #     'todoist-adhoc=actionista.todoist.adhoc_cli:main',
        #     'todoist_today_or_overdue=actionista.todoist.adhoc_cli:print_today_or_overdue_tasks',
        # ],
        # 'gui_scripts': [
        # ]
    },
    # pip will install these modules as requirements.
    install_requires=[
    ],
    python_requires='>=3.5',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',
        # 'Intended Audience :: Science/Research',
        # 'Intended Audience :: Developers',
        # 'Intended Audience :: Education',
        # 'Intended Audience :: Healthcare Industry',

        # 'Topic :: Software Development :: Build Tools',
        # 'Topic :: Education',
        # 'Topic :: Scientific/Engineering',

        # Pick your license as you wish (should match 'license' above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX :: Linux',
    ],
)
