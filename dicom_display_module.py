import os
import random
import pydicom
import csv

def save_dicom_tags_to_csv(directory, output_csv_path):
    with open(output_csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['File', 'Tag', 'Tag Name', 'Value'])

        for study_name in os.listdir(directory):
            study_dir = os.path.join(directory, study_name)
            dicom_files = [os.path.join(root, file) for root, dirs, files in os.walk(study_dir) for file in files if file.lower().endswith(".dcm")]
            if dicom_files:
                random_dicom = random.choice(dicom_files)
                try:
                    ds = pydicom.dcmread(random_dicom)
                    for tag in ds.keys():
                        try:
                            tag_info = [random_dicom, str(tag), ds[tag].name, str(ds[tag].value)]
                            writer.writerow(tag_info)
                        except Exception as e:
                            writer.writerow([random_dicom, str(tag), 'Error', str(e)])
                except Exception as e:
                    writer.writerow([random_dicom, 'Error reading DICOM file', '', str(e)])
