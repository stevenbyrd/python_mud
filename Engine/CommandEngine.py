from Event.Event import Event
from Event.EventHandler import EventHandler
from Event.EventReceiver import EventReceiver
from Command.Command import Command
from Command.Say import Say
from Command.Emote import Emote
from Command.Look import Look
from Command.Go import Go
from Engine import *
import os
import json


def receiveEvent(event):
	CommandEngine.instance.receiveEvent(event)
	

class CommandEngine(EventReceiver):
	instance = None
	
	
	def __init__(self):
		EventReceiver.__init__(self)
		attributes = {
			'commandList' : {}
		}

		for key in attributes.keys():
			self.attributes[key] = attributes[key]

		self.addEventHandler(CommandExecutionEventHandler())
		
		CommandEngine.instance = self
		
		self.buildCommandList()
	
	
	def buildCommandList(self):
		cmdList = self.attributes['commandList']
		
		cmdList['go']	= Go()
		cmdList['look']	= Look()
		cmdList['l']	= cmdList['look']
		cmdList['ls']	= cmdList['look']
		cmdList['say']	= Say()
		
		
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

			RoomEngine.receiveEvent(logoutEvent)
			ActorEngine.receiveEvent(logoutEvent)
			ConnectionEngine.receiveEvent(logoutEvent)
		else:
			commandList = receiver.attributes['commandList']
			command		= commandList['go']

			if commandList.has_key(cmdName):
				command = commandList[cmdName]

			command.receiveEvent(event)