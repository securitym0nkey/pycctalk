import struct
import serial
from threading import Thread
import time
#A ccTalk Message
class Message:

 HEADER_SIMPLEPOLL=254
 HEADER_REQ_POLLIG_PRIO=249
 HEADER_REQ_STATUS=248
 HEADER_REQ_VAR_SET=247
 HEADER_REQ_MANUFACTURER_ID = 246
 HEADER_REQ_EQM_CAT_ID = 245
 HEADER_REQ_PRO_CODE = 244
 HEADER_REQ_SN = 242
 HEADER_REQ_SOFT_VER = 241
 HEADER_REQ_DBVERION=243
 HEADER_MOD_INHIBIT=231
 HEADER_REQ_INHIBIT_STATUS=230
 HEADER_READ_BUFFERED_CREDIT=229
 HEADER_MOD_MASTER_INHIBIT=228
 HEADER_REQ_MASTER_INHIBIT=227
 HEADER_REQ_COINID=184
 HEADER_RESPONSE=0

 def __init__(self,src,dst,header,data=b'',checksum=None):
  self.src=src
  self.dst=dst
  self.header=header
  self.data=data
  self.checksum=checksum

 #Checks whether the data is valid by using the checksum
 def is_valid(self):
  pass

 def set_checksum(self):
  pass

 @staticmethod
 def calcchecksum(d):
  return 256-(sum(d) & 0xFF)


 def getBytes(self):
  b=struct.pack('BBBB',self.dst,len(self.data),self.src,self.header)
  b+=self.data
  b+=struct.pack('B',Message.calcchecksum(b))
  return b

#A ccTalk interface. The master part
class Interface(Thread):
 __loop=True
 __devices = []
 def addDevice(self,dev):
  self.__devices.append(dev)
 def run(self):
  #init devices
  for dev in self.__devices:
   dev.init()

  while self.__loop:
   time.sleep(0.2)
   for dev in self.__devices:
    dev.poll()

 #Sends a message to the Bus should return the response Message
 def send(self,msg):
  pass

class SerialInterface(Interface):
 def __init__(self,serint):
  super().__init__()
  self.ser=serial.Serial(serint,9600)

 def receive(self):
  headers = self.ser.read(4)
  (dst,size,src,header) = struct.unpack('BBBB',headers)
  if size > 0:
   data = self.ser.read(size)
  else:
   data = b''
  checksum=self.ser.read(1)
  msg = Message(src=src,dst=dst,header=header,data=data,checksum=checksum)
  return msg

 def send(self,msg):
  self.ser.write(msg.getBytes())
  while True:
   msg = self.receive()
   if msg.header == Message.HEADER_RESPONSE:
    return msg


