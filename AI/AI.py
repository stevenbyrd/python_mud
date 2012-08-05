from Event.EventReceiver import EventReceiver
from Event.Event import Event

class AI(EventReceiver):
	def __init__(self, aiJson, owner):
		EventReceiver.__init__(self)
		
		self.attributes['current_state']	= 'idle'
		self.attributes['next_state']		= None
		self.attributes['owner']			= owner
		
		if aiJson != None:
			for key in aiJson.keys():
				if key == 'eventHandlers':					
					for element in aiJson[key]:		
						adjusters = (lambda dictionary: dictionary.has_key('adjusters') and dictionary['adjusters'] or None)(element)
						
						self.addEventHandlerByNameWithAdjusters(element['name'], adjusters)
				else:
					self.attributes[key] = aiJson[key]
		
	
	def receiveEvent(self, event, emitter):
		if event.attributes['signature'] == 'game_tick':
			self.attributes['tick_count'] += 1
		
		filterFunc = (lambda receiver: receiver.attributes['signature'] == event.attributes['signature'])
	
		for handler in filter(filterFunc, self.attributes['event_handlers']):
			newEvent = Event()
		
			newEvent.attributes = {
				'signature'		: event.attributes['signature'],
				'data'			: event.attributes['data'].copy(),
				'flags'			: event.attributes['flags'][:],
				'receiver'		: self,
				'event_target'	: None
			}
			
			handler.receiveEvent(newEvent)
			
		if self.attributes['next_state'] != None:
			self.attributes['current_state']	= self.attributes['next_state']
			self.attributes['next_state']		= None