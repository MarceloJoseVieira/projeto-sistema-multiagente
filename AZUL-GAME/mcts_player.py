from model import *
from utils import *
import copy
import math
import random


SIMULATION_COUNT = 300
C_PARAM = 1.0


class MCTSNode:
    def __init__(self, game_state, player_id_to_move, parent=None, move=None, move_player=None):
        self.game_state = game_state
        self.player_id_to_move = player_id_to_move
        self.parent = parent
        self.move = move
        self.move_player = move_player
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = []

    def uct_value(self, total_parent_visits):
        if self.visits == 0:
            return math.inf
        exploitation_term = self.wins / self.visits
        exploration_term = C_PARAM * math.sqrt(math.log(total_parent_visits) / self.visits)
        return exploitation_term + exploration_term

    def select_child(self):
        inf_children = [c for c in self.children if c.visits == 0]
        if inf_children:
            return random.choice(inf_children)
        best_child = max(self.children, key=lambda child: child.uct_value(self.visits))
        return best_child

    def expand(self, move, next_state, next_player_id, move_player):
        child = MCTSNode(game_state=next_state, player_id_to_move=next_player_id, parent=self, move=move, move_player=move_player)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        if result > 0:
            self.wins += 1
        elif result < 0:
            self.wins -= 1

class MCTSPlayer(Player):
    def __init__(self, _id):
        super().__init__(_id)

    def _heuristic_rollout_policy(self, moves, game_state, player_id):
        best_move = None
        best_score = -math.inf
        player_state = game_state.players[player_id]
        opponent_id = (player_id + 1) % len(game_state.players)

        for move in moves:
            score = 0
            try:
                tgrab = move[2]
            except Exception:
                tgrab = None

            if tgrab and getattr(tgrab, 'num_to_pattern_line', 0) > 0:
                line_idx = tgrab.pattern_line_dest
                if player_state.lines_number[line_idx] + tgrab.num_to_pattern_line == line_idx + 1:
                    score += 500

            if tgrab:
                score -= getattr(tgrab, 'num_to_floor_line', 0) * 10

            if tgrab:
                score += getattr(tgrab, 'num_to_pattern_line', 0) * 2

            try:
                if move[0] == Move.TAKE_FROM_FACTORY:
                    factory_id = move[1]
                    factory = game_state.factories[factory_id]
                    remaining_tiles = getattr(factory, 'total', 0) - (tgrab.number if tgrab and hasattr(tgrab, 'number') else 0)
                    if remaining_tiles > 3:
                        score -= remaining_tiles * 1
            except Exception:
                pass

            if score > best_score:
                best_score = score
                best_move = move

        return best_move if best_move is not None else random.choice(moves)

    # EXECUÇÃO DO ALGORITMO MCTS
    def SelectMove(self, moves, game_state):
        root = MCTSNode(game_state=game_state, player_id_to_move=self.id, move_player=None)
        root.untried_moves = copy.deepcopy(moves)

        num_players = len(game_state.players)

        for _ in range(SIMULATION_COUNT):
            node = root

            # SELEÇÃO
            while node.untried_moves == [] and node.children != []:
                node = node.select_child()

            # EXPANSÃO
            if node.untried_moves != []:
                if not node.game_state.TilesRemaining():
                    pass
                else:
                    move = random.choice(node.untried_moves)
                    node.untried_moves.remove(move)

                    next_state = copy.deepcopy(node.game_state)

                    current_player_id = node.player_id_to_move
                    try:
                        returned = next_state.ExecuteMove(current_player_id, move)
                        if isinstance(returned, int):
                            next_player_id = returned
                        else:
                            next_player_id = getattr(next_state, 'current_player_id', (current_player_id + 1) % num_players)
                    except Exception:
                        next_player_id = getattr(next_state, 'current_player_id', (current_player_id + 1) % num_players)

                    child = node.expand(move, next_state, next_player_id, move_player=current_player_id)

                    try:
                        child.untried_moves = copy.deepcopy(next_state.players[next_player_id].GetAvailableMoves(next_state))
                    except Exception:
                        child.untried_moves = []

                    node = child

            # SIMULAÇÃO
            playout_state = copy.deepcopy(node.game_state)
            playout_player_id = node.player_id_to_move

            while playout_state.TilesRemaining():
                current_player_state = playout_state.players[playout_player_id]
                try:
                    avail_moves = current_player_state.GetAvailableMoves(playout_state)
                except Exception:
                    avail_moves = []

                if not avail_moves:
                    break

                move = self._heuristic_rollout_policy(avail_moves, playout_state, playout_player_id)

                try:
                    playout_state.ExecuteMove(playout_player_id, move)
                except Exception:
                    break

                playout_player_id = getattr(playout_state, 'current_player_id', (playout_player_id + 1) % num_players)

            initial_scores = [p.score for p in playout_state.players]
            try:
                playout_state.ExecuteEndOfRound()
            except Exception:
                pass

            mcts_player_score_after = playout_state.players[self.id].score
            opponent_id = (self.id + 1) % num_players
            opponent_score_after = playout_state.players[opponent_id].score

            mcts_player_score_before = initial_scores[self.id]
            opponent_score_before = initial_scores[opponent_id]

            result = (mcts_player_score_after - mcts_player_score_before) - (opponent_score_after - opponent_score_before)

            # RETROPROPAGAÇÃO
            while node is not None:
                mover = node.move_player
                if mover is None or mover == self.id:
                    node.update(result)
                else:
                    node.update(-result)
                node = node.parent

        if not root.children:
            return random.choice(moves)

        best_child = max(root.children, key=lambda child: child.visits)
        return best_child.move
