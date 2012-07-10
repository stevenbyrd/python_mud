from Event.EventReceiver import EventReceiver
from Event.EventEmitter import EventEmitter

class Exit(EventReceiver, EventEmitter):
	def __init__(self):
		EventReceiver.__init__(self)
		EventEmitter.__init__(self)
		
		attributes = {
			'name'			: '',
			'destination'	: '',
			'isHidden'		: False
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]