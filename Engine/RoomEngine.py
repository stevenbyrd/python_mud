from Event.Event import Event
from Event.EventHandler import EventHandler
from Engine import Engine
import CommandEngine
from Environment.Room import Room
from Environment.Exit import Exit
from Driver import ConnectionListUpdater
import os
import json


def addEventSubscriber(subscriber):
	RoomEngine.instance.addEventSubscriber(subscriber)


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
				
		
		self.addEventHandler(ActorMovedEventHandler())
		self.addEventHandler(PlayerLoginEventHandler())
		self.addEventHandler(RoomEnginePlayerLogoutEventHandler())
		
		
		RoomEngine.instance = self
		
		self.buildWorld()
		
		ConnectionListUpdater.addEventSubscriber(self)
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
				
				room.addEventSubscriber(self)
	
	
	def getRoom(self, roomID):
		return self.attributes['roomMap'][roomID]
		
		
		
		
class ActorMovedEventHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)

		self.attributes['signature']	= 'actor_moved'
		self.attributes['function']		= self.actorMoved


	def actorMoved(self, receiver, event):
		actor			= event.attributes['data']['actor']
		exit			= event.attributes['data']['exit']
		fromRoomID		= event.attributes['data']['fromRoomID']
		destinID		= event.attributes['data']['toRoomID']
		source			= receiver.getRoom(fromRoomID)
		destination		= receiver.getRoom(destinID)
		
		movedFromEvent								= Event()
		movedFromEvent.attributes['signature']		= 'actor_moved_from_room'
		movedFromEvent.attributes['data']['actor']	= actor
		movedFromEvent.attributes['data']['exit']	= exit
		movedFromEvent.attributes['data']['room']	= source
		
		receiver.emitEvent(movedFromEvent)
		
		movedToEvent								= Event()
		movedToEvent.attributes['signature']		= 'actor_added_to_room'
		movedToEvent.attributes['data']['actor']	= actor
		movedToEvent.attributes['data']['room']		= destination
		
		receiver.emitEvent(movedToEvent)




class PlayerLoginEventHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)

		self.attributes['signature']	= 'player_login'
		self.attributes['function']		= self.playerLogin


	def playerLogin(self, receiver, event):
		player			= event.attributes['data']['player']
		roomID			= player.attributes['roomID']
		room			= receiver.getRoom(roomID)
		playerInEvent	= Event()

		playerInEvent.attributes['signature']		= 'actor_added_to_room'
		playerInEvent.attributes['data']['actor']	= player
		playerInEvent.attributes['data']['room']	= room

		receiver.emitEvent(playerInEvent)






class RoomEnginePlayerLogoutEventHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)

		self.attributes['signature']	= 'player_logout'
		self.attributes['function']		= self.playerLogout


	def playerLogout(self, receiver, event):
		connection	= event.attributes['data']['connection']
		player		= connection.attributes['player']
		roomID		= player.attributes['roomID']
		room		= receiver.getRoom(roomID)
		logoutEvent = Event()

		logoutEvent.attributes['signature']				= 'player_logout'
		logoutEvent.attributes['data']['actor']			= player
		logoutEvent.attributes['data']['exitMessage']	= None

		receiver.emitEvent(logoutEvent)