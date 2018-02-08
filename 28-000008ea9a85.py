import sys
import time
import datetime
import gspread
import oauth2client.client
import json
import os
import argparse
import glob

from oauth2client.service_account import ServiceAccountCredentials

import httplib2
from oauth2client import client

#json filename for credentials
JSON_FILENAME = 'gspread.json'

# Google sheet to save to
GSHEET_NAME = 'Temp_log'
SCOPES = ['https://spreadsheets.google.com/feeds']

#load credentials from json and open the spreadsheet for writing
json_key = json.load(open(JSON_FILENAME))

creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILENAME, SCOPES)

client_inst = gspread.authorize(creds)
gsheet = client_inst.open(GSHEET_NAME).get_worksheet(0)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm strong_pullup=1')
while True:
        temp_sensor = '/sys/bus/w1/devices/28-000008ea9a85/w1_slave'

        def temp_raw():
                f = open(temp_sensor, 'r')
                lines = f.readlines()
                f.close()
                return lines

        def read_temp():
                lines = temp_raw()
                while lines[0].strip()[-3:] != 'YES':
                        time.sleep(0.2)
                        lines = temp_raw()
                temp_output = lines[1].find('t=')

                if temp_output != -1:
                        temp_string = lines[1].strip()[temp_output+2:]
                        temp_c = float(temp_string) / 1000.0
                        temp_f = temp_c * 9.0 / 5.0 + 32.0
                        return temp_c

        temp_c = read_temp()
        curr_time = datetime.datetime.now()
        print ("Writing")
#write a new row to the spreadsheet with the current time and temperature
gsheet.append_row((curr_time, temp_c))
#remove all rows once row count reaches 200
        if gsheet.row_count >= 200:
            gsheet.resize(rows=1)
