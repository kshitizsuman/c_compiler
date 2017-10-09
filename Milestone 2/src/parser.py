import sys
import os
import lexer
import ply.yacc as yacc
import SymbolTable
import ast
import createAST

from SymbolTable import *
from ast import *
from createAST import *

global type_of_declaration
type_of_declaration = 0		#0 default 1 for var declaraion -1 for func declaration
global nullStruct
nullStruct = 0
global varNode
varNode = []

global functionDefinition
functionDefinition = 0  #0 default 1 if it is a function defintion

global returnSpecifier
returnSpecifier = 'void'
global structDeclarationCount
structDeclarationCount = 0
global currentStructName
currentStructName = ''
global tempTable
tempTable = -1

global currentScopeNodes
currentScopeNodes = []

global currentSymbolTable
currentSymbolTable = SymbolTable(-1)
global FUNCTION_LIST_DECLARATION
FUNCTION_LIST_DECLARATION = [{'NAME':' ','INPUT':'',"OUTPUT":''}]
global FUNCTION_LIST_DEFINITION
FUNCTION_LIST_DEFINITION = [{'NAME':' ','INPUT':'',"OUTPUT":''}]
global functions
functions = []
global parameter_symbol_table
parameter_symbol_table = SymbolTable(-1)
tableNumber = 1;


tokens = lexer.tokens
flag_for_error = 0

def print_symbol_table(symbol_table,flag):
	filename =str(symbol_table.tableNumber)+".csv"
	f = open(filename, 'wb')
	
	f.write("          Table Number = %s\n" %str(symbol_table.tableNumber))

	num_var=len(symbol_table.attributes)
	if(flag == 1 ):
		f.write("Name,Type,Pointer,Array,Index1\n")
	else:
		f.write("Name,Type,Pointer,Array,Index1,Index2\n")
	for x in range(0,num_var):
		if(flag ==1 ):
			f.write("%s,%s,%s,%s,%s\n" %(symbol_table.attributes[x]['NAME'],symbol_table.attributes[x]['TYPE'],symbol_table.attributes[x]['POINTER'],symbol_table.attributes[x]['ARRAY'],symbol_table.attributes[x]['INDEX1']))
		else:
			f.write("%s,%s,%s,%s,%s,%s\n" %(symbol_table.attributes[x]['NAME'],symbol_table.attributes[x]['TYPE'],symbol_table.attributes[x]['POINTER'],symbol_table.attributes[x]['ARRAY'],symbol_table.attributes[x]['INDEX1'],symbol_table.attributes[x]['INDEX2']))
	f.close()


def type_cast_assign(s1,s2):
	data_types=["short","float","double","int","long","long long","char"]
	if((s1 in data_types) and (s2 in data_types)):
		return s1
	else:
		return "error"


def type_cast_addmul(s1,s2):
	if(s1>s2):
		tmp_var=s1
		s1=s2
		s2=tmp_var

	if(s1=="float" and s2 =="int"):
		return "float"
	elif(s1=="double" and s2 =="float"):
		return "double"
	elif(s1=="double" and s2 =="int"):
		return "double"
	elif(s1=="int" and s2 =="long"):
		return "long"
	elif(s1=="int" and s2 =="long long"):
		return "long long"
	elif(s1=="int" and s2=="short"):
		return "int"
	else:
		return "error"

def p_translation_unit(p):
	'''translation_unit : external_declaration
						| translation_unit external_declaration '''
	#print "translational_unit"
	#p[0]=("translational_unit",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[2]]

def p_primary_expression(p):
	'''primary_expression : constant
							| string '''
	#print "primary_expression"
	#p[0]=("primary_expression",)+tuple(p[-len(p)+1:])
	p[0] = p[1]

def p_primary_expression2(p):
	'''primary_expression : LPAREN expression RPAREN
							| generic_selection '''
	#print "primary_expression"
	#p[0]=("primary_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 4):
		p[0] = p[2]
	else:
		pass

def p_primary_expression3(p):
	'''primary_expression : IDENTIFIER  '''
	flag = 0
	check = currentSymbolTable.lookup(p[1])
	if(check == False):
		check = parameter_symbol_table.lookup(p[1])
		if(check == False):
			for func in FUNCTION_LIST_DEFINITION :
				if(p[1] in func['NAME']):
					flag = 1
					break
			if(flag == 0):
				print "ERROR at line number ", p.lineno(1) ,": parameter Variable not declared: ", p[1]
				sys.exit()
	if(flag == 0):
		p[0] = check['attributes']
	else:
		p[0] = func
	#print "primary_expression"
	#p[0]=("primary_expression",)+tuple(p[-len(p)+1:])

def p_constant(p):
	'''constant : I_CONSTANT '''
	#print "constant"
	#p[0]=("primary_expression",)+tuple(p[-len(p)+1:])
	p[0] = {'INDEX2': '', 'INDEX1': '', 'ARRAY': 0, 'TYPE':'int','POINTER':0}
	newAstNode = AstNode(p[1],[])
	p[0]['astChildList'] = [newAstNode]

def p_constant2(p):
	'''constant : F_CONSTANT '''
	#print "constant"
	#p[0]=("primary_expression",)+tuple(p[-len(p)+1:])
	p[0] = {'INDEX2': '', 'INDEX1': '', 'ARRAY': 0, 'TYPE':'float','POINTER':0}
	newAstNode = AstNode(p[1],[])
	p[0]['astChildList'] = [newAstNode]

def p_constant3(p):
	'''constant : CCONST '''
	#print "constant"
	#p[0]=("primary_expression",)+tuple(p[-len(p)+1:])
	p[0] = {'INDEX2': '', 'INDEX1': '', 'ARRAY': 0, 'TYPE':'char','POINTER':0}
	newAstNode = AstNode(p[1],[])
	p[0]['astChildList'] = [newAstNode]

def p_enumeration_constant(p):
	'''enumeration_constant : IDENTIFIER'''
	#print "enumeration_constant"
	#p[0]=("enumeration_constant",)+tuple(p[-len(p)+1:])

def p_string(p):
	'''string : STRINGLITERAL
				| FUNC_NAME '''
	#p[0]=("string",)+tuple(p[-len(p)+1:])
	p[0] = {'INDEX2': '', 'INDEX1': '', 'ARRAY': 1, 'TYPE':'char','POINTER':1}
	newAstNode = AstNode(p[1],[])
	p[0]['astChildList'] = [newAstNode]

def p_generic_selection(p):
	'''generic_selection : GENERIC LPAREN assignment_expression COMMA generic_assoc_list RPAREN '''
	#print "generic_selection"
	#p[0]=("generic_selection",)+tuple(p[-len(p)+1:])
	
def p_generic_assoc_list(p):
	'''generic_assoc_list : generic_association
							| generic_assoc_list COMMA generic_association '''
	#print "generic_assoc_list"
	#p[0]=("generic_assoc_list",)+tuple(p[-len(p)+1:])
	
def p_generic_association(p):
	'''generic_association : type_name COLON assignment_expression
							| DEFAULT COLON assignment_expression '''
	#print "generic_association"
	#p[0]=("generic_association",)+tuple(p[-len(p)+1:])
		
def p_postfix_expression(p):
	'''postfix_expression : primary_expression
							| postfix_expression LBRACKET expression RBRACKET'''
	#print "postfix_expresssion"
	#p[0]=("postfix_expresssion",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		p[0] = p[1]
		p[0]['POINTER'] = 0
		p[0]['ARRAY'] = 0
		#print p[3]
		if(p[3].has_key('TYPE')):
			if((str(p[3]['TYPE']) != "int" and str(p[3]['TYPE']) != "char")):
				print "Error at line number", p.lineno(1) ,": array index should be integer "
				sys.exit()
		else:
			if((str(p[3]['OUTPUT']) != "int" and str(p[3]['OUTPUT']) != "char")):
				print "Error at line number", p.lineno(1) ,": array index should be integer "
				sys.exit()
		
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   check it >>>>>>>>>>>>>>>>>>>>>>>>>>>>

