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
from ij.plugin.frame import RoiManager
import os
import time
import gc
# preinstalled Ellipse Split plugin in ImageJ is needed!

def reemovNestings(l):  #removes nested or subfolder in a given (l)ist
    for i in l:
        if type(i) == list:
            reemovNestings(i)
        else:
            itemlist.append(i)

todolist = ["foldername01", "foldername02"] # processing a list of directories on the level of multiple folders
todoitem = ["test"] # filterlist: elements that should be included; if files were differently named

IJ1.batchMode = True
startTime = time.clock()

for multi in todolist:
    itemlist = []
    source = "G:/folder_lvl01/folder_lvl02/folder_lvl03/3_Destacked/" + multi   # directory location for images that should be processed (TIFF-format!)
    save = "G:/folder_lvl01/folder_lvl02/folder_lvl03/4_Elli_Results/" + multi  # directory location for processed images

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
    rm = RoiManager.getInstance() 
    for folder in itemlist:
        l = list()
        if (folder.endswith(".tif")):
            print("Why is here a tif!")# If this print out appears then you are giving him a too deep or too swallow level of directories; ...
			# ...on this level (folder) is the sample folder, in the sample folder are all the .tiff-files
            print(source)
        else :
            addsource = source + "/" + folder
            list3 = os.listdir(addsource)
            for c in list3:
                if (c.endswith(".tif")):
                    imp = IJ.openImage(os.path.join(addsource, c))
                    print("Processing", c)
                    if imp is None:
                        print("Could not open image from file:", c)# If this print out appears then probably the file-format is wrong; ...
						# on "c"-level .tiff-files are expected
                    else:
                        #IJ.run(imp, "Invert LUT", "") # depends on the operating system, feature "Analyze Particles" measures white pixels on black background
                        #IJ.run(imp, "Median...", "radius=3") # reduces the noise
                        IJ.setAutoThreshold(imp, "Intermodes dark no-reset Prefs.blackBackground=true") # applies threshold filter with setting the background to black; result: binary image (important!)
                        IJ.run(imp, "Convert to Mask", "")
                        IJ.run("Set Measurements...", "area mean centroid center perimeter fit shape feret's integrated "
                                                      "median display redirect=None decimal=3") # predefine what features should be measured
                        IJ.run(imp, "Ellipse Split", "binary=[Use standard watershed] add_to_manager add_to_results_table " # put the results in to the roi manager
                                                     "remove merge_when_relativ_overlap_larger_than_threshold overlap=50 " # exclude edge region and overlapping of objects by 50%
                                                     "major=50-Infinity minor=50-Infinity aspect=1-2") # measures everything bigger than 50 pixels and between an aspect ration of 1 to 2
                        rm = RoiManager.getInstance()
                        roicount = rm.getCount() # calls the amount of spores he found from ellipse split measurement
                        print(roicount)
                        if (rm.getCount()==0): # 0 = empty image; ignores this image and go further to the next image without saving
                                continue
                        else:
                            IJ.selectWindow("Results")
                            addsave = save + "/" + folder
                            if not os.path.exists(addsave): # if save folder already exists
                                os.makedirs(addsave) # creates new folder with the same folder name and directory structure in the save directory
                            IJ.run("Clear Results", "")
                            IJ.selectWindow("Results")
                            rm = RoiManager.getInstance()  # don't delete!
                            rm.runCommand(imp, "Show All with labels")
                            rm.runCommand(imp, "Measure")
                            IJ.selectWindow("Results")
                            IJ.saveAs("Results", os.path.join(addsave, c[:-4]) + "_ResultsElli.csv")
                            IJ.run("Clear Results", "")
                            imp2 = imp.flatten()
                            IJ.saveAs(imp2, "Tiff", os.path.join(addsave, c[:-4]) + "_resultElli.tif")
                            imp.close()
                        # following commands are making sure the roi manager is empty before the next image is loaded
                        # and "tries" to unload the memory for the next images (does not always work)
                        rm = RoiManager.getInstance()
                        rm.runCommand(imp, "Delete")
                        rm.runCommand("Reset")
                        rm.reset()
                        IJ.selectWindow("Results")
                        IJ.run("Close")
                        rm.close()
                        imp = None
                        imp2 = None
                        gc.collect()
                        IJ.run("Collect Garbage")
                    gc.collect()
                    IJ.run("Collect Garbage")
IJ1.batchMode = False
print(time.clock() - startTime, "seconds")
print("Done!")
