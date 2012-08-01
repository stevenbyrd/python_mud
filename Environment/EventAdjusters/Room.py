from Event.Event import Event

class NoSpeakingEventAdjuster:
	def __init__(self):
		self.attributes = {'signature':'actor_emoted'}
	
	def adjustEvent(self, event):
		receiver	= event.attributes['receiver']
		room		= event.attributes['data']['room']
		
		if room == receiver and event.attributes['data']['command'] == 'say':
			event.attributes['signature'] = None
			
			feedbackEvent									= Event()
			feedbackEvent.attributes['signature']			= 'received_feedback'
			feedbackEvent.attributes['data']['feedback']	= 'No sound escapes your lips.'
			feedbackEvent.attributes['data']['actor']		= event.attributes['data']['emoter']
			
			receiver.emitEvent(feedbackEvent)