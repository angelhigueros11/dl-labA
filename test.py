# Implementación en Python con código en español

# Función para convertir una expresión regular de notación infija a postfija
def convertir_infija_a_postfija(expresion_regular):
  pila = []
  salida = ''
  prioridad = {'*': 3, '.': 2, '|': 1, '(': 0}

  for caracter in expresion_regular:
    if caracter == '(':
      pila.append(caracter)
    elif caracter == ')':
      while len(pila) != 0 and pila[-1] != '(':
        salida += pila.pop()
      pila.pop()
    elif caracter in prioridad:
      while len(pila) != 0 and prioridad[pila[-1]] >= prioridad[caracter]:
        salida += pila.pop()
      pila.append(caracter)
    else:
      salida += caracter

  while len(pila) != 0:
    salida += pila.pop()
  
  return salida

# Función para obtener el árbol de análisis sintáctico
def construir_arbol_de_analisis_sintactico(expresion_regular):
  postfija = convertir_infija_a_postfija(expresion_regular)
  pila = []

  for caracter in postfija:
    if caracter in ['*', '.', '|']:
      n2 = pila.pop()
      n1 = pila.pop()
      pila.append((caracter, n1, n2))
    else:
      pila.append(caracter)

  return pila[0]

# Función para convertir un árbol de análisis sintáctico a un AFN
def convertir_arbol_a_AFN(arbol):
  return AFN(arbol)

# Clase para crear el AFN
class AFN:
  def __init__(self, arbol):
    self.arbol = arbol
    self.estados = dict()
    self.estado_inicial = None
    self.estados_de_aceptacion = set()
    self.transiciones = dict()
    self.contador_de_estados = 0

    self._crear_estados(arbol, None)

  def _crear_estados(self, arbol, estado_anterior):
    raiz = arbol[0]
    nodo_izquierdo = arbol[1]
    nodo_derecho = arbol[2]

    estado_actual = self.contador_de_estados
    self.estados[estado_actual] = set()
    self.contador_de_estados += 1

    if estado_anterior is not None:
      self.estados[estado_anterior].add(estado_actual)

    if type(nodo_izquierdo) is tuple:
      self._crear_estados(nodo_izquierdo, estado_actual)
    else:
      self.estados[estado_actual].add(estado_actual + 1)
      self.transiciones[(estado_actual, nodo_izquierdo)] = estado_actual + 1
      self.contador_de_estados += 1

    if type(nodo_derecho) is tuple:
      self._crear_estados(nodo_derecho, estado_actual)
    else:
      self.estados[estado_actual].add(estado_actual + 1)
      self.transiciones[(estado_actual, nodo_derecho)] = estado_actual + 1
      self.contador_de_estados += 1

    if raiz == '*':
      self.estados[estado_actual].add(estado_actual)
      self.estados[estado_actual].add(estado_actual + 1)
      self.transiciones[(estado_actual, 'ε')] = estado_actual + 1
    elif raiz == '.':
      self.estados[estado_actual].add(estado_actual + 1)
      self.transiciones[(estado_actual, 'ε')] = estado_actual + 1
    elif raiz == '|':
      self.estados[estado_actual].add(estado_actual + 1)

    self.estado_inicial = 0
    self.estados_de_aceptacion.add(self.contador_de_estados - 1)

  def __str__(self):
    cadena = ''

    for estado in self.estados:
      cadena += f'Estado {estado}: {self.estados[estado]}\n'

    cadena += f'Estado inicial: {self.estado_inicial}\n'
    cadena += f'Estados de aceptación: {self.estados_de_aceptacion}\n'

    for transicion in self.transiciones:
      cadena += f'Transición: {transicion} -> {self.transiciones[transicion]}\n'

    return cadena

# Función que toma una expresión regular como entrada y devuelve un AFN
def construir_AFN(expresion_regular):
  arbol = construir_arbol_de_analisis_sintactico(expresion_regular)
  return convertir_arbol_a_AFN(arbol)

# Prueba 
expresion_regular = '(a|b).c*'
afn = construir_AFN(expresion_regular)
print(afn)