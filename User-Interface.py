# User-Interface.py
#
# This is the main Graphical User Interface for communicating
# with the setup in the lab.
# Developed with the help of many people
# For Baylor University, Summer 2016.

from Tkinter import *
from datetime import datetime
from initialClass import initialTests
from cardInfoClass import cardInformation
from Tools import Tools
import temp
import json
import client
import subprocess

if (0):
    fontc="black"
    topc="white"
    rightc="white"
    midc="white"
    backc="#DDDDDD"
    rightc="white"
    buttonsc=["CadetBlue1","lemon chiffon","salmon2","#CCDDFF","#FFE699","#FFCC66","orange","#ffbbbb","#99FF99"]
    dimbuttonsc=["#76D3DD","#DDD8AB","#D86050","#AABBDD","#DDC477","#DDAA44","#AA6633","#DD9999","#77DD77"]
    dimc="#DDDDDD"
else:
    fontc='#DDDDDD'
    topc='#333333'
    rightc='#333333'
    midc='#333333'
    backc='#222222'
    buttonsc=["#000066","#666611","#551111","#445588","#AA9122","#AA0011","#666611","#880000","#115511"]
    dimbuttonsc=["#222288","#888822","#772222","#6677AA","#CCB344","#CC2233","#888822","#AA0000","#227722"]
    dimc="#555555"

