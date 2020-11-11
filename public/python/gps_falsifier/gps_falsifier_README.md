
gps_falsifier : Malicious Modification Script
Author: George Pappas
Original Creation Date: July 2013
Version 1.0

gps_falsifier_README:

HOW TO RUN - METHOD 1:
    The method can be executed by specifying a single filename in the '-i' command line argument. This will create a copy of the input file and export it as "fake_'filename'" in the same directory as the original file.

    Input example:
        python3 gps_falsifier.py -i cat.jpg

    *Note: This mode only works if the original file is in the same directory as the script*


HOW TO RUN - METHOD 2:
    The method can be executed by specifying a path and a single filename in the '-i' command line argument. This will create a copy of the input file and export it as "fake_'filename'" in the same directory as the original file.

    Input example:
        python3 gps_falsifier.py -i c:\Temp1\images\cat.jpg

    *Note: This mode will NOT replace an already existing file with the same filename*


HOW TO RUN - METHOD 3:
    The method can be executed by specifying a path and a single filename in the '-i' command line argument. It will also take a filename in the '-f' command line argument for the name of the duplicated file. It will export it in the same directory as the original file.

    Input example:
        python3 gps_falsifier.py -i c:\Temp1\images\cat.jpg -f fakecat.jpg

    *Note: This mode will replace an already existing file with the same filename*


HOW TO RUN - METHOD 4:
    The method can be executed by specifying a path and a single filename in the '-i' command line argument. It will also take a filename in the '-f' command line argument for the name of the duplicated file. It will export it in the same directory as the original file.

    Input example:
        python3 gps_falsifier.py -i c:\Temp1\images\cat.jpg -f c:\Temp4\images\fakecat.jpg

    *Note: This mode will NOT create additional directories and will either place the duplicated file in the original file directory or return with "File already exists in specified directory. Please delete and try again." if the file already exists in the original file directory*