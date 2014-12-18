#############################################################################
#
# Copyright 2014 Dmitry Volovnenko
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#############################################################################

import os
import sys
import getopt
import filecmp
import shutil

# Variables where saved paths to folders
parentFolder = ''
heirFolder = ''
# Getting subdirs
def getSubdir(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]
# Function for synchronize folders 
def syncFolders(parent, heir):
	d_comp = filecmp.dircmp(parent, heir)
	subdirList = getSubdir(parent)
	for dirItem in d_comp.common_dirs:
		syncFolders(os.path.join(parent, dirItem), os.path.join(heir, dirItem))
	for item in d_comp.left_only:
		if item in subdirList:
			shutil.copytree(os.path.join(parent, item), os.path.join(heir, item))
		else:
			shutil.copyfile(os.path.join(parent, item), os.path.join(heir, item))
	

# Boolean variables for options(printing lists with diff, compare and synchronize with each other)
isShow = False
isRecursive = False

# Use -p(parent) and -h(heir) keys to set folders passes through command-line
# If needed, use -r key compare and to synchronize folders with each other
# Set -s key for showing files and folders inside target directories with different in they are  
# In this step, parsing sys.argv with getopt
opts, args = getopt.getopt(sys.argv[1:],"rsp:h:")
# If have not incoming data - get out from here
if len(opts) == 0:
	print 'No input paths' # Here, must be more intellectual text, I think so
	sys.exit(2)
# and getting needed value
for opt, arg in opts:
	if opt == '-r':
		isRecursive = True 		
	elif opt == '-s':
		isShow	= True
	elif opt in '-p':
		parentFolder = arg
	elif opt in '-h':
		heirFolder = arg	

# Checking folder paths
if len(parentFolder) == 0 or len(heirFolder) == 0:
	print 'No input paths' # one more, here, must be more intellectual text, I think so
	sys.exit(2)
# synchronize folders

syncFolders(parentFolder, heirFolder)
