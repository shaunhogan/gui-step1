# User-Interface.py
#
# This is the main Graphical User Interface for communicating
# with the setup in the lab.
# Developed with the help of many people
# For Baylor University, Summer 2016.
#
# This is a comment to see if I got git to work properly
# round 2 electric boogaloo

from Tkinter import *
from datetime import datetime
from initialClass import initialTests
from cardInfoClass import cardInformation
import igloo_test as it
import temp
import json
import client
import subprocess

class makeGui:
	def __init__(self, parent):
		# Create a webBus instance
		self.myBus = client.webBus("pi7",0)

		# Create an instance of initialTests
		self.initialTest = initialTests()

		# Create an instance of cardInformation
		self.cardInfo = cardInformation()
		
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
		self.iglooMajVerEntry      =  StringVar()
		self.iglooMinVerEntry      =  StringVar()
	
		# Place an all-encompassing frame in the parent window. All of the following
		# frames will be placed here (topMost_frame) and not in the parent window.
		self.topMost_frame = Frame(parent)
		self.topMost_frame.pack()

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
		###	BEGIN MAKING SUB-FRAMES        ### 
		###		                       ###
		##########################################

		# Make and pack a sub-frame within topMost_frame that will contain
		# all of the controls for non-hardware related test information
		# (i.e. name of tester)
		self.info_frame = Frame(
			self.topMost_frame,
			borderwidth=5, relief=RIDGE,
			height=50,
			background="white",
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
		self.topHalf_frame.pack(side=TOP)

		# Make a frame for containing an experiment diagram
		self.experiment_frame = Frame(
			self.topHalf_frame,
			borderwidth=5, relief=RIDGE,
			height=580, width=300,
			background="white"
			)
		self.experiment_frame.pack_propagate=(False)
		self.experiment_frame.pack(
			side=LEFT,
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
			background="white"
			)
		self.experi_rightFrame.pack_propagatte=(False)
		self.experi_rightFrame.pack(
			side=RIGHT,
			ipadx=frame_ipadx,
			ipady=frame_ipady,
			padx=frame_padx,
			pady=frame_pady
			)

		##########################################
		###                                    ###
		###	BEGIN MAKING WIDGETS           ### 
		###		                       ###
		##########################################

		######################################
		#####				 #####
		#####    Widgets in info frame   #####
		#####				 #####
		######################################

		# Make and pack a text label for name selector
		self.info_Label = Label(self.info_frame, text="Testing Information/Parameters")
		self.info_Label.configure(
			padx=button_padx,
			pady=button_pady,
			background="white"
			)
		self.info_Label.pack(side=TOP)

		# Make a sub-sub-frame within the frame to hold another label and a dropdown box
		self.info_subTop_frame = Frame(self.info_frame,background="white")
		self.info_subTop_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
                        )

		# Make a sub-sub-frame within the frame to hold comment box
		self.info_subBot_frame = Frame(self.info_frame,background="white")
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
			background="white"
			)
		self.info_nameLabel.pack(side=LEFT)

		# Make and pack a listbox to pick which QIE card to talk to:
		self.info_nameBox = OptionMenu(self.info_subTop_frame, self.nameChoiceVar,
					      "Shaun Hogan","Caleb Smith","Adryanna Smith","Jordan Potarf",
					      "John Lawrence","Andrew Baas","Mason Dorseth","Josh Hiltbrand")
		self.info_nameBox.pack(side=LEFT)
		self.nameChoiceVar.set("Choose Name") # initializes the OptionMenu

		# Make a label for the name drop-down:
		self.info_commentLabel = Label(self.info_subBot_frame, text="User Testing Comments: ")
		self.info_commentLabel.configure(
			padx=button_padx,
			pady=button_pady,
			background="white"
			)
		self.info_commentLabel.pack(side=LEFT)

		# Make a entrybox for testing comments
		self.info_commentBox = Entry(
			self.info_subBot_frame,
			textvariable=self.infoCommentVar
			)
		self.info_commentBox.pack(side=LEFT)

		######################################
		#####                            #####
		#####  Experiment Setup Frames   #####
		#####				 #####
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
			background="white"
			)
		self.experi_subFrame_lbl.pack(side=TOP)

		# Make top 2 subframe
		self.experi_subTop2_frame = Frame(self.experiment_frame,background="white")
		self.experi_subTop2_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
			)

		# Make top 2_0 subframe
		self.experi_subTop2_0_frame = Frame(self.experiment_frame,background="white")
		self.experi_subTop2_0_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
			)

		# Make top 2_1 subframe
		self.experi_subTop2_1_frame = Frame(self.experiment_frame,background="white")
		self.experi_subTop2_1_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
			)

		# Make top 2_2 subframe
		self.experi_subTop2_2_frame = Frame(self.experiment_frame,background="white")
		self.experi_subTop2_2_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
			)

		# Make top 2_3 subframe
		self.experi_subTop2_3_frame = Frame(self.experiment_frame,background="white")
		self.experi_subTop2_3_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
			)

		# Make top 2_4 subframe
		self.experi_subTop2_4_frame = Frame(self.experiment_frame,background="white")
		self.experi_subTop2_4_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
			)


		# Make top 2_4_5 subframe
		self.experi_subTop2_4_5_frame = Frame(self.experiment_frame,background="white")
		self.experi_subTop2_4_5_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
			)

		# Make top 2_5 subframe
		self.experi_subTop2_5_frame = Frame(self.experiment_frame,background="white")
		self.experi_subTop2_5_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
			)

		# Make top 2_6 subframe
		self.experi_subTop2_6_frame = Frame(self.experiment_frame, bg="white")
		self.experi_subTop2_6_frame.pack(
			side=TOP,
			ipadx=frame_ipadx, padx=frame_padx,
			ipady=frame_ipady, pady=frame_pady,
			)

		# Make top 2_7 subframe
		self.experi_subTop2_7_frame = Frame(self.experiment_frame, bg="white")
		self.experi_subTop2_7_frame.pack(
			side=TOP,
			ipadx=frame_ipadx, padx=frame_padx,
			ipady=frame_ipady, pady=frame_pady,
			)
		
		# Make top 2_8 subframe
		self.experi_subTop2_8_frame = Frame(self.experiment_frame, bg="white")
		self.experi_subTop2_8_frame.pack(
			side=TOP,
			ipadx=frame_ipadx, padx=frame_padx,
			ipady=frame_ipady, pady=frame_pady,
			)

		###################################
		### 				###
		###   Subframes on right side   ###
		###				###
		###################################

		# Make a buffer frame
		self.experi_subTopBuffer_frame = Frame(self.experi_rightFrame,bg="white")
		self.experi_subTopBuffer_frame.pack(
			side=TOP,
			ipady=frame_ipady,
			ipadx=frame_ipadx,
			padx=frame_padx,
			pady=frame_pady
			)

		# Make an "inspections and tests" label
		self.experi_inspections_label = Label(self.experi_subTopBuffer_frame,
						text="Inspections and Tests")
		self.experi_inspections_label.configure(bg="white")
		self.experi_inspections_label.pack()

		# Make a subframe for the barcode box
		self.experi_barcode_frame = Frame(self.experi_rightFrame, bg="white")
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
			background="white",
			padx=button_padx,
			pady=button_pady,
			)
		self.experi_barcode_lbl.pack(side=LEFT)
		
		# Make an entry box for the barcode
		# Make a entrybox for testing comments
		self.experi_barcode_entry = Entry(
			self.experi_barcode_frame,
			textvariable=self.barcodeEntry
			)
		self.experi_barcode_entry.pack(side=RIGHT)

		# Make another buffer frame
		self.experi_subTopBuffer2_frame = Frame(self.experi_rightFrame,bg="white")
		self.experi_subTopBuffer2_frame.pack(
			side=TOP,
			ipady=frame_ipady,
			ipadx=frame_ipadx,
			padx=frame_padx,
			pady=frame_pady
			)

		# Make top 3 subframe
		self.experi_subTop3_frame = Frame(self.experi_rightFrame,background="white")
		self.experi_subTop3_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        padx=frame_padx,
			)

		# Make top 3 subframe for text
		self.experi_subTop3_fText = Frame(self.experi_rightFrame,background="white")
		self.experi_subTop3_fText.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        padx=frame_padx,
			)

		# Make top 4 subframe
		self.experi_subTop4_frame = Frame(self.experi_rightFrame,background="white")
		self.experi_subTop4_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        padx=frame_padx,
			)

		# Make top 4 subframe for text
		self.experi_subTop4_fText = Frame(self.experi_rightFrame,background="white")
		self.experi_subTop4_fText.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        padx=frame_padx,
			)

		# Make top 5 subframe
		self.experi_subTop5_frame = Frame(self.experi_rightFrame,background="white")
		self.experi_subTop5_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        padx=frame_padx,
			)

		# Make top 5 subframe for text
		self.experi_subTop5_fText = Frame(self.experi_rightFrame,background="white")
		self.experi_subTop5_fText.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        padx=frame_padx,
			)

		# Make top 6 subframe
		self.experi_subTop6_frame = Frame(self.experi_rightFrame,background="white")
		self.experi_subTop6_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        padx=frame_padx,
			)

		# Make top 6 subframe for text
		self.experi_subTop6_fText = Frame(self.experi_rightFrame,background="white")
		self.experi_subTop6_fText.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        padx=frame_padx,
			)

		# Make top 7 subframe
		self.experi_subTop7_frame = Frame(self.experi_rightFrame,background="white")
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
		###			      ###
		###       Info for Card       ###
		###			      ###
		#################################

		# Make a label for the uniqueID entry
		self.experi_uniqueID_lbl = Label(self.experi_subTop2_frame, text="Unique ID: ")
		self.experi_uniqueID_lbl.configure(
			background="white",
			padx=button_padx,
			pady=button_pady,
			)
		self.experi_uniqueID_lbl.pack(side=LEFT)
		
		# Make an entry box for the UniqueID
		# Make a entrybox for testing comments
		self.experi_uniqueID_entry = Entry(
			self.experi_subTop2_frame,
			textvariable=self.uniqueIDEntry,
			state="readonly"
			)
		self.experi_uniqueID_entry.pack(side=RIGHT)

		# Make a label for the temperature entry
		self.experi_temperature_lbl = Label(self.experi_subTop2_0_frame, text="Temperature: ")
		self.experi_temperature_lbl.configure(
			background="white",
			padx=button_padx,
			pady=button_pady,
			)
		self.experi_temperature_lbl.pack(side=LEFT)
		
		# Make an entry box for the temperature
		# Make a entrybox for testing comments
		self.experi_temperature_entry = Entry(
			self.experi_subTop2_0_frame,
			textvariable=self.tempEntry,
			state="readonly"
			)
		self.experi_temperature_entry.pack(side=RIGHT)

		# Make a label for the main firmware ver entry
		self.experi_firmwareVer_lbl = Label(self.experi_subTop2_1_frame, text="Bridge Ver (Major): ")
		self.experi_firmwareVer_lbl.configure(
			background="white",
			padx=button_padx,
			pady=button_pady,
			)
		self.experi_firmwareVer_lbl.pack(side=LEFT)
		
		# Make an entry box for the main firmware ver
		# Make a entrybox for testing comments
		self.experi_firmwareVer_entry = Entry(
			self.experi_subTop2_1_frame,
			textvariable=self.firmwareVerEntry,
			state="readonly"
			)
		self.experi_firmwareVer_entry.pack(side=RIGHT)

		# Make a label for the minor firmware ver entry
		self.experi_firmwareVerMin_lbl = Label(self.experi_subTop2_2_frame, text="Bridge Ver (Minor): ")
		self.experi_firmwareVerMin_lbl.configure(
			background="white",
			padx=button_padx,
			pady=button_pady,
			)
		self.experi_firmwareVerMin_lbl.pack(side=LEFT)
		
		# Make an entry box for the minor firmware
		# Make a entrybox for testing comments
		self.experi_firmwareVerMin_entry = Entry(
			self.experi_subTop2_2_frame,
			textvariable=self.firmwareVerMinEntry,
			state="readonly"
			)
		self.experi_firmwareVerMin_entry.pack(side=RIGHT)

		# Make a label for the other firmware entry
		self.experi_firmwareVerOther_lbl = Label(self.experi_subTop2_3_frame, text="Bridge Ver (Other): ")
		self.experi_firmwareVerOther_lbl.configure(
			background="white",
			padx=button_padx,
			pady=button_pady,
			)
		self.experi_firmwareVerOther_lbl.pack(side=LEFT)
		
		# Make an entry box for the other firmware
		# Make a entrybox for testing comments
		self.experi_firmwareVerOther_entry = Entry(
			self.experi_subTop2_3_frame,
			textvariable=self.firmwareVerOtherEntry,
			state="readonly"
			)
		self.experi_firmwareVerOther_entry.pack(side=RIGHT)

