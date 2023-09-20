#!/usr/bin/env python3

###########
# Imports #
###########

import argparse                 # Import for the arguments handeling
import os                       # OS base functions
from Config.Params import *     # Get Version Number String

############################
# Argument Parser Settings #
############################

# Declare empty argumant array
Args_Arr = []

parser = argparse.ArgumentParser(description=desc,
                                 usage='%(prog)s [OPTIONS]', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-C', '-c', '--CleanUp', action='store_true',
                    help="Remove source folder after moveing the media files, will only work if no other files or folders left inside.")
parser.add_argument('-G', '-g', '--GroupFiles', action='store_true',
                    help="Group media files based on data extracted from file names.")
parser.add_argument('-L', '-l', '--LoadList',
                    help="Load external TV show and Movie list to select the correct one from it.", default="")
parser.add_argument('-M', '-m', '--Move', action='store_true',
                    help="Move the TV Show Episodes or Movie to the path provided.", default=False)
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
    os.path.isfile(args.LoadList)) else NList)
Args_Arr.append(args.Move)
Args_Arr.append(args.CleanUp)
Args_Arr.append(args.GroupFiles)
