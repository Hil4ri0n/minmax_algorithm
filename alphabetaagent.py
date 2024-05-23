import copy
import math
from exceptions import AgentException
from minmaxagent import MinMaxAgent


class AlphaBetaAgent(MinMaxAgent):
    def __init__(self, my_token='o', depth=4):
        super().__init__(my_token, depth)

    def decide(self, connect4):
        _, best_move = self.alphabeta(connect4, self.depth, -math.inf, math.inf, True)
        return best_move

    def alphabeta(self, connect4, depth, alpha, beta, maximizingPlayer):
        if connect4.game_over:
            if connect4.wins == self.my_token:
                return 1, None
            elif connect4.wins == self.opponent_token:
                return -1, None
            elif connect4.wins is None:
                return 0, None
        if depth == 0:
            return self.heuristic(connect4), None

        possible_moves = connect4.possible_drops()
        best_move = possible_moves[0]

        if maximizingPlayer:
            value = -math.inf
            for move in possible_moves:
                connect4_copy = copy.deepcopy(connect4)
                connect4_copy.drop_token(move)
                eval, _ = self.alphabeta(connect4_copy, depth-1, alpha, beta, False)
                if eval > value:
                    value = eval
                    best_move = move
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, best_move
        else:
            value = math.inf
            for move in possible_moves:
                connect4_copy = copy.deepcopy(connect4)
                connect4_copy.drop_token(move)
                eval, _ = self.alphabeta(connect4_copy, depth-1, alpha, beta, True)
                if eval < value:
                    value = eval
                    best_move = move
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value, best_move
