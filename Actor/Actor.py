from Event.Event import Event
from Event.EventHandler import EventHandler
from Event.EventReceiver import EventReceiver
from Event.EventEmitter import EventEmitter
import Engine.RoomEngine
import Engine.ActorEngine


class Actor(EventReceiver, EventEmitter):
	def __init__(self, actorJSON):
		EventReceiver.__init__(self)
		EventEmitter.__init__(self)
		
		attributes = {
			'actorID'		: '',
			'uniqueID'		: '',
			'name'			: '',
			'description'	: [],
			'race'			: '',
			'gender'		: '',
			'roomID'		: '0',
			'stats'			: {
									'strength'		: 0,	#physical skills, inventory limit
									'constitution'	: 0,	#combat tree, max hp
									'agility'		: 0,	#stealth tree, dodging
									'energy'		: 0,	#magic skills, max mana
									'focus'			: 0,	#psionic skills, mana regen
									'awareness'		: 0,	#traps tree, searching
									'ingenuity'		: 0,	#crafting tree, critical hits
									'composure'		: 0		#support tree, hp regen
			},
			'currentHP'		: 0,
			'maxHP'			: 0,
			'currentMana'	: 0,
			'maxMana'		: 0,
			'eventAdjusters': [],
			'eventHandlers'	: []
		}
		
		for key in actorJSON.keys():
			if attributes.has_key(key):
				attributes[key] = actorJSON[key]
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
		
		Engine.ActorEngine.addEventSubscriber(self)
		
		startingRoom = Engine.RoomEngine.getRoom(self.attributes['roomID'])
		
		startingRoom.addEventSubscriber(self)
		
		for adjusterName in self.attributes['eventAdjusters']:
			self.addEventAdjuster(adjusterName)
		
		for key in self.attributes['eventHandlers']:
			handlers = self.attributes['eventHandlers'][key]
			
			for handlerName in handlers:
				self.addEventHandler(key, handlerName)