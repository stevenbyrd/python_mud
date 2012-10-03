import Engine.ActorEngine
import Engine.RoomEngine
from Event.Event import Event
from AI.AITransition import AITransition

class WaveToNewcomersTransition(AITransition):
	def __init__(self, args):
		AITransition.__init__(self, args)
		
		self.attributes['signature'] = 'actor_added_to_room'


	def transition(self, event):
		receiver	= event.attributes['receiver']
		actor		= event.attributes['data']['actor']
		
		if actor != receiver:
			commandEvent									= Event()
			commandEvent.attributes['signature']			= 'execute_command'
			commandEvent.attributes['data']['command']		= 'wave'
			commandEvent.attributes['data']['args']			= actor.attributes['name']
			commandEvent.attributes['data']['source']		= receiver
	
			Engine.ActorEngine.emitEvent(commandEvent)
			
			
			
			
class Move(AITransition):
	def __init__(self, args):
		AITransition.__init__(self, args)
		
		self.attributes['signature'] = 'game_tick'


	def transition(self, event):
		receiver	= event.attributes['receiver']
		room		= Engine.RoomEngine.getRoom(receiver.attributes['roomID'])
		exitList	= filter(lambda exit : exit.attributes['name'] == self.attributes['direction'],
							 room.attributes['exits'])

		if len(exitList) > 0:
			commandEvent								= Event()
			commandEvent.attributes['signature']		= 'execute_command'
			commandEvent.attributes['data']['command']	= 'go'
			commandEvent.attributes['data']['args']		= [exitList[0]]
			commandEvent.attributes['data']['source']	= receiver

			Engine.ActorEngine.emitEvent(commandEvent)