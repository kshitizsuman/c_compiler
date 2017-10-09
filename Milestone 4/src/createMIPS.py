from SymbolTable import *

data_section = []
text_section = []
global_text = []
global if_begin

addressDescriptor = {}
activation_record = []
registerDescriptor = { '$t0' : None, '$t1' : None, '$t2' : None, '$t3' : None, '$t4' : None, '$t5' : None,  '$t6' : None, '$t7' : None, '$t8' : None, '$t9' : None, '$s0' : None, '$s1' : None, '$s2' : None, '$s3' : None, '$s4' : None }
freeRegisters = ['$s4','$s3','$s2','$s1','$s0','$t9', '$t8', '$t7', '$t6', '$t5', '$t4', '$t3', '$t2', '$t1', '$t0']
parameterDescriptor={ '$a1' : None, '$a2' : None, '$a3' : None}
busyRegisters = []
funlist = {}
lru_list = []
freed_labels = {}

declaredVars = []
global currentSymbolTable
global symbolTableStack
symbolTableStack = []
global tempVarCounter

def reset_reg():
	global registerDescriptor
	global freeRegisters
	global busyRegisters
	global parameterDescriptor
	global addressDescriptor

	addressDescriptor = {}
	registerDescriptor = { '$t0' : None, '$t1' : None, '$t2' : None, '$t3' : None, '$t4' : None, '$t5' : None,  '$t6' : None, '$t7' : None, '$t8' : None, '$t9' : None, '$s0' : None, '$s1' : None, '$s2' : None, '$s3' : None, '$s4' : None }
	freeRegisters = ['$s4','$s3','$s2','$s1','$s0','$t9', '$t8', '$t7', '$t6', '$t5', '$t4', '$t3', '$t2', '$t1', '$t0']
	busyRegisters = []	
	parameterDescriptor={ '$a1' : None, '$a2' : None, '$a3' : None}

def convName(var):
	global currentSymbolTable
	tmp = currentSymbolTable.lookup(var)
	if(tmp == False):
		return ('VAR_'+currentSymbolTable.tableName+"_"+var)
	else:
		return ('VAR_'+tmp['scope']+"_"+var)
				
def addIns(ins):
	global if_begin
	global text_section
	global global_text

	if(if_begin == 1):
		text_section += [ins]
	else:
		global_text += [ins]

def isVar(var):
	#global currentSymbolTable
	#global tempVarCounter
	#if(currentSymbolTable.lookup(var) == False):
	#	if(var[0:2] == 't_' and int(var[2:]) <= tempVarCounter):
	#		return True
	#	return False
	#return True
	if(var[0] == '-'):
		return False
	return (not var.isdigit())

def getReg(var):
	global registerDescriptor
	global freeRegisters
	global busyRegisters
	global addressDescriptor
	global text_section
	global declaredVars
	global parameterDescriptor
	global funlist
	global lru_list
	
	register = ""
	if(var.split("_")[1] == 'GLOBALTABLE'):
		of = currentSymbolTable.lookup(var.split("_")[-1])['offset']
		if len(freeRegisters):
			register = freeRegisters.pop()
		#register = freeRegisters.pop()
		addIns("\taddi\t"+register+",\t$zero,\t"+str(of))
		addIns("\tlw\t"+register+",\tVAR_global"+"("+register+")")
	elif(currentSymbolTable.lookupCurrentParameter(var.split("_")[-1]) != False):
		reg = "$a" + str(funlist[currentSymbolTable.tableName].index(var.split("_")[-1]) + 1)
		return reg 
	elif(var in registerDescriptor.values()):
		register = addressDescriptor[var]
	else:
		if(len(freeRegisters) == 0):
			for x in lru_list:
				onhold_reg = x        #assigned register
				assigned_var = registerDescriptor[onhold_reg]      # checked the previously alloted variable
				c_var = assigned_var.split("_")       #c code name of the variable
				name = c_var[-1] 
				if(name.isdigit() == False):              #if it is not a label
					addIns("\tsw\t"+onhold_reg+",\t"+assigned_var)          #store the register value in the memory
					registerDescriptor[onhold_reg] = var         # assign the register to the alloted variable
					tmp_var = addressdescriptor.pop(assigned_var,None)        #delete the entry from the addressDescriptor
					addressdescriptor[var] = onhold_reg          # add entry to the address Descriptor
					break
			register = onhold_reg
			if register in lru_list:
				lru_list.remove(register)			
		else:
			register = freeRegisters.pop()
			addressDescriptor[var] = register
			busyRegisters.append(register)
			registerDescriptor[register] = var
			if(var in declaredVars):
				addIns("\tlw\t"+register+",\t"+var)
	lru_list.append(register)
	return register

def data_size(data_type):
	if(data_type=="float"):
		return 4
	if(data_type == "int"):
		return 4;
	if(data_type == "double"):
		return 8
	if(data_type == "char"):
		return 1


def lifeSpan(code):
	#print "\n\n\n\n >>>>>>> \n\n\n\n\n"
	global freed_labels
	operators = ["+","-","*","/","",">=","<=","==","=","++","--","&&","||","!",">","<"]
	ind = len(code) - 1                  # get the line of code
	while ind >= 0 :                     # for each line backwards
		if(code[ind][0] in operators ):                #  if it is a operator
			for element in code[ind][2:]:             # for each label in the right of th operator
				if(isVar(element) and element[0]=="t"):           # if the label is t_12
					if(element not in freed_labels.keys()):         # if the label has not been freed yet
						freed_labels[element] = ind               # add key to the dictionary 
		elif(code[ind][0]=='IF'):
			element = code[ind][1]
			if(isVar(element) and element[0]=="t"):
				if(element not in freed_labels.keys()):         # if the label has not been freed yet
						freed_labels[element] = ind
			element=code[ind][3]
			if(isVar(element) and element[0]=="t"):
				if(element not in freed_labels.keys()):         # if the label has not been freed yet
						freed_labels[element] = ind

		ind -= 1

