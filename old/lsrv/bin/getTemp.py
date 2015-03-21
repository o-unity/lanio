#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, os, time

# function: read and parse sensor data file
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

# define pathes to 1-wire sensor data
pathes = (
  "/sys/bus/w1/devices/28-0314640daeff/w1_slave"
)

# read sensor data
#for path in pathes:
#  path = "/sys/bus/w1/devices/28-0314640daeff/w1_slave"
#  print read_sensor(path)
#  time.sleep(30)
  
 
flag = 1
temp = 0
temp2 = 0
while (flag): 
  temp2 = temp
  temp = read_sensor("/sys/bus/w1/devices/28-0314640daeff/w1_slave")
  if temp2 != temp:
    print temp
  time.sleep(11)
    
    