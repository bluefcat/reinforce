"""
environment 
"""
from collections import Counter

import random
import numpy as np

class Agent:
    """
    agent
    """
    def __init__(self, id, env):
        self.id = id
        self.env = env

    def select_action(self, state):
        """
        select action in possible
        """

    def update_table(self, transition):
        """
        update q table
        """

    def anneal_eps(self):
        """
        anneal_eps
        """

    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id

class Env:
    """
    environment
    """
    def __init__(self, players: list[Agent]):
        self.size = (3, 3)
        self.in_row = 3
        self.players = players

        self.field = np.zeros(self.size)
        self.h = 0
        self.turn = 0
        random.shuffle(self.players)
        self.winner = 0

    def reset(self):
        """
        reset env
        """
        self.field = np.zeros(self.size)
        self.h = 0
        self.turn = 0
        random.shuffle(self.players)

        self.winner = 0

    def print(self):
        for row in self.field:
            print(row)
        
        print()

    def candidate(self):
        """
        can move candidate
        """
        width, height = self.size

        return [(i, j)
                for i in range(width) for j in range(height)
                if self.field[i][j] == 0]

    def step(self, player: Agent, action: tuple[int, int]):
        """
        gaming
        """
        x, y = action
        self.field[x][y] = 1 + self.players.index(player)
        self.winner = self.check()
        reward = (-1, -1)

        if self.winner != 0:
            reward = (10, 10)

        self.h = ""

        for _, row in enumerate(self.field):
            for _, x in enumerate(row):
                self.h += f"{int(x)}"

        return self.h, reward, self.winner != 0

    def check(self):
        """
        winner checking
        """
        width, height = self.size

        #check horizon line
        for row in self.field:
            for x, count in Counter(row).items():
                if x != 0 and count == self.in_row:
                    return x

        #check vertical line
        for col in self.field.T:
            for x, count in Counter(col).items():
                if x != 0 and count == self.in_row:
                    return x

        #check diagonal line
        target = self.field[0][0]
        if target != 0 and all([
            target == self.field[i][i] for i in range(width)
        ]):
            return target

        target = self.field[0][height-1]
        if target != 0 and all([
            target == self.field[i][height - (1+i)]
            for i in range(height)
        ]):
            return target
        if len(np.nonzero(self.field)[0]) == width * height:
            return -1
        return 0
