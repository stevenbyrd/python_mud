from Event.EventReceiver import EventReceiver
from Event.Event import Event
import Engine.ActorEngine


class Menu(EventReceiver):
	def __init__(self, player):
		EventReceiver.__init__(self)
		
		attributes = {
			'player'	: player,
			'options'	: {}
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
		
		self.addEventHandlerByNameWithAdjusters('Menu.EventHandlers.MenuOptionChosenHandler.MenuOptionChosenHandler', None)
	
	
	def executeCommand(self, command, args, popAfterExecute = False):
		commandEvent								= Event()
		commandEvent.attributes['signature']		= 'execute_command'
		commandEvent.attributes['data']['command']	= command
		commandEvent.attributes['data']['args']		= args
		commandEvent.attributes['data']['source']	= self.attributes['player']

		if popAfterExecute:
			player		= self.attributes['player']
			menuStack	= player.attributes['menus']
		
			if len(menuStack) > 1:
				menuStack.pop()

		Engine.ActorEngine.emitEvent(commandEvent)
		
		
	def cancelMenu(self):
		player		= self.attributes['player']
		menuStack	= player.attributes['menus']
		
		if len(menuStack) > 1:
			menuStack.pop()
			player.insertCommand('look')
			
			
	def pushMenu(self, menu):
		player		= self.attributes['player']
		menuStack	= player.attributes['menus']
		
		menuStack.append(menu)
		
		player.insertCommand('look')
		
		
	def getOptions(self):
		optionList = ''
		
		for key in sorted(self.attributes['options'].keys()):
			option		= self.attributes['options'][key]
			optionList	= '{}\n\r\t    {}{}'.format(optionList, key, option[0])
			
		return optionList