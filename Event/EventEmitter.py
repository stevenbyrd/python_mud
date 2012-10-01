from lib.BaseClass import BaseClass
import importlib

class EventEmitter(BaseClass):				
	def __init__(self, out_adjusters):
		BaseClass.__init__(self)
		self.attributes['subscribers']	= []
		self.attributes['out_adjusters']	= []
		
		if out_adjusters != None:
			for adjusterJSON in out_adjusters:
				out_adjuster = self.loadAdjusterFromJSON(adjusterJSON)
		
				self.attributes['out_adjusters'].append(out_adjuster)


	def emitEvent(self, event):
		filterFunc = (lambda adjuster: adjuster.attributes['signature'] == event.attributes['signature'])
		
		for adjuster in filter(filterFunc, self.attributes['out_adjusters']):
			adjuster.adjustEvent(event)
			
			if event.attributes['signature'] == None:
				break
		
		if event.attributes['signature'] != None:
			for subscriber in self.attributes['subscribers'][:]:
				subscriber.receiveEvent(event, self)
				
	
	def addEventSubscriber(self, subscriber):
		if subscriber not in set(self.attributes['subscribers']):
			self.attributes['subscribers'].append(subscriber)

	
	def removeEventSubscriber(self, subscriber):
		if subscriber in set(self.attributes['subscribers']):
			self.attributes['subscribers'].remove(subscriber)
				
			
	def loadAdjusterFromJSON(self, adjusterJSON):
		adjusterName	= adjusterJSON['name']
		args			= (lambda dictionary : dictionary.has_key('args') and dictionary['args'] or None)(adjusterJSON)
		path			= adjusterName.split('.')
		modulePath		= path[0]

		for step in path[1:-1]:
			modulePath = '{}.{}'.format(modulePath, step)

		adjusterModule	= importlib.import_module(modulePath)
		adjusterClass	= getattr(adjusterModule, path[-1])
		adjuster		= adjusterClass(args)
		
		return adjuster