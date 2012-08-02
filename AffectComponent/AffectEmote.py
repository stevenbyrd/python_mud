from Event.Event import Event
from AffectComponent import AffectComponent
import Engine.ActorEngine
import Engine.RoomEngine

	
class AffectEmote(AffectComponent):

	def __init__(self, source, target, args):
		AffectComponent.__init__(self, source, target, args)
			
	def execute(self):
		emoteEvent	= Event()
		eventData	= None
		source		= self.attributes['source']
		target		= self.attributes['target']
		roomID		= source.attributes['roomID']
		room		= Engine.RoomEngine.getRoom(roomID)
		
		if target == source:
			eventData			= self.attributes['template']['untargeted'].copy()
			eventData['target']	= None
		else:
			eventData			= self.attributes['template']['targeted'].copy()
			eventData['target']	= target.attributes['name']

		eventData['emoter']	= source

		emoteEvent.attributes['signature']		= 'actor_emoted'
		emoteEvent.attributes['data']			= eventData
		emoteEvent.attributes['data']['room']	= room
	
		Engine.RoomEngine.emitEvent(emoteEvent)