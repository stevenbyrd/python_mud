from Event.EventHandler import EventHandler
from Event.EventReceiver import EventReceiver
from Humanoid import Humanoid


class Player(Humanoid):
	def __init__(self, actorJSON):
		import EventHandlers.Player
		
		Humanoid.__init__(self, actorJSON)

		self.attributes['connection'] = None
		
		if actorJSON != None:
			self.addEventHandler(EventHandlers.Player.ReceivedNotificationHandler())
			self.addEventHandler(EventHandlers.Player.ReceivedFeedbackHandler())
			self.addEventHandler(EventHandlers.Player.EntityDescribedSelfHandler())
			self.addEventHandler(EventHandlers.Player.ActorAttemptedDropHandler())
			self.addEventHandler(EventHandlers.Player.ItemDroppedHandler())
			self.addEventHandler(EventHandlers.Player.ActorInitiatedItemGrabHandler())
			self.addEventHandler(EventHandlers.Player.ActorGrabbedItemHandler())
			self.addEventHandler(EventHandlers.Player.ActorViewedEquipmentHandler())
			self.addEventHandler(EventHandlers.Player.ActorAddedToRoomEventHandler())
		
	
	def send(self, message):
		if message != None and len(message) > 0:
			self.attributes['connection'].send(message)
	
	
	def sendFinal(self, message):
		if message != None and len(message) > 0:
			self.attributes['connection'].sendFinal('\n\r' + message)
		
	
	def insertCommand(self, command):
		self.attributes['connection'].attributes['inputBuffer'].append(command)