from Event.EventHandler import EventHandler
from Event.EventReceiver import EventReceiver
from Humanoid import Humanoid
import lib.ANSI

class Player(Humanoid):
	def __init__(self):
		Humanoid.__init__(self)
		attributes = {
			'connection' : None
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
		
		self.addEventHandler(ActorEnteredRoomHandler())
		self.addEventHandler(ReceivedNotificationHandler())
		self.addEventHandler(EntityDescribedSelfHandler())
		self.addEventHandler(ReceivedFeedbackHandler())
		self.addEventHandler(ActorEmotedHandler())
				
		
	def send(self, message):
		self.attributes['connection'].send(message) 
		
	
	def sendFinal(self, message):
		self.attributes['connection'].sendFinal('\n\r' + message)
		
		
	def insertCommand(self, command):
		self.attributes['connection'].attributes['inputBuffer'].append(command)
		
		
		

class ReceivedNotificationHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'received_notification'
		self.attributes['function']		= (lambda receiver, event :
												(lambda : 
													receiver.sendFinal((lambda :
																 		lib.ANSI.yellow('### {} '.format((lambda : 
																											event.attributes['data']['message'])())))()))())









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