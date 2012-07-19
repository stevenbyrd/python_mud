import random
import Engine.RoomEngine
import Engine.ActorEngine
from Event.Event import Event


class GameTickedHandler:
	def __init__(self):
		self.attributes = {'signature':'game_tick'}

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if random.random() < receiver.attributes['spawnRate']:
			newNPC											= Engine.ActorEngine.loadNPC(receiver.attributes['npcID'])
			newNPC.attributes['roomID']						= receiver.attributes['room'].attributes['roomID']
			spawnEvent										= Event()
			spawnEvent.attributes['signature']				= 'actor_added_to_room'
			spawnEvent.attributes['data']['room']			= receiver.attributes['room']
			spawnEvent.attributes['data']['actor']			= newNPC
			
			receiver.attributes['room'].addEventSubscriber(newNPC)
			
			Engine.RoomEngine.emitEvent(spawnEvent)
			
			receiver.attributes['npcs'].append(newNPC)
		
		wanderingNPCs = []
		
		for npc in receiver.attributes['npcs']:
			if random.random() < receiver.attributes['wanderRate']:
				wanderingNPCs.append(npc)
				
		for npc in wanderingNPCs:
			npc.wander()