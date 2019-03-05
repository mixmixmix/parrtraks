import cv2
import numpy as np
from datetime import datetime

from cv2 import __version__
__version__ # I wrote that in 3.4.3, yeah!


d = datetime(2019, 12, 6, 16, 29, 43)
time = d.strftime("%I:%M%:%Sp")
fps = 25

cap = cv2.VideoCapture('test.mp4')

cap.set(cv2.CAP_PROP_FPS,30)
fps = cap.get(cv2.CAP_PROP_FPS)
fcount = cap.get(cv2.CAP_PROP_FRAME_COUNT)

print(fps)
print(fcount)

# Check if camera opened successfully
if (cap.isOpened()== False):
    print("Error opening video stream or file")


ret, frame = cap.read()
w = frame.shape[1]
h = frame.shape[0]

print(frame.shape[0])

# Read until video is completed
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        # Display the resulting frame
        cv2.imshow('Frame',frame)
        #depressedKey = cv2.waitKey(1000//fps)
        depressedKey = cv2.waitKey(2)
        if depressedKey == 'q':
            break

        # processing
        # M = cv2.getRotationMatrix2D((w/2,h/2), 30, 1)
        # rotated = cv2.warpAffine(frame, M, (w, h))
        # cropped = rotated[200:400, 200:400]
        # cv2.putText(cropped, time,  (30,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (200,200,250), 1);

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
