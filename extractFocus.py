"""
This program reads vie
"""
import signal
import cv2, yaml
import sys, argparse
import numpy as np
from datetime import datetime, timedelta
import yaml


from cv2 import __version__
__version__  # I wrote that in 3.4.3, yeah!

brexit = 0

def signal_handler(sig, frame):
        global brexit
        print('You pressed Ctrl+C!')
        brexit = 1
        print(brexit)

def byfactor(v,factor):
    dvx = v[2]-v[0]
    dvy = v[3]-v[1]
    dvfx = factor * dvx
    dvfy = factor * dvy
    boxwidth = max(dvfy,dvfx)
    incx= (boxwidth-dvx)/2
    incy= (boxwidth-dvy)/2
    return (v[0]-incx,v[1]-incy,v[2]+incx,v[3]+incy)

def constframe(v,framesize):
    cvx = v[2] - (v[2]-v[0])/2
    cvy = v[3] - (v[3]-v[1])/2
    inc= (framesize)/2
    return (cvx-inc,cvy-inc,cvx+inc,cvy+inc)

def main(args):
    global brexit
    signal.signal(signal.SIGINT, signal_handler) #allow Ctr+C to end program with saving

    fourCC = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    S = (160,160)
    framesize = 80
    outwriters = dict()

    if args.visual:
        cv2.namedWindow('frame', cv2.WINDOW_GUI_EXPANDED)
        cv2.moveWindow('frame', 20,20)

        #Output save video
        cv2.namedWindow('outvid', cv2.WINDOW_GUI_EXPANDED)
        cv2.moveWindow('outvid', 20,20)



    fname = args.fname[0]
    tname = args.tname[0]
    rname = args.rname[0]
    print(fname)
    save_warp = np.load(rname,allow_pickle=True)

    cap = cv2.VideoCapture(fname)

    # cap.set(cv2.CAP_PROP_FPS, 30)
    fps = cap.get(cv2.CAP_PROP_FPS)
    fcount = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    print("No of frames:")
    print(fcount)

    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error opening video stream or file")


    tracks = dict()
    #get the next track
    mfile = open(tname,'r')
    lines = mfile.readlines()
    lineit = 0
    line = lines[lineit]

    ctrack = line.split(",")
    currentTrackFrame = int(ctrack[0])

    iterator = 0
    ret, frame = cap.read()
    w = frame.shape[1]
    h = frame.shape[0]

    # Read until video is completed
    while (cap.isOpened()):
        if brexit == 1:
            break
        if currentTrackFrame > iterator:
            ret, frame = cap.read()
            if ret == True:
                iterator=iterator+1
                # Display the resulting frame
            else:
                brexit=1
        elif currentTrackFrame == iterator: 
            while True:
                lineit = lineit + 1
                if lineit >= len(lines):
                        break
                ctrack = lines[lineit].split(",")
                if int(ctrack[0]) != currentTrackFrame:
                    currentTrackFrame = int(ctrack[0])
                    break
                else:
                    tracks[ctrack[1]]=(float(ctrack[2]),float( ctrack[3] ),float( ctrack[4] ),float(ctrack[5]))
                    #x1,y1 x2,y2

            #show bboxez
            dispframe = frame.copy()
            for k in tracks:
                v=tracks[k]
                # v=byfactor(v,3)
                # v=constframe(v,framesize)
                full_warp = save_warp[iterator]
                try:
                    inv_warp = np.linalg.inv(full_warp)
                except:
                    print('Couldn\'t invert matrix, not transforming this frame')
                    inv_warp = np.linalg.inv(np.eye(3, 3, dtype=np.float32))

                iwarp = (full_warp)
                corner1 = np.expand_dims(
                    [v[0], v[1]], axis=0)
                corner1 = np.expand_dims(corner1, axis=0)
                corner1 = cv2.perspectiveTransform(corner1,
                                                    iwarp)[0, 0, :]
                minx = corner1[0]
                miny = corner1[1]
                corner2 = np.expand_dims(
                    [v[2], v[3]], axis=0)
                corner2 = np.expand_dims(corner2, axis=0)
                corner2 = cv2.perspectiveTransform(corner2,
                                                    iwarp)[0, 0, :]
                maxx = corner2[0]
                maxy = corner2[1]
                # r = np.random.randint(256)
                r = 255
                g = 255
                b = 233
                (minx,miny,maxx,maxy)=constframe((minx,miny,maxx,maxy),framesize)
                #(minx,miny,maxx,maxy)=byfactor((minx,miny,maxx,maxy),3)
                # print("{},{},{},{}".format(minx,miny,maxx,maxy))
                cv2.rectangle(dispframe, (int(minx)-4, int(miny)-4),
                                (int(maxx)+4, int(maxy)+4), (r, g, b), 4)
                cv2.putText(dispframe, str(k),
                            (int(minx) - 5, int(miny) - 5), 0,
                            5e-3 * 200, (r, g, b), 2)

                #write to a file
                if k not in outwriters:
                    outwriters[k] = cv2.VideoWriter(args.output[0]+"/"+str(k)+".avi", fourCC, fps, S, True)
                crop_img = frame[int(miny):int(maxy),int(minx):int(maxx)]
                if crop_img.size > 0:
                        sized_img = cv2.resize(crop_img,S)
                        outwriters[k].write(sized_img)

            if args.visual:
                #(x,y)
                cv2.imshow('frame', dispframe)
                key = cv2.waitKey(int(1000/fps))


            tracks = dict()
        else:
            print("Something went horribly wrong")


    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()

    for w in outwriters:
        outwriters[w].release()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=
        'Extract images containing tracks',
        epilog=
        'Any issues and clarifications: github.com/mixmixmix/parrtrak/issues')
    parser.add_argument(
        '--fname', '-f', required=True, nargs=1, help='video filename')
    parser.add_argument(
        '--tname', '-t', required=True, nargs=1, help='tracks list filename')
    parser.add_argument(
        '--rname', '-r', required=True, nargs=1, help='transforms')
    parser.add_argument(
        '--output', '-o', required=True, nargs=1, help='output directory')
    parser.add_argument('--visual', '-v', default=False, action='store_true',
                        help='Display tracking progress')


    args = parser.parse_args()
    main(args)