###################################################################################

		# Make a label for the major igloo firmware entry
		self.experi_iglooMajVer_lbl = Label(self.experi_subTop2_4_frame, text="Igloo Ver (Major): ")
		self.experi_iglooMajVer_lbl.configure(
			background="white",
			padx=button_padx,
			pady=button_pady,
			)
		self.experi_iglooMajVer_lbl.pack(side=LEFT)
		
		# Make an entry box for the major firmware
		self.experi_iglooMajVer_entry = Entry(
			self.experi_subTop2_4_frame,
			textvariable=self.iglooMajVerEntry,
			state="readonly"
			)
		self.experi_iglooMajVer_entry.pack(side=RIGHT)


		# Make a label for the minor igloo firmware entry
		self.experi_iglooMinVer_lbl = Label(self.experi_subTop2_4_5_frame, text="Igloo Ver (Minor): ")
		self.experi_iglooMinVer_lbl.configure(
			background="white",
			padx=button_padx,
			pady=button_pady,
			)
		self.experi_iglooMinVer_lbl.pack(side=LEFT)
		
		# Make an entry box for the minor firmware
		self.experi_iglooMinVer_entry = Entry(
			self.experi_subTop2_4_5_frame,
			textvariable=self.iglooMinVerEntry,
			state="readonly"
			)
		self.experi_iglooMinVer_entry.pack(side=RIGHT)

