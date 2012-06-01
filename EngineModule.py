import os
import json
import threading
import EnvironmentModule
import ConnectionModule
from ConnectionModule import *
from EnvironmentModule import *
from ActorModule import *
from EventModule import *
from CommandModule import *


class RoomEngine(EventReceiver):
	def __init__(self):
		EventReceiver.__init__(self)
		attributes = {
			'roomMap'	: {},
			'roomList'	: []
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
		
		playerLoginHandler	= EventHandler()
		playerLogoutHandler = EventHandler()
		actorMoveHandler	= EventHandler()
		
		playerLoginHandler.attributes['signature']	= 'player_login'
		playerLoginHandler.attributes['function']	= self.playerLogin
		
		playerLogoutHandler.attributes['signature'] = 'player_logout'
		playerLogoutHandler.attributes['function']	= self.playerLogout
		
		actorMoveHandler.attributes['signature']	= 'move_actor'
		actorMoveHandler.attributes['function']		= self.moveActor
		
		self.addEventHandler(playerLoginHandler)
		self.addEventHandler(playerLogoutHandler)
		self.addEventHandler(actorMoveHandler)
		
	
	def buildWorld(self):
		currentDir	= os.getcwd()
		worldDir	= currentDir + '/gameContent/world' 
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
		
		
	def moveActor(self, event):
		actor			= event.attributes['data']['actor']
		fromRoomID		= event.attributes['data']['fromRoomID']
		destinID		= event.attributes['data']['toRoomID']
		exitMessage		= event.attributes['data']['exitMessage']
		source			= self.getRoom(fromRoomID)
		destination		= self.getRoom(destinID)
		
		# send exit event to the room the actor is leaving
		exitEvent									= Event()
		exitEvent.attributes['signature']			= 'actor_exited'
		exitEvent.attributes['data']['actor']		= actor
		exitEvent.attributes['data']['exitMessage'] = exitMessage
		
		source.receiveEvent(exitEvent)
		
		# send entered event to destination room
		enterEvent								= Event()
		enterEvent.attributes['signature']		= 'player_entered'
		enterEvent.attributes['data']['player'] = actor
		
		destination.receiveEvent(enterEvent)									
		
		
	
	def playerLogin(self, event):
		player			= event.attributes['data']['player']
		roomID			= player.attributes['roomID']
		room			= self.getRoom(roomID)
		playerInEvent	= Event()
		
		playerInEvent.attributes['signature']		= 'player_entered'
		playerInEvent.attributes['data']['player']	= player
		
		room.receiveEvent(playerInEvent)
	
	
	def playerLogout(self, event):
		connection	= event.attributes['data']['connection']
		player		= connection.attributes['player']
		roomID		= player.attributes['roomID']
		room		= self.getRoom(roomID)
		logoutEvent = Event()
		
		logoutEvent.attributes['signature']				= 'player_logout'
		logoutEvent.attributes['data']['actor']			= player
		logoutEvent.attributes['data']['exitMessage']	= None

		room.receiveEvent(logoutEvent)




class ActorEngine(EventReceiver):
	def __init__(self):
		EventReceiver.__init__(self)
		attributes = {
			'playerSetSemaphore'	: threading.BoundedSemaphore(1),
			'playerMap'				: {},
			'playerList'			: [],
			'npcMap'				: {}
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
	
		playerLoginHandler	= EventHandler()
		playerLogoutHandler = EventHandler()
		broadcastHandler	= EventHandler()

		playerLoginHandler.attributes['signature']	= 'player_login'
		playerLoginHandler.attributes['function']	= self.playerLogin
		
		playerLogoutHandler.attributes['signature'] = 'player_logout'
		playerLogoutHandler.attributes['function']	= self.playerLogout
		
		broadcastHandler.attributes['signature']	= 'broadcast_to_all_players'
		broadcastHandler.attributes['function']		= self.broadcastToAllPlayers

		self.addEventHandler(playerLoginHandler)
		self.addEventHandler(playerLogoutHandler)
		self.addEventHandler(broadcastHandler)
		
		
	def broadcastToAllPlayers(self, event):
		self.attributes['playerSetSemaphore'].acquire();

		message											= event.attributes['data']['message']
		notificationEvent								= Event()
		notificationEvent.attributes['signature']		= 'receive_notification'
		notificationEvent.attributes['data']['message'] = message
		
		
		for player in self.attributes['playerList']:
			player.receiveEvent(notificationEvent)

		self.attributes['playerSetSemaphore'].release();	
	
	
	def playerLogin(self, event):
		player = event.attributes['data']['player']
		
		self.addPlayer(player)
		
		
		
	def playerLogout(self, event):
		connection	= event.attributes['data']['connection']
		player		= connection.attributes['player']
		
		self.removePlayer(player)
		
		
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
		filePath	= '{}/gameContent/players/{}.txt'.format(currentDir, playerName) 
		playerFile	= open(filePath, 'r')
		jsonString	= playerFile.read()
		jsonObj		= json.loads(jsonString)
		player		= Player()
		
		playerFile.close()
		
		for key in jsonObj.keys():
			player.attributes[key] = jsonObj[key]
			
		player.attributes['roomID'] = '0'
		
		return player
		
		
	def playerExists(self, playerName):
		try:
			currentDir	= os.getcwd()
			filePath	= '{}/gameContent/players/{}.txt'.format(currentDir, playerName)

			open(filePath, 'r')
			
			return True
		except IOError as e:
			return False
			
			



class CommandEngine(EventReceiver):
	def __init__(self):
		EventReceiver.__init__(self)
		attributes = {
			'commandList' : {}
		}

		for key in attributes.keys():
			self.attributes[key] = attributes[key]

		commandExecutionHandler = EventHandler()

		commandExecutionHandler.attributes['signature'] = 'execute_command'
		commandExecutionHandler.attributes['function']	= self.executeCommand

		self.addEventHandler(commandExecutionHandler)
		
		
	def executeCommand(self, event):
		cmdName = event.attributes['data']['command']
		
		if cmdName == 'quit':
			player											= event.attributes['data']['source']
			connection										= player.attributes['connection']
			logoutEvent										= Event()
			logoutEvent.attributes['signature']				= 'player_logout'
			logoutEvent.attributes['data']['connection']	= connection
			
			roomEngine.receiveEvent(logoutEvent)
			actorEngine.receiveEvent(logoutEvent)
			ConnectionModule.connectionList.receiveEvent(logoutEvent)
		else:
			commandList = self.attributes['commandList']
			command		= commandList['go']
			
			if commandList.has_key(cmdName):
				command = commandList[cmdName]
			
			command.receiveEvent(event)
	
	
	def buildCommandList(self):
		cmdList = self.attributes['commandList']
		
		cmdList['go']	= Go()
		cmdList['look']	= Look()
		cmdList['l']	= cmdList['look']
		cmdList['ls']	= cmdList['look']
		cmdList['say']	= Say()
		
		
		# EMOTES
		currentDir	= os.getcwd()
		emoteDir	= currentDir + '/gameContent/commands/emotes' 
		fileList	= os.listdir(emoteDir)

		for fname in fileList:			
			if fname.endswith('.txt'):
				filePath		= '{}/{}'.format(emoteDir, fname)
				emoteFile		= open(filePath, 'r')
				jsonString		= emoteFile.read()
				jsonObj			= json.loads(jsonString)
				emote			= Emote(jsonObj['template'])

				emoteFile.close()

				for cmdName in jsonObj['commandNames']:
					cmdList[cmdName] = emote
		