class makeGui(Tools):
    def __init__(self, parent):
        # Create a webBus instance
        #self.myBus = client.webBus("192.168.1.41",0)
        self.myBus = client.webBus("pi7",0)

        # Create a permanent I2C address of QCard (slot 1)
        self.address = 0x19
        
        # Permanent I2C address of Igloo FPGA
        self.iglooAddress = 0x09
        
        # Specify "top" or "bottom" Igloo FPGA
        self.igloo = "top"

        # Create an instance of initialTests
        self.initialTest = initialTests()

        # Create an instance of cardInformation
        self.cardInfo = cardInformation()

        # Read info from left side?
        self.readFromList = True

        # Make an empty list that will eventually contain all of
        # the active card slots
        self.outSlotNumbers = []

        # Name the parent. This is mostly for bookkeeping purposes
        # and doesn't really get used too much.
        self.myParent = parent

        # Make a placeholder for the shortened unique ID
        self.uniqueIDPass = ""

        self.nameChoiceVar         =  StringVar()
        self.gpioChoiceVar         =  StringVar()
        self.infoCommentVar        =  StringVar()
        self.barcodeEntry          =  StringVar()
        self.uniqueIDEntry         =  StringVar()
        self.tempEntry             =  StringVar()
        self.firmwareVerEntry      =  StringVar()
        self.firmwareVerMinEntry   =  StringVar()
        self.firmwareVerOtherEntry =  StringVar()
        self.iglooToggleEntry      =  StringVar()
        self.iglooMajVerEntry      =  StringVar()
        self.iglooMinVerEntry      =  StringVar()
        self.overwriteVar          =  IntVar()

        # Place an all-encompassing frame in the parent window. All of the following
        # frames will be placed here (topMost_frame) and not in the parent window.
        self.topMost_frame = Frame(parent)
        self.topMost_frame.pack()
        self.topMost_frame.configure(bg=backc)
        #----- constants for controlling layout
        button_width = 6

        button_padx = "2m"
        button_pady = "1m"

        frame_padx = "3m"
        frame_pady = "2m"
        frame_ipadx = "3m"
        frame_ipady = "1m"
        #---------- end layout constants ------


        ##########################################
        ###                                    ###
        ###     BEGIN MAKING SUB-FRAMES        ###
        ###                                    ###
        ##########################################

        # Make and pack a sub-frame within topMost_frame that will contain
        # all of the controls for non-hardware related test information
        # (i.e. name of tester)
        self.info_frame = Frame(
            self.topMost_frame,
            borderwidth=5, relief=RIDGE,
            height=50,
            background=topc,
            )
        self.info_frame.pack(
            side=TOP,
            ipadx=frame_ipadx,
            ipady=frame_ipady,
            padx=frame_padx,
            pady=frame_pady
            )

        # Make a top half-frame
        self.topHalf_frame = Frame(self.topMost_frame)
        self.topHalf_frame.configure(bg=backc)
        self.topHalf_frame.pack(side=TOP)

        # Make a frame for containing an experiment diagram
        self.experiment_frame = Frame(
            self.topHalf_frame,
            borderwidth=5, relief=RIDGE,
            height=580, width=300,
            background=rightc
            )
        self.experiment_frame.pack_propagate=(False)
        self.experiment_frame.pack(
            side=RIGHT,
            ipadx=frame_ipadx,
            ipady=frame_ipady,
            padx=frame_padx,
            pady=frame_pady
            )

        # Make a label for the entire right frame
        self.experi_rightFrame = Frame(
            self.topHalf_frame,
            borderwidth=5, relief=RIDGE,
            height=580, width=300,
            background=midc
            )
        self.experi_rightFrame.pack_propagatte=(False)
        self.experi_rightFrame.pack(
            side=LEFT,
            ipadx=frame_ipadx,
            ipady=frame_ipady,
            padx=frame_padx,
            pady=frame_pady
            )

        ##########################################
        ###                                    ###
        ###     BEGIN MAKING WIDGETS           ###
        ###                                    ###
        ##########################################

        ######################################
        #####                            #####
        #####    Widgets in info frame   #####
        #####                            #####
        ######################################

        # Make and pack a text label for name selector
        self.info_Label = Label(self.info_frame, text="Testing Information/Parameters")
        self.info_Label.configure(
            padx=button_padx,
            pady=button_pady,
            background=topc,
            foreground=fontc
            )
        self.info_Label.pack(side=TOP)

        # Make a sub-sub-frame within the frame to hold another label and a dropdown box
        self.info_subTop_frame = Frame(self.info_frame,background=topc)
        self.info_subTop_frame.pack(
            side=TOP,
            ipadx=frame_ipadx,
            ipady=frame_ipady,
            padx=frame_padx,
            pady=frame_pady
            )

        # Make a sub-sub-frame within the frame to hold comment box
        self.info_subBot_frame = Frame(self.info_frame,background=topc)
        self.info_subBot_frame.pack(
            side=TOP,
            ipadx=frame_ipadx,
            ipady=frame_ipady,
            padx=frame_padx,
            pady=frame_pady
            )

        # Make a label for the name drop-down:
        self.info_nameLabel = Label(self.info_subTop_frame, text="Tester Name: ")
        self.info_nameLabel.configure(
            padx=button_padx,
            pady=button_pady,
            background=topc,
            foreground=fontc
            )
        self.info_nameLabel.pack(side=LEFT)

        # Make and pack a listbox to pick which QIE card to talk to:
        self.info_nameBox = OptionMenu(self.info_subTop_frame, self.nameChoiceVar,
                          "Shaun Hogan","Caleb Smith","Adryanna Smith","Jordan Potarf",
                          "John Lawrence","Andrew Baas","Mason Dorseth","Josh Hiltbrand")
        self.info_nameBox.pack(side=LEFT)
        self.info_nameBox.configure(bg=topc,fg=fontc,activebackground=dimc,activeforeground=fontc)
        self.info_nameBox["menu"].config(bg=topc,fg=fontc,activebackground=dimc,activeforeground=fontc)
        self.nameChoiceVar.set("Choose Name") # initializes the OptionMenu
        # Make a label for the name drop-down:
        self.info_commentLabel = Label(self.info_subBot_frame, text="User Testing Comments: ")
        self.info_commentLabel.configure(
            padx=button_padx,
            pady=button_pady,
            background=topc,
            foreground=fontc
            )
        self.info_commentLabel.pack(side=LEFT)

        # Make a entrybox for testing comments
        self.info_commentBox = Entry(
            self.info_subBot_frame,
            textvariable=self.infoCommentVar
            )
        self.info_commentBox.pack(side=LEFT)
        self.info_commentBox.configure(bg=topc,fg=fontc)

        ######################################
        #####                            #####
        #####  Experiment Setup Frames   #####
        #####                            #####
        ######################################

        self.testLabelList = ["Res_1","Res_2","Res_3","Res_4",
                          "Res_5","Res_6","Res_7","Res_8",
                      "Res_9","Res_10","Res_11", "Res_12",
                      "Res_13", "Res_14", "Res_15", "SuplCur", "Vis", "Program",
                      "Res_16"]

        # Make a label for the entire left frame
        self.experi_subFrame_lbl = Label(self.experiment_frame,text="QIE Card Setup & Parameters")
        self.experi_subFrame_lbl.configure(
            padx=button_padx,
            pady=button_pady,
            background=rightc,
            foreground=fontc
            )
        self.experi_subFrame_lbl.pack(side=TOP)

        # Make top 2_7 subframe
        self.experi_subTop2_7_frame = Frame(self.experiment_frame, bg=rightc)
        self.experi_subTop2_7_frame.pack(
            side=TOP,
            ipadx=frame_ipadx, padx=frame_padx,
            ipady=frame_ipady, pady=frame_pady,
            )

        # Make top 2_8 subframe
        self.experi_subTop2_8_frame = Frame(self.experiment_frame, bg=rightc)
        self.experi_subTop2_8_frame.pack(
            side=TOP,
            ipadx=frame_ipadx, padx=frame_padx,
            ipady=frame_ipady, pady=frame_pady,
            )

        # Make top 2_6 subframe
        self.experi_subTop2_6_frame = Frame(self.experiment_frame, bg=rightc)
        self.experi_subTop2_6_frame.pack(
            side=TOP,
            ipadx=frame_ipadx, padx=frame_padx,
            ipady=frame_ipady, pady=frame_pady,
            )

        # Make top 2 subframe
        self.experi_subTop2_frame = Frame(self.experiment_frame,background=rightc)
        self.experi_subTop2_frame.pack(
            side=TOP,
            ipadx=frame_ipadx,
            ipady=frame_ipady,
            padx=frame_padx,
            pady=frame_pady
            )

        # Make top 2_0 subframe
        self.experi_subTop2_0_frame = Frame(self.experiment_frame,background=rightc)
        self.experi_subTop2_0_frame.pack(
            side=TOP,
            ipadx=frame_ipadx,
            ipady=frame_ipady,
            padx=frame_padx,
            pady=frame_pady
            )

        # Make top 2_1 subframe
        self.experi_subTop2_1_frame = Frame(self.experiment_frame,background=rightc)
        self.experi_subTop2_1_frame.pack(
            side=TOP,
            ipadx=frame_ipadx,
            ipady=frame_ipady,
            padx=frame_padx,
            pady=frame_pady
            )

        # Make top 2_2 subframe
        self.experi_subTop2_2_frame = Frame(self.experiment_frame,background=rightc)
        self.experi_subTop2_2_frame.pack(
            side=TOP,
            ipadx=frame_ipadx,
            ipady=frame_ipady,
            padx=frame_padx,
            pady=frame_pady
            )

        # Make top 2_3 subframe
        self.experi_subTop2_3_frame = Frame(self.experiment_frame,background=rightc)
        self.experi_subTop2_3_frame.pack(
            side=TOP,
            ipadx=frame_ipadx,
            ipady=frame_ipady,
            padx=frame_padx,
            pady=frame_pady
            )

        # Make top 2_4 subframe
        self.experi_subTop2_4_frame = Frame(self.experiment_frame,background=rightc)
        self.experi_subTop2_4_frame.pack(
            side=TOP,
            ipadx=frame_ipadx,
            ipady=frame_ipady,
            padx=frame_padx,
            pady=frame_pady
            )

        # Make top 2_4_5 subframe
        self.experi_subTop2_4_5_frame = Frame(self.experiment_frame,background=rightc)
        self.experi_subTop2_4_5_frame.pack(
            side=TOP,
            ipadx=frame_ipadx,
            ipady=frame_ipady,
            padx=frame_padx,
            pady=frame_pady
            )

        # Make top 2_4_6 subframe
        self.experi_subTop_2_4_6_frame = Frame(self.experiment_frame, background=rightc)
        self.experi_subTop_2_4_6_frame.pack(
            side=TOP,
            ipadx=frame_ipadx,
            ipady=frame_ipady,
            padx=frame_padx,
            pady=frame_pady
            )


        # Make top 2_5 subframe
        self.experi_subTop2_5_frame = Frame(self.experiment_frame,background=rightc)
        self.experi_subTop2_5_frame.pack(
            side=TOP,
            ipadx=frame_ipadx,
            ipady=frame_ipady,
            padx=frame_padx,
            pady=frame_pady
            )

        ###################################
        ###                             ###
        ###   Subframes on right side   ###
        ###                             ###
        ###################################

        # Make a buffer frame
        self.experi_subTopBuffer_frame = Frame(self.experi_rightFrame,bg=midc)
        self.experi_subTopBuffer_frame.pack(
            side=TOP,
            ipady=frame_ipady,
            ipadx=frame_ipadx,
            padx=frame_padx,
            pady=frame_pady
            )

        # Make an "inspections and tests" label
        self.experi_inspections_label = Label(self.experi_subTopBuffer_frame,
                        text="Inspections and Tests",fg=fontc)
        self.experi_inspections_label.configure(bg=midc)
        self.experi_inspections_label.pack()

        # Make a subframe for the barcode box
        self.experi_barcode_frame = Frame(self.experi_rightFrame, bg=midc)
        self.experi_barcode_frame.pack(
            side=TOP,
            ipady=frame_ipady,
            ipadx=frame_ipadx,
            padx=frame_padx,
            pady=frame_pady
            )

        # Make a label for the Barcode entry
        self.experi_barcode_lbl = Label(self.experi_barcode_frame, text="Barcode: ")
        self.experi_barcode_lbl.configure(
            background=midc,
            padx=button_padx,
            pady=button_pady,
            foreground=fontc
            )
        self.experi_barcode_lbl.pack(side=LEFT)

        # Make an entry box for the barcode
        # Make a entrybox for testing comments
        self.experi_barcode_entry = Entry(
            self.experi_barcode_frame,
            textvariable=self.barcodeEntry
            )
        self.experi_barcode_entry.pack(side=RIGHT)
        self.experi_barcode_entry.configure(bg=midc,fg=fontc)

        # Make another buffer frame
        self.experi_subTopBuffer2_frame = Frame(self.experi_rightFrame,bg=midc)
        self.experi_subTopBuffer2_frame.pack(
            side=TOP,
            ipady=frame_ipady,
            ipadx=frame_ipadx,
            padx=frame_padx,
            pady=frame_pady
            )

        # Make top 3 subframe
        self.experi_subTop3_frame = Frame(self.experi_rightFrame,background=midc)
        self.experi_subTop3_frame.pack(
            side=TOP,
            ipadx=frame_ipadx,
            ipady=frame_ipady,
            padx=frame_padx,
            )

        # Make top 3 subframe for text
        self.experi_subTop3_fText = Frame(self.experi_rightFrame,background=midc)
        self.experi_subTop3_fText.pack(
            side=TOP,
            ipadx=frame_ipadx,
            ipady=frame_ipady,
            padx=frame_padx,
            )

        # Make top 4 subframe
        self.experi_subTop4_frame = Frame(self.experi_rightFrame,background=midc)
        self.experi_subTop4_frame.pack(
            side=TOP,
            ipadx=frame_ipadx,
            padx=frame_padx,
            )

        # Make top 4 subframe for text
        self.experi_subTop4_fText = Frame(self.experi_rightFrame,background=midc)
        self.experi_subTop4_fText.pack(
            side=TOP,
            ipadx=frame_ipadx,
            padx=frame_padx,
            )

        # Make top 5 subframe
        self.experi_subTop5_frame = Frame(self.experi_rightFrame,background=midc)
        self.experi_subTop5_frame.pack(
            side=TOP,
            ipadx=frame_ipadx,
            padx=frame_padx,
            )

        # Make top 5 subframe for text
        self.experi_subTop5_fText = Frame(self.experi_rightFrame,background=midc)
        self.experi_subTop5_fText.pack(
            side=TOP,
            ipadx=frame_ipadx,
            padx=frame_padx,
            )

        # Make top 6 subframe
        self.experi_subTop6_frame = Frame(self.experi_rightFrame,background=midc)
        self.experi_subTop6_frame.pack(
            side=TOP,
            ipadx=frame_ipadx,
            padx=frame_padx,
            )

        # Make top 6 subframe for text
        self.experi_subTop6_fText = Frame(self.experi_rightFrame,background=midc)
        self.experi_subTop6_fText.pack(
            side=TOP,
            ipadx=frame_ipadx,
            padx=frame_padx,
            )

        # Make top 7 subframe
        self.experi_subTop7_frame = Frame(self.experi_rightFrame,background=midc)
        self.experi_subTop7_frame.pack(
            side=TOP,
            ipadx=frame_ipadx,
            ipady=frame_ipady,
            pady=frame_pady,
            padx=frame_padx,
            )


        # Create variables for each manual check (16 placeholders for now)
        self.testPassList = [StringVar() for i in range(0,19)]
        self.testPassState = ("Pass","Fail")

        #################################
        ###               ###
        ###       Info for Card       ###
        ###               ###
        #################################

        # Make a label for the uniqueID entry
        self.experi_uniqueID_lbl = Label(self.experi_subTop2_frame, text="Unique ID: ")
        self.experi_uniqueID_lbl.configure(
            background=rightc,
            foreground=fontc,
            padx=button_padx,
            pady=button_pady,
            )
        self.experi_uniqueID_lbl.pack(side=LEFT)

        # Make an entry box for the UniqueID
        # Make a entrybox for testing comments
        self.experi_uniqueID_entry = Entry(
            self.experi_subTop2_frame,
            textvariable=self.uniqueIDEntry,
            state="readonly",
            readonlybackground=rightc,
            foreground=fontc
            )
        self.experi_uniqueID_entry.pack(side=RIGHT)

        # Make a label for the temperature entry
        self.experi_temperature_lbl = Label(self.experi_subTop2_0_frame, text="Temperature: ")
        self.experi_temperature_lbl.configure(
            background=rightc,
            foreground=fontc,
            padx=button_padx,
            pady=button_pady,
            )
        self.experi_temperature_lbl.pack(side=LEFT)

        # Make an entry box for the temperature
        # Make a entrybox for testing comments
        self.experi_temperature_entry = Entry(
            self.experi_subTop2_0_frame,
            textvariable=self.tempEntry,
            state="readonly",
            readonlybackground=rightc,
            foreground=fontc
            )
        self.experi_temperature_entry.configure(bg=rightc,fg=fontc)
        self.experi_temperature_entry.pack(side=RIGHT)

        # Make a label for the main firmware ver entry
        self.experi_firmwareVer_lbl = Label(self.experi_subTop2_1_frame, text="Bridge Ver (Major): ")
        self.experi_firmwareVer_lbl.configure(
            background=rightc,
            foreground=fontc,
            padx=button_padx,
            pady=button_pady,
            )
        self.experi_firmwareVer_lbl.pack(side=LEFT)

        # Make an entry box for the main firmware ver
        # Make a entrybox for testing comments
        self.experi_firmwareVer_entry = Entry(
            self.experi_subTop2_1_frame,
            textvariable=self.firmwareVerEntry,
            state="readonly",
            readonlybackground=rightc,
            foreground=fontc
            )
        self.experi_firmwareVer_entry.pack(side=RIGHT)

        # Make a label for the minor firmware ver entry
        self.experi_firmwareVerMin_lbl = Label(self.experi_subTop2_2_frame, text="Bridge Ver (Minor): ")
        self.experi_firmwareVerMin_lbl.configure(
            background=rightc,
            foreground=fontc,
            padx=button_padx,
            pady=button_pady,
            )
        self.experi_firmwareVerMin_lbl.pack(side=LEFT)

        # Make an entry box for the minor firmware
        # Make a entrybox for testing comments
        self.experi_firmwareVerMin_entry = Entry(
            self.experi_subTop2_2_frame,
            textvariable=self.firmwareVerMinEntry,
            state="readonly",
            readonlybackground=rightc,
            foreground=fontc
            )
        self.experi_firmwareVerMin_entry.pack(side=RIGHT)

        # Make a label for the other firmware entry
        self.experi_firmwareVerOther_lbl = Label(self.experi_subTop2_3_frame, text="Bridge Ver (Other): ")
        self.experi_firmwareVerOther_lbl.configure(
            background=rightc,
            foreground=fontc,
            padx=button_padx,
            pady=button_pady,
            )
        self.experi_firmwareVerOther_lbl.pack(side=LEFT)

        # Make an entry box for the other firmware
        # Make a entrybox for testing comments
        self.experi_firmwareVerOther_entry = Entry(
            self.experi_subTop2_3_frame,
            textvariable=self.firmwareVerOtherEntry,
            state="readonly",
            readonlybackground=rightc,
            foreground=fontc
            )
        self.experi_firmwareVerOther_entry.pack(side=RIGHT)

        # Make a label for the major igloo firmware entry
        self.experi_iglooMajVer_lbl = Label(self.experi_subTop2_4_frame, text="Igloo Ver (Major): ")
        self.experi_iglooMajVer_lbl.configure(
            background=rightc,
            foreground=fontc,
            padx=button_padx,
            pady=button_pady,
            )
        self.experi_iglooMajVer_lbl.pack(side=LEFT)

        # Make an entry box for the major firmware
        self.experi_iglooMajVer_entry = Entry(
            self.experi_subTop2_4_frame,
            textvariable=self.iglooMajVerEntry,
            state="readonly",
            readonlybackground=rightc,
            foreground=fontc
            )
        self.experi_iglooMajVer_entry.pack(side=RIGHT)


        # Make a label for the minor igloo firmware entry
        self.experi_iglooMinVer_lbl = Label(self.experi_subTop2_4_5_frame, text="Igloo Ver (Minor): ")
        self.experi_iglooMinVer_lbl.configure(
            background=rightc,
            foreground=fontc,
            padx=button_padx,
            pady=button_pady,
            )
        self.experi_iglooMinVer_lbl.pack(side=LEFT)

        # Make an entry box for the minor firmware
        self.experi_iglooMinVer_entry = Entry(
            self.experi_subTop2_4_5_frame,
            textvariable=self.iglooMinVerEntry,
            state="readonly",
            readonlybackground=rightc,
            foreground=fontc
            )
        self.experi_iglooMinVer_entry.pack(side=RIGHT)

        # Make a label for the igloo toggle check
        self.iglooToggle_label = Label(self.experi_subTop_2_4_6_frame, text="Igloo Toggle Test: ")
        self.iglooToggle_label.configure(bg=rightc,fg=fontc,padx=button_padx,pady=button_pady)
        self.iglooToggle_label.pack(side=LEFT)

        # Make an entry box for the minor firmware
        self.iglooToggle_entry = Entry(
            self.experi_subTop_2_4_6_frame,
            textvariable=self.iglooToggleEntry,
            state="readonly",
            readonlybackground=rightc,
            foreground=fontc
            )
        self.iglooToggle_entry.pack(side=RIGHT)


        # Make a button to read the unique ID & firmware LEFT SIDE
        self.experi_uniqueID_left_get = Button(self.experi_subTop2_5_frame, text ="Get Unique ID & Firmware Ver. from Left", command=self.getUniqueIDPress_left)
        self.experi_uniqueID_left_get.configure(bg=buttonsc[0],fg=fontc,activebackground=dimbuttonsc[0],activeforeground=fontc)
        self.experi_uniqueID_left_get.pack(side=TOP)

        # Make a button to read the unique ID & firmware RIGHT SIDE
        self.experi_uniqueID_right_get = Button(self.experi_subTop2_5_frame, text ="Get Unique ID & Firmware Ver. from Right", command=self.getUniqueIDPress_right)
        self.experi_uniqueID_right_get.configure(bg=buttonsc[1],fg=fontc,activebackground=dimbuttonsc[1],activeforeground=fontc)
        self.experi_uniqueID_right_get.pack(side=TOP)

        # Make a button to submit the unique ID & firmware
        self.experi_uniqueID_give = Button(self.experi_subTop2_5_frame, text ="Upload Unique ID & Firmware Ver.", command=self.infoSubmitButtonPress)
        self.experi_uniqueID_give.configure(bg=buttonsc[2],fg=fontc,activebackground=dimbuttonsc[2],activeforeground=fontc)
        self.experi_uniqueID_give.pack(side=TOP)

        # Make a line of hypens
        self.experi_hyphenLine = Label(self.experi_subTop2_6_frame, text="----------------------------------")
        self.experi_hyphenLine.configure(bg=rightc,fg=fontc,padx=button_padx,pady=button_pady)
        self.experi_hyphenLine.pack()

        # Make a label for the GPIO selection
        self.gpioSelect_label = Label(self.experi_subTop2_7_frame, text="Select GPIO Option: ")
        self.gpioSelect_label.configure(bg=rightc,fg=fontc,padx=button_padx,pady=button_pady)
        self.gpioSelect_label.pack(side=LEFT)

        # Make a option menu for GPIO selection
        self.gpioSelect_box = OptionMenu(self.experi_subTop2_7_frame, self.gpioChoiceVar,
                          "J2 and J21","J3 and J20","J4 and J19","J5 and J18",
                          "J7 and J26","J8 and J25","J9 and J24","J10 and J23")
        self.gpioSelect_box.configure(bg=rightc,fg=fontc,activebackground=dimc,activeforeground=fontc)
        self.gpioSelect_box.pack(side=LEFT)
        self.gpioSelect_box["menu"].config(bg=topc,fg=fontc,activebackground=dimc,activeforeground=fontc)
        self.gpioChoiceVar.set("J2 and J21")

        # Make a button to submit GPIO option
        self.gpioSelect_bttn = Button(self.experi_subTop2_8_frame, command=self.gpioBttnPress,
                          text="Submit GPIO Choice")
        self.gpioSelect_bttn.configure(bg=buttonsc[0],fg=fontc,activebackground=dimbuttonsc[0],activeforeground=fontc)
        self.gpioSelect_bttn.pack()

        ################################
        ###                          ###
        ###     Visual Tests         ###
        ###                          ###
        ################################

        self.testDescDict = {"Res_1" : "Bkpln to GND", "Res_2" : "1.2V to GND", "Res_3" : "1.5V to GND",
                     "Res_4" : "2.5V to GND", "Res_5" : "3.3V to GND", "Res_6" : "5.0V to GND",
                     "Res_7" : "1.2V to 1.5V", "Res_8" : "1.2V to 2.5V", "Res_9" : "1.2V to 3.3V",
                     "Res_10" : "1.2V to 5.0V", "Res_11" : "1.5V to 2.5V", "Res_12" : "1.5V to 5.0V",
                     "Res_13" : "2.5V to 3.3V", "Res_14" : "2.5V to 5.0V", "Res_15" : "3.3V to 5.0V",
                     "SuplCur" : "Supply Current", "Vis" : "Visual Inspec.", "Program" : "Programming OK", "Res_16" : "1.5V to 3.3V"}

