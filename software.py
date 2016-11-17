import MFRC522
import signal
import MySQLdb
import os
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


continue_reading = True
MIFAREReader = MFRC522.MFRC522()

os.system('cls' if os.name == 'nt' else 'clear')

print "Starting system, wait a moment"

access = 1
db = MySQLdb.connect(host="originalnigga.com", user="original_rfid", passwd="rfidcea", db="original_rfid")
cur = db.cursor()
cardid = 0
cdb = 0
autorizacion = 0
user = "clear"

#GPIO.setup(8, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
#GPIO.output(8, False)

number = 0.001
timer = 150

time.sleep(1)
os.system('cls' if os.name == 'nt' else 'clear')
print "Place the card near the reader"


def end_read(signal, frame):
  global continue_reading
  continue_reading = False
  print "Ctrl+C captured, ending read."
  MIFAREReader.GPIO_CLEEN()

signal.signal(signal.SIGINT, end_read)

while continue_reading:
  (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
  if status == MIFAREReader.MI_OK:
    os.system('cls' if os.name == 'nt' else 'clear')
    print "Card detected"
  (status,backData) = MIFAREReader.MFRC522_Anticoll()
  if status == MIFAREReader.MI_OK:
        
    back = str(backData[0])+str(backData[1])+str(backData[2])+str(backData[3])+str(backData[4])
    back2 = str (back)
    print "Cheking User and Card"
    cur.execute("SELECT cardid FROM Usuarios WHERE cardid= %s", (back2,) )
    cardid = cur.fetchone()
    
    if cardid != None:
      cdb = cardid[0]

    cur.execute("SELECT nombre FROM Usuarios WHERE cardid= %s", (back2,) )
    nombre = cur.fetchone()
    if nombre != None:
      user = nombre[0]

    cur.execute("SELECT autorizacion FROM Usuarios WHERE cardid= %s", (back2,) )
    autorizacion = cur.fetchone()
    if autorizacion != None:
      acs = autorizacion[0]
    
    
    print "Wait....."
    if  back2  == cdb:
      if access == acs:
            print "is Card Allowed, Welcome ",user
            #GPIO.output(26, True)
            GPIO.setup(8, GPIO.OUT)
            while timer != 0 :
                     GPIO.output(18, True)
                     time.sleep(number)
                     GPIO.output(18, False)
                     time.sleep(number)
                     timer = timer - 1
            timer = 150
            #GPIO.output(26, 0)
            GPIO.setup(8, GPIO.IN)

      else:
            print user,", You have restricted access"
            for x in range (0, 4):
              while timer != 0 :
                  GPIO.output(18, True)
                  time.sleep(number)
                  GPIO.output(18, False)
                  time.sleep(number)
                  timer = timer - 1
              timer = 150
              time.sleep(0.3)

    else:
            print "Access denied, unregistered card"
            for x in range (0, 4):
              while timer != 0 :
                  GPIO.output(18, True)
                  time.sleep(number)
                  GPIO.output(18, False)
                  time.sleep(number)
                  timer = timer - 1
              timer = 150
              time.sleep(0.3)

        
