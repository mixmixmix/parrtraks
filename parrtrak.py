"""
This program reads and displays my recording from phase 2 experiments (group size migration with constant flow)
Assumptions:
- recordings done at 10fps
"""
import signal
import cv2, yaml
import sys, argparse
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

brexit = 0
def signal_handler(sig, frame):
        global brexit
        print('You pressed Ctrl+C!')
        brexit = 1
        print(brexit)


def main(args):
    signal.signal(signal.SIGINT, signal_handler) #allow Ctr+C to end program with saving

    if args.visual:
        cv2.namedWindow('frame', cv2.WINDOW_GUI_EXPANDED)
        cv2.moveWindow('frame', 20,20)
        cv2.namedWindow('fg', cv2.WINDOW_GUI_EXPANDED)
        cv2.moveWindow('fg', 20,20)
        #Output save video
        cv2.namedWindow('outvid', cv2.WINDOW_GUI_EXPANDED)
        cv2.moveWindow('outvid', 20,20)



    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
    # fgbg = cv2.bgsegm.createBackgroundSubtractorCNT()
    # fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()
    # fgbg = cv2.createBackgroundSubtractorMOG()

    # fname = '2019mar29_1800_23h.h264'
    # fname = '2019apr14_0008_unknown.h264'
    # fname = '2019mar20_0905_4h.h264'
    # fname = '2019may02_2118_all.h264'
    fname = args.fname[0]
    # fname = '2019apr27_1131_groupA9.mp4'
    print(fname)
    start_date = ripFname(fname)
    current_date = start_date
    ctime = current_date.strftime("%I:%M%:%S")
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
    iterator = 1
    w = frame.shape[1]
    h = frame.shape[0]

    if args.output[0] != "":
        fourCC = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
        S = (int(w),2*int(h))
        out = cv2.VideoWriter(args.output[0]+".avi", fourCC, fps, S, True)

    noPixels = h * w
    movement = []
    # Read until video is completed
    i=0
    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        i=i+1
        if ret == True and brexit==0:
            iterator=iterator+1
            fgmask = fgbg.apply(frame)
            current_date = current_date + timedelta(seconds=(1/fps))
            ctime = current_date.strftime("%I:%M%:%S")
            ones = cv2.countNonZero(fgmask)
            coverage = 100 * (ones/noPixels)
            cover_str = "{0:.2f}".format(coverage)
            # Display the resulting frame
            if args.visual:
                #(x,y)
                cv2.imshow('fg',fgmask)
                cv2.imshow('frame', frame)
                key = cv2.waitKey(int(1000/fps))
                if key == ord('q'):
                    print("quit")
                    break
            if args.save:
                if (iterator % 100 == 0):
                    cv2.imwrite('may'+str(iterator)+'f.png', frame)
                    sys.stdout.write('.')
                    sys.stdout.flush()

            # print("{0} : {1:.2f} ".format(ctime, coverage ))
            movement.append([ctime,coverage])
            sys.stdout.write('\r')
            sys.stdout.write("[%-20s] %d%% %d/%d" %
                                ('=' * int(20 * i / float(fcount)),
                                 int(100.0 * i / float(fcount)), i, fcount))

            fgmask_tricolor = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR)
            cv2.putText(fgmask_tricolor, cover_str,  (40,100), cv2. FONT_HERSHEY_SCRIPT_COMPLEX, 2.6, (0,240,240), 1);
            cv2.putText(fgmask_tricolor, "[% of foreground pixels]",  (20,140), cv2. FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0,240,240), 1);
            cv2.putText(frame, ctime,  (30,60), cv2. FONT_HERSHEY_COMPLEX_SMALL, 2.0, (0,170,0), 2);
            img_pair = np.concatenate((frame, fgmask_tricolor), axis=0)
            if args.visual:
                cv2.imshow('outvid',img_pair)
                if args.output[0]!="":
                    out.write(img_pair)



            #depressedKey = cv2.waitKey(1000//fps)
            # depressedKey = cv2.waitKey(40)
            # if depressedKey == 'q':
                # break

            # processing
            # M = cv2.getRotationMatrix2D((w/2,h/2), 30, 1)
            # rotated = cv2.warpAffine(frame, M, (w, h))
            # cropped = rotated[200:400, 200:400]

            # cv2.imshow('Rotated',rotated)
            # cv2.imwrite( "rotated.jpg", rotated )
            # cv2.imwrite( "cropped.jpg", cropped )

            # Press Q on keyboard to    exit
        else:
            break

    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()

    with open(args.output[0], 'w') as handle:
        yaml.dump(movement, handle)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=
        'Analyse videos of migrating fish',
        epilog=
        'Any issues and clarifications: github.com/mixmixmix/parrtrak/issues')
    parser.add_argument(
        '--fname', '-f', required=True, nargs=1, help='filename')
    parser.add_argument(
        '--output', '-o', required=True, nargs=1, help='outputfile')
    parser.add_argument('--visual', '-v', default=False, action='store_true',
                        help='Display tracking progress')
    parser.add_argument('--save', '-s', default=False, action='store_true',
                        help='save every 100th frame')


    args = parser.parse_args()
    main(args)
