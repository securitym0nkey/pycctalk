from cctalk import *
import struct
import re

#Handles a Coin Acceptor
#keeps track of insert events
class CoinAcceptor:
 ERR_NO = 0
 ERR_REJECT_COIN = 1
 ERR_INHIBITED_COIN = 2
 ERR_MULTIPLE_WINDOW = 3
 ERR_WAKE_UP_TIMEOUT = 4
 ERR_VALIDATION_TIMEOUT = 5
 ERR_CREDIT_SENSOR_TIMEOUT = 6
 ERR_SORTER_OPTO_TIMEOUT = 7
 ERR_2ND_CLOSE_COIN = 8
 ERR_ACCEPT_GATE_NOT_RDY = 9
 ERR_CREDIT_SENS_NOT_RDY = 10
 ERR_SORTER_NOT_RDY = 11
 ERR_REJECT_COIN_NOT_CLD = 12
 ERR_VALIDATION_SENS_NOT_RDY = 13
 ERR_CREDIT_SENS_BLOCKED = 14
 ERR_SORTER_OPTP_BLOCKED = 15
 ERR_CREDIT_SEQ = 16
 ERR_COIN_BACKWARDS = 17
 ERR_COIN_TOO_FAST = 18
 ERR_COIN_TOO_SLOW = 19
 ERR_COS = 20
 ERR_DCE_OPTO_TIMEOUT = 21
 ERR_DCE_OPTO_NOT_SEEN = 22
 ERR_CREDIT_SEN_TOO_ERL = 23
 ERR_REJECT_COIN_REP = 24
 ERR_REJECT_SLUG = 25
 ERR_REJECT_SENS_BLOCKED = 26
 ERR_GAMES_OVERLOAD = 27
 ERR_MAX_COIN_METER_PULSE_EXCEEDED = 28
 ERR_ACCEPT_GATE_OPEN = 29
 ERR_ACCEPT_GATE_CLOSED = 30
 ERR_MANIFOLD_OPTO_TIMEOUT = 31
 ERR_MANIFOLD_OPTO_BLOCKED = 32
 ERR_MAINFOLD_NOT_RDY = 33
 ERR_SECURITY_STATUS_CHD = 34
 ERR_MOTOR_EXCEPTION = 35
 ERR_SWALLOWED_COIN = 36
 ERR_COIN_TOO_FAST2 = 37
 ERR_COIN_TOO_SLOW2 = 38
 ERR_COIM_INCORRECTLY_SORTED = 39
 ERR_EXT_LIGHT_ATTACK = 40
 ERR_COIN_RETURN_MECH_ACT = 254
 ERR_UNKNOWN_ALARM = 255
 manufacturer = ''
 equipment_category = ''
 product_code = ''

 def __init__(self,iface,addr=2):
  self.events = 0
  self.addr = addr
  self.iface = iface
  self.pollmsg = Message(src=1,dst=addr,header=Message.HEADER_READ_BUFFERED_CREDIT)
  self._supportedcoins = ['Error']
  self.__acceptedcoins = 0
  self.iface.addDevice(self)


 def onCoinAccept(self,coin):
  pass
 def __onAccept(self,coinnumid,output):
  self.__acceptedcoins += 1
  self.onCoinAccept(self._supportedcoins[coinnumid])
#  print('[{}] Coin {} into {}'.format(self.events,coinnumid,output) )
#  print(self._supportedcoins[coinnumid])
 def __onError(self,err):
  print('[{}] Error {}'.format(self.events,err))
 def init(self):
  #Get Manufactur
  r = self.iface.send(Message(src=1,dst=self.addr,header=Message.HEADER_REQ_MANUFACTURER_ID))
  self.manufacturer = r.data.decode('ascii')

  r = self.iface.send(Message(src=1,dst=self.addr,header=Message.HEADER_REQ_EQM_CAT_ID))
  self.equipment_category = r.data.decode('ascii')

  r = self.iface.send(Message(src=1,dst=self.addr,header=Message.HEADER_REQ_PRO_CODE))
  self.product_code = r.data.decode('ascii')


  #Get all coin IDs
  msg = Message(src=1,dst=self.addr,header=Message.HEADER_REQ_COINID)
  for x in range(1,9):
   msg.data=struct.pack('B',x)
   response = self.iface.send(msg)
   self._supportedcoins.append(Coin(response.data))

  #Get the current eventcounter value
  startbuffer = self.iface.send(self.pollmsg)
  self.events = startbuffer.data[0]

  #Accept all coins
  msg = Message(src=1,dst=self.addr,header=Message.HEADER_MOD_INHIBIT,data=b'\xff')
  self.iface.send(msg)
  self.onInitCompleted()

 def onInitCompleted(self):
  pass
 def poll(self):
  response = self.iface.send(self.pollmsg)
  eventpointer = response.data[0]

  #No new events nothing todo
  if eventpointer == self.events:
   return

  #New events without overflow
  if eventpointer > self.events:
   eventdiff = eventpointer - self.events
  else: #overflow
   eventdiff = 255-self.events+eventpointer

  #5 or less events to process
  if eventdiff <= 5:
   #go over all events
   for x in range(0,eventdiff):
    p = x*2 +1
    (coinid,slot) = struct.unpack('BB',response.data[p:p+2])

    # coin 0 is actually an error
    if coinid > 0:
     self.__onAccept(coinid,slot)
    else:
     self.__onError(slot)
  self.events = eventpointer

class Coin:
 def __init__(self,coinid):
  self.__id=coinid.decode('ascii')
  rx = re.match('^([A-Z]{2})([0-9]{3})([A-Z])$',self.__id)
  if rx is not None:
   self.__value = int(rx.group(2))
   self.__currency = rx.group(1)
   self.__coinversion = rx.group(3)
  else:
   self.__value = 0
   self.__currency = ''
   self.__coinversion = ''

 @property
 def value(self):
  return self.__value

 def __str__(self):
  return self.__id + " Coin"


