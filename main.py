import pygame
from archivos import *
from Classpokemon import *
from Classbotones import *
from Classanimacion import *
import random
import os

NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AZUL_CLARO = (0, 150, 255)
BLANCO = (255, 255, 255)

# Configuración de la ventana
ANCHO_VENTANA = 650 
ALTO_VENTANA = 720
TAMANO_VENTANA = (ANCHO_VENTANA, ALTO_VENTANA)

# Inicialización de Pygame
pygame.init()

# Cargar la lista de Pokemons
lista_pokemons = cargar_lista_pokemons('pokemons.csv')
lista_nombre = cargar_nombre_pokemons('pokemon_names_multilang.csv')

# Configurar la ventana
ventana = pygame.display.set_mode(TAMANO_VENTANA)
pygame.display.set_caption("Who's That Pokemon?")
icono = pygame.image.load('Recursos\Icono\Pokeball.png')
pygame.display.set_icon(icono)
ventana.fill(AZUL_CLARO)

# Banderas
reino_unido = pygame.image.load(r'Recursos\Banderas\Reino_Unido.png')
reino_unido = pygame.transform.scale(reino_unido, (25,25))
francia = pygame.image.load(r'Recursos\Banderas\Francia.png')
francia = pygame.transform.scale(francia, (25,25))
italia = pygame.image.load(r'Recursos\Banderas\Italia.png')
italia = pygame.transform.scale(italia, (25,25))
alemania = pygame.image.load(r'Recursos\Banderas\Alemania.png')
alemania = pygame.transform.scale(alemania, (25,25))

# Fuentes
fuente = pygame.font.SysFont('consolas', 20)
fuente_titulo = pygame.font.SysFont('Arial', 40)

