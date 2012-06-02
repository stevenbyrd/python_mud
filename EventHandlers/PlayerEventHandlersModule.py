from EventModule import *
import lib.ANSI


class ReceivedNotificationHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'received_notification'
		self.attributes['function']		= (lambda receiver, event : 
												(lambda : 
													receiver.sendFinal((lambda :
																 		lib.ANSI.yellow('### {} '.format((lambda : 
																											event.attributes['data']['message'])())))()))())
																											
																											


class WasObservedHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'was_observed'
		self.attributes['function']		= self.wasObserved
		
		#(lambda receiver, event:
		#		"observer".receiveEvent((lambda : SET((lambda : SET((lambda : Event())().attributes['signature'], 'entity_described_self'))().attributes['data']['description'], (lambda : receiver.attributes['description'][:])()))()))
																											
	def wasObserved(self, receiver, event):
			observer										= event.attributes['data']['observer']
			description										= receiver.attributes['description'][:]
			describeEvent									= Event()
			describeEvent.attributes['signature']			= 'entity_described_self'
			describeEvent.attributes['data']['description'] = description

			observer.receiveEvent(describeEvent)
			
			
			
			
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
			
			
			


class ActorEnteredRoomHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'player_entered'
		self.attributes['function']		= self.playerEnteredRoom


	def playerEnteredRoom(self, receiver, event):
		player	= event.attributes['data']['player']
		name	= player.attributes['name']

		receiver.sendFinal('{} just arrived.'.format(name))
		
		
		
		
		
		
class EntityDescribedSelfHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'entity_described_self'
		self.attributes['function']		= self.entityDescribedSelf
	
	
	def entityDescribedSelf(self, receiver, event):
		description = event.attributes['data']['description']
		
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
					
					
					
					
					
class ReceivedFeedbackHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'received_feedback'
		self.attributes['function']		= self.receivedFeedback
		
		
	def receivedFeedback(self, receiver, event):
		feedback = event.attributes['data']['feedback']

		receiver.sendFinal('{}'.format(feedback))
		
		
		
		
		
class PlayerLoginHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'player_login'
		self.attributes['function']		= self.playerLogin

	def playerLogin(self, receiver, event):
		player		= event.attributes['data']['player']
		connection	= player.attributes['connection']

		receiver.addConnection(connection)
		
		
		
		

class PlayerLogoutHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'player_logout'
		self.attributes['function']		= self.playerLogout
		
	
	def playerLogout(self, receiver, event):
		connection = event.attributes['data']['connection']

		receiver.removeConnection(connection)