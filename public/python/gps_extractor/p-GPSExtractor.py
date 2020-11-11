#
# Modifier: George Pappas
# Last Modified Date: October 20, 2020
# Version 1.1
#
# GPS Extraction
# Python-Forensics
# No HASP required
#

# Import Declarations.
import os
import _modEXIF
import _csvHandler
import _commandParser
from classLogging import _ForensicLog

# Offsets into the return EXIFData for
# TimeStamp, Camera Make and Model
TS = 0
MAKE = 1
MODEL = 2

# Process the Command Line Arguments
userArgs = _commandParser.ParseCommandLine()

# create a log object
logPath = userArgs.logPath + "ForensicLog.txt"
oLog = _ForensicLog(logPath)

oLog.writeLog("INFO", "Scan Started")

csvPath = userArgs.csvPath + "imageResults.csv"
oCSV = _csvHandler._CSVWriter(csvPath)

# define a directory to scan
scanDir = userArgs.scanPath
try:
    picts = os.listdir(scanDir)
except:
    oLog.writeLog("ERROR", "Invalid Directory: " + scanDir)
    exit(0)

print("Program Start")
print()

for aFile in picts:
    targetFile = scanDir + aFile

    if os.path.isfile(targetFile):

        # Update 1.1
        try:
            gpsDictionary, exifList = _modEXIF.ExtractGPSDictionary(targetFile)
        except TypeError:
            gpsDictionary = None
            exifList = None
        # End Update 1.1 ===========================

        if (gpsDictionary):
            # Obtain the Lat Lon values from the gpsDictionary
            # Converted to degrees
            # The return value is a dictionary key value pairs
            dCoor = _modEXIF.ExtractLatLon(gpsDictionary)

            lat = dCoor.get("Lat")
            latRef = dCoor.get("LatRef")

            lon = dCoor.get("Lon")
            lonRef = dCoor.get("LonRef")

            alt = dCoor.get("Alt")  # Update 1.1
            altRef = dCoor.get("AltRef")    # Update 1.1

            if (lat and lon and latRef and lonRef):
                if (alt and altRef):    # Update 1.1
                    print(aFile+': '+str(lat)+', '+str(lon)+', '+str(alt))

                    # Write one row to the output file.
                    oCSV.writeCSVRow(targetFile, exifList[TS], exifList[MAKE], exifList[MODEL], latRef, lat, lonRef, lon, altRef, alt)
                    oLog.writeLog("INFO", "GPS Data Calculated for: " + targetFile)
                else:
                    print(aFile+': '+str(lat)+', '+str(lon)+', '+'No ALT Data')

                    # write one row to the output file
                    oCSV.writeCSVRow(targetFile, exifList[TS], exifList[MAKE], exifList[MODEL], latRef, lat, lonRef, lon, 0, 0)
                    oLog.writeLog("INFO", "GPS Data Calculated for: " + targetFile)
            else:
                oLog.writeLog("WARNING", "No GPS EXIF Data for: " + targetFile)
                print(aFile + ": No GPS EXIF Data") # Update 1.1
        else:
            oLog.writeLog("WARNING", "No GPS EXIF Data for " + targetFile)
            print(aFile + ": No GPS EXIF Data") # Update 1.1
    else:
        oLog.writeLog("WARNING", targetFile + " not a valid file")
        print(aFile + ": Not a valid file") # Update 1.1

# Clean up and Close Log and CSV File
del oLog
del oCSV

print("Program End")    # Update 1.1
print() # Update 1.1
