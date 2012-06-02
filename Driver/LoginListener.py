import threading
import socket
from time import sleep
from Connection.Connection import Connection
from Event.Event import Event
from Engine import ActorEngine
from Engine import ConnectionEngine

class LoginListener(threading.Thread):
	def run(self):
		serversocket	= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		hostname		= socket.gethostname() #hack to get my host name
		
		try:
			tokenized	= hostname.split('.')
			hostname	= '{}.{}.{}.{}'.format(tokenized[3], tokenized[2], tokenized[1], tokenized[0])
		except:
			hostname = 'localhost'
		
		print socket.gethostname()
		print hostname
	
		serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		serversocket.bind((hostname, 8888))
		serversocket.listen(5)
		
		while True:
			clientsocket = serversocket.accept()[0]
			
			clientsocket.setblocking(False)
						
			clientsocket.send('\n\rWelcome! Enter your name:\n\r')

			playerInput = ''

			while playerInput == '':
				try:
					playerInput = clientsocket.recv(1024)
				except:
					playerInput = ''

				if len(playerInput) > 0:
					playerInput = playerInput.strip()

					if ActorEngine.playerExists(playerInput) == True:
						player		= ActorEngine.loadPlayer(playerInput)				
						connection	= Connection(clientsocket, player)
						loginEvent	= Event()

						player.attributes['connection']			= connection
						loginEvent.attributes['signature']		= 'player_login'
						loginEvent.attributes['data']['player'] = player

						ActorEngine.receiveEvent(loginEvent)
						ConnectionEngine.receiveEvent(loginEvent)
					else:
						clientsocket.send('\n\rPlayer not found.\n\rEnter your name:')

						playerInput = ''
				else:
					playerInput = ''		
			
			sleep(2)