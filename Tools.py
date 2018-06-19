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

######################################################################
#   Methods (color theme, formatting, etc) used by makeGui class     #
######################################################################

    # setColorTheme(): set color theme
    def setColorTheme(self):
        print "color theme: {0}".format(self.color_theme)
        # sunrise
        if self.color_theme == "sunrise":
            self.fontc="black"
            self.topc="white"
            self.rightc="white"
            self.midc="white"
            self.backc="#DDDDDD"
            self.rightc="white"
            self.buttonsc=["#75BBFD","#C9643B","#EC2D01","#748B97","#48C072","#FF964F","#FFA62B","#FFBBBB","#99FF99"]
            self.dimbuttonsc=self.getDimColors(self.buttonsc, "#222222", -1)
            #self.dimbuttonsc=["#76D3DD","#DDD8AB","#D86050","#AABBDD","#DDC477","#DDAA44","#AA6633","#DD9999","#77DD77"]
            self.dimc="#DDDDDD"
            self.checkc="White"

        # dark
        elif self.color_theme == "dark":
            self.fontc='#DDDDDD'
            self.topc='#333333'
            self.rightc='#333333'
            self.midc='#333333'
            self.backc='#222222'
            self.buttonsc=["#000066","#113311","#551111","#445588","#885122","#AA0011","#665511","#880000","#115511"]
            self.dimbuttonsc=["#222288","#225522","#772222","#6677AA","#AA7344","#CC2233","#887722","#AA0000","#227722"]
            self.dimc="#555555"
            self.checkc="#222222"

        # nightfall
        elif self.color_theme == "nightfall":
            self.fontc='#DDDDDD'
            self.topc='#333333'
            self.rightc='#333333'
            self.midc='#333333'
            self.backc='#222222'
            self.buttonsc=["#5A7D9A","#658B38","#B00000","#445588","#0033CC","#402090","#B30059","#003399","#3F9B0B"]
            self.dimbuttonsc=self.getDimColors(self.buttonsc, "#222222", 1)
            #self.dimbuttonsc=["#7C9FBC","#87AD5A","#772222","#6677AA","#CCB344","#CC2233","#888822","#AA0000","#227722"]
            self.dimc="#555555"
            self.checkc="#222222"

        # bright is default
        else:
            self.fontc="black"
            self.topc="white"
            self.rightc="white"
            self.midc="white"
            self.backc="#DDDDDD"
            self.rightc="white"
            self.buttonsc=["CadetBlue1","lemon chiffon","salmon2","#CCDDFF","#FFE699","#FFCC66","orange","#ffbbbb","#99FF99"]
            self.dimbuttonsc=["#76D3DD","#DDD8AB","#D86050","#AABBDD","#DDC477","#DDAA44","#AA6633","#DD9999","#77DD77"]
            self.dimc="#DDDDDD"
            self.checkc="white"

    # getDimColors(): return slightly brighter or darker colors 
    # WARNING: Technically you should not add total hex color values... add/subtract per color RGB
    def getDimColors(self, colors, change, sign=1):
        change_str = change[1:]
        change_list = list(int(change_str[i:i+2],16) for i in xrange(0,len(change_str),2))
        dimColors = []
        for color in colors:
            rgb_str = color[1:]
            rgb_list = list(int(rgb_str[i:i+2],16) for i in xrange(0,len(rgb_str),2))
            rgb_values = list(rgb_list[i] + sign * change_list[i] for i in xrange(len(rgb_list)))
            # keep RGB values bounded by 0x00 and 0xff
            for i in xrange(len(rgb_values)):
                if rgb_values[i] < 0x00:
                    rgb_values[i] = 0x00
                if rgb_values[i] > 0xff:
                    rgb_values[i] = 0xff
            new_rgb_list = list("{0:02X}".format(v) for v in rgb_values)
            new_rgb_str = "#" + "".join(new_rgb_list)
            if sign > 0:
                print "In getDimColors(): Color addition {0} + {1} = {2}".format(color,change,new_rgb_str)
            else:
                print "In getDimColors(): Color subtraction {0} - {1} = {2}".format(color,change,new_rgb_str)
            dimColors.append(new_rgb_str)
        return dimColors
        
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
        #print "In getMessageList(): hex value = 0x{0:x}".format(value)
        #print "In getMessageList(): hex message = {0}".format(hex_message)
        mList = list(int(hex_message[a:a+2],16) for a in xrange(0,total_length,2))
        mList.reverse()
        return mList

#########################################################################
#   Methods for communication (read,write) with FPGAs (Bridge, Igloo)   #
#########################################################################

    # Function to setup multiplex steps for fanout and ngCCM emulator (but without sendbatch)
    def multiplex(self):

        if self.jslot in [18,19,20,21]:
            self.myBus.write(0x72, [0x01])
            self.myBus.write(0x74,[0x18])
        if self.jslot in [23,24,25,26]:
            self.myBus.write(0x72, [0x01])
        if self.jslot in [2,3,4,5]:
           self.myBus.write(0x72, [0x02])
           self.myBus.write(0x74, [0x0A])
        if self.jslot in [7,8,9,10]:
           self.myBus.write(0x72, [0x02])
           self.myBus.write(0x74, [0x28])

    # Function to read from Bridge FPGA
    def readBridge(self, registerAddress, num_bytes):
        self.myBus.write(0x00,[0x06])
        self.multiplex()
        #self.myBus.sendBatch()
        self.myBus.write(self.card_i2c_address,[registerAddress])
        self.myBus.read(self.card_i2c_address, num_bytes)
        message = self.myBus.sendBatch()[-1]
        if message[0] != '0':
            print "In readBridge(): Bridge I2C_ERROR"
        return self.reverseBytes(message[2:])

    # Function to write to Bridge FPGA
    def writeBridge(self, registerAddress,messageList):
        self.multiplex()
        self.myBus.write(self.card_i2c_address, [registerAddress]+messageList)
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
        self.multiplex()
        self.myBus.write(self.card_i2c_address,[0x11,i2cSelectValue,0,0,0])
        self.myBus.write(self.iglooAddress,[registerAddress])
        self.myBus.read(self.iglooAddress, num_bytes)
        message = self.myBus.sendBatch()[-1]
        if message[0] != '0':
            print 'In readIgloo(): Igloo I2C_ERROR'
        print "In readIgloo(): Reading {0} Igloo; message = {1}".format(igloo, message)
        return self.reverseBytes(message[2:])



