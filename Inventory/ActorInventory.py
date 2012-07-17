from Inventory import Inventory


class ActorInventory(Inventory):
	def __init__(self, inventoryJson, owner):
		import EventHandlers.ActorInventory
		
		Inventory.__init__(self, inventoryJson, owner)

		self.attributes['equipment'] = {
				'Head'		: None,
				'Ears'		: None,
				'Eyes'		: None,
				'Face'		: None,
				'Neck'		: [None, None],
				'Body'		: None,
				'Arms'		: None,
				'Wrist'		: [None, None],
				'Hands'		: None,
				'Finger'	: [None, None],
				'Waist'		: None,
				'Legs'		: None,
				'Feet'		: None,
				'Shield'	: None,
				'Wielded'	: None,
		}
		
		if inventoryJson.has_key('equipment'):
			equipment = inventoryJson['equipment']
		
			for key in equipment.keys():
				self.attributes['equipment'][key] = self.createItem(equipment[key])

		
		self.addEventHandler(EventHandlers.ActorInventory.ActorAttemptedDropHandler())
		self.addEventHandler(EventHandlers.ActorInventory.ItemDroppedHandler())
		self.addEventHandler(EventHandlers.ActorInventory.ActorInitiatedItemGrabHandler())
		self.addEventHandler(EventHandlers.ActorInventory.ActorGrabbedItemHandler())
		self.addEventHandler(EventHandlers.ActorInventory.ActorViewedEquipmentHandler())
		self.addEventHandler(EventHandlers.ActorInventory.ActorAttemptedItemEquipHandler())
		self.addEventHandler(EventHandlers.ActorInventory.ActorEquippedItemHandler())
		
		
	def listItems(self):
		retVal = 'You don\'t have anything.'
		
		if len(self.attributes['items']) > 0:
			retVal = 'You have:'
			
			for item in self.attributes['items']:
				retVal = '{} {} {},'.format(retVal, item.attributes['adjective'], item.attributes['name'])
				
			retVal = retVal[0:-1]
		
		return retVal