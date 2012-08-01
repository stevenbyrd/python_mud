from Event.EventReceiver import EventReceiver
from Event.EventEmitter import EventEmitter
from lib import ANSI


class Actor(EventReceiver, EventEmitter):
	def __init__(self, actorJSON):
		import Engine.RoomEngine
		import Engine.ActorEngine
		from Inventory.ActorInventory import ActorInventory

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
			'eventAdjusters': {},
			'eventHandlers'	: {},
			'inventory'		: None
		}
		
		if actorJSON != None:
			for key in actorJSON.keys():
				if key == 'inventory':
					inventory		= ActorInventory(actorJSON[key], self)
					attributes[key]	= inventory
				elif key == 'eventHandlers':					
					for category in actorJSON[key].keys():
						for element in actorJSON[key][category]:		
							adjusters = (lambda dictionary: dictionary.has_key('adjusters') and dictionary['adjusters'] or None)(element)
							
							self.addEventHandlerByNameWithAdjusters('Actor.EventHandlers.{}.{}'.format(category, element['name']), adjusters)
				else:
					attributes[key] = actorJSON[key]
		
			for key in attributes.keys():
				self.attributes[key] = attributes[key]
			
			if self.attributes['inventory'] == None:
				self.attributes['inventory'] = ActorInventory(None, self)
		
			Engine.ActorEngine.addEventSubscriber(self)
		
			startingRoom = Engine.RoomEngine.getRoom(self.attributes['roomID'])
		
			startingRoom.addEventSubscriber(self)
				
			self.addEventHandlerByNameWithAdjusters('Actor.EventHandlers.Actor.ActorAttemptedDropHandler', None)
			self.addEventHandlerByNameWithAdjusters('Actor.EventHandlers.Actor.ItemDroppedHandler', None)
			self.addEventHandlerByNameWithAdjusters('Actor.EventHandlers.Actor.ActorInitiatedItemGrabHandler', None)
			self.addEventHandlerByNameWithAdjusters('Actor.EventHandlers.Actor.ActorGrabbedItemHandler', None)
			self.addEventHandlerByNameWithAdjusters('Actor.EventHandlers.Actor.ActorAttemptedItemEquipHandler', None)
			self.addEventHandlerByNameWithAdjusters('Actor.EventHandlers.Actor.ActorAttemptedItemRemovalHandler', None)
			self.addEventHandlerByNameWithAdjusters('Actor.EventHandlers.Actor.ActorMovedFromRoomEventHandler', None)
	
	
	def getDescription(self):
		description = [ANSI.yellow('You see {} the {}.'.format(self.attributes['name'], self.attributes['race']))]
		
		if len(self.attributes['description']) > 0:
			for line in self.attributes['description']:
				description.append(ANSI.cyan(line))
			
		equipment = self.attributes['inventory'].listEquipment()
		
		if len(equipment) > 0:
			description = description + equipment
			
		return description
			
		