# series_mover_module.py
import os
import shutil
import csv
import dicom_series_info_module as dsi

def read_series_mapping(file_path):
    series_mapping = {}
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header
        for row in reader:
            study_name = row[0]
            series_list_str = row[5]  # 6th column contains the series list
            series_list = series_list_str.split(',')
            series_mapping[study_name] = [int(s.strip()) for s in series_list]
    return series_mapping

def find_series_path(all_studies_info, study_name, series_number):
    for study in all_studies_info:
        if study['study_name'] == study_name:
            for series in study['series_info']:
                if series['series_number'] == series_number:
                    return series['series_path']
    return None

def move_series(temp_dir1, temp_dir2, series_mapping, all_studies_info):
    for study, series_numbers in series_mapping.items():
        study_destination_path = os.path.join(temp_dir2, study)
        if not os.path.exists(study_destination_path):
            os.makedirs(study_destination_path)

        for series_number in series_numbers:
            series_path = find_series_path(all_studies_info, study, series_number)
            if series_path:
                series_name = os.path.basename(series_path)
                destination_path = os.path.join(study_destination_path, series_name)
                if os.path.exists(series_path) and not os.path.exists(destination_path):
                    shutil.copytree(series_path, destination_path)

def process_studies(temp_dir1, temp_dir2, mapping_file):
    all_studies_info = dsi.process_studies(temp_dir1)
    series_mapping = read_series_mapping(mapping_file)
    move_series(temp_dir1, temp_dir2, series_mapping, all_studies_info)
