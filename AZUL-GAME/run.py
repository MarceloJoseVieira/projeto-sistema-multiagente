# Written by Michelle Blom, 2019
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
from model import GameRunner,Player
from iplayer import InteractivePlayer
from minimax_player import MinimaxPlayer
from mcts_player import MCTSPlayer
from greedy_player import GreedyPlayer
from utils import *


# SELEÇÃO DE CONFRONTO ENTRE AGENTES
players = [GreedyPlayer(0), MinimaxPlayer(1)]
#players = [GreedyPlayer(0), MCTSPlayer(1)]
#players = [MinimaxPlayer(0), MCTSPlayer(1)]


# CONFIGURAÇÃO DA SIMULAÇÃO EM X PARTIDAS
numero_de_partidas = 10
vitorias = {player.id: 0 for player in players}

print(f"--- Iniciando simulação de {numero_de_partidas} partidas ---")

# LOOP DE EXECUÇÃO
for i in range(numero_de_partidas):
    gr = GameRunner(players, None)

    resultado = gr.Run(False) 
    
    scores = {}
    for pid, dados in resultado.items():
        pontuacao_final = dados[0]
        scores[pid] = pontuacao_final

    vencedor_id = max(scores, key=scores.get)
    
    vitorias[vencedor_id] += 1

    if (i + 1) % 1 == 0:
        print(".", end="", flush=True)

# EXIBIÇÃO DOS RESULTADOS
print("\n")
for pid in vitorias:
    nome_algoritmo = type(players[pid]).__name__
    total_vitorias = vitorias[pid]
    porcentagem = (total_vitorias / numero_de_partidas) * 100
    
    print(f"Jogador {pid} [{nome_algoritmo}]: {total_vitorias} vitórias ({porcentagem:.1f}%)")

'''

#CONFIGURAÇÃO DA SIMULAÇÃO AGENTE VS AGENTE INTERATIVO
gr = GameRunner(players, None)

activity = gr.Run(True)

print("Player 0 score is {}".format(activity[0][0]))
print("Player 1 score is {}".format(activity[1][0]))
'''