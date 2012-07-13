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
		
		self.addEventHandler(ActorMovedFromRoomEventHandler())
		self.addEventHandler(ActorAddedToRoomEventHandler())
		self.addEventHandler(ReceivedNotificationHandler())
		self.addEventHandler(ActorEmotedHandler())
		self.addEventHandler(ReceivedFeedbackHandler())
		self.addEventHandler(EntityDescribedSelfHandler())
		
	
	def send(self, message):
		self.attributes['connection'].send(message)
	
	
	def sendFinal(self, message):
		self.attributes['connection'].sendFinal('\n\r' + message)
		
	
	def insertCommand(self, command):
		self.attributes['connection'].attributes['inputBuffer'].append(command)
		
		
		
		

class ActorMovedFromRoomEventHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'actor_moved_from_room'
		self.attributes['function']		= self.actorMovedFromRoom

	
	def actorMovedFromRoom(self, receiver, event):
		actor	= event.attributes['data']['actor']
		exit	= event.attributes['data']['exit']
		room	= event.attributes['data']['room']
		message	= ''
		
		if actor == receiver:
			message = 'You leave {}.'.format(exit.attributes['name'])
		else:
			message	= '{} leaves {}.'.format(actor.attributes['name'], exit.attributes['name'])
			
		if message != None and len(message) > 0:
			receiver.sendFinal(message)
		
				
				

class ActorAddedToRoomEventHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'actor_added_to_room'
		self.attributes['function']		= self.actorAddedToRoom

	
	def actorAddedToRoom(self, receiver, event):
		actor = event.attributes['data']['actor']
		room	= event.attributes['data']['room']
		
		if actor != receiver:
			name = actor.attributes['name']
			
			receiver.sendFinal('{} just arrived.'.format(name))
		
		
		

class ReceivedNotificationHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'received_notification'
		self.attributes['function']		= self.receiveNotification
	
	def receiveNotification(self, receiver, event):
		actor = event.attributes['data']['actor']
		
		#actor == None indicates a broadcast
		if actor == receiver or actor == None:
			message = '\n\r### {}\n\r'.format(event.attributes['data']['message'])
			colored	= lib.ANSI.yellow(message)
			
			receiver.sendFinal(colored)





class ActorEmotedHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'actor_emoted'
		self.attributes['function']		= self.actorEmoted
	
	def actorEmoted(self, receiver, event):
		emoter	= event.attributes['data']['emoter']
		target	= event.attributes['data']['target']
		text	= None
		
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




class ReceivedFeedbackHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'received_feedback'
		self.attributes['function']		= self.receivedFeedback

	
	def receivedFeedback(self, receiver, event):
		if event.attributes['data']['actor'] == receiver:
			feedback = event.attributes['data']['feedback']
			
			receiver.sendFinal('{}'.format(feedback))




class EntityDescribedSelfHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'entity_described_self'
		self.attributes['function']		= self.entityDescribedSelf

	
	def entityDescribedSelf(self, receiver, event):
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