def p_postfix_expression2(p):
	'''postfix_expression : postfix_expression LPAREN RPAREN
							| postfix_expression LPAREN argument_expression_list RPAREN'''
	#print "postfix_expresssion"
	#p[0]=("postfix_expresssion",)+tuple(p[-len(p)+1:])
	if(len(p) == 4):
		p[0] = p[1]
		newAstNode = AstNode(p[1]['NAME'],[])
		p[0]['astChildList'] = [newAstNode]
		if(str(p[1]['INPUT'][0]) != "void"):
			print "Error at line number", p.lineno(1) ,": insufficient function arguments for function ",p[1]['NAME']
			sys.exit()
	else:
		if(p[3].has_key('TYPE')):
			if(str(p[1]['INPUT']) == str(p[3]['TYPE'])):
				p[0] = p[1]
				newAstNode = AstNode(p[1]['NAME'],p[3]['astChildList'])
				p[0]['astChildList'] = [newAstNode]
			else:
				print "Error at line number", p.lineno(1) ,": invalid function arguments for function ",p[1]['NAME']
				sys.exit()
		else:
			if(str(p[1]['INPUT']) == str(p[3]['OUTPUT'])):
				p[0] = p[1]
				newAstNode = AstNode(p[1]['NAME'],p[3]['astChildList'])
				p[0]['astChildList'] = [newAstNode]
			else:
				print "Error at line number", p.lineno(1) ,": invalid function arguments for function ",p[1]['NAME']
				sys.exit()

def p_postfix_expression3(p):	
	'''postfix_expression : postfix_expression PERIOD IDENTIFIER
							| postfix_expression PTR_OP IDENTIFIER '''
	#print "postfix_expresssion"
	#p[0]=("postfix_expresssion",)+tuple(p[-len(p)+1:])
	global currentSymbolTable
	global tempTable
	x = ''

	if(tempTable == -1):
		tempTable = currentSymbolTable

	while(not(tempTable==-1)):
		for x in tempTable.structChildList:
			if(str(x.structName) == str(p[1]['NAME'])):
				check = x.lookupCurrentTable(p[3])
				if(check == False):
					print "Error at line number", p.lineno(1) ,": struct ",x.structName, " does not have varable named ", p[3]
					sys.exit()
				else:
					p[0] = check['attributes']
					tempTable = x
				break
		if(x != ''):
			if(str(x.structName) == str(p[1]['NAME'])):
				break
		tempTable = tempTable.father
	if(tempTable==-1):
		print "Error at line number", p.lineno(1) ,": struct not declared"
		sys.exit()
	#print p[3]
	#print currentSymbolTable.structChildList[0].symbols
	

def p_postfix_expression4(p):
	'''postfix_expression : postfix_expression INC_OP
							| postfix_expression DEC_OP
							| LPAREN type_name RPAREN left_brace initializer_list right_brace
							| LPAREN type_name RPAREN left_brace initializer_list COMMA right_brace '''
	#print "postfix_expresssion"
	#p[0]=("postfix_expresssion",)+tuple(p[-len(p)+1:])
	if(len(p) == 3):
		if(p[1]['ARRAY'] != 0):
			print "Error at line number", p.lineno(1) ,": lvalue required as increment operand"
		p[0] = p[1]
	#check here
		newAstNode = AstNode(p[2],p[1]['astChildList'])
		p[0]['astChildList'] = [newAstNode]
	else:
		pass

def p_argument_expression_list(p):
	'''argument_expression_list : assignment_expression
								| argument_expression_list COMMA assignment_expression '''
	#print "argument_expression_list"
	#p[0]=("argument_expression_list",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		if(p[1].has_key('TYPE')):
			p[0] = {'TYPE':[p[1]['TYPE']],'astChildList':p[1]['astChildList']}
		else:
			p[0] = {'OUTPUT':[p[1]['OUTPUT']],'astChildList':p[1]['astChildList']}
	else:
		if(p[3].has_key('TYPE')):
			p[0] = {'TYPE':p[1]['TYPE']+[p[3]['TYPE']],'astChildList':p[1]['astChildList'] + p[3]['astChildList']}
		else:
			p[0] = {'OUTPUT':p[1]['OUTPUT']+[p[3]['OUTPUT']],'astChildList':p[1]['astChildList'] + p[3]['astChildList']}


def p_unary_expression(p):
	'''unary_expression : postfix_expression
						| INC_OP unary_expression
						| DEC_OP unary_expression
						| unary_operator cast_expression
						| SIZEOF unary_expression
						| SIZEOF LPAREN type_name RPAREN
						| ALIGNOF LPAREN type_name RPAREN '''
	#print "unary_expression"
	#p[0]=("unary_expression",)+tuple(p[-len(p)+1:])
	global tempTable
	tempTable = -1

	if(len(p) == 2):
		p[0] = p[1]
	elif(len(p) == 3):
		p[0] = p[2]
		newAstNode = AstNode(p[1],p[2]['astChildList'])
		p[0]['astChildList'] = [newAstNode]
		if(p[1] == '&'):
			p[0]['POINTER'] += 1
	else:
		pass
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   check it >>>>>>>>>>>>>>>>>>>>>>>>>>>>

def p_unary_operator(p):
	'''unary_operator : AND_OP
						| TIMES
						| PLUS
						| MINUS
						| NOT_OP
						| LNOT '''     #changetoken
	#print "unary_operator"
	#p[0]=("unary_operator",)+tuple(p[-len(p)+1:])
	p[0] = p[1]
		
def p_cast_expression(p):
	'''cast_expression : unary_expression
						| LPAREN type_name RPAREN cast_expression '''
	#print "cast_expression"
	#p[0]=("cast_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		p[0] = {'TYPE':p[2]['TYPE']}


def p_multiplicative_expression(p):
	'''multiplicative_expression : cast_expression
								 | multiplicative_expression TIMES cast_expression
								 | multiplicative_expression DIVIDE cast_expression 
								 | multiplicative_expression MOD cast_expression '''
	#print "multiplicative_expression"
	#p[0]=("multiplicative_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		if(p[1]['TYPE'] == p[3]['TYPE'] and p[1]['POINTER'] == p[3]['POINTER']):
			p[0] = {'TYPE':p[1]['TYPE'],'POINTER':p[1]['POINTER']}
		else:
			result=type_cast_addmul(p[1]['TYPE'],p[3]['TYPE'])
			if(result == "error"):
				print "Error at line number", p.lineno(1) ,": mismatched type"
				sys.exit()
			else:
				p[0] = {'TYPE':result}
		newAstNode = AstNode(p[2],p[1]['astChildList']+p[3]['astChildList'])
		p[0]['astChildList'] = [newAstNode]

def p_additive_expression(p):
	'''additive_expression : multiplicative_expression
							| additive_expression PLUS multiplicative_expression
							| additive_expression MINUS multiplicative_expression '''
	#print "additive_expression"
	#p[0]=("additive_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		if(p[1]['TYPE'] == p[3]['TYPE'] and p[1]['POINTER'] == p[3]['POINTER']):
			p[0] = {'TYPE':p[1]['TYPE'],'POINTER':p[1]['POINTER']}
		else:
			result=type_cast_addmul(p[1]['TYPE'],p[3]['TYPE'])
			if(result == "error"):
				print "Error at line number", p.lineno(1) ,": mismatched type"
				sys.exit()
			else:
				p[0] = {'TYPE':result}	
		newAstNode = AstNode(p[2],p[1]['astChildList']+p[3]['astChildList'])
		p[0]['astChildList'] = [newAstNode]

def p_shift_expression(p):
	'''shift_expression : additive_expression
						| shift_expression LEFT_OP additive_expression
						| shift_expression RIGHT_OP additive_expression '''
	#print "shift_expression"
	#p[0]=("shift_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		if(((str(p[1]['TYPE']) in ["char","int","short","long"]) and (str(p[3]['TYPE']) in ["char","int","short","long"])) and (p[1]['POINTER'] == 0 and p[3]['POINTER']==0) ) :
			p[0] = {'TYPE': 'int','POINTER':0}
		else:
			print "Error at line number",p.lineno(1),": incorrect data types , shift operation between",str(p[1]['TYPE']),(p[1]['POINTER'])*"*","and",str(p[3]['TYPE']),(p[3]['POINTER'])*"*"
			sys.exit()
		newAstNode = AstNode(p[2],p[1]['astChildList']+p[3]['astChildList'])
		p[0]['astChildList'] = [newAstNode]

def p_relational_expression(p):
	'''relational_expression : shift_expression
								| relational_expression LT_OP shift_expression
								| relational_expression GT_OP shift_expression
								| relational_expression LE_OP shift_expression
								| relational_expression GE_OP shift_expression '''
	#print "relational_expression"
	#p[0]=("relational_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		if(p[1]['POINTER'] == p[3]['POINTER']):
			p[0] = {'TYPE':'int','POINTER':p[1]['POINTER']}
		else:
			print "Error at line number", p.lineno(1) ,": incorrect comparison "
			sys.exit()
		newAstNode = AstNode(p[2],p[1]['astChildList']+p[3]['astChildList'])
		p[0]['astChildList'] = [newAstNode]


