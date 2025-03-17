import heapq
import time
import tracemalloc
from collections import deque

#CLASSE NODE
class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.blank_pos = self.find_blank()

    #Encontrar o espaço vazio

    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return (i, j)
        return None

    #Descobrir quais movimentos são possíveis

    def get_possible_actions(self):
        i, j = self.blank_pos
        actions = []
        if i > 0:
            actions.append('cima') # se não estiver na 1ª linha pode subir
        if i < 2:
            actions.append('baixo') # se não estiver na última linha pode descer
        if j > 0:
            actions.append('esquerda') # se não estiver na 1ª coluna pode ir para a esquerda
        if j < 2:
            actions.append('direita') # se não estiver na última coluna pode ir para a direita
        return actions


    #Mover o espaço vazio

    def apply_action(self, action):
        i, j = self.blank_pos
        new_state = [row[:] for row in self.state] #Copia o tabuleiro atual
        if action == 'cima':
            new_state[i][j], new_state[i-1][j] = new_state[i-1][j], new_state[i][j] # Troca de posição

            '''temp = new_state[i][j]  # Guarda o valor da posição atual em uma variável temporária
                new_state[i][j] = new_state[i-1][j]  # Move o valor de cima para a posição atual
                new_state[i-1][j] = temp  # Coloca o valor original da posição atual na posição de cima'''
            
        elif action == 'baixo':
            new_state[i][j], new_state[i+1][j] = new_state[i+1][j], new_state[i][j]
        elif action == 'esquerda':
            new_state[i][j], new_state[i][j-1] = new_state[i][j-1], new_state[i][j]
        elif action == 'direita':
            new_state[i][j], new_state[i][j+1] = new_state[i][j+1], new_state[i][j]
        return new_state
    
    def __lt__(self, other):
        #Permite que os nós sejam comparados no heapq com base no cost.
        return self.cost < other.cost

#FUNÇÕES AUXILIARES

#Inserir tabuleiro inicial e final

def ler_config():
    print("Digite os números de 0 a 8 para representar o tabuleiro (0 é o espaço vazio).")
    tabuleiro = []
    for i in range(3):
        while True:
            try:
                linha = list(map(int, input(f"Linha {i+1}: ").split())) # Lê a linha do utilizador
                if len(linha) == 3 and all(0 <= n <= 8 for n in linha): # Verifica se input é válido
                    tabuleiro.append(linha)
                    break
                else:
                    print("Entrada inválida. Digite 3 números entre 0 e 8.")
            except ValueError:
                print("Entrada inválida. Digite 3 números separados por espaço.")
    return tabuleiro

def mostrar_tabuleiro(tabuleiro):
    for linha in tabuleiro:
        print(" ".join(str(n) if n != 0 else "_" for n in linha)) 
    print()

def contar_inversoes(arr):
    inversoes = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inversoes += 1
    return inversoes

def is_solvable(initial_state, goal_state):
    initial_flat = [num for row in initial_state for num in row if num != 0]
    goal_flat = [num for row in goal_state for num in row if num != 0]

    #O puzzle é solucionável se ambas as contagens de inversões forem pares ou ímpares
    return contar_inversoes(initial_flat) % 2 == contar_inversoes(goal_flat) % 2

#BFS
def bfs(initial_state, goal_state):
    if not is_solvable(initial_state, goal_state):
        return None

    if initial_state == goal_state:
        return Node(initial_state)

    fronteira = deque([Node(initial_state)])
    reached = {str(initial_state)}

    while fronteira:
        node = fronteira.popleft() #FIFO

        for action in node.get_possible_actions():
            new_state = node.apply_action(action)
            child = Node(new_state, node, action, node.cost + 1)

            if child.state == goal_state:
                return child

            if str(child.state) not in reached:
                reached.add(str(child.state))
                fronteira.append(child)

    return None

