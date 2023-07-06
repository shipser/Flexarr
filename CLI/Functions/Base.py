#!/usr/bin/env python3

###########
# Imports #
###########

import os                               # OS base functions
import re                               # For Regex Strings
from Config.Params import *             # Import configurations
import shutil                           # For copy file operations
from Functions.Logger import *          # Import logger functions

# Includes for inquirerpy
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator


# Get files list inside the path
def GetFiles(src):
    """
    Get all media file paths in the source folder.

    depends on:
        imports:
            os

    :param src: Media folder path to work on.
    :return: [File path array] if found at least one file, [NFiles] if no files found, [FGFiles] on any error.
    """
    try:
        Show_Files = []  # Declare blank show file array
        # Make sure path ends with /
        if (not src.lower().endswith("/")):
            src = src + "/"
        # Get Files
        Show_Files = [os.path.join(root, name) for root, dirs, files in os.walk(
            src) for name in files if name.lower().endswith(MFsfx + SFsfx + EFsfx)]
        # Make sure files were found, if not reset the list
        if (len(Show_Files) == 0):
            Show_Files.append(NFiles)
        # Return what was found
        return Show_Files
    except:
        # return an error
        return [FGFiles]


# Extract all media infro from the file name
def Get_Movie_TV_Data(FilePath):
    """
    Extract all possible info from the file name and path

    depends on:
        imports:
            os
            re

    :param FilePath: Media folder path to work on.
    :return: [File path array] if found at least one file, [NFiles] if no files found, [FGFiles] on any error.
    """
    try:
        # Initialize Season and Episode placeholders
        Seas = ""
        Epi = []
        MedT = ""
        MedName = ""
        MedYear = ""
        HebDub = False
        MedRes = SDRes
        deli = ""
        FileT = ""
        # Get the file name from the path
        FileName = os.path.splitext(os.path.basename(FilePath))[0]
        # Get the folder containing the file
        FileDir = os.path.dirname(FilePath)
        # Get file extention
        FileExt = os.path.splitext(FilePath)[-1]
        # Set File Type
        if (FileExt in MFsfx):  # Movie
            FileT = MedFType[0]
        elif (FileExt in SFsfx):  # Subtitle
            FileT = MedFType[1]
        elif (FileExt in EFsfx):  # Extra like nfo or image
            FileT = MedFType[2]
        else:  # Unkown
            FileT = MedFType[3]
        # Get HebDub
        HebDub = True if (
            (re.search(r'hebdub', FileName, flags=re.IGNORECASE)) != None) else False
        # Build the delimiter for resolution search
        for de in UHDRes:
            if (deli == ""):
                deli = de
            else:
                deli = deli + "|" + de
        # Extract media resulution
        if (re.search(deli, FileName, flags=re.IGNORECASE)):
            MedRes = UHDRes[0]
        # Check if the file name has SxxExx format
        if (re.search(r's\d+E\d+', FileName, flags=re.IGNORECASE) != None):
            # Set media type to TV
            MedT = MedTy[0]
            # Extract TV Show Name
            MedName = re.split(r'\.s\d+', FileName, flags=re.IGNORECASE)[0]
            # Extract season number
            Seas = re.split(
                r'S', (re.search(r'S\d+', FileName, flags=re.IGNORECASE).group().upper()), maxsplit=2)[1]
            # Check if episode format matches Exx-Exx
            if (re.search(r'E\d+-E\d+', FileName, flags=re.IGNORECASE) != None):
                # Get the episode numbers
                Epi = re.split(
                    r'E', (re.search(r'E\d+-E\d+', FileName, flags=re.IGNORECASE).group().upper()))
                Epi.pop(0)  # Remove first empty list element
                # Remove the extra - from the first episode number
                Epi[0] = re.split(r'-', Epi[0])[0]
            # Search for the pattern ExxExx
            elif (re.search(r'E\d+E\d+', FileName, flags=re.IGNORECASE) != None):
                # Get the episode numbers
                Epi = re.split(
                    r'E', (re.search(r'E\d+E\d+', FileName, flags=re.IGNORECASE).group().upper()))
                Epi.pop(0)  # Remove first empty list element
            elif (re.search(r'E\d+', FileName, flags=re.IGNORECASE) != None):  # Serach for Exx pattern
                # Get the episode numbers
                Epi = re.split(
                    r'E', (re.search(r'E\d+', FileName, flags=re.IGNORECASE).group().upper()))
                Epi.pop(0)  # Remove first empty list element
            else:  # No episode number
                Epi = ["-1"]
        else:  # Movie File
            # Set media type to Movie
            MedT = MedTy[1]
            # Extract TV Show Name
            MedName = (re.split(r'\d{4}', os.path.splitext(FileName)[0],
                       flags=re.IGNORECASE)[0]).strip(r'\.$')
            # Get Movie Year
            MedYear = re.search(r'\d{4}', FileName, flags=re.IGNORECASE).group() if (
                re.search(r'\d{4}', FileName, flags=re.IGNORECASE) != None) else ""
            Seas = "-1"  # Clear season number
            Epi = ["-1"]  # Clear episode number
        return SuccessM, MedT, Seas, Epi, FileName, FileDir, FileExt, MedName, MedYear, HebDub, MedRes, FileT
    except:
        # Return an error
        return DetMTErr, "", "", [""], "", "", "", "", "", False, "", MedFType[3]


