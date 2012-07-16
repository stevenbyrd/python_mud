from Inventory import Inventory


class ActorInventory(Inventory):
	def __init__(self, inventoryJson, owner):
		import EventHandlers.ActorInventory
		from Item.Equipable.Wieldable import Wieldable
		
		Inventory.__init__(self, inventoryJson, owner)

		self.attributes['equipment'] = {
				'head'		: None,
				'ears'		: None,
				'eyes'		: None,
				'face'		: None,
				'neck'		: [None, None],
				'body'		: None,
				'arms'		: None,
				'wrist'		: [None, None],
				'hands'		: None,
				'finger'	: [None, None],
				'waist'		: None,
				'legs'		: None,
				'feet'		: None,
				'shield'	: None,
				'wielded'	: None,
		}
		
		if inventoryJson.has_key('equipment'):
			equipment = inventoryJson['equipment']
		
			for key in equipment.keys():
				itemJson = equipment[key]
			
				if key == 'wielded':
					self.attributes['equipment'][key] = Wieldable(itemJson, self)
		
		self.addEventHandler(EventHandlers.ActorInventory.ActorAttemptedDropHandler())
		self.addEventHandler(EventHandlers.ActorInventory.ItemDroppedHandler())
		self.addEventHandler(EventHandlers.ActorInventory.ActorInitiatedItemGrabHandler())
		self.addEventHandler(EventHandlers.ActorInventory.ActorGrabbedItemHandler())
		self.addEventHandler(EventHandlers.ActorInventory.ActorViewedEquipmentHandler())
		
		
	def listItems(self):
		retVal = 'You don\'t have anything.'
		
		if len(self.attributes['items']) > 0:
			retVal = 'You have:'
			
			for item in self.attributes['items']:
				retVal = '{} {} {},'.format(retVal, item.attributes['adjective'], item.attributes['name'])
				
			retVal = retVal[0:-1]
		
		return retVal