def p_equality_expression(p):
	'''equality_expression : relational_expression
							| equality_expression EQ_OP relational_expression
							| equality_expression NE_OP relational_expression '''
	#print "equality_expression"
	#p[0]=("equality_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		if(p[1]['POINTER'] == p[3]['POINTER']):
			p[0] = {'TYPE':'int','POINTER':p[1]['POINTER']}
		else:
			print "Error at line number", p.lineno(1) ,": incorrect comparison"
			sys.exit()
		newAstNode = AstNode(p[2],p[1]['astChildList']+p[3]['astChildList'])
		p[0]['astChildList'] = [newAstNode]

def p_and_expression(p):
	'''and_expression : equality_expression
						| and_expression AND_OP equality_expression '''
	#print "and_expression"
	#p[0]=("and_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		if(((str(p[1]['TYPE']) in ["char","int","short","long"]) and (str(p[3]['TYPE']) in ["char","int","short","long"])) and (p[1]['POINTER'] == 0 and p[3]['POINTER']==0) ) :
			p[0] = {'TYPE': 'int','POINTER':0}
		else:
			print "Error at line number",p.lineno(1),": incorrect data types"
			sys.exit()
		newAstNode = AstNode(p[2],p[1]['astChildList']+p[3]['astChildList'])
		p[0]['astChildList'] = [newAstNode]
	
def p_exclusive_or_expression(p):
	'''exclusive_or_expression : and_expression
								| exclusive_or_expression XOR and_expression '''
	#print "exclusive_or_expression"
	#p[0]=("exclusive_or_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		if(((str(p[1]['TYPE']) in ["char","int","short","long"]) and (str(p[3]['TYPE']) in ["char","int","short","long"])) and (p[1]['POINTER'] == 0 and p[3]['POINTER']==0) ):
			p[0] = {'TYPE': 'int','POINTER':0}
		else:
			print "Error at line number",p.lineno(1),": incorrect data types"
			sys.exit()
		newAstNode = AstNode(p[2],p[1]['astChildList']+p[3]['astChildList'])
		p[0]['astChildList'] = [newAstNode]
	
def p_inclusive_or_expression(p):
	'''inclusive_or_expression : exclusive_or_expression
								| inclusive_or_expression OR_OP exclusive_or_expression '''
	#print "inclusive_or_expression"
	#p[0]=("inclusive_or_expression",)+tuple(p[-len(p)+1:])

	if(len(p) == 2):
		p[0] = p[1]
	else:
		if(((str(p[1]['TYPE']) in ["char","int","short","long"]) and (str(p[3]['TYPE']) in ["char","int","short","long"])) and (p[1]['POINTER'] == 0 and p[3]['POINTER']==0) ):
			p[0] = {'TYPE': 'int','POINTER':0}
		else:
			print "Error at line number",p.lineno(1),": incorrect data types"
			sys.exit()
		newAstNode = AstNode(p[2],p[1]['astChildList']+p[3]['astChildList'])
		p[0]['astChildList'] = [newAstNode]

def p_logical_and_expression(p):
	'''logical_and_expression : inclusive_or_expression
								| logical_and_expression LAND inclusive_or_expression '''
	#print "logical_and_expression"
	#p[0]=("logical_and_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		p[0] = {'TYPE':'int','POINTER':0}
		newAstNode = AstNode(p[2],p[1]['astChildList']+p[3]['astChildList'])
		p[0]['astChildList'] = [newAstNode]

def p_logical_or_expression(p):
	'''logical_or_expression : logical_and_expression
								| logical_or_expression LOR logical_and_expression '''
	#print "logical_or_expression"
	#p[0]=("logical_or_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		p[0] = {'TYPE':'int','POINTER':0}
		newAstNode = AstNode(p[2],p[1]['astChildList']+p[3]['astChildList'])
		p[0]['astChildList'] = [newAstNode]
	
def p_conditional_expression(p):
	'''conditional_expression : logical_or_expression
								| logical_or_expression CONDOP expression COLON conditional_expression '''
	#print "conditional_expression"
	#p[0]=("conditional_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		print "Rule not added conditional_expression"

def p_assignment_expression(p):
	'''assignment_expression : conditional_expression
								| unary_expression assignment_operator assignment_expression '''
	#print "assignment_expression"
	#p[0]=("assignment_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		#if(str(p[1]['TYPE']) == str(p[3]['TYPE'])):
		#	p[0] = {'TYPE': p[1]['TYPE']}
		result=type_cast_assign(str(p[1]['TYPE']),str(p[3]['TYPE']))
		if(result != "error"):
			p[0] = {'TYPE': result}
		else:
			print "Error at line number", p.lineno(2) ,": type mismatch in assignment"
			sys.exit()
		newAstNode = AstNode(p[2],[p[1]['astChildList'],p[3]['astChildList']])
		p[0]['astChildList'] = [newAstNode]


def p_assignment_operator(p):
	'''assignment_operator : EQUALS 
							| MUL_ASSIGN
							| DIV_ASSIGN
							| MOD_ASSIGN
							| ADD_ASSIGN
							| SUB_ASSIGN
							| LEFT_ASSIGN
							| RIGHT_ASSIGN
							| AND_ASSIGN
							| XOR_ASSIGN
							| OR_ASSIGN
							 '''                         #changetoken
	#print "assignment_operator"
	#p[0]=("assignment_operator",)+tuple(p[-len(p)+1:])
	p[0] = p[1]

def p_expression(p):
	'''expression : assignment_expression
					| expression COMMA assignment_expression '''
	#print "expression"
	#p[0]=("expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		#newAstNode = AstNode(p[2],p[1]['astChildList'] + p[3]['astChildList'])
		#p[0] = {'astChildList' :[newAstNode] }
		#print newAstNode.astChildList
		pass

def p_constant_expression(p):
	'''constant_expression : conditional_expression'''
	#print "constant_expression"
	#p[0]=("constant_expression",)+tuple(p[-len(p)+1:])
	p[0] = p[1]

def p_declaration(p):
	'''declaration : declaration_specifiers SEMI
					| declaration_specifiers init_declarator_list SEMI
					| static_assert_declaration '''
	#print "declaration"
	#print dict
	global type_of_declaration
	global FUNCTION_LIST_DECLARATION
	global FUNCTION_LIST_DEFINITION

	if(len(p) == 3):
		p[0] = {'astChildList':p[1]['astChildList']}

	if(len(p) == 4):
		if(type_of_declaration == 1) :
			for x in p[2]:
				if(x.has_key('TYPE')):
					result=type_cast_assign(x['TYPE'],p[1]['TYPE'])

					if(result=="error"):
						print "Error at line number", p.lineno(2) ,": invalid assignment"

			global varNode
			itr = -1
			for x in p[2]:
				itr = itr + 1
				#if (currentSymbolTable.insert(x['ID'],{'TYPE':p[1]['TYPE'],'STATIC':0,'ARRAY': x['ARRAY'],'INDEX1':x['INDEX1'],'INDEX2':x['INDEX2'],'SCOPETYPE':'GLOBAL','POINTER':x['POINTER'],'astChildList':x['astChildList']}) == False):
				if (currentSymbolTable.insert(x['ID'],{'TYPE':p[1]['TYPE'],'STATIC':0,'ARRAY': x['ARRAY'],'INDEX1':x['INDEX1'],'INDEX2':x['INDEX2'],'SCOPETYPE':'GLOBAL','POINTER':x['POINTER'],'astChildList':[varNode[itr]]}) == False):
					print x['ID'],': Variable already declared '
					sys.exit()
				else:
					x['SCOPETYPE'] = 'GLOBAL'
					check = currentSymbolTable.lookupCurrentTable(x['ID'])
					#print check
					x['TYPE'] = p[1]['TYPE']
					x['offset'] = check['offset']
					x['STATIC'] = 0
					#print "current"
					#print currentSymbolTable.symbols
			newAstNode = p[1]['astChildList'][0]
			for n in p[2]:
				newAstNode.astChildList += n['astChildList']
			p[0] = {'astChildList':[newAstNode]}
			#p[0]['astChildList'] = [newAstNode]
			varNode = []
		else:
			inp=[]
			ptr = []
			if(len(p[2][0]) <= 2 ):
				inp = ['void']
				ptr = [0]
			else:
				for i in p[2][0][1]:
					inp=inp+[i[0]['TYPE']]
					ptr=ptr+[i[1]['POINTER']]
			
			p[0] = {'NODE_TYPE':'function_declaration', 'OUTPUT':p[1]['TYPE'], 'INPUT': inp, 'IDENTIFIER': p[2][0][0],'partProgram':'','OUTPUT POINTER':p[2][0][-1],'INPUT POINTERS':ptr}
			#print p[2][1][0]
			flag = 0
			for func in FUNCTION_LIST_DECLARATION :
					if(p[2][0][0] in func['NAME'] or p[2][0][0] == 'main'):
						print "Error at line number", p.lineno(1) ,":function already declared"
						flag = 1
						break
			for func in FUNCTION_LIST_DEFINITION :
					if(p[2][0][0] in func['NAME'] or p[2][0][0] == 'main'):
						print "Error at line number", p.lineno(1) ,":function already declared"
						flag = 1
						break
			#print p[2][1][0]
			if(flag != 1):
				CURRENT_DECLARATION = [{"NAME":p[2][0][0],"INPUT":inp,"OUTPUT":p[1]['TYPE'],'OUTPUT POINTER':p[2][0][-1],'INPUT POINTERS':ptr}]
				FUNCTION_LIST_DECLARATION = FUNCTION_LIST_DECLARATION + CURRENT_DECLARATION
				print_symbol_table(parameter_symbol_table,1)
				parameter_symbol_table = SymbolTable(-1)

			newAstNode = p[1]['astChildList'][0]
			newFunAstNode = AstNode(p[2][0][0],[])
			newAstNode.astChildList += [newFunAstNode]
			if(len(p[2][0]) > 2 ):
				for n in p[2][0][1]:
					newAstNode2 = AstNode(n[0]['TYPE'],[])
					newAstNode3 = AstNode(n[1]['ID'],[])
					newAstNode2.astChildList += [newAstNode3]
					newAstNode.astChildList += [newAstNode2]
			p[0] = {'astChildList':[newAstNode]}

		type_of_declaration = 0

	#p[0]=("declaration",)+tuple(p[-len(p)+1:])
		
