def loadCommand(commandName):
	commandModule	= __import__('Command.{}'.format(commandName))	
	classModule		= getattr(commandModule, commandName)
	commandClass	= getattr(classModule, commandName)
	
	return commandClass()