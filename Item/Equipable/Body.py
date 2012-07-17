from Equipable import Equipable

class Body(Equipable):
	def __init__(self, itemJson, inventory):
		Equipable.__init__(self, itemJson, inventory)