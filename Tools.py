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

#########################################################
#   Methods (formatting, etc) used by makeGui class     #
#########################################################

    # reverseBytes(): input message and output message with bytes reversed
    def reverseBytes(self, message):
        message_list = message.split()
        message_list.reverse()
        s = " "
        return s.join(message_list)
    
    # toHex(): input message and output corresponding hex string with formatting
    def toHex(self, message, colon=0):
        message_list = message.split()
        for byte in xrange(len(message_list)):
            message_list[byte] = hex(int(message_list[byte]))
            message_list[byte] = message_list[byte][2:]
            if len(message_list[byte]) == 1:
                message_list[byte] = '0' + message_list[byte]
        if colon == 2:
            s = ":"
            return s.join(message_list)
        if colon == 1:
            s = " "
            return s.join(message_list)
        s = ""
        return '0x' + s.join(message_list)

    # getValue(): input message in decimal and output corresponding integer value in decimal
    def getValue(self, message):
        hex_message = self.toHex(message)[2:]
        return int(hex_message,16)

    # serialNum(): get 6 unique bytes from UniqueID
    def serialNum(self, message):
        message_list = message.split()
        message_list = message_list[1:-1]
        s = " "
        return s.join(message_list)

    # getMessageList(): input value and number of bytes; output message as list
    def getMessageList(self, value, num_bytes):
        total_length = 2 * num_bytes
        hex_message = hex(value)[2:]
        hex_message = hex_message.zfill(total_length)
        #message_length = len(hex_message)
        #zeros = "".join(list('0' for i in xrange(total_length - message_length)))
        #zeros = (total_length - message_length) * "0"
        #hex_message = zeros + hex_message
        print "In getMessageList(): hex value = 0x{0:x}".format(value)
        print "In getMessageList(): hex message = {0}".format(hex_message)
        mList = list(int(hex_message[a:a+2],16) for a in xrange(0,total_length,2))
        mList.reverse()
        return mList

#########################################################################
#   Methods for communication (read,write) with FPGAs (Bridge, Igloo)   #
#########################################################################

    # Function to read from Bridge FPGA
    def readBridge(self, registerAddress, num_bytes):
        self.myBus.write(0x00,[0x06])
        self.myBus.sendBatch()
        self.myBus.write(self.address,[registerAddress])
        self.myBus.read(self.address, num_bytes)
        message = self.myBus.sendBatch()[-1]
        if message[0] != '0':
            print "In readBridge(): Bridge I2C_ERROR"
        return self.reverseBytes(message[2:])

    # Function to write to Bridge FPGA
    def writeBridge(self, registerAddress,messageList):
        self.myBus.write(self.address, [registerAddress]+messageList)
        return self.myBus.sendBatch()

    # Function to read from Igloo FPGA (top or bottom)
    def readIgloo(self, igloo, registerAddress, num_bytes=1):
        i2cSelectValue = -1
        iglooSelectDictionary = {"top":0x03, "bottom":0x06}
        try:
            i2cSelectValue = iglooSelectDictionary[igloo]
        except KeyError:
            print "In readIgloo(): i2cSelectValue = {0} (should be 0x03 or 0x07, -1 is the default if not set)".format(i2cSelectValue)
            print "In readIgloo(): igloo = {0} which is not 'top' or 'bototm'".format(igloo)
            sys.exit(1)
        self.myBus.write(0x00,[0x06])
        self.myBus.write(self.slot,[0x11,i2cSelectValue,0,0,0])
        self.myBus.write(self.iglooAddress,[registerAddress])
        self.myBus.read(self.iglooAddress, num_bytes)
        message = self.myBus.sendBatch()[-1]
        if message[0] != '0':
            print 'In readIgloo(): Igloo I2C_ERROR'
        print "In readIgloo(): Reading {0} Igloo; message = {1}".format(igloo, message)
        return self.reverseBytes(message[2:])



