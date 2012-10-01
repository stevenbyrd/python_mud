import importlib


def loadAdjusterFromJSON(adjusterJSON):
	adjusterName	= adjusterJSON['name']
	args			= (lambda dictionary : dictionary.has_key('args') and dictionary['args'] or None)(adjusterJSON)
	path			= adjusterName.split('.')
	modulePath		= path[0]

	for step in path[1:-1]:
		modulePath = '{}.{}'.format(modulePath, step)

	adjusterModule	= importlib.import_module(modulePath)
	adjusterClass	= getattr(adjusterModule, path[-1])
	adjuster		= adjusterClass(args)
	
	return adjuster


class EventHandler:
	def __init__(self, adjusters):
		self.attributes = {
			'signature'		: '',
			'data'			: {},
			'adjusters'	: []
		}

		if adjusters != None:
			for adjusterJSON in adjusters:
				adjuster = loadAdjusterFromJSON(adjusterJSON)
		
				self.attributes['adjusters'].append(adjuster)
		


	def receiveEvent(self, event):
		for adjuster in self.attributes['adjusters']:
			adjuster.adjustEvent(event)
			
			if event.attributes['signature'] == None:
				break
		
		if event.attributes['signature'] != None:
<<<<<<< HEAD
			self.handleEvent(event)
			
			
			
	def loadAdjusterFromJSON(self, adjusterJSON):
		adjusterName	= adjusterJSON['name']
		args			= (lambda dictionary : dictionary.has_key('args') and dictionary['args'] or None)(adjusterJSON)
		path			= adjusterName.split('.')
		modulePath		= path[0]

		for step in path[1:-1]:
			modulePath = '{}.{}'.format(modulePath, step)

		adjusterModule	= importlib.import_module(modulePath)
		adjusterClass	= getattr(adjusterModule, path[-1])
		adjuster		= adjusterClass(args)
		
		return adjuster
=======
			self.handleEvent(event)
>>>>>>> bf64e254f8059325d6762aa2de1dc819677452d0