####################################################################################

		# Make a button to read the unique ID & firmware
		self.experi_uniqueID_get = Button(self.experi_subTop2_5_frame, text ="Get Unique ID & Firmware Ver.", command=self.getUniqueIDPress)
		self.experi_uniqueID_get.configure(bg="salmon")
		self.experi_uniqueID_get.pack(side=TOP)

		# Make a button to submit the unique ID & firmware
		self.experi_uniqueID_give = Button(self.experi_subTop2_5_frame, text ="Upload Unique ID & Firmware Ver.", command=self.infoSubmitButtonPress)
		self.experi_uniqueID_give.configure(bg="salmon2")
		self.experi_uniqueID_give.pack(side=TOP)
		
		# Make a line of hypens
		self.experi_hyphenLine = Label(self.experi_subTop2_6_frame, text="----------------------------------")
		self.experi_hyphenLine.configure(bg="white",padx=button_padx,pady=button_pady)
		self.experi_hyphenLine.pack()

		# Make a label for the GPIO selection
		self.gpioSelect_label = Label(self.experi_subTop2_7_frame, text="Select GPIO Option: ")
		self.gpioSelect_label.configure(bg="white",padx=button_padx,pady=button_pady)
		self.gpioSelect_label.pack(side=LEFT)

		# Make a option menu for GPIO selection
		self.gpioSelect_box = OptionMenu(self.experi_subTop2_7_frame, self.gpioChoiceVar,
					      "J2 and J18","J3 and J19","J4 and J20","J5 and J21",
					      "J7 and J23","J8 and J24","J9 and J25","J10 and J26")
		self.gpioSelect_box.pack(side=LEFT)
		self.gpioChoiceVar.set("J2 and J18")

		# Make a button to submit GPIO option
		self.gpioSelect_bttn = Button(self.experi_subTop2_8_frame, command=self.gpioBttnPress,
					      text="Submit GPIO Choice")
		self.gpioSelect_bttn.configure(bg="CadetBlue1")
		self.gpioSelect_bttn.pack()

		################################
		###			     ###
		###     Visual Tests 	     ###
		###			     ###
		################################

		self.testDescDict = {"Res_1" : "Bkpln to GND", "Res_2" : "1.2V to GND", "Res_3" : "1.5V to GND",
				     "Res_4" : "2.5V to GND", "Res_5" : "3.3V to GND", "Res_6" : "5.0V to GND",
				     "Res_7" : "1.2V to 1.5V", "Res_8" : "1.2V to 2.5V", "Res_9" : "1.2V to 3.3V",
				     "Res_10" : "1.2V to 5.0V", "Res_11" : "1.5V to 2.5V", "Res_12" : "1.5V to 5.0V",
				     "Res_13" : "2.5V to 3.3V", "Res_14" : "2.5V to 5.0V", "Res_15" : "3.3V to 5.0V",
				     "SuplCur" : "Supply Current", "Vis" : "Visual Inspec.", "Program" : "Programming OK", "Res_16" : "1.5V to 3.3V"}

