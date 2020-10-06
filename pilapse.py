"""PiLapse
A python command line tool

Usage:
  pilapse.py [-vq] [--interval INTERVAL] 
                   (--photos | --time | --cliplen) VALUE 
                   [--email EMAIL] ...
  pilapse.py --help
  pilapse.py --version

Arguments:
  VALUE                 Total number of time or photos
  EMAIL                 Email to send file to

Options:
  -v                    verbose mode
  -q                    quiet mode
  --photos              Number of photos to be taken
  --time                Total time to be elapsed
  --cliplen             Length of time lapse clip
  --interval=INTERVAL   Interval of photos [default: 5s]
  --email=EMAIL         Email to send file to
  --help                Show this screen
  --version             Show version

"""
from docopt import docopt

def pilapse(args):
    # logger for verbose or quiet or whatever level
    print(args)


if __name__ == '__main__':
    args = docopt(__doc__, version='PiLapse 1.0')
    pilapse(args)