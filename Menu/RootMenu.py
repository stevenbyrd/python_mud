from Menu import Menu
from MovementMenu import MovementMenu
from ExamineMenu import ExamineMenu

class RootMenu(Menu):
	def __init__(self, player):
		Menu.__init__(self, player)
		
		self.attributes['options'] = {
			'1'	: ('. Move', lambda : self.pushMenu(MovementMenu(player))),
			'2' : ('. Examine', lambda : self.pushMenu(ExamineMenu(player)))
		}