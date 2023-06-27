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
    src = ArgsArr[0]        # Source folder path
    Verb = ArgsArr[1]       # Print messeges to users
    ListPath = ArgsArr[2]   # Path to media list file
    MoveFiles = ArgsArr[3]  # Move files to correct folders
    remsrc = ArgsArr[4]     # Remove source folder to cleanup
    File_List = []          # Place holder for files in source directory
    Med_List_Names = []     # Place holder for media list info
    Med_List_Full = []      # Place holder for media list info
    ExtList = ""            # Place holder for testing if external list load was successfull
    GDSucc = ""             # Extract data success or not
    Mtyp = ""               # Media type
    Se = ""                 # Season number
    Ep = []                 # Episode numbers
    Fname = ""              # File name
    Fdir = ""               # File directory
    FExt = ""               # File extension
    MName = ""              # Media name
    MYear = ""              # Media year
    Hdeb = False            # Hebrew dub
    MRes = ""               # Media resolution
    Ftype = ""              # File type
    ChoiceList = []         # Place holder for chioces in selector
    SelMed = ""             # Selected media name
    LName = ""              # Name from list or manual input
    LPath = ""              # Path from list or manual input
    ModName = ""            # New name for the file after all modifications
    ModPath = ""            # New folder path for the file after all modifications
    ModFullPath = ""        # New full path for the file after all modifications
    ind = ""                # Counter index

    try:
        # TODO: Add logger functionality
        # Check if the source folder is valid and do the logic
        if (src != NSRC):
            if Verb:  # Show progress if requested
                print("Source folder is valid, searching for media files...")
            # Get all media files inside the sorce folder
            File_List = GetFiles(src)
            if (File_List[0] == FGFiles):  # Check if failed to get files
                if Verb:
                    print("Cann't get media files, exiting!")
                return False
            elif (File_List[0] == NFiles):  # Check if found media files, if not exit
                if Verb:
                    print("No media files found, exiting!")
                return False
            else:  # Found media files, do the logic
                if Verb:
                    print("Found media files to work on, Continueing...")
                # Load external list
                if (ListPath != NList):
                    ExtList, Med_List_Full, Med_List_Names = Load_List(
                        ListPath)
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
                # Loop the file list
                for f in File_List:
                    # Extract file data
                    GDSucc, Mtyp, Se, Ep, Fname, Fdir, FExt, MName, MYear, Hdeb, MRes, Ftype = Get_Movie_TV_Data(
                        f)
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
                            # Massage the user about skiping
                            if (Verb):
                                print('Skiping "{}"'.format(MName))
                        else:
                            # Build new file name
                            ModName = Build_New_Name(
                                Se, Ep, Mtyp, LName, LFsfx, FExt, Ftype)
                            # Build new folder path
                            ModPath = Build_New_Path(
                                MName, Fdir, LName, Mtyp, Se, Hdeb, MRes)
                            # TODO: Add log file here...
                            # Update the path to list location if user requested a move
                            if (MoveFiles):
                                ModPath = os.path.join(LPath, LName)
                                if (Verb):
                                    print("Moveing to new location ({})".format(
                                        ModPath))
                            # Make full file path
                            ModFullPath = os.path.join(ModPath, ModName)
                            # Rename the file and move it to correct folder structure
                            Rename_TV_Movie(f, ModFullPath, Verb)
                            # Print new line
                            if (Verb):
                                print("######\n")
                    else:
                        # Messege the user - fail
                        if (Verb):
                            print("Failed to extract data from: ",
                                  f, "\nContinueing to next task...")
                # Clean up
                if (Clean_Up(src, remsrc)):
                    if (Verb):
                        print("Removed all empty sub folders in {}".format(src))
                # Print finished message
                if (Verb):
                    print("Finished all tasks!")
                return True
        else:  # Source path is not valid
            if Verb:  # Print error message if user wants to see info
                print("Source path is not valid, exiting!")
            return False
    except:
        print("Unknown error.\nFailed to run!!!")
        return False


# Make sure to run only if called directly
if __name__ == "__main__":
    main(Args_Arr)