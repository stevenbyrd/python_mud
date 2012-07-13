import threading
from Event.Event import Event
from time import sleep
from Event.EventEmitter import EventEmitter


def addEventSubscriber(subscriber):
	TickDriver.instance.addEventSubscriber(subscriber)
	
	
def removeEventSubscriber(subscriber):
	TickDriver.instance.removeEventSubscriber(subscriber)


class TickDriver(threading.Thread, EventEmitter):
	instance = None
	
	def __init__(self):
		threading.Thread.__init__(self)
		EventEmitter.__init__(self)
		
		tickEvent							= Event()
		tickEvent.attributes['signature']	= 'game_tick'

		self.tickEvent						= tickEvent
		
		TickDriver.instance					= self
		
		
	def run(self):
		while True:
			self.emitEvent(self.tickEvent)
			
			sleep(1)