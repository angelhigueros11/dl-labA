class Estado:
    def __init__(self, identificador, aceptacion=False):
        self.id = identificador
        self.aceptacion = aceptacion
        self.transiciones = {}

    def agregar_transicion(self, simbolo, estado_destino):
        if simbolo not in self.transiciones:
            self.transiciones[simbolo] = []
        self.transiciones[simbolo].append(estado_destino)

class AFN:
    def __init__(self, inicial, aceptacion):
        self.inicial = inicial
        self.aceptacion = aceptacion

    def acepta(self, cadena):
        estados_actuales = [self.inicial]
        for simbolo in cadena:
            nuevos_estados = []
            for estado in estados_actuales:
                if simbolo in estado.transiciones:
                    nuevos_estados.extend(estado.transiciones[simbolo])
            estados_actuales = nuevos_estados
        return any(estado.aceptacion for estado in estados_actuales)

def construir_afn(r):
    # Convertir la expresión regular en notación infix a notación postfix
    r_postfix = infix_a_postfix(r)

    # Construir un árbol de análisis sintáctico a partir de la expresión regular postfix
    raiz_arbol = construir_arbol(r_postfix)

    # Construir el AFN utilizando el algoritmo de McNaughton-Yamada-Thompson
    estado_actual = Estado(0)
    estado_final = Estado(1, aceptacion=True)
    construir_afn_rec(raiz_arbol, estado_actual, estado_final, 2)

    return AFN(estado_actual, estado_final)

def construir_afn_rec(arbol, estado_actual, estado_final, siguiente_id):
    if arbol != None:
        if arbol.valor == 'ε':
            estado_actual.agregar_transicion('ε', estado_final)
        elif arbol.valor in ['|', '.']:
            estado_intermedio = Estado(siguiente_id)
            siguiente_id += 1
            construir_afn_rec(arbol.hijo_izquierdo, estado_actual, estado_intermedio, siguiente_id)
            construir_afn_rec(arbol.hijo_derecho, estado_intermedio, estado_final, siguiente_id)
        elif arbol.valor == '*':
            estado_intermedio1 = Estado(siguiente_id)
            siguiente_id += 1
            estado_intermedio2 = Estado(siguiente_id, aceptacion=True)
            siguiente_id += 1
            estado_actual.agregar_transicion('ε', estado_intermedio1)
            estado_intermedio1.agregar_transicion('ε', estado_intermedio2)
            estado_intermedio1.agregar_transicion('ε', estado_final)
            estado_final.agregar_transicion('ε', estado_intermedio1)
            construir_afn_rec(arbol.hijo_izquierdo, estado_intermedio1, estado_intermedio2, siguiente_id)
        else:
            estado_siguiente = Estado(siguiente_id)
            siguiente_id += 1
            estado_actual.agregar_transicion(arbol.valor, estado_siguiente)
            construir_afn_rec(arbol.hijo_izquierdo, estado_siguiente, estado_final, siguiente_id)

def infix_a_postfix(infix):
    operadores = {'*': 3, '.': 2, '|': 1, '(': 0}
    salida = []
    pila = []
    tokens = infix
    for token in tokens:
        if token == '(':
            pila.append(token)
        elif token == ')':
            while pila[-1] != '(':
                salida.append(pila.pop())
            pila.pop()
        elif token in operadores:
            while pila and pila[-1] != '(' and operadores[token] <= operadores.get(pila[-1], 0):
                salida.append(pila.pop())
            pila.append(token)
        else:
            salida.append(token)
    while pila:
        salida.append(pila.pop())
    return ''.join(salida)

class Nodo:
    def __init__(self, valor, hijo_izquierdo=None, hijo_derecho=None):
        self.valor = valor
        self.hijo_izquierdo = hijo_izquierdo
        self.hijo_derecho = hijo_derecho

def construir_arbol(postfix):
    pila = []
    for token in postfix:
        if token == '|':
            derecho = pila.pop()
            izquierdo = pila.pop()
            pila.append(Nodo('|', izquierdo, derecho))
        elif token == '.':
            derecho = pila.pop()
            izquierdo = pila.pop()
            pila.append(Nodo('.', izquierdo, derecho))
        elif token == '*':
            subarbol = pila.pop()
            pila.append(Nodo('*', subarbol))
        else:
            pila.append(Nodo(token))
    return pila[0]


from graphviz import Digraph

def generar_grafo(afn):
    grafo = Digraph()
    estados_visitados = set()

    def agregar_estado(estado):
        if estado in estados_visitados:
            return
        estados_visitados.add(estado)
        opciones_transiciones = {}
        for simbolo, destinos in estado.transiciones.items():
            for destino in destinos:
                if simbolo == 'ε':
                    agregar_estado(destino)
                else:
                    opciones_transiciones[simbolo] = opciones_transiciones.get(simbolo, []) + [destino]
        for simbolo, destinos in opciones_transiciones.items():
            grafo.edge(str(estado.id), str(destinos[0].id), label=simbolo)
        if estado.aceptacion:
            grafo.node(str(estado.id), shape='doublecircle')
        else:
            grafo.node(str(estado.id), shape='circle')

    agregar_estado(afn.inicial)

    return grafo

    
afn = construir_afn('a*b')
grafo = generar_grafo(afn)
grafo.render('afn', view=True)
