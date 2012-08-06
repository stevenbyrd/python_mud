import importlib
from Event.Event import Event

class AIState:
	def __init__(self, stateJSON):
		self.attributes = {
			'state_id'		: '',
			'transitions'	: []
		}
		
		if stateJSON != None:
			self.attributes['state_id'] = stateJSON['state_id']

			for element in stateJSON['transitions']:		
				args			= (lambda dictionary: dictionary.has_key('args') and dictionary['args'] or None)(element)
				transitionName	= element['name']
						
				self.addTransitionByNameWithArgs(transitionName, args)
						
		
	
	def receiveEvent(self, event):
		retVal = None
		
		for transition in self.attributes['transitions']:
			if transition.attributes['signature'] == event.attributes['signature']:
				retVal = transition.receiveEvent(event)
				
				break
		
		return retVal			

			
			
	def addTransitionByNameWithArgs(self, transitionName, args):
		path		= transitionName.split('.')
		modulePath	= path[0]
	
		for step in path[1:-1]:
			modulePath = '{}.{}'.format(modulePath, step)
	
		transitionModule	= importlib.import_module(modulePath)
		transitionClass		= getattr(transitionModule, path[-1])
		transition			= transitionClass(args)
		
		self.attributes['transitions'].append(transition)