from Menu import Menu
from ExamineSelfMenu import ExamineSelfMenu

class ExamineMenu(Menu):
	def __init__(self, player):
		Menu.__init__(self, player)
		
		self.attributes['options'] = {
			'1' : ('. Youself', lambda : self.pushMenu(ExamineSelfMenu(player))),
			'2' : ('. Cancel', lambda : self.cancelMenu())
		}