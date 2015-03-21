#!/usr/bin/python


import sys, getopt, json, os, signal, re, socket
import inspect
import logging
import time



realpath = os.path.realpath(__file__)
direname = os.path.dirname(realpath)

json_data=open(direname + "/../../etc/conf/global.json").read()
cfg = json.loads(json_data) 


def signal_term_handler(signal, frame):
  logger.info('terminate message bus normaly')
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

  fh_format = logging.Formatter('%(asctime)s - %(lineno)d - %(levelname)-5s - MSGBUS  - %(message)s')
  fh.setFormatter(fh_format)
  logger.addHandler(fh)

  return logger


# -------------------------------------------------------------------


logger = wl(logging.INFO)
logger.info('======================================================')
logger.info('start message bus')
logger.info('======================================================')



# -------------------------------------------------------------------


HOST = ''                 							# Symbolic name meaning all available interfaces
PORT = cfg['msgbus']['cfg']['port']              	# Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((HOST, PORT))
s.listen(1)



try:
  while 1:
    conn, addr = s.accept()
    data = ""
    connSTR = 'Connected by', addr
    logger.info(connSTR)
    
    while 1:
      data = conn.recv(1024)
      data = data.replace('\n', '')
      data = data.replace('\r', '')
      logger.info('data received: '+data)
      logger.info('')
    
      if not data: break
      
      conn.sendall("ok\n")
	  
      # PARSE DATA
      conn.close() 
      break


except KeyboardInterrupt:  
    logger.info('terminate message bus by keyboard') 
























