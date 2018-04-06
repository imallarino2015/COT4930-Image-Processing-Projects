# -*- coding: utf-8 -*-
"""
	Ian Mallarino
	Intro to Image and Video Processing
	Embeds a watermark in to an image
"""

import tkinter as tk
from tkinter import filedialog
from PIL import Image,ImageTk

class Gui(tk.Frame):
	"""Main window for program"""
	def __init__(self,master=None):
		"""Constructor"""
		super(Gui,self).__init__()
		tk.Frame.__init__(self,master)
		master.protocol('WM_DELETE_WINDOW',quit)
		self.pack(fill="both",expand=True)
		self.master.title("Watermark")
		self.lImg=Image.new("RGB",(640,480),"black")
		self.rImg=Image.new("RGB",(160,120),"black")
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
		#"open image" button
		self.openI=tk.Button(self.buttons,text="Open Image",command=self.openImg)
		self.openI.pack(side="left")
		#"open watermark" button
		self.openWM=tk.Button(self.buttons,text="Open Watermark",command=self.openWatermark)
		self.openWM.pack(side="left")
		#"embed" button
		self.embed=tk.Button(self.buttons,text="Embed",command=self.embed)
		self.embed.pack(side="left")
		#"extract" button
		self.extract=tk.Button(self.buttons,text="Extract",command=self.extract)
		self.extract.pack(side="left")
		#"save" button
		self.save=tk.Button(self.buttons,text="Save",command=self.saveImg)
		self.save.pack(side="left")
		
	def update(self):
		"""Recalls itself constantly"""
		self.lPreview=ImageTk.PhotoImage(self.lImg.resize((640,480)))
		self.lPre.configure(image=self.lPreview)
		self.rPreview=ImageTk.PhotoImage(self.rImg.resize((160,120)))
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
			self.rImg=self.rImg.resize((int(self.lImg.size[0]/4),int(self.lImg.size[1]/4)))
		except:
			print("Couldn't open file.")
		return
		
	def openWatermark(self):
		"""Open a new watermark image"""
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
			self.rImg=Image.open(filePath)
			self.rImg=self.rImg.resize((int(self.lImg.size[0]/4),int(self.lImg.size[1]/4)))
		except:
			print("Couldn't open file.")
		return
		
	def embed(self):
		"""Embed a watermark in to an image"""
		print("Embedding...")
		pixel=self.lImg.load()
		val=0
		bit=0
		rCol=0
		rX=0
		rY=0
		for x in range(0,int(self.lImg.size[0]/4)*4,2):
			for y in range(0,int(self.lImg.size[1]/4)*4):
				for lCol in range(0,3):
					#collect the color
					val=(self.rImg.getpixel((rX,rY))[rCol]>>bit)&1
					pixel[x,y]=(
						self.lImg.getpixel((x,y))[0]&(~1)|val if lCol==0 else self.lImg.getpixel((x,y))[0],
						self.lImg.getpixel((x,y))[1]&(~1)|val if lCol==1 else self.lImg.getpixel((x,y))[1],
						self.lImg.getpixel((x,y))[2]&(~1)|val if lCol==2 else self.lImg.getpixel((x,y))[2],
					)
					bit+=1
					if(bit>=8):
						bit=0
						rCol+=1
						if(rCol==3):
							rCol=0
							rX+=1
							if(rX>=self.rImg.size[0]):
								rX=0
								rY+=1
		return
		
	def extract(self):
		"""Extract a watermark from an image"""
		val=0
		bit=0
		rCol=0
		rX=0
		rY=0
		pixel=self.rImg.load()
		for x in range(0,int(self.lImg.size[0]/4)*4,2):
			for y in range(0,int(self.lImg.size[1]/4)*4):
				for lCol in range(0,3):
					#collect the color
					val+=(self.lImg.getpixel((x,y))[lCol]&1)<<bit
					bit+=1
					if(bit>=8):
						bit=0
						#write to the color
						pixel[rX,rY]=(
							val if rCol==0 else self.rImg.getpixel((rX,rY))[0],
							val if rCol==1 else self.rImg.getpixel((rX,rY))[1],
							val if rCol==2 else self.rImg.getpixel((rX,rY))[2]
						)
						val=0
						rCol+=1
						if(rCol>=3):
							rCol=0
							rX+=1
							if(rX>=self.rImg.size[0]):
								rX=0
								rY+=1
		return
		
	def saveImg(self):
		"""Outputs the image to the harddrive TODO: """
		self.lImg.save("out.png","png")
		return

root=tk.Tk()
gui=Gui(master=root)
gui.mainloop()
gui.destroy()