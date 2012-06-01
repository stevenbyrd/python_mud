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
		playerLogoutHandler = EventHandler()
		actorMoveHandler	= EventHandler()
		wasLookedAtHandler	= EventHandler()
		actorObserveHandler	= EventHandler()
		actorSpokeHandler	= EventHandler()
		
		playerInHandler.attributes['signature']		= 'player_entered'
		playerInHandler.attributes['function']		= self.addPlayer

		playerOutHandler.attributes['signature']	= 'actor_exited'	
		playerOutHandler.attributes['function']		= self.removeActor
		
		playerLogoutHandler.attributes['signature'] = 'player_logout'
		playerLogoutHandler.attributes['function']	= self.removeActor
		
		actorMoveHandler.attributes['signature']	= 'actor_move'
		actorMoveHandler.attributes['function']		= self.moveActor
		
		wasLookedAtHandler.attributes['signature']	= 'was_observed'
		wasLookedAtHandler.attributes['function']	= self.wasObserved
		
		actorObserveHandler.attributes['signature']	= 'actor_observed'
		actorObserveHandler.attributes['function']	= self.actorObserved
		
		actorSpokeHandler.attributes['signature']	= 'actor_spoke'
		actorSpokeHandler.attributes['function']	= self.actorSpoke
		
		self.addEventHandler(playerInHandler)
		self.addEventHandler(playerOutHandler)
		self.addEventHandler(playerLogoutHandler)
		self.addEventHandler(actorMoveHandler)
		self.addEventHandler(wasLookedAtHandler)
		self.addEventHandler(actorObserveHandler)
		self.addEventHandler(actorSpokeHandler)


	def actorSpoke(self, event):
		for player in self.attributes['players']:
			player.receiveEvent(event)


	def actorObserved(self, event):
		observer	= event.attributes['data']['observer']
		target		= event.attributes['data']['target']
		targetList	= filter(lambda actor : 
								actor.attributes['name'].lower().startswith(target.lower()), 
							self.attributes['players'])
		
		if len(targetList) == 0:
			feedbackEvent									= Event()
			feedbackEvent.attributes['signature']			= 'received_feedback'
			feedbackEvent.attributes['data']['feedback']	= 'You don\'t see that here.'
			
			actor.receiveEvent(feedbackEvent)
		else:
			lookEvent									= Event()
			lookEvent.attributes['data']['observer']	= observer
			lookEvent.attributes['signature']			= 'was_observed'

			targetList[0].receiveEvent(lookEvent)
			
			
		
	def wasObserved(self, event):
		player		= event.attributes['data']['observer']
		description = [ANSI.red(self.attributes['name']) + '\n']
		exitList	= 'Obvious exits:'
		playerList	= filter(lambda p: p != player, self.attributes['players'])
		
		for line in self.attributes['description']:
			description.append(line)
		
		for exit in self.attributes['exits']:
			if exit.attributes['isHidden'] == False:
				exitList = exitList + ' ' + exit.attributes['name'] + ','
		
		if exitList == 'Obvious exits:':
			exitList = 'Obvious exits: none'

		if exitList.endswith(','):
			exitList = exitList[0:-1]
		
		description.append(ANSI.blue(exitList))
		
		if len(playerList) > 0:
			playerLine = 'Players:'
			
			for p in playerList:
				playerLine = playerLine + ' ' + p.attributes['name'] + ','
		
			if playerLine.endswith(','):
				playerLine = playerLine[0:-1]
				
			description.append(ANSI.green(playerLine))
		
		describeEvent									= Event()
		describeEvent.attributes['signature']			= 'entity_described_self'
		describeEvent.attributes['data']['description'] = description
		
		player.receiveEvent(describeEvent)
		
		
	def moveActor(self, event):
		actor		= event.attributes['data']['source']
		direction	= event.attributes['data']['direction']
		exit		= None
		
		if direction != None and direction != '':
			exitList = filter(lambda e : 
									e.attributes['name'].lower().startswith(direction.lower()), 
								self.attributes['exits'])
								
			if len(exitList) > 0:
				exit = exitList[0]
	
		
		if exit == None:
			feedbackEvent									= Event()
			feedbackEvent.attributes['signature']			= 'received_feedback'
			feedbackEvent.attributes['data']['feedback']	= ANSI.yellow('You can\'t go that way!')
			
			actor.receiveEvent(feedbackEvent)

		else:			
			currentRoom									= self.attributes['roomID']
			destination									= exit.attributes['destination']
			moveEvent									= Event()
			moveEvent.attributes['signature']			= 'move_actor'
			moveEvent.attributes['data']['actor']		= actor
			moveEvent.attributes['data']['fromRoomID']	= currentRoom
			moveEvent.attributes['data']['toRoomID']	= destination
			moveEvent.attributes['data']['exitMessage'] = '{} leaves {}.'.format(actor.attributes['name'], exit.attributes['name'])
			
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
			
			player.insertCommand('look')

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
					feedbackEvent									= Event()
					feedbackEvent.attributes['signature']			= 'received_feedback'
					feedbackEvent.attributes['data']['feedback']	= message

					p.receiveEvent(feedbackEvent)

		self.attributes['playerSemaphore'].release()