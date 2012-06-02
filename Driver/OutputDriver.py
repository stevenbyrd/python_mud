import threading
from time import sleep
from Engine import ConnectionEngine

class OutputDriver(threading.Thread):
	def run(self):
		while True:
			ConnectionEngine.lock('openConnectionsSemaphore')
			
			for connection in ConnectionEngine.attribute('connectionList'):
				try:
					for line in connection.attributes['outputBuffer']:
						connection.attributes['socket'].send(line)
						
					connection.attributes['outputBuffer'] = []
				
				except:
					#socket unavailable for now, we'll get it next time
					pass
			
			ConnectionEngine.release('openConnectionsSemaphore')
			
			sleep(0.005)