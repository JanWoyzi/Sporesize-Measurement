'''
MIT License

Copyright (c) 2020 Jan Woyzichovski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import os
from ij import IJ

# This script is mainly for the segmentation step with weka. Within the weka script it is not possible to automatically create folders or directories.
# But weka needs a preexisting folder to save the results.
# Therefore creating folders should be done before the segmentation step with this script.

#be careful this script overwrites without warning!

def reemovNestings(l):  #removes nested or subfolder in a given (l)ist
    for i in l:
        if type(i) == list:
            reemovNestings(i)
        else:
            itemlist.append(i)

todolist = ["foldername01", "foldername02"] # processing a list of directories on the level of multiple folders
todoitem = ["test"] # filterlist: elements that should be included; if files were differently named

for multi in todolist:
    itemlist = []
    source = "G:/folder_lvl01/folder_lvl02/folder_lvl03/0_Raw/" + multi   # directory location for images that should be processed (TIFF-format!)
	save1 = "G:/folder_lvl01/folder_lvl02/folder_lvl03/2_Weka/" + multi	# directory location for segmented images
	save2 = "G:/folder_lvl01/folder_lvl02/folder_lvl03/processed_1_Separation/" + multi # directory location for processed images, not necessary step, takes source files and located them in his directory, helps to keep track which file was already processed

    itlist = []
    list2 = os.listdir(source) # creates list of files based on source directory
    try:														#
        for i in todoitem:										#
            ilist = list(filter(lambda x:  i in x, list2))		# Filter: let only the string (given from "todoitem") in the list
            itlist.append(ilist)								#
    except ValueError:											#
        pass													#
    itlist = [i for i in itlist if i] # removes empty cells
    reemovNestings(itlist)
    for folder in itemlist:
		if (folder.endswith(".tif")):
			print("Why is here a tif!")# If this print out appears then you are giving him a too deep or too swallow level of directories; ...
			# ...on this level (folder) is the sample folder, in the sample folder are all the .tiff-files
		else :
			addsource = source + "/" + folder
			list3 = os.listdir(addsource)
			list3.sort()
			count = 1
			for c in list3:
				### begin of renaming function
				# comment this part for deactivating renaming function (line 48 to 58) or make a if-rule
				filename_without_ext = os.path.splitext(c)[0] # removes the ".tif"-part from the filename
				extension = os.path.splitext(c)[1] # saves the file extension (".tif")
				new_file_name = folder +"_stru__"+ str(count) #
				new_file_name_with_ext = new_file_name+extension
				renameto = addsource + "/" + new_file_name_with_ext
				renamefrom = addsource + "/" + c
				if (renamefrom == renameto):
					count = count + 1
				else:
					os.rename(renamefrom, renameto)
					count = count + 1
				### end of renaming function
				if (c.endswith(".tif")):
					addsave1 = save1 + "/" + folder
					addsave2 = save2 + "/" + folder
					if not os.path.exists(addsave1):  # if save folder already exists
						os.makedirs(addsave1)  # creates new folder with the same folder name and directory structure in the save directory
					if not os.path.exists(addsave2):
						os.makedirs(addsave2)
#print(l)
print("Finished!")
