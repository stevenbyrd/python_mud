from Event.EventHandler import EventHandler
from Event.Event import Event
import Engine.ActorEngine
from lib import ANSI

class MenuOptionChosenHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'menu_option_chosen'
	
	def handleEvent(self, event):
		receiver		= event.attributes['receiver']
		option			= event.attributes['data']['option']
		validOptions	= receiver.attributes['options']
		player			= receiver.attributes['player']
		
		if validOptions.has_key(option):
			tuple		= validOptions[option]
			function	= tuple[1]
						
			function()
		else:
			feedbackEvent									= Event()
			feedbackEvent.attributes['signature']			= 'received_feedback'
			feedbackEvent.attributes['data']['feedback']	= ANSI.yellow('Invalid option!')
			feedbackEvent.attributes['data']['actor']		= player

			Engine.ActorEngine.emitEvent(feedbackEvent)