def p_declaration_specifiers(p):
	'''declaration_specifiers : storage_class_specifier declaration_specifiers
								| storage_class_specifier
								| type_specifier declaration_specifiers
								| type_specifier
								| type_qualifier declaration_specifiers
								| type_qualifier
								| function_specifier declaration_specifiers
								| function_specifier
								| alignment_specifier declaration_specifiers
								| alignment_specifier '''
	#print "declaration_specifiers"
	#p[0]=("declaration_specifiers",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	
def p_init_declarator_list(p):
	'''init_declarator_list : init_declarator
							| init_declarator_list COMMA init_declarator '''
	#print "init_declarator_list"
	#p[0]=("init_declarator_list",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[3]]

def p_init_declarator(p):
	'''init_declarator : declarator EQUALS initializer
						| declarator '''
	#print "init_declarator"
	#p[0]=("init_declarator",)+tuple(p[-len(p)+1:])
	global varNode
	if(len(p) == 4):
		if(p[3].has_key('TYPE')):
			if(str(p[3]['POINTER']) != str(p[1]['POINTER'])):
				print "Warning at line number", p.lineno(1), "initialization from incompatible pointer type " 
			p[0] = {'INDEX2': p[1]['INDEX2'], 'NODE_TYPE': 'var_decl_id', 'INDEX1': p[1]['INDEX1'], 'ARRAY': p[1]['ARRAY'], 'ID': p[1]['ID'], 'TYPE':p[3]['TYPE'],'POINTER':int(p[1]['POINTER'])}
			varNode += [p[1]['astChildList'][0]]
		else:
			if(str(p[3]['OUTPUT']) != str(p[1]['POINTER'])):
				print "Warning at line number", p.lineno(1), "initialization from incompatible pointer type " 
			p[0] = {'INDEX2': p[1]['INDEX2'], 'NODE_TYPE': 'var_decl_id', 'INDEX1': p[1]['INDEX1'], 'ARRAY': p[1]['ARRAY'], 'ID': p[1]['ID'], 'TYPE':p[3]['OUTPUT'],'POINTER':int(p[1]['POINTER'])}
			varNode += [p[1]['astChildList'][0]]
		newAstNode = AstNode(p[2],p[1]['astChildList']+p[3]['astChildList'])
		p[0]['astChildList'] = [newAstNode]
	else:
		p[0] = p[1]
		varNode += [p[1]['astChildList'][0]]
		
def p_storage_class_specifier(p):
	'''storage_class_specifier : TYPEDEF
								| EXTERN
								| STATIC
								| THREAD_LOCAL
								| AUTO
								| REGISTER '''
	#print "storage_class_specifier"
	#p[0]=("storage_class_specifier",)+tuple(p[-len(p)+1:])
	p[0] = p[1]

def p_type_specifier(p):
	'''type_specifier : VOID
						| CHAR 
						| SHORT
						| INT 
						| LONG
						| FLOAT
						| DOUBLE
						| SIGNED
						| UNSIGNED
						| BOOL
						| COMPLEX
						| IMAGINARY
						| TYPEID '''
	#print "type_specifier"
	newAstNode = AstNode(p[1],[])
	p[0] = {'NODE_TYPE': 'type_specifier', 'TYPE': p[1], 'astChildList':[newAstNode]}
	#p[0]=("type_specifier",)+tuple(p[-len(p)+1:])

def p_type_specifier2(p):
	'''type_specifier : struct_or_union_specifier
						| enum_specifier '''
	#print "type_specifier"
	#p[0]=("type_specifier",)+tuple(p[-len(p)+1:])
	p[0] = p[1]
	
def p_struct_or_union_specifier(p):
	'''struct_or_union_specifier : struct_or_union left_brace struct_declaration_list right_brace
								| struct_or_union struct_name left_brace struct_declaration_list right_brace
								| struct_or_union struct_name '''
	#print "struct_or_union_specifier"
	#p[0]=("struct_or_union_specifier",)+tuple(p[-len(p)+1:])
	if(len(p) == 5):
		global nullStruct
		newAstNode = AstNode("struct",[AstNode("STRUCT-NAME",[AstNode("UNNAMED STRUCT"+str(nullStruct),[])])])
		newAstNode2 = AstNode("STRUCT-BODY",[])
		if(type(p[3]) is list):
			for n in p[3]:
				newAstNode2.astChildList += n['astChildList']
		else:
			newAstNode2.astChildList += p[3]['astChildList']
		newAstNode.astChildList += [newAstNode2]
		p[0] = {'NODE_TYPE': 'struct_decl','TYPE':p[1],'ARRAY':0, 'ID' : "UNNAMED STRUCT"+str(nullStruct), 'INDEX1': '','INDEX2':'','POINTER':0,'astChildList':[newAstNode]}
		if (currentSymbolTable.insert("UNNAMED STRUCT"+str(nullStruct),{'TYPE':p[1],'STATIC':0,'ARRAY': 0,'INDEX1':'','INDEX2':'','POINTER':0,'astChildList':[]}) == False):
			print 'UNNAMED STRUCT',str(nullStruct),': Variable already declared '
			sys.exit()
		else:
			check = currentSymbolTable.lookupCurrentTable("UNNAMED STRUCT"+str(nullStruct))
			#print check
			p[0]['offset'] = check['offset']
			p[0]['STATIC'] = 0
			#print "current"
			#print currentSymbolTable.symbols
		nullStruct = nullStruct + 1
	elif(len(p) == 6):
		newAstNode = AstNode("struct",[AstNode("STRUCT-NAME",p[2]['astChildList'])])
		newAstNode2 = AstNode("STRUCT-BODY",[])
		if(type(p[4]) is list):
			for n in p[4]:
				newAstNode2.astChildList += n['astChildList']
		else:
			newAstNode2.astChildList += p[4]['astChildList']
		newAstNode.astChildList += [newAstNode2]
		p[0] = {'NODE_TYPE': 'struct_decl','TYPE':p[1],'ARRAY':0, 'ID' : p[2]['ID'], 'INDEX1': '','INDEX2':'','POINTER':0,'astChildList':[newAstNode]}
		if (currentSymbolTable.insert(p[2]['ID'],{'TYPE':p[1],'STATIC':0,'ARRAY': 0,'INDEX1':'','INDEX2':'','POINTER':0,'astChildList':p[2]['astChildList']}) == False):
			print p[2]['ID'],': Variable already declared '
			sys.exit()
		else:
			check = currentSymbolTable.lookupCurrentTable(p[2]['ID'])
			#print check
			p[0]['offset'] = check['offset']
			p[0]['STATIC'] = 0
			#print "current"
			#print currentSymbolTable.symbols
	else:
		check = currentSymbolTable.lookup(p[2]['ID'])
		if(check == False):
			print "Error at line number", p.lineno(1),': Struct ',p[2]['ID'],'not declared '
			sys.exit()
		p[0] = {'NODE_TYPE': 'struct_decl','TYPE':p[1],'ARRAY':0, 'ID' : p[2]['ID'], 'INDEX1': '','INDEX2':'','POINTER':0,'astChildList':check['attributes']['astChildList']}

