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
import subprocess               # For running other cli tools and commands
import json                     # For json data handeling
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
desc = "******************************************************************************************\n\n  Subtitle Extractor by Shay Pasvolsky (C).\n\n******************************************************************************************"
# Input error vlaues
NSRC = "No_Source"  # Sorce path is not valid
Args_Arr = []           # Declare empty argumant array

# MKVToolNix path - Leave empty if you have the tools added to $PATH.
#   This is needed e.g. on macOS, if you downloaded MKVToolNix app
#   and just dragged it to the Applications folder.
MKVtoolPath = '/Applications/MKVToolNix-76.0.app/Contents/MacOS/'
# MKVTOOLS pathes
MKVMergePath = os.path.join(MKVtoolPath, "mkvmerge")
MKVExtractPath = os.path.join(MKVtoolPath, "mkvextract")

############################
# Argument Parser Settings #
############################

parser = argparse.ArgumentParser(description=desc,
                                 usage='%(prog)s [OPTIONS]', formatter_class=argparse.RawTextHelpFormatter)
# parser.add_argument('-V', '-v', '--Verbose', action='store_true',
#                    help="Show user masseges!", default=False)
parser.add_argument('-S', '-s', '--Source', required=True,
                    help="Source directory of the TV Show or Movie. Required to operate!")
parser.add_argument('--Version', '--version',
                    action='version', version='%(prog)s ' + Ver)
args = parser.parse_args()

# Build The argumant array for the system
Args_Arr.append(args.Source if (os.path.isdir(args.Source)
                or os.path.isfile(args.Source)) else NSRC)
# Args_Arr.append(args.Verbose)
# Args_Arr.append(args.Output)

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


def Get_Files_In_Path(Path):
    """
    Get all MKV and mp4 files from a folder and subfolders

    :param Path: path to the folder
    :return: Array of files
    """
    try:
        MediaFiles = []  # Place holder for the py files
        # Get the list of folders and files and loop threw it
        for (Root_dir, dirs, Files) in os.walk(Path, topdown=False):
            # Check if the folder has file(s) in it (starts with a .)
            if (Files):
                # Loop threw the files
                for File in Files:
                    # Check if the file name ends with .py
                    if (File.lower().endswith(".mkv") or File.lower().endswith(".mp4")):
                        # Save the file path to the arrays
                        MediaFiles.append(os.path.join(Root_dir, File))
        return MediaFiles
    except Exception as Error:
        return Error


def Get_Subtitle_Tracks(File):
    """
    Extract subtitle track data from a media file

    :param File: Media file path
    :return: ['track id', 'track codac']
    """
    try:
        TempData = ""       # Place holder for Json data
        TracksData = []     # Place holder for track data
        TrackData = []      # Place holder for track data
        # Extract Json data from the file
        TempData = json.loads((subprocess.run(
            [MKVMergePath, '-J', File], encoding='utf-8', stdout=subprocess.PIPE)).stdout)
        # loop threw Tracks in the Json
        for track in TempData['tracks']:
            # Check if track type is subtitles
            if (track['type'] == 'subtitles'):
                # Check if subtitle track is english
                if (track['properties']['language'] == "eng"):
                    # Check if subtitle track codac is SRT or ass
                    if (track['codec'] == "SubRip/SRT" or track['codec'] == "SubStationAlpha"):
                        # Save track number and track codac
                        TracksData.append([str(track['id']), track['codec']])
        # Check if array has more than one track
        if (len(TracksData) > 1):
            # loop threw the array to find the first srt track
            for track in TracksData:
                # check if track codac is SRT
                if (track[1] == "SubRip/SRT"):
                    # Add the track to the final list and stop the loop
                    TrackData.append([track[0], track[1]])
                    break
            # Make sure to have at least one track
            if (len(TrackData) < 1):
                # Add the first subtitle track to the final list
                TrackData.append([TracksData[0][0], TracksData[0][1]])
        else:
            # Return the data found if les than 2 tracks
            TrackData = TracksData
        return TrackData[0]
    except Exception as Error:
        return Error


def Extract_Subtitle_Track(File, SubFile, SubID):
    """
    Extract subtitle track from file

    :param File: Path to file to work on
    :param SubFile: path to new file
    :param SubID: Subtitle track id
    :return: True on success, Error on fail
    """
    try:
        # Run the extraction command
        subprocess.run([MKVExtractPath, 'tracks', File,
                       SubID + ":" + SubFile])
        return True
    except Exception as Error:
        return Error


def Remove_Unwanted_Tags(File):
    """
    Remove tags from srt file

    :param File: Path for the file to work on
    :return: True on success, Error on fail
    """
    try:
        # Read the file
        with open(File) as DataToModify:
            # Read the data
            DataToModify = DataToModify.read()
        # Remove tags
        DataToModify = re.sub(r'\<.*\>', '', DataToModify)
        # Save to file
        with open(File, "w") as f:
            f.write(DataToModify)
        return True
    except Exception as Error:
        return Error


#########
# Logic #
#########


def main(Args_Arr):
    """
    Main function
    """
    try:
        Files = []          # Place holder for the files to work on
        FileBaseName = ""   # Place holder for file base name
        SubArr = []         # Place holder for subtitle track info
        Ext = ""            # Place holder for subtitle extansion
        # TODO: Add verbose functionality and remove unwanted massages when extracting subtitles
        # Make sure the path is valid
        if (Args_Arr[0] != NSRC):
            # Check if an MKV or mp4 File
            if (os.path.isfile(Args_Arr[0]) and (Args_Arr[0].lower().endswith(".mkv") or Args_Arr[0].lower().endswith(".mp4"))):
                # Add the file to thr files to work on array
                Files.append(Args_Arr[0])
            # Check if the path is a folder
            elif (os.path.isdir(Args_Arr[0])):
                # Get all files to work on in the path
                Files = Get_Files_In_Path(Args_Arr[0])
            # Make sure at least one file was found
            if (Files):
                # Loop threw the files
                for File in Files:
                    # Extract file name without extension
                    FileBaseName = os.path.join(os.path.dirname(
                        File), (re.split(r'.mkv|.mp4', os.path.basename(File).lower())[0]))
                    # Get first srt subtitle track info (if available) or ASS (if available) and store
                    SubArr = (Get_Subtitle_Tracks(File))
                    # Set extention
                    if (SubArr[1] == "SubRip/SRT"):
                        Ext = ".srt"
                    elif (SubArr[1] == "SubStationAlpha"):
                        Ext = ".ass"
                    # Update the subtitle file name
                    FileBaseName = FileBaseName + Ext
                    # If subtitle tracks found extract it
                    Extract_Subtitle_Track(File, FileBaseName, SubArr[0])
                    # TODO: add convert ass to srt functionality
                    # Remove unwanted tags from srt file
                    if (SubArr[1] == "SubRip/SRT"):
                        Remove_Unwanted_Tags(FileBaseName)
        return True
    except Exception as Error:
        return Error


# Make sure to run only if called directly
if __name__ == "__main__":
    main(Args_Arr)
