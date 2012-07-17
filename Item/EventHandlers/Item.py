import Engine.RoomEngine


class ActorAttemptedDropHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_attempted_item_drop'}

	def handleEvent(self, event):		
		receiver = event.attributes['receiver']

		if event.attributes['data']['item'] == receiver:
			event.attributes['signature'] = 'item_dropped'

			Engine.RoomEngine.emitEvent(event)
			
			
			
			
class ItemDroppedHandler:
	def __init__(self):
		self.attributes = {'signature': 'item_dropped'}

	def handleEvent(self, event):		
		receiver = event.attributes['receiver']

		if event.attributes['data']['item'] == receiver:
			receiver.attributes['inventory'].removeEventSubscriber(receiver)
			event.attributes['data']['room'].attributes['inventory'].addEventSubscriber(receiver)
			
			
			
			
class ActorGrabbedItemHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_grabbed_item'}

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['item'] == receiver:
			receiver.attributes['inventory'].removeEventSubscriber(receiver)
			event.attributes['data']['actor'].attributes['inventory'].addEventSubscriber(receiver)
			
			
			
			
class ActorAttemptedItemGrabHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_attempted_item_grab'}

	def handleEvent(self, event):
		receiver = event.attributes['receiver']			
		
		if event.attributes['data']['item'] == receiver:			
			event.attributes['signature'] = 'actor_grabbed_item'
					
			Engine.RoomEngine.emitEvent(event)
			
			
			
			
			
class ActorAttemptedItemEquipHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_attempted_item_equip'}

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['item'] == receiver:
			actor = event.attributes['data']['actor']
			
			if receiver.attributes['itemType'] != 'Equipable':
				feedbackEvent									= Event()
				feedbackEvent.attributes['signature']			= 'received_feedback'
				feedbackEvent.attributes['data']['feedback']	= 'You can\'t equip that.'
				feedbackEvent.attributes['data']['actor']		= actor

				Engine.ActorEngine.emitEvent(feedbackEvent)
			else:
				event.attributes['signature'] = 'actor_equipped_item'
				
				actor.emitEvent(event)
				
				
				
				
				
				
				
				