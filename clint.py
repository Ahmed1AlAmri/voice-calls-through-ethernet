#4.2.3 Simplex Communication/Client side
import RPi.GPIO as GPIO
import socket


pushON=16
pushOFF=20
LED=23
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)#LED
GPIO.setup(pushOFF, GPIO.IN)#PushOff
GPIO.setup(pushON, GPIO.IN)#PushON

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = '192.168.1.100'
port = 9999



while True:
   
    if (GPIO.input(pushON)==True):
        data="Y"
        bytesToSend =str.encode(data)
        s.sendto(bytesToSend,(host, port))
    if (GPIO.input(pushOFF)==True):
        data="N"
        bytesToSend =str.encode(data)
        s.sendto(bytesToSend,(host, port))
        
        
        
        
GPIO.cleanup()






























#                                                                               
