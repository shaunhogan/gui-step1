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
import json
import client

class makeGui:
	def __init__(self, parent):
		# Create a webBus instance
		self.myBus = client.webBus("pi5",0)

		# Create an instance of initialTests
		self.initialTest = initialTests()
		
		# Make an empty list that will eventually contain all of
		# the active card slots
		self.outSlotNumbers = []

		# Name the parent. This is mostly for bookkeeping purposes
		# and doesn't really get used too much.
		self.myParent = parent

		self.nameChoiceVar  =  StringVar()
		self.infoCommentVar =  StringVar()	
		self.barcodeEntry   =  StringVar()
		self.uniqueIDEntry  =  StringVar()
	
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
					      "shogan","csmith","asmith","jpotarf",
					      "jlawrence","abaas")
		self.info_nameBox.pack(side=LEFT)
		self.nameChoiceVar.set("shogan") # initializes the OptionMenu

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
		#####  Experiment Setup Frm      #####
		#####				 #####
		######################################

		self.testLabelList = ["Test 1","Test 2","Test 3","Test 4",
		      		      "Test 5","Test 6","Test 7","Test 8",
				      "Test 9","Test 10","Test 11","Test 12",
				      "Test 13","Test 14","Test 15","Test 16"]

		# Make a label for the entire frame
		self.experi_subFrame_lbl = Label(self.experiment_frame,text="Hardware Setup (Check boxes to add cards to test)")
		self.experi_subFrame_lbl.configure(
			padx=button_padx,
			pady=button_pady,
			background="white"
			)
		self.experi_subFrame_lbl.pack(side=TOP)

		# Make top 1 subframe
		self.experi_subTop1_frame = Frame(self.experiment_frame,background="white")
		self.experi_subTop1_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        ipady=frame_ipady,
                        padx=frame_padx,
                        pady=frame_pady
			)

		# Make top 2 subframe
		self.experi_subTop2_frame = Frame(self.experiment_frame,background="white")
		self.experi_subTop2_frame.pack(
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


		# Make top 3 subframe
		self.experi_subTop3_frame = Frame(self.experiment_frame,background="white")
		self.experi_subTop3_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        padx=frame_padx,
			)

		# Make top 3 subframe for text
		self.experi_subTop3_fText = Frame(self.experiment_frame,background="white")
		self.experi_subTop3_fText.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        padx=frame_padx,
			)

		# Make top 4 subframe
		self.experi_subTop4_frame = Frame(self.experiment_frame,background="white")
		self.experi_subTop4_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        padx=frame_padx,
			)

		# Make top 4 subframe for text
		self.experi_subTop4_fText = Frame(self.experiment_frame,background="white")
		self.experi_subTop4_fText.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        padx=frame_padx,
			)

		# Make top 5 subframe
		self.experi_subTop5_frame = Frame(self.experiment_frame,background="white")
		self.experi_subTop5_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        padx=frame_padx,
			)

		# Make top 5 subframe for text
		self.experi_subTop5_fText = Frame(self.experiment_frame,background="white")
		self.experi_subTop5_fText.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        padx=frame_padx,
			)

		# Make top 6 subframe
		self.experi_subTop6_frame = Frame(self.experiment_frame,background="white")
		self.experi_subTop6_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        padx=frame_padx,
			)

		# Make top 6 subframe for text
		self.experi_subTop6_fText = Frame(self.experiment_frame,background="white")
		self.experi_subTop6_fText.pack(
			side=TOP,
                        ipadx=frame_ipadx,
                        padx=frame_padx,
			)

		# Make top 7 subframe
		self.experi_subTop7_frame = Frame(self.experiment_frame,background="white")
		self.experi_subTop7_frame.pack(
			side=TOP,
                        ipadx=frame_ipadx,
			ipady=frame_ipady,
			pady=frame_pady,
                        padx=frame_padx,
			)


		# Create variables for each manual check (16 placeholders for now)
		self.testPassList = [StringVar() for i in range(0,17)]
		self.testPassState = ("Pass","Fail")

		# Make a label for the Barcode entry
		self.experi_barcode_lbl = Label(self.experi_subTop1_frame, text="Barcode: ")
		self.experi_barcode_lbl.configure(
			background="white",
			padx=button_padx,
			pady=button_pady,
			)
		self.experi_barcode_lbl.pack(side=LEFT)
		
		# Make an entry box for the barcode
		# Make a entrybox for testing comments
		self.experi_barcode_entry = Entry(
			self.experi_subTop1_frame,
			textvariable=self.barcodeEntry
			)
		self.experi_barcode_entry.pack(side=RIGHT)

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
			textvariable=self.uniqueIDEntry
			)
		self.experi_uniqueID_entry.pack(side=RIGHT)

		# Make a button to read the unique ID
		self.experi_uniqueID_get = Button(self.experi_subTop2_5_frame, text ="Get Unique ID", command=self.getUniqueIDPress)
		self.experi_uniqueID_get.configure(bg="salmon")
		self.experi_uniqueID_get.pack()

		for i in range(0,4):
			self.testPassInfo = OptionMenu(self.experi_subTop3_frame,self.testPassList[i],"Fail","Pass")
			self.testPassList[i].set("Fail")
			self.testPassInfo.pack(side=LEFT)

			self.testPassLabel=Label(self.experi_subTop3_fText, text=self.testLabelList[i]+"\n", bg="white")
			self.testPassLabel.configure(padx=13)
			self.testPassLabel.pack(side=LEFT)
		
		for i in range(4,8):
			self.testPassInfo = OptionMenu(self.experi_subTop4_frame,self.testPassList[i],"Fail","Pass")
			self.testPassList[i].set("Fail")
			self.testPassInfo.pack(side=LEFT)

			self.testPassLabel=Label(self.experi_subTop4_fText, text=self.testLabelList[i]+"\n", bg="white")
			self.testPassLabel.configure(padx=13)
			self.testPassLabel.pack(side=LEFT)

		for i in range(8,12):
			self.testPassInfo = OptionMenu(self.experi_subTop5_frame,self.testPassList[i],"Fail","Pass")
			self.testPassList[i].set("Fail")
			self.testPassInfo.pack(side=LEFT)

			self.testPassLabel=Label(self.experi_subTop5_fText, text=self.testLabelList[i]+"\n", bg="white")
			self.testPassLabel.configure(padx=12)
			self.testPassLabel.pack(side=LEFT)

		for i in range(12,16):
			self.testPassInfo = OptionMenu(self.experi_subTop6_frame,self.testPassList[i],"Fail","Pass")
			self.testPassList[i].set("Fail")
			self.testPassInfo.pack(side=LEFT)

			self.testPassLabel=Label(self.experi_subTop6_fText, text=self.testLabelList[i]+"\n", bg="white")
			self.testPassLabel.configure(padx=12)
			self.testPassLabel.pack(side=LEFT)

		# Make a button to submit tests and information
		self.initSubmitBttn = Button(self.experi_subTop7_frame, text="Submit Tests & Info", command=self.initSubmitBttnPress)
		self.initSubmitBttn.configure(bg="turquoise")
		self.initSubmitBttn.pack()



	#################################
	###			      ###
	###  BEGIN MEMBER FUNCTIONS   ###
	###			      ###
	#################################

	def jdefault(self,o):
		return o.__dict__
	
	def initSubmitBttnPress(self):
		self.initialTest.testerName = self.nameChoiceVar.get()
		self.initialTest.testComment = self.infoCommentVar.get()
		self.initialTest.barcode     = self.barcodeEntry.get()
		self.initialTest.uniqueID    = self.uniqueIDEntry.get()

		for i in range(len(self.testPassList)):
			if self.testPassList[i].get() == "Pass":
				self.initialTest.testResults[self.testLabelList[i-1]] = True
			else:
				self.initialTest.testResults[self.testLabelList[i-1]] = False
		
		fileString = self.uniqueIDEntry.get()+"_step1_raw.json"		
	
		with open(fileString,"w") as jsonFile:
			json.dump(self.initialTest, jsonFile, default = self.jdefault)	
		
		print "Preliminary step recorded. Thank you!"

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

	def getUniqueIDPress(self):
		self.myBus.write(0x00,[0x06])
		self.myBus.write(0x19,[0x11,0x04,0,0,0])
		self.myBus.write(0x50,[0x00])
		self.myBus.read(0x50, 8)
		raw_bus = self.myBus.sendBatch()
		print raw_bus
		cooked_bus = self.reverseBytes(raw_bus[-1])
		cooked_bus = self.serialNum(cooked_bus)
		self.uniqueIDEntry.set(self.toHex(cooked_bus))

root = Tk()
myapp = makeGui(root)
root.mainloop()
