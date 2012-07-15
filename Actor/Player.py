from Event.EventHandler import EventHandler
from Event.EventReceiver import EventReceiver
from Humanoid import Humanoid
import lib.ANSI


class Player(Humanoid):
	def __init__(self, actorJSON):
		Humanoid.__init__(self, actorJSON)

		attributes = {
			'connection' : None
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
		

		self.attributes['event_handlers'].append(ReceivedNotificationHandler())
		self.attributes['event_handlers'].append(ReceivedFeedbackHandler())
		self.attributes['event_handlers'].append(EntityDescribedSelfHandler())
		
	
	def send(self, message):
		if message != None and len(message) > 0:
			self.attributes['connection'].send(message)
	
	
	def sendFinal(self, message):
		if message != None and len(message) > 0:
			self.attributes['connection'].sendFinal('\n\r' + message)
		
	
	def insertCommand(self, command):
		self.attributes['connection'].attributes['inputBuffer'].append(command)
		
		
		
		

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





class EntityDescribedSelfHandler:#(EventHandler):
	def __init__(self):
		#EventHandler.__init__(self)
		self.attributes = {'signature':'entity_described_self'}
		#self.attributes['function']		= self.entityDescribedSelf

	
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