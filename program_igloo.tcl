# Microsemi Tcl Script
# flashpro
# Date: Tue Oct 11 09:37:47 2016
# Directory C:\Users\pastika\Desktop
# File C:\Users\pastika\Desktop\program_igloo.tcl
open_project -project {C:/Users/pastika/Documents/ngCCM/gui-step1/HE_igloo/HE_igloo.pro} -connect_programmers 1
set_programming_file -file {C:/Users/pastika/Documents/ngCCM/gui-step1/HE_igloo/projectData/main_HE_RM_01_0B.stp}
run_selected_actions
close_project
