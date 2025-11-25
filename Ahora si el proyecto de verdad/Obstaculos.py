import pygame
import Constantes
class Ladrillo():
    def __init__(self, x, y, ancho, alto):

        self.forma = pygame.Rect(x, y, ancho, alto)
        
        # Guardamos la posición X inicial para aplicarle el scroll
        self.initial_x = x
        