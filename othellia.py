import numpy as np
from collections import defaultdict
from main import *

class ReversIA():
    def __init__(self, state, parent=None, parent_action=None):
        self.state = Reversi()
        self.state.tablero = state.copy()
        self.state.turno = 1
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[ 1] = self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return
    
    def untried_actions(self):
        self._untried_actions = self.state.obtener_jugadas_validas()
        return self._untried_actions
    
    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits
    
    def expand(self):
        action = self._untried_actions.pop()
        self.state.realizar_jugada(*action)
        next_state = self.state
        child_node = ReversIA(next_state.tablero, parent=self, parent_action=action)
        self.children.append(child_node)
        return child_node 
    
    def is_terminal_node(self):
        return self.state.is_game_over()
    
    def rollout(self):
        current_rollout_state = self.state
    
        while not current_rollout_state.is_game_over():           
            possible_moves = current_rollout_state.obtener_jugadas_validas()
            action = self.rollout_policy(possible_moves)
            current_rollout_state.realizar_jugada(*action)
            current_rollout_state = self.state
        return current_rollout_state.game_result()

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)
    
    def is_fully_expanded(self):
        return len(self._untried_actions) == 0
    
    def best_child(self, c_param=0.1):
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():
            
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = 100
        
        for i in range(simulation_no):
            
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        
        return self.best_child(c_param=0.)


def main():
    raiz = tk.Tk()

    def task():
        if interfaz.juego.turno == 1:
            othellia.best_action().state.mostrar_tablero()
        raiz.after(2000, task)

    interfaz = InterfazReversi(raiz)
    othellia = ReversIA(state= interfaz.juego.tablero)
    raiz.after(2000, task)
    raiz.mainloop()
    return

main()