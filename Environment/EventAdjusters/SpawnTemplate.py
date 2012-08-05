from Event.Event import Event
from Event.EventAdjuster import EventAdjuster

class LimitSpawnByNumberInRoom(EventAdjuster):
	def __init__(self, args):
		EventAdjuster.__init__(self, args)
	
	def adjustEvent(self, event):
		receiver = event.attributes['receiver']
		
		if len(receiver.attributes['npcs']) >= self.attributes['max_in_room']:
			event.attributes['signature'] = None