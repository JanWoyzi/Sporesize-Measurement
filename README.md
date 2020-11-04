# Supplement 2 of:
# More than just diameter: a workflow for automated image analysis of spore shapes in myxomycetes

*Jan Woyzichovski<sup>1</sup>, Oleg N. Shchepin<sup>1,2</sup>, Nikki H.A Dagamac<sup>1,3</sup> and Martin Schnittler<sup>1</sup>

*<sup>1</sup> Institute of Botany and Landscape Ecology, Greifswald University, Soldmannstr. 15, D-17487 Greifswald, Germany*

*<sup>2</sup> Komarov Botanical Institute of the Russian Academy of Sciences, Laboratory of Systematics and Geography of Fungi, 
Prof. Popov Street 2, 197376 St. Petersburg, Russia*

*<sup>3</sup> Department of Biological Sciences and Research Center for the Natural and Applied Sciences, University of Santo Tomas, Manila, Philippines*

*Corresponding author: Jan Woyzichovski, e-mail: jan.woyzichovski@uni-greifswald.de

**DOI: Doitestdoitest**

The article can be found on [Link to Journal.](http://google.com) (*links to google, right now*)

## Abstract
Measuring spore size is a standard method for the description of fungal taxa, but results in nothing more than a size range. We present a method to analyze the shape of large quantities of spherical bodies, like spores or pollen, without using expensive equipment. A spore suspension mounted at a slide is treated with a high-vibration device to achieve a uniform distribution of spores. Subsequent automated image processing allows to measure between 10 000 and 50 000 spores per slide. One result is a size distribution of spores, which can yield a lot of additional information, as shown on the example of the slime mold *Physarum albescens*. The exact distribution curves for spore size reveal irregularities in spore formation, as a result of the influence of environmental conditions on spore maturation. A comparison of the spore size distribution curves within and between colonies of sporocarps shows a high degree of environmental variation together with apparent genetic variation. In addition, some of the specimens have a proportion of apparently unreduced spores, which have roughly twice the volume of normal spores. Here we give a detailed guideline for slide preparation and image processing scripts, which can be universally used for spherical bodies like spores or pollen grains, and describe conceivable applications.

## Description
This is supplement 2 of the work, as mentioned above. 
These scripts provide the user the ability to analyze the shape of large quantities of spherical bodies, like spores or pollen, with the usage of ImageJ software. Prepared microscopy slides with the sample are scanned in, and the resulting images can be fed to ImageJ with these scripts. 
Within the repository, all scripts created and used for this work are listed. The general workflow for this method and order of scripts can be seen in Figure 1.
In general, these scripts can be fused together if the results are satisfactory. It is designed so that every significant image processing step is separate and can be checked for correctness. 
![Image of Workflow](https://github.com/JanWoyzi/Sporesize-Measurement/blob/main/ImgForReadme/workflow-02.png) 
*Figure 1: Workflow overview from sample preparation to data acquisition. See Table 1 for the respective scripts.*

*Table 1 Scripts used for image analysis. Underlined scripts are crucial for the results of the analysis. The column D/S indicates if the respective calculations are desktop (D) or server (S) based.*

Script name	 | S/D |	Script function
-------------|-|-----------------
IScore.py |	D |	Assesses background intensities (calculates a score for background intensity by mixing RGB values into a greyscale; figure must be comparable for all images)
BScore_v2.py |	D |	Calculates a score for spore density from the brightness of the total area covered by spores
CreatingDir.py | S/D	| A script designed to build directories for scripts (for instance, Elli.py) that cannot create them automatically
Structurefilter_v3.py |	S/D	| Detects edges of and sharp angles between objects to separate them by a regional watershed line; the result is an image with overlaid separation lines between spores; necessary for handling images with high spore density
Weka.py |	S/D |	Machine Learning algorithm, works with a pre-trained model to recognize objects (as differently colored patches of pixels); the result is a classification probability of each pixel as spore or background (more than two classes can be defined as well); this is presented as a stacked image (one for each class)
Destacking_2ndSclice_v4.py |	S/D  |	Separates the Weka segmentation stack (here two classes, i.e., spores and background) and saves the relevant results
ParticleAnalyzer_v5.py |	S/D |	Particle Analyzer, analyzes spore shapes, describes features like circularity, roundness, etc. (does not use a pre-defined shape, therefore more sensitive but requires precise segmentation)
Elli_v6.py |	D	| Ellipse Split plugin (alternative algorithm to Paana.py), analyses the spore shapes according to a pre-defined ellipsoid shape (less sensitive to a particular shape, since measurements are based on approximated ellipses), more robust in case of segmentation errors. Both algorithms are alternatives; in each case, the result is an array of object features which can be further evaluated (or filtered to exclude non-target objects)
RGBSporesV2.py |	S/D	| Additional script, allows extracting area-related object features (e.g., RGB values) by comparison with the raw image

*Within the scripts important command lines are further explained and with additional options presented.*


## Code Review
This repository has not undergone code review only by the corresponding author. This notice will be removed once the repository has undergone proper review.

## Acknowledgements
OS received support from the Russian Foundation for Basic Research (project 18-04-01232 А) and the state task of BIN RAS ‘Biodiversity, ecology, structural and functional features of fungi and fungus-like protists’ (АААА-А19-119020890079-6).
Funding for this study was provided in the frame of a PhD position for JW within the Research Training Group RESPONSE (RTG 2010), supported by the Deutsche Forschungsgemeinschaft (DFG).
