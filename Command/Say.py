from Event.Event import Event
from Command import Command
import Engine.RoomEngine

class Say(Command):
	def __init__(self):
		Command.__init__(self)
		
	
	def execute(self, source, args):
		actor		= source
		words		= args
		roomID		= actor.attributes['roomID']
		room		= Engine.RoomEngine.getRoom(roomID)
		speakEvent	= Event()
		
		speakEvent.attributes['signature']		= 'actor_emoted'
		speakEvent.attributes['data']['emoter']	= actor
		speakEvent.attributes['data']['target']	= None
		speakEvent.attributes['data']['room']	= room

		if words == None or len(words) == 0:
			speakEvent.attributes['data']['emoterText']		= 'Say what?'
			speakEvent.attributes['data']['audienceText']	= None		
		else:	
			sentence = ''
		
			for word in words:
				sentence										= '{} {}'.format(sentence, word)
				speakEvent.attributes['data']['emoterText']		= 'You say, "{}".'.format(sentence[1:])
				speakEvent.attributes['data']['audienceText']	= '{} says, "{}".'.format(actor.attributes['name'], sentence[1:])
		
		Engine.RoomEngine.emitEvent(speakEvent)