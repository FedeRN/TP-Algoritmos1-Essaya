jugador = '@'
objetivo = '.'
pared = '#'
caja = '$'
objetivo_caja = '*'
objetivo_jugador = '+'

def crear_grilla(desc):
    '''Crea una grilla a partir de la descripción del estado inicial que recibe.
    La descripción es una lista de cadenas, cada cadena representa una
    fila y cada caracter una celda. Los caracteres pueden ser los siguientes:

    Caracter  Contenido de la celda
    --------  ---------------------
           #  Pared
           $  Caja
           @  Jugador
           .  Objetivo
           *  Objetivo + Caja
           +  Objetivo + Jugador

    Esta función devuelve la grilla como una matriz, es decir, una lista de listas
    '''
    grilla = []
    cant_de_filas = len(desc)
    for f in range(cant_de_filas):
        grilla.append(list(desc[f]))
    
    return grilla
   

def dimensiones(grilla):
    '''Recibe la grilla y devuelve una tupla con la cantidad de columnas y filas de la grilla.'''
    max_col = 0
    for f in range(len(grilla)):
        if len(grilla[f]) > max_col:
            max_col = len(grilla[f])
    return max_col, len(grilla)
    
def hay_pared(grilla, c, f):
    '''Recibe la grilla y devuelve True si hay una pared en la columna y fila (c, f).'''
    return grilla [f][c] == pared

def hay_objetivo(grilla, c, f):
    '''Recibe la grilla y devuelve True si hay un objetivo en la columna y fila (c, f).'''
    return grilla [f][c] == objetivo or grilla[f][c] == objetivo_caja or grilla[f][c] == objetivo_jugador

def hay_caja(grilla, c, f):
    '''Recibe la grilla y devuelve True si hay una caja en la columna y fila (c, f).'''
    return grilla [f][c] == caja or grilla[f][c] == objetivo_caja

def hay_jugador(grilla, c, f):
    '''Recibe la grilla y devuelve True si el jugador está en la columna y fila (c, f).'''
    return grilla [f][c] == jugador or grilla[f][c] == objetivo_jugador

def juego_ganado(grilla):
    '''Recibe la grilla y devuelve True si el juego está ganado.'''
    for f in range(len(grilla)):
        if objetivo in grilla[f] or objetivo_jugador in grilla[f]:
            return False
    return True

def posicion_jugador(grilla):
    '''Recibe la grilla y devuelve la posicion del jugador como (c,f)'''
    for f in range(len(grilla)):
        for c in range(len(grilla[f])):
            if hay_jugador(grilla, c, f):
                return c, f

def clonar_grilla(grilla):
    '''Creación de la grilla 2 clonando la grilla que recibe originalmente'''
    clonar_grilla = []
    for f in range(len(grilla)):
        fila = grilla[f].copy()
        clonar_grilla.append(fila)

    return clonar_grilla

def movimientos_vacio(nueva_grilla, pos):
    '''Recibe la grilla, la posicion del jugador y evalua que debe tener la casilla
    que abandona el jugador dependiendo si había un objetivo o no'''
    if nueva_grilla[pos[1]][pos[0]] == jugador:
        nueva_grilla[pos[1]][pos[0]] = " "
    else:
        nueva_grilla[pos[1]][pos[0]] = objetivo

def movimiento_jugador(grilla, nueva_grilla, mov, pos):
    '''Ejecuta los movimientos del jugador dependiendo si hay un objetivo o vacio en 
    la posición a mover el jugador'''
    if hay_objetivo(grilla, mov[0], mov[1]): # objetivo en la posicion a mover jugador
        nueva_grilla[mov[1]][mov[0]] = objetivo_jugador
        movimientos_vacio(nueva_grilla, pos)
    else: #vacio en la posicion a mover jugador
        nueva_grilla[mov[1]][mov[0]] = jugador
        movimientos_vacio(nueva_grilla, pos)


def mover(grilla, direccion):
    '''Mueve el jugador en la dirección indicada.

    La dirección es una tupla con el movimiento horizontal y vertical. Dado que
    no se permite el movimiento diagonal, la dirección puede ser una de cuatro
    posibilidades:

    direccion  significado
    ---------  -----------
    (-1, 0)    Oeste
    (1, 0)     Este
    (0, -1)    Norte
    (0, 1)     Sur

    La función debe devolver una grilla representando el estado siguiente al
    movimiento efectuado. La grilla recibida NO se modifica; es decir, en caso
    de que el movimiento sea válido, la función devuelve una nueva grilla.
    '''
    pos = posicion_jugador(grilla) #posicion inicial del jugador
    mov = pos[0] + direccion[0], pos[1] + direccion[1] #posicion a moverse
    nueva_grilla = clonar_grilla(grilla)
    if hay_pared(grilla, mov[0], mov[1]): #pared en la posicion a moverse
        return nueva_grilla 
    elif hay_objetivo(grilla, mov[0], mov[1]) and not hay_caja(grilla, mov[0], mov[1]): #objetivo en la posicion a moverse
        nueva_grilla[mov[1]][mov[0]] = objetivo_jugador
        movimientos_vacio(nueva_grilla, pos)
    elif hay_caja(grilla, mov[0], mov[1]): #caja en la posicion a moverse
        sig = pos[0] + direccion[0]*2, pos[1] + direccion[1]*2
        if hay_pared(grilla, sig[0], sig[1]) or hay_caja(grilla, sig[0], sig[1]): #pared o caja en la posicion a la que se mueve la caja
            return nueva_grilla
        elif hay_objetivo(grilla, sig[0], sig[1]): #objetivo en la posicion a la que se mueve la caja
            nueva_grilla[sig[1]][sig[0]] = objetivo_caja
            movimiento_jugador(grilla, nueva_grilla, mov, pos)
        else:  #vacio en la posicion a la que se mueve la caja
            nueva_grilla[sig[1]][sig[0]] = caja
            movimiento_jugador(grilla, nueva_grilla, mov, pos)
    else: #hay vacio en la posicion a moverse
        nueva_grilla[mov[1]][mov[0]] = jugador
        movimientos_vacio(nueva_grilla, pos)
    return nueva_grilla


