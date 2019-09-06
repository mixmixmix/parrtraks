"""
This program records from camera. More details: run program without arguments
"""
import time
import socket
import signal
import sys, argparse
import numpy as np
from datetime import datetime, timedelta
import picamera
import datetime as dt
import io

brexit = 0
def signal_handler(sig, frame):
        global brexit
        print('You pressed Ctrl+C!')
        brexit = 1
        print('We shall now attempt to exit...')

class MePipe(object):
        def __init__(self, fname):
                self.frameout = io.open(fname + '.h264','wb')
                self.timeout = io.open(fname + '.txt','w')
                self.frameno = 0

        def write(self, buf):
                self.frameout.write(buf)
                self.timeout.write(datetime.now().strftime("%H%M%S")+'\n')

def main(args):
    signal.signal(signal.SIGINT, signal_handler) #allow Ctr+C to end program with saving

    name_seed = "TEST"
    if args.output is not None:
        name_seed = args.output[0]

    print("Name seed is {}".format(name_seed))

    fps = int(args.fps[0])
    width = 1280
    height = 720
    hostname = socket.gethostname()

    camera = picamera.PiCamera(resolution=(width, height), framerate=fps)
    # camera.start_preview()
    camera.annotate_background = picamera.Color('black')
    camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    current_date = datetime.now()
    current_date_str = current_date.strftime("-%d%b-%Y-%H%M%S")
    camera.start_preview() # for debugging
    outputpipe = MePipe(name_seed+current_date_str+'_stream_' + hostname + '.h264')
    camera.start_recording(outputpipe,quality=10,format='h264')

    while brexit == 0:
        current_date = datetime.now()
        current_date_str = current_date.strftime("%d-%b-%Y %H:%M:%S")
        camera.annotate_text = name_seed + ' ||' + current_date_str
        camera.wait_recording(0.2)
    camera.stop_recording()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=
        'Record video for migration study',
        epilog=
        'Any issues and clarifications: github.com/mixmixmix/parrtrak/issues')
    parser.add_argument('--visual', '-v', default=False, action='store_true',
                        help='Show camera image with data overlay')
    parser.add_argument(
        '--output', '-o', required=False, nargs=1, help='Seed for output file name. A lot will be added to it...')
    parser.add_argument(
        '--fps', '-f', required=True, nargs=1, help='Recording framerate')

    args = parser.parse_args()
    main(args)
