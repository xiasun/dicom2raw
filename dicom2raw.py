import dicom
import os
import numpy
import sys

dicomPath = "./../nn/"
lstFilesDCM = []  # create an empty list
for dirName, subdirList, fileList in os.walk(dicomPath): # file name should be ordered correctly
    allInOne = ""

    for filename in fileList:
        if "".join(filename).endswith((".dcm", ".DCM")): # check whether the file's DICOM
            path = dicomPath + "".join(filename)
            dataset = dicom.read_file(path)

            for n,val in enumerate(dataset.pixel_array.flat): 
                dataset.pixel_array.flat[n] = val / 60
                if val < 0:
                    dataset.pixel_array.flat[n] = 0
                    
            dataset.PixelData = numpy.uint8(dataset.pixel_array).tostring() # convert int16 to int8
            allInOne += dataset.PixelData
            print "slice " + "".join(filename) + " done"

    newFile = open("./all_in_one.raw", "wb")
    newFile.write(allInOne)
    newFile.close()
    print "RAW file generated"
