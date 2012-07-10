from Event.Event import Event
from Command import Command
from Engine import RoomEngine

class Look(Command):
	def __init__(self):
		Command.__init__(self)


	def execute(self, receiver, event):
		if event.attributes['data']['commandInstance'] == receiver:
			args		= event.attributes['data']['args']
			actor		= event.attributes['data']['source']
			roomID		= actor.attributes['roomID']
			room		= RoomEngine.getRoom(roomID)
			lookEvent	= Event()
		
			lookEvent.attributes['data']['observer']	= actor
			lookEvent.attributes['data']['room']		= room
		
			if args == None or len(args) == 0:
				lookEvent.attributes['signature'] = 'was_observed'
			else:
				lookEvent.attributes['signature']		= 'actor_observed'
				lookEvent.attributes['data']['target']	= args[0]
				
			receiver.emitEvent(lookEvent)