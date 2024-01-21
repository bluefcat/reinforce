"""
Agent
"""
import random
from env import Agent, Env

class QAgent(Agent):
    """
    auto agent
    """
    def __init__(self, id: str, env: Env):
        super().__init__(id, env)

        self.eps = 0.9
        self.q_table: dict = {}

    def select_action(self, state):
        actionable = self.env.candidate()

        strategy = self.q_table.get(state, {})
        actions = list(set(actionable) & set(strategy.keys()))

        if not actions or random.random() < self.eps:
            try:
                return random.choice(actionable)
            except IndexError:
                print(self.env.print())
                print(actionable)
                raise IndexError
        return max(actions, key= lambda x: strategy[x])

    def update_table(self, transition):
        s, a, r, ns = transition

        pv = self.q_table.get(s, {})
        npv = self.q_table.get(ns, {0:0})
        m = max(npv.values())

        pv[a] = pv.get(a, 0) + 0.1 * (r + m - pv.get(a, 0))
        self.q_table[s] = pv

    def anneal_eps(self):
        """
        a
        """
        self.eps = max(self.eps - 0.00001, 0.1)

class Player(Agent):
    """
    player
    """
    def __init__(self, id: str, env):
        super().__init__(id, env)

    def select_action(self, state):
        x, y = map(int, input(">").split())
        while (x, y) not in self.env.candidate():
            x, y = map(int, input(">").split())
        return (x, y)

    def update_table(self, transition):
        return
    
class RAgent(Agent):
    """
    player
    """
    def __init__(self, id: str, env):
        super().__init__(id, env)

    def select_action(self, state):
        return random.choice(self.env.candidate())

    def update_table(self, transition):
        return

