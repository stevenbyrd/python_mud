from Event.EventHandler import EventHandler
from Event.EventReceiver import EventReceiver

class Command(EventReceiver):
	def __init__(self):
		EventReceiver.__init__(self)

		commandExecutionHandler = EventHandler()

		commandExecutionHandler.attributes['signature'] = 'execute_command'
		commandExecutionHandler.attributes['function']	= self.execute

		self.addEventHandler(commandExecutionHandler)