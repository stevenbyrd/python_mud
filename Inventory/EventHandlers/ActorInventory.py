from Event.Event import Event
from Event.EventHandler import EventHandler
import Engine.ActorEngine
import Engine.RoomEngine
import re
from lib import ANSI


pattern = re.compile('[1-9][0-9]*')


class ActorAttemptedDropHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_attempted_item_drop'

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
			
			
			
			
class ItemDroppedHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'item_dropped'

	def handleEvent(self, event):		
		receiver	= event.attributes['receiver']
		item		= event.attributes['data']['item']

		receiver.attributes['items'].remove(item)
		
		event.attributes['data']['item'] = item

		receiver.emitEvent(event)
		
		
		
		
class ActorInitiatedItemGrabHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_initiated_item_grab'

	def handleEvent(self, event):
		# as of now, this is sort of a superfluous step in the event chain -- we'll come back here when
		# we implement containers (bags) so that an actor can get items out of containers within his own
		# inventory. For now, just publish an event to the RoomEngine
		event.attributes['signature']		= 'actor_attempted_item_grab'
		event.attributes['data']['room']	= event.attributes['data']['room']
		
		Engine.RoomEngine.emitEvent(event)
		
		
		
		
class ActorGrabbedItemHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_grabbed_item'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		receiver.attributes['items'].append(event.attributes['data']['item'])
		
		
		
		
class ActorViewedEquipmentHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_viewed_equipment'

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		actor		= receiver.attributes['owner']
		equipString	= ' nothing'		
		equipment	= receiver.listEquipment()
			
		if len(equipment) != 0:
			equipString = ''
			
			for line in equipment:
				equipString = '{}\n{}'.format(equipString, line)
		
		feedbackEvent									= Event()
		feedbackEvent.attributes['signature']			= 'received_feedback'
		feedbackEvent.attributes['data']['feedback']	= 'You are wearing:{}\n'.format(equipString)
		feedbackEvent.attributes['data']['actor']		= actor

		Engine.ActorEngine.emitEvent(feedbackEvent)		




class ActorAttemptedItemEquipHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_attempted_item_equip'

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




class ActorEquippedItemHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_equipped_item'

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		item		= event.attributes['data']['item']
		actor		= event.attributes['data']['actor']
		slot		= item.attributes['itemClass']
		equipment	= receiver.attributes['equipment']
		slotFull	= (lambda eq, sl: 
							eq[sl] != None and
							(type(eq[sl]) != type([]) or (eq[sl][0] != None and eq[sl][1] != None)))(equipment, slot)
		
		if slotFull:
			feedbackEvent								= Event()
			feedbackEvent.attributes['signature']		= 'received_feedback'
			feedbackEvent.attributes['data']['actor']	= actor
			
			if slot == 'Wielded':
				feedbackEvent.attributes['data']['feedback'] = 'You already have something wielded.'
			else:
				feedbackEvent.attributes['data']['feedback'] = 'You\'re already wearing something on your {}.'.format(slot.lower())

			Engine.ActorEngine.emitEvent(feedbackEvent)
		else:
			if equipment[slot] != None:
				if equipment[slot][0] == None:
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
														"emoterText":"You {} the {}.".format(event.attributes['data']['equipperVerb'], item.attributes['name']),
														"audienceText":"#emoter# {} {} {}.".format(event.attributes['data']['audienceVerb'], item.attributes['adjective'], item.attributes['name'])
			}

			Engine.RoomEngine.emitEvent(emoteEvent)
			
			
			
			
class ActorAttemptedItemRemovalHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_attempted_item_removal'

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		itemName	= event.attributes['data']['itemName']
		args		= event.attributes['data']['args']
		itemNumber	= 0
		equipment	= filter(lambda element: element != None and element.attributes['name'].lower().startswith(itemName.lower()),
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
		
		
		if len(args) >= 1 and args[0] != '':				
			if pattern.match(args[0]) and re.search('[^0-9]', args[0]) == None:
				itemNumber = int(args[0]) - 1
				
		if itemNumber < len(equipment):						
			event.attributes['data']['item'] = equipment[itemNumber]
			
			receiver.emitEvent(event)
		else:
			feedbackEvent									= Event()
			feedbackEvent.attributes['signature']			= 'received_feedback'
			feedbackEvent.attributes['data']['actor']		= event.attributes['data']['actor']
			feedbackEvent.attributes['data']['feedback']	= 'Remove what?'

			Engine.ActorEngine.emitEvent(feedbackEvent)
			
			
			
			
class ActorRemovedItemHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_removed_item'

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		item		= event.attributes['data']['item']
		actor		= event.attributes['data']['actor']
		slot		= item.attributes['itemClass']
		equipment	= receiver.attributes['equipment']
		
		if type(equipment[slot]) == type([]):
			if equipment[slot][0] == item:
				equipment[slot][0] = None
			else:
				equipment[slot][1] = None
		else:
			equipment[slot] = None
			
		receiver.attributes['items'].append(item)
		
		receiver.emitEvent(event)
		
		emoteEvent	= Event()
		emoter		= actor
		roomID		= emoter.attributes['roomID']
		room		= Engine.RoomEngine.getRoom(roomID)
		
		emoteEvent.attributes['signature']		= 'actor_emoted'
		emoteEvent.attributes['data']			= {
														'target'		: None,
														'emoter'		: actor,
														'room'			: room,
														"emoterText"	: "You removed the {}.".format(item.attributes['name']),
														"audienceText"	: "#emoter# removed {} {}.".format(item.attributes['adjective'], item.attributes['name'])
			}

		Engine.RoomEngine.emitEvent(emoteEvent)
		
		
		
		
class ActorObservedHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='actor_observed'

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		observer	= event.attributes['data']['observer']
		target		= event.attributes['data']['target']
		items		= receiver.attributes['items']
		equipment	= receiver.attributes['equipment']
		equipped	= []
		
		for key in equipment.keys():
			equippedItem = equipment[key]
			
			if key == 'Neck' or key == 'Wrist' or key == 'Finger':
				for item in equippedItem:
					if item != None:
						equipped.append(item)
			else:
				if equippedItem != None:
					equipped.append(equippedItem)
		
		if target != None and target in set(items + equipped):
			lookEvent									= Event()
			lookEvent.attributes['data']['observer']	= observer
			lookEvent.attributes['data']['target']		= target
			lookEvent.attributes['signature']			= 'was_observed'

			receiver.emitEvent(lookEvent)
		else:
			#The actor meant to look at the room, or something in it
			if target == None:
				event.attributes['signature'] = 'was_observed'
			
			Engine.RoomEngine.emitEvent(event)
			
