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
		
		EngineModule.roomEngine.buildWorld()

		loginListener	= LoginListener()
		inputDriver		= InputDriver()
		outputDriver	= OutputDriver()
		updateDriver	= UpdateDriver()
		roomDriver		= RoomDriver()		

		loginListener.start()
		inputDriver.start()
		outputDriver.start()
		updateDriver.start()
		roomDriver.start()





class InputDriver(threading.Thread):
	def run(self):
		while True:
			ConnectionModule.connectionList.attributes['semaphore'].acquire()
			
			for connection in ConnectionModule.connectionList.attributes['connectionList']:
				try:
					playerInput = connection.attributes['socket'].recv(1024)
					playerInput = playerInput.strip()
				
					if len(playerInput) > 0:
						connection.attributes['inputBuffer'].append(playerInput)
				except:
					pass
					#socket unavailable for now, we'll get it next time
			
			ConnectionModule.connectionList.attributes['semaphore'].release()
			
			sleep(0.05)



class OutputDriver(threading.Thread):
	def run(self):
		while True:
			ConnectionModule.connectionList.attributes['semaphore'].acquire()
			
			for connection in ConnectionModule.connectionList.attributes['connectionList']:
				try:
					for line in connection.attributes['outputBuffer']:
						connection.attributes['socket'].send(line)
						
					connection.attributes['outputBuffer'] = []
				
				except:
					pass
					#socket unavailable for now, we'll get it next time
			
			ConnectionModule.connectionList.attributes['semaphore'].release()
			
			sleep(0.05)



class UpdateDriver(threading.Thread):
	def run(self):
		while True:
			for connection in ConnectionModule.connectionList.attributes['connectionList']:
				pass



class RoomDriver(threading.Thread):
	def run(self):
		pass
		
		
if __name__ == "__main__":
    GameMain()