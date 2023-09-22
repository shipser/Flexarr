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

import argparse                             # Import for the arguments handeling
import os                                   # OS base functions
from Functions.Base import *                # Import base functions
from Functions.ListFunctions import *       # Import list builder functions

############################
# Argument Parser Settings #
############################

# Declare empty argumant array
Args_Arr = []

parser = argparse.ArgumentParser(description=desc,
                                 usage='%(prog)s [OPTIONS]', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-L', '-l', '--LoadList',
                    help="Load external TV show and Movie list to select the correct one from it.", default="")
parser.add_argument('-V', '-v', '--Verbose', action='store_true',
                    help="Show user masseges!", default=False)
parser.add_argument('-S', '-s', '--Source', required=True,
                    help="Source directory of the TV Show or Movie. Required to operate!")
parser.add_argument('--Version', '--version',
                    action='version', version='%(prog)s ' + Ver)
args = parser.parse_args()

# Build The argumant array for the system
Args_Arr.append(args.Source if (os.path.isdir(args.Source)) else NSRC)
Args_Arr.append(args.Verbose)
Args_Arr.append(args.LoadList if (
    not os.path.isfile(args.LoadList)) else NList)

###############################
# Global Variables Defenition #
###############################

Files = ""
File = ""
FileData = []
Is4K = False
IsDub = False
IsMovieTV = ""
MediaName = ""
MediaNewPath = ""
MediaArray = []
MessageUser = ""
RecomandedLocation = ""
MessageUserTemp = ""
TempData = []
FinalList = []
TempLine = ""


###########################
# Do Not Change From Here #
###########################

def main(ArgsArr):
    """
    Main loop of the program

    :param Args_Arr: ArgsArr = Args_Arr
    :return: True on success, False on any error
    """
    # TODO: Add functionality to get imdb and tvdb data
    # TODO: Add the ability to overwrite existing file
    # TODO: Add the ability to build a list from current folder structure
    # TODO: Add 2 list merge functionality
    # TODO: Add counter (num of num) for progress
    # TODO: fix blank () and (
    # TODO: fix mishandaling folders in some cases
    # TODO: fix mishandaling file names in some cases
    try:
        # Message the user
        if (Args_Arr[1]):
            print("Checking if source folder is valid and if list does not exists.")
        # Check if source folder is valid folder and list does not exists
        if (Args_Arr[2] != NList and Args_Arr[0] != NSRC):
            # Message the user
            if (Args_Arr[1]):
                print("Source is valid and list does not exists!")
                print("Collecting media files in source directory.")
            # Get all files in the directory
            Files = GetFiles(Args_Arr[0])
            # Massage the user
            if (Args_Arr[1]):
                print("Files collected. starting to extract data from them.")
            # Loop threw all the files
            for File in Files:
                # Extract all the data
                FileData = Get_Movie_TV_Data(File)
                # Get Media Name, replace . with space
                MediaName = FileData[7].replace(".", " ")
                # Get Movie or TV
                IsMovieTV = FileData[1]
                # Add the year if it is a movie
                if (IsMovieTV == MedTy[1]):
                    MediaName = MediaName + " (" + FileData[8] + ")"
                # Get Resolution
                Is4K = (True if (FileData[10] == UHDRes[0]) else False)
                # Set to true if dubed
                IsDub = FileData[9]
                # Build the temp data array
                TempData.append([MediaName, IsMovieTV, Is4K, IsDub])
            # Maassage the user
            if (Args_Arr[1]):
                print("All media data extracted.")
                print("Sorting the data and filtering out duplicates.")
            # Sort the Data
            TempData.sort()
            # Get uniqe values and loop threw them
            for FileData in Get_Uniqe_Data(TempData):
                # Build the user message
                MessageUser = "Please select a path or type new one for the "
                # Add resolution part
                if (FileData[2]):
                    MessageUserTemp = UHDRes[0]
                else:
                    MessageUserTemp = "standart resolution"
                # Add dubed part
                if (FileData[3]):
                    MessageUserTemp = MessageUserTemp + " " + HeDub
                # Add tv or movie part
                MessageUserTemp = MessageUserTemp + " " + FileData[1]
                if (FileData[1] == MedTy[0]):
                    MessageUserTemp = MessageUserTemp + " show -"
                # Add media name part
                MessageUserTemp = MessageUserTemp + ' "' + FileData[0] + '": '
                # Merge the message
                MessageUser += MessageUserTemp
                # Find recomanded location
                RecomandedLocation = Get_Recomanded_Location(
                    FileData[2], FileData[3], FileData[1], PreSetPathes)
                # Ask the user to confirm the recomanded location
                if (not Confirm_Select('Do you want to use "{}" for {}'.format(RecomandedLocation, MessageUserTemp))):
                    # Get new path
                    MediaNewPath = inquirer.text(
                        message=MessageUser, completer=PreSetPathes, multicolumn_complete=True,).execute()
                    # Validate the path
                    if (not MediaNewPath.endswith("/")):
                        MediaNewPath = MediaNewPath + "/"
                else:
                    # Use the recomanded path
                    MediaNewPath = RecomandedLocation
                # Build the line to add to the list
                TempLine = FileData[0] + " : " + MediaNewPath
                # Add the data to the final list
                FinalList.append(TempLine)
            # Massage the user
            if (Args_Arr[1]):
                print('Finished building the list, writing to "{}"'.format(
                    Args_Arr[2]))
            # Create the file
            WriteNewList(Args_Arr[2], FinalList)
            # Massage the user
            if (Args_Arr[1]):
                print('Finished writing the list to "{}"'.format(Args_Arr[2]))
        return True
    except Exception as Error:
        print(Error)
        return False


# Make sure to run only if called directly
if __name__ == "__main__":
    main(Args_Arr)
