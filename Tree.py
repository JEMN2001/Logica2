negacion = "~"
conectoresB = ["Y", "O", "->", "<->"]
#Class
class Tree(object):
	def __init__(self, Label, Left, Right):
		self.Label = Label
		self.Left = Left
		self.Right = Right
	def getLabel(self):
		return self.Label
	def getRight(self):
		return self.Right
	def getLeft(self):
		return self.Left
	def toString(self):
		if (self.Right != None and self.Left != None):
			return self.Left.toString()+self.Label+self.Right.toString()
		elif (self.Right != None and self.Left == None):
			return self.Label+self.Right.toString()
		elif (self.Right == None and self.Left == None):
			return self.Label
#set of Atoms
def Atoms(arb):
	if (arb.Label == negacion):
		return Atoms(arb.Right)
	elif (arb.Label in conectoresB):
		return Atoms(arb.Left)|Atoms(arb.Right)
	else:
		return {arb.Label}
#Interpretations
letrasProposicionales = ["p", "q", "r"]
interps = []
aux = {}
for a in letrasProposicionales:
	aux[a] = 1
interps.append(aux)
for a in letrasProposicionales:
	interps_aux = [i for i in interps] 
	for i in interps_aux:
		aux1 = {} 
		for b in letrasProposicionales:
			if a == b:
				aux1[b] = 1 - i[b]
			else:
				aux1[b] = i[b]
		interps.append(aux1)
print interps[0]["p"]
#Vi
def V1(Arb, num):
    if Arb.Right == None:
        return interps[num][Arb.Label]
    elif(Arb.Label == "~"):
        if(Arb.Right)=='v':
            return False
        else:
            return True
    elif(Arb.Label=="&"):
        if(V1(Arb.Left, num)== True and V1(Arb.Right, num)==True):
            return True
        else:
            return False
    elif(Arb.Label=="v"):
        if(V1(Arb.Left, num)==True or V1(Arb.Right, num)==True):
            return True
        else:
            return False
    elif(Arb.Label =="->"):
        if(V1(Arb.Left, num)==False or V1(Arb.Right, num)==True):
            return True
        else:
            return False
    elif(Arb.Label=="<->"):
        if(V1(Arb.Left, num)==V1(Arb.Right, num)):
            return True
        else:
	    return False
#function that define equivalence
def Equivalence(A1, A2):
	for i in range(7):
		if (V1(A1, i) != V1(A2, i)):
			return False
	return True
#Trees
P = Tree("p", None, None)
R = Tree("r", None, None)
Q = Tree("q", None, None)
A1 = Tree("&", Tree("p", None, None), Tree("v", Tree("q", None, None), Tree("r", None, None)))
A2 = Tree("v", Tree("&", P, Q), Tree("&", P, R))
D1 = Tree("->", P, Q)
D2 = Tree("v", Tree("~", None, P), Q)
C1 = Tree("&", P, Q)
C2 = Tree("~", None, Tree("v", Tree("~", None, P), Tree("~", None, Q)))
arb = Tree("&", Q, R)
print Equivalence(A1, A2)
print Equivalence(C1, C2)
print Equivalence(D1, D2)


