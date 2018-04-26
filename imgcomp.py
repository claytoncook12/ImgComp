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

def compress(fn,qual=70,cfn=True):
    """Compress Image with Pillow module
    If cfn is True will add _comp extension to file name
    """

    # file path, file name and file ending
    fnP,fn = os.path.split(fn)
    fnE = fn.split(".")[-1]
    fnS = fn.split(".")[0]

    exif = get_exif(fnP + "\\" + fn) # Get exif data
    photo = Image.open(fnP + "\\" + fn)
    exifBytes = photo.info['exif']

    # Save photo
    if cfn:
        photo.save(fnP + "\\" + fnS + "_comp." + fnE,"JPEG",optimize=True,quality=qual,exif=exifBytes)
    else:
        photo.save(fnP + "\\" + fnS + "." + fnE,"JPEG",optimize=True,quality=qual,exif=exifBytes)        

if __name__ == "__main__":
    imageLocal = easygui.fileopenbox(msg="Select image you want to compress?")

    compress(imageLocal)

        












    
