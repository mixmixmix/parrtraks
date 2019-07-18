"""
This program records from camera. More details: run program without arguments
"""
import time

import signal
import cv2, yaml
import sys, argparse
import numpy as np
from datetime import datetime, timedelta


brexit = 0
def signal_handler(sig, frame):
        global brexit
        print('You pressed Ctrl+C!')
        brexit = 1
        print('We shall now attempt to exit...')

def main(args):
    signal.signal(signal.SIGINT, signal_handler) #allow Ctr+C to end program with saving

    name_seed = "TEST"
    if args.output is not None:
        name_seed = args.output[0]

    print("Name seed is {}".format(name_seed))

    camera_input_number = int(args.camera[0])


    if args.visual:
        cv2.namedWindow("preview")

    print("Opening camera input number {}".format(camera_input_number))
    cap = cv2.VideoCapture(camera_input_number)
    read_fps = cap.get(cv2.CAP_PROP_FPS);
    read_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT);
    read_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH);

    print('Fps: {0}, height: {1}, width {2}'.format(read_fps, read_height, read_width))

    if cap.isOpened(): # try to get the first frame
        rval, frame = cap.read()
    else:
        rval = False

    height=frame.shape[0]
    width=frame.shape[1]
    fps = int(args.fps[0])
    ms_gap = int(1000/fps)
    print("Time between frames should be in ms: {}".format(ms_gap))
    fourCC = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    S = (int(width),int(height))

    current_date = datetime.now()
    current_date_str = current_date.strftime("-%d%b-%Y-%H%M%S")

    out = cv2.VideoWriter(name_seed+current_date_str+".avi", fourCC, fps, S, True)


    start = time.time()
    last_time = start
    frameno = 0
    processing_list = []
    while rval:
        processing_ms = int((time.time() - start) * 1000)
        left_over_time=max(ms_gap-processing_ms,2)
        # key = cv2.waitKey(left_over_time)
        time.sleep(left_over_time/1000)#sleep in seconds
        start = time.time()
        rval, frame = cap.read()

        frameno = frameno+1
        this_time = time.time()
        processing_total_ms = int((this_time - last_time) * 1000)
        if len(processing_list) > 10:
            processing_list.pop(0)
        processing_list.append(processing_total_ms)
        avg_processing_total_ms = sum(processing_list)/len(processing_list)
        last_time = this_time
        current_date = datetime.now()
        current_date_str = current_date.strftime("%d-%b-%Y %H:%M%:%S")

        cv2.rectangle(frame,(30, 10), (200,35), (255,255,255),-1) 
        cv2.putText(frame, current_date_str,  (30,20), cv2. FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0,170,0), 1);
        cv2.putText(frame, str(left_over_time) ,  (30,30), cv2. FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0,1,124), 1);
        cv2.putText(frame, "frame: "+ str(frameno) ,  (120,30), cv2. FONT_HERSHEY_COMPLEX_SMALL, 0.5, (222,1,22), 1);
        cv2.putText(frame, "FPS: "+ str(int(1000/avg_processing_total_ms)) ,  (50,30), cv2. FONT_HERSHEY_COMPLEX_SMALL, 0.5, (222,1,22), 1);
        if args.visual:
            key = cv2.waitKey(1)
            cv2.imshow("preview", frame)
        out.write(frame)

        if brexit == 1: #sigint
            break

    if args.visual:
        cv2.destroyWindow("preview")
    cap.release()
    out.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=
        'Record video for migration study',
        epilog=
        'Any issues and clarifications: github.com/mixmixmix/parrtrak/issues')
    parser.add_argument(
        '--camera', '-c', required=True, nargs=1, help='camera number (0 for raspi, 1 for external?)')
    parser.add_argument('--visual', '-v', default=False, action='store_true',
                        help='Show camera image with data overlay')
    parser.add_argument(
        '--output', '-o', required=False, nargs=1, help='Seed for output file name. A lot will be added to it...')
    parser.add_argument(
        '--fps', '-f', required=True, nargs=1, help='Recording framerate')

    args = parser.parse_args()
    main(args)
