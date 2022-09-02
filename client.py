#4.2.6 Streaming/Client
import socket
from time import ctime
import threading
import sys
import select
import pyaudio

##configuration to Server Socket##
MYADDR = ("0.0.0.0", 45003)
buff = 8192
servSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servSock.bind(MYADDR)
##configuration to Client Socket##
add = '192.168.1.100'
port =12345
cliSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096
cliSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
audio = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    for s in read_list[1:]:
        servSock.sendto(in_data , (x,y))
    return (None, pyaudio.paContinue)

stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
    input=True, frames_per_buffer=CHUNK, stream_callback=callback)
streamr = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
        output=True, frames_per_buffer=CHUNK)
read_list = [servSock]
print ("Waiting for a connection...")
## handShake to get the ip from each other..
# send message so the other side get your IP .
msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)
cliSock.sendto(bytesToSend, (add,port))
# get the client IP
wait_packet = servSock.recvfrom(buff)
Cadd= wait_packet[1]
Cm=wait_packet[0]
y = Cadd[1]
x = Cadd[0]
print ("...Connection made with {0}".format(wait_packet[1]))

def receive():
    try:   
        while True:
            rMessage = cliSock.recvfrom(buff)
          
            streamr.write(rMessage[0])
            #cliSock.close()
    except KeyboardInterrupt:
        pass
    

def send():
    try:
        while True:
            for s in read_list:
                if s is servSock:
                    read_list.append(Cm)
                else:
                    data = servSock.recvfrom(buff)

                    if not data:
                        read_list.remove(servSock)
    except KeyboardInterrupt:
        pass
    servSock.close()


t1 = threading.Thread(target=send, name=1)
t2 = threading.Thread(target=receive, name=2)

t1.start()
t2.start()

t1.join()
t2.join()
















































#                                                                       
