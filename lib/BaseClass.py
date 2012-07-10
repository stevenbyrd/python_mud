class BaseClass:
    def __init__(self):
		try:
			if self.attributes == None:
				self.attributes = {}
		except:
			self.attributes = {}