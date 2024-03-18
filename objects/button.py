import pygame
import config

class Button():

    def __init__(self,x, y,text="No Text",
                 width=100, height=40):
       self.x = x
       self.y = y
       self.w = width
       self.h = height
       self.text = text
       self.button_rect = pygame.Rect(x,y, width, height)

       self.clicked = False

    def draw(self,surface):
    
        called = False
        # Define the button surface and font
        button_font = pygame.font.Font(None, 28)
        button_surface = pygame.Surface((self.w, self.h))
        button_surface.fill(config.WALK_BLUE)

        # Render the button text
        text_rendered = button_font.render(self.text, True, "White")
        text_rect = text_rendered.get_rect(center=(self.w // 2, self.h // 2))
        button_surface.blit(text_rendered, text_rect)

        #action of the button
        pos = pygame.mouse.get_pos() 
        if self.button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                called = True
        else:
            self.clicked = False
        # Blit the button surface to the screen
        surface.blit(button_surface, (self.x, self.y))

        return called