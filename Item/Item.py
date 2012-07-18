from Event.EventReceiver import EventReceiver
from Event.EventEmitter import EventEmitter


class Item(EventReceiver, EventEmitter):
	def __init__(self, itemJson, inventory):
		import EventHandlers.Item
		
		EventReceiver.__init__(self)
		EventEmitter.__init__(self)
		
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
		
		for key in itemJson.keys():
			self.attributes[key] = itemJson[key]
			
		self.attributes['adjective'] = (lambda char: 
											((char == 'a' or char == 'e' or char == 'i' or char == 'o' or char == 'u') and 'an') or 'a')(self.attributes['name'].lower()[0])
			
		self.addEventHandler(EventHandlers.Item.ActorAttemptedDropHandler())
		self.addEventHandler(EventHandlers.Item.ItemDroppedHandler())
		self.addEventHandler(EventHandlers.Item.ActorAttemptedItemGrabHandler())
		self.addEventHandler(EventHandlers.Item.ActorGrabbedItemHandler())
		self.addEventHandler(EventHandlers.Item.ActorAttemptedItemEquipHandler())
		self.addEventHandler(EventHandlers.Item.WasObservedHandler())
		
		inventory.addEventSubscriber(self)