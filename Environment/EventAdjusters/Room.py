from Event.Event import Event
from Event.EventAdjuster import EventAdjuster

class NoSpeakingEventAdjuster(EventAdjuster):
	def __init__(self, args):
		EventAdjuster.__init__(self, args)
		self.attributes['signature'] = 'actor_emoted'
	
	def adjustEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['command'] == 'say':
			event.attributes['signature'] = None
			
			feedbackEvent									= Event()
			feedbackEvent.attributes['signature']			= 'received_feedback'
			feedbackEvent.attributes['data']['feedback']	= 'No sound escapes your lips.'
			feedbackEvent.attributes['event_target']		= event.attributes['data']['emoter']
			
			receiver.emitEvent(feedbackEvent)
			
			
			
			
class ObservedWhileDarkAdjuster(EventAdjuster):
	def __init__(self, args):
		EventAdjuster.__init__(self, args)
	
	def adjustEvent(self, event):
		receiver = event.attributes['receiver']
		