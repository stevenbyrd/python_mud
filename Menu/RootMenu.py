from Menu import Menu
from MovementMenu import MovementMenu

class RootMenu(Menu):
	def __init__(self, player):
		Menu.__init__(self, player)
		
		self.attributes['options'] = {
			'1'	: ('. Move', lambda : self.pushMenu(MovementMenu(player)))
		}