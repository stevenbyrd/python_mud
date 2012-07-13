functions = {
	'multiply'			: lambda event, args: evaluateFunction(event, args[0]) * evaluateFunction(event, args[1]),
	'static_value'		: lambda event, args: args[0],
	'attribute_at_path'	: lambda event, args: getAttributeAtPath(event.attributes, args[0])
}


def evaluateFunction(event, argument):
	func = functions[argument['name']]
	
	return func(event, argument['args'])
	
	
def getAttributeAtPath(object, path):
	if path == '' or path == None:
		print 'returning {}'.format(object)
		return object
	else:
		delimeterIndex	= path.find('.')
		key				= path[0:delimeterIndex]
		
		if delimeterIndex == -1:
			key		= path[:]
			path	= ''
		else:
			path = path[delimeterIndex + 1:]
		
		if type(object) == type(dict()):
			return getAttributeAtPath(object[key], path)
		else:
			return getAttributeAtPath(getattr(object, key), path)
			