def p_struct_name(p):
	'''struct_name : IDENTIFIER '''
	global currentStructName
	currentStructName = p[1]
	newAstNode = AstNode(p[1],[])
	p[0] = {'ID':p[1],'astChildList':[newAstNode]}

def p_struct_or_union(p):
	'''struct_or_union : STRUCT
						| UNION '''
	#print "struct_or_union"
	#p[0]=("struct_or_union",)+tuple(p[-len(p)+1:])
	p[0] = p[1]
	global structDeclarationCount
	structDeclarationCount = structDeclarationCount + 1


def p_struct_declaration_list(p):
	'''struct_declaration_list : struct_declaration
								| struct_declaration_list struct_declaration '''
	#print "struct_declaration_list"
	#p[0]=("struct_declaration_list",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[2]]

def p_struct_declaration(p):
	'''struct_declaration : specifier_qualifier_list SEMI 
							| specifier_qualifier_list struct_declarator_list SEMI
							| static_assert_declaration '''
	#print "struct_declaration"
	#p[0]=("struct_declaration",)+tuple(p[-len(p)+1:])
	if(len(p) == 4):
		for x in p[2]:
			p[1]['astChildList'][0].astChildList += x['astChildList']
			if (currentSymbolTable.insert(x['ID'],{'TYPE':p[1]['TYPE'],'STATIC':0,'ARRAY': x['ARRAY'],'INDEX1':x['INDEX1'],'INDEX2':x['INDEX2'],'SCOPETYPE':'GLOBAL','POINTER':x['POINTER'],'astChildList':x['astChildList']}) == False):
				print x['ID'],': Variable already declared '
				sys.exit()
			else:
				x['SCOPETYPE'] = 'GLOBAL'
				check = currentSymbolTable.lookupCurrentTable(x['ID'])
				#print check
				x['TYPE'] = p[1]['TYPE']
				x['offset'] = check['offset']
				x['STATIC'] = 0
				#print "current"
				#print currentSymbolTable.symbols
	#print "warning:: you forgot to update p[0] here"
	p[0] = p[1]

def p_specifier_qualifier_list(p):
	'''specifier_qualifier_list : type_specifier specifier_qualifier_list
								| type_specifier
								| type_qualifier specifier_qualifier_list
								| type_qualifier '''
	#print "specifier_qualifier_list"
	#p[0]=("specifier_qualifier_list",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	
def p_struct_declarator_list(p):
	'''struct_declarator_list : struct_declarator
								| struct_declarator_list COMMA struct_declarator '''
	#print "struct_declarator_list"
	#p[0]=("struct_declarator_list",)+tuple(p[-len(p)+1:])                       #changetoken
	if(len(p) == 2):
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[3]]

def p_struct_declarator(p):
	'''struct_declarator : COLON constant_expression
							| declarator COLON constant_expression
							| declarator '''
	#print "struct_declarator"
	#p[0]=("struct_declarator",)+tuple(p[-len(p)+1:])                        #changetoken
	if(len(p) == 2):
		p[0] = p[1]

def p_enum_specifier(p):
	'''enum_specifier : ENUM left_brace enumerator_list right_brace
						| ENUM left_brace enumerator_list COMMA right_brace
						| ENUM IDENTIFIER left_brace enumerator_list right_brace
						| ENUM IDENTIFIER left_brace enumerator_list COMMA right_brace
						| ENUM IDENTIFIER '''
	#print "enum_specifier"
	#p[0]=("enum_specifier",)+tuple(p[-len(p)+1:])                        #changetoken
	
def p_enumerator_list(p):
	'''enumerator_list : enumerator
						| enumerator_list COMMA enumerator '''
	#print "enumerator_list"
	#p[0]=("enumerator_list",)+tuple(p[-len(p)+1:])                        #changetoken
	
def p_enumerator(p):
	'''enumerator : enumeration_constant EQUALS constant_expression
					| enumeration_constant '''
	#print "enumerator"
	#p[0]=("enumerator",)+tuple(p[-len(p)+1:])                      
	
def p_type_qualifier(p):
	'''type_qualifier : CONST
						| RESTRICT
						| VOLATILE
						'''
	#print "type_qualifier"
	#p[0]=("type_qualifier",)+tuple(p[-len(p)+1:])
	
def p_function_specifier(p):
	'''function_specifier : INLINE
							| NORETURN '''
	#print "function_specifier"
	#p[0]=("function_specifier",)+tuple(p[-len(p)+1:])
	
def p_alignment_specifier(p):
	'''alignment_specifier : ALIGNAS LPAREN type_name RPAREN 
							| ALIGNAS LPAREN constant_expression RPAREN '''
	#print "alignment_specifier"
	#p[0]=("alignment_specifier",)+tuple(p[-len(p)+1:])
	
def p_declarator(p):
	'''declarator : pointer direct_declarator
					| direct_declarator '''
	#print "declarator"
	#p[0]=("declarator",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
		if(type_of_declaration == -1):
			p[0] += [0]
	else:
		if(type_of_declaration == 1):
			newAstNode = AstNode("<POINTER,"+str(p[1])+">",p[2]['astChildList'])
			p[0] = {'astChildList':[newAstNode],'POINTER':int(p[1]),'INDEX2': p[2]['INDEX2'], 'NODE_TYPE': p[2]['NODE_TYPE'], 'INDEX1': p[2]['INDEX1'], 'ARRAY': p[2]['ARRAY'], 'ID': p[2]['ID']}
		else:
			p[0] = p[2]	+ [int(p[1])]

def p_direct_declarator(p):
	'''direct_declarator : IDENTIFIER
							| IDENTIFIER LBRACKET arrayindex RBRACKET
							| IDENTIFIER LBRACKET arrayindex RBRACKET LBRACKET arrayindex RBRACKET '''
	#print "direct_declarator"
	global type_of_declaration
	type_of_declaration = 1
	newAstNode = AstNode(p[1],[])
	if(len(p) == 2 ):
		p[0] = {'NODE_TYPE' : 'var_decl_id', 'ARRAY':0, 'ID' : p[1], 'INDEX1': 0,'INDEX2':0,'POINTER':0}
	elif(len(p) == 5):
		p[0] = {'NODE_TYPE': 'var_decl_id','ARRAY':1, 'ID' : p[1], 'INDEX1': p[3],'INDEX2':'','POINTER':1}
		newAstNode2 = newAstNode
		newAstNode = AstNode("<ARRAY,1>",[newAstNode2])
	else:
		p[0] = {'NODE_TYPE': 'var_decl_id','ARRAY':2, 'ID' : p[1], 'INDEX1': p[3],'INDEX2':p[6],'POINTER':2}
		newAstNode2 = newAstNode
		newAstNode = AstNode("<ARRAY,2>",[newAstNode2])
		#print t[1]
	#p[0]=("direct_declarator",)+tuple(p[-len(p)+1:])
	p[0]['astChildList'] = [newAstNode]

def p_arrayindex(p):
	'''arrayindex : IDENTIFIER
				| I_CONSTANT '''
	p[0] = p[1]

def p_direct_declarator2(p):
	'''direct_declarator : IDENTIFIER LBRACKET RBRACKET
							| IDENTIFIER LBRACKET RBRACKET LBRACKET RBRACKET
							| IDENTIFIER LBRACKET RBRACKET LBRACKET arrayindex RBRACKET '''
	#print "direct_declarator"
	global type_of_declaration
	type_of_declaration = 1
	newAstNode = AstNode(p[1],[])
	if(len(p) == 4 ):
		p[0] = {'NODE_TYPE' : 'var_decl_id', 'ARRAY':1, 'ID' : p[1], 'INDEX1': '0','INDEX2':'','POINTER':0}
		newAstNode2 = newAstNode
		newAstNode = AstNode("<ARRAY,1>",[newAstNode2])
	elif(len(p) == 6):
		p[0] = {'NODE_TYPE': 'var_decl_id','ARRAY':2, 'ID' : p[1], 'INDEX1': '0','INDEX2':'0','POINTER':1}
		newAstNode2 = newAstNode
		newAstNode = AstNode("<ARRAY,2>",[newAstNode2])
	else:
		p[0] = {'NODE_TYPE': 'var_decl_id','ARRAY':2, 'ID' : p[1], 'INDEX1': '0','INDEX2':p[5],'POINTER':2}
		newAstNode2 = newAstNode
		newAstNode = AstNode("<ARRAY,2>",[newAstNode2])
	p[0]['astChildList'] = [newAstNode]

