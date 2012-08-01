from Item.Item import Item

class Equipable(Item):
	def __init__(self, itemJson, inventory):
		import importlib
		
		Item.__init__(self, itemJson, inventory)
		
		self.attributes['size'] = 'all'
		
		Handlers = importlib.import_module('Item.EventHandlers.Equipable')

		self.addEventHandlerByNameWithAdjusters('Item.EventHandlers.Equipable.ActorAttemptedItemRemovalHandler', None)