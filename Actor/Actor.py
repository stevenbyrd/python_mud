from Event.Event import Event
from Event.EventHandler import EventHandler
from Event.EventReceiver import EventReceiver

class Actor(EventReceiver):
	def __init__(self):
		EventReceiver.__init__(self)
		attributes = {
			'actorID'		: '',
			'uniqueID'		: '',
			'name'			: '',
			'description'	: [],
			'race'			: '',
			'gender'		: '',
			'roomID'		: '',
			'stats'			: {
									'strength'		: 0,
									'constitution'	: 0,
									'agility'		: 0,
									'energy'		: 0,
									'focus'			: 0,
									'awareness'		: 0
			},
			'currentHP'		: 0,
			'maxHP'			: 0,
			'currentMana'	: 0,
			'maxMana'		: 0
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
			
		self.addEventHandler(WasObservedEventHandler())
		
	
	
		
		
class WasObservedEventHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'was_observed'
		self.attributes['function']		= self.wasObserved


	def wasObserved(self, receiver, event):
			observer										= event.attributes['data']['observer']
			description										= receiver.attributes['description'][:]
			describeEvent									= Event()
			describeEvent.attributes['signature']			= 'entity_described_self'
			describeEvent.attributes['data']['description'] = description

			observer.receiveEvent(describeEvent)