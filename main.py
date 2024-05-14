import pygame
import networkx as nx
import matplotlib.pyplot as plt

# Inicializar o pygame
pygame.init()

# Definir algumas constantes
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
CELL_SIZE = 100
GRID_ROWS, GRID_COLS = 6, 6

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
YELLOW = 'yellow'
RED = 'red'
GREEN = 'green'
BLUE = 'blue'
DARK_GRAY = (50, 50, 50)

# Configuração da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man com A* e NetworkX")

# Fonte para mensagens
font = pygame.font.Font(None, 36)

# Representação do tabuleiro
board = [
    [0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 0, 0]
]

# Função heurística: distância de Manhattan
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Criar o grafo a partir do tabuleiro
def create_graph_from_board(board):
    G = nx.grid_2d_graph(len(board), len(board[0]))
    walls = [(r, c) for r in range(len(board)) for c in range(len(board[0])) if board[r][c] == 1]
    G.remove_nodes_from(walls)
    return G

# Função do algoritmo A* usando networkx
def a_star_search(G, start, end):
    try:
        return nx.astar_path(G, start, end, heuristic=heuristic)
    except nx.NetworkXNoPath:
        return None

# Função para desenhar o tabuleiro e o caminho
def draw_board(screen, board, path, start, end, no_path_msg):
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            color = WHITE
            if board[row][col] == 1:
                color = BLACK
            pygame.draw.rect(screen, color, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLUE, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    if path:
        for (row, col) in path:
            pygame.draw.rect(screen, YELLOW, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    if start:
        pygame.draw.rect(screen, RED, pygame.Rect(start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    if end:
        pygame.draw.rect(screen, GREEN, pygame.Rect(end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    if no_path_msg:
        msg_surface = font.render(no_path_msg, True, (255, 0, 0))
        screen.blit(msg_surface, (SCREEN_WIDTH // 2 - msg_surface.get_width() // 2, SCREEN_HEIGHT // 2 - msg_surface.get_height() // 2))

def draw_buttons(screen):
    reset_button = pygame.Rect(10, SCREEN_HEIGHT - 50, 100, 40)
    pygame.draw.rect(screen, GRAY, reset_button)
    reset_text = font.render('Reset', True, BLACK)
    screen.blit(reset_text, (reset_button.x + 10, reset_button.y + 5))
    return reset_button

# Função para desenhar o grafo usando matplotlib
def draw_graph(G, path, start, end):
    pos = {(x, y): (y, -x) for x, y in G.nodes()}
    plt.figure(figsize=(8, 8))
    nx.draw(G, pos, node_size=300, node_color="white", edge_color="gray", with_labels=False)

    # Desenhar o caminho
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color=YELLOW, node_size=300)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color=YELLOW, width=2)

    # Desenhar os nós de início e fim
    nx.draw_networkx_nodes(G, pos, nodelist=[start], node_color=RED, node_size=300)
    nx.draw_networkx_nodes(G, pos, nodelist=[end], node_color=GREEN, node_size=300)

    plt.title("Grafo do Tabuleiro")
    plt.show()

# Função principal
def main():
    clock = pygame.time.Clock()
    G = create_graph_from_board(board)
    start = None
    end = None
    path = None
    running = True
    show_graph = False
    no_path_msg = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if y > SCREEN_HEIGHT - 50 and x < 110:
                    start = None
                    end = None
                    path = None
                    no_path_msg = None
                else:
                    row, col = y // CELL_SIZE, x // CELL_SIZE
                    if start is None:
                        start = (row, col)
                    elif end is None:
                        end = (row, col)
                        path = a_star_search(G, start, end)
                        if path is None:
                            no_path_msg = "No path available"
                        else:
                            no_path_msg = None
                        show_graph = True

        screen.fill(DARK_GRAY)
        draw_board(screen, board, path, start, end, no_path_msg)
        reset_button = draw_buttons(screen)
        pygame.display.flip()
        clock.tick(60)

        if show_graph:
            draw_graph(G, path, start, end)
            show_graph = False

    pygame.quit()

if __name__ == "__main__":
    main()
