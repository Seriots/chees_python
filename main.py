import pygame
from game import Game

pygame.init()

background = pygame.image.load("assets/plateau_background.jpg")
board_size = 600
screen = pygame.display.set_mode((board_size, board_size))
pygame.display.set_caption('Chess')
case_size = board_size/8

game = Game(case_size)

running = True
while running:
    screen.blit(background, (0, 0))
    game.update(screen)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.piece_in_movement is None:
                game.pick(case_size)
                if game.piece_in_movement is not None and game.possible_case == []:
                    game.all_possible_case()
                    game.generate_blue_cases()
            else:
                game.drop(case_size)
