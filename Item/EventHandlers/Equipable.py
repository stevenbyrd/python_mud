from Event.EventHandler import EventHandler


class ActorAttemptedItemRemovalHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_attempted_item_removal'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['item'] == receiver:
			event.attributes['signature'] = 'actor_removed_item'
		
			event.attributes['data']['actor'].emitEvent(event)