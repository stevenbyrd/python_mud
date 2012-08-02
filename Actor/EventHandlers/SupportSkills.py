from Event.Event import Event
from Event.EventHandler import EventHandler

class RegenerationHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'gained_health_from_tick'
	
	def handleEvent(self, event):	
		receiver = event.attributes['receiver']

		receiver.attributes['currentHP'] += event.attributes['data']['hp']
			
		if receiver.attributes['currentHP'] > receiver.attributes['maxHP']:
			receiver.attributes['currentHP'] = receiver.attributes['maxHP']