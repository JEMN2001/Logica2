#-*-coding: utf-8-*-
negacion = '~'
Y = '&'
O = 'v'
implicacion = '>'

from random import choice

class Tree(object):
	def __init__(self, label, left, right):
		self.left = left
		self.right = right
		self.label = label
	def __eq__(self, B):
		if B != None:
			return (self.label == B.label and self.left == B.left and self.right == B.right)

def Inorder(f):
    # Imprime una formula como cadena dada una formula como arbol
    # Input: tree, que es una formula de logica proposicional
    # Output: string de la formula

	if f.right == None:
		return f.label
	elif f.label == negacion:
		return f.label + Inorder(f.right)
	else:
		return "(" + Inorder(f.left) + f.label + Inorder(f.right) + ")"

def StringtoTree(A, letrasProposicionales):
    # Crea una formula como tree dada una formula como cadena escrita en notacion polaca inversa
    # Input: A, lista de caracteres con una formula escrita en notacion polaca inversa
             # letrasProposicionales, lista de letras proposicionales
    # Output: formula como tree
	delimeter = ','
	conectivos = [negacion, O, Y, implicacion]
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
			if c == negacion:
				formulaAux = Tree(c, None, pila[-1])
				del pila[-1]
				pila.append(formulaAux)
			elif c in conectivos and c != negacion:
				formulaAux = Tree(c, pila[-1], pila[-2])
				del pila[-1]
				del pila[-1]
 				pila.append(formulaAux)
	return pila[-1]

def imprime_tableau(tableau):
	cadena = '['
	for l in tableau:
		cadena += "{"
		primero = True
		for f in l:
			if primero == True:
				primero = False
			else:
				cadena += ", "
			cadena += Inorder(f)
		cadena += "}"
	return cadena + "]"

def imprime_hoja(H):
	cadena = "{"
	primero = True
	for f in H:
		if primero == True:
			primero = False
		else:
			cadena += ", "
		cadena += Inorder(f)
	return cadena + "}"


