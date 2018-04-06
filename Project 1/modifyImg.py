# -*- coding: utf-8 -*-
"""
	Ian Mallarino
	Intro to Image and Video Processing
	Opens a GUI that allows the user to open an image from file and modify it
"""

from math import *
import random
import tkinter as tk
from tkinter import filedialog
from PIL import Image,ImageTk

random.seed(a=None)

class Gui(tk.Frame):
	"""Main window for program"""
	def __init__(self,master=None,WIDTH=640,HEIGHT=480):
		"""Constructor"""
		super(Gui,self).__init__()
		tk.Frame.__init__(self,master)
		master.protocol('WM_DELETE_WINDOW',quit)
		self.pack(fill="both",expand=True)
		self.master.title("Generate Image")
		self.lImg=Image.new("RGB",(640,480),"black")
		self.rImg=Image.new("RGB",(640,480),"black")
		self.load()
		self.update()
		
	def load(self):
		"""Loads the contents within the window"""
		self.isOpening=False
		#image preview
		self.pre=tk.Frame(self)
		self.pre.pack(side="bottom")
		#left image
		self.lPre=tk.Label(self.pre)
		self.lPre.pack(side="left")
		#right image
		self.rPre=tk.Label(self.pre)
		self.rPre.pack(side="right")
		#buttons for user
		self.buttons=tk.Frame(self)
		self.buttons.pack(side="bottom")
		#"open" button
		self.open=tk.Button(self.buttons,text="Open",command=self.openImg)
		self.open.pack(side="left")
		#"proces" button
		self.modify=tk.Button(self.buttons,text="Modify",command=self.modImg)
		self.modify.pack(side="left")
		#"save" button
		self.save=tk.Button(self.buttons,text="Save",command=self.saveImg)
		#self.save.pack(side="left")
		
	def update(self):
		"""Recalls itself constantly"""
		self.lPreview=ImageTk.PhotoImage(self.lImg.resize((640,480)))
		self.lPre.configure(image=self.lPreview)
		self.rPreview=ImageTk.PhotoImage(self.rImg.resize((640,480)))
		self.rPre.configure(image=self.rPreview)
		self.after(50,self.update)
		return
		
	def openImg(self):
		"""Opens the image to the GUI"""
		filePath=filedialog.askopenfilename(
			parent=self,
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
		try:
			self.lImg=Image.open(filePath)
			self.rImg=Image.new("RGB",self.lImg.size,"black")
		except:
			print("Couldn't open file.")
		return
		
	def modImg(self):
		""""""
		pixel=self.rImg.load()
		for x in range(0,self.lImg.size[0]):
			for y in range(0,self.lImg.size[1]):
				R=self.lImg.getpixel((x,y))[0]
				G=self.lImg.getpixel((x,y))[1]
				B=self.lImg.getpixel((x,y))[2]
				pixel[x,y]=(
					int(R/127)*255,
					int(G/127)*255,
					int(B/127)*255
				)
		
	def saveImg(self):
		"""Outputs the image to the harddrive TODO: """
		self.rImg.save("out.png","png")
		return
		
root=tk.Tk()
gui=Gui(master=root)
gui.mainloop()
gui.destroy()