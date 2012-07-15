from Event.Event import Event
from Event.EventHandler import EventHandler
from Engine import Engine
import CommandEngine
from Actor.Player import Player
import Driver.ConnectionListUpdater
import threading
import os
import json


def emitEvent(event):
	ActorEngine.instance.emitEvent(event)

def addEventSubscriber(subscriber):
	ActorEngine.instance.addEventSubscriber(subscriber)


def playerExists(playerName):
	return ActorEngine.instance.playerExists(playerName)
	
	
def loadPlayer(playerName):
	return ActorEngine.instance.loadPlayer(playerName)


class ActorEngine(Engine):
	instance = None
	
	def __init__(self):
		Engine.__init__(self)
		attributes = {
			'playerSetSemaphore'	: threading.BoundedSemaphore(1),
			'playerMap'				: {},
			'playerList'			: [],
			'npcMap'				: {}
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
	
		self.attributes['event_handlers'].append(PlayerLoginEventHandler())
		self.attributes['event_handlers'].append(PlayerLogoutEventHandler())
		self.attributes['event_handlers'].append(BroadcastEventHandler())
		
		ActorEngine.instance = self
		
		Driver.ConnectionListUpdater.addEventSubscriber(self)
		CommandEngine.addEventSubscriber(self)
		
		
	def addPlayer(self, player):
		self.attributes['playerSetSemaphore'].acquire();
		
		playerID								= player.attributes['uniqueID']
		self.attributes['playerMap'][playerID]	= player
		
		self.attributes['playerList'].append(player)
		
		self.attributes['playerSetSemaphore'].release();
		
		
	def removePlayer(self, player):
		self.attributes['playerSetSemaphore'].acquire();
		
		playerID = player.attributes['uniqueID']
		
		if self.attributes['playerMap'].has_key(playerID):
			del self.attributes['playerMap'][playerID]
		
		if player in set(self.attributes['playerList']):
			self.attributes['playerList'].remove(player)
		
		self.attributes['playerSetSemaphore'].release();
	
		
	def loadPlayer(self, playerName):
		currentDir	= os.getcwd()
		filePath	= '{}/Content/players/{}.txt'.format(currentDir, playerName) 
		playerFile	= open(filePath, 'r')
		jsonString	= playerFile.read()
		jsonObj		= json.loads(jsonString)
		player		= Player(jsonObj)
		
		playerFile.close()
		
		return player
		
		
	def playerExists(self, playerName):
		try:
			currentDir	= os.getcwd()
			filePath	= '{}/Content/players/{}.txt'.format(currentDir, playerName)

			open(filePath, 'r')
			
			return True
		except:
			return False
			
			

class BroadcastEventHandler:
	def __init__(self):
		self.attributes = {'signature':'broadcast_to_all_players'}

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		receiver.attributes['playerSetSemaphore'].acquire();

		message											= event.attributes['data']['message']
		notificationEvent								= Event()
		notificationEvent.attributes['signature']		= 'received_notification'
		notificationEvent.attributes['data']['message'] = message
		notificationEvent.attributes['data']['actor']	= None

		receiver.emitEvent(notificationEvent)
		
		receiver.attributes['playerSetSemaphore'].release();





class PlayerLoginEventHandler:
	def __init__(self):
		self.attributes = {'signature' : 'player_login'}

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		player		= event.attributes['data']['player']

		receiver.addPlayer(player)






class PlayerLogoutEventHandler(EventHandler):
	def __init__(self):
		self.attributes = {'signature':'player_logout'}

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		connection	= event.attributes['data']['connection']
		player		= connection.attributes['player']

		receiver.removePlayer(player)


		