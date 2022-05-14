from pieces import King, Pawn, Bishop, Rook, Knight, Queen
import pygame


class Game:
    def __init__(self, case_size):
        self.black_death = []
        self.case_size = case_size
        self.white_death = []
        self.turn = 'white'
        self.all_piece_placed = self.init_board()
        self.piece_in_movement = None
        self.possible_case = []
        self.possible_case_color = []

    def update(self, screen):
        for element in self.possible_case_color:
            pygame.draw.rect(screen, (83, 193, 239), element)

        for element in self.all_piece_placed:
            screen.blit(element.image, element.image_position)

        if self.piece_in_movement is not None:
            pos_mouse = pygame.mouse.get_pos()
            piece_placement = pos_mouse[0] - self.case_size / 2, pos_mouse[1] - self.case_size / 2
            self.piece_in_movement.image_position = piece_placement

        self.blit_death(screen)

    def blit_death(self, screen):
        x, y = 2, 2
        for element in self.white_death:
            element.image = pygame.transform.scale(element.image, (20, 20))
            screen.blit(element.image, (x, y))
            x += 10
        x, y = 2, 578
        for element in self.black_death:
            element.image = pygame.transform.scale(element.image, (20, 20))
            screen.blit(element.image, (x, y))
            x += 10

    def all_possible_case(self):
        for i in range(8):
            for j in range(8):
                test = self.piece_in_movement.test_possible_move((j, i))
                if test:
                    self.possible_case.append((j, i))
        for element in self.all_piece_placed:
            if element.position in self.possible_case:
                if element.color == self.piece_in_movement.color:
                    self.possible_case.remove(element.position)

    def generate_blue_cases(self):
        for element in self.possible_case:
            case = pygame.rect.Rect(element[0]*75+4, element[1]*75+4, 67, 67)
            self.possible_case_color.append(case)

    def pick(self, case_size):
        if self.piece_in_movement is None:

            pos_mouse = pygame.mouse.get_pos()
            pos_mouse = int(pos_mouse[0] / case_size), int(pos_mouse[1] / case_size)

            for element in self.all_piece_placed:

                if element.position == pos_mouse and element.color == self.turn:
                    self.piece_in_movement = element
                    self.all_piece_placed.remove(element)
                    self.all_piece_placed.append(self.piece_in_movement)
                    break

    def drop(self, case_size):
        pos_mouse = pygame.mouse.get_pos()  # game fonction
        pos_mouse = int(pos_mouse[0] / case_size), int(pos_mouse[1] / case_size)
        if pos_mouse in self.possible_case:
            for element in self.all_piece_placed:
                if element.position == pos_mouse:
                    if element.color == 'black':
                        self.sort_black(element)
                    else:
                        self.sort_white(element)
                    self.all_piece_placed.remove(element)
            self.piece_in_movement.x, self.piece_in_movement.y = pos_mouse
            self.piece_in_movement.image_position = self.piece_in_movement.x * 75, self.piece_in_movement.y * 75
            self.piece_in_movement.position = self.piece_in_movement.x, self.piece_in_movement.y
            print(self.piece_in_movement.name, self.piece_in_movement.position)
            self.roque()
            self.piece_in_movement.first_move = False
            self.change_turn()

        else:
            self.piece_in_movement.image_position = self.piece_in_movement.x*75, self.piece_in_movement.y*75
        self.piece_in_movement = None
        self.possible_case = []
        self.possible_case_color = []

    def change_turn(self):
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'

    def sort_white(self, piece):
        if not self.white_death:
            self.white_death.append(piece)
        else:
            for i in range(0, len(self.white_death)):
                if piece.value >= self.white_death[i].value:
                    self.white_death.insert(i, piece)
                    break

    def sort_black(self, piece):
        if not self.black_death:
            self.black_death.append(piece)
        else:
            for i in range(0, len(self.black_death)):
                if piece.value >= self.black_death[i].value:
                    self.black_death.insert(i, piece)
                    break

    def roque(self):
        if self.piece_in_movement.name == 'KING':
            if self.piece_in_movement.first_move:
                obstacle, tower = False, None
                if self.piece_in_movement.position == (6, 0):
                    for element in self.all_piece_placed:
                        if element.name == 'ROOK' and element.position == (7, 0) and element.first_move:
                            element.position = (5, 0)
                            element.x = element.position[0]
                            element.y = element.position[1]
                            element.image_position = (element.position[0] * 75, element.position[1] * 75)

                elif self.piece_in_movement.position == (2, 0):
                    for element in self.all_piece_placed:
                        if element.name == 'ROOK' and element.position == (0, 0) and element.first_move:
                            tower = element
                        elif element.position == (1, 0):
                            obstacle = True
                            break
                    if not obstacle and tower is not None:
                        tower.position = (3, 0)
                        tower.x = tower.position[0]
                        tower.y = tower.position[1]
                        tower.image_position = (tower.position[0] * 75, tower.position[1] * 75)

                elif self.piece_in_movement.position == (6, 7):
                    for element in self.all_piece_placed:
                        if element.name == 'ROOK' and element.position == (7, 7) and element.first_move:
                            element.position = (5, 7)
                            element.x = element.position[0]
                            element.y = element.position[1]
                            element.image_position = (element.position[0]*75, element.position[1]*75)

                elif self.piece_in_movement.position == (2, 7):
                    for element in self.all_piece_placed:
                        if element.name == 'ROOK' and element.position == (0, 7) and element.first_move:
                            element.position = (3, 7)
                            element.x = element.position[0]
                            element.y = element.position[1]
                            element.image_position = (element.position[0] * 75, element.position[1] * 75)

    def init_board(self):
        board = []

        white_king = King('white', 4, 7, self)
        black_king = King('black', 4, 0, self)
        board.append(white_king)
        board.append(black_king)

        white_queen = Queen('white', 3, 7, self)
        black_queen = Queen('black', 3, 0, self)
        board.append(white_queen)
        board.append(black_queen)
        for i in range(2):
            white_knight = Knight('white', 1+5*i, 7, self)
            black_knight = Knight('black', 1+5*i, 0, self)
            board.append(white_knight)
            board.append(black_knight)

        for i in range(2):
            white_tower = Rook('white', 0+i*7, 7, self)
            board.append(white_tower)
            black_tower = Rook('black', 0+i*7, 0, self)
            board.append(black_tower)

        for i in range(2):
            white_foul = Bishop('white', 2+3*i, 7, self)
            black_foul = Bishop('black', 2+3*i, 0, self)
            board.append(white_foul)
            board.append(black_foul)

        for i in range(8):
            white_pawn = Pawn('white', i, 6, self)
            black_pawn = Pawn('black', i, 1, self)
            board.append(white_pawn)
            board.append(black_pawn)
        return board
