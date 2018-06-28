from optparse import OptionParser
from datetime import datetime
from scripts import Teststand
import os
import subprocess as sp
import json

def writeTCLFile(programFile):
    with open("program_igloo.tcl", "w") as file:
        file.write("# Microsemi Tcl Script\n")
        file.write("# flashpro\n")
        file.write("# Date: Tue Oct 11 09:37:47 2016\n")
        file.write("# Directory C:\Users\hcaldaq\gui-step1\n")
        file.write("# File C:\Users\hcaldaq\gui-step1\program_igloo.tcl\n")
        file.write("open_project -project {%s} -connect_programmers 1\n"%(os.path.abspath("HB_igloo/HB_igloo.pro").replace("\\","/")))
        file.write("set_programming_file -file {%s}\n"%os.path.abspath(programFile).replace("\\","/"))
        file.write("run_selected_actions\n")
        file.write("close_project\n")
        

if __name__ ==  "__main__":
    begin_time = datetime.now()
    print "Begin time is: {0}".format(begin_time)
    parser = OptionParser()
    parser.add_option("-f", "--file",               dest="filename",    help="Firmware programming file")
    parser.add_option("-i", "--ip",                 dest="ip",          help="ip address of Raspberry Pi")
    parser.add_option("-s", "--slot",               dest="slot",        default = -2,   help="Specify a single slot")
    parser.add_option("-b", "--no_fanout_board",    dest="no_fanout_board", action="store_true",  default=False, help="Do not use fanout board")
    parser.add_option("-t", "--stop",               dest="stop",            action="store_true",  default=False, help="Stop after checking active slots")
    parser.add_option("-c", "--calibration",        dest="calibration",     action="store_true",  default=False, help="Include calibration unit")

    (options, args) = parser.parse_args()

    writeTCLFile(options.filename)
    # use_fanout_board is True if you are using a fanout board
    use_fanout_board = not(options.no_fanout_board)
    if options.ip:
        ts = Teststand(use_fanout_board, calibration=options.calibration, ip=options.ip)
    else:
        ts = Teststand(use_fanout_board, calibration=options.calibration)

    if options.stop:
        exit()
    
    slots = []
    if options.slot >0:
        slot = int(options.slot)
        if slot in ts.active_slots:
            slots = [slot]
        else:
            print "Invalid Slot"
            exit()
    else:
        slots = ts.active_slots
    
    # program top and bottom igloos
    igloos = ["top","bot"]
    iglooData = []
    if ts.piStatus and ts.busStatus:
        for slot in slots:
            Igloos_Programmed=False
            data = ts.readInfo(slot)
            print "time: ", data["DateRun"]
            print "temp: ", data["temperature"]
            for igloo in igloos:
                print ""
                print "Initiated Programing of SpecifiedSlot: {0} {1} Igloo FPGA".format(slot,igloo)
                print ""

                ts.selectGpio(slot,igloo)

                print "Starting Flashpro batch programming mode"
                # Please include the correct Microsemi path here 
                #sp.check_output("C:\\Microsemi\\Program_Debug_v11.7\\bin\\flashpro.exe script:C:\\Users\\pastika\\Desktop\\program_igloo.tcl console_mode:brief", shell=True)
                try:
                    sp.check_output("C:\\Microsemi\\Program_Debug_v11.7\\bin\\flashpro.exe script:%s console_mode:brief"%os.path.abspath("program_igloo.tcl"), shell=True)
                    Igloos_Programmed=True
                    print "Success: Programing: {0} {1} Igloo FPGA".format(slot,igloo) 
                except:
                    print "Error: Failed Programing: {0} {1} Igloo FPGA".format(slot,igloo) 
                    Igloos_Programmed=False
                    break
                #raw_input("press enter to continue")

            data = ts.readInfo(slot)
            if Igloos_Programmed:
                data["Igloos_Programmed"]="Passed"
            else:
                data["Igloos_Programmed"]="Failed"

            print "time: ", data["DateRun"]
            print "temp: ", data["temperature"]
            iglooData.append(data)
            jsonFile = "temp_json/{0}_step3_raw.json".format(data["Unique_ID"])
            with open(jsonFile, 'w') as jf:
                json.dump(data, jf)
        
        for datum in iglooData:
            print "Top Igloo FW: {0} {1}".format(datum["IglooMajVerT"], datum["IglooMinVerT"])
            print "Bottom Igloo FW: {0} {1}".format(datum["IglooMajVerB"], datum["IglooMinVerB"])
        print ""
        print "Uploading results to database"
        print ""
        sp.check_output("bash uploadIgloo.sh", shell=True)
    
    else:
        print "Failed Raspberry Pi and/or Websocket status."
        print "    1. Did you turn on the Raspberry Pi?"
        print "    2. Did you start the server?"
        print "    3. Did you plug in the ethernet cable?"
        print "    4. Did you use the correct ip address?"
        print "    5. Did you have coffee today?"
    
    end_time = datetime.now()
    print "End time is: {0}".format(end_time)
    total_time = end_time-begin_time
    print "total run time is: {0}".format(total_time)



