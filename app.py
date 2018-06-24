import wx
import os
import cv2
import pytesseract
from PIL import Image

mode_global = "Standard Noise Mode"

class AppOCR(wx.Frame):
	
	def __init__(self, parent, id):
		# initialize the frame
		wx.Frame.__init__(self, parent, id, "Optical Character Recognition", size=(600, 550))
		# initialize a panel
		self.panel = wx.Panel(self)
		# position the frame in the center of the screen
		self.Centre()
		# create and bind the radio buttons
		self.RadioButtonsInit()
		# create the widgets related to the image 
		self.WidgetsInit()

	def RadioButtonsInit(self):
		# add radio buttons
		wx.StaticText(self.panel, -1, "Select a working mode:", (10,10))
		self.rb1 = wx.RadioButton(self.panel, label='Standard Noise Mode', pos=(10, 30), style=wx.RB_GROUP)
		self.rb2 = wx.RadioButton(self.panel, label='Salt and Pepper Noise Mode', pos=(10, 50))
		# bind the radio buttons to an event handler
		self.rb1.Bind(wx.EVT_RADIOBUTTON, self.SetVal)
		self.rb2.Bind(wx.EVT_RADIOBUTTON, self.SetVal)

	def WidgetsInit(self):
		# initialize the image section
		self.image = wx.Image(565, 250)
		self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(self.image), (10, 100))
		# initialize the browser button
		self.browse = wx.Button(self.panel, pos=(230, 380), size=(100, -1), label="Browse")
		self.browse.Bind(wx.EVT_BUTTON, self.OnBrowse)
		# initialize the image path display field
		self.imageURL = wx.TextCtrl(self.panel, pos=(10, 382), size=(200,-1))
		# initialize the submit button
		self.submit = wx.Button(self.panel, pos=(475, 380), size=(100, -1), label="Submit")
		self.submit.Bind(wx.EVT_BUTTON, self.OnSubmit)
		

	def SetVal(self, e):
		mode = e.GetEventObject()
		global mode_global
		if mode.GetLabel() == "Standard Noise Mode":
			mode_global = "Standard Noise Mode"
		else:
			mode_global = "Salt and Pepper Noise Mode"

	def OnBrowse(self, event):
		# browse for the image
		wildcard = "PNG files (*.png)|*.png"
		browseDialog = wx.FileDialog(None, "Choose an image", wildcard=wildcard, style=wx.FD_OPEN)
		if browseDialog.ShowModal() == wx.ID_OK:
			self.imageURL.SetValue(browseDialog.GetPath())
		browseDialog.Destroy()
		self.ShowImage()

	def ShowImage(self, filepath = ""):
		# get the filepath
		if filepath == "":
			filepath = self.imageURL.GetValue()
		self.image = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
		self.imageCtrl.SetBitmap(wx.Bitmap(self.image))
		self.panel.Refresh()

	def OnSubmit(self, event):	
		global mode_global
		image = cv2.imread(self.imageURL.GetValue())
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		if mode_global == "Standard Noise Mode":
			gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
		else:
			gray = cv2.medianBlur(gray, 3)
		filename = '{}.png'.format(os.getpid())
		cv2.imwrite(filename, gray)
		text = pytesseract.image_to_string(Image.open(filename))
		print(text)
		# initialize the results field
		self.result = wx.StaticText(self.panel, -1, text, pos=(10, 450), size=(300, -1))
		#self.result2 = wx.StaticText(self.panel, -1, "standard noise", pos=(10, 470), size=(300, -1))
		self.result.SetForegroundColour('black')
		self.result.SetBackgroundColour('white')
		#self.result2.SetForegroundColour('black')
		#self.result2.SetBackgroundColour('white')

if __name__ == '__main__':
	app = wx.App()
	frame = AppOCR(parent = None, id = -1)
	frame.Show()
	app.MainLoop()