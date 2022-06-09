import hardest_game
import random


def play_game_AI(str, map_name='map1.txt'):
    game = hardest_game.Game(map_name=map_name, game_type='AI').run_AI_moves_graphic(moves=str)
    return game


def simulate(str, map_name='map1.txt'):
    game = hardest_game.Game(map_name=map_name, game_type='AI').run_AI_moves_no_graphic(moves=str)
    return game


def run_whole_generation(list_of_strs, N, map_name='map1.txt'):
    game = hardest_game.Game(map_name=map_name, game_type='AIS').run_generation(list_of_moves=list_of_strs, move_len=N)
    return game


def play_human_mode(map_name='map1.txt'):
    hardest_game.Game(map_name=map_name, game_type='player').run_player_mode()


def genetic():
    population = [""] * 1000
    fitness = [0] * 1000
    keywords = ['w', 's', 'a', 'd', 'x']
    for i in range(1000):
        string_run = ""
        for j in range(50):
            random_num = random.randint(0, 4)
            string_run += keywords[random_num]
        population[i] = string_run
    counter = 0
    len_str = 50
    for k in range(10000):
        counter += 1
        game = run_whole_generation(population, len_str, 'map1.txt')
        players = game.players
        goals = game.goal_player
        sum_fit = 0
        new_population = [0] * 1000
        chance_player = [0] * 1000
        for i in range(1000):
            fitness[i] = fitness_cal(players[i], goals, i, game.end, game.start, game.enemies, game.player_x,
                                     game.player_y, game.Vlines, game.Hlines)
            sum_fit += fitness[i]
            if fitness[i] == 100000000:
                return population[i]
        fitness, population = sort(fitness, population)
        print(fitness[0])
        for i in range(1, 1000):
            chance_player[i] = (fitness[i] / sum_fit) + chance_player[i - 1]
        for i in range(1000):
            num = random.random()
            gen = 999
            for j in range(999):
                if chance_player[j] < num < chance_player[j + 1]:
                    gen = j
                    break
            new_population[i] = population[gen]
        for i in range(250, 500):
            j = i * 2
            k = i * 2 + 1
            cut = int(random.random() * len_str)
            data = new_population[j]
            data2 = new_population[k]
            population[j] = data[0: cut] + data2[cut: len_str]
            population[k] = data2[0: cut] + data2[cut: len_str]
        for i in range(500, 1000):
            if random.random() > 0.4:
                for j in range(len_str // 30):
                    x = random.randint(0, len_str)
                    population[i] = population[i][0:x] + keywords[random.randint(0, 4)] + population[i][x + 1:len_str]
        if counter == 4:
            keywords = ['w', 's', 'a', 'd', 'x']
            for i in range(1000):
                string_run = ""
                for j in range(50):
                    random_num = random.randint(0, 4)
                    string_run += keywords[random_num]
                population[i] += string_run
            counter = 0
            len_str += 50


def sort(fitness, population):
    for i in range(len(fitness)):
        for j in range(len(fitness) - 1):
            if fitness[j] < fitness[j + 1]:
                fitness[j], fitness[j + 1] = fitness[j + 1], fitness[j]
                population[j], population[j + 1] = population[j + 1], population[j]
    return [fitness, population]


def fitness_cal(player, goals, k, end, start, enemy, player_x, player_y, vil, hli):
    if player[2]:
        return 100000000
    fitness = 0
    for i in range(len(goals)):
        if goals[i][k]:
            fitness += 240
    if abs(start.x - end.x) > abs(start.y - end.y):
        fitness += (1 / (1 + (end.x - player[0].x))) * (end.x * 40)
    else:
        fitness += (1 / (1 + (end.y - player[0].y))) * (end.y * 20)
    if player[1] == -1 and (
            player[0].x > start.w + start.x or player[0].y > start.h + start.y or player[0].y < start.y or player[
        0].x < start.x):
        fitness += 15
    for i in range(len(enemy)):
        if (((enemy[i].x - 3 * enemy[i].r < player[0].x < enemy[i].x + 3 * enemy[i].r) and (
                enemy[i].y - 3 * enemy[i].r < player[0].y < enemy[i].y + 3 * enemy[i].r)) and (
                    player[0].x > start.w + start.x or player[0].y > start.h + start.y or player[0].y < start.y or
                    player[
                        0].x < start.x)) and player[1] == -1:
            fitness += 35
            break
    if player[0].x > start.w + start.x or player[0].y > start.h + start.y or player[0].y < start.y or player[
        0].x < start.x:
        fitness += abs(player[0].x - player_x) + abs(player[0].y - player_y) + 10
    for v in vil:
        if ((end.x + end.w > v.x1 > start.x + start.w or end.x + end.w < v.x1 < start.x + start.w) and player[
            0].y > v.y2 and player[0].y < v.y1 and player[0].x - player[0].width < v.x1 < player[0].x + player[
                0].width) or player[0].x > v.x1:
            fitness += 5
    for h in hli:
        if ((end.y + end.h > h.y1 > start.y + start.h or end.y + end.h < h.y1 < start.y + start.h) and v.y2 < player[
            0].y < h.y1 and player[0].y - player[0].width < h.y1 < player[0].y + player[
                0].width) or player[0].y > h.y1:
            fitness += 5
    return fitness


genetic()
