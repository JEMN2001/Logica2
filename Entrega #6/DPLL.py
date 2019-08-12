#-*-coding: utf-8-*-

import copy

class Tree(object):
	def __init__(self, r, iz, der):
		self.left = iz
		self.right = der
		self.label = r

def Inorder(f):
    # Imprime una formula como cadena dada una formula como arbol
    # Input: tree, que es una formula de logica proposicional
    # Output: string de la formula

    if f.right == None:
        return f.label
    elif f.label == '~':
        return f.label + Inorder(f.right)
    else:
        return "(" + Inorder(f.left) + f.label + Inorder(f.right) + ")"

def StringtoTree(A, letrasProposicionales):
    # Crea una formula como tree dada una formula como cadena escrita en notacion polaca inversa
    # Input: A, lista de caracteres con una formula escrita en notacion polaca inversa
             # letrasProposicionales, lista de letras proposicionales
    # Output: formula como tree
    delimeter = ','
    conectivos = ['~', 'v', '&', '>']
    pila = []
    letra = ""
    for c in A:
        if c not in conectivos and c != delimeter:
            letra += c
        elif c == delimeter:
            if letra in letrasProposicionales:
                pila.append(Tree(letra, None, None))
            letra = ""
        else :
            if c == '~':
                formulaAux = Tree(c, None, pila[-1])
                del pila[-1]
                pila.append(formulaAux)
            elif c in conectivos and c != '~':
                formulaAux = Tree(c, pila[-1], pila[-2])
                del pila[-1]
                del pila[-1]
                pila.append(formulaAux)
    return pila[-1]

def quitarDobleNegacion(f):
    # Elimina las dobles negaciones en una formula como arbol
    # Input: tree, que es una formula de logica proposicional
    # Output: tree sin dobles negaciones

    if f.right == None:
        return f
    elif f.label == '~':
        if f.right.label == '~':
            return quitarDobleNegacion(f.right.right)
        else:
            return Tree('~', \
                        None, \
                        quitarDobleNegacion(f.right)\
                        )
    else:
        return Tree(f.label, \
                    quitarDobleNegacion(f.left), \
                    quitarDobleNegacion(f.right)\
                    )

def reemplazarImplicacion(f):
    # Regresa la formula reemplazando p>q por -pOq
    # Input: tree, que es una formula de logica proposicional
    # Output: tree

    if f.right == None:
        return f
    elif f.label == '~':
        return Tree('~', None, reemplazarImplicacion(f.right))
    elif f.label == '>':
        noP = Tree('~', None, reemplazarImplicacion(f.left))
        Q = reemplazarImplicacion(f.right)
        return Tree('v', noP, Q)
    else:
        return Tree(f.label, reemplazarImplicacion(f.left), reemplazarImplicacion(f.right))

def deMorgan(f):
    # Regresa la formula aplicando deMorgan -(pYq) por -pO-q
    # Input: tree, que es una formula de logica proposicional
    # Output: tree

    if f.right == None:
        return f
    elif f.label == '~':
        if f.right.label == '&':
            print "La formula coincide negacion Y"
            return Tree('v', \
                        Tree('~', None, deMorgan(f.right.left)),\
                        Tree('~', None, deMorgan(f.right.right))\
                        )
        elif f.right.label == 'v':
            print "La formula coincide negacion O"
            return Tree('&', \
                        Tree('~', None, deMorgan(f.right.left)),\
                        Tree('~', None, deMorgan(f.right.right))\
                        )
        else:
            return Tree('~', \
                        None, \
                        deMorgan(f.right) \
                        )
    else:
        return Tree(f.label, \
                    deMorgan(f.left),\
                    deMorgan(f.right)\
                    )

def distributiva(f):
    # Distribuye O sobre Ys: convierte rO(pYq) en (rOp)Y(rOq)
    # Input: tree, que es una formula de logica proposicional
    # Output: tree

    if f.right == None:
        print("Llegamos a una rama")
        return f
    elif f.label == 'v':
        print("Encontramos O...")
        if f.left.label == '&':
            print("... encontramos Y a la izquierda")
            P = f.left.left
            Q = f.left.right
            R = f.right
            return Tree('&', \
                        Tree('v', P, R), \
                        Tree('v', Q, R)
                        )
        if f.right.label == '&':
            print("... encontramos Y a la derecha")
            R = f.left
            P = f.right.left
            Q = f.right.right
            return Tree('&', \
                        Tree('v', R, P), \
                        Tree('v', R, Q)
                        )
        else:
            print("... pero no hay Y")
            print("Pasamos a hijos de O")
            return Tree(f.label, \
                        distributiva(f.left), \
                        distributiva(f.right)
                        )
    elif f.label == '~':
        print("Pasamos a hijo de negacion")
        return Tree('~', \
                    None, \
                    distributiva(f.right)
                    )
    else:
        print("Pasamos a hijos de ", f.label)
        return Tree(f.label, \
                    distributiva(f.left), \
                    distributiva(f.right)
                    )

