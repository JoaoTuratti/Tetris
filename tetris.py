import pygame
import random

grid_width = 10
grid_height = 20
block_size = 30
preview_width = 6

screen_width = grid_width * block_size + preview_width * block_size + 200
screen_height = grid_height * block_size

gray = (128, 128, 128)
black = (0, 0, 0)
white = (255, 255, 255)
colors = [
    (0, 240, 240), (0, 0, 240), (240, 160, 0),
    (240, 240, 0), (0, 240, 0), (160, 0, 240), (240, 0, 0)
]
tetris_letters = list("TETRIS")
tetris_colors = [(255, 0, 0), (0, 0, 255), (255, 165, 0), (0, 255, 255), (0, 255, 0), (255, 0, 255)]

tetrominoes = {
    'I': [[1, 1, 1, 1]], 'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]], 'O': [[1, 1], [1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]], 'T': [[0, 1, 0], [1, 1, 1]],
    'Z': [[1, 1, 0], [0, 1, 1]]
}

class Piece:
    def _init_(self, x, y, shape):
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
        if y >= 0 and 0 <= x < grid_width and 0 <= y < grid_height:
            grid[y][x] = color
    return grid

def convert_shape_format(piece):
    positions = []
    if piece:
        for i, line in enumerate(piece.image()):
            for j, col in enumerate(line):
                if col:
                    # Pac-Man style wrapping: if x goes out of bounds, wrap to other side
                    x = (piece.x + j) % grid_width
                    y = piece.y + i
                    positions.append((x, y))
    return positions

def valid_space(piece, grid):
    if not piece:
        return False
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

def detect_full_rows(grid):
    return [i for i, row in enumerate(grid) if black not in row]

def remove_rows(locked, rows):
    for row in rows:
        for x in range(grid_width):
            locked.pop((x, row), None)
    for (x, y) in sorted(list(locked), key=lambda k: k[1], reverse=True):
        shift = sum(1 for r in rows if y < r)
        if shift > 0:
            color = locked.pop((x, y))
            locked[(x, y + shift)] = color

def flash_rows(surface, grid, rows, letter_colors, flash_times=6, delay=100):
    for i in range(flash_times):
        for y in rows:
            for x in range(grid_width):
                grid[y][x] = random.choice(colors) if i % 2 == 0 else black
        draw_window(surface, grid, 0, None, letter_colors, (0, 255, 0), None, None)
        pygame.display.update()
        pygame.time.delay(delay)

def draw_grid(surface, grid):
    for y in range(grid_height):
        for x in range(grid_width):
            if grid[y][x] != black:
                # Desenha bloco com efeito 3D
                draw_3d_block(surface, grid[y][x], x * block_size + 200, y * block_size, block_size)
            else:
                # Desenha bloco vazio
                pygame.draw.rect(surface, black, (x * block_size + 200, y * block_size, block_size, block_size), 0)
    
    # Linhas da grade
    for y in range(grid_height):
        pygame.draw.line(surface, gray, (200, y * block_size), (200 + grid_width * block_size, y * block_size))
    for x in range(grid_width):
        pygame.draw.line(surface, gray, (x * block_size + 200, 0), (x * block_size + 200, grid_height * block_size))

def draw_next_pieces(surface, pieces):
    font = pygame.font.SysFont('comicsans', 25)
    label = font.render('Próximas:', True, white)
    x_off = grid_width * block_size + 210
    y_off = 20
    surface.blit(label, (x_off, y_off))
    for idx, (piece, color) in enumerate(pieces):
        if piece:
            format = piece.shape[0]
            for i, line in enumerate(format):
                for j, col in enumerate(line):
                    if col:
                        # Desenha peças da preview com efeito 3D
                        draw_3d_block(surface, color,
                                     x_off + j * block_size,
                                     y_off + 30 + idx * 4 * block_size + i * block_size,
                                     block_size)

def draw_sidebar(surface, score, letter_colors, box_color):
    font = pygame.font.SysFont('comicsans', 30, bold=True)
    pygame.draw.rect(surface, box_color, (10, 10, 180, 110), 0)
    pygame.draw.rect(surface, white, (10, 10, 180, 110), 3)
    label = font.render('Pontuação:', True, white)
    surface.blit(label, (20, 20))

    score_font = pygame.font.SysFont('comicsans', 45, bold=True)
    score_label = score_font.render(f'{score:05d}', True, white)
    surface.blit(score_label, (40, 60))

    font_tetris = pygame.font.SysFont('comicsans', 50, bold=True)
    for i, letter in enumerate(tetris_letters):
        color = letter_colors[i]
        label = font_tetris.render(letter, True, color)
        surface.blit(label, (85, 130 + i * 55))
        
        
def draw_controls(surface):
    font = pygame.font.SysFont('arial', 20)
    controls = [
        "Controles:",
        " ← → : mover",
        "↓    : acelerar queda",
        "↑    : girar peça",
        "ESC  : sair"
    ]
    x = 20
    y = screen_height - 140
    for line in controls:
        label = font.render(line, True, white)
        surface.blit(label, (x, y))
        y += 25

