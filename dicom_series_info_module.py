# dicom_series_info_module.py
import os
import pydicom

def is_dicom_file(file_path):
    try:
        pydicom.dcmread(file_path, stop_before_pixels=True)
        return True
    except:
        return False

def get_series_info(study_dir):
    series_info = []
    for root, dirs, files in os.walk(study_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if is_dicom_file(file_path):
                try:
                    ds = pydicom.dcmread(file_path, stop_before_pixels=True)
                    if hasattr(ds, 'SeriesNumber'):
                        series_number = ds.SeriesNumber
                        series_info.append({'series_number': series_number, 'series_path': root})
                        # Once we find one DICOM file in a series, we can skip the rest
                        break
                except Exception as e:
                    print(f"Error reading DICOM file {file_path}: {e}")
    return series_info

def process_studies(base_dir):
    all_studies_info = []
    for study_name in os.listdir(base_dir):
        study_dir = os.path.join(base_dir, study_name)
        if os.path.isdir(study_dir) and study_name != "UnknownSeries":
            study_info = get_series_info(study_dir)
            if study_info:
                all_studies_info.append({'study_name': study_name, 'series_info': study_info})
    return all_studies_info
