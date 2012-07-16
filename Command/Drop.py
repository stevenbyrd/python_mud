from Event.Event import Event
from Command import Command
import Engine.ActorEngine

class Drop(Command):
	def __init__(self):
		Command.__init__(self)
		

	def execute(self, source, args):	
		if args == None or len(args) == 0:
			args = ['']
			
		if len(args) == 1:
			args.append('')
	
		dropEvent									= Event()
		dropEvent.attributes['signature']			= 'actor_attempted_item_drop'
		dropEvent.attributes['data']['itemName']	= args[0]
		dropEvent.attributes['data']['args']		= args[1:]
		dropEvent.attributes['data']['actor']		= source
	
		Engine.ActorEngine.emitEvent(dropEvent)