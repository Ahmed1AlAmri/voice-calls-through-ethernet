# 4.2.1 Controlling LED ON/OFF using Push Button
import RPi.GPIO as GPIO

pushON=16
pushOFF=20
LED=23
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED, GPIO.OUT)#LED
GPIO.setup(pushOFF, GPIO.IN)#PushOff
GPIO.setup(pushON, GPIO.IN)#PushON

while True:
    if (GPIO.input(pushON)==True):
        GPIO.output(LED,1)
    if (GPIO.input(pushOFF)==True):
        GPIO.output(LED,0)
GPIO.cleanup()
















































#                                                                   
