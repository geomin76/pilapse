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
from picamera import PiCamera
from time import sleep
import os
from getch import pause
import logging

# q = 0

def pilapse(args):
    if args['-v']:
      logging.basicConfig(format='LOGGING: %(message)s', level=logging.DEBUG)
    elif args['-q']:
      logging.basicConfig(level=logging.CRITICAL)
    else:
      logging.basicConfig(format='LOGGING: %(message)s', level=logging.INFO)
    
    logging.debug("Initializing PiCamera")
    camera = PiCamera()

    logging.debug("Orienting the camera")
    camera.rotation = 180

    # camera.sensor_mode = 2
    logging.info("Previewing the camera frame")
    preview(camera)

    # print(args)


def preview(camera):
  logging.debug("Starting camera preview")

  camera.start_preview(fullscreen=False, window=(100, 100, 640, 480))
  pause('Position your frame for the timelapse. \nPress any key to exit preview.')

  logging.debug("Stopping camera preview")
  camera.stop_preview()


if __name__ == '__main__':
    args = docopt(__doc__, version='PiLapse 1.0')
    pilapse(args)