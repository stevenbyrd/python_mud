from Event.EventReceiver import EventReceiver
from Event.EventEmitter import EventEmitter
from lib import ANSI
import os
import json


currentDir = os.getcwd()


class Actor(EventReceiver, EventEmitter):
	def __init__(self, actorJSON):
		import Engine.RoomEngine
		import Engine.ActorEngine
		from Inventory.ActorInventory import ActorInventory
		from AI.AI import AI

		EventReceiver.__init__(self)
		
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
		
		out_adjusters	= []
		inventory		= None
		ai				= None
		
		if actorJSON != None:
			for key in actorJSON.keys():
				if key == 'inventory':
					inventory = actorJSON[key]
				elif key == 'eventHandlers':					
					for element in actorJSON[key]:		
						adjusters = (lambda dictionary: dictionary.has_key('adjusters') and dictionary['adjusters'] or None)(element)
						
						self.addEventHandlerByNameWithAdjusters(element['name'], adjusters)
				elif key == 'out_adjusters':
					out_adjusters = actorJSON[key]
				elif key == 'AI':
					ai = actorJSON[key]
				else:
					attributes[key] = actorJSON[key]
		
			for key in attributes.keys():
				self.attributes[key] = attributes[key]				
		
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
			self.addEventHandlerByNameWithAdjusters('Actor.EventHandlers.Actor.ActorGainedHealthFromTickHandler', None)
			
		#add event handlers specific to this actor's race
		
		filePath	= '{}/Content/races/{}.txt'.format(currentDir, self.attributes['race']) 
		raceFile	= open(filePath, 'r')
		jsonString	= raceFile.read()
		jsonObj		= json.loads(jsonString)
		handlers	= jsonObj['eventHandlers']
		
		if jsonObj.has_key('out_adjusters'):
			out_adjusters = out_adjusters + jsonObj['out_adjusters']

		raceFile.close()
		
		for handler in handlers:
			adjusters = (lambda dictionary: dictionary.has_key('adjusters') and dictionary['adjusters'] or None)(handler)
			
			self.addEventHandlerByNameWithAdjusters(handler['name'], adjusters)
			
		EventEmitter.__init__(self, out_adjusters)
		
		if inventory != None:
			self.attributes['inventory'] = ActorInventory(inventory, self)
		else:
			self.attributes['inventory'] = ActorInventory(None, self)
			
		if ai != None:
			self.attributes['AI'] = AI(ai, self)
	
	
	def getDescription(self):
		description = [ANSI.yellow('You see {} the {}.'.format(self.attributes['name'], self.attributes['race']))]
		
		if len(self.attributes['description']) > 0:
			for line in self.attributes['description']:
				description.append(ANSI.cyan(line))
			
		equipment = self.attributes['inventory'].listEquipment()
		
		if len(equipment) > 0:
			description = description + equipment
			
		return description
			
		