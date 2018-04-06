# -*- coding: utf-8 -*-
"""
	Ian Mallarino
	Intro to Image and Video Processing
	Opens a GUI that allows the user to either open or create an image and save it to disk
"""

from math import *
import sys
import random
import tkinter as tk
from tkinter import filedialog
from PIL import Image,ImageTk

random.seed(a=None)

def fibonacciTest(image):
	"""Use fibonacci sequence to generate image"""
	pixel=image.load()
	a=0
	b=1
	color=[0]*3
	
	for i in range(0,image.size[0]):
		for j in range(0,image.size[1]):
			for k in range(0,3):
				color[k]=b%256
				a=a+b
				a,b=b,a
			pixel[i,j]=(
				color[0],
				color[1],
				color[2]
			)
	
	return image

class Gui(tk.Frame):
	"""Main window for program"""
	def __init__(self,master=None,WIDTH=640,HEIGHT=480):
		"""Constructor"""
		super(Gui,self).__init__()
		tk.Frame.__init__(self,master)
		master.protocol('WM_DELETE_WINDOW',quit)
		self.pack(fill="both",expand=True)
		self.master.title("Generate Image")
		self.img=Image.new("RGB",(640,480),"black")
		self.load()
		self.update()
		
	def load(self):
		"""Loads the contents within the window"""
		#image preview
		self.label=tk.Label(self)
		self.label.pack(side="top")
		#buttons for user
		self.buttons=tk.Frame(self)
		self.buttons.pack(side="bottom")
		#"open" button
		self.open=tk.Button(self.buttons,text="Open",command=self.open)
		self.open.pack(side="left")
		#"generate image" button
		self.generate=tk.Button(self.buttons,text="Generate",command=self.generateImg)
		self.generate.pack(side="left")
		#"random image" button
		self.random=tk.Button(self.buttons,text="Random",command=self.randomImg)
		self.random.pack(side="left")
		#"save" button
		self.save=tk.Button(self.buttons,text="Save",command=self.saveImg)
		self.save.pack(side="left")
		
	def update(self):
		"""Recalls itself constantly"""
		self.preview=ImageTk.PhotoImage(self.img.resize((640,480)))
		self.label.configure(image=self.preview)
		self.after(50,self.update)
		return
		
	def open(self):
		"""Opens the image to the GUI"""
		filePath=filedialog.askopenfilename(
			parent=self,
			initialfile="out.png",
			filetypes=[
				("Image files","*.bmp,*.dib,*.gif,*.jpg,*.jpe,*.jpeg,*.psd,*.tif,*.tiff"),
				("BMP","*.bmp,*.dib"),
				("GIF","*.gif"),
				("JPEG","*.jpg,*.jpe,*.jpeg"),
				("PSD","*.psd"),
				("TIFF","*.tif,*.tiff")
			]
		)
		try:
			self.img=Image.open(filePath)
		except:
			print("Couldn't open file.")
		return
	
	def generateImg(self):
		"""Test function; generates using math functions"""
		pixel=self.img.load()
		imgSize=self.img.size
		p=1
		
		for x in range(0,self.img.size[0]):
			for y in range(0,self.img.size[1]):
				#Begin generation
				
				#loss=y/(x+1)*tan((x)*(y)*pi/180)
				#diamond=(cos(x*pi/180)+sin(y*pi/180))*255%sys.maxsize
				#wave=(cos(x*pi/180)+tan(y*pi/180))*255%sys.maxsize
				grid=(tan(x*pi/180)+tan(y*pi/180))%sys.maxsize
				#gradient1=(x/imgSize[0]+y/imgSize[1])/2*255%sys.maxsize
				#gradient2=(x/imgSize[0]-y/imgSize[1])*255%sys.maxsize
				#diagGrad1=cos((x/imgSize[0]-y/imgSize[1])/2*pi)*255
				#diagGrad2=sin((x/imgSize[0]+y/imgSize[1])/2*pi)*255
				#eye=(sin(y*pi/180)-cos(x*pi/180)*2)*255
				circ=255 if int(pow((2*x-imgSize[0])/9,2)+pow((2*y-imgSize[1])/9,2))<127 else 0
				invCirc=int((pow((2*x-imgSize[0])/9,2)+pow((2*y-imgSize[1])/9,2))/127)*255
				ripple=int(pow((2*x-imgSize[0])/10,2)+pow((2*y-imgSize[1])/10,2))
				
				R=grid
				G=grid
				B=ripple
				pixel[x,y]=(
					int(R*p+random.randint(0,255)*(1-p))%256,
					int(G*p+random.randint(0,255)*(1-p))%256,
					int(B*p+random.randint(0,255)*(1-p))%256
				)
				#End generation
		#self.img=fibonacciTest(self.img)
		return
	
	def randomImg(self):
		"""Generates pixels with random values"""
		pixel=self.img.load()
		
		for i in range(0,self.img.size[0]):
			for j in range(0,self.img.size[1]):
				pixel[i,j]=(
					random.randint(0,255),
					random.randint(0,255),
					random.randint(0,255)
				)
		return
		
	def saveImg(self):
		"""Outputs the image to the harddrive"""
		#TODO: filedialog.asksaveasfilename()
		self.img.save("out.png","png")
		return

root=tk.Tk()
gui=Gui(master=root)
gui.mainloop()
gui.destroy()
