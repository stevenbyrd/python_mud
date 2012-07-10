from Event.Event import Event
from Event.EventHandler import EventHandler
from Engine import Engine
import os
import json

	
def getAffect(affectName):
	if AffectEngine.instance.attributes['affectList'].has_key(affectName):
		return AffectEngine.instance.attributes['affectList'][affectName]
	
	return None

	
class AffectEngine(Engine):
	instance = None

	def __init__(self):
		Engine.__init__(self)
		attributes = {
			'affectList' : {}
		}

		for key in attributes.keys():
			self.attributes[key] = attributes[key]
			
		AffectEngine.instance = self
			
			
	def buildAffectList(self):
		affectList = self.attributes['affectList']


		





