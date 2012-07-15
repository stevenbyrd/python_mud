from Event.Event import Event
from Event.EventHandler import EventHandler
from Engine import Engine
import CommandEngine
import ActorEngine
from Environment.Room import Room
from Environment.Exit import Exit
import Driver.ConnectionListUpdater
import os
import json


def addEventSubscriber(subscriber):
	RoomEngine.instance.addEventSubscriber(subscriber)
	

def emitEvent(event):
	RoomEngine.instance.emitEvent(event)


def getRoom(roomID):
	return RoomEngine.instance.getRoom(roomID)


class RoomEngine(Engine):
	instance = None
	
	def __init__(self):
		Engine.__init__(self)
		
		attributes = {
			'roomMap'	: {},
			'roomList'	: []
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
		
		self.attributes['event_handlers'].append(PlayerLoginEventHandler())
		self.attributes['event_handlers'].append(RoomEnginePlayerLogoutEventHandler())
		
		RoomEngine.instance = self
		
		self.buildWorld()
		
		Driver.ConnectionListUpdater.addEventSubscriber(self)
		CommandEngine.addEventSubscriber(self)
		
	
	def buildWorld(self):
		currentDir	= os.getcwd()
		worldDir	= currentDir + '/Content/world' 
		fileList	= os.listdir(worldDir)
		
		for fname in fileList:			
			if fname.endswith('.txt'):
				filePath	= '{}/{}'.format(worldDir, fname)
				roomFile	= open(filePath, 'r')
				jsonString	= roomFile.read()
				jsonObj		= json.loads(jsonString)
				room		= Room(jsonObj)
				
				roomFile.close()
				
				self.attributes['roomList'].append(room)
				self.attributes['roomMap'][room.attributes['roomID']] = room

	
	
	def getRoom(self, roomID):
		return self.attributes['roomMap'][roomID]




class PlayerLoginEventHandler:
	def __init__(self):
		self.attributes = {'signature':'player_login'}

	def handleEvent(self, event):
		receiver		= event.attributes['receiver']
		player			= event.attributes['data']['player']
		roomID			= player.attributes['roomID']
		room			= receiver.getRoom(roomID)
		playerInEvent	= Event()

		playerInEvent.attributes['signature']		= 'actor_added_to_room'
		playerInEvent.attributes['data']['actor']	= player
		playerInEvent.attributes['data']['room']	= room

		receiver.emitEvent(playerInEvent)




class RoomEnginePlayerLogoutEventHandler:
	def __init__(self):
		self.attributes = {'signature':'player_logout'}

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		connection	= event.attributes['data']['connection']
		player		= connection.attributes['player']
		roomID		= player.attributes['roomID']
		room		= receiver.getRoom(roomID)
		logoutEvent = Event()

		logoutEvent.attributes['signature']				= 'player_logout'
		logoutEvent.attributes['data']['actor']			= player
		logoutEvent.attributes['data']['exitMessage']	= None

		receiver.emitEvent(logoutEvent)