def Tableaux(lista_hojas, letrasProposicionales):

	# Algoritmo de creacion de tableau a partir de lista_hojas

	# Imput: - lista_hojas: lista de lista de formulas
	#			(una hoja es una lista de formulas)
	#		 - letrasProposicionales: lista de letras proposicionales del lenguaje

	# Output: - String: Satisfacible/Insatisfacible
	# 		  - interpretaciones: lista de listas de literales que hacen verdadera
	#			la lista_hojas

	print "Trabajando con: ", imprime_tableau(lista_hojas)

	interpretaciones = [] # Lista para guardar interpretaciones que satisfacen la raiz

	while len(lista_hojas) > 0: # Verifica si hay hojas no marcadas

		# Hay hojas sin marcar
		# Crea la lista de hojas sin marcar
		booleano = True
		cantidad = len(lista_hojas)
		print u"Cantidad de hojas sin marcar: ", cantidad
		# Selecciona una hoja no marcada
		hoja = choice(lista_hojas)
		#if (len(hojas_no_marcadas)%1000 == 0):
		#print "Trabajando con hoja: ", imprime_hoja(hoja)

		# Busca formulas que no son literales
		formulas_no_literales = []
		for x in hoja:
			if x.label not in letrasProposicionales:
				if x.label != negacion:
					# print Inorder(x) + " no es un literal"
					formulas_no_literales.append(x)
					break
				elif x.right.label not in letrasProposicionales:
					# print Inorder(x) + " no es un literal"
					formulas_no_literales.append(x)
					break

		# print "Formulas que no son literales: ", imprime_hoja(formulas_no_literales)

		if formulas_no_literales != []: # Verifica si hay formulas que no son literales
			# Hay formulas que no son literales
			print "Hay formulas que no son literales"
			# Selecciona una formula no literal
			f = choice(formulas_no_literales)
			if f.label == Y:
				# print u"Fórmula 2alfa" # Identifica la formula como A1 y A2
				hoja.remove(f) # Quita a f de la hoja
				A1 = f.left
				if  A1 not in hoja:
					hoja.append(A1) # Agrega A1
					if Tree(negacion, None, A1) in hoja:
						lista_hojas.remove(hoja)
						booleano = False
						print "Se elimino la hoja ", imprime_hoja(hoja), " porque ", Inorder(A1), " esta en sus 2 formas"
				A2 = f.right
				if  A2 not in hoja:
					hoja.append(A2) # Agrega A2
					if Tree(negacion, None, A1) in hoja and booleano:
						lista_hojas.remove(hoja)
						print "Se elimino la hoja ", imprime_hoja(hoja), " porque ", Inorder(A2), " esta en sus 2 formas"
			elif f.label == O:
				#print u"Fórmula 2beta" # Identifica la formula como B1 o B2
				hoja.remove(f) # Quita la formula de la hoja
				lista_hojas.remove(hoja) # Quita la hoja de la lista de hojas
				S1 = [x for x in hoja]
				S2 = [x for x in hoja]
				B1 = f.left
				if  B1 not in hoja:
					S1.append(B1) # Crea nueva hoja con B1
					if Tree(negacion, None, B1) in S1:
						booleano = False
				if S1 not in lista_hojas and booleano:
					lista_hojas.append(S1) # Agrega nueva hoja con B1
				elif not booleano:
					booleano = True
					print "No se agrego la hoja ", imprime_hoja(S1), " porque ", Inorder(B1), " estaba en sus 2 formas"
				B2 = f.right
				if B2 not in hoja:
					S2.append(B2) # Crea nueva hoja con B2
					if Tree(negacion, None, B2) in S2:
						booleano = False
				if S2 not in lista_hojas and booleano:
					lista_hojas.append(S2) # Agrega nueva hoja con B2
				elif not booleano:
					print "No se agrego la hoja ", imprime_hoja(S2), " porque ", Inorder(B2), " estaba en sus 2 formas"
			elif f.label == implicacion:
				#print u"Fórmula 3beta" # Identifica la formula como B1 > B2
				hoja.remove(f) # Quita la formula de la hoja
				lista_hojas.remove(hoja) # Quita la hoja de la lista de hojas
				S1 = [x for x in hoja]
				S2 = [x for x in hoja]
				noB1 = Tree(negacion, None, f.left)
				if  noB1 not in hoja:
					S1.append(noB1) # Crea nueva hoja con no B1
					if f.left in S1:
						booleano = False
				if S1 not in lista_hojas and booleano:
					lista_hojas.append(S1) # Agrega nueva hoja con no B1
				elif not booleano:
					booleano = True
					print "No se agrego la hoja ", imprime_hoja(S1), " porque ", Inorder(f.left), " estaba en sus 2 formas"
				B2 = f.right
				if B2 not in hoja:
					S2.append(B2)
					if Tree(negacion, None, B2) in S2:
						booleano = False
				if S2 not in lista_hojas and booleano:
					lista_hojas.append(S2) # Agrega nueva hoja con B2
				elif not booleano:
					print "No se agrego la hoja ", imprime_hoja(S2), " porque ", Inorder(B2), " estaba en sus 2 formas"
			elif f.label == negacion:
				if f.right.label == negacion:
					# print u"Fórmula 1alfa" # Identifica la formula como no no A1
					hoja.remove(f) # Quita a f de la hoja
					A1 = f.right.right
					if A1 not in hoja:
						hoja.append(A1) # Agrega la formula sin doble negacion
						if Tree(negacion, None, A1) in hoja:
							lista_hojas.remove(hoja)
							print "Se elimino la hoja ", imprime_hoja(hoja), " porque ", Inorder(A1), " esta en sus 2 formas"
				elif f.right.label == O:
					# print u"Fórmula 3alfa" # Identifica la formula como no(A1 o A2)
					hoja.remove(f) # Quita a f de la hoja
					noA1 = Tree(negacion, None, f.right.left)
					if noA1 not in hoja:
						hoja.append(noA1) # Agrega no A1
						if f.right.left in hoja:
							lista_hojas.remove(hoja)
							booleano = False
							print "Se elimino la hoja ", imprime_hoja(hoja), " porque ", Inorder(f.right.left), " esta en sus 2 formas"
					noA2 = Tree(negacion, None, f.right.right)
					if noA2 not in hoja:
						hoja.append(noA2) # Agrega no A2
						if f.right.right in hoja and booleano:
							lista_hojas.remove(hoja)
							print "Se elimino la hoja ", imprime_hoja(hoja), " porque ", Inorder(f.right.right), "esta en sus 2 formas"
				elif f.right.label == implicacion:
					# print u"Fórmula 4alfa" # Identifica la formula como no(A1 > A2)
					hoja.remove(f) # Quita a f de la hoja
					A1 = f.right.left
					if A1 not in hoja:
						hoja.append(A1) # Agrega A1
						if Tree(negacion, None, A1) in hoja:
							lista_hojas.remove(hoja)
							booleano
							print "Se elimino la hoja ", imprime_hoja(hoja), " porque ", Inorder(A1), " esta en sus 2 formas"
					noA2 = Tree(negacion, None, f.right.right)
					if noA2 not in hoja:
						hoja.append(noA2) # Agrega no A2
						if f.right.right in hoja and booleano:
							lista_hojas.remove(hoja)
							print "Se elimino la hoja ", imprime_hoja(hoja), " porque habia una formula y su negacion"
				elif f.right.label == Y:
					# print u"Fórmula 1beta" # Identifica la formula como no(B1 y B2)
					hoja.remove(f) # Quita la formula de la hoja
					lista_hojas.remove(hoja) # Quita la hoja de la lista de hojas
					S1 = [x for x in hoja]
					S2 = [x for x in hoja]
					noB1 = Tree(negacion, None, f.right.left)
					if  noB1 not in hoja:
						S1.append(noB1) # Crea nueva hoja con no B1
						if f.right.left in S1:
							booleano = False
					if S1 not in lista_hojas and booleano:
						lista_hojas.append(S1) # Agrega nueva hoja con no B2
					elif not booleano:
						print "No se agrego la hoja ", imprime_hoja(S1), " porque ", Inorder(f.right.left), " estaba en sus 2 formas"
						booleano = True
					noB2 = Tree(negacion, None, f.right.right)
					if  noB2 not in hoja:
						S2.append(noB2) # Crea nueva hoja con no B2
						if f.right.right in S2:
							booleano = False
					if S2 not in lista_hojas and booleano:
						lista_hojas.append(S2) # Agrega nueva hoja con no B2
					elif not booleano:
						print "No se agrego la hoja ", imprime_hoja(S2), " porque ", Inorder(f.right.right), " estaba en sus 2 formas"

		else: # No hay formulas que no sean literales
			p = True
			for i in letrasProposicionales:
				t = Tree(i, None, None)
				if t in hoja and Tree("~", None, t) in hoja:
					print "La hoja ", imprime_hoja(hoja), " es inconcistente porque esta las dos formas de ", Inorder(t)
					lista_hojas.remove(hoja)
					p = False
					break
			if p:
				print "La hoja ", imprime_hoja(hoja), " es consistente"
				interpretaciones.append(hoja)
				lista_hojas.remove(hoja)

	# Dice si la raiz es inconsistente
	# print "Hay " + str(len(interpretaciones)) + u" interpretaciones que satisfacen la fórmula"
	if len(interpretaciones) > 0:
		print u"La fórmula es satisfacible por las siguientes interpretaciones: "

		# Interpreta como string la lista de interpretaciones
		INTS = []
		for i in interpretaciones:
			aux = [Inorder(l) for l in i]
			INTS.append(aux)
			print aux
			
		# Eliminamos repeticiones dentro de cada interpretacion
		INTS = [list(set(i)) for i in INTS]
		# Eliminamos interpretaciones repetidas
		INTS_set = set(tuple(x) for x in INTS)
		INTS = [list(x) for x in INTS_set]
		print "Hay " + str(len(INTS)) + u" interpretaciones que satisfacen la fórmula"

		return "Satisfacible", INTS
	else:
		print(u"La lista de fórmulas dada es insatisfacible!")
		return "Insatisfacible", None

##############################################################################
# Fin definicion de objeto tree y funciones
##############################################################################
