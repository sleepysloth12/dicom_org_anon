# dicom_anonymizer_module.py
import os
import csv
import pydicom
import json

def read_csv_mapping(file_path):
    mapping = {}
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header
        for row in reader:
            mapping[row[0]] = row[1]
    return mapping

def read_anonymization_settings(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def anonymize_dicom(dicom, settings):
    for tag_str, value in settings.items():
        tag_tuple = tuple(int(x, 16) for x in tag_str.split(","))
        if tag_tuple in dicom:
            if dicom[tag_tuple].VR == 'SQ':  # Sequence
                dicom[tag_tuple].value = pydicom.sequence.Sequence([])
            elif dicom[tag_tuple].VR in ['AS', 'DS']:  # Age String, Decimal String
                dicom[tag_tuple].value = '000Y' if dicom[tag_tuple].VR == 'AS' else '0'
            elif value == "HASH" and dicom[tag_tuple].VR == 'DA':  # Date
                dicom[tag_tuple].value = '19700101'
            else:
                dicom[tag_tuple].value = value

def anonymize_directory(temp_dir2, output_dir, csv_path, settings_path):
    mapping = read_csv_mapping(csv_path)
    settings = read_anonymization_settings(settings_path)
    
    for study_name in os.listdir(temp_dir2):
        renamed_study = mapping.get(study_name, study_name)
        study_dir = os.path.join(temp_dir2, study_name)
        output_study_dir = os.path.join(output_dir, renamed_study)
        
        os.makedirs(output_study_dir, exist_ok=True)
        
        for series in os.listdir(study_dir):
            series_dir = os.path.join(study_dir, series)
            output_series_dir = os.path.join(output_study_dir, series)
            
            if not os.path.isdir(series_dir):
                continue
            
            os.makedirs(output_series_dir, exist_ok=True)
            
            for dicom_file in os.listdir(series_dir):
                dicom_path = os.path.join(series_dir, dicom_file)
                
                if not os.path.isfile(dicom_path):
                    continue
                
                dicom = pydicom.dcmread(dicom_path)
                anonymize_dicom(dicom, settings)
                
                output_path = os.path.join(output_series_dir, dicom_file)
                dicom.save_as(output_path)
