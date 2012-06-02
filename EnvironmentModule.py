from EventHandlers.EnvironmentEventHandlersModule import *
from EngineModule import *
import EngineModule
import threading
import lib.ANSI

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





class Room(EventReceiver):
	def __init__(self):
		EventReceiver.__init__(self)
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
			'updateRate'		: 0
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
		
		
		self.addEventHandler(PlayerEnteredHandler())
		self.addEventHandler(PlayerExitedHandler())
		self.addEventHandler(PlayerLogoutHandler())
		
		self.addEventHandler(ActorMovedHandler())
		self.addEventHandler(WasObservedHandler())
		self.addEventHandler(ActorObservedHandler())
		self.addEventHandler(ActorEmotedHandler())
		
		
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