def aplicaDistributiva(f):
    # Devuelve True si la distributiva de f es distinta a f
    # Input: tree, que es una formula de logica proposicional
    # Output: - True/False,
    #         - tree
    aux1 = Inorder(f)
    print "Se analiza: ", aux1
    B = distributiva(f)
    aux2 = Inorder(B)
    print "Se obtuvo : ", aux2
    if  aux1 != aux2:
        print "Hubo distribucion"
        return True, B
    else:
        print "No hubo distribucion"
        return False, f

def eliminaConjunciones(f):
    # Devuelve una lista de disyunciones de literales
    # Input: tree, que es una formula en CNF
    # Output: lista de cadenas
    if f.right == None:
        a = [Inorder(f)]
        print "Clausula unitaria positiva, ", a
        return a
    elif f.label == 'v':
        return [Inorder(f)]
    elif f.label == '&':
        print "Dividiendo los lados de la conjuncion"
        a = eliminaConjunciones(f.left)
        print("a, ", a)
        b = eliminaConjunciones(f.right)
        print("b, ", b)
        c = a + b
        print("c, ", c)
        return a + b
    else:
        if f.label == '~':
            if f.right.right == None:
                print "Clausula unitaria negativa"
                return [Inorder(f)]
            else:
                print "Oh, Oh, la formula no estaba en CNF!"

def complemento(l):
    # Devuelve el complemento de un literal
    # Input: l, que es una cadena con un literal (ej: p, -p)
    # Output: l complemento
    if '~' in l:
        return l[1:]
    else:
        return '~' + l

def formaClausal(f):
    # Obtiene la forma clausal de una formula en CNF
    # Input: tree, que es una formula de logica proposicional en CNF
    # Output: lista de clausulas

    # Primero elimino las conjunciones, obteniendo
    # una lista de disyunciones de literales
    #print "Encontrando lista de disyunciones de literales..."
    aux = eliminaConjunciones(f)
    badChars = ['(', ')']
    conjuntoClausulas = []
    for C in aux:
        C = ''.join([x for x in C if x not in badChars])
        C = C.split('v')
        conjuntoClausulas.append(C)

    aux = []
    print "Eliminando clausulas triviales..."
    for C in conjuntoClausulas:
        trivial = False
        for x in C:
            xComplemento = complemento(x)
            if xComplemento in C:
                print "Clausula trivial encontrada"
                trivial = True
                break
        if not trivial:
            aux.append(C)

    print "Eliminando repeticiones..."
    # Eliminamos repeticiones dentro de cada clausula
    aux = [list(set(i)) for i in aux]
    # Eliminamos clausulas repetidas
    aux_set = set(tuple(x) for x in aux)
    aux = [list(x) for x in aux_set]

    conjuntoClausulas = aux

    return conjuntoClausulas

def unitPropagate(f, letrasProposicionales, interpretaciones):
    # Realiza la rutina unit propagat
    # Input: f, conjunto de clausulas
    #        letrasProposicionales, lista con las letras proposicionales
    #        interpretaciones, lista con las interpretaciones hasta el momento
    # Output: conjunto de clausulas sin la clausula unitarias
    #         interpretacion para el literal unitario  
    OK = True
    while (OK): 
        OK = False
        for i in f:
            if len(i) == 1:
                literal = i[0]
                if not '~' in literal and literal in letrasProposicionales:
                    interpretaciones[literal] = True
                elif '~' in literal and literal[1:] in letrasProposicionales:
                    interpretaciones[literal[1:]] = False
                f.pop(f.index(i))
                for j in f:
                    if literal in j:
                        f.pop(f.index(j))
                    elif complemento(literal) in j:
                        j.pop(j.index(complemento(literal)))
                OK = True
    return f, interpretaciones

def DPLL(S,letrasProposicionales,I):
    SE = copy.deepcopy(S)
    S,I = unitPropagate(S,letrasProposicionales,I)
    if([] in S):
        return False,I
    elif(len(S)==0):
        return True,I
    else:
        x = S[0][0]
        nx = complemento(x)
        Sp = []
        Ip = I
        for i in SE:
            if(x not in i):
                if(nx in i):
                    temp = copy.deepcopy(i)
                    temp.pop(temp.index(nx))
                    Sp.append(temp)
                else:
                    Sp.append(i)
        if('~' in x):
            Ip[x[1]] = False
        else:
            Ip[x] = True
        r1,i1 = DPLL(Sp,letrasProposicionales,Ip)
        if(r1==True):
            return True,Ip
        else:
            Spp = []
            Ipp = I
            for i in S:
                if(nx not in i):
                    if(x in i):
                        temp = copy.deepcopy(i)
                        temp.pop(temp.index(x))
                        Spp.append(temp)
                    else:
                        Spp.append(i)
            if('~' in x):
                Ipp[x[1]] = True
            else:
                Ipp[x] = False
            return DPLL(Spp,letrasProposicionales,Ipp)
		