def p_direct_declarator3(p):
	'''direct_declarator : IDENTIFIER LPAREN parameter_type_list RPAREN
							| IDENTIFIER LPAREN RPAREN '''
	#print "direct_declarator"
		#print t[1]
	#p[0]=("direct_declarator",)+tuple(p[-len(p)+1:])
	global type_of_declaration
	type_of_declaration = -1

	if(len(p)==5):
		p[0] = [p[1]]+[p[3]]
	
	if(len(p)==4):
		p[0] = [p[1]]

def p_pointer(p):
	'''pointer : TIMES pointer
				| TIMES '''
	#print "pointer"
	#p[0]=("pointer",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = 1
	else:
		p[0] = p[2] + 1

def p_pointer2(p):
	'''pointer : TIMES type_qualifier_list pointer
				| TIMES type_qualifier_list '''
	#print "pointer"
	#p[0]=("pointer",)+tuple(p[-len(p)+1:])


def p_type_qualifier_list(p):
	'''type_qualifier_list : type_qualifier
							| type_qualifier_list type_qualifier '''
	#print "type_qualifier_list"
	#p[0]=("type_qualifier_list",)+tuple(p[-len(p)+1:])
	
def p_parameter_type_list(p):
	'''parameter_type_list : parameter_list '''
	#print "parameter_type_list"
	#p[0]=("parameter_type_list",)+tuple(p[-len(p)+1:])
	p[0]=p[1]

def p_parameter_list(p):
	'''parameter_list : parameter_declaration
						| parameter_list COMMA parameter_declaration '''
	#print "parameter_list"
	#p[0]=("parameter_list",)+tuple(p[-len(p)+1:])
	#print p[1]
	if(len(p)==2):
		p[0]=[p[1]]
		if(len(p[1]) > 1):
			parameter_symbol_table.insert(p[1][1]['ID'],{'TYPE':p[1][0]['TYPE'],'ARRAY':p[1][1]['ARRAY'],'SCOPETYPE':'PARAMETER','INDEX1':p[1][1]['INDEX1'],'STATIC':0,'POINTER':int(p[1][1]['POINTER']),'astChildList':p[1][1]['astChildList']})

	if(len(p)==4):
		p[0]=p[1]+[p[3]]
		if(len(p[3]) > 1):
			parameter_symbol_table.insert(p[3][1]['ID'],{'TYPE':p[3][0]['TYPE'],'ARRAY':p[3][1]['ARRAY'],'SCOPETYPE':'PARAMETER','INDEX1':p[3][1]['INDEX1'],'STATIC':0,'POINTER':int(p[3][1]['POINTER']),'astChildList':p[3][1]['astChildList']})
	#print "para---"
	#print parameter_symbol_table.symbols


def p_parameter_declaration(p):
	'''parameter_declaration : declaration_specifiers declarator
								| declaration_specifiers abstract_declarator
								| declaration_specifiers '''
	#print "parameter_declaration"
	#p[0]=("parameter_declaration",)+tuple(p[-len(p)+1:])
	if(len(p)==3):
		p[0]=[p[1]]+[p[2]]
	
	if(len(p)==2):
		p[0]=[p[1]]	

#def p_identifier_list(p):
#	'''identifier_list : IDENTIFIER
#						| identifier_list COMMA IDENTIFIER '''
	#print "identifier_list"
	#p[0]=("identifier_list",)+tuple(p[-len(p)+1:])
	
def p_type_name(p):
	'''type_name : specifier_qualifier_list abstract_declarator
					| specifier_qualifier_list '''
	#print "type_name"
	#p[0]=("type_name",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	
def p_abstract_declarator(p):
	'''abstract_declarator : pointer direct_abstract_declarator
							| pointer
							| direct_abstract_declarator '''
	#print "abstarct_declarator"
	#p[0]=("abstarct_declarator",)+tuple(p[-len(p)+1:])
	
def p_direct_abstract_declarator(p):
	'''direct_abstract_declarator : LPAREN abstract_declarator RPAREN 
									| LBRACKET RBRACKET
									| LBRACKET TIMES RBRACKET 
									| LBRACKET STATIC type_qualifier_list assignment_expression RBRACKET 
									| LBRACKET STATIC assignment_expression RBRACKET 
									| LBRACKET type_qualifier_list STATIC assignment_expression RBRACKET 
									| LBRACKET type_qualifier_list assignment_expression RBRACKET 
									| LBRACKET type_qualifier_list RBRACKET 
									| LBRACKET assignment_expression RBRACKET 
									| direct_abstract_declarator LBRACKET RBRACKET
									| direct_abstract_declarator LBRACKET TIMES RBRACKET
									| direct_abstract_declarator LBRACKET STATIC type_qualifier_list assignment_expression RBRACKET
									| direct_abstract_declarator LBRACKET STATIC assignment_expression RBRACKET
									| direct_abstract_declarator LBRACKET type_qualifier_list assignment_expression RBRACKET
									| direct_abstract_declarator LBRACKET type_qualifier_list STATIC assignment_expression RBRACKET 
									| direct_abstract_declarator LBRACKET type_qualifier_list RBRACKET
									| direct_abstract_declarator LBRACKET assignment_expression RBRACKET
									| LPAREN RPAREN 
									| LPAREN parameter_type_list RPAREN 
									| direct_abstract_declarator LPAREN RPAREN
									| direct_abstract_declarator LPAREN parameter_type_list RPAREN
									 '''
	#print "direct_abstract_declarator"
	#p[0]=("direct_abstract_declarator",)+tuple(p[-len(p)+1:])
	
def p_initializer(p):
	'''initializer : left_brace initializer_list right_brace
					| left_brace initializer_list COMMA right_brace 
					| assignment_expression '''
	#print "initializer"
	#p[0]=("initializer",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]


def p_initializer_list(p):
	'''initializer_list : designation initializer
						| initializer
						| initializer_list COMMA designation initializer
						| initializer_list COMMA initializer
						'''
	#print "initializer_list"
	#p[0]=("initializer_list",)+tuple(p[-len(p)+1:])
	
def p_designation(p):
	'''designation : designator_list EQUALS '''
	#print "designation"
	#p[0]=("designation",)+tuple(p[-len(p)+1:])
	
def p_designator_list(p):
	'''designator_list : designator
						| designator_list designator '''
	#print "designator_list"
	#p[0]=("designator_list",)+tuple(p[-len(p)+1:])
	
def p_designator(p):
	'''designator : LBRACKET constant_expression RBRACKET 
					| PERIOD IDENTIFIER '''
	#print "designator"
	#p[0]=("designator",)+tuple(p[-len(p)+1:])
	
def p_static_assert_declaration(p):
	'''static_assert_declaration : STATIC_ASSERT LPAREN constant_expression COMMA STRINGLITERAL RPAREN SEMI '''
	#print "static_assert_declaration"
	#p[0]=("static_assert_declaration",)+tuple(p[-len(p)+1:])
	
def p_statement(p):
	'''statement : compound_statement
					| expression_statement '''
	#print "statement"
	#p[0]=("statement",)+tuple(p[-len(p)+1:])
	p[0] = p[1]

def p_statement2(p):
	'''statement : selection_statement '''
	#print "statement"
	#p[0]=("statement",)+tuple(p[-len(p)+1:])
	p[0] = p[1]
	#print p[0]['astChildList'][0].astChildList[1].astChildList

def p_statement3(p):
	'''statement : iteration_statement '''
	#print "statement"
	#p[0]=("statement",)+tuple(p[-len(p)+1:])
	p[0] = p[1]

def p_statement4(p):
	'''statement : labeled_statement
					| jump_statement '''
	#print "statement"
	#p[0]=("statement",)+tuple(p[-len(p)+1:])
	p[0] = p[1]
	pass


def p_labeled_statement(p):
	'''labeled_statement : IDENTIFIER COLON statement
						| CASE constant_expression COLON statement
						| DEFAULT COLON statement
						 '''
	#print "labeled_statement"
	#p[0]=("labeled_statement",)+tuple(p[-len(p)+1:])
	
