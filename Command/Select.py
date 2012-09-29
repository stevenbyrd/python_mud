from Event.Event import Event
from Command import Command
import Engine.ActorEngine

class Select(Command):
	def __init__(self):
		Command.__init__(self)


	def execute(self, source, args):	
		if args == None or len(args) == 0:
			feedbackEvent									= Event()
			feedbackEvent.attributes['signature']			= 'received_feedback'
			feedbackEvent.attributes['data']['feedback']	= 'Select which option?'
			feedbackEvent.attributes['data']['actor']		= actor

			Engine.ActorEngine.emitEvent(feedbackEvent)
		else:
			selectEvent									= Event()
			selectEvent.attributes['signature']			= 'menu_option_chosen'
			selectEvent.attributes['data']['option']	= args[0]
		
			source.attributes['menus'][-1].receiveEvent(selectEvent, None)