#       self.testPassList = [StringVar() for i in range(0,19)]

#       self.testLabelList = ["Res_1","Res_2","Res_3","Res_4",
#                         "Res_5","Res_6","Res_7","Res_8",
#                     "Res_9","Res_10","Res_11", "Res_12",
#                     "Res_13", "Res_14", "Res_15", "SuplCur", "Vis", "Program",
#                     "Res_16"]

        self.testPassInfo = []

        for i in range(0,4):
            self.testPassInfo.append(OptionMenu(self.experi_subTop3_frame,self.testPassList[i],"Fail","Pass","N/A",command=self.infoValChange))
            self.testPassInfo[i].configure(width=15,bg=buttonsc[3],fg=fontc,activebackground=dimbuttonsc[3],activeforeground=fontc)
            self.testPassInfo[i]["menu"].config(bg=topc,fg=fontc,activebackground=dimc,activeforeground=fontc)
            self.testPassList[i].set("N/A")
            self.testPassInfo[i].pack(side=LEFT)

            self.testPassLabel=Label(self.experi_subTop3_fText, text=self.testDescDict[self.testLabelList[i]]+"\n",bg=midc,fg=fontc)
            self.testPassLabel.configure(width=20)
            self.testPassLabel.pack(side=LEFT)

        for i in range(4,9):
            self.testPassInfo.append(OptionMenu(self.experi_subTop4_frame,self.testPassList[i],"Fail","Pass","N/A",command=self.infoValChange))
            self.testPassInfo[i].configure(width=11, bg=buttonsc[3],fg=fontc,activebackground=dimbuttonsc[3],activeforeground=fontc)
            self.testPassInfo[i]["menu"].config(bg=topc,fg=fontc,activebackground=dimc,activeforeground=fontc)
            self.testPassList[i].set("N/A")
            self.testPassInfo[i].pack(side=LEFT)

            self.testPassLabel=Label(self.experi_subTop4_fText, text=self.testDescDict[self.testLabelList[i]]+"\n", bg=midc,fg=fontc)
            self.testPassLabel.configure(width=15)
            self.testPassLabel.pack(side=LEFT)

        for i in range(9,14):
            self.testPassInfo.append(OptionMenu(self.experi_subTop5_frame,self.testPassList[i],"Fail","Pass","N/A",command=self.infoValChange))
            self.testPassInfo[i].configure(width=11,bg=buttonsc[3],fg=fontc,activebackground=dimbuttonsc[3],activeforeground=fontc)
            self.testPassInfo[i]["menu"].config(bg=topc,fg=fontc,activebackground=dimc,activeforeground=fontc)
            self.testPassList[i].set("N/A")
            self.testPassInfo[i].pack(side=LEFT)

            self.testPassLabel=Label(self.experi_subTop5_fText, text=self.testDescDict[self.testLabelList[i]]+"\n", bg=midc,fg=fontc)
            self.testPassLabel.configure(width=15)
            self.testPassLabel.pack(side=LEFT)

        for i in range(14,19):
            self.testPassInfo.append(OptionMenu(self.experi_subTop6_frame,self.testPassList[i],"Fail","Pass","N/A",command=self.infoValChange))
            self.testPassInfo[i].configure(width=11,bg=buttonsc[3],fg=fontc,activebackground=dimbuttonsc[3],activeforeground=fontc)
            self.testPassInfo[i]["menu"].config(bg=topc,fg=fontc,activebackground=dimc,activeforeground=fontc)
            self.testPassList[i].set("N/A")
            self.testPassInfo[i].pack(side=LEFT)

            self.testPassLabel=Label(self.experi_subTop6_fText, text=self.testDescDict[self.testLabelList[i]]+"\n", bg=midc,fg=fontc)
            self.testPassLabel.configure(width=15)
            self.testPassLabel.pack(side=LEFT)

        # Make a checkbox to overwrite/not overwrite pre-existing data
        self.overwriteBox = Checkbutton(self.experi_subTop7_frame, text="Overwrite existing QIE Card data (if applicable)?", variable=self.overwriteVar)
        self.overwriteBox.configure(bg=buttonsc[1],fg=fontc,activebackground=dimbuttonsc[1],activeforeground=fontc)
        self.overwriteBox.pack(side=TOP,
                       padx = button_padx,
                       pady = button_pady,
                       ipady = button_pady*2,
                       ipadx = button_padx*2)

        # Make a button to submit tests and information
        self.passAllTestsBttn = Button(self.experi_subTop7_frame, text="Pass All Tests", command=self.throwPassAllBox)
        self.passAllTestsBttn.configure(bg=buttonsc[4], fg=fontc, width=40, activebackground=dimbuttonsc[4], activeforeground=fontc)
        self.passAllTestsBttn.pack(side=TOP)

        # Make a button to submit tests and information
        self.initSubmitBttn = Button(self.experi_subTop7_frame, text="Submit Inspections & Tests", command=self.initSubmitBttnPress)
        self.initSubmitBttn.configure(bg=buttonsc[5], fg=fontc, width=40, activebackground=dimbuttonsc[5], activeforeground=fontc)
        self.initSubmitBttn.pack(side=TOP)

        # Make a button to clear all results
        self.clearDataBttn = Button(self.experi_subTop7_frame, text="Clear Inspections, Tests, & Info", command=self.clearDataBttnPress)
        self.clearDataBttn.configure(bg=buttonsc[6], fg=fontc, width=40, activebackground=dimbuttonsc[6], activeforeground=fontc)
        self.clearDataBttn.pack(side=TOP)



    #################################
    ###                           ###
    ###  BEGIN MEMBER FUNCTIONS   ###
    ###                           ###
    #################################

    # This function is needed to make the json dumps print properly
    def jdefault(self,o):
        return o.__dict__