def p_compound_statement(p):
	'''compound_statement : left_brace right_brace 
							| left_brace block_item_list right_brace '''
	#print "compound_statement"
	#p[0]=("compound_statement",)+tuple(p[-len(p)+1:])
	if(len(p) == 3):
		newAstNode = AstNode("NULL",[])
		p[0] = {'astChildList':[newAstNode]}
	else:
		p[0] = p[2]

def p_block_item_list(p):
	'''block_item_list : block_item
						| block_item_list block_item '''
	#print "block_item_list"
	#p[0]=("block_item_list",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[2]]

def p_block_item(p):
	'''block_item : declaration
					| statement '''
	#print "block_item"
	#p[0]=("block_item",)+tuple(p[-len(p)+1:])
	p[0] = p[1]

def p_expression_statement(p):
	'''expression_statement : SEMI 
							| expression SEMI  '''
	#print "expression_statement"
	#p[0]=("expression_statement",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		newAstNode = AstNode("NULL",[])
		p[0] = {'astChildList':[newAstNode]}
	else:
		p[0] = p[1]

def p_selection_statement(p):
	'''selection_statement : IF LPAREN expression RPAREN statement ELSE statement
							| IF LPAREN expression RPAREN statement '''
	#print "selection_statement"
	#p[0]=("selection_statement",)+tuple(p[-len(p)+1:])
	if(len(p) == 6):
		newAstNode3 = AstNode("IF-CONDITION",p[3]['astChildList'])
		newAstNode2 = AstNode(p[1],[newAstNode3])
		newAstNode3 = AstNode("IF-BODY",[])
		if(type(p[5]) is list):
			for n in p[5]:
				newAstNode3.astChildList += n['astChildList']
		else:
			newAstNode3.astChildList += p[5]['astChildList']
		newAstNode2.astChildList += [newAstNode3]
		p[0] = {'astChildList':[newAstNode2]}
		pass
	else:
		newAstNode = AstNode(p[6],[])
		if(type(p[7]) is list):
			for n in p[7]:
				newAstNode.astChildList += n['astChildList']
		else:
			newAstNode.astChildList += p[7]['astChildList']
		newAstNode3 = AstNode("IF-CONDITION",p[3]['astChildList'])
		newAstNode2 = AstNode(p[1],[newAstNode3])
		newAstNode3 = AstNode("IF-BODY",[])
		if(type(p[5]) is list):
			for n in p[5]:
				newAstNode3.astChildList += n['astChildList']
		else:
			newAstNode3.astChildList += p[5]['astChildList']
		newAstNode2.astChildList += [newAstNode3]
		newAstNode2.astChildList += [newAstNode]
		p[0] = {'astChildList':[newAstNode2]}
		pass

def p_selection_statement2(p):
	'''selection_statement : SWITCH LPAREN expression RPAREN statement '''
	#print "selection_statement"
	#p[0]=("selection_statement",)+tuple(p[-len(p)+1:])
	pass

def p_iteration_statement(p):
	'''iteration_statement : WHILE LPAREN expression RPAREN statement
							'''
	#print "iteration_statement"
	#p[0]=("iteration_statement",)+tuple(p[-len(p)+1:])
	newAstNode = AstNode(p[1],[])
	newAstNode2 = AstNode("WHILE-CONDITION",p[3]['astChildList'])
	newAstNode.astChildList += [newAstNode2]
	newAstNode2 = AstNode("WHILE-BODY",[])
	if(type(p[5]) is list):
		for n in p[5]:
			newAstNode2.astChildList += n['astChildList']
	else:
		newAstNode2.astChildList += p[5]['astChildList']
	newAstNode.astChildList += [newAstNode2]
	p[0] = {'astChildList':[newAstNode]}

def p_iteration_statement2(p):
	'''iteration_statement : DO statement WHILE LPAREN expression RPAREN SEMI
							'''
	#print "iteration_statement"
	#p[0]=("iteration_statement",)+tuple(p[-len(p)+1:])
	newAstNode = AstNode(p[1],[])
	newAstNode2 = AstNode("DO-BODY",[])
	if(type(p[2]) is list):
		for n in p[2]:
			newAstNode2.astChildList += n['astChildList']
	else:
		newAstNode2.astChildList += p[2]['astChildList']
	newAstNode.astChildList += [newAstNode2]
	newAstNode2 = AstNode("DO-CONDITION",p[5]['astChildList'])
	newAstNode.astChildList += [newAstNode2]
	p[0] = {'astChildList':[newAstNode]}


def p_iteration_statement3(p):
	'''iteration_statement : FOR LPAREN expression_statement expression_statement RPAREN statement
							| FOR LPAREN expression_statement expression_statement expression RPAREN statement
							'''
	#print "iteration_statement"
	#p[0]=("iteration_statement",)+tuple(p[-len(p)+1:])
	if(len(p) == 7):
		newAstNode = AstNode(p[1],[])
		newAstNode2 = AstNode("FOR-INIT",p[3]['astChildList'])
		newAstNode.astChildList += [newAstNode2]
		
		newAstNode2 = AstNode("FOR-CONDITION",p[4]['astChildList'])
		newAstNode.astChildList += [newAstNode2]

		newAstNode2 = AstNode("FOR-INCREMENT",[AstNode("NULL",[])])
		newAstNode.astChildList += [newAstNode2]
		
		newAstNode2 = AstNode("FOR-BODY",[])
		if(type(p[6]) is list):
			for n in p[6]:
				newAstNode2.astChildList += n['astChildList']
		else:
			newAstNode2.astChildList += p[6]['astChildList']
		newAstNode.astChildList += [newAstNode2]
		p[0] = {'astChildList':[newAstNode]}
	else:
		newAstNode = AstNode(p[1],[])
		newAstNode2 = AstNode("FOR-INIT",p[3]['astChildList'])
		newAstNode.astChildList += [newAstNode2]
		
		newAstNode2 = AstNode("FOR-CONDITION",p[4]['astChildList'])
		newAstNode.astChildList += [newAstNode2]

		newAstNode2 = AstNode("FOR-INCREMENT",p[5]['astChildList'])
		newAstNode.astChildList += [newAstNode2]
		
		newAstNode2 = AstNode("FOR-BODY",[])
		if(type(p[7]) is list):
			for n in p[7]:
				newAstNode2.astChildList += n['astChildList']
		else:
			newAstNode2.astChildList += p[7]['astChildList']
		newAstNode.astChildList += [newAstNode2]
		p[0] = {'astChildList':[newAstNode]}

def p_iteration_statement4(p):
	'''iteration_statement : FOR LPAREN declaration expression_statement RPAREN statement
							| FOR LPAREN declaration expression_statement expression RPAREN statement
							 '''
	#print "iteration_statement"
	#p[0]=("iteration_statement",)+tuple(p[-len(p)+1:])
	if(len(p) == 7):
		newAstNode = AstNode(p[1],[])
		newAstNode2 = AstNode("FOR-INIT",p[3]['astChildList'])
		newAstNode.astChildList += [newAstNode2]
		
		newAstNode2 = AstNode("FOR-CONDITION",p[4]['astChildList'])
		newAstNode.astChildList += [newAstNode2]

		newAstNode2 = AstNode("FOR-INCREMENT",[AstNode("NULL",[])])
		newAstNode.astChildList += [newAstNode2]
		
		newAstNode2 = AstNode("FOR-BODY",[])
		if(type(p[6]) is list):
			for n in p[6]:
				newAstNode2.astChildList += n['astChildList']
		else:
			newAstNode2.astChildList += p[6]['astChildList']
		newAstNode.astChildList += [newAstNode2]
		p[0] = {'astChildList':[newAstNode]}
	else:
		newAstNode = AstNode(p[1],[])
		newAstNode2 = AstNode("FOR-INIT",p[3]['astChildList'])
		newAstNode.astChildList += [newAstNode2]
		
		newAstNode2 = AstNode("FOR-CONDITION",p[4]['astChildList'])
		newAstNode.astChildList += [newAstNode2]

		newAstNode2 = AstNode("FOR-INCREMENT",p[5]['astChildList'])
		newAstNode.astChildList += [newAstNode2]
		
		newAstNode2 = AstNode("FOR-BODY",[])
		if(type(p[7]) is list):
			for n in p[7]:
				newAstNode2.astChildList += n['astChildList']
		else:
			newAstNode2.astChildList += p[7]['astChildList']
		newAstNode.astChildList += [newAstNode2]
		p[0] = {'astChildList':[newAstNode]}

def p_jump_statement(p):
	'''jump_statement : GOTO IDENTIFIER SEMI 
						| CONTINUE SEMI
						| BREAK SEMI '''
	#print "jump_statement"
	#p[0]=("jump_statement",)+tuple(p[-len(p)+1:])

