# Microsemi Tcl Script
# flashpro
# Date: Tue Oct 11 09:37:47 2016
# Directory C:\Users\hcaldaq\gui-step1
# File C:\Users\hcaldaq\gui-step1\program_igloo.tcl
open_project -project {C:/Users/hcaldaq/gui-step1/HB_igloo/HB_igloo.pro} -connect_programmers 1
set_programming_file -file {C:/Users/hcaldaq/gui-step1/HB_igloo/fixed_HB_RM_v1_03.stp}
remove_prg (name {84830})*
run_selected_actions
close_project