#		self.testPassList = [StringVar() for i in range(0,19)]

#		self.testLabelList = ["Res_1","Res_2","Res_3","Res_4",
#		      		      "Res_5","Res_6","Res_7","Res_8",
#				      "Res_9","Res_10","Res_11", "Res_12",
#				      "Res_13", "Res_14", "Res_15", "SuplCur", "Vis", "Program",
#				      "Res_16"]
		
		self.testPassInfo = []
		
		for i in range(0,4):
			self.testPassInfo.append(OptionMenu(self.experi_subTop3_frame,self.testPassList[i],"Fail","Pass","N/A",command=self.infoValChange))
			self.testPassInfo[i].configure(width=15,bg="#ff3333")
			self.testPassList[i].set("Fail")
			self.testPassInfo[i].pack(side=LEFT)

			self.testPassLabel=Label(self.experi_subTop3_fText, text=self.testDescDict[self.testLabelList[i]]+"\n",bg="white")
			self.testPassLabel.configure(width=20)
			self.testPassLabel.pack(side=LEFT)
		
		for i in range(4,9):
			self.testPassInfo.append(OptionMenu(self.experi_subTop4_frame,self.testPassList[i],"Fail","Pass","N/A",command=self.infoValChange))
			self.testPassInfo[i].configure(width=11, bg="#ff3333")
			self.testPassList[i].set("Fail")
			self.testPassInfo[i].pack(side=LEFT)

			self.testPassLabel=Label(self.experi_subTop4_fText, text=self.testDescDict[self.testLabelList[i]]+"\n", bg="white")
			self.testPassLabel.configure(width=15)
			self.testPassLabel.pack(side=LEFT)

		for i in range(9,14):
			self.testPassInfo.append(OptionMenu(self.experi_subTop5_frame,self.testPassList[i],"Fail","Pass","N/A",command=self.infoValChange))
			self.testPassInfo[i].configure(width=11,bg="#ff3333")
			self.testPassList[i].set("Fail")
			self.testPassInfo[i].pack(side=LEFT)

			self.testPassLabel=Label(self.experi_subTop5_fText, text=self.testDescDict[self.testLabelList[i]]+"\n", bg="white")
			self.testPassLabel.configure(width=15)
			self.testPassLabel.pack(side=LEFT)

		for i in range(14,19):
			self.testPassInfo.append(OptionMenu(self.experi_subTop6_frame,self.testPassList[i],"Fail","Pass","N/A",command=self.infoValChange))
			self.testPassInfo[i].configure(width=11,bg="#ff3333")
			self.testPassList[i].set("Fail")
			self.testPassInfo[i].pack(side=LEFT)

			self.testPassLabel=Label(self.experi_subTop6_fText, text=self.testDescDict[self.testLabelList[i]]+"\n", bg="white")
			self.testPassLabel.configure(width=15)
			self.testPassLabel.pack(side=LEFT)

		# Make a button to submit tests and information
		self.initSubmitBttn = Button(self.experi_subTop7_frame, text="Submit Inspections & Tests", command=self.initSubmitBttnPress)
		self.initSubmitBttn.configure(bg="lemon chiffon", width=40)
		self.initSubmitBttn.pack(side=TOP)

		# Make a button to clear all results
		self.clearDataBttn = Button(self.experi_subTop7_frame, text="Clear Inspections, Tests, & Info", command=self.clearDataBttnPress)
		self.clearDataBttn.configure(bg="orange", width=40)
		self.clearDataBttn.pack(side=TOP)



	#################################
	###			      ###
	###  BEGIN MEMBER FUNCTIONS   ###
	###			      ###
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

		for i in range(len(self.testPassList)):
			if self.testPassList[i].get() == "Pass":
				self.initialTest.testResults[self.testLabelList[i]] = True
			elif self.testPassList[i].get() == "Fail":
				self.initialTest.testResults[self.testLabelList[i]] = False
			else:
				self.initialTest.testResults[self.testLabelList[i]] = "na"
		
		fileString = self.barcodeEntry.get()+"_step1_raw.json"		
	
		with open('/home/django/testing_database/uploader/temp_json/'+fileString,'w') as jsonFile:
