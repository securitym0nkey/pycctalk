#!/usr/bin/env python
import os
import sys
import serial
import argparse
sys.path.append(os.getcwd())
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
 argp = argparse.ArgumentParser(description='This tool connects to a ccTalk speaking coin acceptor over a serial Inteface.')
 argp.add_argument('--port',help='The serial port. Default is /dev/ttyUSB0 ', default="/dev/ttyUSB0")
 args = argp.parse_args()

 try:
  interface = cctalk.SerialInterface(args.port)
  ca = TestAcceptor(interface)
  interface.start()
 except serial.SerialException:
  print("Error while opening serial port {}".format(args.port))


if __name__ == '__main__':
 main()
