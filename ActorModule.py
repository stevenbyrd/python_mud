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
		actorEmoteHandler		= EventHandler()
		
		playerInHandler.attributes['signature']			= 'player_entered'
		playerInHandler.attributes['function']			= self.playerEnteredRoom
		
		notificationHandler.attributes['signature']		= 'receive_notification'
		notificationHandler.attributes['function']		= self.receivedNotification
		
		entityDescribedHandler.attributes['signature']	= 'entity_described_self'
		entityDescribedHandler.attributes['function']	= self.entityDescribedSelf
		
		feedbackHandler.attributes['signature']			= 'received_feedback'
		feedbackHandler.attributes['function']			= self.receivedFeedback
		
		actorEmoteHandler.attributes['signature']		= 'actor_emoted'
		actorEmoteHandler.attributes['function']		= self.actorEmoted
		
		self.addEventHandler(playerInHandler)
		self.addEventHandler(notificationHandler)
		self.addEventHandler(entityDescribedHandler)
		self.addEventHandler(feedbackHandler)
		self.addEventHandler(actorEmoteHandler)
		
		
	def actorEmoted(self, event):
		emoter	= event.attributes['data']['emoter']
		target	= event.attributes['data']['target']
		text	= None
		
		if emoter == self:
			text = event.attributes['data']['emoterText']
		elif target != None and target == self:
			text = event.attributes['data']['targetText']
		else:
			text = event.attributes['data']['audienceText']
		
		if text != None and text != '':
			text = text.replace('#emoter#', emoter.attributes['name'])

			if target != None:
				text = text.replace('#target#', target.attributes['name'])

			self.sendFinal(text)
		
		
	def entityDescribedSelf(self, event):
		description = event.attributes['data']['description']
		
		if len(description) > 0:
			if len(description) == 1:
				self.sendFinal('{}\n'.format(description[0]))
			else:
				self.send('\n{}\n'.format(description[0]))
		
				if len(description) == 2:
					self.sendFinal('{}\n'.format(description[1]))
				else:
					for line in description[1:-1]:
						self.send('{}\n'.format(line))
					
					self.attributes['connection'].sendFinal('{}\n'.format(description[-1]))
		
		
		
	def receivedNotification(self, event):
		message			= event.attributes['data']['message']
		notification	= ANSI.yellow('### {} '.format(message))

		self.sendFinal(notification)
		
		
	def playerEnteredRoom(self, event):
		player	= event.attributes['data']['player']
		name	= player.attributes['name']
		
		self.sendFinal('{} just arrived.'.format(name))
		
		
	def receivedFeedback(self, event):
		feedback = event.attributes['data']['feedback']

		self.sendFinal('{}'.format(feedback))
		
		
	def send(self, message):
		self.attributes['connection'].send(message) 
		
	
	def sendFinal(self, message):
		self.attributes['connection'].sendFinal('\n' + message)
		
		
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