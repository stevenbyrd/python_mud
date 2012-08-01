from Engine import Engine


def addEventSubscriber(subscriber):
	if RoomEngine.instance != None:
		RoomEngine.instance.addEventSubscriber(subscriber)
	else:
		RoomEngine.subscribers.append(subscriber)
	

def emitEvent(event):
	RoomEngine.instance.emitEvent(event)


def getRoom(roomID):
	return RoomEngine.instance.getRoom(roomID)


class RoomEngine(Engine):
	instance	= None
	subscribers = []
	
	def __init__(self):
		import Driver.ConnectionListUpdater
		import CommandEngine
		
		Engine.__init__(self)
		
		attributes = {
			'roomMap'	: {},
			'roomList'	: []
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
		
		self.addEventHandlerByNameWithAdjusters('Engine.EventHandlers.RoomEngine.PlayerLoginEventHandler', None)
		self.addEventHandlerByNameWithAdjusters('Engine.EventHandlers.RoomEngine.PlayerLogoutEventHandler', None)
		
		RoomEngine.instance = self
		
		for subscriber in RoomEngine.subscribers:
			self.addEventSubscriber(subscriber)
			
		RoomEngine.subscribers = []
		
		self.buildWorld()
		
		Driver.ConnectionListUpdater.addEventSubscriber(self)
		CommandEngine.addEventSubscriber(self)
		
	
	def buildWorld(self):
		from Environment.Room import Room
		from Environment.Exit import Exit
		import os
		import json

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

