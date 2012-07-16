import lib.ANSI

class ReceivedNotificationHandler:
	def __init__(self):
		self.attributes = {'signature':'received_notification'}
	
	def handleEvent(self, event):
		actor = event.attributes['data']['actor']
		receiver	= event.attributes['receiver']
		
		#actor == None indicates a broadcast
		if actor == receiver or actor == None:
			message = '\n\r### {}\n\r'.format(event.attributes['data']['message'])
			colored	= lib.ANSI.yellow(message)
			
			receiver.sendFinal(colored)
			
			
			
			

class ReceivedFeedbackHandler:
	def __init__(self):
		self.attributes = {'signature': 'received_feedback'}

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['actor'] == receiver:
			feedback = event.attributes['data']['feedback']
			
			receiver.sendFinal('{}'.format(feedback))





class EntityDescribedSelfHandler:
	def __init__(self):
		self.attributes = {'signature':'entity_described_self'}
	
	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		description = event.attributes['data']['description']
		observer	= event.attributes['data']['observer']
		
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
						
						
						
						
						
class ActorAttemptedDropHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_attempted_item_drop'}

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['actor'] == receiver:
			if event.attributes['data']['itemName'] == '':			
				receiver.sendFinal('Drop what?')
				



class ItemDroppedHandler:
	def __init__(self):
		self.attributes = {'signature': 'item_dropped'}

	def handleEvent(self, event):		
		receiver	= event.attributes['receiver']
		itemName	= event.attributes['data']['item'].attributes['name']

		if event.attributes['data']['actor'] == receiver:
			receiver.sendFinal('You dropped {}.'.format(itemName))
		else:
			receiver.sendFinal('{} dropped {}.'.format(event.attributes['data']['actor'].attributes['name'], itemName))
			
			
			
			
class ActorInitiatedItemGrabHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_initiated_item_grab'}

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['actor'] == receiver:
			if event.attributes['data']['itemName'] == '':			
				receiver.sendFinal('Get what?')
				
				
				
				
				
class ActorGrabbedItemHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_grabbed_item'}

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		itemName	= event.attributes['data']['item'].attributes['name']
		actor		= event.attributes['data']['actor']
		
		if actor == receiver:
			receiver.sendFinal('You picked up the {}.'.format(itemName))
		else:
			receiver.sendFinal('{} picked up a {}.'.format(actor.attributes['name'], itemName))
			
			
			
			
class ActorViewedEquipmentHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_viewed_equipment'}

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['actor'] == receiver:
			receiver.emitEvent(event)
			