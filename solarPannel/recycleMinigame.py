import pygame
import random

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
PANEL_TYPES = ['silicon', 'thin-film', 'organic']
COLORS = {
   'silicon': (0, 0, 255),
   'thin-film': (255, 0, 0),
   'organic': (0, 255, 0)
}

# Custom events
SPAWN_PANEL_EVENT = pygame.USEREVENT + 1
PANEL_MISSED_EVENT = pygame.USEREVENT + 2

class SolarPanel(pygame.sprite.Sprite):
   def __init__(self, panel_type):
       super().__init__()
       self.type = panel_type
       self.image = pygame.Surface((40, 60))
       self.image.fill(COLORS[panel_type])
       self.rect = self.image.get_rect()
       self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
       self.rect.y = 0
       self.speed = 4

   def update(self):
       self.rect.y += self.speed
       if self.rect.top > SCREEN_HEIGHT:
           pygame.event.post(pygame.event.Event(PANEL_MISSED_EVENT))
           self.kill()

class RecyclingBin(pygame.sprite.Sprite):
   def __init__(self, panel_type, x, key_number):
       super().__init__()
       self.type = panel_type
       self.image = pygame.Surface((120, 80))
       self.image.fill(COLORS[panel_type])
       font = pygame.font.Font(None, 36)
       text = font.render(f"{key_number}", True, (0, 0, 0))
       text_rect = text.get_rect(center=(60, 70))
       self.image.blit(text, text_rect)
       self.rect = self.image.get_rect()
       self.rect.centerx = x
       self.rect.bottom = SCREEN_HEIGHT

class Recycler(pygame.sprite.Sprite):
   def __init__(self):
       super().__init__()
       
       self.image = pygame.Surface((60, 60))
       self.current_color = (128, 128, 128)  # Initial gray color
       self.image.fill(self.current_color)
       self.rect = self.image.get_rect()
       self.rect.centerx = SCREEN_WIDTH // 2
       self.rect.bottom = SCREEN_HEIGHT - 20
       self.speed = 16
       self.held_panel = None

   def update(self, keys):
       # Update color based on held panel
       self.image.fill(self.current_color)
       
       # Movement logic
       if keys[pygame.K_LEFT] and self.rect.left > 0:
           self.rect.x -= self.speed
       if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
           self.rect.x += self.speed

def game_over_screen(screen, score):
   screen.fill((255, 255, 255))
   font = pygame.font.Font(None, 74)
   game_over_text = font.render("Game Over!", True, (255, 0, 0))
   screen.blit(game_over_text, (SCREEN_WIDTH//2 - 140, SCREEN_HEIGHT//2 - 50))
   score_text = font.render(f"Score: {score}", True, (0, 0, 0))
   screen.blit(score_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50))
   pygame.display.flip()
   pygame.time.wait(3000)

def run(screen):
   #screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
   pygame.display.set_caption("Solar Panel Recycling")
   clock = pygame.time.Clock()
   
   #load background
   background = pygame.transform.scale(pygame.image.load("images/gameBackground.png"), (1280, 720))

   # Initialize sprites
   all_sprites = pygame.sprite.Group()
   panels = pygame.sprite.Group()
   bins = pygame.sprite.Group()

   # Create recycling bins
   bin_positions = [SCREEN_WIDTH//4, SCREEN_WIDTH//2, 3*SCREEN_WIDTH//4]
   for i, panel_type in enumerate(PANEL_TYPES):
       bin = RecyclingBin(panel_type, bin_positions[i], i+1)
       bins.add(bin)
       all_sprites.add(bin)

   recycler = Recycler()
   all_sprites.add(recycler)

   # Game state
   score = 0
   lives = 3
   running = True

   pygame.time.set_timer(SPAWN_PANEL_EVENT, 2000)

   while running:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False
           elif event.type == SPAWN_PANEL_EVENT:
               panel_type = random.choice(PANEL_TYPES)
               panel = SolarPanel(panel_type)
               panels.add(panel)
               all_sprites.add(panel)
           elif event.type == PANEL_MISSED_EVENT:
               lives -= 1
               if lives <= 0:
                   running = False
           elif event.type == pygame.KEYDOWN:
               if event.key in (pygame.K_1, pygame.K_2, pygame.K_3) and recycler.held_panel:
                   bin_index = event.key - pygame.K_1
                   target_bin = list(bins)[bin_index]
                   if recycler.held_panel.type == target_bin.type:
                       score += 10
                   
                   if score >= 100:
                       running = False
                   recycler.held_panel.kill()
                   recycler.held_panel = None
                   recycler.current_color = (128, 128, 128)  # Reset to gray

       # Update recycler
       keys = pygame.key.get_pressed()
       recycler.update(keys)

       # Collect panels
       if not recycler.held_panel:
           collided = pygame.sprite.spritecollide(recycler, panels, True)
           if collided:
               recycler.held_panel = collided[0]
               recycler.current_color = COLORS[collided[0].type]  # Change color

       # Move collected panel with recycler
       if recycler.held_panel:
           recycler.held_panel.rect.center = recycler.rect.center

       # Update sprites
       panels.update()

       # Draw everything
       screen.fill((255, 255, 255))
       screen.blit(background, (0, 0))
       all_sprites.draw(screen)

       # Display UI
       font = pygame.font.Font(None, 36)
       score_text = font.render(f"Score: {score}", True, (0, 0, 0))
       screen.blit(score_text, (10, 10))
       
       #lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
       #screen.blit(lives_text, (10, 50))

       pygame.display.flip()
       clock.tick(30)

   #game_over_screen(screen, score)

if __name__ == "__main__":
   main()
