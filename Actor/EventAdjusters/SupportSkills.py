from Event.EventAdjuster import EventAdjuster

class RegenerationAdjuster(EventAdjuster):
	def __init__(self, args):
		EventAdjuster.__init__(self, args)
	
	def adjustEvent(self, event):
		event.attributes['data']['hp'] = int(self.attributes['skill_level'] * event.attributes['data']['hp'])