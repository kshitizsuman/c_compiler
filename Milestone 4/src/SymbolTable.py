# ------------------------------------------------------------------------------------------------------#
#   Compiler:                                                                                           #
#   Source Language: ANSI C, Implementation Language: Python, Target Language: MIPS                     #
#                                                                                                       #
#   Authors: Rishabh Bhardwaj, Kshitiz Suman
#   Group Number:                                                                    #
#   File: SymbolTable.py                                                                                     #
# ------------------------------------------------------------------------------------------------------#
TableNumber = 0
def getDataSize(type):
		if(type=='void'):
			return 0
		elif(type=='char'):
			return 1
		elif(type=='int'):
			return 4
		elif(type=='long'):
			return 8
		elif(type=='float'):
			return 4
		elif(type=='double'):
			return 8
		else:
			return 0

def getIDSize(type,dim,dims):
	if(dim == 0):
		return getDataSize(type)
	elif(dim == 1):
		return getDataSize(type)*dims[0]
	else:
		return getDataSize(type)*dims[0]*dims[1]

class SymbolTable:
	def __init__(self,theParent):
		global TableNumber
		self.symbols=[]
		self.attributes=[]
		self.entries=[]
		self.parent = theParent
		self.childList = dict()
		self.parameterTable = []
		self.tableNumber = TableNumber
		#self.isStructTable = False
		#self.structName = ''
		#self.structChildList = []
		TableNumber += 1
		if(theParent == -1):
			self.depth=0
			self.offsets = []
			self.offset_count=0
			self.tableName = 'GLOBALTABLE'
			self.insert(['FN','put',['void'],'void'])
			self.insert(['FN','get',['void'],'void'])
			self.insert(['FN','typeof',['void'],'void'])
		else:
			self.depth = theParent.depth+1
			self.offsets = []
			self.offset_count=theParent.offset_count
			self.tableName = ''

	def insert(self,entry):
		if(self.lookupCurrentTable(entry[1]) == False):
			newEntry = {}
			newEntry['type'] = entry[0]
			newEntry['name'] = entry[1]
			newEntry['input'] = entry[2]
			newEntry['output'] = entry[3]
			newEntry['scope'] = self.tableName
			self.offsets += [self.offset_count]
			newEntry['offset'] = self.offset_count
			if(newEntry['type'] == 'ID'):
				newEntry['array'] = entry[4]
				newEntry['dimension'] = entry[5]
				self.offset_count += getIDSize(newEntry['output'],newEntry['array'],newEntry['dimension'])
			self.symbols += [newEntry['name']]
			self.entries += [newEntry]
			return True
		else:
			return False

	def lookup(self,name):
		table = self
		while( not( table == -1 )):
			if(name in table.symbols):
				return table.entries[table.symbols.index(name)]
			for pTable in table.parameterTable :
				if(name in pTable.symbols):
					return pTable.entries[pTable.symbols.index(name)]
			table = table.parent
		for table in self.parameterTable :
			if(name in table.symbols):
				return table.entries[table.symbols.index(name)]
		return False

	def lookupCurrentTable(self,name):
		table = self
		if(name in table.symbols):
			return table.entries[table.symbols.index(name)]
		for table in self.parameterTable :
			if(name in table.symbols):
				return table.entries[table.symbols.index(name)]
		return False

	def lookupCurrentParameter(self,name):
		for table in self.parameterTable :
			if(name in table.symbols):
				return table.entries[table.symbols.index(name)]
		return False

	def addName(self):
		for e in self.entries:
			e['scope'] = self.tableName

#	def lookup(self,mystring):
#		table = self
#		while( not( table == -1 )):
#			if(mystring in table.symbols):
#				myindex = table.symbols.index(mystring)
#				return {"attributes":table.attributes[myindex],'offset':table.offset[myindex],'TABLE':table.tableNumber}
#			table = table.parent
#		return False
	
#	def lookupCurrentTable(self,mystring):
#		table = self
#		if(mystring in table.symbols):
#			myindex = table.symbols.index(mystring)
#			return {"attributes":table.attributes[myindex],'offset':table.offset[myindex],'TABLE':table.tableNumber}
#		return False
	
#	def insert(self,mystring,attributes_new):
#		if(self.lookupCurrentTable(mystring)==False):
#			self.symbols += [mystring]
#			attributes_new['NAME'] = mystring
#			self.attributes += [attributes_new]
#			self.offset += [self.offset_count]
#			data_size = 0
#
#			if(self.attributes[-1]['TYPE']=='void') : data_size=0
#			elif(self.attributes[-1]['TYPE']=='char') : data_size=1
#			elif(self.attributes[-1]['TYPE']=='bool') : data_size=1
#			elif(self.attributes[-1]['TYPE']=='short') :data_size=2
#			elif(self.attributes[-1]['TYPE']=='int') : data_size=4
#			elif(self.attributes[-1]['TYPE']=='long') : data_size=8
#			elif(self.attributes[-1]['TYPE']=='float') : data_size=4
#			elif(self.attributes[-1]['TYPE']=='double') : data_size=8
#			elif(self.attributes[-1]['TYPE']=='signed') : data_size=4
#			elif(self.attributes[-1]['TYPE']=='unsigned') : data_size=4
#			
#
#			if(self.attributes[-1]['ARRAY'] == 0):
#				totalIndex = 1
#			elif(self.attributes[-1]['ARRAY'] == 1):
#				totalIndex = int(self.attributes[-1]['INDEX1'])
#			elif(self.attributes[-1]['ARRAY'] == 2):
#				totalIndex = int(self.attributes[-1]['INDEX1'])
#				totalIndex *= int(self.attributes[-1]['INDEX2'])
#				
#			self.offset_count = self.offset_count + data_size*totalIndex
#			return True
#		else : return False