import sys
import os
import argparse

import cv2
print(cv2.__version__)

def extractImages(pathInp, pathOut):
    """Main program function when run on from the command line                                           
    Args (list): arguments                                                                               
    Usage: python split2.py
    --pathInp=input/SupplementaryProctor_AllenBradley_1492_sp40\(Joy\).MOV
    --pathOut=AllenBradley
    Note: provide path to input folder and pathOut folder should be created in advance.
    """
    count = 0
    vidcap = cv2.VideoCapture(pathInp)
    (prefix1, sep1, suffix1) = pathInp.rpartition('/')
    fn = os.path.splitext(suffix1)[0]
    success,image = vidcap.read()
    success = True
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))    # 1 sec framd 
        success,image = vidcap.read()
        print ('Read a new frame: ', success, ' ', count)
        if not success:
            #if no success the break the loop                                                
            break
        # Saves the frames with frame-count
        print("Writing to folder: ", args.pathOut)
        cv2.imwrite(str(args.pathOut)+"/"+fn+"_frame%d.jpg" % count, image) # save frame 
        count = count + 1

if __name__=="__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--pathInp", help="path to video")
    a.add_argument("--pathOut", help="path to images")
    args = a.parse_args()
    print(args)
    extractImages(args.pathInp, args.pathOut)