#		with open(fileString,'w') as jsonFile:     # Uncomment this line for debugging
			json.dump(self.initialTest, jsonFile, default = self.jdefault)	

		
		subprocess.call("/home/django/testing_database/uploader/upload.sh", shell=True)
		print "Preliminary step recorded. Thank you!"
##########################################################################################

	def throwErrorBox(self):
		self.top = Toplevel()
		self.top.title("Name Choice Error")
		self.top.config(height=50, width=360)
		self.top.pack_propagate(False)

		self.msg = Label(self.top, text="Please select a name before continuing.")
		self.msg.pack()

		self.button = Button(self.top, text="Sorry...", command=self.top.destroy)
		self.button.pack()	

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

		fileString = self.barcodeEntry.get()+"_step2_raw.json"

		with open('/home/django/testing_database/uploader/temp_json/'+fileString,'w') as jsonFile:
			json.dump(self.cardInfo, jsonFile, default = self.jdefault)

		subprocess.call("/home/django/testing_database/uploader/upload.sh", shell=True)
		print "Secondary step recorded. Thank you!"

###########################################################################################

	def clearDataBttnPress(self):
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

		# On the gui, change all the tests to "Fail"
		for i in range(len(self.testPassList)):
			self.testPassList[i].set("Fail")

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
		self.cardInfo.IglooMinVer = self.iglooMinVerEntry.get()
		self.cardInfo.IglooMajVer = self.iglooMajVerEntry.get()

		# Behind the scenes, change all the tests to "Fail"
		for i in range(len(self.testPassList)):
			if self.testPassList[i].get() == "Pass":
				self.initialTest.testResults[self.testLabelList[i-1]] = True
			else:
				self.initialTest.testResults[self.testLabelList[i-1]] = False

		# Change the buttons back to their red state
		self.infoValChangeNonevent()
	
