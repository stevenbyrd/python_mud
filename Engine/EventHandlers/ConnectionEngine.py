class PlayerLoginHandler:
	def __init__(self):
		self.attributes = {'signature':'player_login'}

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		player		= event.attributes['data']['player']
		connection	= player.attributes['connection']

		receiver.addConnection(connection)





class PlayerLogoutHandler:
	def __init__(self):
		self.attributes = {'signature':'player_logout'}

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		connection	= event.attributes['data']['connection']

		receiver.removeConnection(connection)