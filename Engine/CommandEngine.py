from Event.Event import Event
from Event.EventHandler import EventHandler
from Command.Command import Command
from Command.Say import Say
from Command.Emote import Emote
from Command.Look import Look
from Command.Go import Go
from Command.Cast import Cast
from Engine import Engine
from Driver import UpdateDriver
import os
import json


def addEventSubscriber(subscriber):
	CommandEngine.instance.addEventSubscriber(subscriber)


def addSubscriberForCommand(cmdName, subscriber):
	if cmdName == 'emote':
		for emote in CommandEngine.instance.attributes['emoteList']:
			emote.addEventSubscriber(subscriber)
	else:
		commandList = CommandEngine.instance.attributes['commandList']

		if commandList.has_key(cmdName):
			command = commandList[cmdName]
		
			command.addEventSubscriber(subscriber)


class CommandEngine(Engine):
	instance = None
	
	
	def __init__(self):
		Engine.__init__(self)
		attributes = {
			'commandList' : {},
			'emoteList': []
		}

		for key in attributes.keys():
			self.attributes[key] = attributes[key]

		self.addEventHandler(CommandExecutionEventHandler())
		
		CommandEngine.instance = self
		
		self.buildCommandList()
		
		UpdateDriver.addEventSubscriber(self)
	
	
	def buildCommandList(self):
		cmdList = self.attributes['commandList']
		
		cmdList['go']	= Go()
		cmdList['look']	= Look()
		cmdList['l']	= cmdList['look']
		cmdList['ls']	= cmdList['look']
		cmdList['say']	= Say()
		cmdList['cast']	= Cast()
		cmdList['c']	= cmdList['cast']
		
		
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
					
					
					

class CommandExecutionEventHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)

		self.attributes['signature']	= 'execute_command'
		self.attributes['function']		= self.executeCommand


	def executeCommand(self, receiver, event):
		cmdName = event.attributes['data']['command']

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

			if commandList.has_key(cmdName):
				command = commandList[cmdName]
				
			event.attributes['data']['commandInstance'] = command

			receiver.emitEvent(event)