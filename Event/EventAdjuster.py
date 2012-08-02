class EventAdjuster:
	def __init__(self, args):
		self.attributes = {'signature': ''}

		if args != None:
			for key in args.keys():
				self.attributes[key] = args[key]