"""
Project module that displays skills using Git version control, managing Python virtual environments, and fetching, handling, and writing processed data from the web to files 
"""

# Importing dependencies 

# Standard library imports 
import csv
from pathlib import Path
import json

# External library imports (using virtual environment)
import requests
import pandas as pd
import openpyxl

# Local module imports
import dgraves_utils
import dgraves_projsetup

# Define function to create necessary data directories

def create_directories():
    folder_names = ['data-txt', 'data-csv', 'data-excel', 'data-json']
    for folder_name in folder_names:
        path = Path(folder_name)
        path.mkdir(exist_ok=True)  # 'exist_ok=True' prevents an error if the directory already exists

# Define functions for data aquisition of each file type

def fetch_and_write_txt_data(folder_name, filename, url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            write_txt_file(folder_name, filename, response.text)
        else:
            print(f"Failed to fetch data: {response.status_code}")
    
    # Implement an exception handling example with txt data:
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")

def fetch_and_write_csv_data(folder_name, filename, url):
    response = requests.get(url)
    if response.status_code == 200:
        write_csv_file(folder_name, filename, response.text)
    else:
        print(f"Failed to fetch CSV data: {response.status_code}")

def fetch_and_write_excel_data(folder_name, filename, local_path):
    try:
        # Read the Excel file directly using pandas
        df = pd.read_excel(local_path)
        # Write the DataFrame to the specified folder and filename
        write_excel_file(folder_name, filename, df)
    except Exception as e:  #Exception for errors
        print(f"An unexpected error occurred: {e}")

def fetch_and_write_json_data(folder_name, filename, url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            write_json_file(folder_name, filename, json_data)
        else:
            print(f"Failed to fetch JSON data: {response.status_code}")
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")

# Define functions to write data for file types

def write_txt_file(folder_name, filename, data):
    file_path = Path(folder_name).joinpath(filename)
    with file_path.open('w') as file:
        lines = data.split('\n')
        romeo_lines = [line for line in lines if line.strip().lower().startswith('romeo')]
        file.write('\n'.join(romeo_lines))
        print(f"Text data (lines starting with 'romeo') saved to {file_path}")

def write_csv_file(folder_name, filename, data):
    file_path = Path(folder_name).joinpath(filename)
    with file_path.open('w', newline='') as file:
        file.write(data)
        print(f"CSV data saved to {file_path}")

def write_excel_file(folder_name, filename, data):
    file_path = Path(folder_name).joinpath(filename)
    try:
        # Check if the data is a DataFrame
        if isinstance(data, pd.DataFrame):
            # Write DataFrame to Excel
            data.to_excel(file_path, index=False)
            print(f"Excel data saved to {file_path}")
        else:
            print("Invalid data type. Expected DataFrame.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def write_json_file(folder_name, filename, data):
    file_path = Path(folder_name).joinpath(filename)
    with file_path.open('w') as file:
        json.dump(data, file, indent=2)
        print(f"JSON data saved to {file_path}")

# Process Data and Generate Output Functions

def process_txt_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        romeo_lines_count = sum(1 for line in lines if line.strip().lower().startswith('romeo'))

    with open(output_file, 'w') as result_file:
        result_file.write(f"Number of lines spoken by Romeo: {romeo_lines_count}")

def process_csv_file(input_file, output_file):
    with open(input_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        country_counts = {}

        for row in csv_reader:
            country = row.get('Country')

            if country:
                country_counts[country] = country_counts.get(country, 0) + 1

    with open(output_file, 'w') as result_file:
        result_file.write("Number of Customers per Country:\n")
        for country, count in country_counts.items():
            result_file.write(f"{country}: {count}\n")

def process_excel_file(input_file, output_file):
    try:
        print(f"Reading Excel file: {input_file}")
        df = pd.read_excel(input_file, engine='openpyxl')
        print("Read successful.")

        # Check if 'q1', 'q2', and 'q3' columns are present
        if 'q1' in df.columns and 'q2' in df.columns and 'q3' in df.columns:
            # Calculate averages for 'q1', 'q2', and 'q3'
            average_q1 = df['q1'].mean()
            average_q2 = df['q2'].mean()
            average_q3 = df['q3'].mean()

            # Save the averages generated to output file
            with open(output_file, 'w') as result_file:
                result_file.write(f"Average Q1: {average_q1}\nAverage Q2: {average_q2}\nAverage Q3: {average_q3}\n")
                print(f"Averages for 'q1', 'q2', and 'q3' saved to {output_file}")
        else:
            print("Required columns not found in the Excel file.")
    except pd.errors.EmptyDataError:
        print("Empty Excel file. No data to process.")
    except pd.errors.ParserError as e:
        print(f"Error parsing Excel data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
def process_json_file(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            json_data = json.load(file)

            if 'objects' in json_data:
                representatives = json_data['objects']

                if not representatives:
                    print("No representatives found in JSON data.")
                    return

                # Create a dictionary to store the count of representatives per state
                state_rep_count = {}

                for rep in representatives:
                    if 'state' in rep:
                        state = rep['state']
                        state_rep_count[state] = state_rep_count.get(state, 0) + 1

                with open(output_file, 'w') as result_file:
                    for state, count in state_rep_count.items():
                        result_file.write(f"State: {state}, Representatives Count: {count}\n")

                    print(f"State-wise representative count saved to {output_file}")
            else:
                print("Invalid JSON format. 'objects' key not found.")
    except Exception as e:
        print(f"An error occurred while processing JSON file: {e}")

# Main Function
def main():
    print(f'Byline: {dgraves_utils.byline}')

    # Create needed directories
    create_directories()

    # Example data URLs
    txt_url = 'https://www.gutenberg.org/cache/epub/1513/pg1513.txt'
    csv_url = 'https://media.githubusercontent.com/media/datablist/sample-csv-files/main/files/customers/customers-100.csv'
    excel_url = 'C:/Users/derek/Downloads/demand.xls'
    json_url = 'https://www.govtrack.us/api/v2/role?current=true&role_type=representative&limit=438'

    # Folder names for data types
    txt_folder_name = 'data-txt'
    csv_folder_name = 'data-csv'
    excel_folder_name = 'data-excel'
    json_folder_name = 'data-json'

    # File names for data types
    txt_filename = 'data.txt'
    csv_filename = 'data.csv'
    excel_filename = 'data.xlsx'
    json_filename = 'data.json'

    # Fetch and write data
    fetch_and_write_txt_data(txt_folder_name, txt_filename, txt_url)
    fetch_and_write_csv_data(csv_folder_name, csv_filename, csv_url)
    fetch_and_write_excel_data(excel_folder_name, excel_filename, r'C:\Users\derek\Downloads\demand.xls')  #using local drive for compatibility issue with excel file
    fetch_and_write_json_data(json_folder_name, json_filename, json_url)

    # Process data
    process_txt_file(Path(txt_folder_name).joinpath(txt_filename), Path(txt_folder_name).joinpath('results_txt.txt'))
    process_csv_file(Path(csv_folder_name).joinpath(csv_filename), Path(csv_folder_name).joinpath('results_csv.txt'))
    process_excel_file(Path(excel_folder_name).joinpath(excel_filename), Path(excel_folder_name).joinpath('results_excel.txt'))
    process_json_file(Path(json_folder_name).joinpath(json_filename), Path(json_folder_name).joinpath('results_json.txt'))


if __name__ == "__main__":
    main()

