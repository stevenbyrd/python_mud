from lib import ANSI

class Connection:
	def __init__(self, socket, player):
		self.attributes = {
			'socket'		: socket,
			'player'		: player,
			'inputBuffer'	: [],
			'outputBuffer'	: []
		}
		
			
	def pollInput(self):
		buffer	= self.attributes['inputBuffer']
		retVal	= ''
		
		if len(buffer) > 0:
			retVal = buffer.pop(0)
		
		return retVal
		

	def send(self, message):
		self.attributes['outputBuffer'].append(message)


	def sendFinal(self, message):
		self.send(message)
		
		self.send('\n\r{}\n\r\t{} {}\n\r\t{} {}\n\r\t{}{}\n\r{}: '.format(ANSI.magenta('['),
																				ANSI.yellow('HP:'),
																				ANSI.white(self.attributes['player'].attributes['currentHP']),
																				ANSI.yellow('Mana:'),
																				ANSI.white(self.attributes['player'].attributes['currentMana']),
																				ANSI.yellow('Options:'),
																				self.attributes['player'].attributes['menus'][-1].getOptions(),
																				ANSI.magenta(']')))