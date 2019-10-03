import numpy as np
class SnakeGame:
    '''
    [head position, ..., body position, ..., tail position]
    direction => 0=up, 1=left, 2=down, 3=right
    board map => 0=empty place, 1=snake body, 2=snake head, 3=food
    initialize the snake at the top left corner with right moving direction
    '''
    def __init__(self, shape=[10,10]):
        self.board = np.zeros(shape, dtype=int)
        self.snake = [[0,1],[0,0]]
        self.snake_direction = 3
        self.score = 0
        self.food_position = None
        self.reset_board()
        self.generate_food()

    def reset_board(self):
        for cube in self.snake:
            row = cube[0]
            col = cube[1]
            if cube == self.snake[0]:
                # draw head as 2, body as 1
                self.board[row][col] = 2
            else:
                self.board[row][col] = 1

    def move_snake(self):
        head_row = self.snake[0][0]
        head_col = self.snake[0][1]
        tail_row = self.snake[-1][0]
        tail_col = self.snake[-1][1]
        to_row = head_row
        to_col = head_col
        if self.snake_direction == 0:
            # move up
            to_row -= 1
        elif self.snake_direction == 1:
            # move left
            to_col -= 1
        elif self.snake_direction == 2:
            # move down
            to_row +=1
        else:
            # move right
            to_col +=1

        if to_row not in range(0,self.board.shape[0]) or to_col not in range(0,self.board.shape[1]) or self.board[to_row, to_col] == 1:
            # hit the body or border, lost.
            return False

        if self.board[to_row, to_col] == 3: # in case snake got food
            self.snake = [[to_row, to_col]] + self.snake
            self.generate_food()
            self.score += 5

        else: # moving to empty space
            self.board[tail_row][tail_col] = 0
            self.snake = [[to_row, to_col]] + self.snake[:-1]

        self.board[head_row][head_col] = 1
        self.board[to_row][to_col] = 2
        return True


    def generate_food(self):
        row, col = np.random.randint(self.board.shape[0], size=2)
        while self.board[row][col]: # keep random rolling until an 0 cell is found
            row, col = np.random.randint(self.board.shape[0], size=2)
        self.board[row][col] = 3
        self.food_position = [row,col]

    def print_board(self):
        print(self.board)

    def fake_move_snake(self, dir):
        head_row = self.snake[0][0]
        head_col = self.snake[0][1]
        to_row = head_row
        to_col = head_col
        if dir == 0:
            # move up
            to_row -= 1
        elif dir == 1:
            # move left
            to_col -= 1
        elif dir == 2:
            # move down
            to_row +=1
        else:
            # move right
            to_col +=1
        dist = self.fake_distance_from_food(to_row, to_col)
        if to_row not in range(0,self.board.shape[0]) or to_col not in range(0,self.board.shape[1]) or self.board[to_row, to_col] == 1:
            return 0, dist
        return 1, dist

    def fake_distance_from_food(self, row, col):
        return abs(row - self.food_position[0]) + abs(col - self.food_position[1])

    def distance_from_food(self):
        return abs(self.snake[0][0] - self.food_position[0]) + abs(self.snake[0][1] - self.food_position[1])


    def calc_open_area(self, dir):
        board = self.board.copy()
        to_row = self.snake[0][0]
        to_col = self.snake[0][1]
        if dir == 0:
            to_row -= 1
        elif dir == 1:
            to_col -= 1
        elif dir == 2:
            to_row += 1
        else:
            to_col += 1

        return self.calc_rec_area(board, to_row, to_col)

    def calc_rec_area(self, board, row, col):
        if row not in range(board.shape[0]) or col not in range(board.shape[1]):
            return 0
        if board[row][col] and board[row][col] != 3:
            return 0
        board[row][col] = 1
        left = self.calc_rec_area(board, row, col-1)
        right = self.calc_rec_area(board, row, col+1)
        up = self.calc_rec_area(board,row-1, col)
        down = self.calc_rec_area(board, row+1, col)
        return 1+left+right+up+down




if __name__ == '__main__':
    s = SnakeGame([10,10])
    to_row = s.snake[0][0] + 1
    to_col = s.snake[0][1]
    print(SnakeGame.calc_open_area(s.board.copy(), [to_row, to_col]))
