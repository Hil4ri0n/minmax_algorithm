import math
import copy

class MinMaxAgent:
    def __init__(self, my_token='o', depth=4, use_heuristic=True):
        self.my_token = my_token
        self.opponent_token = 'x' if my_token == 'o' else 'o'
        self.depth = depth
        self.use_heuristic = use_heuristic

    def decide(self, connect4):
        _, best_move = self.minimax(connect4, self.depth, True)
        return best_move

    def minimax(self, connect4, depth, maximizingPlayer):
        if connect4.game_over:
            if connect4.wins == self.my_token:
                return 1, None
            elif connect4.wins == self.opponent_token:
                return -1, None
            elif connect4.wins is None:
                return 0, None
        if depth == 0:
            if self.use_heuristic:
                return self.heuristic(connect4), None
            else:
                return 0, None

        possible_moves = connect4.possible_drops()
        best_move = possible_moves[0]

        if maximizingPlayer:
            max_eval = -math.inf
            for move in possible_moves:
                connect4_copy = copy.deepcopy(connect4)
                connect4_copy.drop_token(move)
                eval, _ = self.minimax(connect4_copy, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in possible_moves:
                connect4_copy = copy.deepcopy(connect4)
                connect4_copy.drop_token(move)
                eval, _ = self.minimax(connect4_copy, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

    def heuristic(self, connect4):
        score = 0

        center_array = [row[len(row) // 2] for row in connect4.board]
        center_count = center_array.count(self.my_token)
        score += center_count * 0.3

        for window in connect4.iter_fours():
            score += self.evaluate_four(window)

        """if score/30 > 1 or score/30 < -1:
            print(score/30)"""
        return score / 40

    def evaluate_four(self, window):
        score = 0
        if window.count(self.my_token) == 3 and window.count('_') == 1:
            score += 5
        elif window.count(self.my_token) == 2 and window.count('_') == 2:
            score += 2
        if window.count(self.opponent_token) == 3 and window.count('_') == 1:
            score -= 4
        elif window.count(self.opponent_token) == 2 and window.count('_') == 2:
            score -= 2

        return score
