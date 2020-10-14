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
import os, shutil
from getch import pause
import ffmpeg
import logging

def pilapse(args):
    loggingSetter(args, logging)
    
    logging.debug("Initializing PiCamera")
    camera = PiCamera()

    logging.debug("Orienting the camera")
    camera.rotation = 180

    # camera.sensor_mode = 2
    logging.info("Previewing the camera frame")
    preview(camera)

    logging.debug("Getting timelapse interval")
    interval = getInterval(args)
    logging.info("Setting timelapse interval of {0} seconds".format(interval))

    for i in range(5, 0, -1):
      sleep(1)
      logging.critical("Timelapse starting in {0}".format(str(i)))

    # print(args)
    logging.debug("Creating tmp photo directory")
    try:
      os.mkdir('tmp')
    except:
      pass

    if args['--photos']:
      logging.info("Taking timelapse of {0} photos".format(args['VALUE']))
      for i in range(int(args['VALUE'])):
        logging.info("Taking photo {0}".format(str(i)))
        camera.capture('tmp/{0}.jpg'.format(str(i)))
        logging.debug("Saved in /tmp")
        sleep(interval)
        logging.debug("Taking a {0}s interval".format(str(interval)))
    
    
    logging.info("Converting imgs to video file")
    (
        ffmpeg
        .input('./tmp/*.jpg', pattern_type='glob', framerate=25)
        .output('movie.mp4')
        .run(quiet=True)
    )

    logging.debug("Removing tmp photo directory")
    shutil.rmtree('tmp/')



def preview(camera):
    logging.debug("Starting camera preview")
    camera.start_preview(fullscreen=False, window=(100, 100, 640, 480))

    pause('Position your frame for the timelapse. \nPress any key to exit preview.')

    logging.debug("Stopping camera preview")
    camera.stop_preview()


def loggingSetter(args, logging):
    if args['-v']:
      logging.basicConfig(format='LOGGING: %(message)s', level=logging.DEBUG)
    elif args['-q']:
      logging.basicConfig(level=logging.CRITICAL)
    else:
      logging.basicConfig(format='LOGGING: %(message)s', level=logging.INFO)

def getInterval(args):
    interval = 5
    intervalStr = args['--interval']
    if intervalStr.isdigit():
      interval = int(intervalStr)      
    elif intervalStr[-1] == 's':
      interval = int(intervalStr[:-1])
    elif intervalStr[-1] == 'm':
      interval = int(intervalStr[:-1]) * 60
    elif intervalStr[-1] == 'h':
      interval = int(intervalStr[:-1]) * 3600
    elif intervalStr[-1] == 'd':
      interval = int(intervalStr[:-1]) * 86400
    else:
      raise Exception("Interval format not accepted")
    return interval

if __name__ == '__main__':
    args = docopt(__doc__, version='PiLapse 1.0')
    pilapse(args)