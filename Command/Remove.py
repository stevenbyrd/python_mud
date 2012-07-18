from Event.Event import Event
from Command import Command
import Engine.ActorEngine

class Remove(Command):
	def __init__(self):
		Command.__init__(self)
		

	def execute(self, source, args):
		removeEvent									= Event()
		removeEvent.attributes['data']['actor']		= source
		
		if args == None or len(args) == 0:
			removeEvent.attributes['signature']			= 'received_feedback'
			removeEvent.attributes['data']['feedback']	= 'Remove what?'

		else:
			if len(args) == 1:
				args.append('')
			
			removeEvent.attributes['signature']			= 'actor_attempted_item_removal'
			removeEvent.attributes['data']['itemName']	= args[0]
			removeEvent.attributes['data']['args']		= args[1:]
			
		Engine.ActorEngine.emitEvent(removeEvent)