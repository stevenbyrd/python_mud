from EventModule import EventReceiver
from EventModule import EventHandler
import threading

class Exit(EventReceiver):
	def __init__(self):
		EventReceiver.__init__(self)
		attributes = {
			'name'			: '',
			'destinateion'	: '',
			'isHidden'		: False
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]





class Universe(EventReceiver):
	def __init__(self):
		EventReceiver.__init__()
		attributes = {
			'worlds' : []
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]





class World(EventReceiver):
	def __init__(self):
		EventReceiver.__init__(self)
		attributes = {
			'rooms' : []
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
	
		playerInHandler		= EventHandler()
		playerOutHandler	= EventHandler()
		playerLogoutHandler	= EventHandler()
		
		playerInHandler.attributes['signature']	= 'player_entered'
		playerInHandler.attributes['function']	= self.addPlayer

		playerOutHandler.attributes['signature']	= 'player_exited'	
		playerOutHandler.attributes['function']		= self.removePlayer
		
		
		playerLogoutHandler.attributes['signature']	= 'player_logout'
		playerLogoutHandler.attributes['function']	= self.removePlayer
		
		self.addEventHandler(playerInHandler)
		self.addEventHandler(playerOutHandler)
		self.addEventHandler(playerLogoutHandler)
		

	def addPlayer(self, event):
		player		= event.attributes['data']['player']
		playerList	= self.attributes['players']
		
		self.attributes['playerSemaphore'].acquire()
		
		if player not in set(playerList):			
			for player in playerList:
				player.receiveEvent(event)
				
			playerList.append(player)
			
		self.attributes['playerSemaphore'].release()


	def removePlayer(self, event):
		player		= event.attributes['data']['player']
		playerList	= self.attributes['players']
		
		self.attributes['playerSemaphore'].acquire()
		
		if player in set(playerList):
			playerList.remove(player)
			
			if event.attributes['signature'] == 'player_exited':
				for player in playeList:
					player.receiveEvent(event)
				
		self.attributes['playerSemaphore'].release()
