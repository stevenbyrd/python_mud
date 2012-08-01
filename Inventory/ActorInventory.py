from Inventory import Inventory
from lib import ANSI


class ActorInventory(Inventory):
	def __init__(self, inventoryJson, owner):		
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
		
		if inventoryJson != None:
			if inventoryJson.has_key('equipment'):
				equipment = inventoryJson['equipment']
		
				for key in equipment.keys():
					self.attributes['equipment'][key] = self.createItem(equipment[key])

		
		self.addEventHandlerByNameWithAdjusters('Inventory.EventHandlers.ActorInventory.ActorAttemptedDropHandler', None)
		self.addEventHandlerByNameWithAdjusters('Inventory.EventHandlers.ActorInventory.ItemDroppedHandler', None)
		self.addEventHandlerByNameWithAdjusters('Inventory.EventHandlers.ActorInventory.ActorInitiatedItemGrabHandler', None)
		self.addEventHandlerByNameWithAdjusters('Inventory.EventHandlers.ActorInventory.ActorGrabbedItemHandler', None)
		self.addEventHandlerByNameWithAdjusters('Inventory.EventHandlers.ActorInventory.ActorViewedEquipmentHandler', None)
		self.addEventHandlerByNameWithAdjusters('Inventory.EventHandlers.ActorInventory.ActorAttemptedItemEquipHandler', None)
		self.addEventHandlerByNameWithAdjusters('Inventory.EventHandlers.ActorInventory.ActorEquippedItemHandler', None)
		self.addEventHandlerByNameWithAdjusters('Inventory.EventHandlers.ActorInventory.ActorAttemptedItemRemovalHandler', None)
		self.addEventHandlerByNameWithAdjusters('Inventory.EventHandlers.ActorInventory.ActorRemovedItemHandler', None)
		self.addEventHandlerByNameWithAdjusters('Inventory.EventHandlers.ActorInventory.ActorObservedHandler', None)
		
		
	def listItems(self):
		retVal = 'You don\'t have anything.'
		
		if len(self.attributes['items']) > 0:
			retVal = 'You have:'
			
			for item in self.attributes['items']:
				retVal = '{} {} {},'.format(retVal, item.attributes['adjective'], item.attributes['name'])
				
			retVal = retVal[0:-1]
		
		return retVal
		
		
	def listEquipment(self):
		equipArray	= []
		equipment	= filter(lambda item: item != None,
							[self.attributes['equipment']['Head'],
							 self.attributes['equipment']['Ears'],
							 self.attributes['equipment']['Eyes'],
							 self.attributes['equipment']['Face'],
							 self.attributes['equipment']['Neck'][0],
							 self.attributes['equipment']['Neck'][1],
							 self.attributes['equipment']['Body'],
							 self.attributes['equipment']['Arms'],
							 self.attributes['equipment']['Wrist'][0],
							 self.attributes['equipment']['Wrist'][1],
							 self.attributes['equipment']['Hands'],
							 self.attributes['equipment']['Finger'][0],
							 self.attributes['equipment']['Finger'][1],
							 self.attributes['equipment']['Waist'],
							 self.attributes['equipment']['Legs'],
							 self.attributes['equipment']['Feet'],
							 self.attributes['equipment']['Shield'],
							 self.attributes['equipment']['Wielded']])
			
			
		for item in equipment:
			slot = item.attributes['itemClass']
			
			equipArray.append('{}\t: {} {}'.format(ANSI.yellow(slot), item.attributes['adjective'], item.attributes['name']))
			
		return equipArray