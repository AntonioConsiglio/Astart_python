import pygame
import config

def get_font(text_zize=28):
    return pygame.font.Font("./fonts/monogram.ttf", text_zize)

class DynamicLable():
    def __init__(self,x,y,w,h):

        self.rect_render = pygame.Rect(x,y,w,h)
    
    def draw(self,surface,text:None):
        text_render = get_font(24).render(text,1,"White")
        surface.fill(config.BACKGROUND,self.rect_render)
        surface.blit(text_render,self.rect_render)
        return
    
class BoxLable():

    def __init__(self,
                 header_text,font_size=28,
                 right_x=20,right_y=610,
                 h_offset=50,w_offset=120,
                 hl_offset=25):
        
        self.header_text = get_font(font_size).render(header_text,1,"White")
        self.right_x = right_x
        self.right_y = right_y
        self.w_offset = w_offset

        self.right_line = [(right_x, right_y), 
                           (right_x, right_y + h_offset)]
        
        self.left_line = [(right_x + w_offset , right_y), 
                          (right_x + w_offset, right_y + h_offset)]
        
        self.h_line = [(right_x + 10, right_y + hl_offset),
                       (right_x + w_offset - 10, right_y + hl_offset)]


    def draw(self,surface):

        pygame.draw.line(surface, config.GREY, *self.right_line, 2)
        pygame.draw.line(surface, config.GREY, *self.left_line, 2)
        pygame.draw.line(surface, config.GREY, *self.h_line, 2)

        surface.blit(self.header_text,(self.right_x + 10,
                                        self.right_y ,
                                     self.w_offset - 10 ,20))

        return