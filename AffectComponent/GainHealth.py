from Event.Event import Event
from AffectComponent import AffectComponent
import Engine.ActorEngine
	
class GainHealth(AffectComponent):

	def __init__(self, source, target, args):
		AffectComponent.__init__(self, source, target, args)
			
	def execute(self):
		healEvent								= Event()
		healEvent.attributes['signature']		= 'gained_health'
		healEvent.attributes['data']['target']	= self.attributes['target']
		healEvent.attributes['data']['amount']	= self.attributes['amount']
		
		Engine.ActorEngine.emitEvent(healEvent)