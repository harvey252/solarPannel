import pygame

class powerTheCityGame:
    def __init__(self):
        print("init powerTheCityGame")
        self.grid_size = 6
        self.path = []
        self.active = False
        self.completed = False

        # Initialize Pygame display info to get screen size
        pygame.display.init()
        display_info = pygame.display.Info()
        max_width = int(display_info.current_w * 0.9)
        max_height = int(display_info.current_h * 0.9)

        # Load and scale background
        try:
            raw_bg = pygame.image.load("prettyCountryside.png").convert()
            bg_w, bg_h = raw_bg.get_size()
            scale = min(max_width / bg_w, max_height / bg_h)
            self.window_width = int(bg_w * scale)
            self.window_height = int(bg_h * scale)
            self.background = pygame.transform.smoothscale(raw_bg, (self.window_width, self.window_height))
            print("Background loaded and scaled")
        except Exception as e:
            print("Failed to load background:", e)
            self.window_width, self.window_height = 552, 864
            self.background = pygame.Surface((self.window_width, self.window_height))
            self.background.fill((0, 100, 0))
            scale = 1.0

        # Tile and layout setup
        self.tile_size = min(self.window_width // (self.grid_size + 2), self.window_height // (self.grid_size + 2))
        grid_pixel_size = self.grid_size * self.tile_size
        self.offset_x = (self.window_width - grid_pixel_size) // 2
        self.offset_y = (self.window_height - grid_pixel_size) // 2

        self.grid_data = [
            ['B', 'B', 'R', 'B', 'B', ' '],
            ['B', 'R', 'R', 'R', 'B', ' '],
            ['R', 'R', 'B', 'R', 'B', ' '],
            ['B', 'R', 'B', 'R', 'R', ' '],
            ['R', 'R', 'R', 'B', 'R', 'R'],
            [' ', ' ', 'B', 'B', 'R', 'R'],
        ]

        icon_size = int(self.tile_size * 1.5)

        try:
            solar = pygame.image.load("solarpanelFarm.png").convert_alpha()
            self.solar_img = pygame.transform.smoothscale(solar, (icon_size, icon_size))
            print("Solar panel loaded")
        except Exception as e:
            print("Failed to load solar panel:", e)

        try:
            ground = pygame.image.load("groundSymbol.png").convert_alpha()
            self.ground_img = pygame.transform.smoothscale(ground, (icon_size, icon_size))
            print("Ground symbol loaded")
        except Exception as e:
            print("Failed to load ground symbol:", e)

        # Place solar panel bottom center aligned with top-right corner
        self.start_rect = self.solar_img.get_rect()
        self.start_rect.centerx = self.offset_x + self.grid_size * self.tile_size
        self.start_rect.bottom = self.offset_y

        # Place ground symbol top center aligned with bottom-left corner
        self.end_rect = self.ground_img.get_rect()
        self.end_rect.centerx = self.offset_x
        self.end_rect.top = self.offset_y + self.grid_size * self.tile_size

        self.colors = {
            'R': (200, 200, 200),
            'B': (200, 0, 0),
            ' ': (0, 0, 0),
            'P': (255, 255, 0)
        }

        pygame.font.init()
        self.font = pygame.font.SysFont("arial", 28)
        self.message = ""

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                tile = self.grid_data[row][col]
                color = self.colors[tile]
                rect = pygame.Rect(
                    col * self.tile_size + self.offset_x,
                    row * self.tile_size + self.offset_y,
                    self.tile_size,
                    self.tile_size
                )
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (50, 50, 50), rect, 1)

        for row, col in self.path:
            rect = pygame.Rect(
                col * self.tile_size + self.offset_x + self.tile_size // 6,
                row * self.tile_size + self.offset_y + self.tile_size // 6,
                self.tile_size * 2 // 3,
                self.tile_size * 2 // 3
            )
            pygame.draw.rect(screen, self.colors['P'], rect)

        screen.blit(self.solar_img, self.start_rect.topleft)
        screen.blit(self.ground_img, self.end_rect.topleft)

        if self.message:
            msg_surface = self.font.render(self.message, True, (255, 255, 255))
            screen.blit(msg_surface, (20, 20))

        pygame.display.flip()

    def run(self, clock):
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if self.start_rect.collidepoint(mx, my) and not self.completed:
                    self.active = True
                    self.path = []
                    self.message = ""
                elif not self.completed:
                    self.active = False
                    self.path = []
                    self.message = ""

        if self.active and not self.completed:
            mx, my = pygame.mouse.get_pos()
            col = (mx - self.offset_x) // self.tile_size
            row = (my - self.offset_y) // self.tile_size

            if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
                tile = self.grid_data[row][col]
                pos = (row, col)

                if tile == 'R':
                    if not self.path:
                        self.path.append(pos)
                    elif pos != self.path[-1]:
                        if pos in self.path:
                            idx = self.path.index(pos)
                            self.path = self.path[:idx+1]
                        elif self.is_adjacent(pos, self.path[-1]):
                            self.path.append(pos)
            elif self.end_rect.collidepoint(mx, my):
                if self.path and self.is_adjacent(self.end_grid_pos(), self.path[-1]):
                    self.path.append(self.end_grid_pos())
                    self.completed = True
                    self.active = False
                    if len(self.path) >= self.longest_path_length():
                        self.message = "Great work! Now most of your city is powered by solar energy :)"
                        return False
                    else:
                        self.message = "Surely you can power more houses than that?"

        return True

    def is_adjacent(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1

    def end_grid_pos(self):
        return (self.grid_size - 1, 0)

    def longest_path_length(self):
        return 14