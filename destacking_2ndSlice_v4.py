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

from ij import IJ
import os

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
    source = "G:/folder_lvl01/folder_lvl02/folder_lvl03/2_Weka/" + multi   # directory location for images that should be processed (TIFF-format!)
    save = "G:/folder_lvl01/folder_lvl02/folder_lvl03/3_Destacked/" + multi  # directory location for processed images

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
			print(source)
		else :
			addsource = source + "/" + folder
			list3 = os.listdir(addsource)
			for c in list3:
				if (c.endswith(".tif")):
					print("Processing", c)
					imp = IJ.openImage(os.path.join(addsource, c))
					addsave = save + "/" + folder
					if imp is None:
						print("Could not open image from file:", c)# If this print out appears then probably the file-format is wrong; ...
						# on "c"-level .tiff-files are expected
					else:
						imp.setSlice(1) # change between "1" or "2" depending which slice should be deleted!
						IJ.run(imp, "Delete Slice", "")
						if not os.path.exists(addsave): # if save folder already exists
							os.makedirs(addsave) # creates new folder with the same folder name and directory structure in the save directory
						IJ.saveAs(imp, "Tiff", os.path.join(addsave, c[:-4]) +"_destack.tif")
print("Finished!")
