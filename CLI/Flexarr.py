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

from Functions.Base import *                # Import all base functions
from Functions.Argunamts import Args_Arr    # Import argumant handeling
from Config.Params import *                 # Import Configurations
from Functions.Logger import *              # Import logger functions

###############################
# Global Variables Defenition #
###############################


###########################
# Do Not Change From Here #
###########################

def main(ArgsArr):
    """
    Main loop of the program

    :param Args_Arr: ArgsArr = Args_Arr
    :return: True on success, False on any error
    """
    # Set variables
    src = ArgsArr[0]            # Source folder path
    Verb = ArgsArr[1]           # Print messeges to users
    ListPath = ArgsArr[2]       # Path to media list file
    MoveFiles = ArgsArr[3]      # Move files to correct folders
    remsrc = ArgsArr[4]         # Remove source folder to cleanup
    File_List = []              # Place holder for files in source directory
    Med_List_Names = []         # Place holder for media list info
    Med_List_Full = []          # Place holder for media list info
    ExtList = ""                # Place holder for testing if external list load was successfull
    GDSucc = ""                 # Extract data success or not
    Mtyp = ""                   # Media type
    Se = ""                     # Season number
    Ep = []                     # Episode numbers
    Fname = ""                  # File name
    Fdir = ""                   # File directory
    FExt = ""                   # File extension
    MName = ""                  # Media name
    MYear = ""                  # Media year
    Hdeb = False                # Hebrew dub
    MRes = ""                   # Media resolution
    Ftype = ""                  # File type
    ChoiceList = []             # Place holder for chioces in selector
    SelMed = ""                 # Selected media name
    LName = ""                  # Name from list or manual input
    LPath = ""                  # Path from list or manual input
    ModName = ""                # New name for the file after all modifications
    ModPath = ""                # New folder path for the file after all modifications
    ModFullPath = ""            # New full path for the file after all modifications
    ind = ""                    # Counter index
    LogPath = ""                # Log file path
    LogFileInit = False         # Log file state
    LogCreateTimeStamp = ""     # Time stamp of log file initial creation

    try:
        # TODO: allow for similar files (for TV) to be named once
        # TODO: Allow to disable log file
        # TODO: Allow for user selected log file
        # Initialize Log file
        LogFileInit, LogPath, LogCreateTimeStamp = Create_Log_File(
            (src if (src != NSRC) else os.path.dirname(__file__)), Verb)
        # Check if the source folder is valid and do the logic
        if (src != NSRC):
            # Log operation
            LogMassage("Source folder ('{}') is valid".format(src), LogPath)
            if (MoveFiles):
                LogMassage(
                    "User selected to move the files to new location.", LogPath)
            if (remsrc):
                LogMassage(
                    "User selected to remove source folder after moveing all media files.", LogPath)
            if Verb:  # Show progress if requested
                LogMassage("Verbose is enabled.", LogPath)
                print("Source folder is valid, searching for media files...")
            # Get all media files inside the sorce folder
            File_List = GetFiles(src)
            if (File_List[0] == FGFiles):  # Check if failed to get files
                # Log Files Found
                LogMassage("Failed to get files in source directory.", LogPath)
                if Verb:
                    print("Cann't get media files, exiting!")
                return False
            elif (File_List[0] == NFiles):  # Check if found media files, if not exit
                # Log Files Found
                LogMassage("No media files found in directory.", LogPath)
                if Verb:
                    print("No media files found, exiting!")
                return False
            else:  # Found media files, do the logic
                # Log Files Found
                LogMassage(BuildLogMassageFromArray(
                    "Files found:", File_List, 1, "'"), LogPath)
                if Verb:
                    print("Found media files to work on, Continueing...")
                # Log list path provided
                if (ListPath == NList):
                    LogMassage("No valid external list provided.", LogPath)
                # Load external list
                if (ListPath != NList):
                    # Log external list path
                    LogMassage("External list path: '" +
                               ListPath + "'", LogPath)
                    ExtList, Med_List_Full, Med_List_Names = Load_List(
                        ListPath)
                    # Log data from external list
                    LogMassage("External list read status: " +
                               ExtList, LogPath)
                    if (ExtList == SuccessM):
                        LogMassage(BuildLogMassageFromArray(
                            "Media in list:", Med_List_Full, 2, "'"), LogPath)
                    # Add Manual as a choice
                    ChoiceList.append(EnterManualChoice)
                    # Add Skip as a choice
                    ChoiceList.append(EnterSkipChoice)
                    # Set Counter
                    ind = int(2)
                    # Add the list of choices for the selector
                    for Med_List_Full_choice in Med_List_Full:
                        # Insert the choice value to the array
                        ChoiceList.append(Med_List_Full_choice[0])
                        # Make sure the lines where the media is HebDubed the choice value shows it
                        if (HeDub in Med_List_Full_choice[1]):
                            ChoiceList[ind] += " (" + HeDub + ")"
                        # Increment counter
                        ind += 1
                    # Messege the user
                    if (ExtList == SuccessM and Verb):
                        print("Media list loaded, Continueing...\n")
                    elif (ExtList == NList and Verb):
                        print(
                            "Failed to load media list, path not valid. Continueing without it...\n")
                    elif (ExtList == GenFail and Verb):
                        print(
                            "Failed to read list, unkown error. Continueing without the list...\n")
                # Log working on files
                LogMassage("Starting to work on files:", LogPath)
                # Loop the file list
                for f in File_List:
                    # Extract file data
                    GDSucc, Mtyp, Se, Ep, Fname, Fdir, FExt, MName, MYear, Hdeb, MRes, Ftype = Get_Movie_TV_Data(
                        f)
                    # Log File Data
                    LogMassage("Data for file ('{}')\n".format(f) + BuildMassageJSON(["Data extract status:", "Media type:", "Season:", "Episode(s):", "File name:", "File location:", "File extention:",
                               "Media name:", "Year:", "Hebrew dubed:", "Media resolution:", "File category:"], [GDSucc, Mtyp, Se, Ep, Fname, Fdir, FExt, MName, MYear, Hdeb, MRes, Ftype]), LogPath)
                    if (GDSucc == SuccessM):
                        # Message the user - success
                        if (Verb):
                            print("######\nExtracted data for: ", f)
                        # Do some logic
                        if (ExtList == SuccessM):
                            # Create the message to display
                            Mess = "Select Movie or TV Show from the list for " + MName + ":"
                            # Add Hebdub to Messege if needed
                            if (Hdeb):
                                Mess = Mess[:-1] + " (" + HeDub + "):"
                            # Ask the user to choose a media
                            SelMed = Choice_Select(
                                ChoiceList, Mess)
                            # Check if user wants to type manualy
                            if (SelMed == EnterManualChoice):
                                LName, LPath = Man_Detailes(
                                    ManMediaInputMess, ManMediaPathInputMess, PreSetPathes)
                            elif (SelMed == EnterSkipChoice):
                                LName = LPath = EnterSkipChoice
                            else:
                                # LName = SelMed
                                LName = Med_List_Full[ChoiceList.index(
                                    SelMed) - 2][0]
                                LPath = Med_List_Full[ChoiceList.index(
                                    SelMed) - 2][1]
                        else:
                            # Ask the user if to skip the file
                            if (not Confirm_Select(('Do you want to set the new file name and path for "{}"').format(MName))):
                                LName = LPath = EnterSkipChoice
                            else:
                                # No extrenal list
                                LName, LPath = Man_Detailes(
                                    ManMediaInputMessFail, ManMediaPathInputMess, PreSetPathes)
                        # Skip file if requested
                        if (LName == LPath and LName == EnterSkipChoice):
                            # Log skip
                            LogMassage(
                                "User selected to skip this file.", LogPath)
                            # Massage the user about skiping
                            if (Verb):
                                print('Skiping "{}"'.format(MName))
                        else:
                            # Log info entered
                            if ((SelMed == EnterManualChoice) or (ExtList != SuccessM)):
                                if (SelMed == EnterManualChoice):
                                    LogMassage(
                                        "User chose to enter name and path namualy.", LogPath)
                                LogMassage(
                                    "Manual name and path input from user:\n\tNew name: '{}'\n\tNew path: '{}'".format(LName, LPath), LogPath)
                            else:
                                LogMassage(
                                    "Selected name and path input from user:\n\tNew name: '{}'\n\tNew path: '{}'".format(LName, LPath), LogPath)
                            # Build new file name
                            ModName = Build_New_Name(
                                Se, Ep, Mtyp, LName, LFsfx, FExt, Ftype)
                            # Build new folder path
                            ModPath = Build_New_Path(
                                MName, Fdir, LName, Mtyp, Se, Hdeb, MRes)
                            # Update the path to list location if user requested a move
                            if (MoveFiles):
                                ModPath = os.path.join(LPath, LName)
                                # Add season folder if needed
                                if (Mtyp == MedTy[0]):
                                    ModPath = os.path.join(
                                        ModPath, SeaPfx + " " + Se)
                                if (Verb):
                                    print("Moveing to new location ({})".format(
                                        ModPath))
                            # Make full file path
                            ModFullPath = os.path.join(ModPath, ModName)
                            # Log new name and path after all modifications
                            LogMassage("\n\tNew name after modification: '{}'\n\tNew path after modification: '{}'\n\tNew full file path after modification: '{}'".format(
                                ModName, ModPath, ModFullPath), LogPath)
                            # Rename the file and move it to correct folder structure
                            Rename_TV_Movie(f, ModFullPath, Verb, LogPath)
                            # Log Rename and move
                            LogMassage("Renamed and moved the file to chosen location and name." if (
                                MoveFiles) else "Renamed the file to the chosen name.", LogPath)
                            # Print new line
                            if (Verb):
                                print("######\n")
                    else:
                        # Log the fail
                        LogMassage(
                            "Failed to extract data for the file '{}'".format(f), LogPath)
                        # Messege the user - fail
                        if (Verb):
                            print("Failed to extract data from: ",
                                  f, "\nContinueing to next task...")
                # Clean up
                if (Clean_Up(src, remsrc)):
                    # Log remove empty folders
                    LogMassage("Cleand up the source folder.", LogPath)
                    if (Verb):
                        print("Removed all empty sub folders in {}".format(src))
                # Print finished message
                if (Verb):
                    print("Finished all tasks!")
                    print("Log savet at: '{}'".format(LogPath))
                # Log finish time
                LogFinishMassage(LogPath, LogCreateTimeStamp)
                return True
        else:  # Source path is not valid
            # Log Error
            LogMassage("Source is not valid.", LogPath)
            LogFinishMassage(LogPath, LogCreateTimeStamp)
            if Verb:  # Print error message if user wants to see info
                print("Source path is not valid, exiting!")
            return False
    except:
        print("Unknown error.\nFailed to run!!!")
        return False


# Make sure to run only if called directly
if __name__ == "__main__":
    main(Args_Arr)
