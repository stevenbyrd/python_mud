from Inventory import Inventory


class ActorInventory(Inventory):
	def __init__(self, inventoryJson, owner):
		import EventHandlers.ActorInventory
		
		Inventory.__init__(self, inventoryJson, owner)

		self.attributes['equipment'] = {
				'head'		: None,
				'ears'		: None,
				'eyes'		: None,
				'face'		: None,
				'neck'		: [None],
				'body'		: None,
				'arms'		: None,
				'wrist'		: [None],
				'hand'		: None,
				'finger'	: [None],
				'waist'		: None,
				'legs'		: None,
				'feet'		: None,
				'shield'	: None,
				'weapon'	: [None],
		}
		
		
		self.addEventHandler(EventHandlers.ActorInventory.ActorAttemptedDropHandler())
		self.addEventHandler(EventHandlers.ActorInventory.ItemDroppedHandler())
		self.addEventHandler(EventHandlers.ActorInventory.ActorInitiatedItemGrabHandler())
		self.addEventHandler(EventHandlers.ActorInventory.ActorGrabbedItemHandler())
		
		
	def listItems(self):
		retVal = 'You don\'t have anything.'
		
		if len(self.attributes['items']) > 0:
			retVal = 'You have:'
			
			for item in self.attributes['items']:
				retVal = '{} {} {},'.format(retVal, item.attributes['adjective'], item.attributes['name'])
				
			retVal = retVal[0:-1]
		
		return retVal