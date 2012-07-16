from Event.Event import Event
from Command import Command
import Engine.ActorEngine

class Grab(Command):
	def __init__(self):
		Command.__init__(self)
		

	def execute(self, source, args):	
		if args == None or len(args) == 0:
			args = ['']
			
		if len(args) == 1:
			args.append('')
	
		getEvent								= Event()
		getEvent.attributes['signature']		= 'actor_initiated_item_grab'
		getEvent.attributes['data']['itemName']	= args[0]
		getEvent.attributes['data']['args']		= args[1:]
		getEvent.attributes['data']['actor']	= source
	
		Engine.ActorEngine.emitEvent(getEvent)