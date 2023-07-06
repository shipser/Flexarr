#!/usr/bin/env python3

###########
# Imports #
###########

import datetime     # For time stamp
import os           # OS base functions
import re           # For Regex Strings

# TODO; Build all the functionality


# Initialize the log file
def LogFile_Init(Log_File, TStemp):
    """
    Initialize log file

    :param Log_File: Log file path to initialize.
    :param TStemp: Time stemp of creation.
    :return: True on success, false on fail.
    """
    try:
        # Heaser defenition
        Header_Mass = "##### Flexarr Log #####\n\nCreated: " + str(TStemp.day) + "-" + str(TStemp.month) + \
            "-" + str(TStemp.year) + " " + str(TStemp.hour) + ":" + \
            str(TStemp.minute) + ":" + str(TStemp.second) + \
            "\n\n##############################\n\n"
        # Create the log file
        if (not os.path.isfile(Log_File)):
            with open(Log_File, "w") as f:
                # Insert header to the file
                f.write(Header_Mass)
            # Success or Fail
            return True
        else:
            # File already exists, cann't cuse it.
            return False
    except Exception as Error:
        # Error Out
        return Error


# Build log file name
def Create_Log_File(SRC, Verbo):
    """
    Create log file

    :param SRC: source directory to work on
    :return: Log path and Time stamp of creation
    """
    try:
        # Time stamp
        Tstemp = datetime.datetime.now()
        # Build log name
        Log_Name = "Flexarr_" + str(Tstemp.year) + "-" + str(Tstemp.month) + "-" + str(
            Tstemp.day) + "_" + str(Tstemp.hour) + "-" + str(Tstemp.minute) + "-" + str(Tstemp.second) + ".log"
        Log_path = os.path.join(SRC, Log_Name)
        # Create the log file and initialize it
        if (LogFile_Init(Log_path, Tstemp)):
            # Massage the user
            if (Verbo):
                print("Log file created and initialized!")
        return True, Log_path, Tstemp
    except Exception as Error:
        return Error


# Log Message
def LogMassage(Massage, LogPath):
    """
    Log string massage to log file

    :param Massage: Massage to log
    :param LogPath: Path to log file
    :return: True on success, Error on fail
    """
    try:
        # Time stamp
        TStemp = datetime.datetime.now()
        # Heaser defenition
        Header_Mass_TS = str(TStemp.day) + "/" + str(TStemp.month) + "/" + str(
            TStemp.year) + " " + str(TStemp.hour) + ":" + str(TStemp.minute) + ":" + str(TStemp.second)
        Header_Mass = Header_Mass_TS + "\t" + Massage + "\n"
        # Create the log file
        if (os.path.isfile(LogPath)):
            with open(LogPath, "a") as f:
                # Insert header to the file
                f.write(Header_Mass)
            # Success or Fail
            return True
        else:
            # File already exists, cann't cuse it.
            return False
    except Exception as Error:
        return Error


# Build log massage from array
def BuildLogMassageFromArray(PFX, Arr, Dim, Del):
    """
    Create massage to save from an array

    :param PFX: Massage prefix to convert
    :param Arr: Array to convert
    :param Dim: Number of array dimentions 
    :param Del: Delimiter 
    :return: Massage to save
    """
    try:
        # Massage place holder
        Mass = PFX + "\n"
        # Counter for rows
        Ci = 1
        # Loop thrugh the array
        for i in Arr:
            # Check if two dimentions or one
            if (Dim == 2):
                # Set Counter
                Count = 1
                # Loop thregh the second dimention
                for j in i:
                    # Check if a seporator is needed
                    if (Count == len(i)):
                        Mass = Mass + " : "
                    # Else add a tab
                    else:
                        Mass = Mass + "\t"
                    Mass = Mass + Del + str(j) + Del
                    Count += 1
            # If not 2, assume 1
            else:
                Mass = Mass + "\t" + Del + str(i) + Del
            # Add line break for every line except the last one
            if (Ci < len(Arr)):
                Mass = Mass + "\n"
            Ci += 1
        return Mass
    except Exception as Error:
        print(Error)
        return Error


# Log data in JSON structure
def BuildMassageJSON(PFXArr, DATAArr):
    """
    Build JSON like massage

    :param PFXArr: Array of prefixies
    :param DATAArr: Array of data
    :return: Massage to log
    """
    try:
        # Massage place holder
        Mass = ""
        # Set counter
        Count = 0
        # Make sure PFXArr length equals DATAArr length
        if (len(PFXArr) == len(DATAArr)):
            Mass = "\t{\n"
            # Loop the arrayes
            for i in PFXArr:
                # Build line
                Mass = Mass + "\t\t" + i + " : " + str(DATAArr[Count])
                # Add line break for every line except the last one
                if (Count < (len(PFXArr) - 1)):
                    Mass = Mass + ",\n"
                Count += 1
            Mass = Mass + "\n\t}"
        return Mass
    except Exception as Error:
        return Error


# Log finish massage
def LogFinishMassage(LogPath, StartTime):
    """
    Log finish massage to the file

    :param LogPath: Path to log file
    :param StartTime: Start of run time.
    :return: True on success
    """
    try:
        # Time stamp
        TStemp = datetime.datetime.now()
        # Heaser defenition
        Footer_Mass = "Finished running after " + str((datetime.datetime.now(
        ) - StartTime).total_seconds()) + " seconds.\n\n##############################\n\n"
        # Add the massage to the file
        LogMassage(Footer_Mass, LogPath)
        return True
    except Exception as Error:
        return Error
