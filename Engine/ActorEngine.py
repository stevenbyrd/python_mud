from Engine import Engine
from Actor.Player import Player
from Actor.NPC import NPC
import os
import json


currentDir = os.getcwd()


def emitEvent(event):
	ActorEngine.instance.emitEvent(event)


def addEventSubscriber(subscriber):
	if ActorEngine.instance != None:
		ActorEngine.instance.addEventSubscriber(subscriber)
	else:
		ActorEngine.subscribers.append(subscriber)


def playerExists(playerName):
	return ActorEngine.instance.playerExists(playerName)
	
	
def loadPlayer(playerName):
	return ActorEngine.instance.loadPlayer(playerName)
	
	
def loadNPC(npcID):
	return ActorEngine.instance.loadNPC(npcID)


class ActorEngine(Engine):
	instance 	= None
	subscribers = []
	
	def __init__(self):
		Engine.__init__(self)
		
		import CommandEngine
		import threading
		import Driver.ConnectionListUpdater
		
		attributes = {
			'playerSetSemaphore'	: threading.BoundedSemaphore(1),
			'playerMap'				: {},
			'playerList'			: [],
			'npcMap'				: {}
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
			
		ActorEngine.instance = self
	
		self.addEventHandlerByNameWithAdjusters('Engine.EventHandlers.ActorEngine.PlayerLoginEventHandler', None)
		self.addEventHandlerByNameWithAdjusters('Engine.EventHandlers.ActorEngine.PlayerLogoutEventHandler', None)
		self.addEventHandlerByNameWithAdjusters('Engine.EventHandlers.ActorEngine.BroadcastEventHandler', None)
		
		
		for subscriber in ActorEngine.subscribers:
			self.addEventSubscriber(subscriber)
			
		ActorEngine.subscribers = []
		
		
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
		filePath	= '{}/Content/players/{}.txt'.format(currentDir, playerName) 
		playerFile	= open(filePath, 'r')
		jsonString	= playerFile.read()
		jsonObj		= json.loads(jsonString)
		player		= Player(jsonObj)
		
		playerFile.close()
		
		return player
		
		
	def loadNPC(self, npcId):
		filePath	= '{}/Content/npc/{}.txt'.format(currentDir, npcId) 
		npcFile		= open(filePath, 'r')
		jsonString	= npcFile.read()
		jsonObj		= json.loads(jsonString)
		npc			= NPC(jsonObj)
		
		npcFile.close()
		
		return npc
		
		
	def playerExists(self, playerName):
		try:
			currentDir	= os.getcwd()
			filePath	= '{}/Content/players/{}.txt'.format(currentDir, playerName)

			open(filePath, 'r')
			
			return True
		except:
			return False
			
			




		