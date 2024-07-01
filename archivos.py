from Classpokemon import *
import re
from funciones import *
import json

def cargar_lista_pokemons(path):
    lista = []

    with open(path, 'r') as archivo:
        archivo.readline()

        for line in archivo:
            lectura = re.split(',|\n', line)
            nombre = lectura[0]
            origen = (int(lectura[1]), int(lectura[2]))
            dimensiones = (int(lectura[3]), int(lectura[4]))
            imagen = lectura[5]
            audio = lectura[6]
            generacion = int(lectura[7])

            pokemon = Pokemon(nombre, origen, dimensiones, imagen, audio, generacion)

            lista.append(pokemon)

    return lista

def cargar_nombre_pokemons(path):
    lista = []

    with open(path, 'r') as archivo:
        archivo.readline()

        for line in archivo:
            lectura = re.split(',|\n', line)
            nombre = lectura[0]
            name_en = lectura[1]
            name_fr = lectura[2]
            name_it = lectura[3]
            name_de = lectura[4]

            nombre_pokemon = (nombre, name_en, name_fr, name_it, name_de)

            lista.append(nombre_pokemon)

    return lista

def guardar_estadisticas(path, aciertos, lista_tiempos):
    estadisticas = leer_estadisticas(path)
    mejor_tiempo, peor_tiempo, tiempo_promedio = calcular_estadisticas(lista_tiempos)
    datos_a_guardar = {
        "aciertos": aciertos,
        "mejor_tiempo": mejor_tiempo,
        "peor_tiempo": peor_tiempo,
        "tiempo_promedio": tiempo_promedio,
        "tiempos": lista_tiempos
    }
    estadisticas.append(datos_a_guardar)
    with open(path, 'w') as archivo:
            json.dump(estadisticas, archivo, indent = 4)

def leer_estadisticas(path):
    diccionario = []
    try:
        with open(path, 'r') as archivo:
            diccionario = json.load(archivo)
    except:
        print('Se creo el archivo')
    
    return diccionario

def record_aciertos(path, aciertos):
    try:
        with open(path, 'r+') as archivo:
            contenido = archivo.read()
            if contenido:
                record_aciertos = int(contenido)
            else:
                record_aciertos = 0
            
            if aciertos > record_aciertos:
                archivo.seek(0)
                archivo.write(str(aciertos))
    except:
        print('El archivo no existe. Se creará uno nuevo.')
        with open(path, 'w') as archivo:
            archivo.write(str(aciertos))
        record_aciertos = aciertos
    
    return record_aciertos