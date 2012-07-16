from Event.Event import Event


functions = {
	'multiply'					: lambda event, args: evaluate(event, args[0]) * evaluate(event, args[1]),
	'attribute_at_path'			: lambda event, args: getAttributeAtPath(event.attributes, evaluate(event, args[0])),
	'value_equal_to'			: lambda event, args: evaluate(event, args[0]) == evaluate(event, args[1]),
	'value_not_equal_to'		: lambda event, args: evaluate(event, args[0]) != evaluate(event, args[1]),
	'modulus'					: lambda event, args: evaluate(event, args[0]) % evaluate(event, args[1]),
	'do_if'						: lambda event, args: doIfElse(event, args),
	'and'						: lambda event, args: And(event, args),
	'set_value_at_path'			: lambda event, args: setValueAtPath(event.attributes, evaluate(event, args[0]), evaluate(event, args[1])),
	'do_in_sequence'			: lambda event, args: evaluateInSequence(event, args),
	'remove_subscriber'			: lambda event, args: removeSubscriber(event, args),
	'add_subscriber'			: lambda event, args: addSubscriber(event, args),
	'get_room'					: lambda event, args: getRoom(event, args),
	'emit_event_from_engine'	: lambda event, args: emitEventFromEngine(event, args),
	'emit_event_from_receiver'	: lambda event, args: emitEventFromReceiver(event, args),
	'new_dict'					: lambda event, args: dict(),
	'create_event'				: lambda event, args: createEvent(event, args),
	'join_strings'				: lambda event, args: joinStrings(event, args),
	'send_final'				: lambda event, args: sendFinal(event, args),
	'text_by_replace'			: lambda event, args: textByReplace(event, args),
	'forward_event'				: lambda event, args: event.attributes['receiver'].emitEvent(event),
	'None'						: lambda event, args: None,
	'get_element_from_list'		: lambda event, args: getElementFromList(event, args),
	'filter_list_with_lambda'	: lambda event, args: filterListWithLambda(event, args)
}




def evaluate(event, expression):	
	if type(expression) == type([]):
		functionName	= expression[0]
		args			= expression[1:]
		
		retVal = functions[functionName](event, args)
		
		return retVal
	elif type(expression) == type(dict()):
		for key in expression.keys():
			expression[key] = evaluate(event, expression[key])
			
		return expression
	else:
		return expression




def evaluateInSequence(event, args):
	for argument in args:
		evaluate(event, argument)
		
		
	
	
def getAttributeAtPath(object, path):
	if path == '' or path == None:
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
			if object.has_key(key):
				return getAttributeAtPath(object[key], path)
			else:
				return None
		elif object != None:
			return getAttributeAtPath(getattr(object, key), path)
		else:
			return None
			
			
			
			
def setValueAtPath(current, value, path):	
	delimeterIndex = path.find('.')

	if delimeterIndex == -1:
		key = path[:]
	
		if type(current) == type(dict()):
			current[key] = value			
		else:
			setattr(current, key, value)
	else:
		key		= path[0:delimeterIndex]
		path	= path[delimeterIndex + 1:]

		if type(current) == type(dict()):
			setValueAtPath(current[key], value, path)
		else:
			setValueAtPath(getattr(current, key), value, path)
		



def removeSubscriber(event, args):
	emitter = evaluate(event, args[0])
	
	emitter.removeEventSubscriber(event.attributes['receiver'])
	
	
	
	
def addSubscriber(event, args):
	emitter = evaluate(event, args[0])
	
	emitter.addEventSubscriber(event.attributes['receiver'])
	
	
	
	
def getRoom(event, args):
	import Engine.RoomEngine
	
	roomID = evaluate(event, args[0])
	
	return Engine.RoomEngine.getRoom(roomID)
	
	
	
	
def emitEventFromEngine(event, args):
	import Engine.ActorEngine
	import Engine.CommandEngine
	import Engine.RoomEngine
	
	engines = {
		'actor_engine'		: Engine.ActorEngine,
		'command_engine'	: Engine.CommandEngine,
		'room_engine'		: Engine.RoomEngine
	}
	
	engine		= engines[args[0]]
	newEvent	= evaluate(event, args[1])
	
	engine.emitEvent(newEvent)
	
	
	
	
def emitEventFromReceiver(event, args):
	newEvent = evaluate(event, args[0])
	
	event.attributes['receiver'].emitEvent(newEvent)
	
	
	
	
def createEvent(event, args):
	newEvent			= Event()
	newEvent.attributes = evaluate(event, args[0])
	
	return newEvent
	
	


def doIfElse(event, args):
	if evaluate(event, args[0]):
		return evaluate(event, args[1])
	else:
		if len(args) > 2:
			return evaluate(event, args[2])
			
			
			
			
def And(event, args):
	for predicate in args:
		if evaluate(event, predicate) == False:
			return False
	
	return True
			
			
			
def joinStrings(event, args):
	str = ''
	
	for argument in args:
		str = '{}{}'.format(str, evaluate(event, argument))
		
	return str
	
	
	
	
def sendFinal(event, args):
	message = evaluate(event, args[0])
	event.attributes['receiver'].sendFinal(message)
		
		
		
		
def textByReplace(event, args):
	text = evaluate(event, args[2])
	
	pattern		= evaluate(event, args[0])
	replacement	= evaluate(event, args[1])
	
	if pattern != None and replacement != None:
		text = text.replace(pattern, replacement)
	
	return text
	
	
	
	
def getElementFromList(event, args):
	index	= evaluate(event, args[0])
	lst		= evaluate(event, args[1])
	
	if lst != None and index < len(lst) and len(lst) > 0:
		return lst[index]
	else:
		return None
		
		
		
def filterListWithLambda(event, args):
	lst		= evaluate(event, args[0])
	func	= eval(evaluate(event, args[1]), {'event':event})
	
	return filter(func, lst)
