def guardar_niveles(archivo_niveles):
    '''Recibe el archivo con los niveles y devuelve un diccionario donde cada clave es un nivel.'''
    niveles = {}
    with open (archivo_niveles) as archivo_niveles:
        i= 1
        contenido = []
        for linea in archivo_niveles:
            linea = linea.rstrip("\n")
            linea_sin_esp = ''.join(linea.split()) #linea sin espacios para evaluar si es alfanumerica
            if linea != '':
                if linea_sin_esp.isalnum() == False and "'" not in linea_sin_esp: #si no es alfanumerica y no tiene comillas
                    contenido.append(linea)
                    niveles [i] = contenido
            else:
                contenido = []
                i += 1
    return niveles

def obtener_teclas(archivo_entrada):
    '''Recibe el archivo con las teclas asignadas y devuelve un dicionario donde cada clave es una funcionalidad/acción.'''
    teclas = {}
    with open (archivo_entrada) as archivo_teclas:
        for linea in archivo_teclas:
            linea = linea.rstrip('\n')
            if linea == '':
                continue
            tecla, accion = linea.split(' = ')
            if accion not in teclas:
                teclas[accion] = [tecla]
            else:
                teclas[accion].append(tecla)
    return teclas