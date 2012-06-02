from Event.Event import Event
from Event.EventHandler import EventHandler
from Event.EventReceiver import EventReceiver
from Environment.Room import Room
from Environment.Exit import Exit
import os
import json

def receiveEvent(event):
	RoomEngine.instance.receiveEvent(event)
	

def getRoom(roomID):
	return RoomEngine.instance.getRoom(roomID)


class RoomEngine(EventReceiver):
	instance = None
	
	
	def __init__(self):
		EventReceiver.__init__(self)
		attributes = {
			'roomMap'	: {},
			'roomList'	: []
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
				
		
		self.addEventHandler(PlayerLoginEventHandler())
		self.addEventHandler(RoomEnginePlayerLogoutEventHandler())
		self.addEventHandler(ActorMovedEventHandler())
		
		RoomEngine.instance = self
		
		self.buildWorld()
		
	
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
	
	
	def getRoom(self, roomID):
		return self.attributes['roomMap'][roomID]
		
		
		
		
class ActorMovedEventHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)

		self.attributes['signature']	= 'move_actor'
		self.attributes['function']		= self.moveActor


	def moveActor(self, receiver, event):
		actor			= event.attributes['data']['actor']
		fromRoomID		= event.attributes['data']['fromRoomID']
		destinID		= event.attributes['data']['toRoomID']
		exitMessage		= event.attributes['data']['exitMessage']
		source			= receiver.getRoom(fromRoomID)
		destination		= receiver.getRoom(destinID)

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

		playerInEvent.attributes['signature']		= 'player_entered'
		playerInEvent.attributes['data']['player']	= player

		room.receiveEvent(playerInEvent)






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

		room.receiveEvent(logoutEvent)