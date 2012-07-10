from Event.Event import Event
from Event.EventHandler import EventHandler
from Event.EventReceiver import EventReceiver
from Event.EventEmitter import EventEmitter
import Engine.RoomEngine
import Engine.ActorEngine

class Actor(EventReceiver, EventEmitter):
	def __init__(self):
		EventReceiver.__init__(self)
		EventEmitter.__init__(self)
		
		attributes = {
			'actorID'		: '',
			'uniqueID'		: '',
			'name'			: '',
			'description'	: [],
			'race'			: '',
			'gender'		: '',
			'roomID'		: '',
			'stats'			: {
									'strength'		: 0,
									'constitution'	: 0,
									'agility'		: 0,
									'energy'		: 0,
									'focus'			: 0,
									'awareness'		: 0
			},
			'currentHP'		: 0,
			'maxHP'			: 0,
			'currentMana'	: 0,
			'maxMana'		: 0
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
			
		self.addEventHandler(ActorMovedFromRoomEventHandler())
		self.addEventHandler(ActorAddedToRoomEventHandler())
		self.addEventHandler(WasObservedEventHandler())
		
		Engine.ActorEngine.addEventSubscriber(self)
		Engine.RoomEngine.addEventSubscriber(self)
		
		
		
		
class ActorMovedFromRoomEventHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'actor_moved_from_room'
		self.attributes['function']		= self.actorMovedFromRoom


	def actorMovedFromRoom(self, receiver, event):
		actor = event.attributes['data']['actor']
		
		if actor == receiver:
			oldRoom	= Engine.RoomEngine.getRoom(receiver.attributes['roomID'])
			
			if oldRoom != None:
				oldRoom.removeEventSubscriber(receiver)
			
			
				
				
class ActorAddedToRoomEventHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'actor_added_to_room'
		self.attributes['function']		= self.actorAddedToRoom


	def actorAddedToRoom(self, receiver, event):
		actor = event.attributes['data']['actor']
		
		if actor == receiver:
			newRoom	= event.attributes['data']['room']

			if newRoom != None:
				newRoom.addEventSubscriber(receiver)
				
				actor.attributes['roomID'] = newRoom.attributes['roomID']
				
				
				

class WasObservedEventHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'was_observed'
		self.attributes['function']		= self.wasObserved


	def wasObserved(self, receiver, event):
		target = event.attributes['data']['target']
		
		if target == receiver:
			observer										= event.attributes['data']['observer']
			description										= receiver.attributes['description'][:]
			describeEvent									= Event()
			describeEvent.attributes['signature']			= 'entity_described_self'
			describeEvent.attributes['data']['description'] = description
			describeEvent.attributes['data']['observer']	= observer

			receiver.emitEvent(describeEvent)
			
			
