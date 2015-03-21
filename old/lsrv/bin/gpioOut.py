import RPi.GPIO as GPIO ## Import GPIO library
import time



GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT) 




try:  
  GPIO.output(11,False) 
  time.sleep(60)
  GPIO.output(11,True) 
  time.sleep(5)
  GPIO.output(11,False) 
  time.sleep(5)
  GPIO.output(11,True) 
  time.sleep(5)
  GPIO.output(11,False) 
  time.sleep(5)
  GPIO.output(11,True) 
  time.sleep(5)
  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  