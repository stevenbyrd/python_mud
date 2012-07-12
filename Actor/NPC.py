class NPC(Actor):
	def __init__(self, roomID):
		Actor.__init__(self, roomID)
		attributes = {
			'wanderRate'	: 0,
			'spawnRate'		: 0,
			'numberInRoom'	: 0,
			'minimumWait'	: 5000,
			'spawnTime'		: '',
			'pluralName'	: ''
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]