# encoding: utf-8
from __future__ import division, print_function, unicode_literals

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from math import pi, tan

class Unitizer ( ReporterPlugin ):
	
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Unitizer',
			# 'de': 'Unitiser',
			# 'fr': 'Unitisateur',
			# 'es': 'Unitador',
			# 'pt': 'Unitador',
			})
	
	@objc.python_method
	def layerMetrics( self, Layer ):
		"""docstring for layerMetrics"""
		try:
			# set defaults:
			layerWidth = Layer.width  # get width of the layer
			yBottom = -200.0 # default descender
			yTop    =  800.0 # default ascender
			unit    =   40.0 # default unit
			currentMaster = Layer.master
			yBottom = currentMaster.descender
			yTop    = currentMaster.ascender
			slant   = currentMaster.italicAngle / 180 * pi
			displacement = tan(slant) * (yTop-yBottom)
			# See https://github.com/impallari/Unitizer/issues/4 for explanation
			xDisplacement = (-yBottom + 0.5 * currentMaster.xHeight) * tan(slant)
			customParameter = currentMaster.customParameters['unitizerUnit']
			if customParameter:
				unit = float(customParameter)
			gap = layerWidth % unit
			gapStart = layerWidth-gap - xDisplacement
			return gap, gapStart, layerWidth, yBottom, yTop, unit, slant, displacement, xDisplacement
		except Exception as e:
			self.logToConsole( "layerMetrics: %s" % str(e) )
	
	@objc.python_method
	def drawGrid( self, Layer ):
		# draw vertical lines
		try:
			if self.getScale() >= 0.2:
				gap, gapStart, layerWidth, yBottom, yTop, unit, slant, displacement, xDisplacement = self.layerMetrics(Layer)
				x = unit - xDisplacement
				unitLines = NSBezierPath.alloc().init() # initialize a path object myPath
				while x <= gapStart:
					# draw vertical line:
					unitLines.moveToPoint_( NSPoint( x, yBottom ) )
					unitLines.lineToPoint_( NSPoint( x+displacement, yTop    ) )
					x += unit # advance to the right
				if gap:
					NSColor.textColor().colorWithAlphaComponent_(0.3).set()
				else:
					NSColor.textColor().colorWithAlphaComponent_(0.07).set()
				unitLines.setLineWidth_( 0.67/self.getScale() )
				unitLines.stroke() # add stroke to the path object
		except Exception as e:
			self.logToConsole( "drawGrid: %s" % str(e) )
	
	@objc.python_method
	def drawGap( self, Layer ):
		# color the width gap:
		try:
			if self.getScale() >= 0.1: # minimum 150pt scale
				gap, gapStart, layerWidth, yBottom, yTop, unit, slant, displacement, xDisplacement = self.layerMetrics(Layer)
				NSColor.redColor().colorWithAlphaComponent_(0.7).set() # set color to red
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
		except Exception as e:
			self.logToConsole( "drawGap: %s" % str(e) )
	
	@objc.python_method
	def background( self, Layer ):
		try:
			self.drawGrid(Layer)
			self.drawGap(Layer)
		except Exception as e:
			self.logToConsole( "background: %s" % str(e) )
	
	@objc.python_method
	def inactiveLayerBackground( self, Layer ):
		try:
			self.drawGap(Layer)
		except Exception as e:
			self.logToConsole( "inactiveLayerBackground: %s" % str(e) )
			

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
