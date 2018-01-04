#!/usr/bin/env python
# encoding: utf-8

import objc
import GlyphsApp
from Foundation import NSObject, NSPoint
from AppKit import NSBezierPath, NSColor
import sys, os, re
from math import pi,tan


GlyphsReporterProtocol = objc.protocolNamed( "GlyphsReporter" )

class Unitizer ( NSObject, GlyphsReporterProtocol ):
	
	def init( self ):
		"""
		Put any initializations you want to make here.
		"""
		try:
			return self
		except Exception as e:
			self.logToConsole( "init: %s" % str(e) )
	
	def interfaceVersion( self ):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		try:
			return 1
		except Exception as e:
			self.logToConsole( "interfaceVersion: %s" % str(e) )
	
	def title( self ):
		"""
		This is the name as it appears in the menu in combination with 'Show'.
		E.g. 'return "Nodes"' will make the menu item read "Show Nodes".
		"""
		try:
			return "Unitizer"
		except Exception as e:
			self.logToConsole( "title: %s" % str(e) )
	
	def keyEquivalent( self ):
		"""
		The key for the keyboard shortcut. Set modifier keys in modifierMask() further below.
		Pretty tricky to find a shortcut that is not taken yet, so be careful.
		If you are not sure, use 'return None'. Users can set their own shortcuts in System Prefs.
		"""
		try:
			return None
		except Exception as e:
			self.logToConsole( "keyEquivalent: %s" % str(e) )
	
	def modifierMask( self ):
		return 0
	
	def drawForegroundForLayer_( self, Layer ):
		pass
	
	def drawBackgroundForLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed BEHIND the paths.
		"""
		try:
			# set defaults:
			layerWidth = Layer.width  # get width of the layer
			yBottom = -200.0 # default descender
			yTop    =  800.0 # default ascender
			unit    = 40.0   # default unit
			
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
				else:
					print "Unitizer plugin: Add your unitizerUnit custom parameter to your master"
			except Exception as e:
				pass
			
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
			self.logToConsole( "drawBackgroundForLayer_: %s" % str(e) )
	
	def drawBackgroundForInactiveLayer_( self, Layer ):
		pass
	
	def needsExtraMainOutlineDrawingForInactiveLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed in the Preview at the bottom.
		Remove the method or return True if you want to leave the Preview untouched.
		Return True to leave the Preview as it is and draw on top of it.
		Return False to disable the Preview and draw your own.
		In that case, don't forget to add Bezier methods like in drawForegroundForLayer_(),
		otherwise users will get an empty Preview.
		"""
		return True
	
	def setController_( self, Controller ):
		"""
		Use self.controller as object for the current view controller.
		"""
		try:
			self.controller = Controller
		except Exception as e:
			self.logToConsole( "Could not set controller" )
	
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Show %s plugin:\n%s" % ( self.title(), message )
		print myLog
		NSLog( myLog )
