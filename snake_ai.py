import pygame
from snake_game import SnakeGame
import os
import numpy as np
import pickle
from genetic_algorithm import Ai, get_fitness_key

def calc_fitness(genome, game):
    actions = possible_actions(game)
    direction = genome.activate(actions) # index of the choosen actions which sorted by direction
    old_dist = game.distance_from_food()
    old_snake_size = len(game.snake)
    game.snake_direction = direction
    if not game.move_snake():
        genome.fitness -= 15
        return False
    if len(game.snake) > old_snake_size:
        genome.fitness += 1
    else:
        if old_dist > game.distance_from_food():
            genome.fitness += .1
        else:
            genome.fitness -= .15
    return True

def possible_actions(game):
    actions = []
    for dir in range(4):
        # if dir == (game.snake_direction + 2)%4:
        #     continue
        alive, dist = game.fake_move_snake(dir)
        open_area = game.calc_open_area(dir)
        snake_len = len(game.snake)
        actions.append([alive,dist,open_area,snake_len])
    return actions

def draw(win, board, fitness, speed):
    width = int(WIN_WIDTH*.7/len(board))
    height = int(WIN_HEIGHT/len(board))
    win.fill(BLACK)
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            rect = (j*width, i*height, width-5, height-5)
            if cell == 1 or cell == 2:
                pygame.draw.rect(win,GREEN,rect)
            if cell == 3:
                pygame.draw.rect(win,RED,rect)
    rect = (WIN_WIDTH*.7, 0, WIN_WIDTH*.3, WIN_HEIGHT)
    pygame.draw.rect(win,(0,0,0),rect)
    text_fitness = FONT.render(f"fitness: {fitness}", 1, (255, 255, 255))
    win.blit(text_fitness, (WIN_WIDTH - 10 - text_fitness.get_width(), 10))
    text_speed = FONT.render(f"Speed: {speed}", 1, (255, 255, 255))
    win.blit(text_speed, (WIN_WIDTH - 10 - text_speed.get_width(), 60 ))
    pygame.display.update()


def eval_genome(genome, speed = 0):
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Snake V3')
    game = SnakeGame([10,10])
    flag = True
    pause = False
    while flag:
        clock.tick(speed)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
            	pygame.quit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    speed += 5
                elif e.key == pygame.K_DOWN:
                    speed -= 5
                elif e.key == 112:
                    pause = not pause

        if not pause:
            flag = calc_fitness(genome, game)
            draw(win, game.board, round(genome.fitness, 3), speed)
            if genome.fitness < -10:
                flag = False

def winner_play(net, speed = 10):
    genome = net.elites[0]
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((400, 400))
    pygame.display.set_caption('Snake AI')
    game = SnakeGame([10,10])
    flag = True
    pause = False
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
            flag = calc_fitness(genome, game)
            if genome.fitness < -10:
                flag = False

if __name__ == '__main__':
    image_index = 1
    WIN_WIDTH = 1000
    WIN_HEIGHT = 600
    RED = (255, 0, 0)
    GREEN = (6, 108, 115)
    BLACK = (30,30,30)
    pygame.font.init()
    FONT = pygame.font.SysFont('rockwell', 40)
    winner_file_path = 'snake_my_net_winner.pickle'
    if os.path.isfile(winner_file_path):
        with open(winner_file_path, "rb") as handle:
            net = pickle.load(handle)
            winner_play(net, 10)
    else:
        ai = Ai(population=1000, input_size=(3,4))
        net = ai.run(eval_genome, 100)
        with open('snake_my_net_winner.pickle', 'wb') as handle:
            net.winners = sorted(net.winners, key=get_fitness_key, reverse=True)
            pickle.dump(net, handle, protocol=pickle.HIGHEST_PROTOCOL)
