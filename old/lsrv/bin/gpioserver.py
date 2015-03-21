#!/usr/bin/python

import sys, getopt, json, os, signal
import inspect
import logging
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


# CONFIG -------------------------------------------------------

#config = '{"24":{"EVENT":"BOTH","OPTION":{"BOUNCE":1000,"DETECTONCE":1}},"18":{"EVENT":"FE","OPTION":{"BOUNCE":200,"DETECTONCE":1}},"17":{"EVENT":"RE","OPTION":{"BOUNCE":200,"DETECTONCE":1}}}'
#conf = json.loads(config)


json_data=open("/var/www/etc/user_gpio.conf").read()
conf = json.loads(json_data)


# FUNCTIONS ---------------------------------------------------

def signal_term_handler(signal, frame):
  logger.info('')
  logger.info('terminate deamon normaly')
  GPIO.cleanup()
  sys.exit(0)

signal.signal(signal.SIGTERM, signal_term_handler)

def wl(file_level, console_level = None):
  function_name = inspect.stack()[1][3]
  logger = logging.getLogger(function_name)
  logger.setLevel(logging.DEBUG) #By default, logs all messages

  fh = logging.FileHandler("../log/" + str(time.strftime("%Y%m%d")) + "_gpioserver.log")
  fh.setLevel(file_level)
  fh_format = logging.Formatter('%(asctime)s - %(lineno)d - %(levelname)-8s - %(message)s')
  fh.setFormatter(fh_format)
  logger.addHandler(fh)

  return logger

#---  
  
def falling_edge(channel): 
  global conf 
  
  logger.info('falling edge detected on channel ['+str(channel)+']')
  #GPIO.remove_event_detect(channel)
  #GPIO.add_event_detect(channel, GPIO.FALLING, callback=rising_edge, bouncetime=10)  
  
  if conf[str(channel)]['ETYPE'] == "FE":
    submitData = conf[str(channel)]['DATA'];
    submitData = submitData.replace("##value##", "1");
    logger.info('calling ->		' + conf[str(channel)]['EURL'])
    logger.info('          		' + conf[str(channel)]['CONTENTTYPE'])
    logger.info('          		' + conf[str(channel)]['REQUESTTYPE'])
    logger.info('          		' + submitData)
    logger.info('          		' + conf[str(channel)]['USR'])
    logger.info('          		' + conf[str(channel)]['PASS'])
    
    
    f = os.popen('curl --user '+conf[str(channel)]['USR']+':'+conf[str(channel)]['PASS']+' -v -H "Content-Type: '+conf[str(channel)]['CONTENTTYPE']+'" -s -X '+conf[str(channel)]['REQUESTTYPE']+' -d \''+submitData+'\' '+conf[str(channel)]['EURL']+' 2> /dev/null &')
    content = f.read()
    logger.info('response:' + content)

#--- 

def rising_edge(channel): 
  global conf 
  
  logger.info('risign edge detected on channel ['+str(channel)+']')
  GPIO.remove_event_detect(channel)
  GPIO.add_event_detect(channel, GPIO.FALLING, callback=falling_edge, bouncetime=1000) 

 	 

# MAIN ---------------------------------------------------------

logger = wl(logging.INFO)
logger.info(' ')
logger.info(' ')
logger.info('======================================================')
logger.info('start service')
logger.info('======================================================')

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
    time.sleep(60)
  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  








#f = os.popen('curl -H "Content-Type: application/json" -s -X POST -d \'{ "jsonrpc":"2.0","method":"GetValue","params":[32483],"id":1}\' http://pvvvgslmgt014:18080/SelfService/monitoring/')
#content = f.read()



	







# DESTRUCT
logging.shutdown()









