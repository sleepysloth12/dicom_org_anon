# dcm_org_module.py
import os
import shutil
import pydicom
from concurrent.futures import ThreadPoolExecutor

def is_dicom_file(file_path):
    try:
        pydicom.dcmread(file_path, stop_before_pixels=True)
        return True
    except:
        return False

def get_series_description(file_path):
    try:
        ds = pydicom.dcmread(file_path, stop_before_pixels=True)
        return ds.SeriesDescription
    except:
        return "UnknownSeries"

def handle_file(file_path, temp_subdir):
    if not os.path.exists(temp_subdir):
        os.makedirs(temp_subdir)

    new_file_path = file_path
    if not file_path.endswith('.dcm'):
        new_file_path = file_path.rsplit('.', 1)[0] + '.dcm'
        shutil.move(file_path, new_file_path)
    temp_file_path = os.path.join(temp_subdir, os.path.basename(new_file_path))
    shutil.copy(new_file_path, temp_file_path)

def process_directory(dir_path, temp_dir1):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(('.dcm', '.ima')) or 'DICOMDIR' in file or is_dicom_file(file_path):
                series_description = get_series_description(file_path)
                parts = os.path.relpath(root, dir_path).split(os.sep)
                parts[-1] = series_description
                new_temp_dir = os.path.join(temp_dir1, *parts)
                handle_file(file_path, new_temp_dir)

def organize_dicom_files(input_dir_path, temp_dir1):
    if not os.path.exists(temp_dir1):
        os.makedirs(temp_dir1)

    with ThreadPoolExecutor() as executor:
        executor.submit(process_directory, input_dir_path, temp_dir1)

    print("Finished processing.")
