#!/usr/bin/python

import sys, getopt, json, os, signal
import inspect
import logging
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)



realpath = os.path.realpath(__file__)
direname = os.path.dirname(realpath)

json_data=open(direname + "/../../etc/conf/globalDev.json").read()
cfg = json.loads(json_data) 

# -----------------------------------------------------------------------  

def signal_term_handler(signal, frame):
  logger.info('terminate GPI Deamon normaly')
  GPIO.cleanup()
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
 
 
# -----------------------------------------------------------------------  
  
  
def falling_edge(channel): 
  global conf 
  logger.info('falling edge detected on channel ['+str(channel)+']')
  print 'falling edge detected on channel ['+str(channel)+']'

    

# -----------------------------------------------------------------------  


# MAIN ---------------------------------------------------------

logger = wl(logging.INFO)
logger.info(' ')
logger.info(' ')
logger.info('======================================================')
logger.info('start GPI Listener')
logger.info('======================================================')






sys.exit(0)

for GPIONO in conf:
  if conf[GPIONO]['active'] == "1":
    logger.info('create interrupt for GPIO ['+GPIONO+']')
    logger.info(' -> Event type: ['+conf[GPIONO]['ETYPE']+']')
  
    if conf[GPIONO]['ETYPE'] == "FE":
      GPIO.setup(int(GPIONO), GPIO.IN, pull_up_down=GPIO.PUD_UP)
      GPIO.add_event_detect(int(GPIONO), GPIO.FALLING, callback=falling_edge, bouncetime=1000) 
  

   


try:  
  flag = 1
  while (flag): 
    logger.info('service up and running, waiting for interrupts')
    time.sleep(300)
  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  








#f = os.popen('curl -H "Content-Type: application/json" -s -X POST -d \'{ "jsonrpc":"2.0","method":"GetValue","params":[32483],"id":1}\' http://pvvvgslmgt014:18080/SelfService/monitoring/')
#content = f.read()



	







# DESTRUCT
logging.shutdown()









