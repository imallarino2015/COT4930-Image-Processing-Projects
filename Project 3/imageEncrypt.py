# -*- coding: utf-8 -*-
"""
	Ian Mallarino
	Intro to Image and Video Processing
	Embeds a watermark in to an image
"""

from sys import getsizeof as size
import numpy
import rng
import time
import tkinter as tk
from tkinter import filedialog
from PIL import Image,ImageTk

def openFile(pnt):
	"""Returns the path of a file chosen by the user"""
	return filedialog.askopenfilename(
		parent=pnt,
		initialfile="out.png",
		filetypes=[
			("Image files","*.*"),
			("BMP","*.bmp,*.dib"),
			("GIF","*.gif"),
			("PNG","*.png"),
			("JPEG","*.jpg,*.jpe,*.jpeg"),
			("PSD","*.psd"),
			("TIFF","*.tif,*.tiff")
		]
	)

class Gui(tk.Frame):
	"""Main window for program"""
	def __init__(self,master=None):
		"""Constructor"""
		super(Gui,self).__init__()
		tk.Frame.__init__(self,master)
		master.protocol('WM_DELETE_WINDOW',quit)
		self.rand=rng	#handler for the rng module
		self.key=1	#the seed for the random generator that processes the image
		self.pack(fill="both",expand=True)
		self.master.title("Watermark")
		self.lImg=Image.new("RGB",(640,480),"black")
		self.load()
		self.update()
		
	def load(self):
		"""Loads the contents within the window"""
		#image preview
		self.pre=tk.Frame(self)
		self.pre.pack(side="bottom")
		#key input bar
		self.keyIn=tk.Entry(self)
		self.keyIn.insert(0,self.key)
		self.keyIn.pack(side="bottom")
		#left image
		self.lPre=tk.Label(self.pre)
		self.lPre.pack(side="left")
		#buttons for user
		self.buttons=tk.Frame(self)
		self.buttons.pack(side="bottom")
		#"open image" button
		self.openI=tk.Button(self.buttons,text="Open Image",command=self.openImg)
		self.openI.pack(side="left")
		#"process image" button
		self.processI=tk.Button(self.buttons,text="Process Image",command=self.processImg)
		self.processI.pack(side="left")
		#"generate key" button
		self.genK=tk.Button(self.buttons,text="Generate Key",command=self.generateKey)
		self.genK.pack(side="left")
		#"save" button
		self.save=tk.Button(self.buttons,text="Save",command=self.saveImg)
		self.save.pack(side="left")
		
	def update(self):
		"""Recalls itself constantly"""
		self.lPreview=ImageTk.PhotoImage(self.lImg.resize((640,480)))
		self.lPre.configure(image=self.lPreview)
		self.after(50,self.update)
		return
		
	def openImg(self):
		"""Opens the image to the GUI"""
		try:
			self.lImg=Image.open(openFile(self))
		except:
			print("Couldn't open file.")
		return
		
	def processImg(self):
		"""Runs the image through an encryption algorithm"""
		self.rand.rndUInt(int(self.keyIn.get()))
		pixel=self.lImg.load()
		for x in range(0,self.lImg.size[0]):
			for y in range(0,self.lImg.size[1]):
				pixel[x,y]=(
					self.lImg.getpixel((x,y))[0]^(self.rand.rndUInt()%256),
					self.lImg.getpixel((x,y))[1]^(self.rand.rndUInt()%256),
					self.lImg.getpixel((x,y))[2]^(self.rand.rndUInt()%256)
				)
	
	def generateKey(self):
		"""Hashes an image in to a number"""
		try:
			keyImg=Image.open(openFile(self))
		except:
			print("Couldn't open file.")
			self.keyIn.delete(0,"end")
			self.keyIn.insert(0,0)
			return
		
		imgArr=numpy.array(keyImg.getdata())
		imgArr=imgArr.flatten()
		key=self.rand.hash(imgArr)
		self.keyIn.delete(0,"end")
		self.keyIn.insert(0,key)
		
	def saveImg(self):
		"""Outputs the image to the harddrive TODO: """
		self.lImg.save("out.png","png")
		return

root=tk.Tk()
gui=Gui(master=root)
gui.mainloop()
gui.destroy()
