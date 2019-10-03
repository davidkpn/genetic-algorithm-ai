import pygame
from tetris_game import TetrisGame
import os
import numpy as np
import pickle
from genetic_algorithm import Ai, get_fitness_key


################################################################################
# User
################################################################################
def draw(win, board, score, shape, speed):
    width = int(WIN_WIDTH*.66/len(board[0]))
    height = int(WIN_HEIGHT/len(board))
    win.fill(BLACK)
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            rect = (j*width, i*height, width-5, height-5)
            if cell > 0:
                pygame.draw.rect(win,COLORS[cell-1],rect)
    rect = (WIN_WIDTH*.66, 0, WIN_WIDTH*.333, WIN_HEIGHT)
    pygame.draw.rect(win,(0,0,0),rect)
    text_score = FONT.render(f"Score: {score}", 1, (255, 255, 255))
    win.blit(text_score, (WIN_WIDTH - 20 - text_score.get_width(), 10))
    text_next_shape = FONT.render(f"next shape:", 1, (255, 255, 255))
    win.blit(text_next_shape, (WIN_WIDTH - 10 - text_next_shape.get_width(), text_score.get_height() + 15))
    text_speed = FONT.render(f"speed:{speed}", 1, (255, 255, 255))
    win.blit(text_speed, (WIN_WIDTH - 10 - text_speed.get_width(), WIN_HEIGHT - text_speed.get_height() ))

    start_width = WIN_WIDTH*.7
    start_height = text_score.get_height() + text_next_shape.get_height() + 35
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            rect = (start_width + j*width, start_height + i*height, width-5, height-5)
            if cell > 0:
                pygame.draw.rect(win,COLORS[cell-1],rect)

    pygame.display.update()

def lose_draw(win, score):
    win.fill(BLACK)
    text_lose = FONT.render(f"You've lost with score: {score}", 1, (230, 235, 230))
    text_restart = FONT.render("Press 'R' to restart the game", 1, (230, 235, 230))
    center_x = round((WIN_WIDTH - text_lose.get_width())/2)
    center_y = round((WIN_HEIGHT - text_lose.get_height())/2)
    win.blit(text_lose, (center_x, center_y - 10))

    win.blit(text_restart, (center_x - 20, center_y + text_lose.get_height() + 10))
    pygame.display.update()

def play(speed=3):
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Tetris Human')
    game = TetrisGame()
    flag = True
    lose_flag = True
    pause = False
    while flag:
        actions = [2]
        clock.tick(speed)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
            	pygame.quit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    actions.append(0)
                if e.key == pygame.K_DOWN:
                    actions.append(2)
                if e.key == pygame.K_LEFT:
                    actions.append(1)
                if e.key == pygame.K_RIGHT:
                    actions.append(3)
                if e.key == 112:
                    pause = not pause
                    print(get_all_possible_moves(game))
                if e.key == 45:
                    speed-=1
                if e.key == 61:
                    speed+=1
        draw(win, game.board, game.score, game.next_shape['shape'], speed)
        if not pause:
            flag, moved, cleared_rows = game.move_shape(actions)

    while lose_flag:
        lose_draw(win, game.score)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
            	pygame.quit()
            elif e.type == pygame.KEYDOWN:
                if e.key == 114:
                    play()
                if e.key == 27:
                	pygame.quit()

################################################################################
# AI handle
################################################################################
def get_all_possible_moves(game):
    last_state = game.get_state()
    possible_moves = []
    for rotations in range(4):
        for t in range(-5,6):
            game.load_state(last_state)
            dx = [t / abs(t) + 2] if t != 0 else []
            actions = [0]*rotations + dx*abs(t)
            alive, moved, cleared_rows = game.move_shape(actions)
            if moved: # if the shape has moved at all
                alive , moved, cleared_rows = game.move_shape([2])
                while moved:
                    alive , moved, cleared_rows = game.move_shape([2])
                action = {
                    'rotations': rotations,
                    'translation': t,
                    'weights': [1 if alive else 0, cleared_rows, pow(game.get_height(), 1.5), game.get_cumulative_height(), game.get_relative_height(), game.get_holes(), game.get_roughness()]
                }
                possible_moves.append(action)
    game.load_state(last_state)
    return possible_moves

def calc_fitness(genome, game, taken_moves):
    max_moves = 500
    moves = get_all_possible_moves(game)
    actions = [move['weights'] for move in moves]
    if actions:
        output = genome.activate(actions) # index of the choosen actions which sorted by direction
    else:
        genome.fitness = genome.fitness - max_moves + taken_moves + game.score
        return False
    t = moves[output]['translation']
    dx = [t / abs(t) + 2] if t != 0 else []
    shape_actions = [0] * moves[output]['rotations'] + dx * abs(t)
    alive, moved, cleared_rows = game.move_shape(shape_actions)
    if alive:
        alive, moved, cleared_rows= game.move_shape([2])
        while moved:
            alive, moved, cleared_rows = game.move_shape([2])
    if not alive:
        genome.fitness = genome.fitness - max_moves + taken_moves + game.score
        return False
    if taken_moves > max_moves:
        genome.fitness += game.score
        return False
    return True


def eval_genome(genome, speed = 0):
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Tetris AI')
    game = TetrisGame()
    # game.reset_board()
    flag = True
    pause = False
    taken_moves = 0
    while flag:
        clock.tick(speed)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
            	pygame.quit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    speed += 5
                if e.key == pygame.K_DOWN:
                    speed -= 5
                if e.key == 112:
                    pause = not pause

        if not pause:
            taken_moves+=1
            flag = calc_fitness(genome, game, taken_moves)
            draw(win, game.board, round(genome.fitness, 3), game.next_shape['shape'], speed)

if __name__ == '__main__':
    WIN_WIDTH = 600
    WIN_HEIGHT = 800
    RED = (255, 0, 0)
    GREEN = (6, 108, 115)
    BLACK = (30,30,30)
    COLORS = [(249, 35, 56), (201, 115, 255), (28, 118, 188), (254, 227, 86), (83, 213, 4), (54, 224, 255), (248, 147, 29)];
    pygame.font.init()
    FONT = pygame.font.SysFont('rockwell', 30)

    #play()
    ai = Ai(population=700, input_size=(50,7))
    net = ai.run(eval_genome, 40)
    with open('tetris_my_net_winner.pickle', 'wb') as handle:
        net.winners = sorted(net.winners, key=get_fitness_key, reverse=True)
        pickle.dump(net, handle, protocol=pickle.HIGHEST_PROTOCOL)
