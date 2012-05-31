from EventModule import *
from EngineModule import *
import EngineModule
import threading
import ANSI

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
	
		playerInHandler		= EventHandler()
		playerOutHandler	= EventHandler()
		playerLogoutHandler	= EventHandler()
		actorMoveHandler	= EventHandler()
		
		playerInHandler.attributes['signature']		= 'player_entered'
		playerInHandler.attributes['function']		= self.addPlayer

		playerOutHandler.attributes['signature']	= 'actor_exited'	
		playerOutHandler.attributes['function']		= self.removeActor
		
		playerLogoutHandler.attributes['signature']	= 'player_logout'
		playerLogoutHandler.attributes['function']	= self.removeActor
		
		actorMoveHandler.attributes['signature']	= 'actor_move'
		actorMoveHandler.attributes['function']		= self.moveActor
		
		self.addEventHandler(playerInHandler)
		self.addEventHandler(playerOutHandler)
		self.addEventHandler(playerLogoutHandler)
		self.addEventHandler(actorMoveHandler)
		
		
	def moveActor(self, event):
		actor		= event.attributes['data']['source']
		direction	= event.attributes['data']['direction']
		exit		= None
		
		if direction != None and direction != '':
			for e in self.attributes['exits']:
				if e.attributes['name'].startswith(direction):
					exit = e
					break
		
		if exit == None:
			if actor.attributes['actorID'] == '0':
				actor.sendFinal(ANSI.yellow('You can\'t go that way!'))
		else:			
			currentRoom									= self.attributes['roomID']
			destination 								= exit.attributes['destination']
			moveEvent									= Event()
			moveEvent.attributes['signature']			= 'move_actor'
			moveEvent.attributes['data']['actor']		= actor
			moveEvent.attributes['data']['fromRoomID']	= currentRoom
			moveEvent.attributes['data']['toRoomID']	= destination
			moveEvent.attributes['data']['exitMessage']	= '{} leaves {}.'.format(actor.attributes['name'], exit.attributes['name'])
			
			EngineModule.roomEngine.receiveEvent(moveEvent)


	def addPlayer(self, event):
		player		= event.attributes['data']['player']
		playerList	= self.attributes['players']
		
		self.attributes['playerSemaphore'].acquire()
		
		if player not in set(playerList):			
			for p in playerList:
				p.receiveEvent(event)
				
			playerList.append(player)
			
			player.attributes['roomID'] = self.attributes['roomID']

		self.attributes['playerSemaphore'].release()


	def removeActor(self, event):
		actor		= event.attributes['data']['actor']
		playerList	= self.attributes['players']
		
		self.attributes['playerSemaphore'].acquire()
		
		if actor in set(playerList):
			playerList.remove(actor)
			
		if event.attributes['signature'] == 'actor_exited':
			message = event.attributes['data']['exitMessage']
			
			if message != None and message != '':
				for p in playerList:
					p.sendFinal(message)

		self.attributes['playerSemaphore'].release()