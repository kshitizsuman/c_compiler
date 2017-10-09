import graphviz as gv

tokenVal = 1

def calc_tree(g1,tk,parentToken):
	global tokenVal
	if type(tk) is not tuple:
		g1.node(str(tokenVal),str(tk))
		g1.edge(str(parentToken),str(tokenVal))
		tokenVal = tokenVal + 1
	else:
		childNumber = len(tk)
		if childNumber > 1:
			for j in range(1,childNumber):
				childToken = tokenVal
				tokenVal = tokenVal + 1
				if type(tk[j]) is tuple:
					calc_tree(g1,tk[j],childToken)
					g1.node(str(childToken),str(tk[j][0]))
					g1.edge(str(parentToken),str(childToken))
				else:
					g1.node(str(childToken),str(tk[j]))
					g1.edge(str(parentToken),str(childToken))
		
	pass

def create_tree(result,name):
	g1 = gv.Graph(format='svg')
	g1.node(str(0),str(result[0]))
	calc_tree(g1,result,0)
	filename = g1.render(filename=name+'tree')
	#print filename
	#print(g1.source)
	#print(result)
	pass


if __name__ == "__main__":
	#result = ('/', ('+', ('NUM', 24), ('NUM', 4)), ('NUM', ))
	create_tree(result)