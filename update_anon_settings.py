import csv
import json
import os

def read_csv_and_update_json(csv_file_path, json_file_path):
    with open(csv_file_path, 'r') as csv_file:

        print(csv_file_path,"anon set upd")

        reader = csv.reader(csv_file)
        next(reader)  # Skip the header

        for row in reader:
            new_study_id = row[2]
            date_control = row[3].strip().lower() == "true"
            new_date = row[4].replace('-', '') if row[4] else '19700101'

            update_json_settings(json_file_path, new_study_id, date_control, new_date)



def update_json_settings(json_file_path, new_study_id, date_control, new_date):
    print(f"Updating JSON settings file: {json_file_path}")  # Add this line for debugging
    with open(json_file_path, 'r') as json_file:
        try:
            settings = json.load(json_file)
        except json.decoder.JSONDecodeError as e:
            print(f"Error in JSON file format: {e}")
            return  # Add error handling