##########################################################################################

    # Dumps the results of the tests & inspections to a json file
    def initSubmitBttnPress(self):
        if (self.nameChoiceVar.get() == "Choose Name"):
            self.throwErrorBox()
            return None

        self.initialTest.User = self.nameChoiceVar.get()
        self.initialTest.TestComment = self.infoCommentVar.get()
        self.initialTest.Barcode     = self.barcodeEntry.get()
        self.initialTest.DateRun = str(datetime.now())

        if self.overwriteVar.get() == 1: self.initialTest.Overwrite = True
        if self.overwriteVar.get() == 0: self.initialTest.Overwrite = False

        for i in range(len(self.testPassList)):
            if self.testPassList[i].get() == "Pass":
                self.initialTest.testResults[self.testLabelList[i]] = True
            elif self.testPassList[i].get() == "Fail":
                self.initialTest.testResults[self.testLabelList[i]] = False
            else:
                self.initialTest.testResults[self.testLabelList[i]] = "na"

        self.initSubmitBttn.configure(state=DISABLED)

        fileString = self.barcodeEntry.get()+"_step1_raw.json"

        with open('/home/django/testing_database/uploader/temp_json/'+fileString,'w') as jsonFile:
#       with open(fileString,'w') as jsonFile:     # Uncomment this line for debugging
            json.dump(self.initialTest, jsonFile, default = self.jdefault)


        subprocess.call("/home/django/testing_database/uploader/step12.sh", shell=True)
        print "Preliminary step recorded. Thank you!"

