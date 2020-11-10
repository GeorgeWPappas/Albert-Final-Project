#
# Data Extraction - Python-Forensics
# Extract GPS Data from EXIF supported Images (jpg, tiff)
# Support Module
#

# Import Declarations.
import os       # Standard Library OS functions
from classLogging import _ForensicLog       # Abstracted Forensic Logging Class
from PIL import Image   # import the Python Image Library
from PIL.ExifTags import TAGS, GPSTAGS  # along with TAGS and GPS related TAGS

#
# Extract EXIF Data
#
# Input: Full Pathname of the target image
#
# Return: gps Dictionary and selected EXIFData list
#
def ExtractGPSDictionary(fileName):

    # Open the image.
    try:
        pilImage = Image.open(fileName)
        exifData = pilImage._getexif()
    except IOError:
        # If exception occurs from PIL processing
        print("Failed to open image file {}".format(fileName)) # Update 1.1
        return None, None

    # Iterate through the EXIFData
    # Searching for GPS Tags
    # Set default values for some image attributes.
    imageTimeStamp = "NA"
    CameraModel = "NA"
    CameraMake = "NA"

    # Only bother if the image has exif data.
    if exifData:
        # Iterate through the values in the exif dictionary.
        for tag, theValue in exifData.items():
            tagValue = TAGS.get(tag, tag)   # obtain the tag

            # Collect basic image data if available
            if tagValue == 'DateTimeOriginal':
                imageTimeStamp = exifData.get(tag)

            if tagValue == 'Make':
                cameraMake = exifData.get(tag)

            if tagValue == 'Model':
                cameraModel = exifData.get(tag)
            
            # check the tag for GPS
            if tagValue == "GPSInfo":
                # Found it !
                # Now create a Dictionary to hold the GPS Data
                gpsDictionary = {}

                # Loop through the GPS Information
                for curTag in theValue:
                    gpsTag = GPSTAGS.get(curTag, curTag)
                    gpsDictionary[gpsTag] = theValue[curTag]    # Add the text name and value to our dictionary.

                basicExifData = [imageTimeStamp, cameraMake, cameraModel]
                return gpsDictionary, basicExifData    
    else:
        return None, None
# End ExtractGPSDictionary ===========================

#
# Extract the Latitude and Longitude Values
# From the gpsDictionary
#
def ExtractLatLon(gps):
    # to perform the calculation we need at least
    # lat, lon, latRef and lonRef

    if (("GPSLatitude" in gps) and ("GPSLongitude" in gps) and ("GPSLatitudeRef" in gps) and ("GPSLongitudeRef" in gps)):   # Update 1.1: Changed syntax.
        latitude = gps["GPSLatitude"]
        latitudeRef = gps["GPSLatitudeRef"]
        longitude = gps["GPSLongitude"]
        longitudeRef = gps["GPSLongitudeRef"]

        lat = ConvertToDegrees(latitude)
        lon = ConvertToDegrees(longitude)

        # Check Latitude Reference
        # If South of the Equator then lat value is negative
        if latitudeRef == "S":
            lat = 0 - lat

        # Check Longitude Reference
        # If West of the Prime Meridian in
        # Greenwich then the Longitude value is negative
        if latitudeRef == "W":
            lat = 0 - lon

        # Update 1.1: Added support for altitude.
        if (("GPSAltitude" in gps) and ("GPSAltitudeRef" in gps)):
            altitude = gps['GPSAltitude']
            altitudeRef = gps['GPSAltitudeRef']
            
            gpsCoor = {"Lat": lat, "LatRef":latitudeRef, "Lon": lon, "LonRef": longitudeRef, "Alt": altitude, "AltRef": altitudeRef}
        else:
            gpsCoor = {"Lat": lat, "LatRef":latitudeRef, "Lon": lon, "LonRef": longitudeRef, "Alt": '', "AltRef": ''}
        # End Update 1.1 ===========================

        return gpsCoor
    else:
        return None
# End Extract Lat Lon ===========================

#
# Convert GPSCoordinates to Degrees
#
# Input gpsCoordinates value from in EXIF Format
#
def ConvertToDegrees(gpsCoordinate):
    deg, mins, secs = gpsCoordinate

    try:
        degrees = float(deg)
    except:
        degrees = 0.0

    try:
        minutes = float(mins)
    except:
        minutes = 0.0

    try:
        seconds = float(secs)
    except:
        seconds = 0.0

    floatCoordinate = float(degrees + (minutes / 60.0) + (seconds / 3600.0))

    return floatCoordinate
