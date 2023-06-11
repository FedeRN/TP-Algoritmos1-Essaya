import soko
import gamelib
import archivos
import pila
import cola
import pistas

ANCHO_VENTANA = 1000
ALTO_VENTANA = 900

DIM_CELDA = (64)


DIRECCIONES = {'NORTE' : (0, -1), 'SUR' : (0, 1), 'ESTE' : (1, 0), 'OESTE' : (-1, 0)}




def cargar_imagenes(juego, c, f):
    '''Esta función carga las imagenes que deban estar en cada celda'''
    gamelib.draw_image('img/ground.gif', c*DIM_CELDA+(DIM_CELDA//2) , f*DIM_CELDA+(DIM_CELDA//2))
    if soko.hay_jugador(juego, c, f):
        gamelib.draw_image('img/player.gif', c*DIM_CELDA+(DIM_CELDA//2) , f*DIM_CELDA+(DIM_CELDA//2))
    if soko.hay_caja(juego, c, f):
        gamelib.draw_image('img/box.gif', c*DIM_CELDA+(DIM_CELDA//2) , f*DIM_CELDA+(DIM_CELDA//2))    
    if soko.hay_objetivo(juego, c, f):
        gamelib.draw_image('img/goal.gif', c*DIM_CELDA+(DIM_CELDA//2) , f*DIM_CELDA+(DIM_CELDA//2))
    if soko.hay_pared(juego, c, f):
        gamelib.draw_image('img/wall.gif', c*DIM_CELDA+(DIM_CELDA//2) , f*DIM_CELDA+(DIM_CELDA//2))
    
       

def dibujar_juego(juego, datos_juego, nivel):
    '''Dibuja el estado del juego y lo actualiza'''
    for f in range(len(juego)):
        for c in range(len(juego[f])):
            cargar_imagenes(juego, c, f) #dibuja el contenido del tablero
    if nivel not in datos_juego['niveles']:
        gamelib.say("Felicidades, has completado todos los niveles!\n Presiona " + datos_juego['teclas'] ['SALIR'][0] + " para cerrar la ventana.")
    if nivel in datos_juego['niveles']:
        gamelib.draw_text("nivel " + str(nivel), DIM_CELDA, DIM_CELDA//3, font='Lucida Console', size = 18, fill='white')
    if datos_juego['soluciones'].esta_vacia() == False:
        gamelib.draw_text("Hay pistas disponibles ", DIM_CELDA*5, DIM_CELDA//3, font='Lucida Console', size = 18, fill='white')



def crear_nivel(datos_juego, nivel):
    '''Crea el juego a partir de los niveles que se encuentran dentro de datos_juego y la clave que recibe, a su vez, le agrega los espacios al final de la columna
    para que el juego sea una grilla de dimensiones perfectas'''
    juego = soko.crear_grilla(datos_juego ['niveles'][nivel])
    c, f = soko.dimensiones(juego)
    for fila in range(len(juego)):
        while len(juego[fila]) < c:
            juego[fila].append(' ')
    return juego

def deshacer(datos_juego, juego, nivel):
    '''Ejecuta las acciones cuando el usuario presiona la tecla de deshacer'''
    des = datos_juego['ultimos movimientos'].desapilar()
    datos_juego['movimientos desechos'].apilar(des)
    
    if not datos_juego['ultimos movimientos'].esta_vacia():
        juego = soko.crear_grilla(datos_juego['ultimos movimientos'].ver_tope())
    else:
        juego = crear_nivel(datos_juego, nivel)
    
    return juego

def rehacer(datos_juego, juego, nivel):
    '''Ejecuta las acciones cuando el usuario presiona la tecla de rehacer'''
    re = datos_juego['movimientos desechos'].desapilar()
    juego = soko.crear_grilla(re)
    datos_juego['ultimos movimientos'].apilar(juego)

    return juego

def resolver_pistas(datos_juego, juego, nivel):
    '''Ejecuta las acciones cuando el usuario pide pistas para resolver el juego'''
    if datos_juego['soluciones'].esta_vacia():
        algoritmo = pistas.buscar_solucion(juego)
        if algoritmo[0]:
            for i in range(len(algoritmo[1])):
                datos_juego['soluciones'].encolar(algoritmo[1][i])

    else:
        mov = datos_juego['soluciones'].desencolar()
        juego = soko.mover(juego, mov)
        datos_juego['ultimos movimientos'].apilar(juego)
        datos_juego['movimientos desechos'] = pila.Pila()
        if soko.juego_ganado(juego):
            nivel += 1
            juego = crear_nivel(datos_juego, nivel)
            datos_juego['ultimos movimientos'] = pila.Pila()
            datos_juego['movimientos desechos'] = pila.Pila()
    
    return juego, nivel

def mover_con_teclas(datos_juego, juego, nivel, direccion):
    '''Ejecuta las acciones cuando el usuario presiona cualquiera de las teclas de direccion'''    
    juego = soko.mover(juego, direccion)
    datos_juego['ultimos movimientos'].apilar(juego)
    datos_juego['movimientos desechos'] = pila.Pila()
    if soko.juego_ganado(juego):
        nivel += 1
        juego = crear_nivel(datos_juego, nivel)
        datos_juego['ultimos movimientos'] = pila.Pila()
        datos_juego['movimientos desechos'] = pila.Pila()
    
    return juego, nivel





def main():
    datos_juego = {}
    try:
        datos_juego ['niveles'] = archivos.guardar_niveles('niveles.txt')
        datos_juego ['teclas'] = archivos.obtener_teclas('teclas.txt')
    except FileNotFoundError:
        print("No se ha encontrado el archivo")
        return
    except:
        print("Ocurrio un error inesperado")
        return

 
    nivel = 1
    juego = crear_nivel(datos_juego, nivel)
    # Inicializar el estado del juego
    datos_juego['ultimos movimientos'] = pila.Pila()
    datos_juego['movimientos desechos'] = pila.Pila()
    datos_juego['soluciones'] = cola.Cola()
    pistas.representacion_estado(juego)
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)

    
    while gamelib.is_alive():
        gamelib.draw_begin()
        # Dibujar la pantalla
        dibujar_juego(juego, datos_juego, nivel)
        gamelib.draw_end()

        ev = gamelib.wait(gamelib.EventType.KeyPress)
        if not ev:
            break
        

        tecla = ev.key
        # Actualizar el estado del juego, según la `tecla` presionada
        if tecla in datos_juego ['teclas']['SALIR']:
            break
        
        if tecla in datos_juego ['teclas']['REINICIAR']:
            juego = crear_nivel(datos_juego, nivel)
        
        if tecla in datos_juego ['teclas']['DESHACER'] and not datos_juego['ultimos movimientos'].esta_vacia():
            juego = deshacer(datos_juego, juego, nivel)

        
        if tecla in datos_juego ['teclas']['REHACER'] and not datos_juego['movimientos desechos'].esta_vacia():
            juego = rehacer(datos_juego, juego, nivel)


        if tecla in datos_juego ['teclas']['PISTA']:
            juego, nivel = resolver_pistas(datos_juego, juego, nivel)


        try:
            if tecla in datos_juego ['teclas']['NORTE'] or tecla in datos_juego ['teclas'] ['ESTE'] or tecla in datos_juego ['teclas'] ['SUR'] or tecla in datos_juego ['teclas'] ['OESTE']:
                
                for t in datos_juego ['teclas']:
                    if tecla in datos_juego ['teclas'][t]:
                        direccion = t
                direccion = DIRECCIONES [direccion]
                juego, nivel = mover_con_teclas(datos_juego, juego, nivel, direccion)

        except KeyError:
            pass

gamelib.init(main)