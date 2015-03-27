#!/usr/bin/python

import sys, getopt, json, os, signal, socket
import inspect
import logging
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)



realpath = os.path.realpath(__file__)
direname = os.path.dirname(realpath)

json_data=open(direname + "/../../etc/conf/global.json").read()
cfg = json.loads(json_data) 

# -----------------------------------------------------------------------  

def signal_term_handler(signal, frame):
  destructSave()
  GPIO.cleanup()
  logger.info('terminate GPI Deamon normaly')
  sys.exit(0)

signal.signal(signal.SIGTERM, signal_term_handler)


def wl(file_level, console_level = None):
  global cfg
  function_name = inspect.stack()[1][3]
  logger = logging.getLogger(function_name)
  logger.setLevel(logging.DEBUG) #By default, logs all messages

  fh = logging.FileHandler(direname+"/../../"+cfg['global']['log'] + str(time.strftime("%Y%m%d")) + "_lanio.log")
  fh.setLevel(file_level)

  fh_format = logging.Formatter('%(asctime)s - %(levelname)-5s - GPINPU  - %(message)s')
  fh.setFormatter(fh_format)
  logger.addHandler(fh)

  return logger
 

def destructSave():
	global lv
	logger.info('save GPI values')
	data_string = json.dumps(lv, sort_keys = True, indent = 4)
	fd = open(direname + "/../../etc/conf/gpiValues.json", 'w')
	fd.write(data_string)
	fd.close() 	
	

# -----------------------------------------------------------------------  
  
  
def falling_edge(channel): 
  global cfg 
  global domain 
  
  logger.info('')
  logger.info('falling edge detected on channel ['+cfg['events'][domain][str(channel)]['name']+']')
  
  if cfg['events'][domain][str(channel)]['condition']['behavior'] == "toggle":
  	if lv['gpi'][str(channel)]['value'] == 1:
  		lv['gpi'][str(channel)]['value'] = 0
  	else:
  		lv['gpi'][str(channel)]['value'] = 1
  		
  
  sendMsgBus('{"gpi": {"'+str(channel)+'":{"value":'+str(lv['gpi'][str(channel)]['value'])+'}}}')
  
  
  

    

# -----------------------------------------------------------------------  

def sendMsgBus(msg):
	#print temp
	HOST = '127.0.0.1'
	PORT = cfg['msgbus']['cfg']['port'] 
	logger.info('open socket to message bus')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	
	logger.info('send message '+msg)
	s.sendall(msg)
	s.close()

	
def setJsonPointer(key):
	global lv
	try:
		lv['gpi'][key]['value'] = lv['gpi'][key]['value']
	except:
		try:
			dicta = json.dumps(lv['gpi'])
		except:
			dicta = ''
		dictb = '"'+key+'": {"value": 0}'
		if dicta == "":
			jsConcat = '{"gpi": {' + dictb + '}}'
		else:
			jsConcat = '{"gpi": ' + dicta[:-1] + ',' + dictb + '}}'

		lv = json.loads(jsConcat) 


# MAIN ---------------------------------------------------------

logger = wl(logging.INFO)
logger.info(' ')
logger.info(' ')
logger.info('======================================================')
logger.info('start GPI Listener')
logger.info('======================================================')


domain = "gpi"

# READ LAST VALUES ---------------------------------------------------------

try:
	json_lastvalue=open(direname + "/../../etc/conf/gpiValues.json").read()
	lv = json.loads(json_lastvalue) 
except:
	nothing = True
	

try:
	for (u1, port) in enumerate(cfg['events'][domain]):
		try:
			portConfig = cfg['events'][domain][port]['condition']['type']
			logger.info('create interrupt for '+cfg['events'][domain][port]['name']+' / '+portConfig)
			
			if portConfig == "FE":
				GPIO.setup(int(port), GPIO.IN, pull_up_down=GPIO.PUD_UP)
				GPIO.add_event_detect(int(port), GPIO.FALLING, callback=falling_edge, bouncetime=1000) 
				setJsonPointer(str(port))
			else:
				logger.info('could not enable config type: ' + portConfig)
		except:
			break
except:
	logger.info('error in parsing cfg array')



try:  
  flag = 1
  while (flag): 
    logger.info('service up and running, waiting for interrupts')
    time.sleep(300)
  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
    logger.info('terminate GPI Deamon by Keyboard')
    destructSave()
GPIO.cleanup()           # clean up GPIO on normal exit  



# DESTRUCT
logging.shutdown()