##########################################################################################

    def throwErrorBox(self):
        self.top = Toplevel()
        self.top.title("Name Choice Error")
        self.top.config(height=50, width=360)
        self.top.pack_propagate(False)

        self.msg = Label(self.top, text="Please select a name before continuing.",fg=fontc)
        self.msg.pack()

        self.button = Button(self.top, text="Sorry...", command=self.top.destroy)
        self.button.configure(bg=buttonsc[7],fg=fontc,activebackground=dimbuttonsc[7],activeforeground=fontc)
        self.button.pack()

##########################################################################################

    def throwPassAllBox(self):
        self.passBox = Toplevel()
        self.passBox.title("Are you sure?")
        self.passBox.config(height=85, width=360)
        self.passBox.pack_propagate(False)

        self.passMsg = Label(self.passBox, text="Are you sure you want to pass all tests?")
        self.passMsg.pack()

        self.yesButton = Button(self.passBox, text="Yes", command=self.passAllSelected)
        self.yesButton.configure(bg=buttonsc[8],fg=fontc,activebackground=dimbuttonsc[8],activeforeground=fontc)
        self.yesButton.pack()

        self.noButton = Button(self.passBox, text="No", command=self.passBox.destroy)
        self.noButton.configure(bg=buttonsc[2],fg=fontc,activebackground=dimbuttonsc[2],activeforeground=fontc)
        self.noButton.pack()

    def passAllSelected(self):
        for i in range(len(self.testPassList)):
            self.testPassList[i].set("Pass")
        self.infoValChangeNonevent()
        self.passBox.destroy()

