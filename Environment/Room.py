from Event.Event import Event
from Event.EventHandler import EventHandler
from Event.EventReceiver import EventReceiver
from Event.EventEmitter import EventEmitter
import Engine.CommandEngine
import Engine.RoomEngine
import threading
from lib import ANSI


class Room(EventReceiver, EventEmitter):
	def __init__(self):
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
			'updateRate'		: 0
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
		
		
		self.addEventHandler(ActorAttemptedMovementEventHandler())
		self.addEventHandler(ActorMovedFromRoomEventHandler())
		self.addEventHandler(ActorAddedToRoomEventHandler())
		self.addEventHandler(ActorEmotedHandler())
		self.addEventHandler(ActorObservedHandler())
		self.addEventHandler(WasObservedHandler())
		self.addEventHandler(EntityDescribedSelfEventHandler())
		self.addEventHandler(PlayerLogoutHandler())
		
		
		
		
		Engine.RoomEngine.addEventSubscriber(self)
		Engine.CommandEngine.addSubscriberForCommand("look", self)
		Engine.CommandEngine.addSubscriberForCommand("emote", self)
		Engine.CommandEngine.addSubscriberForCommand("go", self)
		Engine.CommandEngine.addSubscriberForCommand("say", self)
		
		
		
	def removePlayer(self, player):
		playerList = self.attributes['players']

		self.attributes['playerSemaphore'].acquire()

		if player in set(playerList):
			playerList.remove(player)
			player.removeEventSubscriber(self)

		self.attributes['playerSemaphore'].release()


	def addPlayer(self, player):
		playerList	= self.attributes['players']

		self.attributes['playerSemaphore'].acquire()

		if player not in set(playerList):			
			playerList.append(player)
			player.attributes['roomID'] = self.attributes['roomID']
			player.insertCommand('look')
			player.addEventSubscriber(self)

		self.attributes['playerSemaphore'].release()
		
		
		
		
		
class ActorAttemptedMovementEventHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'actor_attempted_movement'
		self.attributes['function']		= self.actorAttemptedMovement


	def actorAttemptedMovement(self, receiver, event):
		if event.attributes['data']['room'] == receiver:
			actor		= event.attributes['data']['source']
			direction	= event.attributes['data']['direction']
			exit		= None
		
			if direction == '':
				feedbackEvent									= Event()
				feedbackEvent.attributes['signature']			= 'received_feedback'
				feedbackEvent.attributes['data']['feedback']	= 'Go where?'
				feedbackEvent.attributes['data']['actor']		= actor
		
				receiver.emitEvent(feedbackEvent)

			else:
				if direction != None:
					exitList = filter(lambda e : 
											e.attributes['name'].lower().startswith(direction.lower()), 
										receiver.attributes['exits'])

					if len(exitList) > 0:
						exit = exitList[0]

				if exit == None:
					feedbackEvent									= Event()
					feedbackEvent.attributes['signature']			= 'received_feedback'
					feedbackEvent.attributes['data']['feedback']	= ANSI.yellow('You can\'t go that way!')
					feedbackEvent.attributes['data']['actor']		= actor

					receiver.emitEvent(feedbackEvent)

				else:			
					currentRoom									= receiver.attributes['roomID']
					destination									= exit.attributes['destination']
			
					#send event to RoomEngine, which sends MovedFrom and MovedTo events targeted to the relavent rooms
					moveEvent									= Event()
					moveEvent.attributes['signature']			= 'actor_moved'
					moveEvent.attributes['data']['actor']		= actor
					moveEvent.attributes['data']['fromRoomID']	= currentRoom
					moveEvent.attributes['data']['toRoomID']	= destination
					moveEvent.attributes['data']['exit']		= exit
			
					receiver.emitEvent(moveEvent)




class ActorMovedFromRoomEventHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'actor_moved_from_room'
		self.attributes['function']		= self.actorMovedFromRoom


	def actorMovedFromRoom(self, receiver, event):		
		if event.attributes['data']['room'] == receiver:
			actor = event.attributes['data']['actor']
			
			receiver.removePlayer(actor)
			



class ActorAddedToRoomEventHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'actor_added_to_room'
		self.attributes['function']		= self.actorAddedToRoom	


	def actorAddedToRoom(self, receiver, event):		
		if event.attributes['data']['room'] == receiver:
			actor = event.attributes['data']['actor']
			
			receiver.addPlayer(actor)

			
			
			
class ActorEmotedHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'actor_emoted'
		self.attributes['function']		= self.actorEmoted

	def actorEmoted(self, receiver, event):
		if event.attributes['data']['room'] == receiver:
			targetName	= event.attributes['data']['target']
			target		= None
			playerList	= filter(lambda player: 
									player != event.attributes['data']['emoter'],
								receiver.attributes['players'])

			if targetName != None and targetName != '':
				targetList	= filter(lambda player : 
										player.attributes['name'].lower().startswith(targetName.lower()),
									 playerList)

				if len(targetList) > 0:
					target = targetList[0]
				else:
					emoter											= event.attributes['data']['emoter']
					feedbackEvent									= Event()
					feedbackEvent.attributes['signature']			= 'received_feedback'
					feedbackEvent.attributes['data']['feedback']	= 'You don\'t see that here.'

					receiver.emitEvent(feedbackEvent)

					return

			event.attributes['data']['target'] = target	

			receiver.emitEvent(event)





class ActorObservedHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'actor_observed'
		self.attributes['function']		= self.actorObserved


	def actorObserved(self, receiver, event):
		if event.attributes['data']['room'] == receiver:			
			observer	= event.attributes['data']['observer']
			target		= event.attributes['data']['target']
			targetList	= filter(lambda actor : 
									actor.attributes['name'].lower().startswith(target.lower()), 
								receiver.attributes['players'])

			if len(targetList) == 0:
				feedbackEvent									= Event()
				feedbackEvent.attributes['signature']			= 'received_feedback'
				feedbackEvent.attributes['data']['feedback']	= 'You don\'t see that here.'
				feedbackEvent.attributes['data']['actor']		= observer

				receiver.emitEvent(feedbackEvent)
			else:
				lookEvent									= Event()
				lookEvent.attributes['data']['observer']	= observer
				lookEvent.attributes['data']['target']		= targetList[0]
				lookEvent.attributes['signature']			= 'was_observed'

				receiver.emitEvent(lookEvent)





class WasObservedHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'was_observed'
		self.attributes['function']		= self.wasObserved


	def wasObserved(self, receiver, event):
		if event.attributes['data']['room'] == receiver:		
			player		= event.attributes['data']['observer']
			description = [ANSI.red(receiver.attributes['name']) + '\n\r']
			exitList	= 'Obvious exits:'
			playerList	= filter(lambda p: p != player, receiver.attributes['players'])

			for line in receiver.attributes['description']:
				description.append(line)

			for exit in receiver.attributes['exits']:
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
			describeEvent.attributes['data']['observer']	= player

			receiver.emitEvent(describeEvent)
		
		
		
		
class EntityDescribedSelfEventHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'entity_described_self'
		self.attributes['function']		= self.entityDescribedSelf


	def entityDescribedSelf(self, receiver, event):
		receiver.emitEvent(event)
		
		


class PlayerLogoutHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'player_logout'
		self.attributes['function']		= self.playerExited		


	def playerExited(self, receiver, event):
		actor = event.attributes['data']['actor']

		receiver.removePlayer(actor)
