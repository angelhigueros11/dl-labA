
# Angel Higueros
# 20460
# Laboratorio A

import tools as tl
import implementacion as ip

def main():
    # r = '($|a*b)'

    r = '(a|b)*'

    postfix = tl.infix_a_postfix(r)
    afn = ip.crear_afn(postfix)

    if afn != None:
        ip.mostrar_resumen(r, postfix)
        ip.mostrar_afn(afn, r)
    

if __name__ == '__main__':
    main()
