import threading
from time import sleep
from Engine import ConnectionEngine

class InputDriver(threading.Thread):
	def run(self):
		while True:
			ConnectionEngine.lock('openConnectionsSemaphore')
			
			for connection in ConnectionEngine.attribute('connectionList'):
				try:
					playerInput = connection.attributes['socket'].recv(1024)
					playerInput = playerInput.strip()
				
					if len(playerInput) > 0:
						connection.attributes['inputBuffer'].append(playerInput)
				except:
					pass
					#socket unavailable for now, we'll get it next time
			
			ConnectionEngine.release('openConnectionsSemaphore')
			
			sleep(0.005)