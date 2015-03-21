# Echo server program
import socket
import RPi.GPIO as GPIO ## Import GPIO library
import time


GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT) 

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50008              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

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
      
      if data == "on":
        GPIO.output(11,False)
        print "gpio on"
        conn.sendall("gpio on\n")
        conn.close()
        break
      elif data == "off":
        GPIO.output(11,True)
        print "gpio off"
        conn.sendall("gpio off\n")
        conn.close()
        break
      else:
       conn.sendall("unknown\n") 


except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  

GPIO.cleanup()           # clean up GPIO on normal exit  
conn.close()