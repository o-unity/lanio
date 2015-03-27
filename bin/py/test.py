#!/usr/bin/python


import sys, getopt, json, os
from collections import Mapping

from array import *




realpath = os.path.realpath(__file__)
direname = os.path.dirname(realpath)


try:
	json_lastvalue=open(direname + "/../../etc/conf/gpiValues.json").read()
	lv = json.loads(json_lastvalue) 
except:
	nothing = True


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



setJsonPointer("23")
data_string = json.dumps(lv, sort_keys = True, indent = 4)
fd = open(direname + "/../../etc/conf/gpiValues.json", 'w')
fd.write(data_string)
fd.close() 


#try:
#	if lv['gpi']['22']['value'] != "":
#		lv['gpi']['22']['value'] = 0
#except:
	#lv['gpi'] = ['22']
	#lv['gpi']['22'] = ['value']
	#lv['gpi']['22']['value'] = 0


