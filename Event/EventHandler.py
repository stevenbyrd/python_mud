import json
import copy

class EventHandler:
	def __init__(self, attributes):
		self.attributes	= attributes
				

	def handleEvent(self, event):
		import lib.ScriptFunctions
		
		function = copy.deepcopy(self.attributes['function'])
		
		lib.ScriptFunctions.evaluate(event, function)