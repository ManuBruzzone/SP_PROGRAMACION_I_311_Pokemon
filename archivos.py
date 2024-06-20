from Classpokemon import *
import re

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