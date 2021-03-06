from Event.EventReceiver import EventReceiver
from Event.EventEmitter import EventEmitter


class Item(EventReceiver, EventEmitter):
	def __init__(self, itemJson, inventory):		
		EventReceiver.__init__(self)
		
		attributes = {
			'itemType'		: '',
			'itemClass'		: '',
			'itemID'		: '',
			'name'			: '',
			'pluralName'	: '',
			'description'	: [],
			'inventory'		: inventory,
			'stats'			: {
									'weight':0
			}
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
		
		out_adjusters = []
		
		if itemJson != None:
			for key in itemJson.keys():
				if key == 'out_adjusters':
					out_adjusters = itemJson[key]
				else:
					self.attributes[key] = itemJson[key]
			
		self.attributes['adjective'] = (lambda char: 
											((char == 'a' or char == 'e' or char == 'i' or char == 'o' or char == 'u') and 'an') or 'a')(self.attributes['name'].lower()[0])
			
		self.addEventHandlerByNameWithAdjusters('Item.EventHandlers.Item.ActorAttemptedDropHandler', None)
		self.addEventHandlerByNameWithAdjusters('Item.EventHandlers.Item.ItemDroppedHandler', None)
		self.addEventHandlerByNameWithAdjusters('Item.EventHandlers.Item.ActorAttemptedItemGrabHandler', None)
		self.addEventHandlerByNameWithAdjusters('Item.EventHandlers.Item.ActorGrabbedItemHandler', None)
		self.addEventHandlerByNameWithAdjusters('Item.EventHandlers.Item.ActorAttemptedItemEquipHandler', None)
		self.addEventHandlerByNameWithAdjusters('Item.EventHandlers.Item.WasObservedHandler', None)
		
		EventEmitter.__init__(self, out_adjusters)
		
		inventory.addEventSubscriber(self)