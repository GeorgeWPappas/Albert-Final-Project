# Import Declarations.
import csv      # Python Standard Library - reader and writer for csv files
import logging  # Update 1.1

#
# Class: _CSVWriter
#
# Desc: Handles all methods related to comma separated value operations
#
# Methods constructor:  Initializes the CSV File
#                       writeCVSRow: Writes a single row to the csv file
#                       writerClose: Closes the CSV File
class _CSVWriter:
    def __init__(self, fileName):
        log = logging.getLogger('main.pGPSExtractor.py')    # Update 1.1

        try:
            # Open the file we want to write CSV data to.
            # create a writer object and then write the header row
            self.csvFile = open(fileName,'w')
            print() # Update 1.1
            print("Opened results file: " + fileName)    # Update 1.1

            # Create the csv writer object.
            self.writer = csv.writer(self.csvFile, delimiter=',', quoting=csv.QUOTE_ALL, lineterminator='\n')   # Update 1.1: Added "lineterminator" which takes away empty lines in csv file.

            # Write the header row.
            self.writer.writerow(('Image Path', 'UTC Time', 'Make', 'Model', 'Lat Ref', 'Latitude', 'Lon Ref', 'Longitude', 'Alt Ref', 'Altitude'))
        except:
            log.error('CSV File Failure')
            print("Failed to open results file " + fileName)    # Update 1.1
    
    def writeCSVRow(self, fileName, cameraMake, cameraModel, utc, latRef, latValue, lonRef, lonValue, altRef, altValue):
        latStr = '%.8f' % latValue
        lonStr = '%.8f' % lonValue
        altStr = '%.8f' % altValue

        # Update 1.1: If no value is present, then make it a blank entry in the csv file.
        if altRef == 0:
            altRef = ' '

        if altValue == 0:
            altStr = ' '
        # End Update 1.1 ===========================

        self.writer.writerow((fileName, cameraMake, cameraModel, utc, latRef, latStr, lonRef, lonStr, altRef, altStr))

    def __del__(self):
        self.csvFile.close()
        print() # Update 1.1
        print("CSV file closed.")   # Update 1.1
