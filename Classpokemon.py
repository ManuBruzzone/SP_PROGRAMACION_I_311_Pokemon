import pygame

class Pokemon:
    def __init__(self, nombre, origen, dimensiones, imagen, audio, generacion):
        self.nombre = nombre
        self.imagen = pygame.image.load(imagen)
        self.imagen = pygame.transform.scale(self.imagen, dimensiones)
        self.rectangulo = self.imagen.get_rect()
        self.rectangulo.center = origen
        self.generacion = generacion
        self.audio = audio

    def dibujar(self, pantalla, mostrar_silueta, dificultad):
        silueta = self.imagen.copy()
        silueta.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)

        if dificultad == ['Easy']:
            pantalla.blit(self.imagen, self.rectangulo)
        elif dificultad == ['Hard']:
            silueta_pixelada = pygame.transform.scale(silueta, (silueta.get_width() // 10, silueta.get_height() // 10))
            silueta_pixelada = pygame.transform.scale(silueta_pixelada, silueta.get_size())
            if mostrar_silueta:
                pantalla.blit(silueta_pixelada, self.rectangulo)
                pantalla.blit(silueta_pixelada, self.rectangulo)
            else:
                pantalla.blit(self.imagen, self.rectangulo)
        else:
            if mostrar_silueta:
                pantalla.blit(silueta, self.rectangulo)
            else:
                pantalla.blit(self.imagen, self.rectangulo)
    

    def nombres(self, lista_nombres, fuente, color, pantalla):
        encontrado = False
        for nombre in lista_nombres:
            if self.nombre == nombre[0]:
                name_en = nombre[1]
                name_fr = nombre[2]
                name_it = nombre[3]
                name_de = nombre[4]
                encontrado = True
                break

        if encontrado:
            texto_1 = fuente.render(name_en, True, color)
            texto_2 = fuente.render(name_fr, True, color)
            texto_3 = fuente.render(name_it, True, color)
            texto_4 = fuente.render(name_de, True, color)

            pantalla.blit(texto_1, (30, 170))
            pantalla.blit(texto_2, (30, 220))
            pantalla.blit(texto_3, (30, 270))  
            pantalla.blit(texto_4, (30, 320))
 

    def filtrar_pokemons(self, lista_pokemons, generaciones):
        pokemons_filtrados = []

        if not generaciones:
            pokemons_filtrados = lista_pokemons
        else:
            for pokemon in lista_pokemons:
                if pokemon.generacion in generaciones:
                    pokemons_filtrados.append(pokemon)

        return pokemons_filtrados