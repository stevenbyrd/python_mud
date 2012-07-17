from Equipable import Equipable

class Waist(Equipable):
	def __init__(self, itemJson, inventory):
		Equipable.__init__(self, itemJson, inventory)