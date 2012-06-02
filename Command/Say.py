from Event.Event import Event
from Command import Command
from Engine import RoomEngine

class Say(Command):
	def __init__(self):
		Command.__init__(self)
		
	
	def execute(self, receiver, event):
		actor	= event.attributes['data']['source']
		words	= event.attributes['data']['args']
		
		if words == None or len(words) == 0:
			feedbackEvent									= Event()
			feedbackEvent.attributes['signature']			= 'received_feedback'
			feedbackEvent.attributes['data']['feedback']	= 'Say what?'
			
			actor.receiveEvent(feedbackEvent)
		else:
			roomID		= actor.attributes['roomID']
			room		= RoomEngine.getRoom(roomID)
			speakEvent	= Event()
			sentence	= ''
			
			for word in words:
				sentence = '{} {}'.format(sentence, word)
				
			speakEvent.attributes['signature']				= 'actor_emoted'
			speakEvent.attributes['data']['emoter']			= actor
			speakEvent.attributes['data']['target']			= None
			speakEvent.attributes['data']['emoterText']		= 'You say, "{}".'.format(sentence[1:])
			speakEvent.attributes['data']['audienceText']	= '{} says, "{}".'.format(actor.attributes['name'], sentence[1:])
			
			room.receiveEvent(speakEvent)