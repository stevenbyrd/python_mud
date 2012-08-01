from Event.EventHandler import EventHandler

class PlayerLoginHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='player_login'

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		player		= event.attributes['data']['player']
		connection	= player.attributes['connection']

		receiver.addConnection(connection)





class PlayerLogoutHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='player_logout'

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		connection	= event.attributes['data']['connection']

		receiver.removeConnection(connection)