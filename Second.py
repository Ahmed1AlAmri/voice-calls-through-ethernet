#4.2.7 Controlling the Streaming
import RPi.GPIO as GPIO
import socket
import threading
import pyaudio
import os

print(os.getpid())
os.system("pkill -f first.py")
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096
buff = 8192
##configuration for the GPIO##
pushOFF=20
LED=23
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)#LED
GPIO.setup(pushOFF, GPIO.IN)#PushOff
##configuration to Server Socket##
addressSend = ("0.0.0.0" , 8888)
servSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servSock.bind(addressSend)
##configuration to Client Socket##
cliSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addressRecive=('192.168.1.100',9999)
##configuration to Server Socket##
addressSendV = ("0.0.0.0" , 6666)
servSockV = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servSockV.bind(addressSendV)
##configuration to Client Socket##
cliSockV = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addressReciveV=('192.168.1.100',7777)
audio = pyaudio.PyAudio()
def callback(in_data, frame_count, time_info, status):
    for s in read_list[1:]:
        servSockV.sendto(in_data , (adV))
    return (None, pyaudio.paContinue)
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                input=True, frames_per_buffer=CHUNK, stream_callback=callback)
streamr = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    output=True, frames_per_buffer=CHUNK)
# stream.start_stream()
read_list = [servSockV]
global HandShake ,First_Thread,Secand_Thread
HandShake = 1 # so we do the inination only at the begin
First_Thread = 1 # so we only open the thread once .
Secand_Thread = 1 # so we only open the thread once .
# here one of the node will get the Message first then will leave the while
while ( HandShake == 1):
    def Lis():
        global HandShake
        global ad,da , cm , cmV,adV
        da , ad = servSock.recvfrom(buff)
        daV , adV = servSockV.recvfrom(buff)
        cmV = daV
        cm = da
        ip = ad[0]
        port = ad[1]
        print(ad)
        print(adV)
        print(da[:].decode("utf-8"))
        HandShake = 0
    def SendD():
        global HandShake
        msgFromClient       = "Hi Do You Hear Me ?"
        bytesToSend         = str.encode(msgFromClient)
        cliSock.sendto(bytesToSend, (addressRecive) )
        cliSockV.sendto(bytesToSend, (addressReciveV) )
        HandShake = 0
        print ("Waiting for a connection...")


    if (First_Thread == 1):
        t1 = threading.Thread(target=SendD)
        t2 = threading.Thread(target=Lis)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        First_Thread = 0

if (da[:].decode("utf-8") == "Hi Do You Hear Me ?"):
    msgFromClient       = "Yes I DO"
    bytesToSend         = str.encode(msgFromClient)
    cliSock.sendto(bytesToSend, (addressRecive) )
    cliSockV.sendto(bytesToSend, (addressReciveV) )

print ("WORK aduio !")

import RPi.GPIO as GPIO                                                                                 
def receive():
    try:
        while True:
            rMessage = cliSockV.recvfrom(buff)
            streamr.write(rMessage[0])

            if (GPIO.input(pushOFF)==True ):
                GPIO.output(LED,0)
                msgFromClient       = "END THE CALL"
                bytesToSend         = str.encode(msgFromClient)
                cliSock.sendto(bytesToSend, (addressRecive) )
                GPIO.cleanup()
                os.system("python3 first.py")

    except KeyboardInterrupt:
        pass
            #cliSock.close()

def send():

    try:
        while True:


            for s in read_list:
                if s is servSockV:
                    read_list.append(cmV)

                else:
                    data = servSockV.recvfrom(buff)

                    if not data:
                        read_list.remove(servSockV)
    except KeyboardInterrupt:
        pass
    servSockV.close()

def wait_for_end():
    da , ad = servSock.recvfrom(buff)
    if (da[:].decode("utf-8") == "END THE CALL"):
        GPIO.output(LED,0)
        GPIO.cleanup()
        os.system("python3 first.py")




t3 = threading.Thread(target=send)
t4 = threading.Thread(target=receive)
t5 = threading.Thread(target=hopework)

t3.start()
t4.start()
t5.start()
t3.join()
t4.join()
t5.join()
















































#                                                                           
#       
