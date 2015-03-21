#!/usr/bin/python

import sys, getopt, json, os, signal, re, socket
import inspect
import logging
import time
import RPi.GPIO as GPIO



realpath = os.path.realpath(__file__)
direname = os.path.dirname(realpath)

json_data=open(direname + "/../../etc/conf/global.json").read()
cfg = json.loads(json_data) 
#print json.dumps(cfg)


def signal_term_handler(signal, frame):
  logger.info('terminate one wire deamon normaly')
  sys.exit(0)

signal.signal(signal.SIGTERM, signal_term_handler)


def wl(file_level, console_level = None):
  global cfg
  function_name = inspect.stack()[1][3]
  logger = logging.getLogger(function_name)
  logger.setLevel(logging.DEBUG) #By default, logs all messages

  fh = logging.FileHandler(direname+"/../../"+cfg['global']['log'] + str(time.strftime("%Y%m%d")) + "_lanio.log")
  fh.setLevel(file_level)

  fh_format = logging.Formatter('%(asctime)s - %(lineno)d - %(levelname)-5s - ONEWIR  - %(message)s')
  fh.setFormatter(fh_format)
  logger.addHandler(fh)

  return logger

# -------------------------------------------------------------------

def read_sensor(path):
  value = "U"
  try:
    f = open(path, "r")
    line = f.readline()
    if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
      line = f.readline()
      m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
      if m:
        value = str(round(float(m.group(2)) / 1000.0,1))
    f.close()
  except (IOError), e:
    print time.strftime("%x %X"), "Error reading", path, ": ", e
  return value
  
  
# -------------------------------------------------------------------

def sendMsgBus(msg):
	#print temp
	HOST = '127.0.0.1'
	PORT = cfg['msgbus']['cfg']['port'] 
	logger.info('open socket to message bus')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	
	logger.info('send message ['+msg+']')
	s.sendall(msg)
	s.close()

# -------------------------------------------------------------------

logger = wl(logging.INFO)
logger.info('======================================================')
logger.info('start one wire deamon')
logger.info('======================================================')


for (i, item) in enumerate(cfg['onewire']['devices']):
  sensT = read_sensor(cfg['onewire']['cfg']['path']+item['id']+"/w1_slave")
  cfg['onewire']['devices'][i]['temp'] = sensT
  sendMsgBus('{"onewire":{"temp":' + sensT + '}')
  logger.info('init sensor: '+cfg['onewire']['cfg']['path']+item['id']+': '+sensT)
  		


# ------------------------------------------------------------------- 

try:
  while 1:
  	for (i, item) in enumerate(cfg['onewire']['devices']):
  		sensT = read_sensor(cfg['onewire']['cfg']['path']+item['id']+"/w1_slave")
  		if cfg['onewire']['devices'][i]['temp'] != sensT:
  			#print sensT
  			logger.info(cfg['onewire']['cfg']['path']+item['id']+': '+sensT)
  			cfg['onewire']['devices'][i]['temp'] = sensT
  			sendMsgBus('{"onewire":{"temp":' + sensT + '}')
  		
  		time.sleep(cfg['onewire']['cfg']['wait'])
    
  	
except KeyboardInterrupt:  
  logger.info(' ')
  logger.info('one wire terminated manualy')
  logger.info(' ')











