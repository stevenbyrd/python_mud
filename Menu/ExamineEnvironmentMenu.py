from Menu import Menu
from IteratorMenu import IteratorMenu
import Engine.RoomEngine

class ExamineEnvironmentMenu(Menu):
	def __init__(self, player):
		Menu.__init__(self, player)
		
		room		= Engine.RoomEngine.getRoom(player.attributes['roomID'])
		inventory	= room.attributes['inventory']
		
		self.attributes['options'] = {
			'1' : ('. Players', lambda : self.pushMenu(IteratorMenu(player, 
																	lambda p : room.attributes['players'],
																	'name',
																	'look',
																	False))),
																	
			'2' : ('. NPCs', lambda : self.pushMenu(IteratorMenu(player,
																lambda p : room.attributes['npcs'],
																'name',
																'look',
																False))),
																
			'3' : ('. Items', lambda : self.pushMenu(IteratorMenu(player,
																lambda p : inventory.attributes['items'] + inventory.attributes['permanent_items'],
																'name',
																'look',
																False))),
			'4' : ('. Cancel', lambda : self.cancelMenu())
		}