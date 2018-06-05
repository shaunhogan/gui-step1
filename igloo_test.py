from client import webBus
from operator import add
import sys
#b = webBus("pi7",0)

# Read from Igloo
def readIgloo(b, slot, igloo, address, num_bytes=1):
    iglooAddress = 0x09
    i2cSelectValue = -1
    iglooSelectDictionary = {"top":0x03, "bottom":0x07}
    try:
        i2cSelectValue = iglooSelectDictionary[igloo]
    except KeyError:
        print "In readIgloo(): i2cSelectValue = {0} (should be 0x03 or 0x07, -1 is the default if not set)".format(i2cSelectValue)
        print "In readIgloo(): igloo = {0} which is not 'top' or 'bototm'".format(igloo)
        sys.exit(1)
    b.write(0x00,[0x06])
    b.write(slot,[0x11,i2cSelectValue,0,0,0])
    b.write(iglooAddress,[address])
    b.read(iglooAddress, num_bytes)
    message = b.sendBatch()[-1]
    if message[0] != '0':
        print 'In readIgloo(): Igloo I2C_ERROR'
    return message
