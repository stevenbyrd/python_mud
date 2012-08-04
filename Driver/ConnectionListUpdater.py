import threading
from time import sleep
from Event.Event import Event
import Engine.ConnectionEngine
import Engine.RoomEngine
import Engine.ActorEngine
from Event.EventEmitter import EventEmitter


def addEventSubscriber(subscriber):
	ConnectionListUpdater.instance.addEventSubscriber(subscriber)
	
	
def removeEventSubscriber(subscriber):
	ConnectionListUpdater.instance.removeEventSubscriber(subscriber)


class ConnectionListUpdater(threading.Thread, EventEmitter):
	instance = None
	
	
	def __init__(self):
		threading.Thread.__init__(self)
		EventEmitter.__init__(self, None)
	
		ConnectionListUpdater.instance = self
		
	
	def run(self):
		while True:			
			Engine.ConnectionEngine.lock('openConnectionsSemaphore')
			Engine.ConnectionEngine.lock('openConnectionsSemaphore')
			Engine.ConnectionEngine.lock('openConnectionsSemaphore')
	
			self.removeClosedConnections()
			self.addNewConnections()
	
			Engine.ConnectionEngine.release('openConnectionsSemaphore')
			Engine.ConnectionEngine.release('openConnectionsSemaphore')
			Engine.ConnectionEngine.release('openConnectionsSemaphore')
			
			sleep(0.5)
			
	
	def addNewConnections(self):
		Engine.ConnectionEngine.lock('newConnectionSemaphore')
		
		for connection in Engine.ConnectionEngine.attribute('newConnections'):
			player									= connection.attributes['player']
			loginEvent								= Event()
			loginEvent.attributes['signature']		= 'player_login'
			loginEvent.attributes['data']['player'] = player

			self.emitEvent(loginEvent)
			
			Engine.ConnectionEngine.attribute('connectionList').append(connection)
			
			playerName												= player.attributes['name']
			loginNotificationEvent									= Event()
			loginNotificationEvent.attributes['signature']			= 'broadcast_to_all_players'
			loginNotificationEvent.attributes['data']['message']	= '{} just logged in.'.format(playerName)
		
			self.emitEvent(loginNotificationEvent)
		
		Engine.ConnectionEngine.setAttribute('newConnections', [])
		
		Engine.ConnectionEngine.release('newConnectionSemaphore')
		
		
	def removeClosedConnections(self):
		Engine.ConnectionEngine.lock('closedConnectionSemaphore')
		
		for connection in Engine.ConnectionEngine.attribute('closedConnections'):
			Engine.ConnectionEngine.attribute('connectionList').remove(connection)
			
			connection.attributes['socket'].close()
			
			player													= connection.attributes['player']
			playerName												= player.attributes['name']
			logoutNotificationEvent									= Event()
			logoutNotificationEvent.attributes['signature']			= 'broadcast_to_all_players'
			logoutNotificationEvent.attributes['data']['message']	= '{} logged off.'.format(playerName)
		
			self.emitEvent(logoutNotificationEvent)
		
		Engine.ConnectionEngine.setAttribute('closedConnections', [])
		
		Engine.ConnectionEngine.release('closedConnectionSemaphore')