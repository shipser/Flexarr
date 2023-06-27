#!/usr/bin/env python3

##########################################################
##########################################################
## Writen By: Shay Pasvolsky | Jun 21st, 2023           ##
## Email: spasvolski@gmail.com                          ##
## GitHub: https://github.com/shipser                   ##
## Gitlab: @shipser                                     ##
## Licensce: GNU GPLv3                                  ##
##########################################################
##########################################################

###########
# Imports #
###########

import os                       # OS base functions
import argparse                 # Import for the arguments handeling
import re                       # For Regex Strings
# Includes for inquirerpy
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator


###############################
# Global Variables Defenition #
###############################

# Release number - Major.Minor.Fix, where fix can be uncomplited feature update
Ver = "1.0.0"
# Set help message for the cli
desc = "******************************************************************************************\n\n  TODO list builder by Shay Pasvolsky (C).\n\n******************************************************************************************"
# Input error vlaues
NSRC = "No_Source"                                  # Sorce path is not valid

FileList = []           # Place holder for the list of files to work on
FileListNoBase = []     # Place holder for the list of files to work on
Args_Arr = []           # Declare empty argumant array
SRC = ""                # Source location
Destination = ""        # Destination location
Verb = False            # Verbose place holfer


############################
# Argument Parser Settings #
############################

parser = argparse.ArgumentParser(description=desc,
                                 usage='%(prog)s [OPTIONS]', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-O', '-o', '--Output', required=True,
                    help="Output file location. Required to operate!")
parser.add_argument('-V', '-v', '--Verbose', action='store_true',
                    help="Show user masseges!", default=False)
parser.add_argument('-S', '-s', '--Source', required=True,
                    help="Source directory or file. Required to operate!")
parser.add_argument('--Version', '--version',
                    action='version', version='%(prog)s ' + Ver)
args = parser.parse_args()

# Build The argumant array for the system
Args_Arr.append(args.Source if (os.path.isdir(args.Source)
                or os.path.isfile(args.Source)) else NSRC)
Args_Arr.append(args.Verbose)
Args_Arr.append(args.Output)


#############################
#############################
##                         ##
## Do Not Change From Here ##
##                         ##
#############################
#############################


#############
# Functions #
#############


def TODOList(FromFile):
    """
    Extract a list of TODO items from a python file

    :param FromFile: source file to work on
    :return: string of line seperated todo's on success, "Error!!" on fail
    """
    try:
        Line_Num = 0  # Line counter
        ToDoArray = []  # Blank array for the todo's
        word = "TODO:"  # Word to search for in the lines
        with open(FromFile) as file:  # Open the file to use
            for line in file:  # Loop threw each line in the file
                Line_Num += 1  # Increment the line counter
                if word in line:  # Check for the word presence in the line
                    # Make sure not to add the delimiter defenition to the TODO list
                    if ("word = " not in line and "tab # TODO:" not in line):
                        # Appaned the line to the temporary array after constracting the string to save '(line number) tab # TODO: rest of the line after the it'
                        ToDoArray.append(
                            ("(" + str(Line_Num) + ")\t# To Do: " + line.split(word)[-1]).replace("\n", ""))
        # check if there is at least one TODO in the file
        if (len(ToDoArray) == 0):
            ToDoArray.append("No TODOs in this file!")
        # Convert the array to string with line brackers and return the result
        return '\n'.join(ToDoArray)
    except:
        return "Error!!"


def SaveToFile(TODOFile, DataToSave):
    """
    Save data to a file

    :param TODOFile: Path to the file to save to
    :param DataToSave: Data to save to the file
    :return: True on success, Error code on fail
    """
    try:
        # Open the file in write mode
        with open(TODOFile, "w") as file:
            # Write the data to the file
            file.write(DataToSave)
        return True
    except Exception as Error:
        return Error


def GetPyFiles(srcpath):
    """
    Get all python files in the source directory
    """
    try:
        PyFiles = []  # Place holder for the py files
        # Verify path is a folder and exists
        if (os.path.isdir(srcpath)):
            # Get the list of folders and files and loop threw it
            for (Root_dir, dirs, Files) in os.walk(srcpath, topdown=False):
                # Check if the folder has file(s) in it (starts with a .)
                if (Files):
                    # Loop threw the files
                    for File in Files:
                        # Check if the file name ends with .py
                        if (File.lower().endswith(".py")):
                            # Make sure to ignore __init__.py files and itself
                            if (os.path.basename(File) != "__init__.py" and os.path.basename(File) != os.path.basename(__file__)):
                                # Save the file path to the arrays
                                PyFiles.append([os.path.join(Root_dir, File), os.path.join(re.split(
                                    r'/', srcpath)[-2], re.split(srcpath, os.path.join(Root_dir, File))[-1])])
        return PyFiles
    except Exception as Error:
        return [False, Error]


