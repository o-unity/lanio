#!/usr/bin/python

import lcddriver, os
from time import *
import sys, getopt, json, os, signal, re
import socket
import sched
import time
import threading
import logging
import inspect



realpath = os.path.realpath(__file__)
direname = os.path.dirname(realpath)

json_data=open(direname + "/../../etc/conf/global.json").read()
cfg = json.loads(json_data) 

def signal_term_handler(signal, frame):
  logger.info('terminate display listener normaly')
  lcd.lcd_device.write_cmd(0x00)
  conn.close()
  sys.exit(0)

signal.signal(signal.SIGTERM, signal_term_handler)



lcd = lcddriver.lcd()
scheduler = sched.scheduler(time.time, time.sleep)

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50009              # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((HOST, PORT))
s.listen(1)


def cleanupLCD():
  firstLineDisplay()

#lcd.lcd_display_string("V3.5 192.168.1.1", 1)
#lcd.lcd_display_string("Hallo Tina", 2)

def firstLineDisplay():
  f = os.popen('ifconfig | grep inet | head -1 | cut -d\':\' -f 2 | cut -d\' \' -f 1')
  content = f.read()
  content = content.replace('\n', '')
  content = content.replace('\r', '')
  print content
  lcd.lcd_clear()
  lcd.lcd_display_string(content, 1)

firstLineDisplay()


def wl(file_level, console_level = None):
  global cfg
  function_name = inspect.stack()[1][3]
  logger = logging.getLogger(function_name)
  logger.setLevel(logging.DEBUG) #By default, logs all messages

  fh = logging.FileHandler(direname+"/../../"+cfg['global']['log'] + str(time.strftime("%Y%m%d")) + "_lanio.log")
  fh.setLevel(file_level)

  fh_format = logging.Formatter('%(asctime)s - %(levelname)-5s - DISPLA  - %(message)s')
  fh.setFormatter(fh_format)
  logger.addHandler(fh)

  return logger

# -------------------------------------------------------------------

logger = wl(logging.INFO)
logger.info('======================================================')
logger.info('start display listener')
logger.info('======================================================')



try:
  while 1:
    conn, addr = s.accept()
    data = ""
    print 'Connected by', addr
    while 1:
      data = conn.recv(1024)
      data = data.replace('\n', '')
      data = data.replace('\r', '')
    
      if not data: break

      if data == "quit":
        print "terminate...."
        conn.close()
        break
      
      if data != "":
        try:
      	  scheduler.cancel(e1)
      	  firstLineDisplay()
        except NameError:
          dummy = 1
        except ValueError:
          dummy = 1
  
        lcd.lcd_display_string(data, 2) 
        logger.info('received data: '+ data)
        e1 = scheduler.enter(120, 1, cleanupLCD,())
        t = threading.Thread(target=scheduler.run)
        t.start()
        
        #print e1
        conn.close()
        break


except KeyboardInterrupt:  
    conn.close()      # clean up GPIO on CTRL+C exit  
    lcd.lcd_device.write_cmd(0x00)

conn.close()
lcd.lcd_device.write_cmd(0x00)



#lcd.lcd_device.write_cmd(0x00)
#lcd.lcd_clear()
#lcd.lcd_write(0x00)
