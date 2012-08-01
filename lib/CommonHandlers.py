class FilterGameTicksByModulus:
	def __init__(self):
		self.attributes = {'signature':'game_tick'}
		
		
	def adjustEvent(self, event):
		tickCount	= event.attributes['receiver'].attributes['tick_count']
		modulus		= self.attributes['args']['modulus']
		
		if tickCount % modulus != 0:
			event.attributes['signature'] = None