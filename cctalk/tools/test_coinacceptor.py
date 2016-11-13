#!/usr/bin/env python
import os
import sys
import serial
sys.path.append(os.getcwd())
import serial
import cctalk
from cctalk.coinacceptor import Coin,CoinAcceptor

class TestAcceptor(CoinAcceptor):
 def onCoinAccept(self,coin):
  print("A {} was inserted and accepted".format(coin) )
 def onInitCompleted(self):
  print("Manufacturer:\t\t{}".format(self.manufacturer))
  print("Equipment Category:\t{}".format(self.equipment_category))
  print("Product Code:\t\t{}".format(self.product_code))

def main():

 port = '/dev/ttyUSB0'

 try:
  interface = cctalk.SerialInterface(port)
  ca = TestAcceptor(interface)
  interface.start()
 except serial.SerialException:
  print("Error while opening serial port {}".format(port))

if __name__ == '__main__':
 main()
