#!/usr/bin/env python3

# Release number - Major.Minor.Fix, where fix can be uncomplited feature update
Ver = "1.0.0-alpha2"
# Set help message for the cli
desc = "******************************************************************************************\n\n  Flexarr by Shay Pasvolsky (C).\n\n******************************************************************************************"

# Input error vlaues
NSRC = "No_Source"                                  # Sorce path is not valid
NList = "No_List"                                   # Media list is not valid
NFiles = "SRC_Empty"                                # No media files found
FGFiles = "Failed_Get_Files"                        # Failed to get media files
# Error detecting movie file or tv file
DetMTErr = "Error_Det_Mov_TV"
SuccessM = "Success"                                # Show Success
GenFail = "General_Fail"                            # General fail
EnterManualChoice = "*** Enter manual name. ***"    # Manual name chioce
EnterSkipChoice = "* Skip this file. *"             # Skip file choice
ManMediaInputMess = "Enter media name: "            # Manual media input message
# Manual media input message on fail to extract
ManMediaInputMessFail = "Failed to extract data from file, pleas enter media name: "
# Manual media path input message
ManMediaPathInputMess = "Enter Media Path: "
# Pre configured pathes
PreSetPathes = {"/media/ExtraBigHD/TV/": None,
                "/media/BigHD/TV/": None,
                "/media/ExtraBigHD/HebDub_TV/": None,
                "/media/ExtraBigHD/Courses/": None,
                "/media/ExtraBigHD/HebDub_Movies/": None,
                "/media/ExtraBigHD/HebDub_Movies_4K/": None,
                "/media/ExtraBigHD/Movies/": None,
                "/media/ExtraBigHD/Movies_4K/": None,
                "/media/ExtraBigHD/Shows/": None,
                "/media/ExtraBigHD/Youtube/": None,
                }

# General configurations
MFsfx = (".mkv", ".avi", ".mov", ".mp4", ".mpg",
         ".mpeg", ".flv")       # Movie File Suffix
# Subtitle File Suffix
SFsfx = (".srt", ".ass", ".vtt", ".ssa", ".ttml",
         ".sbv", ".dfxp", ".txt", ".sub", ".smi", ".stl")
# Extra media files suffix
EFsfx = (".jpg", ".jpeg", ".nfo")
# Language Suffix For The Subtitles
LFsfx = ".heb"
# Season folder prefix
SeaPfx = "Season"
# 4k resulotion
UHDRes = ["4k", "UHD", "2160p"]
# File types (movie, subtitle, extra, unkown)
MedFType = ["Movie", "Subtitle", "Extra", "Unkown"]
# Media types
MedTy = ["TV", "Movie"]
# Standart resolution
SDRes = "SD"
# HebDub suffix
HeDub = "HebDub"
