from kivy.app import App #for the main app
from kivy.uix.floatlayout import FloatLayout #the UI layout
from kivy.uix.label import Label #a label to show information
from plyer import camera #object to read the camera

import android
import android.activity
from os import unlink
from jnius import autoclass, cast
from plyer.facades import Camera
from plyer.platforms.android import activity

Intent = autoclass('android.content.Intent')
PythonActivity = autoclass('org.renpy.android.PythonActivity')
MediaStore = autoclass('android.provider.MediaStore')
Uri = autoclass('android.net.Uri')


class AndroidCamera(Camera):

	def _take_picture(self, on_complete, filename=None):
		assert(on_complete is not None)
		self.on_complete = on_complete
		self.filename = filename
		android.activity.unbind(on_activity_result=self._on_activity_result)
		android.activity.bind(on_activity_result=self._on_activity_result)
		intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
		uri = Uri.parse('file://' + filename)
		parcelable = cast('android.os.Parcelable', uri)
		intent.putExtra(MediaStore.EXTRA_OUTPUT, parcelable)
		activity.startActivityForResult(intent, 0x123)

	def _take_video(self, on_complete, filename=None):
		assert(on_complete is not None)
		self.on_complete = on_complete
		self.filename = filename
		android.activity.unbind(on_activity_result=self._on_activity_result)
		android.activity.bind(on_activity_result=self._on_activity_result)
		intent = Intent(MediaStore.ACTION_VIDEO_CAPTURE)
		uri = Uri.parse('file://' + filename)
		parcelable = cast('android.os.Parcelable', uri)
		intent.putExtra(MediaStore.EXTRA_OUTPUT, parcelable)

		# 0 = low quality, suitable for MMS messages,
		# 1 = high quality
		intent.putExtra(MediaStore.EXTRA_VIDEO_QUALITY, 1)
		activity.startActivityForResult(intent, 0x123)

	def _on_activity_result(self, requestCode, resultCode, intent):
		if requestCode != 0x123:
			return
		android.activity.unbind(on_activity_result=self._on_activity_result)
		if self.on_complete(self.filename):
			self._unlink(self.filename)

	def _unlink(self, fn):
		try:
			unlink(fn)
		except:
			pass


def instance():
	return AndroidCamera()

"""
[app]
title = Python Camera
package.name = camera
package.domain = com.wordpress.bytedebugger
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = kivy, plyer
fullscreen = 1
[buildozer]
log_level = 2
"""

class UI(FloatLayout):#the app ui
	def __init__(self, **kwargs):
		super(UI, self).__init__(**kwargs)
		self.lblCam = Label(text="Click to take a picture!") #create a label at the center
		self.add_widget(self.lblCam) #add the label at the screen
		self.my_camera = AndroidCamera()

	def  on_touch_down(self, e):
		self.my_camera._take_picture(self.done, '/storage/sdcard0/example.jpg')
		pass
		#camera.take_picture('/storage/sdcard0/example.jpg', self.done) #Take a picture and save at this location. After will call done() callback

	def done(self, e): #receive e as the image location
		self.lblCam.text = 'sucsses'; #update the label to the image location

class Camera(App): #our app
	def build(self):
		ui = UI()# create the UI
		return ui #show it

	def on_pause(self):
		#when the app open the camera, it will need to pause this script. So we need to enable the pause mode with this method
		return True

	def on_resume(self):
		#after close the camera, we need to resume our app.
		pass

Camera().run() #start our app
