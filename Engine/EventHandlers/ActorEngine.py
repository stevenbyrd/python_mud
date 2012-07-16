from Event.Event import Event

class BroadcastEventHandler:
	def __init__(self):
		self.attributes = {'signature':'broadcast_to_all_players'}


	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		receiver.attributes['playerSetSemaphore'].acquire();

		message											= event.attributes['data']['message']
		notificationEvent								= Event()
		notificationEvent.attributes['signature']		= 'received_notification'
		notificationEvent.attributes['data']['message'] = message
		notificationEvent.attributes['data']['actor']	= None

		receiver.emitEvent(notificationEvent)
		
		receiver.attributes['playerSetSemaphore'].release();





class PlayerLoginEventHandler:
	def __init__(self):
		self.attributes = {'signature' : 'player_login'}


	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		player		= event.attributes['data']['player']

		receiver.addPlayer(player)






class PlayerLogoutEventHandler:
	def __init__(self):
		self.attributes = {'signature':'player_logout'}


	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		connection	= event.attributes['data']['connection']
		player		= connection.attributes['player']

		receiver.removePlayer(player)