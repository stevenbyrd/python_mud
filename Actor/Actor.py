from Event.Event import Event
from Event.EventHandler import EventHandler
from Event.EventReceiver import EventReceiver
from Event.EventEmitter import EventEmitter
import Engine.RoomEngine
import Engine.ActorEngine


class Actor(EventReceiver, EventEmitter):
	def __init__(self, roomID):
		EventReceiver.__init__(self)
		EventEmitter.__init__(self)
		
		attributes = {
			'actorID'		: '',
			'uniqueID'		: '',
			'name'			: '',
			'description'	: [],
			'race'			: '',
			'gender'		: '',
			'roomID'		: roomID,
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
		self.addEventHandler(WasObservedEventHandler())
		self.addEventHandler(GainedHealthEventReceiver())
		
		Engine.ActorEngine.addEventSubscriber(self)
		
		startingRoom = Engine.RoomEngine.getRoom(roomID)
		
		startingRoom.addEventSubscriber(self)
		
		
		
		
class ActorMovedFromRoomEventHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'actor_moved_from_room'
		self.attributes['function']		= self.actorMovedFromRoom


	def actorMovedFromRoom(self, receiver, event):
		actor	= event.attributes['data']['actor']
		oldRoom	= event.attributes['data']['room']
		
		if actor == receiver:
			exit		= event.attributes['data']['exit']
			destination	= exit.attributes['destination']
			newRoom		= Engine.RoomEngine.getRoom(destination)
			
			oldRoom.removeEventSubscriber(receiver)
			newRoom.addEventSubscriber(receiver)
			
			receiver.attributes['roomID'] = destination

			
							
				
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
			describeEvent.attributes['data']['room']		= Engine.RoomEngine.getRoom(receiver.attributes['roomID'])

			Engine.ActorEngine.emitEvent(describeEvent, receiver)
			
			


class GainedHealthEventReceiver(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)
		self.attributes['signature']	= 'gained_health'
		self.attributes['function']		= self.gainedHealth


	def gainedHealth(self, receiver, event):
		target = event.attributes['data']['target']
		
		if target == receiver:
			amount = event.attributes['data']['amount']
			
			receiver.attributes['currentHP'] += amount