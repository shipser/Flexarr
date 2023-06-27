#!/usr/bin/env python3

###########
# Imports #
###########

import os                       # OS base functions
import re                       # For Regex Strings
from Config.Params import *     # Import configurations


def Get_Recomanded_Location(IS4k, ISDub, ISMovieOrTV, Locations):
    """
    Get recomanded location from list based on file data

    :param IS4k: True or False
    :param ISDub: True or False
    :param ISMovieOrTV: TV or Movie
    :param Locations: Tuple of pre set locations
    :return: string of first location relevent
    """
    try:
        # Get only the keys from the dictionary
        LocationList = list(Locations.keys())
        # Get sub list containing only relevent to the media type
        LocationListByType = [i for i in LocationList if ISMovieOrTV in i]
        # Get sub list containing only relevent to the dubed state
        if (ISDub):
            LocationListByDub = [
                i for i in LocationListByType if HeDub.lower() in i.lower()]
        else:
            LocationListByDub = [
                i for i in LocationListByType if HeDub.lower() not in i.lower()]
        # Get sub list containing only relevent to the resolution
        if (IS4k):
            LocationListByRes = [
                i for i in LocationListByDub if UHDRes[0].lower() in i.lower()]
        else:
            LocationListByRes = [
                i for i in LocationListByDub if UHDRes[0].lower() not in i.lower()]
        return LocationListByRes[0]
    except:
        return "Error!!"


def Get_Uniqe_Data(DataToSort):
    """
    Return a list of arrays with uniqe data

    :param Data: List of arrays
    :return: Uniqe list of arrays
    """
    try:
        Outputs = []
        for i in DataToSort:
            if i not in Outputs:
                Outputs.append(i)
        return Outputs
    except:
        return ["Error!!"]


def WriteNewList(ListPath, Contents):
    """
    Write the new list file

    :param ListPath: List path to save
    :param Contents: Data to save to the list
    :return: True on success, False on fail
    """
    try:
        # Create the file
        f = open(ListPath, "w")
        # Write the contents to the file
        f.write('\n'.join(Contents))
        # Close the file
        f.close()
        return True
    except:
        return False
