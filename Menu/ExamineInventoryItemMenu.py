from Menu import Menu
import Engine.RoomEngine

class ExamineInventoryItemMenu(Menu):
	def __init__(self, player):
		Menu.__init__(self, player)
		
		
		self.attributes['options'] = {
			'1' : ('. Cancel', lambda : self.cancelMenu())
		}
		
		'''
		inventory	= player.attributes['inventory']
		options		= {}
		count		= 1
		
		for exit in room.attributes['exits']:
			key				= '{}'.format(count)
			exitName		= '. {}'.format(exit.attributes['name'])
			function		= self.createMover(exit.attributes['name'])
			options[key]	= (exitName, function)
			
			count = count + 1
		
		options['{}'.format(count)] = ('. Cancel', self.cancelMenu)
		
		self.attributes['options'] = options
		
		
	def createMover(self, direction):
		return lambda : self.executeCommand('go', [direction], True)'''