##########################################################################################

    # Dumps the card UID and firmware version to a json file
    def infoSubmitButtonPress(self):
        self.cardInfo.Barcode = self.barcodeEntry.get()
        self.cardInfo.Unique_ID = self.uniqueIDPass
        self.cardInfo.FirmwareMaj = self.firmwareVerEntry.get()
        self.cardInfo.FirmwareMin = self.firmwareVerMinEntry.get()
        self.cardInfo.FirmwareOth = self.firmwareVerOtherEntry.get()
        self.cardInfo.IglooMinVer = self.iglooMinVerEntry.get()
        self.cardInfo.IglooMajVer = self.iglooMajVerEntry.get()
        self.cardInfo.Igloo_FPGA_Control = self.iglooToggleEntry.get()
        self.cardInfo.User = self.nameChoiceVar.get()
        self.cardInfo.DateRun = str(datetime.now())

        fileString = self.barcodeEntry.get()+"_step2_raw.json"

        with open('/home/django/testing_database/uploader/temp_json/'+fileString,'w') as jsonFile:
            json.dump(self.cardInfo, jsonFile, default = self.jdefault)

        subprocess.call("/home/django/testing_database/uploader/step12.sh", shell=True)
        print "Secondary step recorded. Thank you!"

###########################################################################################

    def clearDataBttnPress(self):
        self.initSubmitBttn.configure(state=NORMAL)

        # Clear the data in the GUI displays:
        self.infoCommentVar.set("")
        self.barcodeEntry.set("")
        self.uniqueIDEntry.set("")
        self.tempEntry.set("")
        self.firmwareVerEntry.set("")
        self.firmwareVerMinEntry.set("")
        self.firmwareVerOtherEntry.set("")
        self.iglooMajVerEntry.set("")
        self.iglooMinVerEntry.set("")
        self.iglooToggleEntry.set("")
        self.overwriteVar.set(0)

        # On the gui, change all the tests to "N/A"
        for i in range(len(self.testPassList)):
            self.testPassList[i].set("N/A")

        # Now, clear the stored, behind-the-scenes entries
        self.initialTest.User = self.nameChoiceVar.get()
        self.initialTest.TestComment = self.infoCommentVar.get()
        self.initialTest.Barcode     = self.barcodeEntry.get()
        self.cardInfo.Barcode     = self.barcodeEntry.get()
        self.cardInfo.Unique_ID    = self.uniqueIDEntry.get()
        self.cardInfo.FirmwareMaj = self.firmwareVerEntry.get()
        self.cardInfo.FirmwareMin = self.firmwareVerMinEntry.get()
        self.cardInfo.FirmwareOth = self.firmwareVerOtherEntry.get()
        self.initialTest.DateRun     = str(datetime.now())
        self.cardInfo.User = self.nameChoiceVar.get()
        self.cardInfo.IglooMinVer = self.iglooMinVerEntry.get()
        self.cardInfo.IglooMajVer = self.iglooMajVerEntry.get()
        self.cardInfo.Igloo2_FPGA_Control = self.iglooToggleEntry.get()
        self.initialTest.Overwrite = False

        # Behind the scenes, change all the tests to "Fail"
        for i in range(len(self.testPassList)):
            if self.testPassList[i].get() == "Pass":
                self.initialTest.testResults[self.testLabelList[i-1]] = True
            else:
                self.initialTest.testResults[self.testLabelList[i-1]] = False

        # Change the buttons back to their red state
        self.infoValChangeNonevent()

