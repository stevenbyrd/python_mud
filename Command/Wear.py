from Event.Event import Event
from Command import Command
import Engine.ActorEngine

class Wear(Command):
	def __init__(self):
		Command.__init__(self)
		

	def execute(self, source, args):
		equipEvent									= Event()
		equipEvent.attributes['data']['actor']		= source
		
		if args == None or len(args) == 0:
			equipEvent.attributes['signature']			= 'received_feedback'
			equipEvent.attributes['data']['feedback']	= 'Wear what?'

		else:
			if len(args) == 1:
				args.append('')
			
			equipEvent.attributes['signature']			= 'actor_attempted_item_equip'
			equipEvent.attributes['data']['itemName']	= args[0]
			equipEvent.attributes['data']['args']		= args[1:]
			equipEvent.attributes['data']['command']	= 'wear'
			
		Engine.ActorEngine.emitEvent(equipEvent)