def p_jump_statement2(p):
	'''jump_statement : RETURN SEMI
						| RETURN expression SEMI '''
	#print "jump_statement"
	#p[0]=("jump_statement",)+tuple(p[-len(p)+1:])
	global returnSpecifier
	
	if(len(p) == 3):
		returnSpecifier = 'void'
		p[0] = {'TYPE':'void'}
	else:
		returnSpecifier = str(p[2]['TYPE'])
		p[0] = p[2]

def p_external_declaration(p):
	'''external_declaration : function_definition
							| declaration '''
	#print "external_declaration"
	#p[0]=("external_declaration",)+tuple(p[-len(p)+1:])
	p[0] = p[1]

def p_function_definition(p):
	'''function_definition : declaration_specifiers declarator declaration_list compound_statement
							| declaration_specifiers declarator compound_statement '''
	#print "function_definition"
	#p[0]=("function_definition",)+tuple(p[-len(p)+1:])
	
	global FUNCTION_LIST_DEFINITION
	global FUNCTION_LIST_DECLARATION
	global functions
	global parameter_symbol_table
	global returnSpecifier

	#--------- return type check of a function
	#if(str(p[1]['TYPE']) != 'void'):
	#	if(returnSpecifier == ''):
	#		print "Error at line number", p.lineno(1) ,"return statement not found for function ", str(p[2][0])
	#		sys.exit()
	#	if(returnSpecifier != str(p[1]['TYPE'])):
	#		print "Error at line number", p.lineno(1) ,"invalid return statement for function ", str(p[2][0])
	#		sys.exit()
	#else:
	#	if(returnSpecifier != str(p[1]['TYPE'])):
	#		print "Error at line number", p.lineno(1) ,"invalid return statement for function ", str(p[2][0])
	#		sys.exit()

	returnSpecifier = 'void'
	#sys.call()
	if(len(p) == 5 ):
		p[0] = {'NODE_TYPE':'function_declaration', 'OUTPUT':p[1]['TYPE'], 'INPUT': p[2][0], 'IDENTIFIER': p[2][0],'partProgram': p[4]}
		flag = 0
		for func in FUNCTION_LIST_DECLARATION :
				#print t[2]
				if(p[2][0] in func['NAME'] or p[2][0] == 'main'):
					flag=1
					func['partProgram'] = p[4]
					break
		if(flag != 1):
			print "function definition missing for ",p[2][0]
			currentfunction = {'Function Detail':p[0],'symboltable':parameter_symbol_table}
			functions = functions + [currentfunction]
			CURRENT_DECLARATION = [{"NAME":p[2][0],"INPUT":p[2][0],"OUTPUT":p[1]['TYPE']}]
			FUNCTION_LIST_DEFINITION = FUNCTION_LIST_DEFINITION + CURRENT_DECLARATION
			print_symbol_table(parameter_symbol_table,1)
			parameter_symbol_table = SymbolTable(-1)	

			
	elif(len(p) == 4 ):
		inp=[]
		ptr = []
		#print p[2][-1]
		if(len(p[2]) <= 2):
			inp = ['void']
			ptr = [0]
		else:
			for i in p[2][1]:
				inp=inp+[i[0]['TYPE']]
				ptr=ptr+[i[1]['POINTER']]
		p[0] = {'NODE_TYPE':'function_declaration', 'OUTPUT':p[1]['TYPE'], 'INPUT': inp, 'IDENTIFIER': p[2][0],'OUTPUT POINTER':p[2][-1],'INPUT POINTERS':ptr}
		#print p[2][1][0]
		flag = 0
		for func in FUNCTION_LIST_DECLARATION :
			if(p[2][0] in func['NAME']):
				if(str(func['INPUT']) != str(inp) or str(func['INPUT POINTERS']) != str(ptr)):
					print "Error at line number", p.lineno(1) ,":function definition mismatch errors"
					sys.exit()
					#raise SyntaxError
		for func in FUNCTION_LIST_DEFINITION :
				if(p[2][0] in func['NAME']):
					flag=1
					print "Error at line number", p.lineno(1) ,":function already defined"
					#raise SyntaxError
					break
		#print p[2][1][0]
		if(flag != 1):
			#print p[2][1][0]
			#print "function definition missing for ",p[2][0]
			currentfunction = {'Function Detail':p[0],'symboltable':parameter_symbol_table}
			#print p[2][1][0]
			functions = functions + [currentfunction]
			CURRENT_DECLARATION = [{"NAME":p[2][0],"INPUT":inp,"OUTPUT":p[1]['TYPE'],'OUTPUT POINTER':p[2][-1],'INPUT POINTERS':ptr}]
			#print len(p[2][1][0])
			FUNCTION_LIST_DEFINITION = FUNCTION_LIST_DEFINITION + CURRENT_DECLARATION
			print_symbol_table(parameter_symbol_table,1)
			parameter_symbol_table = SymbolTable(-1)
		newAstNode = p[1]['astChildList'][0]
		newFunAstNode = AstNode(p[2][0],[])
		if(type(p[3]) is list):
			for n in p[3]:
				while (type(n) is list):
					n = n[0]
				newFunAstNode.astChildList += n['astChildList']
		else:
			newFunAstNode.astChildList += p[3]['astChildList']
		newAstNode.astChildList += [newFunAstNode]
		if(len(p[2]) > 2):
			for n in p[2][1]:
				newAstNode2 = AstNode(n[0]['TYPE'],[])
				newAstNode3 = AstNode(n[1]['ID'],[])
				newAstNode2.astChildList += [newAstNode3]
				newAstNode.astChildList += [newAstNode2]
		p[0] = {}	
		p[0]['astChildList'] = [newAstNode]

def p_declaration_list(p):
	'''declaration_list : declaration
						| declaration_list declaration '''
	#print "declaration_list"
	#p[0]=("declaration_list",)+tuple(p[-len(p)+1:])
	
	if(len(p)==2):
		p[0]=[p[1]]
	if(len(p) == 3):
		p[0]=p[1] + [p[3]]



def p_leftbrace(p):
	''' left_brace : LBRACE
					'''
	#p[0] = p[1]
	#print "-----Making NewSymbolTable---------"
	global structDeclarationCount
	global currentSymbolTable
	global currentStructName

	#currentSymbolTable.structChildList += [SymbolTable.TableNumber]
	currentSymbolTable = SymbolTable(currentSymbolTable)
	if(structDeclarationCount > 0):
		currentSymbolTable.isStructTable = True
		currentSymbolTable.structName = currentStructName
		currentSymbolTable.father.structChildList += [currentSymbolTable]

def p_righttbrace(p):
	''' right_brace : RBRACE
					'''
	#p[0] = p[1]
	#print "--------EXITING CURRENT SYMBOL TABLE--------------"
	global currentSymbolTable
	global structDeclarationCount
	global currentStructName

	currentStructName = ''
	print_symbol_table(currentSymbolTable,0)
	currentSymbolTable = currentSymbolTable.father
	print_symbol_table(currentSymbolTable,0)
	if(structDeclarationCount > 0):
		structDeclarationCount = structDeclarationCount - 1






########################### end


	
def p_error(p):
	global flag_for_error
	flag_for_error = 1

	if p is not None:
		print("error at line no:  %s :: %s"%((p.lineno),(p.value)))
		parser.errok()
	else:
		print("Unexpected end of input")


if __name__ == "__main__":
	import profile
	
	if len(sys.argv) < 2:
		print "No input file specified"
	else:
		parser = yacc.yacc()
		fo = open(str(sys.argv[1]), "r+")
		data = fo.read()
		fo.close()
		tree = yacc.parse(data,tracking=True)
		if tree is not None and flag_for_error == 0:
			#createParseTree.create_tree(tree,str(sys.argv[1]))
			#print "Parse tree created : "+str(sys.argv[1])+"tree.svg"
			#os.system("eog "+str(sys.argv[1])+"tree.svg")
			rootAstNode = AstNode("AST_ROOT_NODE",[])
			for n in tree:
				rootAstNode.astChildList += n['astChildList']
			createAST.create_tree(rootAstNode,str(sys.argv[1]))
			os.system("eog "+str(sys.argv[1])+"tree.svg")
			#print rootAstNode.astChildList[0].astChildList[0].astChildList[1].astChildList[0].astChildList[1].astChildList


		#yacc.yacc(method='LALR',write_tables=False,debug=False)

		#profile.run("yacc.yacc(method='LALR')")
