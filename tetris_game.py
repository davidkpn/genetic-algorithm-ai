import numpy as np
class TetrisGame:
    shapes = [
    [[0,0,0,0], [1,1,1,1], [0,0,0,0], [0,0,0,0]], # I
    [[2,0,0], [2,2,2], [0,0,0]],                  # J
    [[0,0,3], [3,3,3], [0,0,0]],                  # L
    [[4,4], [4,4]],                               # O
    [[0,5,5], [5,5,0], [0,0,0]],                  # S
    [[0,6,0], [6,6,6], [0,0,0]],                  # T
    [[7,7,0], [0,7,7], [0,0,0]]                   # Z
    ]
    def __init__(self, shape=[20,10]):
        self.board = np.zeros(shape, dtype=int)
        self.score = 0
        self.current_shape = self.generate_shape()
        self.next_shape = self.generate_shape()
        self.apply_shape()

    def reset_board(self):
        self.board = np.zeros(self.board.shape, dtype=int)
        self.current_shape = self.generate_shape()
        self.next_shape =self.generate_shape()
        self.score = 0
        self.apply_shape()

    def generate_next(self):
        self.current_shape = self.next_shape
        if self.collide(2)[0]:
            #print(f"You've lost, your score is: {self.score}")
            return False
        self.next_shape = self.generate_shape()
        return True

    def generate_shape(self):
        shape_index = np.random.randint(len(TetrisGame.shapes))
        shape = TetrisGame.shapes[shape_index]
        x = round((len(self.board[0]) - len(shape[0]))/2)
        y = 0
        return {'shape': shape, 'x': x, 'y': y}

    def move_shape(self, actions):
        alive = True
        cleared_rows = 0
        moved = False
        for action in actions:
            collide, moved = self.collide(action)
            if collide:
                cleared_rows = self.clear_rows()
                alive = self.generate_next()
        return alive, moved, cleared_rows

    def remove_shape(self):
        for i, row in enumerate(self.current_shape['shape']):
            for j, cell in enumerate(row):
                if cell:
                    x = self.current_shape['x'] + j
                    y = self.current_shape['y'] + i
                    self.board[y][x] = 0

    def apply_shape(self):
        for i, row in enumerate(self.current_shape['shape']):
            for j, cell in enumerate(row):
                if cell:
                    x = self.current_shape['x'] + j
                    y = self.current_shape['y'] + i
                    self.board[y][x] = cell

    def collide(self, action):
        self.remove_shape()
        copied_shape = self.current_shape.copy()
        if action == 0:#rotate
            copied_shape['shape'] = np.rot90(copied_shape['shape'],1)
        elif action == 1:#left
            copied_shape['x'] -= 1
        elif action == 2:#down
            copied_shape['y'] += 1
        elif action == 3:#right
            copied_shape['x'] += 1

        for i, row in enumerate(copied_shape['shape']):
            for j, cell in enumerate(row):
                if cell:
                    x = copied_shape['x'] + j
                    y = copied_shape['y'] + i
                    if x not in range(0, len(self.board[0])):
                        self.apply_shape()
                        return False, False
                    if y not in range(0, len(self.board)) or self.board[y][x]:
                        self.apply_shape()
                        return action==2, False

        self.current_shape = copied_shape
        self.apply_shape()
        return False, True

    def clear_rows(self):
        rows_to_clear = []
        for i, row in enumerate(self.board):
            no_empty_space = True
            for cell in row:
                if not cell:
                    no_empty_space = False
                    break
            if no_empty_space:
                rows_to_clear.append(i)


        for i, row in enumerate(rows_to_clear):
            self.score += 400 + i**2 * 400
            zerow = np.zeros([1, self.board.shape[1]], dtype=int)
            bottom = self.board[row+1:]
            top = self.board[:row]
            if row + 1 < self.board.shape[0]:
                self.board = np.concatenate((zerow, top, bottom), axis=0)
            else:
                self.board = np.concatenate((zerow, top), axis=0)
        return len(rows_to_clear)

    def print_board(self):
        print(self.board)


    def get_cumulative_height(self):
        self.remove_shape()
        peaks = [self.board.shape[1]]*self.board.shape[0]
        total_height = 0
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell and peaks[j] == self.board.shape[1]:
                    peaks[j] = i
                    total_height += 20-i
        self.apply_shape()
        return total_height

    def get_relative_height(self):
        self.remove_shape()
        peaks = [self.board.shape[1]]*self.board.shape[0]
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell and peaks[j] == self.board.shape[1]:
                    peaks[j] = i
        relative_height = max(peaks) - min(peaks)
        self.apply_shape()
        return relative_height

    def get_holes(self):
        self.remove_shape()
        peaks = [self.board.shape[1]]*self.board.shape[0]
        holes = 0
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell and peaks[j] == self.board.shape[1]:
                    peaks[j] = i
                elif not cell and peaks[j] < self.board.shape[1]:
                    holes += 1

        self.apply_shape()
        return holes

    def get_roughness(self):
        self.remove_shape()
        peaks = [self.board.shape[1]]*self.board.shape[0]
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell and peaks[j] == self.board.shape[1]:
                    peaks[j] = i
        roughness = 0
        i = 0
        while i < len(peaks)-1:
            roughness += abs(peaks[i] - peaks[i+1])
            i+=1
        self.apply_shape()
        return roughness

    def get_height(self):
        self.remove_shape()
        peaks = [self.board.shape[1]]*self.board.shape[0]
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell and peaks[j] == self.board.shape[1]:
                    peaks[j] = i
        return 20 - min(peaks)

    def get_state(self):
        state = {
            'board': self.board.copy(),
            'current_shape': self.current_shape.copy(),
            'next_shape': self.next_shape.copy(),
            'score': self.score
        }
        return state

    def load_state(self, state):
        #print(state['board'])
        self.board = state['board'].copy()
        self.current_shape = state['current_shape'].copy()
        self.next_shape = state['next_shape'].copy()
        self.score = state['score']




if __name__ == '__main__':
    t = TetrisGame([20,10])
