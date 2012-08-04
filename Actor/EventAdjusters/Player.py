from Event.EventAdjuster import EventAdjuster

class ActorHasLowLightVisionAdjuster(EventAdjuster):
	def __init__(self, args):
		EventAdjuster.__init__(self, args)
		self.attributes['signature'] = 'actor_observed'
	
	def adjustEvent(self, event):
		event.attributes['flags'].append('low_light_vision')