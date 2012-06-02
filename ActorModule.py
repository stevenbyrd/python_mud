import time
import lib.ANSI
from EventHandlers.PlayerEventHandlersModule import *

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
			
		self.addEventHandler(WasObservedHandler())
		
		
		
		
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
		
		self.addEventHandler(ActorEnteredRoomHandler())
		self.addEventHandler(ReceivedNotificationHandler())
		self.addEventHandler(EntityDescribedSelfHandler())
		self.addEventHandler(ReceivedFeedbackHandler())
		self.addEventHandler(ActorEmotedHandler())
				
		
	def send(self, message):
		self.attributes['connection'].send(message) 
		
	
	def sendFinal(self, message):
		self.attributes['connection'].sendFinal('\n\r' + message)
		
		
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