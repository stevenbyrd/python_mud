from EventModule import *
from EngineModule import *
import EngineModule


class Command(EventReceiver):
    def __init__(self):
        EventReceiver.__init__(self)

        commandExecutionHandler = EventHandler()

        commandExecutionHandler.attributes['signature'] = 'execute_command'
        commandExecutionHandler.attributes['function']  = self.execute

        self.addEventHandler(commandExecutionHandler)
        




class Go(Command):
    def __init__(self):
        Command.__init__(self)
        

    def execute(self, event):
        cmd     = event.attributes['data']['command']
        args    = event.attributes['data']['args']
        actor   = event.attributes['data']['source']
        roomID  = actor.attributes['roomID']
        room    = EngineModule.roomEngine.getRoom(roomID)
        
        if cmd != 'go':
            args = [cmd]
        
        moveEvent                                   = Event()
        moveEvent.attributes['signature']           = 'actor_move'
        moveEvent.attributes['data']['direction']   = args[0]
        moveEvent.attributes['data']['source']      = actor
        
        room.receiveEvent(moveEvent)
        
        



class Look(Command):
    def __init__(self):
        Command.__init__(self)


    def execute(self, event):
        args        = event.attributes['data']['args']
        actor       = event.attributes['data']['source']
        roomID      = actor.attributes['roomID']
        room        = EngineModule.roomEngine.getRoom(roomID)
        lookEvent   = Event()
        
        if args == None or len(args) == 0:
            lookEvent                                   = Event()
            lookEvent.attributes['signature']           = 'was_looked_at'
            lookEvent.attributes['data']['observer']    = actor
        else:
            pass
        
        room.receiveEvent(lookEvent)
            