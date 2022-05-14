from operator import xor

import pygame


class King:
    def __init__(self, color, x, y, game):
        """x, y compris entre 0 et 7"""
        self.game = game
        self.name = 'KING'
        self.image = pygame.image.load(f"assets/pieces/{color}_king.png")
        self.color = color
        self.image_position = (x*75, y*75)
        self.x = x
        self.y = y
        self.first_move = True
        self.position = (x, y)
        self.value = 15

    def test_possible_move(self, case):
        """case = tuple of coord
        test: check all case where coord = +-1 (x/y/xy)
        """
        if case[0] == self.x or case[0] == self.x + 1 or case[0] == self.x - 1:
            if case[1] == self.y or case[1] == self.y+1 or case[1] == self.y - 1:

                return True
        elif self.first_move and case[1] == self.y:
            if case[0] - 2 == self.x or case[0] + 2 == self.x:
                if self.test_obstacle(case):
                    return True

        return False

    def test_obstacle(self, case):
        x = 0
        compteur = 0
        if case[0] > self.x:
            x = -1
        elif case[0] < self.x:
            x = 1

        while case != self.position:
            for element in self.game.all_piece_placed:
                if element.position == case:
                    if self.color == 'white':
                        if element.color == 'white':
                            return False
                        else:
                            if compteur != 0:
                                return False
                    else:
                        if element.color == 'black':
                            return False
                        else:
                            if compteur != 0:
                                return False
            case = case[0] + x, case[1]
            compteur += 1
        return True

class Pawn:
    def __init__(self, color, x, y, game):
        self.name = 'PAWN'
        self.game = game
        self.image = pygame.image.load(f"assets/pieces/{color}_pawn.png")
        self.color = color
        self.image_position = (x * 75, y * 75)
        self.x = x
        self.y = y
        self.first_move = True
        self.position = (x, y)
        self.value = 1

    def test_possible_move(self, case):
        if self.color == 'white':
            if self.y == 6 and case[0] == self.x and self.test_obstacle(first=True):
                if case[1] == self.y-1 or case[1] == self.y-2:
                    return True
            elif case[1] == self.y-1 and case[0] == self.x and self.test_obstacle():
                return True
            elif case[0] == self.x + 1 or case[0] == self.x - 1:
                if case[1] == self.y - 1:
                    for element in self.game.all_piece_placed:
                        if element.position == case:
                            if element.color == 'black':
                                return True
                return False
            else:
                return False
        else:
            if self.color == 'black':
                if self.y == 1 and case[0] == self.x and self.test_obstacle(first=True):
                    if case[1] == self.y + 1 or case[1] == self.y + 2:
                        return True
                elif case[1] == self.y + 1 and case[0] == self.x and self.test_obstacle():
                    return True
                elif case[0] == self.x + 1 or case[0] == self.x - 1:
                    if case[1] == self.y + 1:
                        for element in self.game.all_piece_placed:
                            if element.position == case:
                                if element.color == 'white':
                                    return True
                    return False
                else:
                    return False

    def test_obstacle(self, first=False):
        for element in self.game.all_piece_placed:
            if self.color == 'black':
                if element.position == (self.x, self.y + 1):
                    return False
                elif first and element.position == (self.x, self.y + 2):
                    return False
            else:
                if element.position == (self.x, self.y - 1):
                    return False
                elif first and element.position == (self.x, self.y - 2):
                    return False
        return True


class Bishop:
    def __init__(self, color, x, y, game):
        self.name = 'BISHOP'
        self.game = game
        self.image = pygame.image.load(f"assets/pieces/{color}_foul.png")
        self.color = color
        self.image_position = (x * 75, y * 75)
        self.x = x
        self.y = y
        self.first_move = True
        self.position = (x, y)
        self.value = 3

    def test_possible_move(self, case):
        if self.x - self.y == case[0] - case[1] or (7-self.x)-self.y == 7 - case[0]-case[1]:
            if self.test_obstacle(case):
                return True
        return False

    def test_obstacle(self, case):
        x, y = 1, 1
        compteur = 0
        if case[0] > self.x:
            x = -1
        if case[1] > self.y:
            y = -1

        while case != self.position:
            for element in self.game.all_piece_placed:
                if element.position == case:
                    if self.color == 'white':
                        if element.color == 'white':
                            return False
                        else:
                            if compteur != 0:
                                return False
                    else:
                        if element.color == 'black':
                            return False
                        else:
                            if compteur != 0:
                                return False
            case = case[0] + x, case[1] + y
            compteur += 1
        return True


