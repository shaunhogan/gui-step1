from scripts import Teststand
import subprocess as sp

if __name__ ==  "__main__":
    ts = Teststand()

    for slot in ts.active_slots:
        print ""
        print "Beginning progtamming slot: ", slot
        print ""

        ts.selectGpio(slot)
        print ts.readInfo(slot)

        print "Starting Flashpro batch programming mode"
        sp.check_output("C:\\Microsemi\\Program_Debug_v11.7\\bin\\flashpro.exe script:C:\\Users\\pastika\\Desktop\\program_igloo.tcl console_mode:brief", shell=True)
        
        print ts.readInfo(slot)
