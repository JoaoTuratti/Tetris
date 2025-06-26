import pygame
import random

# Configurações
grid_width = 10
grid_height = 20
block_size = 30
preview_width = 6  # em blocos para painel de próximas peças

screen_width = grid_width * block_size + preview_width * block_size
screen_height = grid_height * block_size + 100  # espaço extra para pontuação

# Cores
gray = (128, 128, 128)
black = (0, 0, 0)
white = (255, 255, 255)
colors = [
    (0, 240, 240),  # I
    (0, 0, 240),    # J
    (240, 160, 0),  # L
    (240, 240, 0),  # O
    (0, 240, 0),    # S
    (160, 0, 240),  # T
    (240, 0, 0)     # Z
]

# Formatos das peças
tetrominoes = {
    'I': [[1, 1, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'Z': [[1, 1, 0], [0, 1, 1]]
}

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.rotation = 0

    def image(self):
        return self.shape[self.rotation % len(self.shape)]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)


def create_grid(locked_positions={}):
    grid = [[black for _ in range(grid_width)] for _ in range(grid_height)]
    for (x, y), color in locked_positions.items():
        if y >= 0:
            grid[y][x] = color
    return grid


def convert_shape_format(piece):
    positions = []
    for i, line in enumerate(piece.image()):
        for j, col in enumerate(line):
            if col:
                positions.append((piece.x + j, piece.y + i))
    return positions


def valid_space(piece, grid):
    allowed = [(x, y) for y in range(grid_height) for x in range(grid_width) if grid[y][x] == black]
    for pos in convert_shape_format(piece):
        if pos not in allowed and pos[1] > -1:
            return False
    return True


def check_lost(locked):
    return any(y < 1 for (_, y) in locked)


def get_shape():
    key = random.choice(list(tetrominoes.keys()))
    rotations = []
    mat = tetrominoes[key]
    for _ in range(4):
        rotations.append(mat)
        mat = [list(row) for row in zip(*mat[::-1])]
    piece = Piece(grid_width // 2 - len(rotations[0][0]) // 2, -2, rotations)
    color = colors[list(tetrominoes.keys()).index(key)]
    return piece, color


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, True, color)
    surface.blit(label, ((screen_width - label.get_width()) // 2,
                         (screen_height - label.get_height()) // 2))


def detect_full_rows(grid):
    return [i for i, row in enumerate(grid) if black not in row]


def remove_rows(locked, rows):
    for row in rows:
        for x in range(grid_width):
            locked.pop((x, row), None)
    # Ajusta de cima para baixo
    for (x, y) in sorted(list(locked), key=lambda k: k[1], reverse=True):
        shift = sum(1 for r in rows if y < r)
        if shift > 0:
            color = locked.pop((x, y))
            locked[(x, y + shift)] = color


def flash_rows(surface, grid, rows, flash_times=6, delay=100):
    for i in range(flash_times):
        for y in rows:
            for x in range(grid_width):
                grid[y][x] = random.choice(colors) if i % 2 == 0 else black
        draw_window(surface, grid)
        pygame.display.update()
        pygame.time.delay(delay)


def draw_grid(surface, grid):
    for y in range(grid_height):
        for x in range(grid_width):
            pygame.draw.rect(surface, grid[y][x],
                             (x * block_size, y * block_size, block_size, block_size), 0)
    for y in range(grid_height):
        pygame.draw.line(surface, gray, (0, y * block_size), (grid_width * block_size, y * block_size))
    for x in range(grid_width):
        pygame.draw.line(surface, gray, (x * block_size, 0), (x * block_size, grid_height * block_size))


def draw_next_pieces(surface, pieces):
    font = pygame.font.SysFont('comicsans', 25)
    label = font.render('Próximas:', True, white)
    x_off = grid_width * block_size + 10
    y_off = 20
    surface.blit(label, (x_off, y_off))
    for idx, (piece, color) in enumerate(pieces):
        format = piece.shape[0]
        for i, line in enumerate(format):
            for j, col in enumerate(line):
                if col:
                    pygame.draw.rect(surface, color,
                                     (x_off + j * block_size,
                                      y_off + 30 + idx * 4 * block_size + i * block_size,
                                      block_size, block_size), 0)


def draw_window(surface, grid, score=0, next_pieces=None):
    surface.fill(black)
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render(f'Pontuação: {score}', True, white)
    surface.blit(label, (10, screen_height - 80))
    draw_grid(surface, grid)
    pygame.draw.rect(surface, white, (0, 0, grid_width * block_size, grid_height * block_size), 5)
    if next_pieces:
        draw_next_pieces(surface, next_pieces)


def main():
    pygame.init()
    win = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Tetris')
    clock = pygame.time.Clock()

    locked = {}
    current_piece, current_color = get_shape()
    next_pieces = [get_shape() for _ in range(4)]
    fall_time = 0
    level_time = 0
    horizontal_time = 0
    soft_time = 0
    fall_speed = 0.5
    horizontal_speed = 0.1  # segundos por passo lateral
    soft_speed = 0.05      # segundos por passo de queda rápida
    score = 0
    speed_increment_score = 1000
    next_speed_threshold = speed_increment_score
    min_fall_speed = 0.1

    run = True
    while run:
        grid = create_grid(locked)
        dt = clock.get_rawtime()
        fall_time += dt
        level_time += dt
        horizontal_time += dt
        soft_time += dt
        clock.tick()

        keys = pygame.key.get_pressed()
        # soft drop
        if keys[pygame.K_DOWN] and soft_time / 1000 >= soft_speed:
            soft_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
        # continuous horizontal
        if keys[pygame.K_LEFT] and horizontal_time / 1000 >= horizontal_speed:
            horizontal_time = 0
            current_piece.x -= 1
            if not valid_space(current_piece, grid):
                current_piece.x += 1
        elif keys[pygame.K_RIGHT] and horizontal_time / 1000 >= horizontal_speed:
            horizontal_time = 0
            current_piece.x += 1
            if not valid_space(current_piece, grid):
                current_piece.x -= 1

        # level up by time
        if level_time / 1000 > 60:
            level_time = 0
            fall_speed = max(min_fall_speed, fall_speed - 0.005)

        # auto fall
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                locked.update({pos: current_color for pos in convert_shape_format(current_piece)})
                grid = create_grid(locked)
                full_rows = detect_full_rows(grid)
                if full_rows:
                    flash_rows(win, grid, full_rows)
                    remove_rows(locked, full_rows)
                    # score update
                    cleared = len(full_rows)
                    score += cleared ** 2 * 100
                    # speed increment by score
                    if score >= next_speed_threshold:
                        fall_speed = max(min_fall_speed, fall_speed - 0.1)
                        next_speed_threshold += speed_increment_score
                current_piece, current_color = next_pieces.pop(0)
                next_pieces.append(get_shape())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        current_piece.rotate()

        # desenhar peça atual
        for pos in convert_shape_format(current_piece):
            x, y = pos
            if y > -1:
                grid[y][x] = current_color

        draw_window(win, grid, score, next_pieces)
        pygame.display.update()

        if check_lost(locked):
            draw_text_middle(win, 'GAME OVER', 60, white)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False

    pygame.quit()

if __name__ == '__main__':
    main()
