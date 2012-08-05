import datetime
from Actor import Actor

class NPC(Actor):
	def __init__(self, actorJSON):
		Actor.__init__(self, actorJSON)
		attributes = {
			'spawnTime'		: datetime.datetime,
			'pluralName'	: '',
			'is_perm'		: False
		}
		
		for key in attributes.keys():
			if self.attributes.has_key(key) == False:
				self.attributes[key] = attributes[key]
		
		if self.attributes['is_perm']:
			self.attributes['adjective'] = ''
		else:
			self.attributes['adjective'] = (lambda char: 
												((char == 'a' or char == 'e' or char == 'i' or char == 'o' or char == 'u') and 'an') or 'a')(self.attributes['name'].lower()[0])
											
		
	def wander(self):
		from Event.Event import Event
		import Engine.ActorEngine
		
		commandEvent									= Event()
		commandEvent.attributes['signature']			= 'execute_command'
		commandEvent.attributes['data']['command']		= 'go'
		commandEvent.attributes['data']['args']			= 'n'
		commandEvent.attributes['data']['source']		= self
	
		Engine.ActorEngine.emitEvent(commandEvent)