import time, sys
from datetime import datetime
import signal
import argparse


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

    save_time = datetime.now()
    print_time = save_time.strftime("%b%d_%Y_%H%M%S")

    outputfilename = print_time + '_' + name_seed + '.csv'
    print("output file name is {}".format(outputfilename))


    i = 0
    actions = ["Flow Clockwise (1)", "Fish Out", "Fish In", "Flow Counterclockwise (2)", "Fish Out", "Fish In"]
    while not brexit:
        action_type_str = actions[i%len(actions)]
        i = i+1
        mycomment = input(action_type_str)
        print_time = datetime.now().strftime('%Y%b%d_%H:%M:%S')
        with open(outputfilename, 'a') as f:
            datme = print_time + ', ' + action_type_str + ', ' + mycomment
            print(datme)
            f.write(datme + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=
        'Run a lab session',
        epilog=
        'Any issues and clarifications: github.com/mixmixmix/parrtrak/issues')
    parser.add_argument(
        '--output', '-o', required=False, nargs=1, help='Seed for output file name. A lot will be added to it...')

    args = parser.parse_args()
    main(args)
