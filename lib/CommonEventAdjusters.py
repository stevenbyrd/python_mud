from Event.EventAdjuster import EventAdjuster

class FilterGameTicksByModulus(EventAdjuster):
	def __init__(self, args):
		EventAdjuster.__init__(self, args)
		self.attributes['signature'] = 'game_tick'
		
		
	def adjustEvent(self, event):
		tickCount	= event.attributes['receiver'].attributes['tick_count']
		modulus		= self.attributes['modulus']
		
		if tickCount % modulus != 0:
			event.attributes['signature'] = None