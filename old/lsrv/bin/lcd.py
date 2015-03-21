import lcddriver, os
from time import *
import socket
import sched
import time
import threading

lcd = lcddriver.lcd()
scheduler = sched.scheduler(time.time, time.sleep)

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50009              # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((HOST, PORT))
s.listen(1)


def cleanupLCD():
  firstLineDisplay()

#lcd.lcd_display_string("V3.5 192.168.1.1", 1)
#lcd.lcd_display_string("Hallo Tina", 2)

def firstLineDisplay():
  f = os.popen('ifconfig | grep inet | head -1 | cut -d\':\' -f 2 | cut -d\' \' -f 1')
  content = f.read()
  content = content.replace('\n', '')
  content = content.replace('\r', '')
  print content
  lcd.lcd_clear()
  lcd.lcd_display_string(content, 1)

firstLineDisplay()


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
      
      if data != "":
        try:
      	  scheduler.cancel(e1)
      	  firstLineDisplay()
        except NameError:
          dummy = 1
        except ValueError:
          dummy = 1
  
        lcd.lcd_display_string(data, 2) 
        e1 = scheduler.enter(10, 1, cleanupLCD,())
        t = threading.Thread(target=scheduler.run)
        t.start()
        
        #print e1
        conn.close()
        break


except KeyboardInterrupt:  
    conn.close()      # clean up GPIO on CTRL+C exit  
    lcd.lcd_device.write_cmd(0x00)

conn.close()
lcd.lcd_device.write_cmd(0x00)



#lcd.lcd_device.write_cmd(0x00)
#lcd.lcd_clear()
#lcd.lcd_write(0x00)
