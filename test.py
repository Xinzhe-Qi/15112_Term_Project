import sys
print(sys.version)

import pygame

print(1+2)
# from pygame.locals import *
# from board import Board
# from network import Network
# from textwrap import fill
# from button import Button
# from AI2 import *


# fps = 30
# boardWidth = 640
# boardHeight = 640
# numDivision = 16
# numPoint = numDivision - 1
# cellSize = boardWidth // numDivision
# chessSize = boardWidth // 40

# #                   R    G    B
# white           = (255, 255, 255)
# black           = (  0,   0,   0)
# aquamarine3     = (102, 205, 170)
# red             = (255,   0,   0)
# blue            = (  0,   0, 255)
# grey            = (128, 128, 128)

# pygame.init()
# win = pygame.display.set_mode((boardWidth, boardHeight))
# pygame.display.set_caption("Five in Row")
# clock = pygame.time.Clock()
# win_rect = win.get_rect()


# def blit_text(surface, text, pos, font, color=pygame.Color('white')):
#     words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
#     space = font.size(' ')[0]  # The width of a space.
#     max_width, max_height = surface.get_size()
#     x, y = pos
#     for line in words:
#         for word in line:
#             word_surface = font.render(word, 0, color)
#             word_width, word_height = word_surface.get_size()
#             if x + word_width >= max_width:
#                 x = pos[0]  # Reset the x.
#                 y += word_height  # Start on new row.
#             surface.blit(word_surface, (x, y))
#             x += word_width + space
#         x = pos[0]  # Reset the x.
#         y += word_height  # Start on new row.


# def settingScreen(win):
#     # Game Rule
#     # Adjustments

#     ruleButton = Button("Game Rule", boardWidth/2 - 100, boardHeight/3)
#     adjustButton = Button("Adjust Game", boardWidth/2 - 100, boardHeight/3*2)
    
#     run = True
#     while run:
#         win.fill(black)

#         ruleButton.draw(win)
#         adjustButton.draw(win)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 run = False

#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if ruleButton.click(event.pos):
#                     ruleButton.clicked = True
#                     ruleScreen(win)
#                     run = False
#                 elif adjustButton.click(event.pos):
#                     adjustButton.click(event.pos)

#                     run = False


#         pygame.display.update()



# def ruleScreen(win):

#     returnButton = Button("Return", 500, 600)
#     egImg = pygame.image.load("gomoku.gif")
#     egImg = pygame.transform.scale(egImg, (300, 300))
#     egRect = egImg.get_rect(topleft = (150, 350))

#     run = True
#     while run:
#         win.fill(black)
#         font = pygame.font.Font("handlee-regular.ttf", 40)
#         text = "It is a board game for two players who take turns in putting black and white stones on the board. Each players' goal is to create an unbroken row of five stones horizontally, vertically, or diagonally."
 
#         blit_text(win, text, (20, 20), font)

#         returnButton.draw(win)

#         win.blit(egImg, egRect)
    

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 run = False
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if returnButton.click(event.pos):
#                     returnButton.clicked = True
#                     settingScreen(win)
#                     run = False

#         pygame.display.update()


# def menuScreen(win):
#     # angle = 0
#     hgImg = pygame.image.load("hg2.png")
#     hgImg = pygame.transform.scale(hgImg, (55, 55))
#     # hgRect = hgImg.get_rect()
#     image_rect = hgImg.get_rect()
#     # hgRect.center = (boardWidth / 2, boardHeight / 2)

#     setImg = pygame.image.load("settings2.png")
#     setting = pygame.transform.scale(setImg, (50, 50))
#     setRect = setting.get_rect(topleft = (400, 50))

#     run = True

#     while run:
#         win.fill(aquamarine3)

#         pygame.font.init()
#         font = pygame.font.Font("FFF_Tusj.ttf", 40)
#         titleText = font.render("Online Chess!", True, red)
#         joinText = font.render("Click To Join a Game!", True, blue)

#         # print(titleText.get_width())
#         # print(titleText.get_height())

#         text_rect = titleText.get_rect()
#         text_rect.left = 0
#         text_rect.bottom = boardHeight

#         win.blit(titleText, text_rect)

#         win.blit(joinText, (boardWidth/2 - joinText.get_width() / 2, 400))

#         win.blit(hgImg, image_rect)
#         win.blit(setting, setRect)

#         # s = pygame.Surface((1000,750))  # the size of your rect
#         # s.set_alpha(128)                # alpha level
#         # s.fill(aquamarine3)           # this fills the entire surface
#         # win.blit(s, (0,0)) 

#         # hgx = boardWidth / 2
#         # hgy = boardHeight / 2
        
#         # hgImg = pygame.transform.rotate(hgImg, angle)
#         # image_rect = hgImg.get_rect(center=image_rect.center)
#         # angle += 1

#         clock.tick(30)

#         pygame.display.update()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 run = False

#             elif event.type == pygame.MOUSEBUTTONUP:
#                 # x, y = event.pos
#                 print(event.pos)
#                 if setRect.collidepoint(event.pos):
#                     run = False
#                     settingScreen(win)

# menuScreen(win)
