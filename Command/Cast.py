from Event.Event import Event
from Command import Command
from Engine import AffectEngine

class Cast(Command):
	def __init__(self):
		Command.__init__(self)


	def execute(self, receiver, event):
		if event.attributes['data']['commandInstance'] == receiver:
			args		= event.attributes['data']['args']
			actor		= event.attributes['data']['source']
		
			if args == None or len(args) == 0:
				self.sendUnknownAffectFeedbackEvent(actor, receiver)
			else:
				spellName	= args[0]
				affect		= AffectEngine.getAffect(spellName)
			
				if affect == None:
					self.sendUnknownAffectFeedbackEvent(actor, receiver)
				else:
					if len(args) == 1:
						args[1]	= None
					
					castEvent								= Event()
					castEvent.attributes['signature']		= 'affect_executed'
					castEvent.attributes['data']['source']	= actor
					castEvent.attributes['data']['target']	= args[1]
				
					receiver.emitEvent(castEvent)
		
		
	def sendUnknownAffectFeedbackEvent(self, actor, receiver):
		feedbackEvent									= Event()
		feedbackEvent.attributes['signature']			= 'received_feedback'
		feedbackEvent.attributes['data']['feedback']	= 'Cast what?'
		feedbackEvent.attributes['data']['actor']		= actor

		receiver.emitEvent(feedbackEvent)
		