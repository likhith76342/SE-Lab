import math
import pygame


class Puller:
    """Represents a puller character anchor on either side of the rope."""

    def __init__(self, x, y, color, label):
        self.x = x
        self.y = y
        self.color = color
        self.label = label
        self.font = pygame.font.SysFont(None, 24)
        self.max_lean_deg = 35

    def render(self, surface, lean=0.0):
        """Draw avatar tilted around its feet; lean in [-1, 1], positive = tilt right."""
        angle = math.radians(lean * self.max_lean_deg)
        pivot_x, pivot_y = self.x, self.y + 35  # feet

        def rot(px, py):
            dx, dy = px - pivot_x, py - pivot_y
            return (
                pivot_x + dx * math.cos(angle) - dy * math.sin(angle),
                pivot_y + dx * math.sin(angle) + dy * math.cos(angle),
            )

        # Body (rotated rectangle)
        corners = [
            rot(self.x - 20, self.y - 35),
            rot(self.x + 20, self.y - 35),
            rot(self.x + 20, self.y + 35),
            rot(self.x - 20, self.y + 35),
        ]
        pygame.draw.polygon(surface, self.color, corners)

        # Head
        head_x, head_y = rot(self.x, self.y - 50)
        pygame.draw.circle(surface, (240, 210, 180), (int(head_x), int(head_y)), 16)

        # Name / control tag (stays upright)
        label_surf = self.font.render(self.label, True, (240, 240, 240))
        surface.blit(label_surf, (self.x - label_surf.get_width() // 2, self.y + 45))
