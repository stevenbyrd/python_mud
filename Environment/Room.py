from Event.EventReceiver import EventReceiver
from Event.EventEmitter import EventEmitter


class Room(EventReceiver, EventEmitter):
	def __init__(self, roomJson):
		import threading
		from Exit import Exit
		import Engine.RoomEngine
		import EventHandlers.Room
		from Inventory.RoomInventory import RoomInventory
		
		EventReceiver.__init__(self)
		EventEmitter.__init__(self)
		
		attributes = {
			'playerSemaphore'	: threading.BoundedSemaphore(1),
			'npcSemaphore'		: threading.BoundedSemaphore(1),
			'roomID'			: '',
			'name'				: '',
			'description'		: [],
			'exits'				: [],
			'players'			: [],
			'npcs'				: [],
			'spawnableNPCs'		: [],
			'updateRate'		: 0,
			'inventory'			: None
		}
		
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
				for handlerName in roomJson[key]:
					self.addCustomEventHandler('room', handlerName)
			elif key == 'eventAdjusters':
				for adjusterName in roomJson[key]:
					self.addCustomEventAdjuster('room', adjusterName)
			elif key == 'inventory':
				inventory = RoomInventory(roomJson[key], self)
				
				self.attributes[key] = inventory
			else:
				self.attributes[key] = roomJson[key]
		
		self.addEventHandler(EventHandlers.Room.ActorAttemptedMovementEventHandler())
		self.addEventHandler(EventHandlers.Room.ActorMovedFromRoomEventHandler())
		self.addEventHandler(EventHandlers.Room.ActorAddedToRoomEventHandler())
		self.addEventHandler(EventHandlers.Room.ActorObservedHandler())
		self.addEventHandler(EventHandlers.Room.WasObservedHandler())
		self.addEventHandler(EventHandlers.Room.ActorEmotedHandler())
		self.addEventHandler(EventHandlers.Room.PlayerLogoutHandler())
		self.addEventHandler(EventHandlers.Room.SpellCastAttempted())
		self.addEventHandler(EventHandlers.Room.ActorAttemptedItemGrabHandler())
		self.addEventHandler(EventHandlers.Room.ActorGrabbedItemHandler())
		self.addEventHandler(EventHandlers.Room.ItemDroppedHandler())
		
		Engine.RoomEngine.addEventSubscriber(self)
		
		
		
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
			player.insertCommand('look')

		self.attributes['playerSemaphore'].release()		