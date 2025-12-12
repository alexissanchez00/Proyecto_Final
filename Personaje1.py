import pygame
import Constantes

class Personaje():
    def _init_ (self, x, y, animaciones, hitbox_offset_x=0, hitbox_offset_bottom=0):
        self.flip = False # Variable booleana: False = mira derecha, True = mira izquierda
        self.animaciones = animaciones # Lista de imágenes para la animación
        self.frame_index = 0 # Índice de la imagen actual
        
        # Marca de tiempo para controlar la velocidad de la animación
        self.update_time = pygame.time.get_ticks()
        
        # Asignamos la imagen inicial
        self.image = self.animaciones[self.frame_index]

        # self.forma: Es el rectángulo de la imagen completa. Se usa para saber DÓNDE DIBUJAR.
        self.forma = self.image.get_rect()
        self.forma.center = (x, y)

        # Calculamos un tamaño de hitbox más pequeño (50% del tamaño de la imagen).
        # Esto hace que el juego se sienta mejor, evitando que mueras si algo apenas roza un pixel transparente.
        hitbox_width = int(self.forma.width * 0.5)
        hitbox_height = int(self.forma.height * 0.5)

        # Offsets: Ajustes finos para mover la hitbox independientemente de la imagen.
        self.hitbox_offset_x = hitbox_offset_x
        self.hitbox_offset_bottom = hitbox_offset_bottom

        # self.hitbox: El rectángulo invisible que usaremos para detectar choques/daño.
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)

        # Alineación inicial: Colocamos la hitbox centrada en X y alineada a los pies (bottom) en Y.
        self.hitbox.centerx = self.forma.centerx + self.hitbox_offset_x
        self.hitbox.bottom = self.forma.bottom - self.hitbox_offset_bottom
        
        self.en_el_aire = False    # Estado: ¿Está saltando o cayendo?
        self.velocidad_y = 0       # Velocidad vertical actual
        self.gravedad = 0.7        # Fuerza que lo empuja hacia abajo cada frame
        self.fuerza_salto = -18    # Fuerza negativa (hacia arriba) al saltar
        self.suelo_y = y           # Límite del suelo (piso fijo para este ejemplo)
        
        self.corriendo = False 

    def update(self):
        # Velocidad de la animación (cuántos ms dura cada frame)
        cooldown_animacion = 100 
        
        # Actualizamos la imagen según el índice actual
        self.image = self.animaciones[self.frame_index]
        
        # Solo animamos si se está moviendo o saltando
        if self.corriendo or self.en_el_aire: 
            # Control de tiempo
            if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
                self.frame_index = self.frame_index + 1
                self.update_time = pygame.time.get_ticks() # Reiniciar cronómetro
                
                # Si llegamos al final de la lista de animaciones, volvemos al inicio (bucle)
                if self.frame_index >= len(self.animaciones):
                    self.frame_index = 0 
        
        # Si está quieto (idle), forzamos el frame 0 (o una animación de "respiro")
        else:
            self.frame_index = 0
            self.image = self.animaciones[self.frame_index]


    def dibujar(self, interfaz):
        # Voltear imagen: Creamos una copia invertida si self.flip es True
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        
        # Dibujar Sprite: Usamos self.forma para poner la imagen en pantalla
        interfaz.blit(imagen_flip, self.forma)
        
        # Dibujamos un cuadro rojo para ver dónde está realmente la hitbox.
        #pygame.draw.rect(interfaz, (255, 0, 0), self.hitbox, 2)
    
    
    def salto(self):
        # Solo permitimos saltar si NO estamos ya en el aire (evita doble salto infinito)
        if self.en_el_aire == False:
            self.velocidad_y = self.fuerza_salto # Aplicamos impulso hacia arriba
            self.en_el_aire = True # Cambiamos estado

    
    def movimiento(self, delta_x, delta_y):
        
        # Si está en el aire, la gravedad aumenta la velocidad de caída constantemente
        if self.en_el_aire == True:
            self.velocidad_y += self.gravedad 
        
        # --- Calcular Movimiento Vertical ---
        if self.en_el_aire:
            # Si salta/cae, el movimiento lo dicta la física (velocidad_y)
            movimiento_vertical = self.velocidad_y 
        else:
            # Si no está en modo física, usa el movimiento manual (ej. escaleras)
            movimiento_vertical = delta_y 
            
        # Verificamos si la posición futura atravesará el suelo
        if self.forma.centery + movimiento_vertical >= self.suelo_y:
            # Ajustamos para que quede justo encima del suelo (ni un pixel abajo)
            movimiento_vertical = self.suelo_y - self.forma.centery 
            self.en_el_aire = False # Ya tocó suelo
            self.velocidad_y = 0    # Detenemos la caída

        # Actualizamos la posición del rectángulo de la imagen
        self.forma.x += delta_x
        self.forma.y += movimiento_vertical
        
        # La hitbox DEBE seguir a la imagen.
        # Recalculamos la posición de la hitbox basándonos en donde quedó la imagen (self.forma)
        # y le sumamos los offsets configurados en el _init_.
        self.hitbox.centerx = self.forma.centerx + self.hitbox_offset_x
        self.hitbox.bottom = self.forma.bottom - self.hitbox_offset_bottom