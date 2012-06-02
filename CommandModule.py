from EventModule import *
from EngineModule import *
import EngineModule


class Command(EventReceiver):
	def __init__(self):
		EventReceiver.__init__(self)

		commandExecutionHandler = EventHandler()

		commandExecutionHandler.attributes['signature'] = 'execute_command'
		commandExecutionHandler.attributes['function']	= self.execute

		self.addEventHandler(commandExecutionHandler)
		




class Go(Command):
	def __init__(self):
		Command.__init__(self)
		

	def execute(self, receiver, event):
		cmd		= event.attributes['data']['command']
		args	= event.attributes['data']['args']
		actor	= event.attributes['data']['source']
		roomID	= actor.attributes['roomID']
		room	= EngineModule.roomEngine.getRoom(roomID)
		
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
		
		



class Look(Command):
	def __init__(self):
		Command.__init__(self)


	def execute(self, receiver, event):
		args		= event.attributes['data']['args']
		actor		= event.attributes['data']['source']
		roomID		= actor.attributes['roomID']
		room		= EngineModule.roomEngine.getRoom(roomID)
		lookEvent	= Event()
		
		lookEvent.attributes['data']['observer'] = actor
		
		if args == None or len(args) == 0:
			lookEvent.attributes['signature'] = 'was_observed'
		else:
			lookEvent.attributes['signature']		= 'actor_observed'
			lookEvent.attributes['data']['target']	= args[0]
		
		room.receiveEvent(lookEvent)
		
		


		

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
			room		= EngineModule.roomEngine.getRoom(roomID)
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
			
			
			
			

class Emote(Command):
	def __init__(self, template):
		Command.__init__(self)
		self.eventTemplate = template
		
	def execute(self, receiver, event):
		emoteEvent	= Event()
		emoter		= event.attributes['data']['source']
		args		= event.attributes['data']['args']
		roomID		= emoter.attributes['roomID']
		room		= EngineModule.roomEngine.getRoom(roomID)
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
		
		
		
		
		
		
		
		
		
		