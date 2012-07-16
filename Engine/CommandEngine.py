from Engine import Engine


def addEventSubscriber(subscriber):
	if CommandEngine.instance != None:
		CommandEngine.instance.addEventSubscriber(subscriber)
	else:
		CommandEngine.subscribers.append(subscriber)
	

def emitEvent(event):
	CommandEngine.instance.emitEvent(event)


class CommandEngine(Engine):
	instance 	= None
	subscribers = []
	
	def __init__(self):
		import Driver.UpdateDriver
		import EventHandlers.CommandEngine

		Engine.__init__(self)
		
		attributes = {
			'commandList' : {},
			'emoteList': []
		}

		for key in attributes.keys():
			self.attributes[key] = attributes[key]

		self.addEventHandler(EventHandlers.CommandEngine.CommandExecutionEventHandler())
		
		CommandEngine.instance = self
		
		for subscriber in CommandEngine.subscribers:
			self.addEventSubscriber(subscriber)
			
		CommandEngine.subscribers = []
		
		self.buildCommandList()
		
		Driver.UpdateDriver.addEventSubscriber(self)
	
	
	def buildCommandList(self):
		import os
		import json
		import Command
		from Command.Emote import Emote
		
		cmdList = self.attributes['commandList']
		
		cmdList['go']			= Command.loadCommand('Go')
		cmdList['look']			= Command.loadCommand('Look')
		cmdList['l']			= cmdList['look']
		cmdList['ls']			= cmdList['look']
		cmdList['say']			= Command.loadCommand('Say')
		cmdList['cast']			= Command.loadCommand('Cast')
		cmdList['c']			= cmdList['cast']
		cmdList['i']			= Command.loadCommand('Inventory')
		cmdList['inventory']	= cmdList['i']
		cmdList['inven']		= cmdList['i']
		cmdList['drop']			= Command.loadCommand('Drop')
		cmdList['grab']			= Command.loadCommand('Grab')
		cmdList['get']			= cmdList['grab']
		cmdList['equip']		= Command.loadCommand('Equip')
		cmdList['eq']			= cmdList['equip']
		cmdList['equipment']	= cmdList['equip']
		
		
		# EMOTES
		currentDir	= os.getcwd()
		emoteDir	= currentDir + '/Content/commands/emotes' 
		fileList	= os.listdir(emoteDir)

		for fname in fileList:			
			if fname.endswith('.txt'):
				filePath		= '{}/{}'.format(emoteDir, fname)
				emoteFile		= open(filePath, 'r')
				jsonString		= emoteFile.read()
				jsonObj			= json.loads(jsonString)
				emote			= Emote(jsonObj['template'])

				emoteFile.close()

				for cmdName in jsonObj['commandNames']:
					cmdList[cmdName] = emote
					
				self.attributes['emoteList'].append(emote)
					
					
					

