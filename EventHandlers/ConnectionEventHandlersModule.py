from EventModule import *
import lib.ANSI
		
		
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