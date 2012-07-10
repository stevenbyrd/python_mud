from Event.Event import Event
from Command import Command
import Engine.RoomEngine

class Go(Command):
	def __init__(self):
		Command.__init__(self)
		

	def execute(self, receiver, event):
		if event.attributes['data']['commandInstance'] == receiver:
			cmd		= event.attributes['data']['command']
			args	= event.attributes['data']['args']
			actor	= event.attributes['data']['source']
			roomID	= actor.attributes['roomID']
			room	= Engine.RoomEngine.getRoom(roomID)
		
			if cmd != 'go':
				args = [cmd]
		
			if args == None or len(args) == 0:
				args = ['']
		
			moveEvent									= Event()
			moveEvent.attributes['signature']			= 'actor_attempted_movement'
			moveEvent.attributes['data']['direction']	= args[0]
			moveEvent.attributes['data']['source']		= actor
			moveEvent.attributes['data']['room']		= room
		
			receiver.emitEvent(moveEvent)