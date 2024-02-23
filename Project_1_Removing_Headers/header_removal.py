"""
Title: Automate the Boring Stuff Chapter 16, Project 1
Purpose: Remove headers from CSV files
Author: drstrangelove4 
"""


import csv
from os import listdir
from os.path import isfile, join
import os
import shutil
from pprint import pprint

CWD = os.getcwd()
NEW_DIR_NAME = "old"
PREFIX = "_new_"

# -----------------------------------------------------------------------------------------------------------------------


def get_csv_paths(directory_path):
    """
    Take a directory path as input and returns a list of CSV file names in the current working directory.
    """

    # Get all the CSV files at a path.
    return [
        file
        for file in listdir(directory_path)
        if ".csv" in file and isfile(join(directory_path, file))
    ]


# -----------------------------------------------------------------------------------------------------------------------


def get_csv_object(csv_path):
    """
    Takes a path to a CSV file as an input and returns a CSV reader object.
    """

    # Just opens a file and returns a reader from it.
    csv_file = open(csv_path)
    return csv.reader(csv_file)


# -----------------------------------------------------------------------------------------------------------------------


def remove_header(csv_reader_object, csv_path, prefix):
    """
    Takes a CSV object as input and returns an object without a header.
    """
    # Skip the first row, which is the header
    not_first_row = False

    # Create a new csv to store the edited data
    with open(f"{prefix}{csv_path}", "w", newline="") as file:
        csv_writer = csv.writer(file)

        # Skip the header and record the rest of the data.
        for row in csv_reader_object:
            if not_first_row:
                csv_writer.writerow(row)
            not_first_row = True


# -----------------------------------------------------------------------------------------------------------------------


def move_old(csv_path, current_directory, new_directory_name):
    """
    Creates a new directory for the old files and moves them there.
    """

    # Create the directory by joining the current dir passed to function and a new name.
    old_files = join(current_directory, new_directory_name)

    # A lazy way of dealing with an existing 'old' folder
    try:
        os.mkdir(old_files)
    except Exception as _:
        pass

    # Move the files to the new dir
    shutil.move(csv_path, join(old_files, csv_path))


# -----------------------------------------------------------------------------------------------------------------------


def rename_new(csv_name, replace):
    """
    Renames the new file to the old file name
    """

    new_name = csv_name.replace(replace, "")
    os.rename(csv_name, new_name)


# -----------------------------------------------------------------------------------------------------------------------


def main():
    csv_files = get_csv_paths(CWD)

    if csv_files:
        pprint(f"The following CSV files have been found:\n{csv_files}")

        # Loop through csvs in path
        for csv_file in csv_files:
            # Get create a reader object from the file at path
            csv_reader = get_csv_object(csv_file)

            # Saves a new file that is a csv without a header
            remove_header(csv_reader, csv_file, PREFIX)

            # Move the old files to a new directory
            move_old(csv_file, CWD, NEW_DIR_NAME)

        # Get the new file names
        new_csv_files = get_csv_paths(CWD)

        # Rename them
        for csv_file in new_csv_files:
            rename_new(csv_file, PREFIX)

        print(
            f"\nCSV headers have been removed. Old files are stored in the 'old' folder at:\n{CWD}/old"
        )

    else:
        raise Exception("No CSV files have been found.")


# -----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    main()
