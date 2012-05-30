from EnvironmentModule import *
from EventModule import *
from ActorModule import *
from EngineModule import *
import EngineModule

room	= Room()
event	= Event()

event.attributes['signature']	= 'player_entered'
event.attributes['data']		= {'player':Player()}

room.receiveEvent(event)

EngineModule.roomEngine = RoomEngine()
EngineModule.roomEngine.buildWorld()

EngineModule.actorEngine = ActorEngine()
EngineModule.actorEngine.loadPlayer('Khoma')