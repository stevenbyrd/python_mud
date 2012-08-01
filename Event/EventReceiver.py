from lib.BaseClass import BaseClass
import copy
from Event import Event
from EventHandler import EventHandler
import os
import json
from EventAdjuster import EventAdjuster
import Driver.TickDriver
import importlib

currentDir = os.getcwd()


class EventReceiver:
	def __init__(self):
		BaseClass.__init__(self)
		
		self.attributes['event_handlers']	= []
		self.attributes['tick_count']		= 0
		
		Driver.TickDriver.addEventSubscriber(self)
		
		
		
	
	def addEventHandlerByNameWithAdjusters(self, handlerName, adjusters):
		path		= handlerName.split('.')
		modulePath	= path[0]
	
		for step in path[1:-1]:
			modulePath = '{}.{}'.format(modulePath, step)
	
		handlerModule				= importlib.import_module(modulePath)
		handlerClass				= getattr(handlerModule, path[-1])
		handler						= handlerClass(adjusters)
		
		self.attributes['event_handlers'].append(handler)
	
	
	
	
	def receiveEvent(self, event, emitter):
		if event.attributes['signature'] == 'game_tick':
			self.attributes['tick_count'] += 1
		
		filterFunc	= (lambda receiver: receiver.attributes['signature'] == event.attributes['signature'])
	
		for handler in filter(filterFunc, self.attributes['event_handlers']):
			newEvent = Event()
		
			newEvent.attributes = {
				'signature'	: event.attributes['signature'],
				'data'		: event.attributes['data'].copy(),
				'receiver'	: self
			}
			
			handler.receiveEvent(newEvent)