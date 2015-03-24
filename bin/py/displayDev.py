#!/usr/bin/python


import sys, getopt, json, os, signal, re, socket
import inspect
import logging
import lcddriver, os
from time import *
import time
import sched
import threading

from array import *




realpath = os.path.realpath(__file__)
direname = os.path.dirname(realpath)

json_data=open(direname + "/../../etc/conf/global.json").read()
cfg = json.loads(json_data) 


def signal_term_handler(signal, frame):
  logger.info('terminate display listener normaly')
  conn.close()
  sys.exit(0)

signal.signal(signal.SIGTERM, signal_term_handler)


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
  
# -----------------------------------------------------------------------
# PRIVATE FUNCTIONS

def text2L(value):
	lcd.lcd_display_string(value, 2)
	displayOff(5)

def displayOff(tValue):
	try:
		scheduler.cancel(e1)
	except:
		dummy = 1
		
	e1 = scheduler.enter(tValue, 1, displayLEDOff,())
	t = threading.Thread(target=scheduler.run)
	t.start()

def displayLEDOff():
	logger.info('display off')
	lcd.lcd_device.write_cmd(0x00)
	 
# -----------------------------------------------------------------------
# LCD DRIVER

lcd = lcddriver.lcd()
scheduler = sched.scheduler(time.time, time.sleep)

# -----------------------------------------------------------------------


logger = wl(logging.INFO)
logger.info('======================================================')
logger.info('start display listener')
logger.info('======================================================')


# -------------------------------------------------------------------
 


def parseMessage(msg):
	try:
	 js = json.loads(msg) 
	 for functionName in js:
	 	try:
	 		logger.info('call private function '+functionName+'('+str(js[functionName])+')')	
	 		getattr(sys.modules[__name__], "%s" % functionName)(js[functionName])
	 	except:  
			logger.info('could not call function name ['+functionName+']')	
	
	except:  
		logger.info('error in parsing message')

			
# -------------------------------------------------------------------

#msg = '{"text2L": "20.4C"}'
#parseMessage(msg)

HOST = '' 
PORT = cfg['display']['cfg']['port']

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((HOST, PORT))
s.listen(1)


try:
  while 1:
    conn, addr = s.accept()
    data = ""
    #print 'Connected by', addr
    logger.info('Connected by: '+ str(addr))
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
        conn.close()
        logger.info('received data: '+data)
        parseMessage(data)
        break


except KeyboardInterrupt:  
    conn.close()      # clean up GPIO on CTRL+C exit  
    lcd.lcd_device.write_cmd(0x00)

conn.close()
lcd.lcd_device.write_cmd(0x00)









