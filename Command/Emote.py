from Event.Event import Event
from Command import Command
import Engine.RoomEngine

class Emote(Command):
	def __init__(self, template):
		Command.__init__(self)
		self.eventTemplate = template
		
	def execute(self, source, args):
		emoteEvent	= Event()
		emoter		= source
		roomID		= emoter.attributes['roomID']
		room		= Engine.RoomEngine.getRoom(roomID)
		eventData	= None
	
		if args == None or len(args) == 0:
			eventData			= self.eventTemplate['untargeted'].copy()
			eventData['target']	= None
		else:
			eventData			= self.eventTemplate['targeted'].copy()
			eventData['target']	= args[0]

		eventData['emoter']	= emoter
		eventData['room']	= room

		emoteEvent.attributes['signature']	= 'actor_emoted'
		emoteEvent.attributes['data']		= eventData
	
		Engine.RoomEngine.emitEvent(emoteEvent, self)
	