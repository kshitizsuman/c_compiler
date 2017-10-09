import graphviz as gv

mp = {}
dump_str=""
tokenVal = 0

def calc_tree(g1,tk,parentToken,sp):
	global tokenVal
	global dump_str
	if(type(tk) is list):
		calc_tree(g1,tk[0],parentToken,sp)
	else:
		dump_str=dump_str+"\n"+(sp)*"	"+tk.name
		#print (sp)*"	",tk.name
		if(not ( mp.has_key(str(tk)) ) ):
			g1.node(str(tokenVal),str(tk.name))
			ct = tokenVal
			tokenVal = tokenVal + 1
			mp[str(tk)] = ct
			if(parentToken >= 0):
				g1.edge(str(parentToken),str(ct))
			parentToken = ct
			childNumber = len(tk.astChildList)
			if childNumber > 0:
				for j in range(0,childNumber):
					calc_tree(g1,tk.astChildList[j],parentToken,sp+1)
		else:
			ct = mp[str(tk)]
			if(parentToken >= 0):
				g1.edge(str(parentToken),str(ct))
	

	pass


def calc_tree2(g1,tk,parentToken):
	global tokenVal
	#print parentToken
	g1.node(str(tokenVal),str(tk.name))
	if(parentToken >= 0):
		g1.edge(str(parentToken),str(tokenVal))
	tokenVal = tokenVal + 1
	parentToken = tokenVal - 1
	print tk.name,tk
	childNumber = len(tk.astChildList)
	if childNumber > 0:
		for j in range(0,childNumber):
			calc_tree2(g1,tk.astChildList[j],parentToken)

	pass

def create_tree(result,name):
	g1 = gv.Graph(format='svg')
	#g1.node(str(0),str(result.name))
	calc_tree(g1,result,-1,0)
	filename = g1.render(filename=name+'tree')
	#print filename
	#print(g1.source)
	#print(result)
	#print result.astChildList
	print dump_str
	f = open('dump.txt', 'wb')
	f.write("%s" % dump_str)
	f.close()
	pass


if __name__ == "__main__":
	#result = ('/', ('+', ('NUM', 24), ('NUM', 4)), ('NUM', ))
	create_tree(result)