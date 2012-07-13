from lib.BaseClass import BaseClass
import copy
from Event import Event
import os
import json
from Adjustments.Adjuster import Adjuster

currentDir = os.getcwd()

class EventReceiver:
	def __init__(self):
		BaseClass.__init__(self)
		
		self.attributes['event_handlers']	= []
		self.attributes['event_adjusters']	= []
	
	
	def addEventHandler(self, handler):
		self.attributes['event_handlers'].append(handler)
		
	
	def addEventAdjuster(self, adjusterName):
		filePath		= '{}/Content/eventAdjusters/{}.txt'.format(currentDir, adjusterName)
		adjusterFile	= open(filePath, 'r')
		jsonString		= adjusterFile.read()
		jsonObj			= json.loads(jsonString)
		adjuster		= Adjuster(jsonObj)
		
		adjusterFile.close()		
		
		self.attributes['event_adjusters'].append(adjuster)
	
	
	def receiveEvent(self, event, emitter):
		filterFunc	= (lambda receiver: receiver.attributes['signature'] == event.attributes['signature'])
		newEvent	= Event()
		
		newEvent.attributes = {
			'signature'	: event.attributes['signature'],
			'data'		: event.attributes['data'].copy()
		}
	
		for adjuster in filter(filterFunc, self.attributes['event_adjusters']):
			newEvent = adjuster.adjust(newEvent)
		
			if newEvent == None:
				break
		
		if newEvent != None:
			for handler in filter(filterFunc, self.attributes['event_handlers']):
					handler.attributes['function'](self, newEvent)			