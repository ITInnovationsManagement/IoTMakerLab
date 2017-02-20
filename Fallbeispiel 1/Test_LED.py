import RPi.GPIO as GPIO
import time
                                                      
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#Setzt PIN12 als Ausgang
GPIO.setup(12, GPIO.OUT)
print("LED ROT AN")
#Legt Strom an PIN12 an
GPIO.output(12,GPIO.HIGH)
time.sleep(2)
#Entfernt Strom von PIN12
GPIO.output(12, GPIO.LOW)

#Setzt PIN13 als Ausgang
GPIO.setup(13, GPIO.OUT)
print("LED GELB AN")
#Legt Strom an PIN13 an
GPIO.output(13,GPIO.HIGH)
time.sleep(1)
#Entfernt Strom von PIN15
GPIO.output(13, GPIO.LOW)

#Setzt PIN15 als Ausgang
GPIO.setup(15, GPIO.OUT)
print("LED GRÜN AN")
#Legt Strom an PIN15 an
GPIO.output(15,GPIO.HIGH)
time.sleep(1)
#Entfernt Strom von PIN15
GPIO.output(15, GPIO.LOW)

