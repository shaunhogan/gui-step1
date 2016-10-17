from scripts import Teststand
import subprocess as sp

if __name__ ==  "__main__":
    ts = Teststand()

    if ts.piStatus and ts.busStatus:
        for slot in ts.active_slots:
            print ""
            print "Beginning progtamming slot: ", slot
            print ""
    
            ts.selectGpio(slot)
            data = ts.readInfo(slot)
            print "time: ", data["date_time"]
            print "temp: ", data["temperature"]
    
            print "Starting Flashpro batch programming mode"
            #sp.check_output("C:\\Microsemi\\Program_Debug_v11.7\\bin\\flashpro.exe script:C:\\Users\\pastika\\Desktop\\program_igloo.tcl console_mode:brief", shell=True)
            
            data = ts.readInfo(slot)
            print "time: ", data["date_time"]
            print "temp: ", data["temperature"]
    else:
        print "Failed Raspberry Pi and/or Websocket status."
        print "    1. Did you plug in the ethernet cable?"
        print "    2. Did you turn on the Raspberry Pi?"
        print "    3. Did you start the server?"
        print "    4. Did you have coffee today?