# A* 
def manhattan_distance(state, goal_state):
    distance = 0
    goal_positions = {goal_state[i][j]: (i, j) for i in range(3) for j in range(3)}
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x_goal, y_goal = goal_positions[state[i][j]]
                distance += abs(i - x_goal) + abs(j - y_goal)
    return distance

def hamming_distance(state, goal_state):
    return sum(1 for i in range(3) for j in range(3) if state[i][j] != 0 and state[i][j] != goal_state[i][j])

def a_star(initial_state, goal_state, heuristic=manhattan_distance):
    if not is_solvable(initial_state, goal_state):
        return None

    if initial_state == goal_state:
        return Node(initial_state)

    fronteira = []
    heapq.heappush(fronteira, (0, Node(initial_state)))
    reached = {str(initial_state): 0}

    while fronteira:
        _, node = heapq.heappop(fronteira)

        if node.state == goal_state:
            return node

        for action in node.get_possible_actions():
            new_state = node.apply_action(action)
            child = Node(new_state, node, action, node.cost + 1)
            cost = child.cost + heuristic(child.state, goal_state)

            if str(child.state) not in reached or child.cost < reached[str(child.state)]:
                reached[str(child.state)] = child.cost
                heapq.heappush(fronteira, (cost, child))

    return None

# ESTUDO DE CUSTO DE TEMPO E MEMÓRIA
def avaliar_algoritmo(algorithm, initial_state, goal_state, heuristic=None):
    tracemalloc.start()
    start_time = time.time()
    
    if heuristic:
        solution_node = algorithm(initial_state, goal_state, heuristic)
    else:
        solution_node = algorithm(initial_state, goal_state)
    
    end_time = time.time()
    memory_usage = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    
    if solution_node:
        path_length = 0
        while solution_node:
            path_length += 1
            solution_node = solution_node.parent
        path_length -= 1  # Desconta o nó inicial
    else:
        path_length = -1
    
    return path_length, end_time - start_time, memory_usage

# =================== EXECUÇÃO PRINCIPAL ===================
def main():
    print("=== Jogo dos 8 ===")
    print("Digite o estado inicial:")
    initial_state = ler_config()

    print("Digite o estado final:")
    goal_state = ler_config()

    if not is_solvable(initial_state, goal_state):
        print("Este puzzle não tem solução.")
        return

    print("Escolha o algoritmo: (1) BFS, (2) A*")
    choice = input("Opção: ")
    algorithm = bfs if choice == '1' else a_star

    if algorithm == a_star:
        print("Escolha a heurística: (1) Manhattan, (2) Hamming")
        heur_choice = input("Opção: ")
        heuristic = manhattan_distance if heur_choice == '1' else hamming_distance
        solution_node = algorithm(initial_state, goal_state, heuristic)
    else:
        solution_node = algorithm(initial_state, goal_state)

    if solution_node:
        path = []
        while solution_node:
            path.append(solution_node.state)
            solution_node = solution_node.parent

        path.reverse()
        print("Solução encontrada:")
    
    else:
        print("Não foi encontrada solução.")

    
    if algorithm == bfs:
        print("Avaliando BFS...")
        bfs_result = avaliar_algoritmo(bfs, initial_state, goal_state)
        print(f"Movimentos: {bfs_result[0]}, Tempo: {bfs_result[1]:.5f} seg, Memória: {bfs_result[2]} bytes")

    elif algorithm == a_star:
        if heuristic == manhattan_distance:
            print("\nAvaliando A* com Manhattan...")
            a_star_result = avaliar_algoritmo(a_star, initial_state, goal_state, manhattan_distance)
        else:
            print("\nAvaliando A* com Hamming...")
            a_star_result = avaliar_algoritmo(a_star, initial_state, goal_state, hamming_distance)

        print(f"Movimentos: {a_star_result[0]}, Tempo: {a_star_result[1]:.5f} seg, Memória: {a_star_result[2]} bytes")

if __name__ == "__main__":
    main()