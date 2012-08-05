import Engine.RoomEngine
import Engine.ActorEngine
from Event.Event import Event
from Event.EventHandler import EventHandler

class WaveToNewcomersHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='actor_added_to_room'

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		owner		= receiver.attributes['owner']
		actor		= event.attributes['data']['actor']
		
		if actor != owner:
			commandEvent									= Event()
			commandEvent.attributes['signature']			= 'execute_command'
			commandEvent.attributes['data']['command']		= 'wave'
			commandEvent.attributes['data']['args']			= actor.attributes['name']
			commandEvent.attributes['data']['source']		= owner
	
			Engine.ActorEngine.emitEvent(commandEvent)