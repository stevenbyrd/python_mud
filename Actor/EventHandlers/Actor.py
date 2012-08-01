import Engine.RoomEngine
import Engine.ActorEngine
from Event.Event import Event
from Event.EventHandler import EventHandler

class ActorAttemptedDropHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_attempted_item_drop'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['actor'] == receiver:
			if event.attributes['data']['itemName'] != '':
				event.attributes['data']['room'] = Engine.RoomEngine.getRoom(receiver.attributes['roomID'])
				receiver.emitEvent(event)
				
				
				
				
class ItemDroppedHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'item_dropped'

	def handleEvent(self, event):		
		receiver = event.attributes['receiver']

		if event.attributes['data']['actor'] == receiver:
			receiver.emitEvent(event)
			
			
			
			
class ActorInitiatedItemGrabHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_initiated_item_grab'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['actor'] == receiver:
			if event.attributes['data']['itemName'] != '':
				event.attributes['data']['room'] = Engine.RoomEngine.getRoom(receiver.attributes['roomID'])
				receiver.emitEvent(event)
				
				
				
				
				
class ActorGrabbedItemHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_grabbed_item'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['actor'] == receiver:
			receiver.emitEvent(event)
			
			
			
			
class ActorAttemptedItemEquipHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_attempted_item_equip'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']

		if event.attributes['data']['actor'] == receiver:
			receiver.emitEvent(event)
			
			
			
			
class ActorAttemptedItemRemovalHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_attempted_item_removal'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']

		if event.attributes['data']['actor'] == receiver:
			receiver.emitEvent(event)
			
			
			
			
class ActorMovedFromRoomEventHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='actor_moved_from_room'

	def handleEvent(self, event):		
		receiver	= event.attributes['receiver']
		actor		= event.attributes['data']['actor']

		if actor == receiver:
			destination = Engine.RoomEngine.getRoom(event.attributes['data']['exit'].attributes['destination'])
			
			event.attributes['data']['room'].removeEventSubscriber(receiver)
			
			destination.addEventSubscriber(receiver)
			
			receiver.attributes['roomID'] = destination.attributes['roomID']
			
			
			
			
class ActorGainedHealthEventHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='gained_health'

	def handleEvent(self, event):		
		receiver	= event.attributes['receiver']
		target		= event.attributes['data']['target']

		if target == receiver:
			receiver.attributes['currentHP'] += event.attributes['data']['amount']
			
			
			
			
class ActorWasObservedEventHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='was_observed'

	def handleEvent(self, event):		
		receiver	= event.attributes['receiver']
		target		= event.attributes['data']['target']

		if target == receiver:
			describeEvent									= Event()
			describeEvent.attributes['signature']			= 'entity_described_self'
			describeEvent.attributes['data']['room']		= receiver.attributes['roomID']
			describeEvent.attributes['data']['observer']	= event.attributes['data']['observer']
			describeEvent.attributes['data']['description']	= receiver.getDescription()
			
			ActorEngine.emitEvent(describeEvent)
		