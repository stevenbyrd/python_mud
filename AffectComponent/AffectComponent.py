	
class AffectComponent:
	def __init__(self, source, target, args):
		self.attributes				= args
		self.attributes['source']	= source
		self.attributes['target']	= target