def create_mips(code,symboltable,tempVarcounter):
	global data_section
	global text_section
	global declaredVars
	global currentSymbolTable
	global tempVarCounter
	global global_text
	global if_begin
	global registerDescriptor
	global freeRegisters
	global busyRegisters
	global parameterDescriptor
	global addressDescriptor
	global funlist
	global freed_labels
	#lifeSpan(code,symboltable)

	tempVarCounter = tempVarcounter
	currentSymbolTable = symboltable
	if_main = 0
	if_begin = 0
	ind=0
	data_section += ["\tVAR_global:\t.space\t"+str(currentSymbolTable.offset_count)]
	for line in code:
		if(code[ind][0]=='GETARRAY' and (ind+1 < len(code))):
			if((code[ind+1][0]=='FCALL' and code[ind+1][1]=='get')):
				tmp_line = line
				tmp_line[0] = 'PUTARRAY'
				code.insert(ind+2,tmp_line)
		ind += 1

	lifeSpan(code)
	#print freed_labels

	#print "----------- Three Address Code -----------\n"
	ind=0
	for line in code:
		#print line,"\t"
		if(line != []):
			if(line[0] == 'ARRDECLARATION'):
				tmp = currentSymbolTable.lookup(line[2])
				if(tmp['scope'] != 'GLOBALTABLE'):
					if(int(line[3])==2):
						tot_mem=(int(line[4])*int(line[5]))*data_size(line[1])
						#check the data type here of the array
						data_section += ["\tVAR_"+line[2]+":\t.space\t"+str(tot_mem)]
					if(int(line[3])==1):
						tot_mem =(int(line[4]))*data_size(line[1])
						data_section += ["\tVAR_"+line[2]+":\t.space\t"+str(tot_mem)]
						#check the data type here of the array
			elif(line[0] == 'GETARRAY'):
				tmp = currentSymbolTable.lookup(line[2])
				if(tmp['scope'] != 'GLOBALTABLE'):
					if(line[3] == '1'):
						if(line[4].isdigit()):
							offset=4*int(line[4])
							
							offset_register = getReg(convName(line[1]))
							addIns("\taddi\t"+offset_register+",\t$zero,\t"+str(offset))
							addIns("\tlw\t"+offset_register+",\tVAR_"+line[2]+"("+offset_register+")")
							
						elif(isVar(line[4])):
							register=getReg(convName(line[4]))
							offset_register = getReg(convName(line[1]))
							addIns("\tmul\t"+offset_register+",\t"+register+",\t4")
							addIns("\tlw\t"+offset_register+",\tVAR_"+line[2]+"("+offset_register+")")
							
					elif(line[3] == '2'):  #change the the offset as the product of current row and the total number of columns 
						#need the dimension of the 2-d array
						arrdet = currentSymbolTable.lookup(line[2])
						col = arrdet['dimension'][1]

						if(line[4].isdigit() and line[5].isdigit()):
							#offset = data_size('int')*int(line[4])*int(line[5])
							#offset_register = freeRegisters.pop()
							offset = (int(line[4])*col + int(line[5]))*data_size(arrdet['output'])
							offset_register = getReg(convName(line[1]))
							addIns("\taddi\t"+offset_register+",\t$zero,\t"+str(offset))
							addIns("\tlw\t"+offset_register+",\tVAR_"+line[2]+"("+offset_register+")")
							
						elif(isVar(line[4]) and line[5].isdigit()):
							reg_var= getReg(convName(line[4]))
							offset_register = getReg(convName(line[1]))
							addIns("\tmul\t"+offset_register+",\t"+reg_var+",\t"+str(col))
							addIns("\taddi\t"+offset_register+",\t"+offset_register+",\t"+line[5])
							addIns("\tmul\t"+offset_register+",\t"+offset_register+",\t"+str(data_size(arrdet['output'])))
							addIns("\tlw\t"+offset_register+",\tVAR_"+line[2]+"("+offset_register+")")

						elif(line[4].isdigit() and isVar(line[5])):
							reg_var= getReg(convName(line[5]))
							offset_register = getReg(convName(line[1]))
							addIns("\taddi\t"+offset_register+",\t$zero,\t"+str(int(line[4])*col))
							addIns("\tadd\t"+offset_register+",\t"+offset_register+",\t"+reg_var)
							addIns("\tmul\t"+offset_register+",\t"+offset_register+",\t"+str(data_size('int')))
							addIns("\tlw\t"+offset_register+",\tVAR_"+line[2]+"("+offset_register+")")
						
						elif(isVar(line[4]) and isVar(line[5])):
							reg_var1 = getReg(convName(line[4]))
							reg_var2 = getReg(convName(line[5]))
							offset_register = getReg(convName(line[1]))
							addIns("\tmul\t"+offset_register+",\t"+reg_var1+",\t"+str(col))
							addIns("\tadd\t"+offset_register+",\t"+offset_register+",\t"+reg_var2)
							addIns("\tmul\t"+offset_register+",\t"+offset_register+",\t"+str(data_size('int')))
							addIns("\tlw\t"+offset_register+",\tVAR_"+line[2]+"("+offset_register+")")
				else:
					#print tmp['offset']
					if(line[3] == '1'):
						if(line[4].isdigit()):
							offset=4*int(line[4])+tmp['offset']
							
							offset_register = getReg(convName(line[1]))
							addIns("\taddi\t"+offset_register+",\t$zero,\t"+str(offset))
							addIns("\tlw\t"+offset_register+",\tVAR_global"+"("+offset_register+")")
							
						elif(isVar(line[4])):
							register=getReg(convName(line[4]))
							offset_register = getReg(convName(line[1]))

							addIns("\tmul\t"+offset_register+",\t"+register+",\t4")
							addIns("\taddi\t"+offset_register+",\t"+offset_register+",\t"+str(tmp['offset']))
							addIns("\tlw\t"+offset_register+",\tVAR_global"+"("+offset_register+")")
							
					elif(line[3] == '2'):  #change the the offset as the product of current row and the total number of columns 
						#need the dimension of the 2-d array
						arrdet = currentSymbolTable.lookup(line[2])
						col = arrdet['dimension'][1]

						if(line[4].isdigit() and line[5].isdigit()):
							#offset = data_size('int')*int(line[4])*int(line[5])
							#offset_register = freeRegisters.pop()
							offset = (int(line[4])*col + int(line[5]))*data_size(arrdet['output'])+tmp['offset']
							offset_register = getReg(convName(line[1]))
							addIns("\taddi\t"+offset_register+",\t$zero,\t"+str(offset))
							addIns("\tlw\t"+offset_register+",\tVAR_global"+"("+offset_register+")")
							
						elif(isVar(line[4]) and line[5].isdigit()):
							reg_var= getReg(convName(line[4]))
							offset_register = getReg(convName(line[1]))
							addIns("\tmul\t"+offset_register+",\t"+reg_var+",\t"+str(col))
							addIns("\taddi\t"+offset_register+",\t"+offset_register+",\t"+line[5])
							addIns("\tmul\t"+offset_register+",\t"+offset_register+",\t"+str(data_size(arrdet['output'])))
							addIns("\taddi\t"+offset_register+",\t"+offset_register+",\t"+str(tmp['offset']))
							addIns("\tlw\t"+offset_register+",\tVAR_global"+"("+offset_register+")")

						elif(line[4].isdigit() and isVar(line[5])):
							reg_var= getReg(convName(line[5]))
							offset_register = getReg(convName(line[1]))
							addIns("\taddi\t"+offset_register+",\t$zero,\t"+str(int(line[4])*col))
							addIns("\tadd\t"+offset_register+",\t"+offset_register+",\t"+reg_var)
							addIns("\tmul\t"+offset_register+",\t"+offset_register+",\t"+str(data_size('int')))
							addIns("\taddi\t"+offset_register+",\t"+offset_register+",\t"+str(tmp['offset']))
							addIns("\tlw\t"+offset_register+",\tVAR_global"+"("+offset_register+")")
						
						elif(isVar(line[4]) and isVar(line[5])):
							reg_var1 = getReg(convName(line[4]))
							reg_var2 = getReg(convName(line[5]))
							offset_register = getReg(convName(line[1]))
							addIns("\tmul\t"+offset_register+",\t"+reg_var1+",\t"+str(col))
							addIns("\tadd\t"+offset_register+",\t"+offset_register+",\t"+reg_var2)
							addIns("\tmul\t"+offset_register+",\t"+offset_register+",\t"+str(data_size('int')))
							addIns("\taddi\t"+offset_register+",\t"+offset_register+",\t"+str(tmp['offset']))
							addIns("\tlw\t"+offset_register+",\tVAR_global"+"("+offset_register+")")


			elif(line[0]=='PUTARRAY'):
				tmp = currentSymbolTable.lookup(line[2])
				if(tmp['scope'] != 'GLOBALTABLE'):
					if(line[3]=='1'):
						if(line[4].isdigit()):
							offset = data_size('int')*int(line[4])
							value_register = getReg(convName(line[1]))
							if len(freeRegisters):
								offset_register = freeRegisters.pop()
							addIns("\taddi\t"+offset_register+",\t$zero,\t"+str(offset))
							addIns("\tsw\t"+value_register+",\tVAR_"+line[2]+"("+offset_register+")")
							freeRegisters.append(offset_register)
							freeRegisters.append(value_register)
							x = addressDescriptor.pop(convName(line[1]) , None)
							if value_register in busyRegisters:
								busyRegisters.remove(value_register)
							registerDescriptor[value_register] = None
						
						elif(isVar(line[4])):
							index_register = getReg(convName(line[4]))
							value_register = getReg(convName(line[1]))
							if len(freeRegisters):
								offset_register = freeRegisters.pop()
							addIns("\tmul\t"+offset_register+",\t"+index_register+",\t"+str(data_size('int')))
							addIns("\tsw\t"+value_register+",\tVAR_"+line[2]+"("+offset_register+")")
							freeRegisters.append(offset_register)
							freeRegisters.append(value_register)
							x = addressDescriptor.pop(convName(line[1]) , None)
							if value_register in busyRegisters:
								busyRegisters.remove(value_register)
							registerDescriptor[value_register] = None

					elif(line[3]=='2'):   #change the offset as the product of the current row and total numnber of colums 
							arrdet = currentSymbolTable.lookup(line[2])
							col = arrdet['dimension'][1]
							if(line[4].isdigit() and line[5].isdigit()):
								#offset=data_size('int')*int(line[4])*int(line[5])
								offset = (int(line[4])*col + int(line[5]))*data_size(arrdet['output'])
								value_register = getReg(convName(line[1]))
								if len(freeRegisters):
									offset_register = freeRegisters.pop()
								addIns("\taddi\t"+offset_register+",\t$zero,\t"+str(offset))
								addIns("\tsw\t"+value_register+",\tVAR_"+line[2]+"("+offset_register+")")
								freeRegisters.append(offset_register)
								freeRegisters.append(value_register)
								x = addressDescriptor.pop(convName(line[1]) , None)
								if value_register in busyRegisters:
									busyRegisters.remove(value_register)
								registerDescriptor[value_register] = None

							if(line[4].isdigit() and isVar(line[5])):
								index_register = getReg(convName(line[5]))
								if len(freeRegisters):
									offset_register = freeRegisters.pop()
								addIns("\taddi\t"+offset_register+",\t$zero,\t"+str(int(line[4])*col))
								addIns("\tadd\t"+offset_register+",\t"+offset_register+",\t"+index_register)
								addIns("\tmul\t"+offset_register+",\t"+offset_register+",\t"+str(data_size(arrdet['output'])))
								value_register = getReg(convName(line[1]))
								addIns("\tsw\t"+value_register+",\tVAR_"+line[2]+"("+offset_register+")")
								freeRegisters.append(offset_register)
								freeRegisters.append(value_register)
								x = addressDescriptor.pop(convName(line[1]) , None)
								if value_register in busyRegisters:
									busyRegisters.remove(value_register)
								registerDescriptor[value_register] = None

							if(isVar(line[4]) and line[5].isdigit()):
								index_register = getReg(convName(line[4]))
								offset_register = freeRegisters.pop()
								addIns("\tmul\t"+offset_register+",\t"+index_register+",\t"+str(col))
								addIns("\taddi\t"+offset_register+",\t"+offset_register+",\t"+line[5])
								addIns("\tmul\t"+offset_register+",\t"+offset_register+",\t"+str(data_size(arrdet['output'])))
								value_register = getReg(convName(line[1]))
								addIns("\tsw\t"+value_register+",\tVAR_"+line[2]+"("+offset_register+")")
								freeRegisters.append(offset_register)
								freeRegisters.append(value_register)
								x = addressDescriptor.pop(convName(line[1]) , None)
								if value_register in busyRegisters:
									busyRegisters.remove(value_register)
								registerDescriptor[value_register] = None

							if(isVar(line[4]) and isVar(line[5])):
								index_register1 = getReg(convName(line[4]))
								index_register2 = getReg(convName(line[5]))
								if len(freeRegisters):
									offset_register = freeRegisters.pop()
								addIns("\tmul\t"+offset_register+",\t"+index_register1+",\t"+str(col))
								addIns("\tadd\t"+offset_register+",\t"+offset_register+",\t"+index_register2)
								addIns("\tmul\t"+offset_register+",\t"+offset_register+",\t"+str(data_size(arrdet['output'])))
								value_register = getReg(convName(line[1]))
								addIns("\tsw\t"+value_register+",\tVAR_"+line[2]+"("+offset_register+")")
								freeRegisters.append(offset_register)
								freeRegisters.append(value_register)
								x = addressDescriptor.pop(convName(line[1]) , None)
								if value_register in busyRegisters:
									busyRegisters.remove(value_register)
								registerDescriptor[value_register] = None
				else:
					if(line[3]=='1'):
						if(line[4].isdigit()):
							offset = data_size('int')*int(line[4])+tmp['offset']
							value_register = getReg(convName(line[1]))
							if len(freeRegisters):
								offset_register = freeRegisters.pop()
							addIns("\taddi\t"+offset_register+",\t$zero,\t"+str(offset))
							addIns("\tsw\t"+value_register+",\tVAR_global"+"("+offset_register+")")
							freeRegisters.append(offset_register)
							freeRegisters.append(value_register)
							x = addressDescriptor.pop(convName(line[1]) , None)
							if value_register in busyRegisters:
									busyRegisters.remove(value_register)
							registerDescriptor[value_register] = None
						
						elif(isVar(line[4])):
							index_register = getReg(convName(line[4]))
							value_register = getReg(convName(line[1]))
							if len(freeRegisters):
								offset_register = freeRegisters.pop()
							addIns("\tmul\t"+offset_register+",\t"+index_register+",\t"+str(data_size('int')))
							addIns("\taddi\t"+offset_register+",\t"+offset_register+",\t"+str(tmp['offset']))
							addIns("\tsw\t"+value_register+",\tVAR_global"+"("+offset_register+")")
							freeRegisters.append(offset_register)
							freeRegisters.append(value_register)
							x = addressDescriptor.pop(convName(line[1]) , None)
							if value_register in busyRegisters:
									busyRegisters.remove(value_register)
							registerDescriptor[value_register] = None
					elif(line[3]=='2'):   #change the offset as the product of the current row and total numnber of colums 
							arrdet = currentSymbolTable.lookup(line[2])
							col = arrdet['dimension'][1]
							if(line[4].isdigit() and line[5].isdigit()):
								#offset=data_size('int')*int(line[4])*int(line[5])
								offset = (int(line[4])*col + int(line[5]))*data_size(arrdet['output'])+tmp['offset']
								value_register = getReg(convName(line[1]))
								if len(freeRegisters):
									offset_register = freeRegisters.pop()
								addIns("\taddi\t"+offset_register+",\t$zero,\t"+str(offset))
								addIns("\tsw\t"+value_register+",\tVAR_global"+"("+offset_register+")")
								freeRegisters.append(offset_register)
								freeRegisters.append(value_register)
								x = addressDescriptor.pop(convName(line[1]) , None)
								if value_register in busyRegisters:
									busyRegisters.remove(value_register)
								registerDescriptor[value_register] = None

							if(line[4].isdigit() and isVar(line[5])):
								index_register = getReg(convName(line[5]))
								if len(freeRegisters):
									offset_register = freeRegisters.pop()
								addIns("\taddi\t"+offset_register+",\t$zero,\t"+str(int(line[4])*col))
								addIns("\tadd\t"+offset_register+",\t"+offset_register+",\t"+index_register)
								addIns("\tmul\t"+offset_register+",\t"+offset_register+",\t"+str(data_size(arrdet['output'])))
								value_register = getReg(convName(line[1]))
								addIns("\taddi\t"+offset_register+",\t"+offset_register+",\t"+str(tmp['offset']))
								addIns("\tsw\t"+value_register+",\tVAR_global"+"("+offset_register+")")
								freeRegisters.append(offset_register)
								freeRegisters.append(value_register)
								x = addressDescriptor.pop(convName(line[1]) , None)
								if value_register in busyRegisters:
									busyRegisters.remove(value_register)
								registerDescriptor[value_register] = None

							if(isVar(line[4]) and line[5].isdigit()):
								index_register = getReg(convName(line[4]))
								if len(freeRegisters):
									offset_register = freeRegisters.pop()
								addIns("\tmul\t"+offset_register+",\t"+index_register+",\t"+str(col))
								addIns("\taddi\t"+offset_register+",\t"+offset_register+",\t"+line[5])
								addIns("\tmul\t"+offset_register+",\t"+offset_register+",\t"+str(data_size(arrdet['output'])))
								value_register = getReg(convName(line[1]))
								addIns("\taddi\t"+offset_register+",\t"+offset_register+",\t"+str(tmp['offset']))
								addIns("\tsw\t"+value_register+",\tVAR_global"+"("+offset_register+")")
								freeRegisters.append(offset_register)
								freeRegisters.append(value_register)
								x = addressDescriptor.pop(convName(line[1]) , None)
								if value_register in busyRegisters:
									busyRegisters.remove(value_register)
								registerDescriptor[value_register] = None

							if(isVar(line[4]) and isVar(line[5])):
								index_register1 = getReg(convName(line[4]))
								index_register2 = getReg(convName(line[5]))
								if len(freeRegisters):
									offset_register = freeRegisters.pop()
								addIns("\tmul\t"+offset_register+",\t"+index_register1+",\t"+str(col))
								addIns("\tadd\t"+offset_register+",\t"+offset_register+",\t"+index_register2)
								addIns("\tmul\t"+offset_register+",\t"+offset_register+",\t"+str(data_size(arrdet['output'])))
								value_register = getReg(convName(line[1]))
								addIns("\taddi\t"+offset_register+",\t"+offset_register+",\t"+str(tmp['offset']))
								addIns("\tsw\t"+value_register+",\tVAR_global"+"("+offset_register+")")
								freeRegisters.append(offset_register)
								freeRegisters.append(value_register)
								x = addressDescriptor.pop(convName(line[1]) , None)
								if value_register in busyRegisters:
									busyRegisters.remove(value_register)
								registerDescriptor[value_register] = None

			elif(line[0] == "!"):
				reg1 = getReg(convName(line[1]))
				reg2 = getReg(convName(line[2]))
				addIns("\tnot\t"+reg1+",\t"+reg2)

			elif(line[0]=='&&'):
				if(isVar(line[2]) and isVar(line[3])):
					reg1=getReg(convName(line[1]))
					reg2=getReg(convName(line[2]))
					reg3=getReg(convName(line[3]))
					addIns("\tand\t"+reg1+",\t"+reg2+",\t"+reg3)

				elif(isVar(line[2]) and line[3].isdigit()):
					reg1=getReg(convName(line[1]))
					reg2=getReg(convName(line[2]))
					addIns("\tandi\t"+reg1+",\t"+reg2+",\t"+line[3])

				elif(isVar(line[3]) and line[2].isdigit()):
					reg1=getReg(convName(line[1]))
					reg2=getReg(convName(line[3]))
					addIns("\tandi\t"+reg1+",\t"+reg2+",\t"+line[2])

			elif(line[0]=='||'):
				if(isVar(line[2]) and isVar(line[3])):
					reg1=getReg(convName(line[1]))
					reg2=getReg(convName(line[2]))
					reg3=getReg(convName(line[3]))
					addIns("\tor\t"+reg1+",\t"+reg2+",\t"+reg3)

				elif(isVar(line[2]) and line[3].isdigit()):
					reg1=getReg(convName(line[1]))
					reg2=getReg(convName(line[2]))
					addIns("\tori\t"+reg1+",\t"+reg2+",\t"+line[3])

				elif(isVar(line[3]) and line[2].isdigit()):
					reg1=getReg(convName(line[1]))
					reg2=getReg(convName(line[3]))
					addIns("\tori\t"+reg1+",\t"+reg2+",\t"+line[2])			

			elif(line[0]=='FCALL'):
				if(line[1] == 'typeof'):
					data_section += ['\tSTR_'+str(ind)+':\t.asciiz\t'+'"'+line[-1]+'"']
					addIns("\tli\t$v0,\t4")
					addIns("\tla\t$a0,\tSTR_"+str(ind))
					addIns("\tsyscall")
					addIns("\tli\t$v0,\t4")
					addIns("\tla\t$a0,\tnewLine")
					addIns("\tsyscall")
					ind = ind + 1
					continue
				if(line[1] == 'get'):
					addIns("\tli\t$v0,\t5")
					addIns("\tsyscall")
					register = getReg(convName(line[-1]))
					addIns("\tmove\t"+register+",\t$v0")
					tmp = currentSymbolTable.lookup(line[-1])
					if(tmp != False):
						if(tmp['scope'] == 'GLOBALTABLE'):
							if len(freeRegisters):
								reg = freeRegisters.pop()
							addIns("\taddi\t"+reg+",\t$zero,\t"+str(tmp['offset']))
							addIns("\tsw\t"+register+",\tVAR_global"+"("+reg+")")
							freeRegisters.append(reg)
							freeRegisters.append(register)
					ind = ind+1
					continue
				if(line[1] == 'put'):
					addIns("\tli\t$v0,\t1")
					if(isVar(line[-1])):
						register = getReg(convName(line[-1]))
						addIns("\tmove\t$a0,\t"+register)
					else:
						addIns("\tli\t$a0,\t"+line[-1])
					addIns("\tsyscall")
					addIns("\tli\t$v0,\t4")
					addIns("\tla\t$a0,\tnewLine")
					addIns("\tsyscall")
					ind = ind + 1
					continue
				counter=0
				tmp_dict = {}
				tmp_dict['registerDescriptor'] = registerDescriptor
				tmp_dict['freeRegister'] = freeRegisters
				tmp_dict['busyRegisters'] = busyRegisters
				tmp_dict['parameterDescriptor'] = parameterDescriptor
				tmp_dict['addressDescriptor'] = addressDescriptor
				activation_record.append(tmp_dict)
				for x in registerDescriptor.keys():
					if registerDescriptor[x] != None:
						addIns("\taddi\t$sp,\t$sp,\t-4")
						addIns("\tsw\t"+x+",\t0($sp)")
				#print parameterDescriptor,"_________"
				for x in parameterDescriptor.keys():
					if parameterDescriptor[x] != None:
						addIns("\taddi\t$sp,\t$sp,\t-4")
						addIns("\tsw\t"+x+",\t0($sp)")
				#print registerDescriptor
				if(line[-1]=='PARAMS'):
					#there are no parameters
					reset_reg()		
					addIns("\tjal\t"+line[1])
					#check whether it returns somthing or not
					tmp_dict = activation_record.pop()
					registerDescriptor = tmp_dict['registerDescriptor'] 
					freeRegisters = tmp_dict['freeRegister']
					busyRegisters = tmp_dict['busyRegisters']
					parameterDescriptor = tmp_dict['parameterDescriptor']
					addressDescriptor = tmp_dict['addressDescriptor']
					for x in registerDescriptor.keys()[::-1]:
						if registerDescriptor[x] != None:
							addIns("\tlw\t"+x+",\t0($sp)")
							addIns("\taddi\t$sp,\t$sp,\t4")

					for x in parameterDescriptor.keys()[::-1]:
						if parameterDescriptor[x] != None:
							addIns("\tlw\t"+x+",\t0($sp)")
							addIns("\taddi\t$sp,\t$sp,\t4")
					tmp = currentSymbolTable.lookup(line[1])
					if (tmp['output']=='void'):
						pass
					elif(tmp['output']=='int'):
						addIns("\tadd\t"+getReg(convName(line[3]))+",\t$zero,\t$v1")

				if(line[-1]!='PARAMS'):
					#there are parameters
					index = line.index('PARAMS')+1
					paras = line[index:]
					i=1
					if(len(paras) <= 3):
						for para in paras:
							if(isVar(para)):
								addIns("\tadd\t$a"+str(i)+",\t$zero,\t"+getReg(convName(para)))
							else:
								addIns("\taddi\t$a"+str(i)+",\t$zero,\t"+para)
							i=i+1
					else:
						for para in paras:
							if(isVar(para)):
								addIns("\taddi\t$sp,\t$sp,\t-4")
								addIns("\tsw\t"+getReg(convName(para))+",\t0($sp)")
							else:
								addIns("\taddi\t$sp,\t$sp,\t-4")
								addIns("\tsw\t"+para+",\t0($sp)")
					reset_reg()		
					addIns("\tjal\t"+line[1])
					#check whether it returns something or not
					tmp_dict = activation_record.pop()
					registerDescriptor = tmp_dict['registerDescriptor'] 
					freeRegisters = tmp_dict['freeRegister']
					busyRegisters = tmp_dict['busyRegisters']
					parameterDescriptor = tmp_dict['parameterDescriptor']
					addressDescriptor = tmp_dict['addressDescriptor']
					for x in parameterDescriptor.keys()[::-1]:
						if parameterDescriptor[x] != None:
							addIns("\tlw\t"+x+",\t0($sp)")
							addIns("\taddi\t$sp,\t$sp,\t4")
					
					for x in registerDescriptor.keys()[::-1]:
						if registerDescriptor[x] != None:
							addIns("\tlw\t"+x+",\t0($sp)")
							addIns("\taddi\t$sp,\t$sp,\t4")

					tmp = currentSymbolTable.lookup(line[1])
					if (tmp['output']=='void'):
						pass
					elif(tmp['output']=='int'):
						addIns("\tadd\t"+getReg(convName(line[3]))+",\t$zero,\t$v1")
			elif(line[0]=='RETURN'):
				if(line[1].isdigit()):
					addIns("\taddi\t$v1,\t$zero,\t"+line[1])
					addIns("\tlw\t$ra,\t0($sp)")
					addIns("\taddi\t$sp,\t$sp,\t4")
					addIns("\tjr\t$ra")
				else:
					addIns("\tadd\t$v1,\t$zero,\t"+getReg(convName(line[1])))
					addIns("\tlw\t$ra,\t0($sp)")
					addIns("\taddi\t$sp,\t$sp,\t4")
					addIns("\tjr\t$ra")

			elif(line[0] == 'BEGINFUCTION'):
				if_begin = 1
				symbolTableStack.append(currentSymbolTable)
				currentSymbolTable = currentSymbolTable.childList[line[2]]
				addIns(line[2]+':')
				if(line[2]=="main"):
					if_main =1
					reset_reg() 
				else:
					if_main=0
					paramtrs=line[5:][::2]
					funlist[currentSymbolTable.tableName] = line[5:][::2]
					count=1
					i=1
					if(len(paramtrs) <= 3):
						for para in paramtrs:
							if(isVar(para)):
								parameterDescriptor["$a"+str(i)] = 'VAR_'+currentSymbolTable.tableName+"_"+para 
								#addIns("\tadd\t$a"+str(i)+",\t$zero,\t"+getReg(convName(para)))
								addIns("\tadd\t$t"+str(i-1)+",\t$zero,\t"+"$a"+str(i))#'VAR_'+currentSymbolTable.tableName+"_"+para)
								if ("$t"+str(i-1)) in freeRegisters:
									freeRegisters.remove("$t"+str(i-1))
								registerDescriptor["$t"+str(i-1)] = 'VAR_'+currentSymbolTable.tableName+"_"+para# 'VAR_'+currentSymbolTable.tableName+"_"+para
								addressDescriptor['VAR_'+currentSymbolTable.tableName+"_"+para] = "$t"+str(i-1)
								busyRegisters.append("$t"+str(i-1))
							else:
								pass
							i=i+1
					else:
						paramtrs.reverse()
						for para in paramtrs:
							if(isVar(para)):
								addIns("\tlw\t"+"$t"+str(i-1)+",\t0($sp)")
								addIns("\taddi\t$sp,\t$sp,\t4")
								if ("$t"+str(i-1)) in freeRegisters:
									freeRegisters.remove("$t"+str(i-1))
								registerDescriptor["$t"+str(i-1)] = 'VAR_PARAMETER'+currentSymbolTable.tableName+"_"+para# 'VAR_'+currentSymbolTable.tableName+"_"+para
								addressDescriptor['VAR_PARAMETER'+currentSymbolTable.tableName+"_"+para] = "$t"+str(i-1)
								busyRegisters.append("$t"+str(i-1))
							else:
								pass
							i = i+1
					addIns("\taddi\t$sp,\t$sp,\t-4")
					addIns("\tsw\t$ra,\t0($sp)")
				
				pass
			elif(line[0] == 'ENDFUNCTION'):
				currentSymbolTable = symbolTableStack.pop()
				if(if_main==1):
					if_main=0
					addIns("\tli\t$v0,\t10")
					addIns("\tsyscall")
				else:
					addIns("\tlw\t$ra,\t0($sp)")
					addIns("\taddi\t$sp,\t$sp,\t4")
					addIns("\tjr\t$ra")
				if_begin = 0

			elif(line[0] == 'VARDECLARATION'):
				data_size2 = 0
				if(line[1]=='void'): 
					data_size2=0
				elif(line[1]=='char'): 
					data_size2=1
				elif(line[1]=='int'): 
					data_size2=4
					tmp = currentSymbolTable.lookup(line[2])
					if(tmp['scope'] != 'GLOBALTABLE'):
						data_section += ['\tVAR_'+tmp['scope']+"_"+line[2]+':\t.word\t0']
						declaredVars.append('VAR_'+tmp['scope']+"_"+line[2])
				elif(line[1]=='float'): 
					data_size2=4
				elif(line[1]=='double'): 
					data_size2s=8
				else:
					pass
				#data_section += ['\tVAR_'+line[2]+'\t.space\t'+str(data_size)]
				pass
			elif(line[0] == 'LABEL'):
				addIns(line[1]+':')
				pass
			elif(line[0] == 'GOTO'):
				addIns("\tb\t"+line[1])
				pass
			elif(line[0] == 'IF'):
				if(line[2] == "=="):
					register = line[1]
					register3 = line[3]
					if(isVar(line[1])):
						register = getReg(convName(line[1]))
					if(isVar(line[3])):
						register3 = getReg(convName(line[3]))
					addIns("\tbeq\t"+register+",\t"+register3+",\t"+line[5])
				elif (line[2] == "<"):
					register = line[1]
					register3 = line[3]
					if(isVar(line[1])):
						register = getReg(convName(line[1]))
					if(isVar(line[3])):
						register3 = getReg(convName(line[3]))
					addIns("\tblt\t"+register+",\t"+register3+",\t"+line[5])
				elif (line[2] == ">"):
					register = line[1]
					register3 = line[3]
					if(isVar(line[1])):
						register = getReg(convName(line[1]))
					if(isVar(line[3])):
						register3 = getReg(convName(line[3]))
					addIns("\tbgt\t"+register+",\t"+register3+",\t"+line[5])
				elif (line[2] == "<="):
					register = line[1]
					register3 = line[3]
					if(isVar(line[1])):
						register = getReg(convName(line[1]))
					if(isVar(line[3])):
						register3 = getReg(convName(line[3]))
					addIns("\tble\t"+register+",\t"+register3+",\t"+line[5])
				elif (line[2] == ">="):
					register = line[1]
					register3 = line[3]
					if(isVar(line[1])):
						register = getReg(convName(line[1]))
					if(isVar(line[3])):
						register3 = getReg(convName(line[3]))
					addIns("\tbge\t"+register+",\t"+register3+",\t"+line[5])
				else:
					pass
				pass
			elif(line[0] == 'PRINTINT'):
				addIns("\tli\t$v0,\t1")
				if(isVar(line[1])):
					register = getReg(convName(line[1]))
					addIns("\tmove\t$a0,\t"+register)
				else:
					addIns("\tli\t$a0,\t"+line[1])
				addIns("\tsyscall")
				pass
			elif(line[0] == '+'):
				register = getReg(convName(line[1]))
				#register = getReg(convName(tmp['scope']+"_"+line[1])
				register2 = line[2]
				register3 = line[3]
				if(isVar(line[2])):
					register2 = getReg(convName(line[2]))
				if(isVar(line[3])):
					register3 = getReg(convName(line[3]))
				addIns("\tadd\t"+register+",\t"+register2+",\t"+register3)
				pass
			elif(line[0] == '-'):
				register = getReg(convName(line[1]))
				register2 = line[2]
				register3 = line[3]
				if(isVar(line[2])):
					register2 = getReg(convName(line[2]))
				if(isVar(line[3])):
					register3 = getReg(convName(line[3]))
				addIns("\tsub\t"+register+",\t"+register2+",\t"+register3)
				pass
			elif(line[0] == '*'):
				register = getReg(convName(line[1]))
				register2 = line[2]
				register3 = line[3]
				if(isVar(line[2])):
					register2 = getReg(convName(line[2]))
				if(isVar(line[3])):
					register3 = getReg(convName(line[3]))
				addIns("\tmul\t"+register+",\t"+register2+",\t"+register3)
				pass
			elif(line[0] == '/'):
				register = getReg(convName(line[1]))
				register2 = line[2]
				register3 = line[3]
				if(isVar(line[2])):
					register2 = getReg(convName(line[2]))
				if(isVar(line[3])):
					register3 = getReg(convName(line[3]))
				addIns("\tdiv\t"+register+",\t"+register2+",\t"+register3)
				pass
			elif(line[0] == '='):
				register = getReg(convName(line[1]))
				if(isVar(line[2])):
					register2 = getReg(convName(line[2]))
					addIns("\tmove\t"+register+",\t"+register2)
				else:
					addIns("\tli\t"+register+",\t"+line[2])


				if(convName(line[1]).split("_")[1] == 'GLOBALTABLE'):
					of = currentSymbolTable.lookup(convName(line[1]).split("_")[-1])['offset']
					if len(freeRegisters):
						reg = freeRegisters.pop()
					addIns("\taddi\t"+reg+",\t$zero,\t"+str(of))
					addIns("\tsw\t"+register+",\tVAR_global"+"("+reg+")")
					freeRegisters.append(reg)
					freeRegisters.append(register)
				pass
			elif(line[0] == '++'):
				register = getReg(convName(line[1]))
				addIns("\tadd\t"+register+",\t"+register+",\t1")
				pass	
			elif(line[0] == '--'):
				register = getReg(convName(line[1]))
				addIns("\tsub\t"+register+",\t"+register+",\t1")
				pass
			else:
				pass


		operators = ["+","-","*","/","",">=","<=","==","=","++","--","&&","||","!",">","<"]
		if(line[0] in operators ):    #if current statement is an operator
			for element in line[2:]:    # for each label in right of the operator
				if(element in freed_labels.keys()):    # if the operator is to be freed list
					if(freed_labels[element] != ind):   # if element is used beyond this line
						continue                          
					else:         #if it needs to be freed
						if(isVar(element) and element[0]=="t"):           # if it is a label starting with t
							used_labels=addressDescriptor.keys()          # take the labels of addressdescriptor
							for x in used_labels:                         # for each such label
								y=x.split("_") 
								#print "\n\n\n",x,"\t\t\tdsff"                           # split the label var_fun_t_12
								label=y[-2]+"_"+y[-1]                     # add last two strings after split ,i.e, t_12
								
								if(label==element):                       # if the current label is t_12
									used_reg = addressDescriptor[x]       # get the mapped register
									freeRegisters.append(used_reg)        # add the register to the free registers list
									registerDescriptor[used_reg] = None   # set the mapping of the register to None
									waste = addressDescriptor.pop(x,None)  # pop it from the address descriptor
									#print "\n"
									#print freeRegisters
									#register gets freed here
									break                    # come out of the loop
		
		elif(line[0]=='IF'):
			element = line[1]
			if(isVar(element) and element[0]=="t"):           # if it is a label starting with t
				used_labels=addressDescriptor.keys()          # take the labels of addressdescriptor
				for x in used_labels:                         # for each such label
					y=x.split("_")                            # split the label var_fun_t_12
					label=y[-2]+"_"+y[-1]                     # add last two strings after split ,i.e, t_12
					if(label==element):                       # if the current label is t_12
						used_reg = addressDescriptor[x]       # get the mapped register
						freeRegisters.append(used_reg)        # add the register to the free registers list
						registerDescriptor[used_reg] = None   # set the mapping of the register to None
						waste = addressDescriptor.pop(x,None)  # pop it from the address descriptor
									#register gets freed here
						break
			element = line[3]
			if(isVar(element) and element[0]=="t"):           # if it is a label starting with t
				used_labels=addressDescriptor.keys()          # take the labels of addressdescriptor
				for x in used_labels:                         # for each such label
					y=x.split("_")                            # split the label var_fun_t_12
					label=y[-2]+"_"+y[-1]                     # add last two strings after split ,i.e, t_12
					if(label==element):                       # if the current label is t_12
						used_reg = addressDescriptor[x]       # get the mapped register
						freeRegisters.append(used_reg)        # add the register to the free registers list
						registerDescriptor[used_reg] = None   # set the mapping of the register to None
						waste = addressDescriptor.pop(x,None)  # pop it from the address descriptor
									#register gets freed here
						break
		ind = ind +1

	#print "\n----------- MIPS code -----------\n"
	f = open('code.asm', 'wb')
	#print ".data"
	data_section += ['\tnewLine:\t.asciiz\t"\\n"']
	f.write(".data\n")
	for line in data_section:
		#print line
		f.write("%s\n" % line)
	#print ".text"
	f.write(".text\n")
	for line in text_section:
		#print line
		if(line == "main:"):
			f.write("%s\n" % line)
			for line2 in global_text:
				f.write("%s\n" % line2)
		else:
			f.write("%s\n" % line)
	f.close()
	#dump_str = ""
	#f = open('dump.txt', 'wb')
	#f.write("%s" % dump_str)
	#f.close()
	pass


if __name__ == "__main__":
	pass

def calcfn(g1,tk,parentToken,sp):
	#global tokenVal
	#global dump_str
	#if(type(tk) is list):
#		calc_tree(g1,tk[0],parentToken,sp)
#	else:
#		dump_str=dump_str+"\n"+(sp)*"	"+tk.name
#		#print (sp)*"	",tk.name
#		if(not ( mp.has_key(str(tk)) ) ):
#			g1.node(str(tokenVal),str(tk.name))
#			ct = tokenVal
#			tokenVal = tokenVal + 1
#			mp[str(tk)] = ct
#			if(parentToken >= 0):
##				g1.edge(str(parentToken),str(ct))
#			parentToken = ct
#			childNumber = len(tk.astChildList)
#			if childNumber > 0:
#				for j in range(0,childNumber):
#					calc_tree(g1,tk.astChildList[j],parentToken,sp+1)
#		else:
##			ct = mp[str(tk)]
##			if(parentToken >= 0):
#				g1.edge(str(parentToken),str(ct))
	pass
