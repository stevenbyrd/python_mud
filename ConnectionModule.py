from EngineModule import *
from EventModule import *
import EngineModule
import threading
import ANSI
import socket
from time import sleep
import select


class LoginListener(threading.Thread):
	def run(self):
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
		#hack to get my host name
		hostname	= socket.gethostname()
		
		try:
			tokenized	= hostname.split('.')
			hostname	= '{}.{}.{}.{}'.format(tokenized[3], tokenized[2], tokenized[1], tokenized[0])
		except:
			hostname = 'localhost'
		
		print socket.gethostname()
		print hostname
	
		serversocket.bind((hostname, 8888))
		serversocket.listen(5)
		
		while True:
			clientsocket = serversocket.accept()[0]
			
			clientsocket.setblocking(False)
						
			clientsocket.send('\nWelcome! Enter your name:\n')

			playerInput = ''

			while playerInput == '':
				try:
					playerInput = clientsocket.recv(1024)
				except:
					playerInput = ''

				if len(playerInput) > 0:
					playerInput = playerInput.strip()

					if EngineModule.actorEngine.playerExists(playerInput) == True:
						player		= EngineModule.actorEngine.loadPlayer(playerInput)				
						connection	= Connection(clientsocket, player)
						loginEvent	= Event()

						player.attributes['connection']			= connection
						loginEvent.attributes['signature']		= 'player_login'
						loginEvent.attributes['data']['player'] = player

						EngineModule.actorEngine.receiveEvent(loginEvent)
						connectionList.receiveEvent(loginEvent)
					else:
						clientsocket.send('\nPlayer not found.\nEnter your name:')

						playerInput = ''
				else:
					playerInput = ''		
			
			sleep(2)
	
	
	
	
	
class Connection:
	def __init__(self, socket, player):
		self.attributes = {
			'socket'		: socket,
			'player'		: player,
			'inputBuffer'	: [],
			'outputBuffer'	: []
		}
		
			
	def pollInput(self):
		buffer	= self.attributes['inputBuffer']
		retVal	= ''
		
		if len(buffer) > 0:
			retVal = buffer.pop(0)
		
		return retVal
		

	def send(self, message):
		self.attributes['outputBuffer'].append(message)


	def sendFinal(self, message):
		self.send(message)
		self.send(	ANSI.magenta('\n[') + 
					ANSI.yellow('HP: ') + ANSI.white(self.attributes['player'].attributes['currentHP']) + 
					ANSI.yellow(' Mana: ') + ANSI.white(self.attributes['player'].attributes['currentMana']) + 
					ANSI.magenta(']: '))
						
						
						


class ConnectionList(EventReceiver):
	def __init__(self):
		EventReceiver.__init__(self)
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
			
		playerLoginHandler	= EventHandler()
		playerLogoutHandler = EventHandler()

		playerLoginHandler.attributes['signature']	= 'player_login'
		playerLoginHandler.attributes['function']	= self.playerLogin
		
		playerLogoutHandler.attributes['signature'] = 'player_logout'
		playerLogoutHandler.attributes['function']	= self.playerLogout

		self.addEventHandler(playerLoginHandler)
		self.addEventHandler(playerLogoutHandler)
	
	
	def addConnection(self, connection):
		self.attributes['newConnectionSemaphore'].acquire()
		self.attributes['newConnections'].append(connection)
		self.attributes['newConnectionSemaphore'].release()
	
	
	def removeConnection(self, connection):
		self.attributes['closedConnectionSemaphore'].acquire()
		self.attributes['closedConnections'].append(connection)
		self.attributes['closedConnectionSemaphore'].release()
	
		
	def playerLogin(self, event):
		player		= event.attributes['data']['player']
		connection	= player.attributes['connection']
		
		self.addConnection(connection)
		
		
	def playerLogout(self, event):
		connection = event.attributes['data']['connection']
		
		self.removeConnection(connection)





class ConnectionListUpdater(threading.Thread):
	def run(self):
		while True:
			connectionList.attributes['openConnectionsSemaphore'].acquire()
			connectionList.attributes['openConnectionsSemaphore'].acquire()
			connectionList.attributes['openConnectionsSemaphore'].acquire()
		
			self.removeClosedConnections()
			self.addNewConnections()
		
			connectionList.attributes['openConnectionsSemaphore'].release()
			connectionList.attributes['openConnectionsSemaphore'].release()
			connectionList.attributes['openConnectionsSemaphore'].release()
			
			sleep(0.5)
			
	
	def addNewConnections(self):
		connectionList.attributes['newConnectionSemaphore'].acquire()
		
		for connection in connectionList.attributes['newConnections']:
			player									= connection.attributes['player']
			loginEvent								= Event()
			loginEvent.attributes['signature']		= 'player_login'
			loginEvent.attributes['data']['player'] = player

			EngineModule.roomEngine.receiveEvent(loginEvent)
			
			connectionList.attributes['connectionList'].append(connection)
			
			playerName												= player.attributes['name']
			loginNotificationEvent									= Event()
			loginNotificationEvent.attributes['signature']			= 'broadcast_to_all_players'
			loginNotificationEvent.attributes['data']['message']	= '{} just logged in.'.format(playerName)
		
			EngineModule.actorEngine.receiveEvent(loginNotificationEvent)
		
		connectionList.attributes['newConnections'] = []
		
		connectionList.attributes['newConnectionSemaphore'].release()
		
		
	def removeClosedConnections(self):
		connectionList.attributes['closedConnectionSemaphore'].acquire()
		
		for connection in connectionList.attributes['closedConnections']:
			connectionList.attributes['connectionList'].remove(connection)
			connection.attributes['socket'].close()
			
			player													= connection.attributes['player']
			playerName												= player.attributes['name']
			logoutNotificationEvent									= Event()
			logoutNotificationEvent.attributes['signature']			= 'broadcast_to_all_players'
			logoutNotificationEvent.attributes['data']['message']	= '{} logged off.'.format(playerName)
		
			EngineModule.actorEngine.receiveEvent(logoutNotificationEvent)
		
		connectionList.attributes['closedConnections'] = []
		
		connectionList.attributes['closedConnectionSemaphore'].release()