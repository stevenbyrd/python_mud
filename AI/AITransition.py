import importlib

class AITransition:
	def __init__(self, args):
		self.attributes = {
			'signature'			: '',
			'transition_state'	: None
		}

		if args != None:
			for key in args.keys():
				self.attributes[key] = args[key]
				
		


	def receiveEvent(self, event):
		self.transition(event)
		
		return self.attributes['transition_state']
		
		
		
		
	def transition(self, event):
		pass