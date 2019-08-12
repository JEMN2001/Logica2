negacion = "~"
conectoresB = ["Y", "O", "->", "<->"]
letrasProposicionales = ["p", "q", "r"]
letrasProposicionales2 = ["p", "q", "r", "s", "t"]
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
def Interpretation(lista):
	interps = []
	aux = {}
	for a in lista:
		aux[a] = 1
	interps.append(aux)
	for a in lista:
		interps_aux = [i for i in interps] 
		for i in interps_aux:
			aux1 = {} 
			for b in lista:
				if a == b:
					aux1[b] = 1 - i[b]
				else:
					aux1[b] = i[b]
			interps.append(aux1)
	return interps
inter = Interpretation(letrasProposicionales)
inter2 = Interpretation(letrasProposicionales2)
#Vi
def V1(Arb, num, interp):
    if Arb.Right == None:
	if interp[num][Arb.Label] == 1:
		return True
        elif interp[num][Arb.Label] == 0:
		return False
	else:
		return None
    elif Arb.Label == "~":
        return not V1(Arb.Right, num, interp)
    elif Arb.Label == "&":
        return V1(Arb.Right, num, interp) and V1(Arb.Left, num, interp)
    elif Arb.Label == "v":
        return (V1(Arb.Right, num, interp) or V1(Arb.Left, num, interp))
    elif Arb.Label == "->" :
        if V1(Arb.Left, num, interp) == False:
		return True
	elif V1(Arb.Right, num, interp) and V1(Arb.Left, num, interp):
		return True
	else:
		return False
    elif(Arb.Label == "<->"):
        if V1(Arb.Right, num, interp) == V1(Arb.Left, num, interp):
		return True
	return False
#function that define equivalence
def Equivalence(A1, A2, interp, leters):
	rango = (2**len(leters)) -1
	for i in range(rango):
		if (V1(A1, i, interp) != V1(A2, i, interp)):
			return False
	return True
#Trees
P = Tree("p", None, None)
R = Tree("r", None, None)
Q = Tree("q", None, None)
NoP = Tree("~", None, P)
NoQ = Tree("~", None, Q)
noR = Tree("~", None, R)
A1 = Tree("&", P, Tree("v", Q, R))
A2 = Tree("v", Tree("&", P, Q), Tree("&", P, R))
D1 = Tree("->", P, Q)
D2 = Tree("v", NoP, Q)
C1 = Tree("&", P, Q)
C2 = Tree("~", None, Tree("v", NoP, NoQ))
B1 = Tree("v", P, Q)
B2 = Tree("~", None, Tree("&", NoP, NoQ))
print Equivalence(A1, A2, inter, letrasProposicionales)
print Equivalence(B1, B2, inter, letrasProposicionales)
print Equivalence(C1, C2, inter, letrasProposicionales)
print Equivalence(D1, D2, inter, letrasProposicionales)
print "--------------------------------------------------"
#Main Tree
S = Tree("s", None, None)
T = Tree("t", None, None)
main = Tree("&", Tree("~", None, Tree("->", Tree("->", P, Q), Tree("v", R, S))), T)
for i in range((2**len(letrasProposicionales2))-1):
	print inter2[i],
	print ": ",
	print V1(main, i, inter2)