###########################################################################################

	def reverseBytes(self, message):
		message_list = message.split()
		message_list.reverse()
		s = " "
		return s.join(message_list)

	def serialNum(self, message):
		message_list = message.split()
		message_list = message_list[1:-1]
		s = " "
		return s.join(message_list)

	# Converts decimal messages to Hex messages. Mostly used for UID
	def toHex(self, message, colon=0):
	    message_list = message.split()
	    for byte in xrange(len(message_list)):
		message_list[byte] = hex(int(message_list[byte]))
		message_list[byte] = message_list[byte][2:]
		if len(message_list[byte]) == 1:
		    message_list[byte] = '0' + message_list[byte]
	    if colon == 2:
		s = ":"
		return s.join(message_list)
	    if colon == 1:
		s = " "
		return s.join(message_list)
	    s = ""
	    return '0x' + s.join(message_list)

##############################################################################

	# A function that changes the menu colors depending on if a test passes
	# or fails. This function is for event cases (IE, changing a single menu value)
	def infoValChange(self,event):
		for i in range(len(self.testPassInfo)):
			if (self.testPassList[i].get() == "Fail"):
				self.testPassInfo[i].configure(bg="#ff3333")
			elif (self.testPassList[i].get() == "Pass"):
				self.testPassInfo[i].configure(bg="green")
			else:
				self.testPassInfo[i].configure(bg="yellow")

	# Duplicate of above function, but for non-event cases (IE hitting the "Clear" button)
	def infoValChangeNonevent(self):
		for i in range(len(self.testPassInfo)):
                         if (self.testPassList[i].get() == "Fail"):
                                 self.testPassInfo[i].configure(bg="#ff3333")
                         elif (self.testPassList[i].get() == "Pass"):
                                 self.testPassInfo[i].configure(bg="green")
			 else:
				self.testPassInfo[i].configure(bg="yellow")

