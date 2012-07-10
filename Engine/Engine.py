from Event.EventReceiver import EventReceiver
from Event.EventEmitter import EventEmitter


class Engine(EventReceiver, EventEmitter):	
	def __init__(self):
		EventReceiver.__init__(self)
		EventEmitter.__init__(self)