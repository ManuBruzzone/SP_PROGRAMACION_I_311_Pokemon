from Classpokemon import *
import re
import datetime
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

def guardar_datos_json(path,datos):
    with open(path, 'w') as archivo:
            json.dump(datos, archivo, indent = 4)