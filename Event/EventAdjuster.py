from lib import ScriptFunctions
import copy

class EventAdjuster:
	def __init__(self, attributes):
		self.attributes = attributes
		
	def adjust(self, event):
		function = copy.deepcopy(self.attributes['function'])
		
		ScriptFunctions.evaluate(event, function)
		
		return event