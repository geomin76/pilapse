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
from datetime import datetime
import logging
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

fromaddr = "EMAIL ADDRESS OF THE SENDER"
passwd = "EMAIL PASSWORD OF THE SENDER"
fps = 25

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

    logging.debug("Removing tmp photo directory in case it still exists")
    shutil.rmtree('tmp/')
    
    logging.debug("Removing movie.mp4 file in case it still exists")
    os.remove("movie.mp4")

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


    if args['--time']:
      logging.info("Taking timelapse of with time of {0}".format(args['VALUE']))
      time = getTime(args['VALUE'])
      now = datetime.timestamp(datetime.now())
      finishedTime = now + time
      count = 1
      while now <= finishedTime:
        logging.info("Taking photo {0}".format(str(count)))
        camera.capture('tmp/{0}.jpg'.format(str(count)))
        logging.debug("Saved in /tmp")
        sleep(interval)
        logging.debug("Taking a {0}s interval".format(str(interval)))
        count += 1
        now = datetime.timestamp(datetime.now())


    if args['--cliplen']:
      logging.info("Taking timelapse of {0} clip length".format(args['VALUE']))
      time = getTime(args['VALUE'])
      for i in range(time * fps):
        logging.info("Taking photo {0}".format(str(i)))
        camera.capture('tmp/{0}.jpg'.format(str(i)))
        logging.debug("Saved in /tmp")
        sleep(interval)
        logging.debug("Taking a {0}s interval".format(str(interval)))
    
    
    logging.info("Converting imgs to video file")
    (
        ffmpeg
        .input('./tmp/*.jpg', pattern_type='glob', framerate=fps)
        .output('movie.mp4')
        .run(quiet=True)
    )

    logging.info("Emailing video to {0}".format(",".join(args['--email'])))
    email(fromaddr, ",".join(args['--email']), passwd)

    logging.debug("Removing tmp photo directory")
    shutil.rmtree('tmp/')
    
    logging.debug("Removing movie.mp4 file")
    os.remove("movie.mp4")



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


def getTime(val):
    if val.isdigit():
      time = int(val)      
    elif val[-1] == 's':
      time = int(val[:-1])
    elif val[-1] == 'm':
      time = int(val[:-1]) * 60
    elif val[-1] == 'h':
      time = int(val[:-1]) * 3600
    elif val[-1] == 'd':
      time = int(val[:-1]) * 86400
    else:
      raise Exception("Time format not accepted")
    return time


def email(fromaddr, toaddr, passwd):
    msg = MIMEMultipart() 
    msg['From'] = fromaddr 
    msg['To'] = toaddr
    msg['Subject'] = "Timelapse from pilapse"
    body = "The timelapse is attached to this email"
    msg.attach(MIMEText(body, 'plain')) 
    filename = 'movie.mp4'
    attachment = open("movie.mp4", "rb") 
    p = MIMEBase('application', 'octet-stream') 
    p.set_payload((attachment).read()) 
    encoders.encode_base64(p) 
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    msg.attach(p) 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login(fromaddr, passwd) 
    text = msg.as_string() 
    s.sendmail(fromaddr, toaddr, text) 
    s.quit() 

if __name__ == '__main__':
    args = docopt(__doc__, version='PiLapse 1.0')
    pilapse(args)