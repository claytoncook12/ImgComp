#! python3
# imgcomp.py

import os
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
import easygui

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

        gpsInfo = ret["GPSInfo"]
        for tag, value in gpsInfo.items():
            decoded = GPSTAGS.get(tag,tag)
            gps[decoded] = value

        ret["GPSInfo"] = gps

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

if __name__ == "__main__":
    #imageLocal = "IMG_20180331_142343.jpg"
    imageLocal = easygui.fileopenbox(msg="Select image you want to compress?",
                                     title="Title Is Here")

    exif = get_exif(imageLocal)
    
    print("Image lat data display before file size reduction:")
    print(exif["GPSInfo"]["GPSLatitude"])
    print("Lat data is: ",lat(exif))

    photo = Image.open(imageLocal)
    print("Dim of photo: ",photo.size)
    print("Size of photo before compression :",os.stat(imageLocal).st_size)
    exifBytes = photo.info['exif']

    print("Now compressing image\n")
    photo.save("IMG_comp.jpg","JPEG",optimize=True,quality=70,exif=exifBytes)
    photoComp = Image.open("IMG_comp.jpg")
    print("Dim of photo after compression: ",photoComp.size)
    print("Size of photo after compression :",os.stat("IMG_comp.jpg").st_size)
    print("File size reduction is: {0:.2f}\n".format(os.stat("IMG_comp.jpg").st_size /
          os.stat(imageLocal).st_size))

    exifComp = get_exif("IMG_comp.jpg")
    print("Image lat data display after file size reduction:")
    print("Lat data after compression: \n",exifComp["GPSInfo"]["GPSLatitude"])
    print("Lat data is: ",lat(exifComp))
        












    
