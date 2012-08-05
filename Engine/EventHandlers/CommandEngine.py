from Event.Event import Event
from Event.EventHandler import EventHandler

class CommandExecutionEventHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'execute_command'

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		cmdName		= event.attributes['data']['command']

		if cmdName == 'quit':
			player											= event.attributes['data']['source']
			connection										= player.attributes['connection']
			logoutEvent										= Event()
			logoutEvent.attributes['signature']				= 'player_logout'
			logoutEvent.attributes['data']['connection']	= connection

			receiver.emitEvent(logoutEvent)
		else:
			commandList = receiver.attributes['commandList']
			command		= commandList['go']
			source		= event.attributes['data']['source']

			if commandList.has_key(cmdName):					
				command = commandList[cmdName]
				args	= event.attributes['data']['args']
			else:
				args = [cmdName]
			
			command.execute(source, args)