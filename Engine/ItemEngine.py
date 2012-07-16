from Engine import Engine


def addEventSubscriber(subscriber):
	if ItemEngine.instance != None:
		ItemEngine.instance.addEventSubscriber(subscriber)
	else:
		ItemEngine.subscribers.append(subscriber)
	

def emitEvent(event):
	ItemEngine.instance.emitEvent(event)
	
	
def loadItem(type, itemName):
	return ItemEngine.instance.loadItem(type, itemName)


class ItemEngine(Engine):
	instance 	= None
	subscribers = []
	
	def __init__(self):
		Engine.__init__(self)
		
		attributes = {
			'itemList'				: [],
			'itemLoadFunctions'		: {
											'wieldable'	: self.loadWeapon
			}
		}

		for key in attributes.keys():
			self.attributes[key] = attributes[key]
			
		ItemEngine.instance = self
		
		for subscriber in ItemEngine.subscribers:
			self.addEventSubscriber(subscriber)
			
		ItemEngine.subscribers = []
			
			
	def loadItem(self, type, itemName):
		import os
		import json
		
		currentDir	= os.getcwd()
		itemInfo	= self.attributes['itemLoadFunctions'][type](itemName)
		filePath	= '{}/Content/items/{}'.format(currentDir, itemInfo[0]) 
		itemFile	= open(filePath, 'r')
		jsonString	= itemFile.read()
		
		print jsonString
		
		jsonObj		= json.loads(jsonString)
		itemClass	= itemInfo[1]
		item		= itemClass(jsonObj)
		
		itemFile.close()
		
		self.attributes['itemList'].append(item)
		
		return item
		
	
	
	def loadWeapon(self, itemName):
		from Item.Equipable.Wieldable import Wieldable
		
		print 'after import'
		
		return 'equipable/wieldable/{}.txt'.format(itemName), Wieldable
		