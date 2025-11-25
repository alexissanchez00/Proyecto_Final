import pygame
import Constantes 

class Personaje():
    def __init__ (self, x, y, animaciones):
        self.flip = False # Controla la orientación de la imagen
        self.animaciones = animaciones
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        
        # --- Carga de Imagen y Hitbox ---
        self.image = self.animaciones[self.frame_index]
        self.forma = self.image.get_rect() 
        self.forma.center = (x,y)
        
        # --- AJUSTAR LA HITBOX (Para centrar y reducir el tamaño) ---
        original_bottom = self.forma.bottom      # Guarda la posición del suelo (base)
        original_center_x = self.forma.centerx   # Guarda el centro horizontal
        
        # 1. Reducir el tamaño de la hitbox (Ajusta estos porcentajes)
        self.forma.width = int(self.forma.width * 0.3)  
        self.forma.height = int(self.forma.height * 0.3) 

        # 2. Crea el nuevo Rect y lo centra en la posición original
        self.forma = pygame.Rect(self.forma.x, self.forma.y, self.forma.width, self.forma.height)
        self.forma.centerx = original_center_x 
        self.forma.bottom = original_bottom     
        
        # --- Variables de Física y Salto ---
        self.en_el_aire = False
        self.velocidad_y = 0
        self.gravedad = 0.7     
        self.fuerza_salto = -18 
        self.suelo_y = y        
        
        # --- Variable de Animación ---
        self.corriendo = False 
        

    def update(self):
        cooldown_animacion = 100
        self.image = self.animaciones[self.frame_index]
        
        if self.corriendo or self.en_el_aire: 
            
            if pygame.time.get_ticks() - self.update_time >=cooldown_animacion:
                self.frame_index = self.frame_index + 1
                self.update_time = pygame.time.get_ticks()
                
                if self.frame_index >= len(self.animaciones):
                    self.frame_index = 0 
        # Si está quieto (no se mueve horizontalmente ni salta), se queda en el frame de reposo
        else:
            self.frame_index = 0
            self.image = self.animaciones[self.frame_index]


    def dibujar(self, interfaz):
        # Refleja la imagen si self.flip es True
        imagen_flip = pygame.transform.flip(self.image,self.flip,False)
        interfaz.blit(imagen_flip, self.forma)
        
        # Muestra la Hitbox (caja de colisión) en rojo
        pygame.draw.rect(interfaz, (255, 0, 0), self.forma, 2)
    
    
    def salto(self):
        # Inicia el salto aplicando el impulso inicial negativo (hacia arriba)
        if self.en_el_aire == False:
            self.velocidad_y = self.fuerza_salto
            self.en_el_aire = True

    
    def movimiento(self,delta_x,delta_y):
        
        # 1. Aplicar la gravedad (si está en el aire)
        if self.en_el_aire == True:
            self.velocidad_y += self.gravedad 
        
        # 2. Determinar el movimiento vertical
        if self.en_el_aire:
            movimiento_vertical = self.velocidad_y 
        else:
            movimiento_vertical = delta_y 
            
        # 3. Restricción y Detección de Suelo
        if self.forma.centery + movimiento_vertical >= self.suelo_y:
            
            # Fija el personaje al suelo
            
            movimiento_vertical = self.suelo_y - self.forma.centery 
            self.en_el_aire = False
            self.velocidad_y = 0

        # 5. Aplicar el movimiento final
        self.forma.x += delta_x
        self.forma.y += movimiento_vertical