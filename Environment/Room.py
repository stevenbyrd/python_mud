from Event.EventReceiver import EventReceiver
from Event.EventEmitter import EventEmitter
from Event.Event import Event
import Engine.ActorEngine


class Room(EventReceiver, EventEmitter):
	def __init__(self, roomJson):
		import threading
		from Exit import Exit
		import Engine.RoomEngine
		from Inventory.RoomInventory import RoomInventory
		from SpawnTemplate import SpawnTemplate
		
		EventReceiver.__init__(self)
		
		attributes = {
			'playerSemaphore'	: threading.BoundedSemaphore(1),
			'roomID'			: '',
			'name'				: '',
			'description'		: [],
			'exits'				: [],
			'players'			: [],
			'npcs'				: [],
			'spawnableNPCs'		: [],
			'inventory'			: None,
			'spawnTemplates'	: []
		}
		
		out_adjusters	= []
		inventory		= None
		spawnTemplates	= None
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
			
		for key in roomJson.keys():
			if key == 'exits':
				for exitJson in roomJson[key]:
					exit = Exit()
					for field in exitJson.keys():
						exit.attributes[field] = exitJson[field]
					
					self.attributes[key].append(exit)
			elif key == 'eventHandlers':
				for element in roomJson[key]:
					adjusters = (lambda dictionary: dictionary.has_key('adjusters') and dictionary['adjusters'] or None)(element)
					
					self.addEventHandlerByNameWithAdjusters(element['name'], adjusters)
			elif key == 'inventory':
				inventory = roomJson[key]
			elif key == 'spawnTemplates':
				spawnTemplates = roomJson[key]
			elif key == 'out_adjusters':
				out_adjusters = roomJson[key]
			else:
				self.attributes[key] = roomJson[key]
		
		self.addEventHandlerByNameWithAdjusters('Environment.EventHandlers.Room.ActorAttemptedMovementEventHandler', None)
		self.addEventHandlerByNameWithAdjusters('Environment.EventHandlers.Room.ActorMovedFromRoomEventHandler', None)
		self.addEventHandlerByNameWithAdjusters('Environment.EventHandlers.Room.ActorAddedToRoomEventHandler', None)
		self.addEventHandlerByNameWithAdjusters('Environment.EventHandlers.Room.ActorObservedHandler', None)
		self.addEventHandlerByNameWithAdjusters('Environment.EventHandlers.Room.WasObservedHandler', None)
		self.addEventHandlerByNameWithAdjusters('Environment.EventHandlers.Room.ActorEmotedHandler', None)
		self.addEventHandlerByNameWithAdjusters('Environment.EventHandlers.Room.PlayerLogoutHandler', None)
		self.addEventHandlerByNameWithAdjusters('Environment.EventHandlers.Room.SpellCastAttempted', None)
		self.addEventHandlerByNameWithAdjusters('Environment.EventHandlers.Room.ActorAttemptedItemGrabHandler', None)
		self.addEventHandlerByNameWithAdjusters('Environment.EventHandlers.Room.ActorGrabbedItemHandler', None)
		self.addEventHandlerByNameWithAdjusters('Environment.EventHandlers.Room.ItemDroppedHandler', None)
		
		Engine.RoomEngine.addEventSubscriber(self)
		
		EventEmitter.__init__(self, out_adjusters)
		
		if inventory != None:
			self.attributes['inventory'] = RoomInventory(inventory, self)
		else:
			self.attributes['inventory'] = RoomInventory(None, self)
			
		if spawnTemplates != None:
			for template in spawnTemplates:
				spawnTemplate = SpawnTemplate(template, self)
					
				self.attributes['spawnTemplates'].append(spawnTemplate)
		
		
		
	def removePlayer(self, player):
		playerList = self.attributes['players']

		self.attributes['playerSemaphore'].acquire()

		if player in set(playerList):
			playerList.remove(player)

		self.attributes['playerSemaphore'].release()



	def addPlayer(self, player):
		playerList	= self.attributes['players']

		self.attributes['playerSemaphore'].acquire()

		if player not in set(playerList):			
			playerList.append(player)
			player.attributes['roomID'] = self.attributes['roomID']
			
			commandEvent									= Event()
			commandEvent.attributes['signature']			= 'execute_command'
			commandEvent.attributes['data']['command']		= 'look'
			commandEvent.attributes['data']['args']			= []
			commandEvent.attributes['data']['source']		= player
	
			Engine.ActorEngine.emitEvent(commandEvent)

		self.attributes['playerSemaphore'].release()
		
		
		
	def removeNPC(self, npc):
		npcList = self.attributes['npcs']

		if npc in set(npcList):
			npcList.remove(npc)



	def addNPC(self, npc):
		npcList = self.attributes['npcs']

		if npc not in set(npcList):
			npcList.append(npc)