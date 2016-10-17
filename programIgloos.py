from optparse import OptionParser

from scripts import Teststand
import os
import subprocess as sp

def writeTCLFile(programFile):
    with open("program_igloo.tcl", "w") as file:
        file.write("# Microsemi Tcl Script\n")
        file.write("# flashpro\n")
        file.write("# Date: Tue Oct 11 09:37:47 2016\n")
        file.write("# Directory C:\Users\pastika\Desktop\n")
        file.write("# File C:\Users\pastika\Desktop\program_igloo.tcl\n")
        file.write("open_project -project {%s} -connect_programmers 1\n"%(os.path.abspath("HE_igloo/HE_igloo.pro").replace("\\","/")))
        file.write("set_programming_file -file {%s}\n"%os.path.abspath(programFile).replace("\\","/"))
        file.write("run_selected_actions\n")
        file.write("close_project\n")
        

if __name__ ==  "__main__":

    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", help="Grab programming file")
    parser.add_option("-s", "--slot", dest="slot",     help="Specify a single slot", default = -2)

    (options, args) = parser.parse_args()

    writeTCLFile(options.filename)
    
    ts = Teststand()
    
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
    
    for slot in slots:
        print ""
        print "Beginning progtamming slot: ", slot
        print ""

        ts.selectGpio(slot)
        data = ts.readInfo(slot)
        print "time: ", data["date_time"]
        print "temp: ", data["temperature"]

        print "Starting Flashpro batch programming mode"
        #sp.check_output("C:\\Microsemi\\Program_Debug_v11.7\\bin\\flashpro.exe script:C:\\Users\\pastika\\Desktop\\program_igloo.tcl console_mode:brief", shell=True)
        sp.check_output("C:\\Microsemi\\Program_Debug_v11.7\\bin\\flashpro.exe script:%s console_mode:brief"%os.path.abspath("program_igloo.tcl"), shell=True)
        
        data = ts.readInfo(slot)
        print "time: ", data["date_time"]
        print "temp: ", data["temperature"]
