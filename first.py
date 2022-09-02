#4.2.7 Controlling the Streaming
import RPi.GPIO as GPIO
import socket
import threading
import os
print(os.getpid())
os.system("pkill -f second.py")
##configuration for the GPIO##
pushON=16
pushOFF=20
LED=23
tone = 12
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)#LED
GPIO.setup(tone, GPIO.OUT)#Tone
GPIO.setup(pushOFF, GPIO.IN)#PushOff
GPIO.setup(pushON, GPIO.IN)#PushON
# Varibals for M/D
global flag, token, Confirm, busy
flag = 2
busy = 0
token = 1
Confirm = 0
buff = 8192
##configuration for Server Socket##
addressSend = ("0.0.0.0" , 2225)
servSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servSock.bind(addressSend)
##configuration for Client Socket##
cliSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addressRecive=('192.168.1.100',1114)

HandShake = 1 # so we do the HandShake only at the begin
First_Thread = 1 # so we only open the thread once .
# here one of the node will get the Message first then will leave the while
#                                                                                                   .
while ( HandShake == 1):
    def Lis():
        global HandShake, ad, da,cm
        da , ad = servSock.recvfrom(buff)
        cm = da
        ip = ad[0]
        port = ad[1]
        HandShake = 0

    def SendD():
        global HandShake
        msgFromClient       = "Hi Do You Hear Me ?"
        bytesToSend         = str.encode(msgFromClient)
        cliSock.sendto(bytesToSend, (addressRecive) )
        HandShake = 0

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
print ("WORK !")
# Here one of the node will start the call by the push buttom.
def MakeTheCall():
    global flag, token, Confirm , busy
    while True:
        if (GPIO.input(pushON)==True and token == 1):
            sdata="CAN I CALL YOU"
            bytesToSend =str.encode(sdata)
            servSock.sendto(bytesToSend,(ad))
            busy = 1
        if (GPIO.input(pushOFF)==True and token == 1):
            sdata="I WANT TO FINSH THE CALL"
            bytesToSend =str.encode(sdata)
            servSock.sendto(bytesToSend,(ad))
def DecisionToMake():
    def AnsOrRjc():
        global flag,busy, token , Confirm
        while True:
            if (flag == 0 ):
                if (GPIO.input(pushON)==True and flag==0):
                        GPIO.output(tone,0)
                        GPIO.output(LED,1)
                        Confirm = 1
                        ConfirmMessage = "OK"
                        bytesToSend =str.encode(ConfirmMessage)
                        servSock.sendto(bytesToSend,(ad))
                        if(Confirm == 1):
                            GPIO.cleanup()
                            cliSock.close()
                            servSock.close()
                            os.system("python3 sec.py")
                if (GPIO.input(pushOFF)==True and flag==0):
                        GPIO.output(tone,0)
                        GPIO.output(LED,0)
                        flag=2
                        busy = 0
                        token = 1
                        ConfirmMessage = "NO"
                        bytesToSend =str.encode(ConfirmMessage)
                        servSock.sendto(bytesToSend,(ad))
                if(flag==1):
                    GPIO.output(tone,0)
                    GPIO.output(LED,0)
                    flag=2
                    token = 1
    def Ring():
         global flag, busy, token , Confirm
         while True:
            data,add = cliSock.recvfrom(buff)
            if (data[:].decode("utf-8") == "CAN I CALL YOU" and busy == 0):
                flag=0 #accept the call
                GPIO.output(tone,1)
                busy=1
                token = 0
            if(data[:].decode("utf-8") == "I WANT TO FINSH THE CALL"):
                flag=2
                busy = 0
                GPIO.output(LED,0)
                GPIO.output(tone,0)
                token = 1
            if (data[:].decode("utf-8") == "OK"):
                
                    Confirm = 1
                    flag=0
                    GPIO.output(LED,1)
                    if(Confirm == 1):
                        GPIO.cleanup()
                        cliSock.close()
                        servSock.close()
                        os.system("python3 sec.py")
            if (data[:].decode("utf-8") == "NO"):
                    Confirm = 0
                    GPIO.output(LED,0)
    t5 = threading.Thread(target=Ring)
    t6 = threading.Thread(target=AnsOrRjc)
    t5.start()
    t6.start()
    t5.join()
    t6.join()
t3 = threading.Thread(target=MakeTheCall)
t4 = threading.Thread(target=DecisionToMake)
t3.start()
t4.start()
t3.join()
t4.join()















































#
