from Event.Event import Event
from Event.EventHandler import EventHandler
from Event.EventReceiver import EventReceiver
from Humanoid import Humanoid
from Menu.RootMenu import RootMenu
import Engine.ActorEngine


class Player(Humanoid):
	def __init__(self, actorJSON):		
		Humanoid.__init__(self, actorJSON)

		self.attributes['connection']	= None
		self.attributes['menus']		= []
		
		self.attributes['menus'].append(RootMenu(self))
		
		if actorJSON != None:
			self.addEventHandlerByNameWithAdjusters('Actor.EventHandlers.Player.ReceivedNotificationHandler', None)
			self.addEventHandlerByNameWithAdjusters('Actor.EventHandlers.Player.ReceivedFeedbackHandler', None)
			self.addEventHandlerByNameWithAdjusters('Actor.EventHandlers.Player.ActorAttemptedDropHandler', None)
			self.addEventHandlerByNameWithAdjusters('Actor.EventHandlers.Player.ItemDroppedHandler', None)
			self.addEventHandlerByNameWithAdjusters('Actor.EventHandlers.Player.ActorInitiatedItemGrabHandler', None)
			self.addEventHandlerByNameWithAdjusters('Actor.EventHandlers.Player.ActorGrabbedItemHandler', None)
			self.addEventHandlerByNameWithAdjusters('Actor.EventHandlers.Player.ActorViewedEquipmentHandler', None)
			
		
	
	def send(self, message):
		if message != None and len(message) > 0:
			self.attributes['connection'].send(message)
	
	
	def sendFinal(self, message):
		if message != None and len(message) > 0:
			self.attributes['connection'].sendFinal('\n\r' + message)
		
	
	def insertCommand(self, command, args = None):
		commandEvent	= Event()
		
		commandEvent.attributes['signature']			= 'execute_command'
		commandEvent.attributes['data']['command']		= command
		commandEvent.attributes['data']['args']			= args
		commandEvent.attributes['data']['source']		= self

		Engine.ActorEngine.emitEvent(commandEvent)