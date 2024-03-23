# Sim racing - track analysis
This project is dedicated for data analysis of track result which came from ACC and are exported as CSV files from MoTeC software. This project would contain tools to process and visualize data.

## How to install
To install program you need to download zip file from `master` branch (green code button)


## Requirements
Current requirements are python3.10 or highier

# How to use CLI
To open program in CLI mode, you have to run `File_preparation_CLI.py` file. TThen you have access to main menu. 

To run the file you need to have python interpreter installed on your system. Then you can run file, either opening file via IDLE, double click on it or run it from console:

### Windows
```cmd
python File_preparation_CLI.py
```
or
```cmd
python3 ./File_preparation_CLI.py
```
or
```cmd
py ./File_preparation_CLI.py
```

### MacOS / Linux
```bash
python ./File_preparation_CLI.py
```
or
```bash
python3 ./File_preparation_CLI.py
```
or
```bash
python3.11 ./File_preparation_CLI.py
```

## Main menu
<img alt="Main_menu" src="https://github.com/Bauero/sim_racing_track_analysis/assets/65217796/4a0016de-6515-445a-baaf-2320d85c5b7b">


### Main Menu - options
In main menu you have 5 options
1. Allows to modify one file
2. Allows to cleanup multiple files
3. Allows to run cleanup for all files in specified directory
4. Changes how much information program display (for more info look below)
5. Allows to exit program from the interface

Whenever you modify one file or multiple you have access to options

### File cleanup options

When you choose option from main menu, you will have an option to modify default configuration of how file is processed.
<img 
  alt="Configuration_normal" 
  src="https://github.com/Bauero/sim_racing_track_analysis/assets/65217796/b9b5cd73-d728-48ed-a50e-60b43e6cc163">
<img 
  alt="Config_modyfication" 
  src="https://github.com/Bauero/sim_racing_track_analysis/assets/65217796/a048ee4a-3974-4848-b2b0-812c45cf3e11">


## Option 4 - verbose or not?

### Settings

<div style="display: flex">
  <div style="display: flex 1; text-align: center">
    <p>Not Verbose</p>
    <img style="display: block;
    margin-left: auto;
    margin-right: auto;" alt="Configuration_normal" src="https://github.com/Bauero/sim_racing_track_analysis/assets/65217796/b9b5cd73-d728-48ed-a50e-60b43e6cc163">
  </div>
  <div style="flex 1; text-align: center">
    <p>Verbose</p>
    <img style="display: block;
    margin-left: auto;
    margin-right: auto;" alt="Configuration_verbose" src="https://github.com/Bauero/sim_racing_track_analysis/assets/65217796/143eec84-6041-4063-8cee-ea8a24a7a227">
  </div>
</div>

### File Processing

<div style="display: flex">
  <div style="display: flex 1; text-align: center">
    <p>Not Verbose</p>
    <img style="display: block;
    margin-left: auto;
    margin-right: auto;" alt="Normal_file_processing" src="https://github.com/Bauero/sim_racing_track_analysis/assets/65217796/6cb40825-4bae-41b7-8f1c-5d24baf915f2">
  </div>
  <div style="flex 1; text-align: center">
    <p>Verbose</p>
    <img style="display: block;
    margin-left: auto;
    margin-right: auto;" alt="Verbose_file_processing" src="https://github.com/Bauero/sim_racing_track_analysis/assets/65217796/d5eef17e-adce-4d42-96be-6e5001216e8a">
  </div>
</div>
