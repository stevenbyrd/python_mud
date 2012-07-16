from lib.BaseClass import BaseClass
import copy
from Event import Event
from EventHandler import EventHandler
import os
import json
from EventAdjuster import EventAdjuster
import Driver.TickDriver


currentDir = os.getcwd()


class EventReceiver:
	def __init__(self):
		BaseClass.__init__(self)
		
		self.attributes['event_handlers']	= []
		self.attributes['event_adjusters']	= []
		self.attributes['tick_count']		= 0
		
		Driver.TickDriver.addEventSubscriber(self)
		
		
	def addEventHandler(self, handler):
		if handler != None:
			self.attributes['event_handlers'].append(handler)
	
	
	
	def addCustomEventHandler(self, handlerType, handlerName):
		filePath	= '{}/Content/eventHandlers/{}/{}.txt'.format(currentDir, handlerType, handlerName)
		handlerFile	= open(filePath, 'r')
		jsonString	= handlerFile.read()
		jsonObj		= json.loads(jsonString)
		handler		= EventHandler(jsonObj)
		
		handlerFile.close()
		
		self.addEventHandler(handler)
		
	
	
	
	def addEventAdjuster(self, adjuster):
		if adjuster != None:
			self.attributes['event_adjusters'].append(adjuster)
	
	
	
	
	def addCustomEventAdjuster(self, adjusterType, adjusterName):
		filePath		= '{}/Content/eventAdjusters/{}/{}.txt'.format(currentDir, adjusterType, adjusterName)
		adjusterFile	= open(filePath, 'r')
		jsonString		= adjusterFile.read()
		jsonObj			= json.loads(jsonString)
		adjuster		= EventAdjuster(jsonObj)
		
		adjusterFile.close()		
		
		self.addEventAdjuster(adjuster)
		
		
	
	
	def receiveEvent(self, event, emitter):
		if event.attributes['signature'] == 'game_tick':
			self.attributes['tick_count'] += 1
		
		filterFunc	= (lambda receiver: receiver.attributes['signature'] == event.attributes['signature'])
		newEvent	= Event()
		
		newEvent.attributes = {
			'signature'	: event.attributes['signature'],
			'data'		: event.attributes['data'].copy(),
			'receiver'	: self
		}
	
		for adjuster in filter(filterFunc, self.attributes['event_adjusters']):
			adjuster.adjust(newEvent)
		
			if newEvent.attributes['signature'] == None:
				break
		
		if newEvent.attributes['signature'] != None:
			for handler in filter(filterFunc, self.attributes['event_handlers']):
					handler.handleEvent(newEvent)			