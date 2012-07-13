import threading
from Event.Event import Event
from time import sleep
import Engine.ConnectionEngine
import Engine.CommandEngine
from Event.EventEmitter import EventEmitter


def addEventSubscriber(subscriber):
	UpdateDriver.instance.addEventSubscriber(subscriber)
	
	
def removeEventSubscriber(subscriber):
	UpdateDriver.instance.removeEventSubscriber(subscriber)


class UpdateDriver(threading.Thread, EventEmitter):
	instance = None
	
	def __init__(self):
		threading.Thread.__init__(self)
		EventEmitter.__init__(self)
		
		UpdateDriver.instance = self
		
	
	def run(self):
		while True:
			Engine.ConnectionEngine.lock('openConnectionsSemaphore')
			
			for connection in Engine.ConnectionEngine.attribute('connectionList'):
				playerInput = connection.pollInput()
				parsedInput = playerInput.lower().strip()
				player		= connection.attributes['player']
				
				if len(playerInput) > 0:
					self.processInput(player, playerInput)
			
			Engine.ConnectionEngine.release('openConnectionsSemaphore')
			
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
		
			self.emitEvent(commandEvent)