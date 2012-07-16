from Event.Event import Event
import Engine.ActorEngine
import Engine.RoomEngine
import re


pattern = re.compile('[1-9][0-9]*')


class ActorAttemptedDropHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_attempted_item_drop'}

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		target		= event.attributes['data']['itemName']
		targetList	= filter(lambda item : 
								item.attributes['name'].lower().startswith(target.lower()), 
							receiver.attributes['items'])

		if len(targetList) == 0:
			feedbackEvent									= Event()
			feedbackEvent.attributes['signature']			= 'received_feedback'
			feedbackEvent.attributes['data']['feedback']	= 'You don\'t have that.'
			feedbackEvent.attributes['data']['actor']		= event.attributes['data']['actor']

			Engine.ActorEngine.emitEvent(feedbackEvent)
		else:
			event.attributes['data']['item']	= targetList[0]
			args								= event.attributes['data']['args']
			
			if len(args) >= 1 and args[0] != '':				
				if pattern.match(args[0]) and re.search('[^0-9]', args[0]) == None:
					itemNumber = int(args[0]) - 1
					
					if itemNumber < len(targetList):						
						event.attributes['data']['item'] = targetList[itemNumber]
			
			receiver.emitEvent(event)
			
			
			
			
class ItemDroppedHandler:
	def __init__(self):
		self.attributes = {'signature': 'item_dropped'}

	def handleEvent(self, event):		
		receiver = event.attributes['receiver']

		receiver.attributes['items'].remove(event.attributes['data']['item'])

		receiver.emitEvent(event)
		
		
		
		
class ActorInitiatedItemGrabHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_initiated_item_grab'}

	def handleEvent(self, event):
		# as of now, this is sort of a superfluous step in the event chain -- we'll come back here when
		# we implement containers (bags) so that an actor can get items out of containers within his own
		# inventory. For now, just publish an event to the RoomEngine
		event.attributes['signature'] = 'actor_attempted_item_grab'
		
		Engine.RoomEngine.emitEvent(event)
		
		
		
		
class ActorGrabbedItemHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_grabbed_item'}

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		receiver.attributes['items'].append(event.attributes['data']['item'])