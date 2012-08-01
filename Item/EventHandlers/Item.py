import Engine.RoomEngine
from Event.Event import Event
from Event.EventHandler import EventHandler


class ActorAttemptedDropHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_attempted_item_drop'

	def handleEvent(self, event):		
		receiver = event.attributes['receiver']

		if event.attributes['data']['item'] == receiver:
			event.attributes['signature'] = 'item_dropped'

			Engine.RoomEngine.emitEvent(event)
			
			
			
			
class ItemDroppedHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'item_dropped'

	def handleEvent(self, event):		
		receiver = event.attributes['receiver']

		if event.attributes['data']['item'] == receiver:
			receiver.attributes['inventory'].removeEventSubscriber(receiver)
			event.attributes['data']['room'].attributes['inventory'].addEventSubscriber(receiver)
			
			
			
			
class ActorGrabbedItemHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_grabbed_item'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['item'] == receiver:
			receiver.attributes['inventory'].removeEventSubscriber(receiver)
			event.attributes['data']['actor'].attributes['inventory'].addEventSubscriber(receiver)
			
			
			
			
class ActorAttemptedItemGrabHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_attempted_item_grab'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']			
		
		if event.attributes['data']['item'] == receiver:			
			event.attributes['signature'] = 'actor_grabbed_item'
					
			Engine.RoomEngine.emitEvent(event)
			
			
			
			
			
class ActorAttemptedItemEquipHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_attempted_item_equip'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['item'] == receiver:
			actor		= event.attributes['data']['actor']
			command		= event.attributes['data']['command']
			itemClass	= receiver.attributes['itemClass']
			itemType	= receiver.attributes['itemType']
			
			if (itemType != 'Equipable') or (command == 'wear' and itemClass == 'Wielded') or (command == 'wield' and itemClass != 'Wielded'):
				feedbackEvent									= Event()
				feedbackEvent.attributes['signature']			= 'received_feedback'
				feedbackEvent.attributes['data']['actor']		= actor
				
				if itemType != 'Equipable':
					feedbackEvent.attributes['data']['feedback'] = 'You can\'t equip that.'
				elif command == 'wear':
					feedbackEvent.attributes['data']['feedback'] = 'You can\'t wear that! Try wielding it.'
				else:
					feedbackEvent.attributes['data']['feedback'] = 'You can\'t wield that! Try wearing it.'

				Engine.ActorEngine.emitEvent(feedbackEvent)
			else:
				event.attributes['signature'] = 'actor_equipped_item'
				
				if itemClass == 'Wielded':
					event.attributes['data']['equipperVerb']	= 'wield'
					event.attributes['data']['audienceVerb']	= 'wielded'
				else:
					event.attributes['data']['equipperVerb']	= 'wear'
					event.attributes['data']['audienceVerb']	= 'wore'
				
				actor.emitEvent(event)
				
				
				
				
class WasObservedHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='was_observed'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['target'] == receiver:
			description = ['There is nothing interesting about this object.']
			descArray	= receiver.attributes['description']
			
			if descArray != None and len(descArray) != 0:
				description = descArray
			
			observer										= event.attributes['data']['observer']
			describeEvent									= Event()
			describeEvent.attributes['signature']			= 'entity_described_self'
			describeEvent.attributes['data']['description'] = description
			describeEvent.attributes['data']['observer']	= observer
			room											= Engine.RoomEngine.getRoom(observer.attributes['roomID'])
			
			room.emitEvent(describeEvent)
				
				
				
				
				
				
				