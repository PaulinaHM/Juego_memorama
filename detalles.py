import pygame

# Inicializar pygame para cargar los sonidos
pygame.mixer.init()


#Medidas y tamaños
altura_boton = 30  # Del botón de abajo, para iniciar juego
medida_cuadro = 160  # Medida de la imagen en pixeles

# Colores para la pantalla
color_blanco = (255, 255, 255)
color_negro = (0, 0, 0)
color_gris = (206, 206, 206)
color_azul = (30, 136, 229)

# Implementar los sonidos
SONIDOS = {
    "fondo": pygame.mixer.Sound("archivos/fondo.wav"),
    "clic": pygame.mixer.Sound("archivos/clic.wav"),
    "exito": pygame.mixer.Sound("archivos/ganador.wav"),
    "fracaso": pygame.mixer.Sound("archivos/equivocado.wav"),
    "voltear": pygame.mixer.Sound("archivos/voltear.wav"),
}