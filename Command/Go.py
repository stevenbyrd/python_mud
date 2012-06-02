from Event.Event import Event
from Command import Command
from Engine import RoomEngine

class Go(Command):
	def __init__(self):
		Command.__init__(self)
		

	def execute(self, receiver, event):
		cmd		= event.attributes['data']['command']
		args	= event.attributes['data']['args']
		actor	= event.attributes['data']['source']
		roomID	= actor.attributes['roomID']
		room	= RoomEngine.getRoom(roomID)
		
		if cmd != 'go':
			args = [cmd]
		
		if args == None or len(args) == 0:
			feedbackEvent									= Event()
			feedbackEvent.attributes['signature']			= 'received_feedback'
			feedbackEvent.attributes['data']['feedback']	= 'Go where?'
			
			actor.receiveEvent(feedbackEvent)
			
			return
		
		moveEvent									= Event()
		moveEvent.attributes['signature']			= 'actor_moved'
		moveEvent.attributes['data']['direction']	= args[0]
		moveEvent.attributes['data']['source']		= actor
		
		room.receiveEvent(moveEvent)