import random
import pygame
from game.rope import Rope
from game.player import Puller


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rope = Rope(width, height)
        self.player = Puller(90, height // 2, (50, 120, 220), "PLAYER (A/D)")
        self.computer = Puller(width - 90, height // 2, (220, 80, 50), "COMPUTER")

        self.last_key = None
        self.winner = None
        self.game_state = "PLAYING"

        self.computer_pull_cooldown = 180
        self.last_computer_pull = pygame.time.get_ticks()

        self.surge_threshold = 0.35   # fraction of the way from center to the player's goal
        self.surge_cooldown = 130     # ms between computer pulls while surging
        self.computer_surging = False

        self.sudden_death_ms = 45000  # match time before Sudden Death starts
        self.match_start = pygame.time.get_ticks()
        self.elapsed_ms = 0
        self.sudden_death = False

        self.font_big = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 26)
        self.font_timer = pygame.font.SysFont(None, 34)

    def pull_multiplier(self):
        return 2.0 if self.sudden_death else 1.0

    def handle_event(self, event):
        if self.game_state != "PLAYING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_d) and event.key != self.last_key:
                self.rope.pull_left(1.0 * self.pull_multiplier())
                self.last_key = event.key

    def update(self):
        if self.game_state != "PLAYING":
            return

        now = pygame.time.get_ticks()

        self.elapsed_ms = now - self.match_start
        self.sudden_death = self.elapsed_ms >= self.sudden_death_ms

        center_x = self.rope.screen_width // 2
        progress = (center_x - self.rope.marker_x) / (center_x - self.rope.left_win_x)
        surging = progress >= self.surge_threshold
        self.computer_surging = surging

        cooldown = self.surge_cooldown if surging else self.computer_pull_cooldown
        if now - self.last_computer_pull >= cooldown:
            computer_variance = random.uniform(0.7, 1.2)
            self.rope.pull_right(computer_variance * self.pull_multiplier())
            self.last_computer_pull = now

        result = self.rope.check_winner()
        if result:
            self.winner = result
            self.game_state = "GAME_OVER"

    def reset(self):
        self.rope.reset()
        self.last_key = None
        self.winner = None
        self.game_state = "PLAYING"
        self.computer_surging = False
        self.last_computer_pull = pygame.time.get_ticks()
        self.match_start = pygame.time.get_ticks()
        self.elapsed_ms = 0
        self.sudden_death = False

    def render(self, screen):
        screen.fill((30, 32, 36))

        mud_rect = pygame.Rect(self.width // 2 - 120, self.height // 2 - 80, 240, 160)
        pygame.draw.rect(screen, (45, 38, 30), mud_rect, border_radius=12)

        self.rope.render(screen)

        center_x = self.width // 2
        momentum = (center_x - self.rope.marker_x) / (center_x - self.rope.left_win_x)
        lean = -max(-1.0, min(1.0, momentum))
        self.player.render(screen, lean)
        self.computer.render(screen, lean)

        # Match timer (top of screen)
        seconds = self.elapsed_ms / 1000.0
        if self.sudden_death:
            timer_text = f"{seconds:.1f}s  -  SUDDEN DEATH (x2 pulls)"
            timer_color = (255, 70, 70)
        else:
            timer_text = f"{seconds:.1f}s"
            timer_color = (240, 240, 240)
        timer_surf = self.font_timer.render(timer_text, True, timer_color)
        screen.blit(timer_surf, (self.width // 2 - timer_surf.get_width() // 2, 10))

        inst_surf = self.font_small.render(
            "Alternate [A] and [D] keys rapidly to pull!", True, (210, 210, 210)
        )
        screen.blit(inst_surf, (self.width // 2 - inst_surf.get_width() // 2, 40))

        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            win_text = f"{self.winner} WINS!"
            color = (80, 220, 80) if self.winner == "PLAYER" else (240, 80, 80)
            text_surf = self.font_big.render(win_text, True, color)
            screen.blit(
                text_surf,
                (self.width // 2 - text_surf.get_width() // 2, self.height // 2 - 50)
            )

            restart_surf = self.font_small.render(
                "Press [R] to Play Again", True, (240, 240, 240)
            )
            screen.blit(
                restart_surf,
                (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 10)
            )
