from Event.Event import Event

class Regneration:
	def __init__(self):
		self.attributes = {'signature':'gained_health'}
	
	def adjustEvent(self, event):
		receiver = event.attributes['receiver']
		
		if room == receiver and event.attributes['data']['command'] == 'say':
			event.attributes['signature'] = None
			
			feedbackEvent									= Event()
			feedbackEvent.attributes['signature']			= 'received_feedback'
			feedbackEvent.attributes['data']['feedback']	= 'No sound escapes your lips.'
			feedbackEvent.attributes['data']['actor']		= event.attributes['data']['emoter']
			
			receiver.emitEvent(feedbackEvent)