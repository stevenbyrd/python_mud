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
	
		serversocket.bind(('localhost', 8888))
		serversocket.listen(2)
		
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
						player 		= EngineModule.actorEngine.loadPlayer(playerInput)				
						connection	= Connection(clientsocket, player)
						loginEvent	= Event()

						player.attributes['connection']			= connection
						loginEvent.attributes['signature'] 		= 'player_login'
						loginEvent.attributes['data']['player']	= player

						EngineModule.roomEngine.receiveEvent(loginEvent)
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
		

	def send(self, message):
		self.attributes['outputBuffer'].append(message)


	def sendFinal(self, message):
		self.send(message)
		self.send(	ANSI.magenta('\n[') + 
					ANSI.yellow('HP: ') + ANSI.white(self.attributes['player'].attributes['currentHP']) + 
					ANSI.yellow(' Mana: ') + ANSI.white(self.attributes['player'].attributes['currentMana']) + 
					ANSI.magenta(']\n'))
						
						
						


class ConnectionList(EventReceiver):
	def __init__(self):
		EventReceiver.__init__(self)
		attributes = {
			'connectionList'	: [],
			'semaphore'			: threading.BoundedSemaphore(2)
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
			
		playerLoginHandler	= EventHandler()

		playerLoginHandler.attributes['signature']	= 'player_login'
		playerLoginHandler.attributes['function']	= self.playerLogin

		self.addEventHandler(playerLoginHandler)
	
	
	def addConnection(self, connection):
		self.attributes['semaphore'].acquire()
		self.attributes['semaphore'].acquire()
		self.attributes['connectionList'].append(connection)
		self.attributes['semaphore'].release()
		self.attributes['semaphore'].release()
	
	
	def removeConnection(self, connection):
		sself.attributes['semaphore'].acquire()
		self.attributes['semaphore'].acquire()
		self.attributes['connectionList'].remove(connection)
		self.attributes['semaphore'].release()
		self.attributes['semaphore'].release()
		
		
	def playerLogin(self, event):
		player 		= event.attributes['data']['player']
		connection	= player.attributes['connection']
		
		self.addConnection(connection)

		