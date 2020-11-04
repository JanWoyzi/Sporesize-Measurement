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
from ij.macro import Interpreter as IJ1
import os
import time
import gc
import re

#function to sort elements in the list(data) alphanumerically:
def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)

def reemovNestings(l):  #removes nested or subfolder in a given (l)ist
    for i in l:
        if type(i) == list:
            reemovNestings(i)
        else:
            itemlist.append(i)

todolist = ["foldername01", "foldername02"] # processing a list of directories on the level of multiple folders
todoitem = ["test"] # filterlist: elements that should be included; if files were differently named

IJ1.batchMode=True
startTime = time.clock()

for multi in todolist:
    itemlist = []
    source = "G:/folder_lvl01/folder_lvl02/folder_lvl03/0_Raw/" + multi   # directory location for images that should be processed (TIFF-format!)
    save = "G:/folder_lvl01/folder_lvl02/folder_lvl03/IScores/" + multi  # directory location for processed images

   # l = list()
    itlist = []
    list2 = sorted_aphanumeric(os.listdir(source)) # creates list of files based on source directory
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
		else:
			addsource = source + "/" + folder
			list3 = sorted_aphanumeric(os.listdir(addsource))
			for c in list3:
				if (c.endswith(".tif")):
					imp = IJ.openImage(os.path.join(addsource, c))
					print("Processing", c)
					if imp is None:
						print("Could not open image from file:", c)# If this print out appears then probably the file-format is wrong; ...
						# on "c"-level .tiff-files are expected
					else:
						IJ.run(imp, "16-bit", "")  # turns image in to a 16 bit grey image
						IJ.run("Set Measurements...", "mean modal min median display nan redirect=None decimal=3") # predefine what features should be measured; in the evaluation (with R) "label" and "mode"-value is taken
						IJ.run(imp, "Measure", "")
						imp.close()
			IJ.selectWindow("Results")
			addsave = save + "/" + folder
			if not os.path.exists(save): # if save folder already exists
				os.makedirs(save) # creates new folder with the same folder name and directory structure in the save directory
			IJ.selectWindow("Results")
			IJ.saveAs("Results", os.path.join(addsave) + "_IScore.csv")
			IJ.run("Clear Results", "")
			IJ.selectWindow("Results")
			IJ.run("Close")
IJ1.batchMode=False
print(time.clock() - startTime, "seconds")
print("Done!")
