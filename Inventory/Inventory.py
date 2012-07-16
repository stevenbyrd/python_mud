from Event.EventReceiver import EventReceiver
from Event.EventEmitter import EventEmitter


class Inventory(EventReceiver, EventEmitter):
	def __init__(self, inventoryJson, owner):		
		EventReceiver.__init__(self)
		EventEmitter.__init__(self)
		
		self.attributes['items']	= []
		self.attributes['owner']	= owner
		
		for itemJson in inventoryJson['items']:
			item = self.createItem(itemJson)
			
			if item != None:
				self.attributes['items'].append(item)
		
		owner.addEventSubscriber(self)
		
		
	def createItem(self, itemJson):
		if itemJson['itemType'] == 'wieldable':
			from Item.Equipable.Wieldable import Wieldable
			
			return Wieldable(itemJson, self)
				
		return None