class Rook:
    def __init__(self, color, x, y, game):
        self.name = 'ROOK'
        self.game = game
        self.image = pygame.image.load(f"assets/pieces/{color}_tower.png")
        self.color = color
        self.image_position = (x * 75, y * 75)
        self.x = x
        self.y = y
        self.first_move = True
        self.position = (x, y)
        self.value = 5

    def test_possible_move(self, case):
        if xor(self.x == case[0], self.y == case[1]):
            if self.test_obstacle(case):
                return True
        return False

    def test_obstacle(self, case):
        x, y = 0, 0
        compteur = 0
        if case[0] > self.x:
            x = -1
        elif case[0] < self.x:
            x = 1
        elif case[1] > self.y:
            y = -1
        elif case[1] < self.y:
            y = 1

        while case != self.position:
            for element in self.game.all_piece_placed:
                if element.position == case:
                    if self.color == 'white':
                        if element.color == 'white':
                            return False
                        else:
                            if compteur != 0:
                                return False
                    else:
                        if element.color == 'black':
                            return False
                        else:
                            if compteur != 0:
                                return False
            case = case[0] + x, case[1] + y
            compteur += 1
        return True


class Knight:
    def __init__(self, color, x, y, game):
        self.name = 'KNIGHT'
        self.game = game
        self.image = pygame.image.load(f"assets/pieces/{color}_knight.png")
        self.color = color
        self.image_position = (x * 75, y * 75)
        self.x = x
        self.y = y
        self.first_move = True
        self.position = (x, y)
        self.value = 3.5

    def test_possible_move(self, case):
        if abs(self.x-case[0])+abs(self.y-case[1]) == 3 and self.x-case[0] != 0 and self.y-case[1] != 0:
            return True
        return False


class Queen:
    def __init__(self, color, x, y, game):
        self.name = 'QUEEN'
        self.game = game
        self.image = pygame.image.load(f"assets/pieces/{color}_queen.png")
        self.color = color
        self.image_position = (x * 75, y * 75)
        self.x = x
        self.y = y
        self.first_move = True
        self.position = (x, y)
        self.value = 9

    def test_possible_move(self, case):
        if xor(self.x == case[0], self.y == case[1]):
            if self.test_obstacle_rook(case):
                return True
        elif self.x - self.y == case[0] - case[1] or (7-self.x)-self.y == 7 - case[0]-case[1]:
            if self.test_obstacle_bishop(case):
                return True

        return False

    def test_obstacle_rook(self, case):
        x, y = 0, 0
        compteur = 0
        if case[0] > self.x:
            x = -1
        elif case[0] < self.x:
            x = 1
        elif case[1] > self.y:
            y = -1
        elif case[1] < self.y:
            y = 1

        while case != self.position:
            for element in self.game.all_piece_placed:
                if element.position == case:
                    if self.color == 'white':
                        if element.color == 'white':
                            return False
                        else:
                            if compteur != 0:
                                return False
                    else:
                        if element.color == 'black':
                            return False
                        else:
                            if compteur != 0:
                                return False
            case = case[0] + x, case[1] + y
            compteur += 1
        return True

    def test_obstacle_bishop(self, case):
        x, y = 1, 1
        compteur = 0
        if case[0] > self.x:
            x = -1
        if case[1] > self.y:
            y = -1

        while case != self.position:
            for element in self.game.all_piece_placed:
                if element.position == case:
                    if self.color == 'white':
                        if element.color == 'white':
                            return False
                        else:
                            if compteur != 0:
                                return False
                    else:
                        if element.color == 'black':
                            return False
                        else:
                            if compteur != 0:
                                return False
            case = case[0] + x, case[1] + y
            compteur += 1
        return True
