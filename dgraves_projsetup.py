"""
This module uses functions to create a series of project folders using loops and branching.
"""

# Imports from Python Standard Library
import pathlib
import math
import statistics
import time
import os  
import dgraves_utils

# Define create_project_directory function
def create_project_directory(directory_name: str):
    """
    Creates a project folder.
    :param directory_name: Folder name to be created.
    """
    # Creates a new directory with pathlib
    new_directory = pathlib.Path.cwd().joinpath(directory_name)
    # Checks for preexisting directory, otherwise creates directory 
    new_directory.mkdir(exist_ok=True)
    print(f"Directory '{directory_name}' {'created successfully.' if not new_directory.exists() else 'already exists.'}")

# Define create_annual_directories range function
def create_annual_directories(directory_name: str, start_year: int, end_year: int):
    """
    Creates annual directories within a project folder for a given range of years.
    :param directory_name: Folder name to be created.
    :param start_year: First year to be created.
    :param end_year: Last year to be created.
    """
    create_project_directory(directory_name)

    for year in range(start_year, end_year + 1):
        year_directory = pathlib.Path(directory_name).joinpath(str(year))
        create_project_directory(year_directory)
        print(f"Created {year_directory}")

# Define create_folders_from_list function
def create_folders_from_list(folder_list: list, base_directory: str, to_lowercase=True, remove_spaces=True):
    """
    Create folders from a list of names.
    :param folder_list: A list of folder names.
    :param base_directory: The base directory where folders will be created.
    :param to_lowercase: If True, converts folder names to lowercase.
    :param remove_spaces: If True, removes spaces from folder names.
    """
    base_path = pathlib.Path(base_directory)

    for folder_name in folder_list:
        folder_check = folder_name

        # Conditional formatting for spaces and capitalization 
        if to_lowercase and remove_spaces:
            folder_check = folder_check.replace(' ', '')  
            folder_check = folder_check.lower()  

        folder_path = base_path.joinpath(folder_check)
        # Creates folder if it doesn't exist
        folder_path.mkdir(exist_ok=True)
        print(f"Folder '{folder_name}' created successfully at {folder_path}")


# Define create_prefixed_folders function
def create_prefixed_folders(folder_list, prefix, base_directory):
    """
    Create prefixed folders.
    :param folder_list: A list of folder names.
    :param prefix: The prefix to be added to each folder name.
    :param base_directory: The base directory where folders will be created.
    :return: A list containing the paths of the created folders.
    """
    base_path = pathlib.Path(base_directory)

    if prefix:
        folders = (base_path.joinpath("data_source", prefix + folder_name) for folder_name in folder_list)
    else:
        folders = (base_path.joinpath("data_source", folder_name) for folder_name in folder_list)

    for folder_path in folders:
        folder_path.mkdir(parents=True, exist_ok=True)
    return folders

# Folder name prefixes defined
prefixed_folder_names = ('raw', 'processed', 'archived', 'internal', 'external', 'test')
prefix = 'source-'

# Define create_folders_periodically function
def create_folders_periodically(duration, folder_name_prefix, num_folders):
    """
    Create folders periodically at a specified time interval
    :param duration: Time interval in seconds between folder creations.
    :param folder_name_prefix: Prefix for the folder names.
    :param num_folders: Number of folders to create.
    """

    base_path = pathlib.Path.cwd()
    # Defines the folder to monitor for creation of new folders
    folder_to_monitor = base_path / "data_import_intervals"
    known_folders = set(os.listdir(folder_to_monitor))

    # Loop to monitor the directory and create folders every time interval 
    while True:
        current_folders = set(os.listdir(folder_to_monitor))
        new_folders = current_folders - known_folders

        if new_folders:
            for new_folder in list(new_folders)[:num_folders]:  # Limit the number of created folders
                folder_path = folder_to_monitor / new_folder
                folder_path.mkdir(exist_ok=True)
                print(f"Folder '{new_folder}' created successfully at {folder_path}")

            known_folders = current_folders

        # Loop function monitors directory and creates folders at intervals (seconds)
        time.sleep(duration)

def main():
    """
    Main function 
    Calls the variables and functions defined to create folders and display byline from imported module
    """
    # Prints byline function from dgraves_utils module
    print(f'Byline: {dgraves_utils.byline}')

    # Calls function to create annual sub-directories under employee_data folder
    create_annual_directories(directory_name='employee_data', start_year=2021, end_year=2024)
   
    # Gives list of folder names to be created
    folder_names_to_create = ('data_source', 'data_import_intervals')
    
    # Specifies the base directory to create folders in
    base_dir = r"C:\Users\derek\OneDrive\Documents\44608 Data Analytics Fundamentals\Mod 2\datafun-02-projects"
  
    # Calls function to create folders from list
    create_folders_from_list(folder_names_to_create, base_directory=base_dir)
   
    # Establishes prefixes for prefixed folder names and calls function to create them
    prefixed_folder_names = ('raw', 'processed', 'archived', 'internal', 'external', 'test')
    prefix = 'source-'
    create_prefixed_folders(prefixed_folder_names, prefix, base_directory=base_dir)
    
    # Calls function to check for and create folders per 10 sec time intervals limited to quantity 5
    create_folders_periodically(duration_secs=10, num_folders=5)

# Call the main function
if __name__ == "__main__":
    main()

