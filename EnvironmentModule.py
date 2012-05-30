from EventModule import EventReceiver
from EventModule import EventHandler

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
			'roomID'		: '',
			'name'			: '',
			'description'	: [],
			'exits'			: [],
			'players'		: [],
			'npcs'			: [],
			'spawnableNPCs'	: [],
			'updateRate'	: 0
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
	
		playerInHandler		= EventHandler()
		playerOutHandler	= EventHandler()
	
		playerInHandler.attributes['signature']		= 'player_entered'
		playerOutHandler.attributes['signature']	= 'player_exited'
		
		playerInHandler.attributes['function']	= self.addPlayer
		playerOutHandler.attributes['function']	= self.removePlayer
		
		self.addEventHandler(playerInHandler)
		self.addEventHandler(playerOutHandler)
		

	def addPlayer(self, event):
		data		= event.attributes['data']
		player		= data['player']
		playerList	= self.attributes['players']
		
		if player not in set(playerList):
			playerList.append(player)
			
			for player in playerList:
				player.receiveEvent(event)


	def removePlayer(self, event):
		data		= event.attributes['data']
		player		= data['player']
		playerList	= self.attributes['players']
		
		if player in set(playerList):
			playerList.remove(player)
			
			for player in playeList:
				player.receiveEvent(event)