# Check If Dir Is Empty
def Is_Dir_Empty(src):
    """
    Make sure the folder provided is empty

    depends on:
        imports:
            os

    :param src: The path to check
    :return: True if empty.
    """
    with os.scandir(src) as scan:
        return next(scan, None) is None


# Rename the file and return the new path
def Rename_TV_Movie(Org_File, New_full_Path, Verbo, LogPath):
    """
    Rename a file.

    depends on:
        imports:
            os
            shutil

    :param Org_File: File path to rename.
    :param New_full_Path: New file path to save.
    :param Verbo: Verbose anable (True or False).
    :param LogPath: Path to log file.
    :return: True on success, False on any fail.
    """
    try:
        # Make sure path exists and create if not
        if (not os.path.exists(os.path.dirname(New_full_Path))):
            os.makedirs(os.path.dirname(New_full_Path))
        # Check if file alredy exists and confirm overwrite
        if (os.path.isfile(New_full_Path)):
            # Log File Exists
            LogMassage("File already exists.", LogPath)
            if (Confirm_Select("File alredy exists. Do you want to overwrite it?")):
                # Log file overwrite
                LogMassage(
                    "User selected to overwrite the existing file.", LogPath)
                if (Verbo):
                    print("Overwrite the file!")
                # Rename The File
                shutil.move(Org_File, New_full_Path)
            elif (Verbo):
                print("Skiping the file!")
        else:
            # Rename The File
            shutil.move(Org_File, New_full_Path)
        return True
    except:
        return False


# Load media list
def Load_List(List_Path):
    """
    Load the media list

    depends on:
        imports:
            os
            re

    :param List_Path: New name for the file.
    :return: Success or fail, Array of names and pathes, Array of only names
    """
    try:
        if (os.path.isfile(List_Path)):  # Make sure the file exists
            with open(List_Path) as Lines:  # Read the file
                # read the contets of the file and split into lines
                Show_List_Unsplit = Lines.read().splitlines()
            Show_List_Names = []  # Set a blank array for the show list
            Show_List_Full = []  # Set a blank array for the show list
            for L in Show_List_Unsplit:  # Loop threw the list lines
                # Check if HebDub
                Show_List_Names.append(re.split(r' : ', L)[0])
                Show_List_Full.append(re.split(r' : ', L))
            return SuccessM, Show_List_Full, Show_List_Names
        else:
            return NList, [""], [""]
    except:
        return GenFail, [""], [""]


# Input selector
def Choice_Select(ChoicArr, MessageUser):
    """
    Load the media list

    depends on:
        imports:
            InquirerPy

    :param ChoicArr: Array of choices to present.
    :param MessageUser: Question to display.
    :return: User choice
    """
    action = inquirer.fuzzy(
        message=MessageUser,
        choices=ChoicArr,
        default=None,
    ).execute()
    return action


# Manual input
def Man_Detailes(MessageUserSN, MessageUserSP, SPOpt):
    """
        Load the media list

    depends on:
        imports:
            InquirerPy

    :param MessageUserSN: Question to display for media name.
    :param MessageUserSP: Question to display for media path.
    :param SPOpt: Path array to auto complete.
    :return: Manual name, Manual path
    """
    name = inquirer.text(message=MessageUserSN).execute()  # Get Sshow name
    ShowPath = inquirer.text(message=MessageUserSP, completer=SPOpt,
                             multicolumn_complete=True,).execute()  # Get Path
    return name, ShowPath


