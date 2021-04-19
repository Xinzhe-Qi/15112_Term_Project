import pygame

white           = (255, 255, 255)
black           = (  0,   0,   0)
aquamarine3     = (102, 205, 170)
red             = (255,   0,   0)
blue            = (  0,   0, 255)
grey            = (128, 128, 128)

class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.color = white
        self.width = 150
        self.height = 100
        self.hovered = False
        self.clicked = False

    def draw(self, win):
        if self.hovered:
            self.color = blue
        else:
            self.color = white

        font = pygame.font.Font("Amatic-Bold.ttf", 40)
        text = font.render(self.text, 1, self.color)
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), 
            self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and \
                self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

    def hover(self, pos):
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.width and \
                self.y <= y1 <= self.y + self.height:
            self.hovered = True
            return True
        else:
            self.hovered = False
            return False





