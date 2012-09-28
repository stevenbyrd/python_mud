from Engine.ConnectionEngine import ConnectionEngine
from Engine.RoomEngine import RoomEngine
from Engine.ActorEngine import ActorEngine
from Engine.AffectEngine import AffectEngine
from Engine.CommandEngine import CommandEngine
from Engine.AffectEngine import AffectEngine
from Engine.ItemEngine import ItemEngine
from Driver.LoginListener import LoginListener
from Driver.InputDriver import InputDriver
from Driver.OutputDriver import OutputDriver
from Driver.TickDriver import TickDriver
from Driver.ConnectionListUpdater import ConnectionListUpdater
from Driver.UpdateDriver import UpdateDriver

class Main:
	def __init__(self):
		self.attributes = {
			'commandList' : {}
		}
		
		tickDriver			= TickDriver()
		loginListener		= LoginListener()
		inputDriver			= InputDriver()
		outputDriver		= OutputDriver()
		updateDriver		= UpdateDriver()
		connectionUpdater	= ConnectionListUpdater()
		
		CommandEngine()		
		ConnectionEngine()
		RoomEngine()
		ActorEngine()
		AffectEngine()
		ItemEngine()
		
		loginListener.start()
		inputDriver.start()
		outputDriver.start()
		updateDriver.start()
		tickDriver.start()
		connectionUpdater.start()
		




if __name__ == "__main__":
	Main()
