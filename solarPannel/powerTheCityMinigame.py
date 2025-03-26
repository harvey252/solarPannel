import pygame

class powerTheCityGame:
    def __init__(self):
        print("init powerTheCityGame")
        self.grid_size = 10
        self.path = []
        self.active = False
        self.completed = False

        pygame.display.init()
        display_info = pygame.display.Info()
        max_width = int(display_info.current_w * 0.9)
        max_height = int(display_info.current_h * 0.9)

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

        self.tile_size = min(self.window_width // (self.grid_size + 2), self.window_height // (self.grid_size + 2))
        grid_pixel_size = self.grid_size * self.tile_size
        self.offset_x = (self.window_width - grid_pixel_size) // 2
        self.offset_y = (self.window_height - grid_pixel_size) // 2

        R = 'R'
        B = 'B'
        self.grid_data = [
            [B, R, R, R, R, R, R, B, B, R],
            [B, R, B, B, B, B, R, B, R, R],
            [B, R, B, B, R, R, R, B, R, B],
            [B, R, R, R, R, B, R, R, R, B],
            [B, R, B, B, B, B, R, B, R, B],
            [B, R, R, R, R, R, R, B, R, B],
            [B, B, B, B, B, B, R, B, R, B],
            [B, B, B, B, B, B, R, R, R, B],
            [R, R, R, R, B, B, B, B, R, B],
            [R, B, B, R, R, R, R, R, R, B],
        ]

        icon_size = int(self.tile_size * 1.5)

        try:
            solar = pygame.image.load("solarpanelFarm.png").convert_alpha()
            self.solar_img = pygame.transform.smoothscale(solar, (icon_size, icon_size))
        except Exception as e:
            print("Failed to load solar panel:", e)

        try:
            ground = pygame.image.load("groundSymbol.png").convert_alpha()
            self.ground_img = pygame.transform.smoothscale(ground, (icon_size, icon_size))
        except Exception as e:
            print("Failed to load ground symbol:", e)

        try:
            building = pygame.image.load("buildings.png").convert()
            self.building_img = pygame.transform.smoothscale(building, (self.tile_size, self.tile_size))
        except Exception as e:
            print("Failed to load building tile:", e)
            self.building_img = None

        self.start_rect = self.solar_img.get_rect()
        self.start_rect.centerx = self.offset_x + self.grid_size * self.tile_size
        self.start_rect.bottom = self.offset_y

        self.end_grid_pos = (self.grid_size - 1, 0)
        self.end_rect = self.ground_img.get_rect()
        self.end_rect.centerx = self.offset_x
        self.end_rect.top = self.offset_y + self.grid_size * self.tile_size

        self.colors = {
            'R': (200, 200, 200),
            'P': (255, 255, 0)
        }

        pygame.font.init()
        self.font = pygame.font.SysFont("arial", 22)
        self.message = ""

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        pygame.draw.rect(
            screen, (0, 0, 0),
            pygame.Rect(self.offset_x - 5, self.offset_y - 5,
                        self.grid_size * self.tile_size + 10,
                        self.grid_size * self.tile_size + 10),
            5
        )

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                tile = self.grid_data[row][col]
                x = col * self.tile_size + self.offset_x
                y = row * self.tile_size + self.offset_y
                rect = pygame.Rect(x, y, self.tile_size, self.tile_size)

                if tile == 'R':
                    pygame.draw.rect(screen, self.colors['R'], rect)
                elif self.building_img:
                    screen.blit(self.building_img, rect.topleft)

                pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        for row, col in self.path:
            x = self.offset_x + col * self.tile_size + self.tile_size // 2 - 5
            y = self.offset_y + row * self.tile_size + self.tile_size // 2 - 5
            pygame.draw.circle(screen, self.colors['P'], (x + 5, y + 5), 6)

        screen.blit(self.solar_img, self.start_rect.topleft)
        screen.blit(self.ground_img, self.end_rect.topleft)

        if self.message:
            wrapped = self.wrap_text(self.message, self.font, self.window_width - 40)
            for i, line in enumerate(wrapped):
                msg_surface = self.font.render(line, True, (255, 255, 255))
                screen.blit(msg_surface, (20, 20 + i * 26))

        pygame.display.flip()

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

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
                elif self.completed:
                    self.active = False
                    self.path = []
                    self.completed = False
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

                if pos == self.end_grid_pos and self.path and self.is_adjacent(pos, self.path[-2]):
                    self.completed = True
                    self.active = False
                    if len(self.path) >= self.longest_path_length():
                        self.message = "Great work! Now most of your city is powered by solar energy :)"
                    else:
                        self.message = "Surely you can power more houses than that?"

        return True

    def is_adjacent(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1

    def longest_path_length(self):
        return 21
