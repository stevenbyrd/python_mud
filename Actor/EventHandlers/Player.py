import lib.ANSI
from .. import Player
from .. import NPC
from Event.EventHandler import EventHandler

class ReceivedNotificationHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='received_notification'
	
	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		message		= '\n\r### {}\n\r'.format(event.attributes['data']['message'])
		colored		= lib.ANSI.yellow(message)
			
		receiver.sendFinal(colored)
			
			
			
			

class ReceivedFeedbackHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'received_feedback'

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		feedback	= event.attributes['data']['feedback']
			
		receiver.sendFinal('{}'.format(feedback))





class EntityDescribedSelfHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='entity_described_self'
	
	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		description = event.attributes['data']['description']
		observer	= event.attributes['data']['observer']
		flagSet		= set(event.attributes['flags'])
		
		if 'room_is_dark' in flagSet and 'low_light_vision' not in flagSet:
			description = [lib.ANSI.yellow('It is too dark to see!')]
		
		if observer == receiver:
			if len(description) > 0:
				if len(description) == 1:
					receiver.sendFinal('{}\n\r'.format(description[0]))
				else:
					receiver.send('\n\r{}\n\r'.format(description[0]))
					
					if len(description) == 2:
						receiver.attributes['connection'].sendFinal('{}\n\r'.format(description[1]))
					else:
						for line in description[1:-1]:
							receiver.send('{}\n\r'.format(line))
						
						receiver.attributes['connection'].sendFinal('{}\n\r'.format(description[-1]))
						
						
						
						
						
class ActorAttemptedDropHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_attempted_item_drop'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['actor'] == receiver:
			if event.attributes['data']['itemName'] == '':			
				receiver.sendFinal('Drop what?')
				



class ItemDroppedHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'item_dropped'

	def handleEvent(self, event):		
		receiver	= event.attributes['receiver']
		itemName	= event.attributes['data']['item'].attributes['name']

		if event.attributes['data']['actor'] == receiver:
			receiver.sendFinal('You dropped {}.'.format(itemName))
		else:
			receiver.sendFinal('{} dropped {}.'.format(event.attributes['data']['actor'].attributes['name'], itemName))
			
			
			
			
class ActorInitiatedItemGrabHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_initiated_item_grab'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['actor'] == receiver:
			if event.attributes['data']['itemName'] == '':			
				receiver.sendFinal('Get what?')
				
				
				
				
				
class ActorGrabbedItemHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_grabbed_item'

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		itemName	= event.attributes['data']['item'].attributes['name']
		actor		= event.attributes['data']['actor']
		
		if actor == receiver:
			receiver.sendFinal('You picked up the {}.'.format(itemName))
		else:
			receiver.sendFinal('{} picked up a {}.'.format(actor.attributes['name'], itemName))
			
			
			
			
class ActorViewedEquipmentHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_viewed_equipment'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['actor'] == receiver:
			receiver.emitEvent(event)
			
			
			
			
class ActorAddedToRoomEventHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='actor_added_to_room'

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		actor		= event.attributes['data']['actor']
		
		if actor != receiver:
			arrivedString = ''
			
			if isinstance(actor, Player.Player):
				arrivedString = actor.attributes['name']
			elif isinstance(actor, NPC.NPC):
				arrivedString = '{} {}'.format(actor.attributes['adjective'].upper(), actor.attributes['name'])
				
			receiver.sendFinal('{} just arrived.'.format(arrivedString))




class ActorEmotedEventHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='actor_emoted'
	
	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		emoter		= event.attributes['data']['emoter']
		target		= event.attributes['data']['target']
		text		= None
		
		if emoter == receiver:
			text = event.attributes['data']['emoterText']
		elif target != None and target == receiver:
			text = event.attributes['data']['targetText']
		else:
			text = event.attributes['data']['audienceText']
		
		if text != None and text != '':
			text = text.replace('#emoter#', emoter.attributes['name'])
			
			if target != None:
				text = text.replace('#target#', target.attributes['name'])
			
			receiver.sendFinal(text)
			
			
			

class ActorMovedFromRoomEventHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='actor_moved_from_room'
	
	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		actor		= event.attributes['data']['actor']
		exitName	= event.attributes['data']['exit'].attributes['name']
		
		if actor == receiver:
			receiver.sendFinal('You leave {}.'.format(exitName))
		else:
			receiver.sendFinal('{} leaves {}.'.format(actor.attributes['name'], exitName))
			
