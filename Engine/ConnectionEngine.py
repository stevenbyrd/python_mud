from Engine import Engine


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
		from Driver import LoginListener
		import threading
		import CommandEngine
		
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


		self.addEventHandlerByNameWithAdjusters('Engine.EventHandlers.ConnectionEngine.PlayerLoginHandler', None)
		self.addEventHandlerByNameWithAdjusters('Engine.EventHandlers.ConnectionEngine.PlayerLogoutHandler', None)
		
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
		