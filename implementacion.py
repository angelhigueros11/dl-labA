
# Angel Higueros
# 20460
# Laboratorio A

EPSILON = 'ε'
from graphviz import Digraph

class Estado:

    def __init__(self, id):
        self.id = id
        self.transiciones = []


class AFN:
    def __init__(self, inicial, final, estados):
        self.inicial = inicial
        self.final = final
        self.estados = estados



def crear_afn(expresion_regular):   # sourcery skip: simplify-len-comparison

    if expresion_regular is None:
        return None

    num_estado = 1
    stack_afns = []

    for i in range(len(expresion_regular)):
        char = expresion_regular[i]

        # Crear nuevos estados, inicio - final
        nuevo_inicio = Estado(f"{num_estado}")
        num_estado += 1
        nuevo_final = Estado(f"{num_estado}")

        if char == '|': #union
            # Obtener los dos ultimos estados
            afn2 = stack_afns.pop()
            afn1 = stack_afns.pop()

            # Conectar el nuevo estado incial a los dos estados que tenemos
            nuevo_inicio.transiciones.append((afn1.inicial, EPSILON))
            nuevo_inicio.transiciones.append((afn2.inicial, EPSILON))

            # Conectar los dos estados que tenemos al nuevo estado final
            afn1.final.transiciones.append((nuevo_final, EPSILON))
            afn2.final.transiciones.append((nuevo_final, EPSILON))

            # Crear un nuevo AFN y agregarlo a nuestra lista
            estados = afn1.estados + afn2.estados + [nuevo_inicio, nuevo_final]
            stack_afns.append(AFN(nuevo_inicio, nuevo_final, estados))

        elif char == '*': # estrella

            # Obtener el utlimo estado
            afn = stack_afns.pop()

            # Crear las transiciones, entrada - salida
            nuevo_inicio.transiciones.append((afn.inicial, EPSILON))
            afn.final.transiciones.append((nuevo_final, EPSILON))


            # Crear las transiciones, arco - incio, final
            afn.final.transiciones.append((afn.inicial, EPSILON))
            nuevo_inicio.transiciones.append((nuevo_final, EPSILON))

            # Crear un nuevo AFN y agregarlo a nuestra lista
            estados = afn.estados + [nuevo_inicio, nuevo_final]
            stack_afns.append(AFN(nuevo_inicio, nuevo_final, estados))
        else: # agregar
            
            nuevo_inicio.transiciones.append((nuevo_final, char))
            stack_afns.append(AFN(nuevo_inicio, nuevo_final, [nuevo_inicio, nuevo_final]))


        num_estado += 1

    
    if len(stack_afns) > 1: # concatenacion
        while len(stack_afns) < 1:

            afn2 = stack_afns.pop()
            afn1 = stack_afns.pop()


        afn2.final.transiciones.append((afn1.inicial, EPSILON))
        afn1.inicial.transiciones.append((afn2.final, EPSILON))

    
        estados = afn1.estados + afn2.estados
        stack_afns.append(AFN(afn1, afn2, estados))



    return stack_afns.pop()

def mostrar_afn(afn, r):
    if afn is None:
        return

    dot = Digraph(name='AFN')
    for estado in afn.estados:
        if estado == afn.inicial:
            dot.node(str(estado.id), shape='circle', style='bold')
        elif estado == afn.final:
            dot.node(str(estado.id), shape='doublecircle', style='bold')
        else:
            dot.node(str(estado.id))

        for transicion in estado.transiciones:
            if transicion[1] is not None:
                dot.edge(str(estado.id), str(transicion[0].id), label=transicion[1])
            else:
                dot.edge(str(estado.id), str(transicion[0].id), label='ε')

    dot.attr(rankdir='LR')
    dot.attr(label=f'AFN generado de r={r}')
    dot.render('afn', format='png')


def mostrar_resumen(r, postfix):
    print("\n:: AFN ::")
    print("[] r = ", r)
    print("[] postfix = ", postfix)