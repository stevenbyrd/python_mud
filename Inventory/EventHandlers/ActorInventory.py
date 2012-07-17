from Event.Event import Event
import Engine.ActorEngine
import Engine.RoomEngine
import re
from lib import ANSI


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
		
		
		
		
class ActorViewedEquipmentHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_viewed_equipment'}

	def handleEvent(self, event):
		actor		= event.attributes['data']['actor']
		receiver	= event.attributes['receiver']
		equipString	= ' nothing'		
		
		equipment	= filter(lambda item: item != None,
							[receiver.attributes['equipment']['Head'],
							 receiver.attributes['equipment']['Ears'],
							 receiver.attributes['equipment']['Eyes'],
							 receiver.attributes['equipment']['Face'],
							 receiver.attributes['equipment']['Neck'][0],
							 receiver.attributes['equipment']['Neck'][1],
							 receiver.attributes['equipment']['Body'],
							 receiver.attributes['equipment']['Arms'],
							 receiver.attributes['equipment']['Wrist'][0],
							 receiver.attributes['equipment']['Wrist'][1],
							 receiver.attributes['equipment']['Hands'],
							 receiver.attributes['equipment']['Finger'][0],
							 receiver.attributes['equipment']['Finger'][1],
							 receiver.attributes['equipment']['Waist'],
							 receiver.attributes['equipment']['Legs'],
							 receiver.attributes['equipment']['Feet'],
							 receiver.attributes['equipment']['Shield'],
							 receiver.attributes['equipment']['Wielded']])
			
		if len(equipment) != 0:
			equipString = ''
			
			for item in equipment:
				slot	= item.attributes['itemClass']
				tabs	= (lambda slotName: len(slotName) <= 5 and '\t\t' or '\t' )(slot)
				
				equipString = '{}\n  {}{}: {} {}'.format(equipString, ANSI.yellow(slot), tabs, item.attributes['adjective'], item.attributes['name'])
		
		feedbackEvent									= Event()
		feedbackEvent.attributes['signature']			= 'received_feedback'
		feedbackEvent.attributes['data']['feedback']	= 'You are wearing:{}'.format(equipString)
		feedbackEvent.attributes['data']['actor']		= actor

		Engine.ActorEngine.emitEvent(feedbackEvent)		




class ActorAttemptedItemEquipHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_attempted_item_equip'}

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




class ActorEquippedItemHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_equipped_item'}

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		item		= event.attributes['data']['item']
		actor		= event.attributes['data']['actor']
		slot		= item.attributes['itemClass']
		equipment	= receiver.attributes['equipment']
		equipable	= (lambda eq, sl: 
							eq[sl] != None and
							(type(eq[sl]) != type([]) or (eq[sl][0] != None and eq[sl][1] != None)))(equipment, slot)
		
		print 'equipable = {}'.format(equipable)
		
		if equipable:
			feedbackEvent									= Event()
			feedbackEvent.attributes['signature']			= 'received_feedback'
			feedbackEvent.attributes['data']['feedback']	= 'You\'re already wearing something there.'
			feedbackEvent.attributes['data']['actor']		= actor

			Engine.ActorEngine.emitEvent(feedbackEvent)
		else:
			if equipment[slot] != None:
				if equipment[slot][0] != None:
					equipment[slot][0] = item
				else:
					equipment[slot][1] = item
			else:
				equipment[slot] = item
			
			receiver.attributes['items'].remove(item)

			receiver.emitEvent(event)
			
			emoteEvent	= Event()
			emoter		= actor
			roomID		= emoter.attributes['roomID']
			room		= Engine.RoomEngine.getRoom(roomID)
			
			emoteEvent.attributes['signature']	= 'actor_emoted'
			emoteEvent.attributes['data']		= {
														'target':None,
														'emoter': actor,
														'room': room,
														"emoterText":"You equip the {}.".format(item.attributes['name']),
														"audienceText":"#emoter# equips {} {}.".format(item.attributes['adjective'], item.attributes['name'])
			}

			Engine.RoomEngine.emitEvent(emoteEvent)