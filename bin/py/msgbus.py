#!/usr/bin/python


import sys, getopt, json, os, signal, re, socket
import inspect
import logging
import time
import threading
import requests
from array import *




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

  fh_format = logging.Formatter('%(asctime)s - %(levelname)-5s - MSGBUS  - %(message)s')
  fh.setFormatter(fh_format)
  logger.addHandler(fh)

  return logger
  
  
# -----------------------------------------------------------------------  

def sendDisplay(params):
	#print "in postDisplay2Line" + str(params)
	opensocket(cfg['display']['cfg']['port'],"display deamon",json.dumps(params))

def switchRelay(params):
	#print "in postDisplay2Line" + str(params)
	opensocket(cfg['gpo']['cfg']['port'],"gpo deamon",json.dumps(params))	

def JSONcall(params):
	#print "in JSONcall\n" + str(params) + "\n\n"
	logger.info('call REST API ' + params['eurl'])
	r = requests.post(params['eurl'], params['data'], auth=(params['usr'], params['pass']))

	logger.info('response: ' + str(r.json))	
	if "Response [200]" in str(r.json): 
		logger.info('REST call successful')	


def threadDispatcher(functionName,params):
	getattr(sys.modules[__name__], "%s" % functionName)(params)
	

def opensocket(port,name,msg):
	#print temp
	try:
		HOST = '127.0.0.1'
		PORT = port 
		logger.info('open socket to ' + name)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, PORT))
		
		logger.info('send message '+msg)
		s.sendall(msg)
		s.close()
		
	except:  
		logger.info('could not connect to ' + name)
		
# -----------------------------------------------------------------------


logger = wl(logging.INFO)
logger.info('======================================================')
logger.info('start message bus')
logger.info('======================================================')


# -------------------------------------------------------------------
 

def parseMessage(msg):
	try:
	 js = json.loads(msg) 
	 for domain in js:
		for instance in js[domain]:
			
			try:
				for (u1, fFunc) in enumerate(cfg['events'][domain][instance]['functions']):
					fDetails = cfg['events'][domain][instance]['functions'][u1]
					eventParams = js[domain][instance]
					params = fDetails['params']
					functionName = fDetails['name'].encode('ascii','ignore')
					
					#print functionName
					
					#for (u1, param) in enumerate(params):
					#	for (u2, eparam) in enumerate(eventParams):
					#		try:
					#			params[param] = params[param].replace("##"+eparam+"##", str(eventParams[eparam]))
					#		except AttributeError:
					#			break
					
					paramsStr = json.dumps(params)
					for (u2, eparam) in enumerate(eventParams):
						try:
							paramsStr = paramsStr.replace("##"+eparam+"##", str(eventParams[eparam]))
						except AttributeError:
							break					
					params = json.loads(paramsStr) 
					
					#logger.info('event found, threading: '+domain+"->"+instance+"-->"+fDetails['function']+"("+str(params)+")")
					logger.info('event found, threading: '+domain+"->"+instance+"-->"+functionName)
					#getattr(sys.modules[__name__], "%s" % fDetails['function'])(params)
					
					t = threading.Thread(target=threadDispatcher, args = (functionName, params))
					t.start()			
					
			except KeyError:
				break
	
	except KeyboardInterrupt:  
		print "keyboard exit"
			
# -------------------------------------------------------------------

#msg = '{"onewire": {"28-0314640daeff":{"value":20.4}}}'
#parseMessage(msg)

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
      
      if not data: break
      
      conn.sendall("ok\n")
      conn.close() 
      
      # PARSE NOW DATA STRING
      parseMessage(data)
      
      # RELOAD CONFIG
      json_data=open(direname + "/../../etc/conf/global.json").read()
      cfg = json.loads(json_data) 
  
      break


except KeyboardInterrupt:  
    logger.info('terminate message bus by keyboard') 
