def Create_Massage_To_Save(File, Prefix_Length):
    """
    Create the massage to save to the file

    :param File: File path to read data from and build the massage for
    :return: Massage to save
    """
    try:
        Massage = ""    # Place holder for the massage to return
        Mass_Prefix = ""    # Prefix for the file data
        Mass_Suffix = ""    # Suffix for the file data
        # Build the prefix of the massage
        Mass_Prefix = "##### " + int((Prefix_Length - len(File[1])) / 2) * " " + \
            File[1] + (int((Prefix_Length - len(File[1]))) -
                       int((Prefix_Length - len(File[1])) / 2)) * " " + " #####\n\n"
        # Build  the suffix of the massage
        Mass_Suffix = "\n\n" + "#" * (Prefix_Length + 12) + "\n"
        # Build the final massage to return
        Massage = Mass_Prefix + TODOList(File[0]) + Mass_Suffix
        return Massage
    except Exception as Error:
        return Error


def MaxMassageLen(Files):
    """
    Get max length of file pathes

    :param Files: File path array
    :return: Max length
    """
    try:
        MaxLength = 0  # Place holder for the max length
        # Loop threw the file array
        for File in Files:
            # Check if the file path length is higher then the current max
            if (len(File[1]) > MaxLength):
                # Set the max length to the current length
                MaxLength = len(File[1])
        return MaxLength
    except Exception as Error:
        return Error


# Input selector
def Confirm_Select(MessageUser):
    """
    Load the media list

    depends on:
        imports:
            InquirerPy

    :param MessageUser: Question to display.
    :return: User choice
    """
    proceeed = False
    proceeed = inquirer.confirm(
        message=MessageUser,
        default=False,
    ).execute()
    return proceeed


#########
# Logic #
#########


def main(Args_Arr):
    """
    Main function
    """
    # TODO: Add functionality to create TODO list without empty files.
    try:
        # Get verbose state
        Verb = Args_Arr[1]
        # Make sure the source is valid and output file path is not empty
        if (Args_Arr[0] != NSRC and Args_Arr[2] != ""):
            SRC = Args_Arr[0]  # Store the source location
            Destination = Args_Arr[2]  # Store the destination path
            DataToSaveToFile = ""   # Place holder for text to write
            # Check if user wants to see massages
            if (Verb):
                print("Source is valid and destination provided!")
            # check if source is a file or a folder
            if (os.path.isdir(SRC)):
                # Check if user wants to see massages
                if (Verb):
                    print(
                        "Source is a directory, collecting all th python files in it!")
                # Get a list of files to work on
                FileList = GetPyFiles(SRC)
                # Get max length
                MaxLength = MaxMassageLen(FileList)
                # Check if the list is not empty
                if (FileList != [] and FileList[0] != False):
                    # Check if user wants to see massages
                    if (Verb):
                        print("Found python files, checking for TODOs in them!")
                    # Loop threw the files
                    for File in FileList:
                        # Add data from the file to the string to save
                        DataToSaveToFile = DataToSaveToFile + \
                            Create_Massage_To_Save(
                                File, MaxLength) + "\n"
                    # Check if user wants to see massages
                    if (Verb):
                        print("Finished collecting TODOs!")
            elif (os.path.isfile(SRC)):
                # Check if user wants to see massages
                if (Verb):
                    print("Source is a file, collecting TODOs in it!")
                # Build the massage to save for single file
                DataToSaveToFile = Create_Massage_To_Save(SRC, len(SRC))
                # Check if user wants to see massages
                if (Verb):
                    print("Finished collecting TODOs!")
            # Check if destination is not a folder
            if (not os.path.isdir(Destination)):
                # Check if user wants to see massages
                if (Verb):
                    print("Destination is valid, continueing to save!")
                # Check if destination is a file already existing
                if (not os.path.isfile(Destination)):
                    # Save to file
                    SaveToFile(Destination, DataToSaveToFile)
                    # Check if user wants to see massages
                    if (Verb):
                        print("Finished saveing, Exiting!")
                else:
                    if (Confirm_Select("File already exists, Do you want to override it?")):
                        # Save to file
                        SaveToFile(Destination, DataToSaveToFile)
                        # Check if user wants to see massages
                        if (Verb):
                            print("Finished saveing, Exiting!")
                    else:
                        # Check if user wants to see massages
                        if (Verb):
                            print("Aborting, data will not be saved!")
            else:
                # Check if user wants to see massages
                if (Verb):
                    print("Destination is not valid, quiting!")
        else:
            # Check if user wants to see massages
            if (Verb):
                print("Source is not valid or Destination is not provided!")
        return True
    except Exception as Error:
        print(Error)
        return Error


# Make sure to run only if called directly
if __name__ == "__main__":
    main(Args_Arr)
