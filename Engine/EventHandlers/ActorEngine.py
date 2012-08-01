from Event.Event import Event
from Event.EventHandler import EventHandler

class BroadcastEventHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='broadcast_to_all_players'


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





class PlayerLoginEventHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'player_login'


	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		player		= event.attributes['data']['player']

		receiver.addPlayer(player)






class PlayerLogoutEventHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='player_logout'


	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		connection	= event.attributes['data']['connection']
		player		= connection.attributes['player']

		receiver.removePlayer(player)