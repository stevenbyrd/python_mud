from Engine import Engine
import os
import json

	
def executeAffect(affectName, source, target):
	AffectEngine.instance.executeAffect(affectName, source, target)
	
	
def affectExists(affectName):
	return AffectEngine.instance.attributes['affects'].has_key(affectName)
	
	
class AffectEngine(Engine):
	instance = None

	def __init__(self):
		Engine.__init__(self)
		attributes = {
			'affects'			: {},
			'affectComponents'	: {}
		}

		for key in attributes.keys():
			self.attributes[key] = attributes[key]
			
		AffectEngine.instance = self
		
		self.buildAffectList()
		self.buildAffectComponentList()
	
	
	def buildAffectComponentList(self):
		import AffectComponent.GainHealth
		import AffectComponent.AffectEmote
		
		componentList = self.attributes['affectComponents']
		
		componentList['gain_health']	= AffectComponent.GainHealth.GainHealth
		componentList['affect_emote']	= AffectComponent.AffectEmote.AffectEmote
		
			
	def buildAffectList(self):
		from Affect.Affect import Affect
		
		affects		= self.attributes['affects']
		currentDir	= os.getcwd()
		affectDir	= currentDir + '/Content/affects' 
		fileList	= os.listdir(affectDir)
		
		for fname in fileList:			
			if fname.endswith('.txt'):
				filePath	= '{}/{}'.format(affectDir, fname)
				affectFile	= open(filePath, 'r')
				jsonString	= affectFile.read()
				jsonObj		= json.loads(jsonString)
				affect		= Affect(jsonObj)
				
				affectFile.close()
				
				for affectName in affect.attributes['affectNames']:
					affects[affectName] = affect
		
		
	def executeAffect(self, affectName, source, target):
		affects = self.attributes['affects']
		
		if affects.has_key(affectName):
			affect		= affects[affectName]
			pipeline	= affect.attributes['pipeline']
			components	= self.attributes['affectComponents']
			
			for componentJSON in pipeline:
				componentName = componentJSON['component_name']
				
				if components.has_key(componentName):
					args		= componentJSON['args']
					component	= components[componentName](source, target, args)
					
					component.execute()
					
					