#############################################################################

	# Opens the proper GPIO slot. Used for programming cards.
	def gpioBttnPress(self):
		jSlotDict = {"J2 and J18" : 0x29, "J3 and J19" : 0x89, "J4 and J20" : 0xA9,
			     "J5 and J21" : 0x49, "J7 and J23" : 0x2A, "J8 and J24" : 0x8A,
			     "J9 and J25" : 0xAA, "J10 and J26" : 0x4A}

		print jSlotDict[self.gpioChoiceVar.get()]

		self.myBus.write(0x74,[0x08]) # PCA9538 is bit 3 on ngccm mux
		# myBus.write(0x70,[0x01,0x00]) # GPIO PwrEn is register 3
		#power on and reset
		    #register 3 is control reg for i/o modes
		self.myBus.write(0x70,[0x03,0x00]) # sets all GPIO pins to 'output' mode
		self.myBus.write(0x70,[0x01,0x08])
		self.myBus.write(0x70,[0x01,0x18]) # GPIO reset is 10
		self.myBus.write(0x70,[0x01,0x08])

		#jtag selectors finnagling for slot 26
		self.myBus.write(0x70,[0x01,jSlotDict[self.gpioChoiceVar.get()]])

		# myBus.write(0x70,[0x03,0x08])
		self.myBus.read(0x70,1)
		batch = self.myBus.sendBatch()
		print 'initial = ', batch

##################################################################################

	def getUniqueIDPress(self):		
		self.myBus.write(0x74,[0x18])
		self.myBus.sendBatch()

		slot = 0x19
		# Getting unique ID
		# 0x05000000ea9c8b7000   <- From main gui
		self.myBus.write(0x00,[0x06])
		self.myBus.write(slot,[0x11,0x04,0,0,0])
		self.myBus.write(0x50,[0x00])
		self.myBus.read(0x50, 8)
		raw_bus = self.myBus.sendBatch()
		print raw_bus
		cooked_bus = self.reverseBytes(raw_bus[-1])
		#cooked_bus = self.serialNum(cooked_bus)
		self.uniqueIDEntry.set(self.toHex(cooked_bus))
		self.uniqueIDPass = self.uniqueIDEntry.get()
		self.uniqueIDEntry.set("0x"+self.uniqueIDPass[4:(len(self.uniqueIDPass)-4)])

	        # Getting bridge firmware	
		self.myBus.write(0x00,[0x06])
		self.myBus.write(slot,[0x04])
		self.myBus.read(slot, 4)
		raw_data = self.myBus.sendBatch()[-1]
		med_rare_data = raw_data[2:]
		cooked_data = self.reverseBytes(med_rare_data)
		data_well_done = self.toHex(cooked_data)	# my apologies for the cooking references
		data_well_done = data_well_done[2:]
		print data_well_done
		self.firmwareVerEntry.set("0x"+data_well_done[0:2])    #these are the worst (best?) variable names ever
		self.firmwareVerMinEntry.set("0x"+data_well_done[2:4])
		self.firmwareVerOtherEntry.set("0x"+data_well_done[4:8])

		# Getting temperature
		self.tempEntry.set(str(round(temp.readManyTemps(slot, 10, "Temperature", "nohold"),4)))

		# Getting IGLOO firmware info
		majorIglooVer = it.readIgloo(slot, 0x00)
		minorIglooVer = it.readIgloo(slot, 0x01)
		# Parse IGLOO firmware info
		majorIglooVer = self.toHex(self.reverseBytes(majorIglooVer))
		minorIglooVer = self.toHex(self.reverseBytes(minorIglooVer))
		# Trim the entries of their error codes
		majorIglooVer = majorIglooVer[0:-2]
		minorIglooVer = minorIglooVer[0:-2]
		# Display igloo FW info on gui
		self.iglooMajVerEntry.set(majorIglooVer)
		self.iglooMinVerEntry.set(minorIglooVer)
		

root = Tk()
myapp = makeGui(root)
root.mainloop()
