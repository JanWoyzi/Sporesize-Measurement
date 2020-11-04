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

from ij import IJ #for imageJ relevant functions
from ij.plugin.frame import RoiManager #for imageJ ROI manager relevant functions
import os #for operation system relevant functions


task = ["foldername01", "foldername02"]

for multi in task:
	print(multi)
	# These directories are given:
	segmented = "G:/folder_lvl01/folder_lvl02/folder_lvl03/2_Destacked/" + multi  # segmented images (binary images) (.tiff-files)
	raw = "G:/folder_lvl01/folder_lvl02/folder_lvl03/1_Separation/" + multi  # raw images or raw images with the structure filter (.tiff-files)
	# These directories will be generated:
	save = "G:/folder_lvl01/folder_lvl02/folder_lvl03/3_Paana/Results/" + multi # directory location for the results (.csv-files)
	rgbROI = "G:/folder_lvl01/folder_lvl02/folder_lvl03/3_Paana/RGB_ROI/" + multi # directory location for saving the selection from the roi manager of imageJ (.zip-files)
	for (dirpath, dirnames, filenames) in os.walk(segmented):
		if dirpath[-1] == "#" or dirpath[-1] == "x" or dirpath[-3:] == "__2":  # filter: folder "dirpath" with a "x", "__2" or "#" at their ends will be excluded
			continue
		else:
			for name in filenames:
				print(os.path.join(dirpath, name))
				if name.endswith(".tif"):
					imp = IJ.openImage(os.path.join(dirpath, name))
					if imp is None:
						print("Could not open image from file:", name)# If this print out appears then probably the file-format is wrong; ...
						# on "c"-level .tiff-files are expected
					else:
						IJ.setAutoThreshold(imp, "Intermodes dark no-reset Prefs.blackBackground=true") # applies threshold filter with setting the background to black; result: binary image (important!)
						IJ.run(imp, "Convert to Mask", "")
						IJ.run(imp, "Watershed", "") # to improve the separation line between spores and reduces dirt particles sizes further
						IJ.run(imp, "Open", "") # convert free single pixel points to nackground, noise reduction
						IJ.run(imp, "Analyze Particles...", "size=50-Infinity exclude add") # analyses the particles, excluding everything that is smaller than 50 pixel and on the edge of the image...
						#... this step will create a list of all spores in the images and gives them an ID
						x = dirpath.split("\\")
						rm = RoiManager.getInstance() # take control to roi manager of imageJ
						if (rm == None): # checks if roi manager is already open, if not he will open it
							rm = RoiManager()
						if (os.path.isdir(rgbROI + "/" + x[1])): # checks if save path with new name already exist; x[1] should be the foldername where all files are or should be...
							#...depending from the operating system (Linux, Windows, etc.) the last foldername can be extracted by x[1] or x[-1]; this issue is connected with line 17 and 34
							rm.runCommand("Save", os.path.join(rgbROI + "/" + x[1], name[:-4]) + "_sel.zip") # saves selection in existing directory
						else:
							os.makedirs(rgbROI + "/" + x[1]) # creates a new directory before the results are saved
							rm.runCommand("Save", os.path.join(rgbROI + "/" + x[1], name[:-4]) + "_sel.zip") # saves selection in existing directory
						imp.close()
						# now for every spores their color value (for each channel in RGB) gets analyzed
						list01 = os.listdir(raw + "/" + x[1]) # makes a list from all raw (unprocessed and rgb) images that should be analyzed
						y = name.split("__")[1] # line 47 and 48 extract the index number of each processed image from the image name
						z = int(y.split("_")[0])-1
						imp = IJ.openImage(os.path.join(raw + "/" + x[1], list01[z])) # this number is used to open the corresponding raw image
						IJ.run(imp, "RGB Stack", "") # splits the images into his three rgb channels
						IJ.run("Set Measurements...",
							   "area mean standard modal min centroid perimeter bounding fit shape feret's median display nan redirect=None decimal=3") # predefine what features should be measured
						imp.setSlice(1) # selects first rgb channel
						rm.runCommand(imp, "Measure") # measures features
						imp.setSlice(2) # selects second rgb channel
						rm.runCommand(imp, "Measure")
						imp.setSlice(3) # selects third rgb channel
						rm.runCommand(imp, "Measure")
						rm.reset()
						addsave = save + "/" + x[1]
						if not (os.path.isdir(addsave)):
							os.makedirs(addsave) # creates new folder with the same folder name and directory structure in the save directory
						### comment for headless mode, he will save it in the slurm report
						IJ.selectWindow("Results")# <-- deactivate for headless mode
						IJ.saveAs("Results", os.path.join(addsave, name[:-4]) +"_Results.csv") # saves the results as .csv-file
						IJ.run("Clear Results", "") # necessary or he will continually add more and more spores in to his list
						IJ.run("Close")#
						### end of headless case
						imp.close()
		print("Finished!")
