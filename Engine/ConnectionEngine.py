from Event.Event import Event
from Event.EventHandler import EventHandler
from Engine import Engine
import CommandEngine
from Driver import LoginListener
import threading


def lock(semaphoreName):
	ConnectionEngine.instance.attributes[semaphoreName].acquire()
	
	
def release(semaphoreName):
	ConnectionEngine.instance.attributes[semaphoreName].release()
	

def attribute(attribute):
	return ConnectionEngine.instance.attributes[attribute]
	
def setAttribute(attribute, value):
	ConnectionEngine.instance.attributes[attribute] = value


class ConnectionEngine(Engine):
	instance = None
	
	def __init__(self):
		Engine.__init__(self)
		attributes = {
			'openConnectionsSemaphore'	: threading.BoundedSemaphore(3),
			'newConnectionSemaphore'	: threading.BoundedSemaphore(1),
			'closedConnectionSemaphore' : threading.BoundedSemaphore(1),
			'connectionList'			: [],
			'newConnections'			: [],
			'closedConnections'			: []
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]

		self.addEventHandler(PlayerLoginHandler())
		self.addEventHandler(PlayerLogoutHandler())
		
		ConnectionEngine.instance = self
		
		LoginListener.addEventSubscriber(self)
		CommandEngine.addEventSubscriber(self)
	
	
	def addConnection(self, connection):
		self.attributes['newConnectionSemaphore'].acquire()
		self.attributes['newConnections'].append(connection)
		self.attributes['newConnectionSemaphore'].release()
	
	
	def removeConnection(self, connection):
		self.attributes['closedConnectionSemaphore'].acquire()
		self.attributes['closedConnections'].append(connection)
		self.attributes['closedConnectionSemaphore'].release()
		
		



class PlayerLoginHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'player_login'
		self.attributes['function']		= self.playerLogin


	def playerLogin(self, receiver, event):
		player		= event.attributes['data']['player']
		connection	= player.attributes['connection']

		receiver.addConnection(connection)





class PlayerLogoutHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'player_logout'
		self.attributes['function']		= self.playerLogout


	def playerLogout(self, receiver, event):
		connection = event.attributes['data']['connection']

		receiver.removeConnection(connection)