class Tree(object):
    
    def __init__(self, left,right,label):
        self.left = left
        self.right = right
        self.label = label
        
    
    
    
def V1(self, Arb):
    if Arb.right == None:
        return I(Arb.label)
    elif(Arb.label == "~"):
        if(V1.right)=='V':
            return False
        else:
            return True
    elif(Arb.label=="&"):
        if(V1(Arb.left)== True and V1(Arb.right)==True):
            return True
        else:
            return False
    elif(Arb.label=="V"):
        if(V1(Arb.left)==True or V1(Arb.right)==True):
            return True
        else:
            return False
    elif(Arb.label =="->"):
        if(V1(Arb.left)==False or V1(Arb.right)==True):
            return True
        else:
            return False
    elif(Arb.label=="<->"):
        if(V1(Arb.left)==V1(Arb.right)):
            return True
        else:
            return False
        
        
        
        
# Define la funcion de imprimir rotulos Inorder(f)
def Inorder(f):
    # Determina si F es una hoja
    if f.right == None:
#        print "Es una hoja!"
        print f.label,
    elif f.label == '-':
        print f.label,
        Inorder(f.right)
    else:
        print "(",
        Inorder(f.left)
        print f.label,
        Inorder(f.right)
        print ")",

# Solicitamos una cadena
f = raw_input('Ingrese una cadena: ') or 'rqpO>' # Cadena por defecto

print "Cadena ingresada " + f

cadena = list(f)

print cadena

letrasProposicionales = ['p', 'q', 'r', 's', 't', 'v']
conectivos = ['O', 'Y', '>']

pila = [] # inicializamos la pila

for c in cadena:
    if c in letrasProposicionales:
        pila.append(Tree(c, None, None))
    elif c == '-':
        aux = Tree(c, None, pila[-1])
        del pila[-1]
        pila.append(aux)
    elif c in conectivos:
        aux = Tree(c, pila[-1], pila[-2])
        del pila[-1]
        del pila[-1]
        pila.append(aux)

formula = pila[-1]

print "La formula ",
Inorder(formula)
print " fue creada como un objeto!"
         
         
         
A1 = Tree(None.None,'p')
A2 = Tree(None,None,'q')
A3 = Tree(None,A1,'~') #~p
A4 = Tree(None,A2,'~') #~q

A5 = Tree(A1,A2,'V') # p V q
A6 = Tree(A3,A4,'&') # ~p & ~q


A7 = Tree(A1,A2,'&') # p & q
A8 = Tree(A3,A4,'V') # ~p V ~q
A9 = Tree(None,A8,'~') # ~(~p V ~q)
A10 = Tree()
        
            