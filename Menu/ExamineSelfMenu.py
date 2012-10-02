from Menu import Menu
from ExamineInventoryMenu import ExamineInventoryMenu

class ExamineSelfMenu(Menu):
	def __init__(self, player):
		Menu.__init__(self, player)
		
		self.attributes['options'] = {
			'1' : ('. Equipment and Description', lambda : self.executeCommand('look', [player], False)),
			'2' : ('. Inventory', lambda : self.pushMenu(ExamineInventoryMenu(player))),
			'3' : ('. Cancel', lambda : self.cancelMenu())
		}