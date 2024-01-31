import os
import tkinter as tk
from tkinter import filedialog
import dcm_org_module as dcm_org
import dicom_series_info_module as dsi
import series_mover_module as smm
import dicom_anonymizer_module as dcm_anon
import update_anon_settings  
import dicom_display_module as ddm
import csv
import shutil

def select_directory(title="Select Directory"):
    """
    Open a dialog to select a directory.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    directory = filedialog.askdirectory(title=title)
    root.destroy()
    return directory

def rename_files_in_output(csv_file_path, output_dir):
    study_name_mapping = {}

    with open(csv_file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header

        for row in reader:
            original_study_name = row[0]  # Assuming original study name is in the first column
            new_study_name = row[1]  # New study name is in the second column
            study_name_mapping[original_study_name] = new_study_name

    for study_name in os.listdir(output_dir):
        new_name = study_name_mapping.get(study_name)
        if new_name and os.path.exists(os.path.join(output_dir, study_name)):
            os.rename(os.path.join(output_dir, study_name), os.path.join(output_dir, new_name))

def empty_directory(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)


# Ask user to select input and output directories
input_dir = select_directory("Select Input Directory")
output_dir = select_directory("Select Output Directory")

# Constructing paths relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
temp_dir1 = os.path.join(script_dir, 'temp')
temp_dir2 = os.path.join(script_dir, 'temp2')
csv_path = os.path.join(script_dir, 'mapping_file.csv')  # Make sure this path is correct
settings_path = os.path.join(script_dir, 'anon_Settings.json')
print(csv_path)

if input_dir and output_dir:
    # Organize DICOM files
    dcm_org.organize_dicom_files(input_dir, temp_dir1)

    # Move specified series
    smm.process_studies(temp_dir1, temp_dir2, csv_path)

    # Update anonymization settings based on the CSV file
    update_anon_settings.read_csv_and_update_json(csv_path, settings_path)

    # Anonymize DICOM files
    # Save DICOM tags to CSV before anonymization
    ddm.save_dicom_tags_to_csv(temp_dir2, os.path.join(output_dir, 'DICOM_tags_before.csv'))
    
    dcm_anon.anonymize_directory(temp_dir2, output_dir, csv_path, settings_path)
    rename_files_in_output(csv_path, output_dir)
   # Save DICOM tags to CSV after anonymization
    ddm.save_dicom_tags_to_csv(output_dir, os.path.join(output_dir, 'DICOM_tags_after.csv'))
    
 # Display DICOM tags after anonymization






empty_directory(temp_dir1)
empty_directory(temp_dir2)