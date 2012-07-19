from Event.EventReceiver import EventReceiver
from Event.EventEmitter import EventEmitter
from lib import ANSI


class Actor(EventReceiver, EventEmitter):
	def __init__(self, actorJSON):
		import Engine.RoomEngine
		import Engine.ActorEngine
		from Inventory.ActorInventory import ActorInventory
		import EventHandlers.Actor

		EventReceiver.__init__(self)
		EventEmitter.__init__(self)
		
		attributes = {
			'actorID'		: '',
			'uniqueID'		: '',
			'name'			: '',
			'description'	: [],
			'race'			: 'Human',
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
			'eventHandlers'	: [],
			'inventory'		: None
		}
		
		if actorJSON != None:
			for key in actorJSON.keys():
				if key == 'inventory':
					inventory		= ActorInventory(actorJSON[key], self)
					attributes[key]	= inventory
				else:
					attributes[key] = actorJSON[key]
		
			for key in attributes.keys():
				self.attributes[key] = attributes[key]
			
			if self.attributes['inventory'] == None:
				self.attributes['inventory'] = ActorInventory(None, self)
		
			Engine.ActorEngine.addEventSubscriber(self)
		
			startingRoom = Engine.RoomEngine.getRoom(self.attributes['roomID'])
		
			startingRoom.addEventSubscriber(self)
			
			for key in self.attributes['eventAdjusters']:
				adjusters = self.attributes['eventAdjusters'][key]
			
				for adjusterName in adjusters:
					self.addCustomEventAdjuster(key, adjusterName)
				
		
			for key in self.attributes['eventHandlers']:
				handlers = self.attributes['eventHandlers'][key]
			
				for handlerName in handlers:
					self.addCustomEventHandler(key, handlerName)
				
			self.addEventHandler(EventHandlers.Actor.ActorAttemptedDropHandler())
			self.addEventHandler(EventHandlers.Actor.ItemDroppedHandler())
			self.addEventHandler(EventHandlers.Actor.ActorInitiatedItemGrabHandler())
			self.addEventHandler(EventHandlers.Actor.ActorGrabbedItemHandler())
			self.addEventHandler(EventHandlers.Actor.ActorAttemptedItemEquipHandler())
			self.addEventHandler(EventHandlers.Actor.ActorAttemptedItemRemovalHandler())
			self.addEventHandler(EventHandlers.Actor.ActorMovedFromRoomEventHandler())
	
	
	def getDescription(self):
		description = [ANSI.yellow('You see {} the {}.'.format(self.attributes['name'], self.attributes['race']))]
		
		if len(self.attributes['description']) > 0:
			
			for line in self.attributes['description']:
				description.append(ANSI.cyan(line))
			
		equipment = self.attributes['inventory'].listEquipment()
		
		if len(equipment) > 0:
			description = description + equipment
			
		return description
			
		