###########################################################################################

    # A function that changes the menu colors depending on if a test passes
    # or fails. This function is for event cases (IE, changing a single menu value)
    def infoValChange(self,event):
        for i in range(len(self.testPassInfo)):
            if (self.testPassList[i].get() == "Fail"):
                self.testPassInfo[i].configure(bg=buttonsc[2],fg=fontc,activebackground=dimbuttonsc[2],activeforeground=fontc)
            elif (self.testPassList[i].get() == "Pass"):
                self.testPassInfo[i].configure(bg=buttonsc[8],fg=fontc,activebackground=dimbuttonsc[8],activeforeground=fontc)
            else:
                self.testPassInfo[i].configure(bg=buttonsc[3],fg=fontc,activebackground=dimbuttonsc[3],activeforeground=fontc)

    # Duplicate of above function, but for non-event cases (IE hitting the "Clear" button)
    def infoValChangeNonevent(self):
        for i in range(len(self.testPassInfo)):
                         if (self.testPassList[i].get() == "Fail"):
                                 self.testPassInfo[i].configure(bg=buttonsc[2],fg=fontc,activebackground=dimbuttonsc[2],activeforeground=fontc)
                         elif (self.testPassList[i].get() == "Pass"):
                                 self.testPassInfo[i].configure(bg=buttonsc[8],fg=fontc,activebackground=dimbuttonsc[8],activeforeground=fontc)
                         else:
                                 self.testPassInfo[i].configure(bg=buttonsc[3],fg=fontc,activebackground=dimbuttonsc[3],activeforeground=fontc)

#############################################################################

    # Opens the proper GPIO slot. Used for programming cards.
    def gpioBttnPress(self):
        jSlotDict = {"J2 and J18" : 0x29, "J3 and J19" : 0x89, "J4 and J20" : 0xA9,
                    "J5 and J21" : 0x49, "J7 and J23" : 0x2A, "J8 and J24" : 0x8A,
                    "J9 and J25" : 0xAA, "J10 and J26" : 0x4A}


        # Full Backplane Functionality
        newJSlotDict = {"J2 and J21" : [0x29,0x49], "J3 and J20" : [0x89,0xA9],
                        "J4 and J19" : [0xA9,0x89], "J5 and J18" : [0x49,0x29],
                        "J7 and J26" : [0x2A,0x4A], "J8 and J25" : [0x8A,0xAA],
                        "J9 and J24" : [0xAA,0x8A], "J10 and J23" : [0x4A,0x2A]}

        dictStringToInts = {"J2 and J21" : [2, 21], "J3 and J20" : [3, 20],
                        "J4 and J19" : [4, 19], "J5 and J18" : [5, 18],
                        "J7 and J26" : [7, 26], "J8 and J25" : [8, 25],
                        "J9 and J24" : [9, 24], "J10 and J23" : [10, 23]}

        gpioVals = newJSlotDict[self.gpioChoiceVar.get()]
        self.jslots = dictStringToInts[self.gpioChoiceVar.get()]
        print 'GPIO '+self.gpioChoiceVar.get()+' values = '+str(gpioVals)

        for gpioValsIndex in xrange(len(gpioVals)):
            gpioVal = gpioVals[gpioValsIndex]
            if gpioValsIndex == 0:
                self.myBus.write(0x72, [0x02])
            else:
                self.myBus.write(0x72, [0x01])
            batch = self.myBus.sendBatch()
            self.myBus.write(0x74, [0x08]) # PCA9538 is bit 3 on ngccm mux
            # myBus.write(0x70,[0x01,0x00]) # GPIO PwrEn is register 3
            #backplane power enable and backplane reset
            #register 3 is control reg for i/o modes
            self.myBus.write(0x70,[0x03,0x00]) # sets all GPIO pins to 'output' mode
            self.myBus.write(0x70,[0x01,0x08])
            self.myBus.write(0x70,[0x01,0x18]) # GPIO reset is 10
            self.myBus.write(0x70,[0x01,0x08])
    
            #jtag selectors finnagling for slot 26
            self.myBus.write(0x70,[0x01,gpioVal])
    
            # myBus.write(0x70,[0x03,0x08])
            self.myBus.read(0x70,1)
            batch = self.myBus.sendBatch()
            print "GPIO Batch = "+str(batch)
    
            if (batch[-1] == "1 0"):
                print "GPIO I2C_ERROR"
                self.gpioSelect_bttn.configure(bg=buttonsc[2],fg=fontc,activebackground=dimbuttonsc[2],activeforeground=fontc)
            elif (batch[-1] == "0 "+str(gpioVal)):
                print "GPIO " + str(newJSlotDict[self.gpioChoiceVar.get()]) + " Opened!"
                self.gpioSelect_bttn.configure(bg=buttonsc[8],fg=fontc,activebackground=dimbuttonsc[8],activeforeground=fontc)
    
            else:
                print "GPIO Error: unexpected message is {0}".format(message)

##################################################################################

    def getUniqueIDPress_left(self):
        self.readFromLeft = True
        self.getUniqueIDPress()

##################################################################################

    def getUniqueIDPress_right(self):
        self.readFromLeft = False
        self.getUniqueIDPress()

