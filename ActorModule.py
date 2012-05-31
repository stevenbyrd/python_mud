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
		
		playerInHandler.attributes['signature']			= 'player_entered'
		playerInHandler.attributes['function']			= self.playerEnteredRoom
		
		notificationHandler.attributes['signature']		= 'receive_notification'
		notificationHandler.attributes['function']		= self.receiveNotification
		
		entityDescribedHandler.attributes['signature']	= 'entity_described_self'
		entityDescribedHandler.attributes['function']	= self.entityDescribedSelf
		
		self.addEventHandler(playerInHandler)
		self.addEventHandler(notificationHandler)
		self.addEventHandler(entityDescribedHandler)
		
		
	def entityDescribedSelf(self, event):
		for line in event.attributes['data']['description']:
			self.send(line)
			
		self.sendFinal(event.attributes['data']['lastLine'])
		
		
		
	def receiveNotification(self, event):
		message			= event.attributes['data']['message']
		notification	= ANSI.yellow('### {} '.format(message))

		self.sendFinal(notification)
		
		
	def playerEnteredRoom(self, event):
		player	= event.attributes['data']['player']
		name	= player.attributes['name']
		
		self.sendFinal('{} just arrived.'.format(name))
		
		
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