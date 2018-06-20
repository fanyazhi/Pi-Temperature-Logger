# Pi-Temperature-Logger
Sensor used: DS18B20-PAR  

## Wireless Temperature Sensing With File Server
### How to access temperature csv data
* Connect both the Pi and your machine to the same internet
* Find the server using your computer
* Mac: Go to Finder=>Shared=>raspberrypi
* [Windows](https://www.techrepublic.com/article/how-to-connect-to-linux-samba-shares-from-windows-10/)

Reconnect if loses connection to server, data should not be affected.  
Temperature updates about every 2 seconds, should move to new file after 2 hours (3600 lines).

### Details 
#### Raspberry Pi Setup

* Install Noob 
* Enable SSH
* Set password with `passwd` 
* Change time zone with `sudo dpkg-reconfigure tzdata`

#### Sensor Configuration
* Will constantly read 85 if this is not done
* Add `dtoverlay=w1-gpio,pullup=1` to `/boot/config.txt`
* Type command

```
sudo modprobe w1-gpio pullup=1
sudo modprobe w1-therm strong_pullup=1
```
* Reboot

#### Set up file server: 
[How to set up file server with Samba](https://www.raspberrypi.org/magpi/samba-file-server/])

Put Python program in `/home/pi`

#### Run at reboot with crontab
```
crontab -e
@reboot python /home/pi/Temp.py
```

Or run at boot by changing`sudo nano /home/pi/.bashrc
`

Add after the last line:

```
echo Running at boot 
sudo python /home/pi/sample.py
```
#### Each digital sensor has a unique serial code, find using:

```
sudo modprobe w1-gpio
sudo modprobe w1-therm
cd /sys/bus/w1/devices
ls
```
Remember to change the serial code in the python script


## Wireless Temperature Sensing With Google Spreadsheet 
Unstable, requires good internet signal.

### Details 
#### Raspberry Pi Setup

* Install Noob 
* Enable SSH
* Set password with `passwd` 
* Change time zone with `sudo dpkg-reconfigure tzdata`

#### Sensor Configuration
* Will constantly read 85 if this is not done
* Add `dtoverlay=w1-gpio,pullup=1` to `/boot/config.txt`
* Type command

```
sudo modprobe w1-gpio pullup=1
sudo modprobe w1-therm strong_pullup=1
```
* Reboot

#### Find the dynamic IP address of raspberry pi: 
* Type `arp -a` in the terminal to discover all local devices. If cannot figure out which is the Pi by guessing, do this before and after connecting the Pi to figure out its address.
* Then to access the Pi via SSH, type ssh `pi@<ip address>`
* Enter password

#### Take temperature readings and push to Google Doc
* Set up a google spreadsheet
* Installed Python Library gspread and oauth2client
* Used [OAuth2](http://gspread.readthedocs.io/en/latest/oauth2.html?highlight=scope#
) for authorization
* Share spreadsheet with client email in the json
* Each pi gets its own json, downloaded from google developer console
* Created Python script to read and push to Google Doc
* Automatically clears when row count reaches a certain number of rows so the sheet does not become too large. Modify python script to change row limit. 




---
updated on 6/20/2018