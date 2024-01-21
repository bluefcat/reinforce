import numpy as np
import os
from agent import QAgent, RAgent, Player, Env
from tqdm import tqdm

import random
import copy
def main():
    env = Env([])

    Aagent = QAgent("a", env)
    Bagent = QAgent("b", env)

    env.players = [Aagent, Bagent]

    fields = [[[1, 1, 1], [0, 0, 0], [0, 0, 0]],
              [[0, 0, 0], [1, 1, 1], [0, 0, 0]],
              [[0, 0, 0], [0, 0, 0], [1, 1, 1]],
              [[1, 0, 0], [1, 0, 0], [1, 0, 0]],
              [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
              [[0, 0, 1], [0, 0, 1], [0, 0, 1]],
              [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
              [[0, 0, 1], [0, 1, 0], [1, 0, 0]],
              ] 
    #111 111 11
    for field in fields:
        env.field = np.array(field)
        print(env.check(), end="")
    print()

    win_rate = [0, 0, 0]

    for _ in tqdm(range(500000)):
        done = False
        env.reset()
        prev = env.h
        action = None
        while not done:
            for player in env.players:
                prev = env.h
                action = player.select_action(env.h)
                h, r, done = env.step(player, action)
                if done:
                    break
                player.update_table((prev, action, -1, env.h))

        if env.winner != 0:
            if env.winner == -1:
                win_rate[0] += 1
            else:
                idx = int(env.winner)
                
                if env.players[idx-1] == Aagent:
                    win_rate[1] += 1

                else:
                    win_rate[2] += 1

            for i, player in enumerate(env.players):
                r = 100
                if env.winner != i-1:
                    r = -100

                player.update_table((prev, action, r, env.h))

        Aagent.anneal_eps()
        Bagent.anneal_eps()

        if _ % 10000 == 0:
            
            if win_rate[1] < win_rate[2]:
                Aagent.q_table = copy.deepcopy(Bagent.q_table)

            if random.random() < 0.5:
                Bagent = QAgent(f"r{_}", env)
            else:
                Bagent = QAgent(f"b{_}", env)

            win_rate = [0, 0, 0]

    print(win_rate)
    if win_rate[1] < win_rate[2]:
        Aagent.q_table = copy.deepcopy(Bagent.q_table)

    random_ = RAgent("r", env)
    env.players = [random_, Aagent]

    win_rate = [0, 0, 0]
    

    for _ in tqdm(range(10000)):
        done = False
        env.reset()
        prev = env.h
        action = None
        while not done:
            for player in env.players:
                prev = env.h
                action = player.select_action(env.h)
                _, r, done = env.step(player, action)
                if done:
                    break
                player.update_table((prev, action, -1, env.h))

        if env.winner != 0:
            if env.winner == -1:
                win_rate[0] += 1
            else:
                idx = int(env.winner)
                
                if env.players[idx-1] == random_:
                    win_rate[1] += 1

                else:
                    win_rate[2] += 1

            for i, player in enumerate(env.players):
                r = 100
                if env.winner != i-1:
                    r = -100

                player.update_table((prev, action, r, env.h))

        Aagent.anneal_eps()
        Bagent.anneal_eps()
    
    print(win_rate)
    input()
    player_ = Player("p", env)
    env.players = [player_, Aagent]

    for _ in range(100):
        print(_)
        done = False
        env.reset()
        prev = env.h
        action = None
        while not done:
            for player in env.players:
                prev = env.h
                action = player.select_action(env.h)
                _, r, done = env.step(player, action)
                if done:
                    break
                player.update_table((prev, action, -1, env.h))
                os.system('cls')
                env.print()
                print("+------------------+")


        if env.winner != 0:
            for i, player in enumerate(env.players):
                r = 50
                if env.winner != i-1:
                    r = -50

                player.update_table((prev, action, r, env.h))
        
        #for aa, bb in Aagent.q_table.items():
        #    print(f"{aa}: {bb}")
        os.system('cls')
if __name__ == "__main__":
    main()