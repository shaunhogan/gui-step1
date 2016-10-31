# Read CLock Counter, QIE Reset Counter and WTE Counter

# Bridge and Igloo Counters
# Clock Counter
#   address 0x12
#   size    4 bytes
# RES_QIE Counter
#   address 0x13
#   size    4 bytes
# WTE Counter
#   address 0x14
#   size    4 bytes

import client
import time

pi = "192.168.1.41"
bus = client.webBus(pi, 0)
ccm = 0x74
gpio = 0x70
igloo = 0x09

# Counter register addresses
counterDict = { "b_clock" : 0x12,
                "b_reset" : 0x13,
                "b_wte"   : 0x14,
                "i_clock" : 0x12,
                "i_reset" : 0x13,
                "i_wte"   : 0x14}
# Counter register size in bytes
size = 4

# RM 1, 2, 3, 4 i2c bus
rmBus   = [0x01, 0x10, 0x20, 0x02]
# Sipm Control 1, 2, 3, 4 i2c bus
sipmBus = [0x02, 0x20, 0x01, 0x04]
calBus = 0x10
# QIE Card i2c address
qieAddress = [0x19, 0x1a, 0x1b, 0x1c]

def getRmBus(rm):
    return rmBus[rm-1]

def getSipmBus(sipm):
    return sipmBus[sipm-1]

def getQieAddress(slot):
    return qieAddress[slot-1]

# Reverse Bytes
def reverseBytes(message):
    message_list = message.split()
    message_list.reverse()
    if message_list.pop() == '1':
        print "I2C ERROR"
    s = " "
    return s.join(message_list)

# Converts Message to Hex
def toHex(message,option=0):
    message_list = message.split()
    for byte in xrange(len(message_list)):
        message_list[byte] = hex(int(message_list[byte]))
        message_list[byte] = message_list[byte][2:]
        if len(message_list[byte]) == 1:
            message_list[byte] = '0' + message_list[byte]
    if option == 2:
        s = ":"
        return s.join(message_list)
    if option == 1:
        s = " "
        return s.join(message_list)
    s = ""
    return '0x' + s.join(message_list)

# Gets Value
def getValue(message):
    message = reverseBytes(message)
    hex_message = toHex(message)[2:]
    return int(hex_message,16)

#########################################################

# Read counter from QIE card given RM (1-4) and Slot (1-4)
# Reads from Bridge or Igloo
def readCounter(rm, slot, counter):
    # Card is i2c address, register is register address 
    card = getQieAddress(slot)
    register = counterDict[counter]
    # Read Bridge Counter
    if counter[0] == 'b':
        bus.write(ccm, [getRmBus(rm)])
        bus.write(card, [register])
        bus.read(card, size)
    # Read Igloo Counter
    else:
        bus.write(ccm, [getRmBus(rm)])
        bus.write(card, [0x11,0x03,0,0,0])
        bus.write(igloo, [register])
        bus.read(igloo, size)
    # Send the batch!
    m = bus.sendBatch()
    return m

def bridgeReset():
    bus.write(0x00, [0x06])
    m = bus.sendBatch()
    return m

# Original value: 41
def magicReset():
    bus.write(ccm,[0x08]) # PCA9538 is bit 3 on ngccm mux
    bus.read(gpio,1)
    batch_1 = bus.sendBatch()
    value = getValue(batch_1[-1])
    print batch_1
    print value
    value | 0x18
    #power on and reset
    #register 3 is control reg for i/o modes
    bus.write(gpio,[0x03,0x00]) # sets all GPIO pins to 'output' mode
    bus.write(gpio,[0x01,0x00])
    bus.write(gpio,[0x01,0x08])
    bus.write(gpio,[0x01,value]) # GPIO reset is 10
    bus.write(gpio,[0x01,0x08])
    batch = bus.sendBatch()
    print 'Batch : '+str(batch)

def reset(bit, on=False):
    bus.write(ccm,[0x08])
    bus.read(gpio,1)
    batch_1 = bus.sendBatch()
    value = getValue(batch_1[-1])
    bus.write(ccm,[0x08])
    if on == True:
        bus.write(gpio, [0x01, setBit(value, bit)])
    else:
        bus.write(gpio, [0x01, killBit(value, bit)])
    bus.read(gpio,1)
    batch_2 = bus.sendBatch()
    value_2 = getValue(batch_2[-1])
    #print batch_2
    #print value_2

def setBit(value, bit):
    value = value | bit
    return value

def killBit(value, bit):
    value = value & ~bit
    return value

def powerReset():
    bus.write(ccm,[0x08])
    bus.write(gpio,[0x08,0])
    bus.sendBatch()

# 8 0 (bit 10 is reset) the bit 08 is counter enable
# reset high
# reset low
# counter enable high
# wait a second
# counter enable low

def readCounters(rm, register_list):
    for c in register_list:
        for slot in [1,2,3,4]:
            # Read and print counter 
            m = readCounter(rm, slot, c)
            v = getValue(m[-1])
            print "{0} : {1}".format(c,v)

def count(rm, wait, register_list):
    # Reset High and Low
    reset(0x10, True)
    reset(0x10, False)

    # Read counters 
    readCounters(rm, register_list)

    # Counter enable high, wait, counter enable low
    reset(0x08, True)
    time.sleep(wait)
    reset(0x08, False)

    # Read counters 
    readCounters(rm, register_list)

#########################################################

if __name__ == "__main__":
    reg_list = ["b_reset", "i_reset", "b_wte", "i_wte"]
    count(2, 1, reg_list)


