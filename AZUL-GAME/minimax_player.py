from model import *
from utils import *
import copy
import math


SEARCH_DEPTH = 2

class MinimaxPlayer(Player):
    def __init__(self, _id):
        super().__init__(_id)

    # EXECUÇÃO DO ALGORITMO MINIMAX
    def SelectMove(self, moves, game_state):
        
        best_score = -math.inf
        best_move = None
        
        for move in moves:
            simulated_game_state = copy.deepcopy(game_state)
            
            simulated_game_state.ExecuteMove(self.id, move)
            
            next_player_id = (self.id + 1) % len(simulated_game_state.players)
            
            score = self._minimax(simulated_game_state, SEARCH_DEPTH - 1, next_player_id, False)
            
            if score > best_score:
                best_score = score
                best_move = move
            
        if best_move is None and moves:
            return random.choice(moves)
            
        return best_move

    def _minimax(self, game_state, depth, current_player_id, is_maximizing_player):
        if depth == 0 or not game_state.TilesRemaining():
            return self._evaluate_state(game_state, self.id)

        current_player_state = game_state.players[current_player_id]
        moves = current_player_state.GetAvailableMoves(game_state)
        
        if not moves:
            return self._evaluate_state(game_state, self.id)

        next_player_id = (current_player_id + 1) % len(game_state.players)

        if is_maximizing_player:
            max_eval = -math.inf
            for move in moves:
                simulated_game_state = copy.deepcopy(game_state)
                simulated_game_state.ExecuteMove(current_player_id, move)
                
                eval = self._minimax(simulated_game_state, depth - 1, next_player_id, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for move in moves:
                simulated_game_state = copy.deepcopy(game_state)
                simulated_game_state.ExecuteMove(current_player_id, move)
                
                eval = self._minimax(simulated_game_state, depth - 1, next_player_id, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def _evaluate_state(self, game_state, player_id):        
        player_state = game_state.players[player_id]
        opponent_id = (player_id + 1) % len(game_state.players)
        opponent_state = game_state.players[opponent_id]
        
        score_diff = player_state.score - opponent_state.score
        
        pattern_line_progress = 0
        for i in range(player_state.GRID_SIZE):
            progress = player_state.lines_number[i] / (i + 1)
            pattern_line_progress += progress
        
        floor_penalty = 0
        for i in range(len(player_state.floor)):
            if player_state.floor[i] == 1:
                floor_penalty += player_state.FLOOR_SCORES[i]
        
        W_SCORE = 100
        W_PROGRESS = 10
        W_FLOOR = 1
        
        evaluation = (W_SCORE * score_diff) + \
                     (W_PROGRESS * pattern_line_progress) + \
                     (W_FLOOR * floor_penalty)
                     
        return evaluation