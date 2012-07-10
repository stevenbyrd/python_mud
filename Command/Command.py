from Event.EventHandler import EventHandler
from Event.EventReceiver import EventReceiver
from Event.EventEmitter import EventEmitter
import Engine.CommandEngine

class Command(EventReceiver, EventEmitter):
	def __init__(self):
		EventReceiver.__init__(self)
		EventEmitter.__init__(self)

		commandExecutionHandler = EventHandler()

		commandExecutionHandler.attributes['signature'] = 'execute_command'
		commandExecutionHandler.attributes['function']	= self.execute

		self.addEventHandler(commandExecutionHandler)
		
		Engine.CommandEngine.addEventSubscriber(self)