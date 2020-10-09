from ij import IJ
from ij.plugin.frame import RoiManager
from ij.gui import Roi  
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
    source = "G:/folder_lvl01/folder_lvl02/folder_lvl03/3_Destacked/" + multi   # directory location for images that should be processed (TIFF-format!)
    save = "G:/folder_lvl01/folder_lvl02/folder_lvl03/4_Paana_Results/" + multi  # directory location for processed images

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
			print("Why is here a tif!") # If this print out appears then you are giving him a too deep or too swallow level of directories; ...
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
						print("Could not open image from file:", c) # If this print out appears then probably the file-format is wrong; ...
						# on "c"-level .tiff-files are expected
					else:
	#					IJ.run(imp, "Invert LUT", "") # depends on the operating system, feature "Analyze Particles" measures white pixels on black background
						IJ.run(imp, "Median...", "radius=3") # reduces the noise
						IJ.setAutoThreshold(imp, "Intermodes dark no-reset Prefs.blackBackground=true") # applies threshold filter with setting the background to black; result: binary image (important!)
						IJ.run(imp, "Convert to Mask", "")
						IJ.run(imp, "Dilate", "") # line 53 - 56: will reduce further noise particles and closes some gaps
						IJ.run(imp, "Dilate", "")
						IJ.run(imp, "Erode", "")
						IJ.run(imp, "Erode", "")
						IJ.run(imp, "Watershed", "") # reinforce separation line between spores (from structurefilter script) and cut down some dirt particles (creates low circularity objects)
						IJ.run("Set Measurements...", "area mean centroid center perimeter fit shape feret's integrated median display redirect=None decimal=3") # predefine what features should be measured
						IJ.run(imp, "Analyze Particles...", "size=1500-Infinity show=Outlines display exclude clear in_situ") # measures everything bigger than 1500 pixels and exclude the edge region
						addsave = save + "/" + folder
						if not os.path.exists(addsave): # if save folder already exists
							os.makedirs(addsave) # creates new folder with the same folder name and directory structure in the save directory
						### comment for headless mode, he will save it in the slurm report
	#					IJ.selectWindow("Results")# <-- deactivate for headless mode, he will save it in the slurm report
	#					IJ.saveAs("Results", os.path.join(addsave, c[:-4]) +"_Resultsb.csv")
	#					IJ.run("Clear Results", "")
	#					IJ.run("Close")
						### end of headless case
						IJ.saveAs(imp, "Tiff", os.path.join(addsave, c[:-4]) +"_resultpaana.tif")
						imp.close()
print("Finished!")
