from Menu import Menu
from ExamineInventoryItemMenu import ExamineInventoryItemMenu

class ExamineInventoryMenu(Menu):
	def __init__(self, player):
		Menu.__init__(self, player)
		
		self.attributes['options'] = {
			'1' : ('. All items', lambda : self.executeCommand('inventory', None, False)),
			'2' : ('. Specific item', lambda : self.pushMenu(ExamineInventoryItemMenu(player))),
			'3' : ('. Cancel', lambda : self.cancelMenu())
		}