from Menu import Menu
import Engine.RoomEngine

class ExamineInventoryItemMenu(Menu):
	def __init__(self, player):
		Menu.__init__(self, player)
		
		
		self.attributes['options'] = {
		}
		
		inventory	= player.attributes['inventory']
		options		= {}
		count		= 1
		items		= []
		equipped	= []
		
		for key in inventory.attributes['equipment'].keys():
			equippedItem = inventory.attributes['equipment'][key]
			
			if key == 'Neck' or key == 'Wrist' or key == 'Finger':
				for item in equippedItem:
					if item != None:
						equipped.append(item)
			else:
				if equippedItem != None:
					equipped.append(equippedItem)	
		
		for item in equipped:
			key				= '{}'.format(count)
			itemName		= '. {} (Equipped)'.format(item.attributes['name'])
			function		= self.createViewer(item)
			options[key]	= (itemName, function)
			
			count = count + 1
		
		for item in inventory.attributes['items']:
			key				= '{}'.format(count)
			itemName		= '. {}'.format(item.attributes['name'])
			function		= self.createViewer(item)
			options[key]	= (itemName, function)
			
			count = count + 1
		
		options['{}'.format(count)] = ('. Cancel', self.cancelMenu)
		
		self.attributes['options'] = options
		
		
	def createViewer(self, item):
		return lambda : self.executeCommand('look', [item])