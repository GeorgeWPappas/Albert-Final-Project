import logging

import azure.functions as func

# Extract EXIF Data
def ExtractGPSDictionary(fileName):
    # Open the image.
    try:
        pilImage = Image.open(fileName)
        exifData = pilImage._getexif()
    except IOError:
        # If exception occurs from PIL processing
        print("Failed to open image file {}".format(fileName))
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

# Extract the Latitude and Longitude Values
def ExtractLatLon(gps):
    if (("GPSLatitude" in gps) and ("GPSLongitude" in gps) and ("GPSLatitudeRef" in gps) and ("GPSLongitudeRef" in gps)):
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

# Convert GPSCoordinates to Degrees
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
# End ConvertToDegrees ===========================

# Main function.
def start():
    # Offsets into the return EXIFData for
    # TimeStamp, Camera Make and Model
    TS = 0
    MAKE = 1
    MODEL = 2

    print("===== Program Start =====")
    print()

    targetFile = 'IMG_7867 copy.jpeg'   # File name.

    try:
        gpsDictionary, exifList = ExtractGPSDictionary(targetFile)
    except TypeError:
        gpsDictionary = None
        exifList = None

    if (gpsDictionary):
        # Obtain the Lat Lon values from the gpsDictionary
        # Converted to degrees
        # The return value is a dictionary key value pairs
        dCoor = ExtractLatLon(gpsDictionary)

        lat = dCoor.get("Lat")
        latRef = dCoor.get("LatRef")

        lon = dCoor.get("Lon")
        lonRef = dCoor.get("LonRef")

        alt = dCoor.get("Alt")
        altRef = dCoor.get("AltRef")

        if (lat and lon and latRef and lonRef):
            if (alt and altRef):
                print(targetFile+':')
                print('     '+'Latitude:   '+str(latRef)+'  '+str(lat))
                print('     '+'Longitude:  '+str(lonRef)+'  '+str(lon))
                print('     '+'Altitude:      '+str(alt))
            else:
                print(targetFile+':')
                print('     '+'Latitude:   '+str(latRef)+'  '+str(lat))
                print('     '+'Longitude:  '+str(lonRef)+'  '+str(lon))
                print('     '+'Altitude:      '+'No ALT Data')
        else:
            print(targetFile+':')
            print('     '+'Latitude:  '+'No LAT Data')
            print('     '+'Longitude: '+'No LON Data')
            print('     '+'Altitude:  '+'No ALT Data')
    else:
        print(targetFile+':')
        print('     '+'Latitude:  '+'No LAT Data')
        print('     '+'Longitude: '+'No LON Data')
        print('     '+'Altitude:  '+'No ALT Data')

    print()
    print("===== Program End =====")
    print()
# End Main function ===========================

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
