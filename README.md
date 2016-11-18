# gui-step1
## Master Branch
A small gui for the first step in the QIE testing process
Fermilab - Summer 2016
## Hack For 904 Branch
A small gui for reprogramming Igloo FPGAs for use at CERN B904 - Fall 2016

Here is information regarding reprogramming Igloo FPGAs using the ngCCM Emulator.

Programming repository: https://github.com/BaylorCMS/gui-step1

Branch: hackFor904

Using Windows Powershell:

Print unique ids and current firmware versions
python.exe .\scripts.py

Print help for programming Igloos
python.exe .\programIgloos.py -h

Program all 8 slots on one half of the backplane (1 or 2 full RMs) with Igloo FW 2.2
python.exe .\programIgloos.py -f .\HE_igloo\fixed_HE_RM_v2_02.stp

Program single slot (say RM 2 slot 3 = J20 in backplane)
python.exe .\programIgloos.py -f .\HE_igloo\fixed_HE_RM_v2_02.stp -s 20

Use simple graphical user interface (GUI)
python.exe .\Simple-Gui.py
