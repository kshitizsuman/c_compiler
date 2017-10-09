# ------------------------------------------------------------------------------------------------------#
#   Compiler:                                                                                           #
#   Source Language: ANSI C, Implementation Language: Python, Target Language: MIPS                     #
#                                                                                                       #
#   Authors: Rishabh Bhardwaj, Kshitiz Suman
#   Group Number:                                                                    #
#   File: SymbolTable.py                                                                                     #
# ------------------------------------------------------------------------------------------------------#
NodeNumber = 1
class AstNode:
	def __init__(self,NodeName,nodeChildList):
		global NodeNumber
		self.name=NodeName
		self.number = NodeNumber
		self.astChildList = nodeChildList
		NodeNumber += 1
