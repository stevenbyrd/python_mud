from Equipable import Equipable

class Wielded(Equipable):
	def __init__(self, itemJson, inventory):
		Equipable.__init__(self, itemJson, inventory)