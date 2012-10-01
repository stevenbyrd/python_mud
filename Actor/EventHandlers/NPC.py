import random
from Event.EventHandler import EventHandler


class GameTickedHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='game_tick'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if random.random() < receiver.attributes['wanderRate']:
			receiver.wander()