# Build New file name To Arrange The File
def Build_New_Name(Season, Episode, ToM, NName, SLang, Msfx, MeFT):
    """
    Build new file name based on plex organization scheme.

    depends on:
        imports:
            os
            re

    :param Season: Season number for TV Episode file.
    :param Episode: Episode number for TV Episode file.
    :param ToM: For TV Show File Set to "TV", For Movie file set to "Movie", everything else will give an error.
    :param NName: New TV Show or Movie Name.
    :param SLang: Languge suffix for the subtitile name, mast have a dot at the start (like .heb).
    :param MPfx: Media file suffix (like .mkv), must have dot at the start.
    :param SPfx: Subtitle file suffix (like .srt), must have dot at the start.
    :return: On any undefind error return "Error!!!", on ToM Error return "Error!!", on success return New File Name
    """
    try:
        # Check if TV Or Movie Title
        if (ToM == MedTy[0]):
            # Build The Episode Name
            New_Name = NName + " - S" + Season + "E" + Episode[0]
            # If the original file is a multi episode, adapt the new episode name
            if (len(Episode) > 1):
                New_Name += "-E" + Episode[1]
        elif (ToM == MedTy[1]):
            # Change The Movie Name To The New Name
            New_Name = NName
        else:
            # Error Out
            New_Name = "Error!!"
        # Check if subtitle file
        if (MeFT == MedFType[1] and New_Name != "Error!!"):
            New_Name = New_Name + SLang + Msfx.lower()
        elif ((MeFT == MedFType[0] or MeFT == MedFType[2]) and New_Name != "Error!!"):
            New_Name += Msfx.lower()
        return New_Name
    except:
        # Error Out
        return "Error!!!"


# Build new path to file
def Build_New_Path(Org_File, Org_Dir, NName, ToM, Season, H_deb, M_Res):
    """
    Build new file path based on plex organization scheme.

    depends on:
        imports:
            os
            re

    :param Org_File: File path to rename.
    :param NName: New TV Show or Movie Name.
    :param ToM: For TV Show File Set to "TV", For Movie file set to "Movie", everything else will give an error.
    :param Season: Season number for TV Episode file.
    :return: On any undefind error return "Error!!!", on ToM Error return "Error!!", on success return New File Name
    """
    try:
        # Build The New File Path
        if (Org_File.lower() in Org_Dir.lower()):
            # Folder structure has the file name as a folder name
            New_Path = os.path.abspath(
                os.path.join(Org_Dir, '..'))
        else:
            # keep the original dir
            New_Path = Org_Dir
        # Check if Dubed
        if (H_deb):
            New_Path = os.path.join(New_Path, ToM + "_" + HeDub)
        else:
            New_Path = os.path.join(New_Path, ToM)
        # Check for res
        if (M_Res in UHDRes):
            New_Path = os.path.join(New_Path, UHDRes[0])
        # Add Media name as a folder in path
        New_Path = os.path.join(New_Path, NName)
        # Check if TV Or Movie Title
        if (ToM == MedTy[0]):  # TV
            New_Path = os.path.join(New_Path, SeaPfx + " " + Season)
        # return the new path
        return New_Path
    except:
        # Error Out
        return "Error!!!"


# Clean up and delete empty folders
def Clean_Up(src, rem_src):
    """
    Remove empty folders and src folder if needed

    depends on:
        imports:
            os

    :param src: source folder to work in.
    :param rem_src: True for delete source folder if empty, false - do not delete source folder.
    :return: True on success, false on fail.
    """
    try:
        # Get the list of folders and files and loop threw it
        for (Root_dir, dirs, Files) in os.walk(src, topdown=False):
            # Check if the folder has file(s) in it (starts with a .)
            if (Files):
                # Loop threw the files
                for File in Files:
                    # Check if the file name starts with .
                    if (File.lower().startswith(".")):
                        # Rebuild the full path to the file
                        f = os.path.join(Root_dir, File)
                        # Delete the file
                        os.remove(f)
                        # Remove the deleted file from the list
                        Files.remove(File)
            # Check if folder does not contain files or sub folders
            if (not dirs and not Files and Root_dir != src):
                # Delete the folder
                os.rmdir(Root_dir)
        # Delete source folder if requested and empty
        if (Is_Dir_Empty(src) and rem_src):
            os.rmdir(src)
        return True
    except:
        # Error Out
        return False


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
