import os
import json
from EnvironmentModule import *
from ActorModule import *
from EventModule import *

import EnvironmentModule


class RoomEngine(EventReceiver):
	def __init__(self):
		EventReceiver.__init__(self)
		attributes = {
			'roomMap'	: {},
			'roomList'	: []
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
		
		playerLoginHandler = EventHandler()
		
		playerLoginHandler.attributes['signature']	= 'player_login'
		playerLoginHandler.attributes['function']	= self.playerLogin
		
		self.addEventHandler(playerLoginHandler)
		
	
	def buildWorld(self):
		currentDir	= os.getcwd()
		worldDir 	= currentDir + '/gameContent/world' 
		fileList	= os.listdir(worldDir)
		
		for fname in fileList:			
			if fname.endswith('.txt'):
				filePath	= '{}/{}'.format(worldDir, fname)
				roomFile	= open(filePath, 'r')
				jsonString	= roomFile.read()
				jsonObj		= json.loads(jsonString)
				room		= Room()
				
				roomFile.close()
				
				for key in jsonObj.keys():
					if key == 'exits':
						for exitJson in jsonObj[key]:
							exit = Exit()
							for field in exitJson.keys():
								exit.attributes[field] = exitJson[field]
							
							room.attributes[key].append(exit)
					else:
						room.attributes[key] = jsonObj[key]

				self.attributes['roomList'].append(room)
				self.attributes['roomMap'][room.attributes['roomID']] = room
	
	def getRoom(self, roomID):
		return self.attributes['roomMap'][roomID]
	
	def playerLogin(self, event):
		player 			= event.attributes['data']['player']
		roomID			= player.attributes['roomID']
		room			= self.getRoom(roomID)
		playerInEvent	= Event()
		
		playerInEvent.attributes['signature']		= 'player_entered'
		playerInEvent.attributes['data']['player']	= player
		
		room.receiveEvent(playerInEvent)
		




class ActorEngine(EventReceiver):
	def __init__(self):
		EventReceiver.__init__(self)
		attributes = {
			'playerMap'	: {},
			'npcMap'	: {}
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
	
		playerLoginHandler = EventHandler()

		playerLoginHandler.attributes['signature']	= 'player_login'
		playerLoginHandler.attributes['function']	= self.playerLogin

		self.addEventHandler(playerLoginHandler)
	
	
	def playerLogin(self, event):
		print 'player logged in!'
		
	def loadPlayer(self, playerName):
		currentDir	= os.getcwd()
		filePath 	= '{}/gameContent/players/{}.txt'.format(currentDir, playerName) 
		playerFile	= open(filePath, 'r')
		jsonString	= playerFile.read()
		jsonObj		= json.loads(jsonString)
		player		= Player()
		
		playerFile.close()
		
		for key in jsonObj.keys():
			player.attributes[key] = jsonObj[key]
			
		player.attributes['roomID'] = '0'

		self.attributes['playerMap'][player.attributes['actorID']] = player
		
		return player
		
		
	def playerExists(self, playerName):
		try:
			currentDir	= os.getcwd()
			filePath 	= '{}/gameContent/players/{}.txt'.format(currentDir, playerName)
			print filePath
			open(filePath, 'r')
			
			return True
		except IOError as e:
			return False