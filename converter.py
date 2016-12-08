#!/usr/bin/python
import os
from  os.path import isdir, join
import sys
import re
import multiprocessing
from concurrent import futures
import time
tif_folder="source folder with subfolders and tif images"
jpeg_destination="destination folder for jpg files"
start_time=time.time()

def sipper(n):
	global raw_folder
	global jpeg_destination
	yTrunc = re.sub(r'....$', "", n)
	result=os.system("convert  \""+tif_folder + n + "\"  \""+jpeg_destination + yTrunc + ".jpg\" > /dev/null" )
	if result==0:
         print "File "+tif_folder+n+" converted succesfuly!"
	else:
         print "Error on converting "+tif_folder+n+" error code= "+result  

def convert_from_folder(root='notes'):
    """
    Collect all directories from root path and files from subdirectories
    and converts all the files to sipper settings.
    """
    global jpeg_destination
    i=0
    categories = filter(lambda d: isdir(join(root, d)), os.listdir(root))
    print categories
    for c in categories:
      if c:
	 if not os.path.exists(jpeg_destination+c):
          os.mkdir(jpeg_destination+c,777)
         dirContent=os.listdir(root+c)
         pictures=( c+"/"+s for s in dirContent)
	 imagepathscleaned = pictures
         with futures.ProcessPoolExecutor() as executor:
           zip(imagepathscleaned, executor.map(sipper, imagepathscleaned))
         i+=len(dirContent)  
    return "Job converting "+str(i)+" files finished in "+str((time.time()-start_time))+" with "+str((time.time()-start_time)/i)+" seconds per image "

if tif_folder!="": 
	print convert_from_folder(tif_folder)
