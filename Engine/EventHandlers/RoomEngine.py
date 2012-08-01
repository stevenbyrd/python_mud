from Event.Event import Event
from Event.EventHandler import EventHandler

class PlayerLoginEventHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='player_login'

	def handleEvent(self, event):
		receiver		= event.attributes['receiver']
		player			= event.attributes['data']['player']
		roomID			= player.attributes['roomID']
		room			= receiver.getRoom(roomID)
		playerInEvent	= Event()

		playerInEvent.attributes['signature']		= 'actor_added_to_room'
		playerInEvent.attributes['data']['actor']	= player
		playerInEvent.attributes['data']['room']	= room

		receiver.emitEvent(playerInEvent)




class PlayerLogoutEventHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='player_logout'

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		connection	= event.attributes['data']['connection']
		player		= connection.attributes['player']
		roomID		= player.attributes['roomID']
		room		= receiver.getRoom(roomID)
		logoutEvent = Event()

		logoutEvent.attributes['signature']				= 'player_logout'
		logoutEvent.attributes['data']['actor']			= player
		logoutEvent.attributes['data']['exitMessage']	= None

		receiver.emitEvent(logoutEvent)