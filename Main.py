from Engine.ConnectionEngine import ConnectionEngine
from Engine.RoomEngine import RoomEngine
from Engine.ActorEngine import ActorEngine
from Engine.CommandEngine import CommandEngine
from Driver.LoginListener import LoginListener
from Driver.InputDriver import InputDriver
from Driver.OutputDriver import OutputDriver
from Driver.RoomDriver import RoomDriver
from Driver.ConnectionListUpdater import ConnectionListUpdater
from Driver.UpdateDriver import UpdateDriver

class Main:
	def __init__(self):
		self.attributes = {
			'commandList' : {}
		}
		
		ConnectionEngine()
		RoomEngine()
		ActorEngine()
		CommandEngine()
		

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





if __name__ == "__main__":
	Main()