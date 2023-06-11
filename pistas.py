import soko
import cola

POS_DIR=[(1, 0), (-1, 0), (0, -1), (0, 1)]

def buscar_solucion(estado_inicial):
    visitados = set()
    return backtrack(estado_inicial, visitados)

def backtrack(estado, visitados):
    visitados.add(representacion_estado(estado))
    if soko.juego_ganado(estado):
        # ¡encontramos la solución!
        return True, []
    for direc in POS_DIR:
        nuevo_estado = soko.mover(estado, direc)
        if representacion_estado(nuevo_estado) in visitados:
            continue
        solución_encontrada, acciones = backtrack(nuevo_estado, visitados)
        if solución_encontrada:
            
            return True, ([direc]+ acciones)
    return False, None

def representacion_estado(juego):
    estado = ''
    for f in range(len(juego)):
        for c in range(len(juego[f])):
            
            estado += juego[f][c]
    return estado
