
# SISTEMA MULTIAGENTE

**Disciplina:** Introdução à Inteligência Artificial  
**Semestre:** 2025.2  
**Professor:** André Luís Fonseca Faustino  
**Turma:** T03

## Integrantes do Grupo

- Marcelo José Vieira da Silva (20210052017)
- Matheus Rodrigues do Rego (20220005440)

## Descrição do Projeto

O projeto implementa uma simulação baseada em agentes para o jogo de tabuleiro Azul. Foram desenvolvidos diferentes agentes de IA utilizando estratégias distintas (Greedy, Minimax e Monte Carlo) que interagem em um ambiente adversário. A performance de cada agente foi validada através de uma análise comparativa de 100 partidas.

## Guia de Instalação e Execução

### 1. Instalação das Dependências

Certifique-se de ter o **Python 3.x** instalado. Clone o repositório:

```bash
# Clone o repositório
git clone https://github.com/MarceloJoseVieira/projeto-sistema-multiagente.git

# Entre na pasta do projeto
cd AZUL-GAME
```

### 2. Execução das simulações

```bash
# Digite no terminal
python3 run.py
```

### 3. Personalizando a Simulação

Para testar diferentes confrontos de IA ou alterar o número de partidas, você deve editar o arquivo run.py.

```bash
Descomente e comente as linhas para escolher quais jogadores de IA se enfrentarão.
# SELEÇÃO DE CONFRONTO ENTRE AGENTES
# players = [GreedyPlayer(0), MinimaxPlayer(1)]
players = [MinimaxPlayer(0), MCTSPlayer(1)] <--- Mude aqui
# players = [GreedyPlayer(0), MCTSPlayer(1)]

Altere o valor da variável numero_de_partidas para aumentar ou diminuir a amostra da simulação.
# CONFIGURAÇÃO DA SIMULAÇÃO EM X PARTIDAS
numero_de_partidas = 10 <--- Mude aqui para 100 partidas

Salve o arquivo run.py e execute-o novamente
```

## Estrutura dos Arquivos

A pasta principal AZUL-GAME, que contém o seguinte código-fonte do projeto:

- `model.py`: Contém a lógica central do jogo (regras, estado do tabuleiro, movimentos).
- `iplayer.py`: Define a interface base para todos os tipos de jogadores (agentes de IA).
- `greedy_player.py`: Implementação de uma estratégia de jogador ganancioso (simples).
- `minimax_player.py`: Implementação de uma estratégia de jogador baseada no algoritmo Minimax.
- `mcts_player.py`: Implementação de uma estratégia de jogador baseada em Monte Carlo Tree Search (MCTS).
- `run.py`: O ponto de entrada para executar o jogo ou simulações.
- `util.py`: Funções utilitárias e auxiliares usadas em todo o projeto.

## Resultados e Demonstração

[Adicione prints da aplicação em execução ou gráficos com os resultados do modelo/agente. Se for uma aplicação Web, coloque um print da interface.]

## Referências

- https://github.com/michelleblom/AZUL
- https://pt.boardgamearena.com/gamepanel?game=azul
