from Event.EventReceiver import EventReceiver
from Event.EventEmitter import EventEmitter
import Engine.ActorEngine


class SpawnTemplate(EventReceiver, EventEmitter):
	def __init__(self, templateJson, room):
		import EventHandlers.SpawnTemplate
		
		EventReceiver.__init__(self)
		EventEmitter.__init__(self, None)
		
		attributes = {
			'npcID'		: '',
			'npcs'		: [],
			'wanderRate'	: .5,
			'spawnRate'	: .5,
			'room'		: room
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
			
		for key in templateJson.keys():
			if key == 'eventHandlers':
				for element in templateJson[key]:
					adjusters = (lambda dictionary: dictionary.has_key('adjusters') and dictionary['adjusters'] or None)(element)
					
					self.addEventHandlerByNameWithAdjusters(element['name'], adjusters)
			else:
				self.attributes[key] = templateJson[key]
		
		room.addEventSubscriber(self)
