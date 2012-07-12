from Event.Event import Event
from Command import Command
import Engine.AffectEngine
import Engine.RoomEngine
import Engine.ActorEngine

class Cast(Command):
	def __init__(self):
		Command.__init__(self)


	def execute(self, source, args):
		roomID	= source.attributes['roomID']
		room	= Engine.RoomEngine.getRoom(roomID)
	
		if args == None or len(args) == 0:
			self.sendUnknownAffectFeedbackEvent(source)
		else:
			spellName = args[0]
			
			print spellName
			
			if Engine.AffectEngine.affectExists(spellName):
				if len(args) == 1:
					args.append(None)
				
				castEvent								= Event()
				castEvent.attributes['signature']		= 'spell_cast_attempted'
				castEvent.attributes['data']['source']	= source
				castEvent.attributes['data']['target']	= args[1]
				castEvent.attributes['data']['spell']	= spellName
				castEvent.attributes['data']['room']	= room
			
				Engine.RoomEngine.emitEvent(castEvent, self)
			else:
				self.sendUnknownAffectFeedbackEvent(source)
					
		
	def sendUnknownAffectFeedbackEvent(self, actor):
		feedbackEvent									= Event()
		feedbackEvent.attributes['signature']			= 'received_feedback'
		feedbackEvent.attributes['data']['feedback']	= 'Cast what?'
		feedbackEvent.attributes['data']['actor']		= actor

		Engine.ActorEngine.emitEvent(feedbackEvent, self)