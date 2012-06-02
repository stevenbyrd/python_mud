import threading
from time import sleep
from Event.Event import Event
from Engine import ConnectionEngine
from Engine import RoomEngine
from Engine import ActorEngine

class ConnectionListUpdater(threading.Thread):
	def run(self):
		while True:			
			ConnectionEngine.lock('openConnectionsSemaphore')
			ConnectionEngine.lock('openConnectionsSemaphore')
			ConnectionEngine.lock('openConnectionsSemaphore')
	
			self.removeClosedConnections()
			self.addNewConnections()
	
			ConnectionEngine.release('openConnectionsSemaphore')
			ConnectionEngine.release('openConnectionsSemaphore')
			ConnectionEngine.release('openConnectionsSemaphore')
			
			sleep(0.5)
			
	
	def addNewConnections(self):
		ConnectionEngine.lock('newConnectionSemaphore')
		
		for connection in ConnectionEngine.attribute('newConnections'):
			player									= connection.attributes['player']
			loginEvent								= Event()
			loginEvent.attributes['signature']		= 'player_login'
			loginEvent.attributes['data']['player'] = player

			RoomEngine.receiveEvent(loginEvent)
			
			ConnectionEngine.attribute('connectionList').append(connection)
			
			playerName												= player.attributes['name']
			loginNotificationEvent									= Event()
			loginNotificationEvent.attributes['signature']			= 'broadcast_to_all_players'
			loginNotificationEvent.attributes['data']['message']	= '{} just logged in.'.format(playerName)
		
			ActorEngine.receiveEvent(loginNotificationEvent)
		
		ConnectionEngine.setAttribute('newConnections', [])
		
		ConnectionEngine.release('newConnectionSemaphore')
		
		
	def removeClosedConnections(self):
		ConnectionEngine.lock('closedConnectionSemaphore')
		
		for connection in ConnectionEngine.attribute('closedConnections'):
			ConnectionEngine.attribute('connectionList').remove(connection)
			connection.attributes['socket'].close()
			
			player													= connection.attributes['player']
			playerName												= player.attributes['name']
			logoutNotificationEvent									= Event()
			logoutNotificationEvent.attributes['signature']			= 'broadcast_to_all_players'
			logoutNotificationEvent.attributes['data']['message']	= '{} logged off.'.format(playerName)
		
			ActorEngine.receiveEvent(logoutNotificationEvent)
		
		ConnectionEngine.setAttribute('closedConnections', [])
		
		ConnectionEngine.release('closedConnectionSemaphore')