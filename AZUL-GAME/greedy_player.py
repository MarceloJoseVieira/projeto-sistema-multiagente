from model import Player, Move, TileGrab
from utils import SameTG


class GreedyPlayer(Player):
    def __init__(self, _id):
        super().__init__(_id)

    # EXECUÇÃO DO ALGORITMO GREEDY
    def SelectMove(self, moves, game_state):
        best_move = None
        largest_pattern_tiles = -1 
        least_floor_tiles = float('inf')

        for move in moves:
            tile_grab = move[2]
            
            current_pattern_tiles = tile_grab.num_to_pattern_line
            current_floor_tiles = tile_grab.num_to_floor_line
            
            # Heurística 1: Maximizar o número de peças na linha de padrão
            if current_pattern_tiles > largest_pattern_tiles:
                largest_pattern_tiles = current_pattern_tiles
                least_floor_tiles = current_floor_tiles
                best_move = move
            
            # Heurística 2: Se o número de peças na linha de padrão for o mesmo,
            # minimizar o número de peças que vão para o chão.
            elif current_pattern_tiles == largest_pattern_tiles:
                if current_floor_tiles < least_floor_tiles:
                    least_floor_tiles = current_floor_tiles
                    best_move = move
            if best_move is None and moves:
                best_move = moves[0]

        return best_move