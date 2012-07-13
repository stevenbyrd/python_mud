import AdjustmentFunctions

class Adjuster:
	def __init__(self, attributes):
		self.attributes = attributes
		
	def adjust(self, event):
		event.attributes['data'][self.attributes['targetValue']] = AdjustmentFunctions.evaluateFunction(event, self.attributes['function'])
		
		return event