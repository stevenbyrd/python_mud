from Menu import Menu
from ExamineSelfMenu import ExamineSelfMenu
from ExamineEnvironmentMenu import ExamineEnvironmentMenu

class ExamineMenu(Menu):
	def __init__(self, player):
		Menu.__init__(self, player)
		
		self.attributes['options'] = {
			'1' : ('. Youself', lambda : self.pushMenu(ExamineSelfMenu(player))),
			'2' : ('. Environment', lambda : self.pushMenu(ExamineEnvironmentMenu(player))),
			'3' : ('. Cancel', lambda : self.cancelMenu())
		}