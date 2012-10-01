from AIState import AIState

class AI:
	def __init__(self, aiJson):
		self.attributes = {
			'current_state'	: None,
			'states'		: []
		}
		
		if aiJson != None:				
			for state in aiJson['states']:
				aiState = AIState(state)
				
				self.attributes['states'].append(aiState)
				
				if aiState.attributes['state_id'] == aiJson['current_state']:
					self.attributes['current_state'] = aiState
					
			
		
	
	def receiveEvent(self, event, emitter):
		currentState = self.attributes['current_state']
		
		if currentState != None:
			nextStateID = currentState.receiveEvent(event)
			
			if nextStateID != None:
				for state in self.attributes['states']:
					if state.attributes['state_id'] == nextStateID:
						self.attributes['current_state'] = state
					
						break