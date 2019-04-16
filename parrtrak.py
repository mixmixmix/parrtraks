"""
This program reads and displays my recording from phase 2 experiments (group size migration with constant flow)
Assumptions:
- recordings done at 10fps

"""
import cv2
import numpy as np
from datetime import datetime, timedelta

from cv2 import __version__
__version__  # I wrote that in 3.4.3, yeah!

def ripFname(fname):
    """
    Rips apart filename to extract timestamp.
    TODO Only works for March and April, hehehe

    Args:\n
        fname: File name to rip apart, format: \'2019mar29_1800_23h.h264\'\n

    Returns:\n
        datetime object\n
    """
    hour = int(fname.split('_')[1][0:2])
    minute = int(fname.split('_')[1][2:4])
    year = int(fname.split('_')[0][0:4])
    day = int(fname.split('_')[0][7:9])
    month = 3 if ( fname.split('_')[0][4:7]=='mar' or \
                   fname.split('_')[0][4:7]=='mar' ) else 4
    ripped_date = datetime(year, month, day, hour, minute, 30)
    return ripped_date


fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
# fgbg = cv2.createBackgroundSubtractorMOG()

fname = '2019mar29_1800_23h.h264'

start_date = ripFname(fname)
current_date = start_date
ctime = current_date.strftime("%I:%M%:%Sp")
fps = 10


cap = cv2.VideoCapture(fname)

# cap.set(cv2.CAP_PROP_FPS, 30)
# fps = cap.get(cv2.CAP_PROP_FPS)
fcount = cap.get(cv2.CAP_PROP_FRAME_COUNT)

print(fps)
print("No of frames:")
print(fcount)

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video stream or file")

ret, frame = cap.read()
w = frame.shape[1]
h = frame.shape[0]

print("Image shape is ")
print(frame.shape)

# Read until video is completed
while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        fgmask = fgbg.apply(frame)
        cv2.imshow('Background mask',fgmask)
        current_date = current_date + timedelta(seconds=0.1)
        ctime = current_date.strftime("%I:%M%:%Sp")
        # Display the resulting frame
        cv2.putText(frame, ctime,  (30,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (200,200,250), 1);
        cv2.imshow('Frame', frame)
        #depressedKey = cv2.waitKey(1000//fps)
        depressedKey = cv2.waitKey(40)
        if depressedKey == 'q':
            break

        # processing
        # M = cv2.getRotationMatrix2D((w/2,h/2), 30, 1)
        # rotated = cv2.warpAffine(frame, M, (w, h))
        # cropped = rotated[200:400, 200:400]

        # cv2.imshow('Rotated',rotated)
        # cv2.imwrite( "rotated.jpg", rotated )
        # cv2.imwrite( "cropped.jpg", cropped )

        #cv2.waitKey(0)
        # break
        # Press Q on keyboard to    exit

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
