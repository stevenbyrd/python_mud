from ConnectionModule import *
import ConnectionModule
from EngineModule import *
import EngineModule
import threading
from time import sleep

class GameMain:
	def __init__(self):
		self.attributes = {
			'commandList' : {}
		}
		
		ConnectionModule.connectionList	= ConnectionList()
		EngineModule.roomEngine			= RoomEngine()
		EngineModule.actorEngine		= ActorEngine()
		EngineModule.commandEngine		= CommandEngine()
		
		EngineModule.roomEngine.buildWorld()
		EngineModule.commandEngine.buildCommandList()

		loginListener		= LoginListener()
		inputDriver			= InputDriver()
		outputDriver		= OutputDriver()
		updateDriver		= UpdateDriver()
		roomDriver			= RoomDriver()
		connectionUpdater	= ConnectionListUpdater()	

		loginListener.start()
		inputDriver.start()
		outputDriver.start()
		updateDriver.start()
		roomDriver.start()
		connectionUpdater.start()





class InputDriver(threading.Thread):
	def run(self):
		while True:
			ConnectionModule.connectionList.attributes['openConnectionsSemaphore'].acquire()
			
			for connection in ConnectionModule.connectionList.attributes['connectionList']:
				try:
					playerInput = connection.attributes['socket'].recv(1024)
					playerInput = playerInput.strip()
				
					if len(playerInput) > 0:
						connection.attributes['inputBuffer'].append(playerInput)
				except:
					pass
					#socket unavailable for now, we'll get it next time
			
			ConnectionModule.connectionList.attributes['openConnectionsSemaphore'].release()
			
			sleep(0.005)



class OutputDriver(threading.Thread):
	def run(self):
		while True:
			ConnectionModule.connectionList.attributes['openConnectionsSemaphore'].acquire()
			
			for connection in ConnectionModule.connectionList.attributes['connectionList']:
				try:
					for line in connection.attributes['outputBuffer']:
						connection.attributes['socket'].send(line)
						
					connection.attributes['outputBuffer'] = []
				
				except:
					#socket unavailable for now, we'll get it next time
					pass
			
			ConnectionModule.connectionList.attributes['openConnectionsSemaphore'].release()
			
			sleep(0.005)



class UpdateDriver(threading.Thread):
	def run(self):
		while True:
			ConnectionModule.connectionList.attributes['openConnectionsSemaphore'].acquire()
			
			for connection in ConnectionModule.connectionList.attributes['connectionList']:
				playerInput	= connection.pollInput()
				parsedInput	= playerInput.lower().strip()
				player		= connection.attributes['player']
				
				if len(playerInput) > 0:
					self.processInput(player, playerInput)
			
			ConnectionModule.connectionList.attributes['openConnectionsSemaphore'].release()
			
			sleep(0.005)
	
	
	def processInput(self, player, inputStr):		
		parsedInput = inputStr.split(' ')
		
		if len(parsedInput) > 0:
			cmd				= parsedInput[0]
			args			= parsedInput[1:]
			commandEvent	= Event()
			
			commandEvent.attributes['signature']			= 'execute_command'
			commandEvent.attributes['data']['command']		= cmd
			commandEvent.attributes['data']['args']			= args
			commandEvent.attributes['data']['source']		= player
		
			EngineModule.commandEngine.receiveEvent(commandEvent);
	

class RoomDriver(threading.Thread):
	def run(self):
		pass
		
		
if __name__ == "__main__":
    GameMain()