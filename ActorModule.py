import time
import ANSI
from EventModule import *

class Actor(EventReceiver):
	def __init__(self):
		EventReceiver.__init__(self)
		attributes = {
			'actorID'		: '',
			'uniqueID'		: '',
			'name'			: '',
			'description'	: [],
			'race'			: '',
			'gender'		: '',
			'roomID'		: '',
			'stats'			: {
									'strength'		: 0,
									'constitution'	: 0,
									'agility'		: 0,
									'energy'		: 0,
									'focus'			: 0,
									'awareness'		: 0
			},
			'currentHP'		: 0,
			'maxHP'			: 0,
			'currentMana'	: 0,
			'maxMana'		: 0
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
			
		wasLookedAtHandler							= EventHandler()
		wasLookedAtHandler.attributes['signature']	= 'was_observed'
		wasLookedAtHandler.attributes['function']	= self.wasObserved
		
		self.addEventHandler(wasLookedAtHandler)
			
			
	def wasObserved(self, event):
		observer										= event.attributes['data']['observer']
		description										= self.attributes['description'][:]
		describeEvent									= Event()
		describeEvent.attributes['signature']			= 'entity_described_self'
		describeEvent.attributes['data']['description'] = description

		observer.receiveEvent(describeEvent)
		
		
		
		
class Humanoid(Actor):
	def __init__(self):
		Actor.__init__(self)





class Player(Humanoid):
	def __init__(self):
		Humanoid.__init__(self)
		attributes = {
			'connection' : None
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
		
		playerInHandler			= EventHandler()
		notificationHandler		= EventHandler()
		entityDescribedHandler	= EventHandler()
		feedbackHandler			= EventHandler()
		actorSpokeHandler		= EventHandler()
		
		playerInHandler.attributes['signature']			= 'player_entered'
		playerInHandler.attributes['function']			= self.playerEnteredRoom
		
		notificationHandler.attributes['signature']		= 'receive_notification'
		notificationHandler.attributes['function']		= self.receivedNotification
		
		entityDescribedHandler.attributes['signature']	= 'entity_described_self'
		entityDescribedHandler.attributes['function']	= self.entityDescribedSelf
		
		feedbackHandler.attributes['signature']			= 'received_feedback'
		feedbackHandler.attributes['function']			= self.receivedFeedback
		
		actorSpokeHandler.attributes['signature']		= 'actor_spoke'
		actorSpokeHandler.attributes['function']		= self.actorSpoke
		
		self.addEventHandler(playerInHandler)
		self.addEventHandler(notificationHandler)
		self.addEventHandler(entityDescribedHandler)
		self.addEventHandler(feedbackHandler)
		self.addEventHandler(actorSpokeHandler)
		
		
	def actorSpoke(self, event):
		speaker		= event.attributes['data']['speaker']
		sentence	= event.attributes['data']['sentence']
		
		if speaker == self:
			sentence = 'You say{}'.format(sentence)
		else:
			sentence = '\n{} says{}'.format(speaker.attributes['name'], sentence)
		
		self.sendFinal(sentence)
		
		
	def entityDescribedSelf(self, event):
		description = event.attributes['data']['description']
		
		if len(description) > 0:
			if len(description) == 1:
				self.sendFinal('\n{}\n'.format(description[0]))
			else:
				self.send('\n{}\n'.format(description[0]))
		
				if len(description) == 2:
					self.sendFInal('{}\n'.format(description[1]))
				else:
					for line in description[1:-1]:
						self.send('{}\n'.format(line))
					
					self.sendFinal('{}\n'.format(description[-1]))
		
		
		
	def receivedNotification(self, event):
		message			= event.attributes['data']['message']
		notification	= ANSI.yellow('\n### {} '.format(message))

		self.sendFinal(notification)
		
		
	def playerEnteredRoom(self, event):
		player	= event.attributes['data']['player']
		name	= player.attributes['name']
		
		self.sendFinal('\n{} just arrived.'.format(name))
		
		
	def receivedFeedback(self, event):
		feedback = event.attributes['data']['feedback']

		self.sendFinal('\n{}'.format(feedback))
		
		
	def send(self, message):
		self.attributes['connection'].send(message) 
		
	
	def sendFinal(self, message):
		self.attributes['connection'].sendFinal(message)
		
		
	def insertCommand(self, command):
		self.attributes['connection'].attributes['inputBuffer'].append(command)
		
	
	


class NPC(Actor):
	def __init__(self):
		Actor.__init__(self)
		attributes = {
			'wanderRate'	: 0,
			'spawnRate'		: 0,
			'numberInRoom'	: 0,
			'minimumWait'	: 5000,
			'spawnTime'		: '',
			'pluralName'	: ''
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]