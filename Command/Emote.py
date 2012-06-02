from Event.Event import Event
from Command import Command
from Engine import RoomEngine

class Emote(Command):
	def __init__(self, template):
		Command.__init__(self)
		self.eventTemplate = template
		
	def execute(self, receiver, event):
		emoteEvent	= Event()
		emoter		= event.attributes['data']['source']
		args		= event.attributes['data']['args']
		roomID		= emoter.attributes['roomID']
		room		= RoomEngine.getRoom(roomID)
		data		= None
		
		if args == None or len(args) == 0:
			data			= self.eventTemplate['untargeted'].copy()
			data['target']	= None
		else:
			data			= self.eventTemplate['targeted'].copy()
			data['target']	= args[0]

		data['emoter'] = emoter

		emoteEvent.attributes['signature']	= 'actor_emoted'
		emoteEvent.attributes['data']		= data
		
		room.receiveEvent(emoteEvent)
		