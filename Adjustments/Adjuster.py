import AdjustmentFunctions

class Adjuster:
	def __init__(self, attributes):
		self.attributes = attributes
		
	def adjust(self, event):
		adjustedValue = AdjustmentFunctions.evaluateFunction(event, self.attributes['function'])
		
		if adjustedValue == False:
			return None
		else:
			event.attributes['data'][self.attributes['targetValue']] = adjustedValue
		
			return event