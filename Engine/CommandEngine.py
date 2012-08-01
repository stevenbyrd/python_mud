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
		import ActorEngine

		Engine.__init__(self)
		
		attributes = {
			'commandList' : {},
			'emoteList': []
		}

		for key in attributes.keys():
			self.attributes[key] = attributes[key]

		self.addEventHandlerByNameWithAdjusters('Engine.EventHandlers.CommandEngine.CommandExecutionEventHandler', None)
		
		CommandEngine.instance = self
		
		for subscriber in CommandEngine.subscribers:
			self.addEventSubscriber(subscriber)
			
		CommandEngine.subscribers = []
		
		self.buildCommandList()
		
		Driver.UpdateDriver.addEventSubscriber(self)
		ActorEngine.addEventSubscriber(self)
	
	
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
		cmdList['inventory']	= Command.loadCommand('Inventory')
		cmdList['i']			= cmdList['inventory']
		cmdList['inven']		= cmdList['inventory']
		cmdList['inv']			= cmdList['inventory']
		cmdList['drop']			= Command.loadCommand('Drop')
		cmdList['grab']			= Command.loadCommand('Grab')
		cmdList['get']			= cmdList['grab']
		cmdList['equip']		= Command.loadCommand('Equip')
		cmdList['eq']			= cmdList['equip']
		cmdList['equipment']	= cmdList['equip']
		cmdList['wear']			= Command.loadCommand('Wear')
		cmdList['wield']		= Command.loadCommand('Wield')
		cmdList['remove']		= Command.loadCommand('Remove')
		cmdList['rem']			= cmdList['remove']
		
		
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
					
					
					

