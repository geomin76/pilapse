# PiLapse

### Welcome to PiLapse! 

sample time lapse demo!

PiLapse is a Raspberry Pi Python command line tool that records, compiles and emails time lapse video clips

### Getting Started

Install arducam jazz and plug in camera

Open pilapse.py, go to line 40 and 41 and fill in the `EMAIL ADDRESS OF THE SENDER` and `EMAIL PASSWORD OF THE SENDER`

Ensure that your email is allowing "less secure apps" to access the account
- [Gmail](https://www.google.com/settings/security/lesssecureapps)
- [Yahoo](https://support.reolink.com/hc/en-us/articles/360004195474-How-to-Allow-Less-Secure-Apps-to-Access-Your-Yahoo-Mail)
- [Outlook](https://answers.microsoft.com/en-us/msoffice/forum/msoffice_outlook-mso_win10-mso_365hp/outlook-security/e92fbfb5-504e-4709-85ce-4996c5a6f14a)

Open a command line, and type these commands
- `$ git clone https://github.com/geomin76/pilapse.git`
- `$ cd pilapse`
- `$ python -m venv venv`
- `$ pip install -r requirements.txt`
- `$ python pilapse.py`

The app is now running! Go to a browser and access

### Documentation

```
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
  --help                Show this scre
```