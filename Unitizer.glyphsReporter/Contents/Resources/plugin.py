# encoding: utf-8
from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
# from Foundation import NSObject, NSPoint
# from AppKit import NSBezierPath, NSColor
import sys, os, re
from math import pi,tan
import traceback

class Unitizer (ReporterPlugin ):
	@objc.python_method
	def settings(self):
		self.menuName = "Unitizer"
		self.hasWarned = False
	
	@objc.python_method
	def background( self, Layer ):
		"""
		Whatever you draw here will be displayed BEHIND the paths.
		"""
		try:
			# set defaults:
			layerWidth = Layer.width  # get width of the layer
			yBottom = -200.0 # default descender
			yTop    =  800.0 # default ascender
			unit    =  40.0  # default unit
			
			try: # try to overwrite defaults with actual values from the master:
				currentMaster = Layer.associatedFontMaster()
				yBottom = currentMaster.descender
				yTop    = currentMaster.ascender
				slant   = currentMaster.italicAngle / 180 * pi
				displacement = tan(slant) * (yTop-yBottom)
				# See https://github.com/impallari/Unitizer/issues/4 for explanation
				xDisplacement = (-yBottom + 0.5 * currentMaster.xHeight) * tan(slant)
				customParameter = currentMaster.customParameters['unitizerUnit']
				if customParameter:
					unit = float(customParameter)
				elif not self.hasWarned:
					print("Unitizer plugin: Add your unitizerUnit custom parameter to your master")
					self.hasWarned = True
			except Exception as e:
				print(traceback.format_exc())
			
			# color the width gap:
			NSColor.redColor().set() # set color to red
			gap = layerWidth % unit
			gapStart = layerWidth-gap - xDisplacement
			if gap:
				bl = NSPoint( gapStart, yBottom )
				tl = NSPoint( gapStart + displacement, yTop )
				br = NSPoint( gapStart + gap, yBottom)
				tr = NSPoint( gapStart + gap + displacement, yTop )
				gapRectangle = NSBezierPath.alloc().init()
				gapRectangle.moveToPoint_(bl)
				gapRectangle.lineToPoint_(tl)
				gapRectangle.lineToPoint_(tr)
				gapRectangle.lineToPoint_(br)
				gapRectangle.lineToPoint_(bl)
				gapRectangle.fill()

			# draw vertical lines:
			# starting point = 1 unit away from LSB at the descender line.
			x = unit - xDisplacement
			unitLines = NSBezierPath.alloc().init() # initialize a path object myPath
			# while x < gapStart:
			while x <= gapStart:
				# draw vertical line:
				unitLines.moveToPoint_( NSPoint( x, yBottom ) )
				unitLines.lineToPoint_( NSPoint( x+displacement, yTop    ) )
				x += unit # advance to the right
			if gap:
				# set color for unit lines:
				# NSColor.lightGrayColor().set()
				NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.7, 0.5, 0.5, 0.6 ).set()
			else:
				# very light gray if there is no gap:
				NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.7, 0.7, 0.7, 0.6 ).set()

			# unitLines.setLineWidth_( 1.0 / self.getScale() ) # set stroke thickness for current scale
			unitLines.setLineWidth_( 1.0 ) # Always 1
			unitLines.stroke() # add stroke to the path object
			
		except Exception as e:
			print(traceback.format_exc())
	
	def needsExtraMainOutlineDrawingForInactiveLayer_(self, Layer):
		"""
		Whatever you draw here will be displayed in the Preview at the bottom.
		Remove the method or return True if you want to leave the Preview untouched.
		Return True to leave the Preview as it is and draw on top of it.
		Return False to disable the Preview and draw your own.
		In that case, don't forget to add Bezier methods like in drawForegroundForLayer_(),
		otherwise users will get an empty Preview.
		"""
		return True
