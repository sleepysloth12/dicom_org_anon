

# DICOM Organizer and Anonymizer (dicom_org_anon)

The `dicom_org_anon` application is designed to organize, anonymize, and process DICOM (Digital Imaging and Communications in Medicine) files. This guide will walk you through installing and using the application.

by Jean Jimenez @sleepysloth12

## Installation

### Prerequisites

Ensure you have Python installed on your system. Python 3.6 or newer is recommended. You can download Python from [python.org](https://www.python.org/downloads/).

### Steps to Install

1. **Download the Application**: Obtain the `dicom_org_anon` application package. This may be provided to you as a `.zip` file or a link to download it.

2. **Extract the Package**: If the application is in a `.zip` file, extract it to a folder of your choice.

3. **Install the Application**:
   - Open a command prompt or terminal window.
   - Navigate to the folder where you extracted `dicom_org_anon`.
   - Run the following command:

     ```sh
     pip install .
     ```

   - This command installs the application and its dependencies.

### Create Executable (Optional)

If you want to use the application without running Python scripts, you can create an executable:

- In the command prompt or terminal, navigate to the `dicom_org_anon` folder.
- Run the following command:

  ```sh
  pyinstaller --onefile main.py
  ```

- After the process completes, you will find an executable file in the `dist` folder.

## Usage

### Running the Application

- **Through Python Script**:
  - Navigate to the `dicom_org_anon` folder in the command prompt or terminal.
  - Run the script using:

    ```sh
    python main.py
    ```

- **Using the Executable**:
  - Simply double-click the executable file created earlier (found in the `dist` folder).

### Application Workflow

1. **Select Input and Output Directories**:
   - Upon running, the application will prompt you to select the input directory (where your DICOM files are located) and the output directory (where you want the processed files to be saved).

2. **Processing**:
   - The application will organize and anonymize your DICOM files based on the settings and instructions provided in the `mapping_file.csv` and `anon_Settings.json` files.
   - It will then save information about DICOM tags before and after processing in CSV files within the output directory.

3. **Review Output**:
   - Check the output directory for organized and anonymized DICOM files.
   - Review the `DICOM_tags_before.csv` and `DICOM_tags_after.csv` files for a summary of the DICOM tags.

### Configuring the Application

- Modify the `mapping_file.csv` and `anon_Settings.json` files in the `dicom_org_anon` folder to change how the application organizes and anonymizes the DICOM files.
- The `mapping_file.csv` controls how files are renamed and organized.
- The `anon_Settings.json` file specifies which DICOM tags are anonymized or altered.

---

## Troubleshooting

- **Application Doesn't Start**: Ensure Python is correctly installed and that all dependencies are installed using `pip install .`.
- **Errors During Execution**: Check the console output for any error messages. These messages can provide clues about what might be going wrong.