##################################################################################

    # Read UniqueID, Bridge and Igloo Firmware Versions
    def getUniqueIDPress(self):

        bridgeDict = { 18 : 0x19, 19 : 0x1A, 20: 0x1B, 21 : 0x1C,
                    23 : 0x19, 24 : 0x1A, 25: 0x1B, 26 : 0x1C,
                     2 : 0x19, 3 : 0x1A, 4 : 0x1B, 5 : 0x1C,
                     7 : 0x19, 8 : 0x1A, 9: 0x1B, 10: 0x1C }

        if self.readFromLeft:
            self.jslot = self.jslots[1]
            self.slot = bridgeDict[self.jslot]
            if self.jslot in [18,19,20,21]:
                self.myBus.write(0x72, [0x01])
                self.myBus.write(0x74,[0x18])
            if self.jslot in [23,24,25,26]:
                self.myBus.write(0x72, [0x01])
                self.myBus.write(0x74,[0x09])
        else:
            self.jslot = self.jslots[0]
            self.slot = bridgeDict[self.jslot]
            if self.jslot in [2,3,4,5]:
               self.myBus.write(0x72, [0x02])
               self.myBus.write(0x74, [0x0A])
            if self.jslot in [7,8,9,10]:
               self.myBus.write(0x72, [0x02])
               self.myBus.write(0x74, [0x28])

        self.myBus.sendBatch()

        print "Reading Unique ID and Firmware versions."
        print "JSlot = {0} ; I2C_Address = 0x{1:02x}".format(self.jslot, self.slot)

        # Getting unique ID
        # 0x05000000ea9c8b7000   <- From main gui
        self.myBus.write(0x00,[0x06])
        self.myBus.write(self.slot,[0x11,0x04,0,0,0])
        self.myBus.write(0x50,[0x00])
        self.myBus.read(0x50, 8)
        raw_bus = self.myBus.sendBatch()
        #print '\nRaw Unique ID = '+str(raw_bus[-1])
        if raw_bus[-1][0] != '0':
            print 'Unique ID i2c Error!'
        cooked_bus = self.reverseBytes(raw_bus[-1])
        #cooked_bus = self.serialNum(cooked_bus)
        self.uniqueIDEntry.set(self.toHex(cooked_bus))
        self.uniqueIDPass = self.uniqueIDEntry.get()
        self.uniqueIDEntry.set("0x"+self.uniqueIDPass[4:(len(self.uniqueIDPass)-4)])

        print "UniqueID: {0}".format(self.uniqueIDEntry.get())


######### TODO: Add UniqueID Checksum to verify correct unique id is read

        # Getting bridge firmware
        self.myBus.write(0x00,[0x06])
        self.myBus.write(self.slot,[0x04])
        self.myBus.read(self.slot, 4)
        raw_data = self.myBus.sendBatch()[-1]
        med_rare_data = raw_data[2:]
        cooked_data = self.reverseBytes(med_rare_data)
        data_well_done = self.toHex(cooked_data)    # my apologies for the cooking references
        data_well_done = data_well_done[2:]
        print 'Bridge FPGA Firmware Version = 0x'+str(data_well_done)
        self.firmwareVerEntry.set("0x"+data_well_done[0:2])    #these are the worst (best?) variable names ever
        self.firmwareVerMinEntry.set("0x"+data_well_done[2:4])
        self.firmwareVerOtherEntry.set("0x"+data_well_done[4:8])

        # Getting temperature
        self.tempEntry.set(str(round(temp.readManyTemps(self.myBus, self.slot, 10, "Temperature", "nohold"),4)))

        # Getting IGLOO firmware info
        majorIglooVer = self.readIgloo(0x00)
        minorIglooVer = self.readIgloo(0x01)
        # Write IGLOO firmware in hex
        majorIglooVer = self.toHex(majorIglooVer)
        minorIglooVer = self.toHex(minorIglooVer)
        # Display igloo FW info on gui
        self.iglooMajVerEntry.set(majorIglooVer)
        self.iglooMinVerEntry.set(minorIglooVer)
        print "{0} Igloo2 FPGA Major Firmware Version = {1}".format(self.igloo, majorIglooVer)
        print "{0} Igloo2 FPGA Minor Firmware Version = {1}".format(self.igloo, minorIglooVer)

        # Verify that the Igloo can be power toggled
        self.iglooToggleEntry.set(str(self.checkIglooToggle()))

#########################################
#   Functions to check igloo toggle     #
#########################################

    def checkIglooToggle(self):
        print '\n--- Begin Toggle Igloo2 Power Test'
        control_address = 0x22
        message = self.readBridge(control_address,4)
        # print 'Igloo Control = '+str(message)

        ones_address = 0x02
        all_ones = '255 255 255 255'

        retval = False

        self.myBus.write(0x00,[0x06])
        self.myBus.sendBatch()

        register = self.readIgloo(ones_address, 4)
        if register != all_ones:
            retval = False
        # print 'Igloo Ones = '+str(register)

        # Turn Igloo Off
        # print 'Igloo Control = '+str(self.toggleIgloo())
        self.toggleIgloo()
        register = self.detectIglooError(ones_address, 4)
        if register != '0':
            retval = True
        # print 'Igloo Ones = '+str(register)

        # Turn Igloo On
        # print 'Igloo Control = '+str(self.toggleIgloo())
        self.toggleIgloo()
        register = self.readIgloo(ones_address, 4)
        if register != all_ones:
            retval = False
        # print 'Igloo Ones = '+str(register)

        if retval:
            print 'Toggle Igloo Power Success!'
        else:
            print 'Toggle Igloo Power Fail!'
            print '\nPlease confirm that the power source is on.'
            print 'Please confirm that the card is in the selected slot (J18 or J23).'
        return retval

    def toggleIgloo(self):
        iglooControl = 0x22
        message = self.readBridge(iglooControl,4)
        value = self.getValue(message)
        value = value ^ 0x400 # toggle igloo power: Igloo2 VDD Enable
        messageList = self.getMessageList(value,4)
        self.writeBridge(iglooControl,messageList)
        return self.readBridge(iglooControl,4)

    def detectIglooError(self, registerAddress, num_bytes):
        self.myBus.write(0x00,[0x06])
        self.myBus.write(self.address,[0x11,0x03,0,0,0])
        self.myBus.write(0x09,[registerAddress])
        self.myBus.read(0x09, num_bytes)
        message = self.myBus.sendBatch()[-1]
        #  if message[0] != '0':
        #          print 'Igloo i2c error detected in detectIglooError'
        return message[0]

###########################################################################################

# Main
def main():
    root = Tk()
    myapp = makeGui(root)
    root.mainloop()

if __name__ == "__main__":
    main()

