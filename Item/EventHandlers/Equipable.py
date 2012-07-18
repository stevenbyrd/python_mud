class ActorAttemptedItemRemovalHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_attempted_item_removal'}

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['item'] == receiver:
			event.attributes['signature'] = 'actor_removed_item'
			
			event.attributes['data']['actor'].emitEvent(event)