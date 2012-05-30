from EventModule import *

class Go(EventReceiver):
	def __init__(self):
		EventReceiver.__init__(self)

		commandExecutionHandler = EventHandler()

		commandExecutionHandler.attributes['signature']	= 'execute_command'
		commandExecutionHandler.attributes['function']	= self.execute

		self.addEventHandler(commandExecutionHandler)
		

	def execute(self, event):
		args		= event.attributes['data']['args']
		connection	= event.attributes['data']['connection']
		
		#generate movement event