def draw_window(surface, grid, score=0, next_pieces=None, letter_colors=None, box_color=(0,255,0), current_piece=None, current_color=None):
    surface.fill(black)
    draw_sidebar(surface, score, letter_colors, box_color)
    draw_controls(surface)
    draw_grid(surface, grid)
    
    # Desenha a peça fantasma (ghost piece)
    if current_piece:
        ghost_piece = get_ghost_piece(current_piece, grid)
        if ghost_piece:
            ghost_color = tuple(c // 3 for c in current_color)  # Cor mais transparente
            for pos in convert_shape_format(ghost_piece):
                x, y = pos
                if y > -1 and 0 <= x < grid_width and 0 <= y < grid_height:
                    # Desenha bloco fantasma com transparência
                    pygame.draw.rect(surface, ghost_color, 
                                   (x * block_size + 200, y * block_size, block_size, block_size), 2)
    
    # Desenha a peça atual com efeito 3D
    if current_piece:
        for pos in convert_shape_format(current_piece):
            x, y = pos
            if y > -1 and 0 <= x < grid_width and 0 <= y < grid_height:
                draw_3d_block(surface, current_color, x * block_size + 200, y * block_size, block_size)
    
    pygame.draw.rect(surface, white, (200, 0, grid_width * block_size, grid_height * block_size), 5)
    if next_pieces:
        draw_next_pieces(surface, next_pieces)

def draw_3d_block(surface, color, x, y, size):
    """Desenha um bloco com efeito 3D"""
    # Cores para o efeito 3D
    light_color = tuple(min(255, c + 60) for c in color)  # Cor mais clara
    dark_color = tuple(max(0, c - 60) for c in color)    # Cor mais escura
    
    # Bloco principal
    pygame.draw.rect(surface, color, (x, y, size, size), 0)
    
    # Borda superior e esquerda (mais clara)
    pygame.draw.polygon(surface, light_color, [
        (x, y), (x + size - 3, y), (x + size - 3, y + 3), (x + 3, y + 3), (x + 3, y + size - 3), (x, y + size - 3)
    ])
    
    # Borda inferior e direita (mais escura)
    pygame.draw.polygon(surface, dark_color, [
        (x + 3, y + size - 3), (x + size - 3, y + size - 3), (x + size - 3, y + 3), (x + size, y + 3), (x + size, y + size), (x, y + size)
    ])
    
    # Borda externa preta
    pygame.draw.rect(surface, gray, (x, y, size, size), 1)

def get_ghost_piece(current_piece, grid):
    """Calcula onde a peça atual vai cair (ghost piece)"""
    if not current_piece:
        return None
    
    ghost_piece = Piece(current_piece.x, current_piece.y, current_piece.shape)
    ghost_piece.rotation = current_piece.rotation
    
    # Move a peça fantasma para baixo até encontrar obstáculo
    while valid_space(ghost_piece, grid):
        ghost_piece.y += 1
    ghost_piece.y -= 1  # Volta uma posição
    
    return ghost_piece

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
    horizontal_speed = 0.1
    soft_speed = 0.05
    score = 0
    next_speed_threshold = 1000
    min_fall_speed = 0.1

    color_change_timer = 0
    letter_colors = tetris_colors.copy()
    box_color = (0, 255, 0)

    run = True
    while run:
        grid = create_grid(locked)
        dt = clock.get_rawtime()
        fall_time += dt
        level_time += dt
        horizontal_time += dt
        soft_time += dt
        color_change_timer += dt
        clock.tick()

        if color_change_timer > 500:
            color_change_timer = 0
            random.shuffle(letter_colors)
            box_color = random.choice(colors)

        keys = pygame.key.get_pressed()
        if current_piece: 
            if keys[pygame.K_DOWN] and soft_time / 1000 >= soft_speed:
                soft_time = 0
                current_piece.y += 1
                if not valid_space(current_piece, grid):
                    current_piece.y -= 1
            if keys[pygame.K_LEFT] and horizontal_time / 1000 >= horizontal_speed:
                horizontal_time = 0
                old_x = current_piece.x
                current_piece.x -= 1
                # Allow wrapping to the right side if going too far left
                if current_piece.x < -3:  # Allow some tolerance for piece width
                    current_piece.x = grid_width - 1
                if not valid_space(current_piece, grid):
                    current_piece.x = old_x  # Restore if invalid
            elif keys[pygame.K_RIGHT] and horizontal_time / 1000 >= horizontal_speed:
                horizontal_time = 0
                old_x = current_piece.x
                current_piece.x += 1
                # Allow wrapping to the left side if going too far right
                if current_piece.x > grid_width + 2:  # Allow some tolerance for piece width
                    current_piece.x = 0
                if not valid_space(current_piece, grid):
                    current_piece.x = old_x  # Restore if invalid

        if level_time / 1000 > 60:
            level_time = 0
            fall_speed = max(min_fall_speed, fall_speed - 0.005)

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            if current_piece: 
                current_piece.y += 1
                if not valid_space(current_piece, grid) and current_piece.y > 0:
                    current_piece.y -= 1
                    locked.update({pos: current_color for pos in convert_shape_format(current_piece)})
                    grid = create_grid(locked)
                    full_rows = detect_full_rows(grid)
                    if full_rows:
                        flash_rows(win, grid, full_rows, letter_colors)
                        remove_rows(locked, full_rows)
                        cleared = len(full_rows)
                        score += cleared ** 2 * 100
                        if score >= next_speed_threshold:
                            fall_speed = max(min_fall_speed, fall_speed - 0.1)
                            next_speed_threshold += 1000
                    current_piece, current_color = next_pieces.pop(0)
                    next_pieces.append(get_shape())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif current_piece and event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        current_piece.rotate() 
                        current_piece.rotate()
                        current_piece.rotate()
        
        draw_window(win, grid, score, next_pieces, letter_colors, box_color, current_piece, current_color)
        pygame.display.update()
        
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            run = False

        if check_lost(locked):
            font = pygame.font.SysFont('comicsans', 60, bold=True)
            label = font.render('GAME OVER', True, white)
            win.blit(label, ((screen_width - label.get_width()) // 2, (screen_height - label.get_height()) // 2))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False

    pygame.quit()

if __name__ == '__main__':
    main()
