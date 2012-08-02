from lib.BaseClass import BaseClass

class EventEmitter(BaseClass):
	def __init__(self):
		BaseClass.__init__(self)
		self.attributes['subscribers'] = []

	
	def emitEvent(self, event):
		if event.attributes['event_target'] != None:
			subscriber = event.attributes['event_target']
			
			if subscriber in set(self.attributes['subscribers']):
				subscriber.receiveEvent(event, self)
		else:
			for subscriber in self.attributes['subscribers']:
				subscriber.receiveEvent(event, self)

	
	def addEventSubscriber(self, subscriber):
		if subscriber not in set(self.attributes['subscribers']):
			self.attributes['subscribers'].append(subscriber)

	
	def removeEventSubscriber(self, subscriber):
		if subscriber in set(self.attributes['subscribers']):
			self.attributes['subscribers'].remove(subscriber)