#! python3
# imgcomp.py

import os, sys
import datetime
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
import easygui as eg

def get_exif(fn):
    """Returns Dict of picture exif data with
    associated descriptive names
    """
    ret = {}
    gps = {}

    try:
        i = Image.open(fn)

        info = i._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value

        try:
            gpsInfo = ret["GPSInfo"]
            for tag, value in gpsInfo.items():
                decoded = GPSTAGS.get(tag,tag)
                gps[decoded] = value

            ret["GPSInfo"] = gps

        except:
            ret["GPSInfo"] = None

    except:
        ret = None

    return ret

def get_float(x):
    return float(x[0])/float(x[1])

def lat(dt):
    """Returns latitude (decimal degrees) from PIL formated exif data"""
    d = get_float(dt["GPSInfo"]['GPSLatitude'][0])
    m = get_float(dt["GPSInfo"]['GPSLatitude'][1])
    s = get_float(dt["GPSInfo"]['GPSLatitude'][2])

    return d + (m/60.0) + (s/3600.0)

def long(dt):
    """Returns longitude (decimal degrees) from PIL formated exif data"""
    d = get_float(dt["GPSInfo"]['GPSLongitude'][0])
    m = get_float(dt["GPSInfo"]['GPSLongitude'][1])
    s = get_float(dt["GPSInfo"]['GPSLongitude'][2])

    return d + (m/60.0) + (s/3600.0)

def compress(fn,qual=70,cfn=True,movDir=None):
    """Compress Image with Pillow module
    cfn - if True will add _comp extension to file name
    qual - sets quality of image upon save
    """

    # file path, file name and file ending
    fnP,fn = os.path.split(fn)
    fnS, fnE = os.path.splitext(fn)
    fnS = fnS.split("\\")[-1]

    exif = get_exif(fnP + "\\" + fn) # Get exif data
    photo = Image.open(fnP + "\\" + fn)
    exifBytes = photo.info['exif']

    # If new location for file was set
    if movDir !=None:
        fnP = movDir

    # Save photo
    if cfn:
        fn = fnP + "\\" + fnS + "_comp" + fnE
        photo.save(fn,"JPEG",optimize=True,quality=qual,exif=exifBytes)
    else:
        fn = fnP + "\\" + fnS + fnE
        photo.save(fn,"JPEG",optimize=True,quality=qual,exif=exifBytes)

    # Log of pictures that have been compressed
    currentTime = str(datetime.datetime.now())
    logPath,pyFile = os.path.split(os.path.realpath(__file__))

    # Test if log exists
    if os.path.exists(logPath+"\\"+"log.txt"):
        appendWrite = 'a'
    else:
        appendWrite = 'w'

    # Wrtie compressed file to log
    f = open(logPath+"\\"+"log.txt",appendWrite)
    f.write(currentTime + " " + fn + "\n")
    f.close()

def find_jpg_files(folder, subs=False):
    """Finds all .jpg, and .jpeg files in folder and returns list
    folder - location of folder with pictures in it
    subs - if True, will include all .png in all sub folders"""

    picList = []

    # Types of images files that are selected
    types = ['.jpg','jpeg']

    if subs == False:
        for file in os.listdir(folder):
            if os.path.splitext(file)[1].lower() in types:
                picList.append(folder + "\\" + file)

    else:
        for folder, sub, files in os.walk(folder):
            for file in files:
                if os.path.splitext(file)[1].lower() in types:
                    picList.append(folder + "\\" + file)

    return picList

if __name__ == "__main__":
    title = 'Image Compress' #Title for popup boxes

    # Show message of welcome
    tell = eg.msgbox("Welcome! Start Compressing Your Images",image="ViceGripPic.png")
    
    # Show message to make selection of one image, mutiple images, or folder location
    selection = eg.choicebox(title=title,
                 msg="Please select what you want to compress",
                 choices=['One File','Multiple Files','Folder Location'])

    if selection == None: # Do nothing if nothing selected
        sys.exit()
    
    else:
        # Show message box based on previous selection
        if selection == 'One File':
            image = eg.fileopenbox(title=title,
                                   msg="Select image you want to compress")
        elif selection == "Multiple Files":
            imageLs = eg.fileopenbox(title=title,
                                     msg="Select images you want to compress",
                                     multiple=True)
        elif selection == "Folder Location":
            path = eg.diropenbox(title=title,
                                 msg="Selection folder location where images will be compressed")

            # Add window for chooice of selecting sub folders
            subs = eg.boolbox(title=title,
                              msg="Inculde all subfolders for image compression?")
            
        # Show message boxes indicating if files renamed
        paraRename = eg.boolbox(msg="Rename files with new _comp extension?")
        
        # Ask if selection is correct for renaming files
        if paraRename:
            tell = "want to rename files."
        else:
            tell = "don't want to rename files.\n(Original files will be overwritten if\nnew folder location is not selected in next window!)"
            
        sure = eg.boolbox(title=title,
                          msg="Confirm that you " + tell)

        if sure == False: # If no Confirmation Exit
            eg.msgbox(title=title,
                      msg="Did not complete compression.")
            sys.exit()

        # Ask if user whats to put the picture/s in a new location
        paraNewLoc = eg.boolbox(msg="Move files to new folder location when compressing?")

        if paraNewLoc:
            newLoc = eg.diropenbox(title=title,
                                   msg="Select destination location for compressed picture[s].")
            if newLoc == None:
                sys.exit()

        # Go About compressing images based on selection
        if selection == 'One File':
            # Picture location based on if new folder location was selected
            oldLoc,imageName = os.path.split(image)
            if paraNewLoc:
                compress(image,cfn=paraRename,movDir=newLoc)
            else:
                compress(image,cfn=paraRename)

            eg.msgbox(title=title,
                      msg="Completed compression of %s." % imageName)


        elif selection == "Multiple Files":
            # Picture locations based on if new folder location was selected
            if paraNewLoc:
                for pic in imageLs:
                    compress(pic,cfn=paraRename,movDir=newLoc)
            else:
                for pic in imageLs:
                    compress(pic,cfn=paraRename)
                            
            eg.msgbox(title=title,
                      msg="Completed compression of %d images." % len(imageLs))
        
        elif selection == "Folder Location":
            # Picture location based on if new folder location was selected
            if subs == True: # If looking in sub folders for images
                picList = find_jpg_files(path,subs=True)
                if paraNewLoc: # If moving files to new location
                    for pic in picList:
                        compress(pic,cfn=paraRename,movDir=newLoc)
                else:
                    for pic in picList:
                        compress(pic,cfn=paraRename)

            else:
                picList = find_jpg_files(path)
                if paraNewLoc: # If moving files to new location
                    for pic in picList:
                        compress(pic,cfn=paraRename,movDir=newLoc)
                else:
                    for pic in picList:
                        compress(pic,cfn=paraRename)

            eg.msgbox(title=title,
                      msg="Completed compression of %d images" % len(picList))

                
        
        












    
