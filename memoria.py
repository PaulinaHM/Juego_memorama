
import pygame
import sys
import math
import time
import random


pygame.init()
pygame.font.init()
pygame.mixer.init()



altura_boton = 30 
medida_cuadro = 160  
nombre_imagen_oculta = "assets/oculta.png"
imagen_oculta = pygame.image.load(nombre_imagen_oculta)
segundos_mostrar_pieza = 2  


class Cuadro:
    def __init__(self, fuente_imagen):
        self.mostrar = True
        self.descubierto = False

        self.fuente_imagen = fuente_imagen
        self.imagen_real = pygame.image.load(fuente_imagen)

cuadros = [
    [Cuadro("assets/coco.png"), Cuadro("assets/coco.png"),
     Cuadro("assets/manzana.png"), Cuadro("assets/manzana.png")],
    [Cuadro("assets/limón.png"), Cuadro("assets/limón.png"),
     Cuadro("assets/naranja.png"), Cuadro("assets/naranja.png")],
    [Cuadro("assets/pera.png"), Cuadro("assets/pera.png"),
     Cuadro("assets/piña.png"), Cuadro("assets/piña.png")],
    [Cuadro("assets/plátano.png"), Cuadro("assets/plátano.png"),
     Cuadro("assets/sandía.png"), Cuadro("assets/sandía.png")],
]
color_blanco = (255, 255, 255)
color_negro = (0, 0, 0)
color_gris = (206, 206, 206)
color_azul = (30, 136, 229)

sonido_fondo = pygame.mixer.Sound("assets/fondo.wav")
sonido_clic = pygame.mixer.Sound("assets/clic.wav")
sonido_exito = pygame.mixer.Sound("assets/ganador.wav")
sonido_fracaso = pygame.mixer.Sound("assets/equivocado.wav")
sonido_voltear = pygame.mixer.Sound("assets/voltear.wav")

anchura_pantalla = len(cuadros[0]) * medida_cuadro
altura_pantalla = (len(cuadros) * medida_cuadro) + altura_boton
anchura_boton = anchura_pantalla

tamanio_fuente = 20
fuente = pygame.font.SysFont("Arial", tamanio_fuente)
xFuente = int((anchura_boton / 2) - (tamanio_fuente / 2))
yFuente = int(altura_pantalla - altura_boton)

boton = pygame.Rect(0, altura_pantalla - altura_boton,
                    anchura_boton, altura_pantalla)

ultimos_segundos = None
puede_jugar = True 
juego_iniciado = False
x1 = None
y1 = None
x2 = None
y2 = None

def ocultar_todos_los_cuadros():
    for fila in cuadros:
        for cuadro in fila:
            cuadro.mostrar = False
            cuadro.descubierto = False


def aleatorizar_cuadros():
    cantidad_filas = len(cuadros)
    cantidad_columnas = len(cuadros[0])
    for y in range(cantidad_filas):
        for x in range(cantidad_columnas):
            x_aleatorio = random.randint(0, cantidad_columnas - 1)
            y_aleatorio = random.randint(0, cantidad_filas - 1)
            cuadro_temporal = cuadros[y][x]
            cuadros[y][x] = cuadros[y_aleatorio][x_aleatorio]
            cuadros[y_aleatorio][x_aleatorio] = cuadro_temporal


def comprobar_si_gana():
    if gana():
        pygame.mixer.Sound.play(sonido_exito)
        reiniciar_juego()

def gana():
    for fila in cuadros:
        for cuadro in fila:
            if not cuadro.descubierto:
                return False
    return True


def reiniciar_juego():
    global juego_iniciado
    juego_iniciado = False


def iniciar_juego():
    pygame.mixer.Sound.play(sonido_clic)
    global juego_iniciado
    # Aleatorizar 3 veces
    for i in range(3):
        aleatorizar_cuadros()
    ocultar_todos_los_cuadros()
    juego_iniciado = True


pantalla_juego = pygame.display.set_mode((anchura_pantalla, altura_pantalla))
pygame.display.set_caption('Memorama en Python')

while True:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and puede_jugar:

            xAbsoluto, yAbsoluto = event.pos
            if boton.collidepoint(event.pos):
                if not juego_iniciado:
                    iniciar_juego()

            else:
                if not juego_iniciado:
                    continue
              
                x = math.floor(xAbsoluto / medida_cuadro)
                y = math.floor(yAbsoluto / medida_cuadro)
                cuadro = cuadros[y][x]
                if cuadro.mostrar or cuadro.descubierto:
                    continue
                if x1 is None and y1 is None:
                    x1 = x
                    y1 = y
                    cuadros[y1][x1].mostrar = True
                    pygame.mixer.Sound.play(sonido_voltear)
                else:
                    x2 = x
                    y2 = y
                    cuadros[y2][x2].mostrar = True
                    cuadro1 = cuadros[y1][x1]
                    cuadro2 = cuadros[y2][x2]
                    if cuadro1.fuente_imagen == cuadro2.fuente_imagen:
                        cuadros[y1][x1].descubierto = True
                        cuadros[y2][x2].descubierto = True
                        x1 = None
                        x2 = None
                        y1 = None
                        y2 = None
                        pygame.mixer.Sound.play(sonido_clic)
                    else:
                        pygame.mixer.Sound.play(sonido_fracaso)
                        ultimos_segundos = int(time.time())
                        puede_jugar = False
                comprobar_si_gana()

    ahora = int(time.time())
    if ultimos_segundos is not None and ahora - ultimos_segundos >= segundos_mostrar_pieza:
        cuadros[y1][x1].mostrar = False
        cuadros[y2][x2].mostrar = False
        x1 = None
        y1 = None
        x2 = None
        y2 = None
        ultimos_segundos = None
        puede_jugar = True

    pantalla_juego.fill(color_blanco)
    x = 0
    y = 0
    for fila in cuadros:
        x = 0
        for cuadro in fila:
            """
            Si está descubierto o se debe mostrar, dibujamos la imagen real. Si no,
            dibujamos la imagen oculta
            """
            if cuadro.descubierto or cuadro.mostrar:
                pantalla_juego.blit(cuadro.imagen_real, (x, y))
            else:
                pantalla_juego.blit(imagen_oculta, (x, y))
            x += medida_cuadro
        y += medida_cuadro

    if juego_iniciado:
        pygame.draw.rect(pantalla_juego, color_blanco, boton)
        pantalla_juego.blit(fuente.render(
            "Iniciar juego", True, color_gris), (xFuente, yFuente))
    else:
        pygame.draw.rect(pantalla_juego, color_azul, boton)
        pantalla_juego.blit(fuente.render(
            "Iniciar juego", True, color_blanco), (xFuente, yFuente))

    pygame.display.update()
