from Menu import Menu


class IteratorMenu(Menu):
	def __init__(self, player, listGetter, attributeName, command, popMenu):
		Menu.__init__(self, player)
		
		options	= {}
		count	= 1
		
		for element in listGetter(player):
			key				= '{}'.format(count)
			option			= '. {}'.format(element.attributes[attributeName])
			function		= self.createLambda(element, command, popMenu)
			options[key]	= (option, function)
			
			count = count + 1
		
		options['{}'.format(count)] = ('. Cancel', self.cancelMenu)
		
		self.attributes['options'] = options
		
		
	def createLambda(self, element, command, popMenu):
		return lambda : self.executeCommand(command, [element], popMenu)