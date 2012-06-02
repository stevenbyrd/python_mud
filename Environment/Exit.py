from Event.EventReceiver import EventReceiver

class Exit(EventReceiver):
	def __init__(self):
		EventReceiver.__init__(self)
		attributes = {
			'name'			: '',
			'destination'	: '',
			'isHidden'		: False
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]