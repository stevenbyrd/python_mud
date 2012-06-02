class EventReceiver:
    def __init__(self):
        self.attributes = {
            'event_handlers' : []
        }
    
    
    def addEventHandler(self, handler):
        self.attributes['event_handlers'].append(handler)
    
    
    def receiveEvent(self, event):
        for handler in self.attributes['event_handlers']:
            if handler.attributes['signature'] == event.attributes['signature']:
                handler.attributes['function'](self, event)