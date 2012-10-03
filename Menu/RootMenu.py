from Menu import Menu
from IteratorMenu import IteratorMenu
from ExamineMenu import ExamineMenu
import Engine.RoomEngine

class RootMenu(Menu):
	def __init__(self, player):
		Menu.__init__(self, player)
		
		self.attributes['options'] = {
			'1'	: ('. Move', lambda : self.pushMenu(IteratorMenu(player,
																lambda p : Engine.RoomEngine.getRoom(p.attributes['roomID']).attributes['exits'],
																'name',
																'go',
																True))),
			'2' : ('. Examine', lambda : self.pushMenu(ExamineMenu(player)))
		}