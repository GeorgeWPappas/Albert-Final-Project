#
# gps_falsifier : Malicious Modification Script
# Author: George Pappas
# Original Creation Date: July 2013
# Version 1.0
#

# Import Declarations.
import os               # Standard Library OS functions
import argparse         # Python Standard Library - Parser for command-line options, arguments
import piexif
import random
import shutil

#
# Name: ParseCommand() Function
#
# Desc: Process and Validate the command line arguments
#       use Python Standard Library module argparse
#
# Input: none
#
# Actions:
#           Uses the standard library argparse to process the command line
#
def ParseCommandLine():
    parser = argparse.ArgumentParser('Python gpsExtractor')

    parser.add_argument('-v', '--verbose', help="enables printing of additional program messages", action='store_true')
    parser.add_argument('-i', '--imageName', type=ValidateFileRead, required=True, help="specify the path and file to scan")
    parser.add_argument('-f', '--fakeImageName', type=str, help="specify the path and file to create", default=os.curdir)

    args = None
    args = parser.parse_args()

    return args
# End Parse Command Line ===========================

#
# Name: ValidateFileRead Function
#
# Desc: Function that will validate that a file exists and is readable
#
# Input: A file name with full path
#
# Actions:
#           if valid will return path
#
#           if invalid it will raise an ArgumentTypeError within argparse
#           which will inturn be reported by argparse to the user
#
def ValidateFileRead(theFile):
    # Validate the path is a valid
    if not os.path.exists(theFile):
        raise argparse.ArgumentTypeError('File does not exist')

    # Validate the path is readable
    if os.access(theFile, os.R_OK):
        return theFile
    else:
        raise argparse.ArgumentTypeError('File is not readable')
# End ValidateFileRead =====================================

def genRandomDate(randomDictionary):
    randYear = random.randint(1990, 2020) # Generates random year.
    randMonth = random.randint(1,12)  # Generates random month.

    if randMonth == 2:    # For the month of february.
        randDay = random.randint(1, 28)
    else:
        randDay = random.randint(1,30)
    
    # Renerates random time.
    randHour = random.randint(1,23)
    randMinute = random.randint(1,59)
    randSecond = random.randint(1,59)

    randDate = ("%d:%02d:%02d %02d:%02d:%02d" % (randYear, randMonth, randDay, randHour, randMinute, randSecond))

    randomDictionary[0] = randDate  # Adds new date and time to randomDictionary.

    return randomDictionary
# End genRandomDate =====================================

def genRandomGPS(randomDictionary):
    # Generates random numbers for latitude.
    randLatDeg = random.randint(0, 89)
    randLatMin = random.randint(0, 59)
    randLatSec = random.randint(0, 59)
    randLatRef = random.randint(0,1)

    # Generates random numbers for longitude.
    randLonDeg = random.randint(0, 179)
    randLonMin = random.randint(0, 59)
    randLonSec = random.randint(0, 59)
    randLonRef = random.randint(0,1)

    # Formats randLat & randLon as a tuple.
    randLat = ((randLatDeg, 1), (randLatMin, 1), (randLatSec, 1))
    randLon = ((randLonDeg, 1), (randLonMin, 1), (randLonSec, 1))

    # Sets north, south, east, or west for latitude & longitude reference.
    if randLatRef == 0:
        randLatRef = 'N'
    else:
        randLatRef = 'S'

    if randLonRef == 0:
        randLonRef = 'W'
    else:
        randLonRef = 'E'

    # Adds random gps values to randomDictionary.
    randomDictionary[1] = randLat
    randomDictionary[2] = randLatRef
    randomDictionary[3] = randLon
    randomDictionary[4] = randLonRef

    return randomDictionary
# End genRandomGPS =====================================

# Main Function.
if __name__ == '__main__':
    GPS_FALSIFIER_VERSION = '1.0'

    # Introduction statement.
    print()
    print("Starting GPS_Falsifier...")

    # Dictionary Declaration.
    randomDictionary = {}   # Creates random dictionary.

    args = ParseCommandLine()  # Process the Command Line Arguments.

    print()
    print('Using image: {}'.format(args.imageName))

    genRandomDate(randomDictionary) # Generates random date & time.
    genRandomGPS(randomDictionary)  # Generates random gps values.

    if args.fakeImageName == os.curdir:
        args.fakeImageName = 'fake_' + os.path.basename(args.imageName)
    else:
        args.fakeImageName = os.path.basename(args.fakeImageName)

    shutil.copy(args.imageName, args.fakeImageName)   # Creates copy of image file.
    fakeImageExifData = piexif.load(args.fakeImageName)   # Loads image EXIF data into imageData.
    fakeImageGpsData = fakeImageExifData['GPS'] # Loads image GPS data into fakeImageGpsData.

    print()
    print("Current " + args.imageName + " GPS data: {}".format(fakeImageGpsData))

    fakeImageExifData['Exif'][piexif.ExifIFD.DateTimeOriginal] = randomDictionary[0]    # Writes randomized time to fakeImageGpsData.
    fakeImageExifData['Exif'][piexif.ExifIFD.DateTimeDigitized] = randomDictionary[0]   # Writes randomized time to fakeImageGpsData.

    fakeImageGpsData[piexif.GPSIFD.GPSDateStamp] = randomDictionary[0]  # Writes randomized date to fakeImageGpsData.
    fakeImageGpsData[piexif.GPSIFD.GPSLatitude] = randomDictionary[1]   # Writes randomized latitude to fakeImageGpsData.
    fakeImageGpsData[piexif.GPSIFD.GPSLatitudeRef] = randomDictionary[2]    # Writes randomized latitude reference to fakeImageGpsData.
    fakeImageGpsData[piexif.GPSIFD.GPSLongitude] = randomDictionary[3]  # Writes randomized longitude to fakeImageGpsData.
    fakeImageGpsData[piexif.GPSIFD.GPSLongitudeRef] = randomDictionary[4]   # Writes randomized longitude reference to fakeImageGpsData.

    print()
    print("Falsified GPS data: {}".format(fakeImageGpsData))

    exif_bytes = piexif.dump(fakeImageExifData) # Converts exif data dictanary into bytes.
    piexif.insert(exif_bytes, args.fakeImageName)   # Writes falsified data to new file.

    try:
        if os.path.dirname(args.imageName) is not '':
            shutil.move(args.fakeImageName, os.path.dirname(args.imageName))    # Moves file to original image directory.
        else:
            print()
            print("File saved in script directory because user did not specify original image directory.")
    except:
        os.remove(args.fakeImageName)   # Deletes new file if it cannot be moved to new directory.
        print()
        print("File already exists in specified directory. Please delete and try again.")

    # Finishing statement.
    print()
    print("Program Terminated Normally")
# End Main Function =====================================