#############################################################################

#letrasProposicionales = ['p', 'q', 'r']

#cadena = 'q,--p,->--'
#cadena = 'q,p,Y-'
#cadena = 'r,q,-p,O->'
#cadena = 'q,p,Yp,r,YO'
#cadena = 'q,p,Yp,r,>O'
#cadena = 'p,r,>q,p,YO'
#cadena = 'q,--q,p,Yp,r,YO->--'
#cadena = 'q,-p,Yq,p,-YO'
#cadena = 'r,-q,-Yp,Y'
#cadena = 'r,-q,Yp,-Y'
#cadena ='r,q,-Yp,-Y'
#cadena = 'p,-q,-Y'
#cadena = 'q,-p,-r,p,q,-OOYO'
letrasProposicionales = []
for i in range(1, 31):
	letrasProposicionales.append(str(i))

#Regla 1, Solo hay 2 bombas
"""formula = ""
disyuncion = ""
letrasauxiliar = []
times = True
for i in range(1, 11):
	letrasauxiliar.append(str(i))
for p in letrasauxiliar:
	aux = [x for x in letrasauxiliar if x != p] # Todas las letras excepto
	for q in aux:
			literal = q+','+p+',' + '&'
			aux2 = [x+','+'~' for x in aux if x != q]
			for k in aux2:
 				literal = k + literal + '&'
			if times:
 				disyuncion = literal
				times = False
			else:
				disyuncion = literal + disyuncion + 'v'
formula = disyuncion
#Regla 2: regla para los unos
formula += "11,2,1,~&>"+'&'
for i in range(2, 10):
		conjuncion1 = str(i-1)+','+str(i+1)+','+'&'
		conjuncion2 = str(i-1)+','+'~'+str(i+1)+','+'~'+'&'
		disyuncion = conjuncion1+conjuncion2+'v'+str(i)+","+'v';
		implica = disyuncion+str(10+i)+','+'~'+'>'
		formula += implica+'&'
formula += "20,9,10,~&>"+'&'
#Regla 3: regla para los 2:
formula += "21,"+'~'+'&'
for i in range(2, 10):
	conjuncion = str(i-1)+','+str(i+1)+','+'&'+str(i)+","+'~'+'&'
	implica = str(20+i)+','+conjuncion+'>'
	formula += implica+'&'
formula += "30,"+'~'+'&'"""

formula = "1,~2,~v1,2,v&1,~2,v&"

A = StringtoTree(formula, letrasProposicionales)

print "Trabajando con la formula:\n ", Inorder(A)

A = quitarDobleNegacion(A)

#print "La formula sin dobles negaciones es:\n ", Inorder(A)

A = reemplazarImplicacion(A)

#print "La formula reemplazando implicaciones es:\n ", Inorder(A)

A = quitarDobleNegacion(A)

#print "La formula sin dobles negaciones es:\n ", Inorder(A)

OK = True
while OK:
    aux1 = Inorder(A)
    #print "Se analiza: ", aux1
    B = deMorgan(A)
    B = quitarDobleNegacion(B)
    aux2 = Inorder(B)
    #print "Se obtuvo : ", aux2
    if  aux1 != aux2:
        #print "Se aplicó deMorgan"
        OK = True
        A = B
    else:
        #print "No se aplicó deMorgan"
        OK = False

OK = True
while OK:
    OK, A = aplicaDistributiva(A)

conjuntoClausulas = formaClausal(A)


print "Conjunto de disyunciones de literales:\n ", conjuntoClausulas
#conjuntoClausulas, interps = unitPropagate(conjuntoClausulas, letrasProposicionales, {})
#print conjuntoClausulas
#print interps

#p1 = [['p','-q','r'],['-p','-q','-r'],['-p','-q','r'],['p','-q','-r']]
#p2 = [['p','q'],['-p','q'],['-q','-r'],['r','-q']]
#p3 = [['p','-q'],['-p','-q'],['q','r'],['-q','-r'],['-p','-r'],['p','-r']]
#p4 = [['p','q'],['p','-q'],['-p','q'],['-p','-r']]

resp,I = DPLL(conjuntoClausulas,letrasProposicionales,{})
print "========================>",resp
print I
