from Event.EventEmitter import EventEmitter

class Command(EventEmitter):
	def __init__(self):
		EventEmitter.__init__(self)