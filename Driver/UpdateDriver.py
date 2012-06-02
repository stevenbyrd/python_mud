import threading
from Event.Event import Event
from time import sleep
from Engine import ConnectionEngine
from Engine import CommandEngine

class UpdateDriver(threading.Thread):
	def run(self):
		while True:
			ConnectionEngine.lock('openConnectionsSemaphore')
			
			for connection in ConnectionEngine.attribute('connectionList'):
				playerInput = connection.pollInput()
				parsedInput = playerInput.lower().strip()
				player		= connection.attributes['player']
				
				if len(playerInput) > 0:
					self.processInput(player, playerInput)
			
			ConnectionEngine.release('openConnectionsSemaphore')
			
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
		
			CommandEngine.receiveEvent(commandEvent)