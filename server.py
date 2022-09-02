#4.2.6 Streaming/Server
import socket
from time import ctime
import threading
import sys
import select
import pyaudio
##configuration to Server Socket##
MYADDR = ("0.0.0.0" , 12345)
buff = 8192
servSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servSock.bind(MYADDR)
##configuration to Client Socket##
rADDR = ('192.168.1.100')
rPOTT = 45003
cliSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096

audio = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    for s in read_list[1:]:
        servSock.sendto(in_data , (ip,RandmoPortC))
    return (None, pyaudio.paContinue)

stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
            input=True,frames_per_buffer=CHUNK,stream_callback=callback)
streamr = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True,
                     frames_per_buffer=CHUNK)
# stream.start_stream()
read_list = [servSock]

print ("Waiting for a connection...")
## handShake to get the ip from each other..
# get the client IP
wait_packet = servSock.recvfrom(buff)
Cm = wait_packet[0]
Cadd= wait_packet[1]
ip = Cadd[0]
RandmoPortC= Cadd[1]
#print ("...Connection made with {0}".format(wait_packet[1]))
# send message so the other side get your IP .
msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)
cliSock.sendto(bytesToSend, (rADDR ,rPOTT) )


def receive():
    try:
        while True:
            rMessage = cliSock.recvfrom(buff)
            
            streamr.write(rMessage[0])

    except KeyboardInterrupt:
        pass
            #cliSock.close()
            
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

t1 = threading.Thread(target=send, name=3 )
t2 = threading.Thread(target=receive, name=4)

t1.start()
t2.start()
t1.join()
t2.join()














































                                                                        
