# Tools.py
#
# Define Tools class
# Tools contains methods used by makeGui class
# Tools class has full access to makeGui attributes
# Tools class should not have an __init__() function
# Tools class should not have any attributes
#
# Caleb Smith
# FNAL, Baylor Universtiy, Summer 2018.

from client import webBus
from operator import add
import sys

class Tools:

    # reverse bytes function: input message and output message with bytes reversed
    def reverseBytes(self, message):
        message_list = message.split()
        message_list.reverse()
        s = " "
        return s.join(message_list)
    
    # Function to read from Bridge FPGA
    def readBridge(self, regAddress, num_bytes):
        self.myBus.write(0x00,[0x06])
        self.myBus.sendBatch()
        self.myBus.write(self.address,[regAddress])
        self.myBus.read(self.address, num_bytes)
        message = self.myBus.sendBatch()[-1]
        if message[0] != '0':
            print "In readBridge(): Bridge I2C_ERROR"
        return self.reverseBytes(message[2:])

    # Function to read from Igloo FPGA (top or bottom)
    def readIgloo(self, registerAddress, num_bytes=1):
        i2cSelectValue = -1
        iglooSelectDictionary = {"top":0x03, "bottom":0x06}
        try:
            i2cSelectValue = iglooSelectDictionary[self.igloo]
        except KeyError:
            print "In readIgloo(): i2cSelectValue = {0} (should be 0x03 or 0x07, -1 is the default if not set)".format(i2cSelectValue)
            print "In readIgloo(): igloo = {0} which is not 'top' or 'bototm'".format(self.igloo)
            sys.exit(1)
        self.myBus.write(0x00,[0x06])
        self.myBus.write(self.slot,[0x11,i2cSelectValue,0,0,0])
        self.myBus.write(self.iglooAddress,[registerAddress])
        self.myBus.read(self.iglooAddress, num_bytes)
        message = self.myBus.sendBatch()[-1]
        if message[0] != '0':
            print 'In readIgloo(): Igloo I2C_ERROR'
        print "In readIgloo(): Reading {0} Igloo; message = {1}".format(self.igloo, message)
        return self.reverseBytes(message[2:])