# Input
input_rect = pygame.Rect(0, 0, 200, 32)
input_rect.center = (ANCHO_VENTANA // 2, ALTO_VENTANA // 1.7 + 1.7)
texto = ''

# Textos
texto_superior = fuente_titulo.render("Who's That Pokemon?", True, BLANCO)
texto_generaciones = fuente.render('Generation', True, NEGRO)
texto_dificultad = fuente.render('Difficulty', True, NEGRO)

# Ruta y configuración de la animación
ruta_frames = 'Recursos/frames-gif'
animacion = Animacion(ruta_frames, 3000)

# Botones
botones_generaciones = Botones()
botones_dificultad = Botones()
botones_generaciones.crear_botones_generacion(75, 45, 3, 3, (50, 480), 1)
botones_dificultad.crear_botones_dificultad(110, 45, 3, 1, (500, 480), 1)

# Seleccionar Pokémon inicial
pokemon_actual = random.choice(lista_pokemons)

# Inicializar generaciones seleccionadas y lista filtrada
generaciones_seleccionadas = botones_generaciones.obtener_generaciones_seleccionadas()
lista_pokemons_filtrada = pokemon_actual.filtrar_pokemons(lista_pokemons, generaciones_seleccionadas)
pokemon_actual = random.choice(lista_pokemons_filtrada) if lista_pokemons_filtrada else None

# Banderas
mostrar_silueta = True
siguiente = False
activo = False
flag = True
aplicar_filtro = False
mostrar_nombres = False 
respuestas_correctas = 0
mejor_racha = 0
tiempo_inicio_respuesta = 0
tiempo_fin_respuesta = 0

while flag:
    lista_eventos = pygame.event.get()
    tiempo_actual = pygame.time.get_ticks()
    tiempo_inicio_respuesta = pygame.time.get_ticks()

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            flag = False

        elif evento.type == pygame.KEYDOWN:
            if activo:
                if evento.key == pygame.K_BACKSPACE:
                    texto = texto[:-1]
                elif evento.key == pygame.K_RETURN:
                    if pokemon_actual.nombre.lower() == texto.lower():
                        mostrar_silueta = False
                        mostrar_nombres = True
                        respuestas_correctas += 1
                        tiempo_fin_respuesta = pygame.time.get_ticks()
                        if respuestas_correctas > mejor_racha:
                            mejor_racha = respuestas_correctas
                        animacion.iniciar(tiempo_actual)
                    else:
                        pass
                    texto = ""
                else:
                    texto += evento.unicode

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(evento.pos):
                activo = not activo
            else:
                activo = False

            pos = evento.pos
            botones_generaciones.actualizar_color_boton(pos)
            botones_dificultad.actualizar_color_boton(pos)
            aplicar_filtro = True

    if siguiente:
        if aplicar_filtro:
            generaciones_seleccionadas = botones_generaciones.obtener_generaciones_seleccionadas()
            lista_pokemons_filtrada = pokemon_actual.filtrar_pokemons(lista_pokemons, generaciones_seleccionadas)
            aplicar_filtro = False

        if lista_pokemons_filtrada:
            pokemon_actual = random.choice(lista_pokemons_filtrada)
        mostrar_silueta = True
        mostrar_nombres = False
        siguiente = False

    if not mostrar_silueta and tiempo_actual - animacion.tiempo_inicial >= animacion.tiempo_maximo:
        tiempo_inicio_respuesta = pygame.time.get_ticks()
        pokemon_actual = random.choice(lista_pokemons)
        mostrar_silueta = True 
        animacion.tiempo_inicial = 0
        siguiente = True
        mostrar_nombres = False

    generaciones_seleccionadas = botones_generaciones.obtener_generaciones_seleccionadas()

    ventana.fill(AZUL_CLARO)

    botones_generaciones.dibujar_botones_generacion(ventana, NEGRO, fuente)
    botones_dificultad.dibujar_botones_dificultad(ventana, NEGRO, fuente)
    dificultad_seleccionada = botones_dificultad.obtener_dificutlad_seleccioanda()
    
    pokemon_actual.dibujar(ventana, mostrar_silueta, dificultad_seleccionada)

    if tiempo_inicio_respuesta > 0 and tiempo_fin_respuesta > 0:
        tiempo_respuesta = tiempo_fin_respuesta - tiempo_inicio_respuesta
        tiempo_respuesta_segundos = tiempo_respuesta / 1000  # Convertir a segundos
        texto_tiempo = fuente.render(f'Tiempo de respuesta: {tiempo_respuesta_segundos:.2f} segundos', True, NEGRO)
        ventana.blit(texto_tiempo, (50, 100))

    margen_derecho = 10
    cuadro_ancho = 150
    cuadro_alto = 60
    pygame.draw.rect(ventana, BLANCO, (ANCHO_VENTANA - margen_derecho - cuadro_ancho, margen_derecho, cuadro_ancho, cuadro_alto))

    pygame.draw.rect(ventana, BLANCO, input_rect)
    superficie_texto = fuente.render(texto, True, NEGRO)
    ventana.blit(superficie_texto, (input_rect.x + 5, input_rect.y + (input_rect.height - superficie_texto.get_height()) // 2))
    ventana.blit(texto_superior, (ANCHO_VENTANA // 2 - texto_superior.get_width() // 2, 50))
    ventana.blit(texto_generaciones, (110, 690))
    ventana.blit(texto_dificultad, (498, 690))



    texto_respuestas_correctas = fuente.render(f'Streak: {respuestas_correctas}', True, NEGRO)
    texto_mejor_racha = fuente.render(f'Best: {mejor_racha}', True, NEGRO)

    # Pruebas
    nombre_pokemon = fuente.render(f'{pokemon_actual.nombre} {pokemon_actual.generacion}', True, NEGRO)
    ventana.blit(nombre_pokemon, (50, 50))

    animacion.actualizar(tiempo_actual)
    animacion.dibujar(ventana, (input_rect.right + 50, input_rect.y + (input_rect.height - 90) // 2))
 
    if mostrar_nombres:
        pokemon_actual.nombres(lista_nombre, fuente, NEGRO, ventana)
        ventana.blit(reino_unido, (0,168))
        ventana.blit(francia, (0,218))
        ventana.blit(italia, (0,268))
        ventana.blit(alemania, (0,318))


    pygame.display.update()

pygame.quit()