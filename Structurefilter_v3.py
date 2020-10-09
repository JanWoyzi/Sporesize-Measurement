from ij import IJ #for imageJ relevant functions
import os #for operation system relevant functions
# preinstalled FeatureJ plugin in ImageJ is needed!
# preinstalled BioVoxxel plugin in ImageJ is needed!


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
    save = "G:/folder_lvl01/folder_lvl02/folder_lvl03/1_Separation/" + multi  # directory location for processed images

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
        if (folder.endswith(".tif")): # preventing that imageJ process non-.tiff files
            print("Why is here a tif!")
            print(source)
        else :
            addsource = source + "/" + folder # creates new folder with the same folder name and directory structure in the save directory
            list3 = os.listdir(addsource) # catches all images in now processed folder
            for img in list3:
                if (img.endswith(".tif")):
                    addsave = save + "/" + folder
                    if not os.path.exists(os.path.join(addsave, img[:-4]) + "_stru.tif"): # processed images get renamed based on their old (raw) name and "_stru" gets attached at the end
                        imp = IJ.openImage(os.path.join(addsource, img))
                        raw = IJ.openImage(os.path.join(addsource, img)) # double open image for overlaying step later on (line 60)
                        print("Processing", img)
                        if imp is None:
                            print("Could not open image from file:", img)# If this print out appears then probably the file-format is wrong; ...
						# on "c"-level .tiff-files are expected
                        else:
                            IJ.run(imp, "16-bit", "") # turns image in to a 16 bit grey image
                            IJ.run(imp, "FeatureJ Structure", "smallest smoothing=1.0 integration=3.0") # will create two short lines between touching points of spores on the background ; preinstalled FeatureJ plugin in ImageJ is needed!
                            imp = IJ.getImage()
                            IJ.setAutoThreshold(imp, "Otsu no-reset Prefs.blackBackground=true") # applies threshold filter with setting the background to black; result: binary image (important!)
                            IJ.run(imp, "Convert to Mask", "")
                            IJ.run(imp, "Watershed Irregular Features", "erosion=25 convexity_threshold=0 separator_size=0-60") # bridging the pairwise results from featureJ (line 52) together, resulting into a separating line running between to spores; preinstalled BioVoxxel plugin in ImageJ is needed!
                            IJ.setAutoThreshold(imp, "Otsu no-reset Prefs.blackBackground=False") # result: binary image
                            IJ.run(imp, "Convert to Mask", "")
                            IJ.run(imp, "Skeletonize (2D/3D)", "") # thin down the separation lines to 1 pixel
                            IJ.run(imp, "Create Selection", "")
                            IJ.run(imp, "Make Inverse", "") # all separation lines are now in the selection
                            raw.show()
                            IJ.run(raw, "Restore Selection", "") # overlay selected separation lines on the raw image
                            IJ.setForegroundColor(255, 255, 255) # turn color of separation lines to white
                            IJ.run(raw, "Fill", "slice")
                            IJ.run(raw, "Select None", "") # deselect
                            if not os.path.exists(addsave): # if save folder already exists
                                os.makedirs(addsave) # creates new folder with the same folder name and directory structure in the save directory
                            IJ.saveAs(raw, "Tiff", os.path.join(addsave, img[:-4]) + "_stru.tif") # saves result image
                            IJ.run("Close")
                            IJ.run("Close") # double close is necessary! don't comment or delete this line
print("Finished!")