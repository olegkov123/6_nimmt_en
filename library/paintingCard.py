import pygame
import math

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
RED = (255, 100, 100)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
BLUE = (100, 100, 255)
GRAY = (230, 230, 255)
GREEN = (100, 255, 100)

# Define constants for card size and shadow
SHADOW_OFFSET_X = 5
SHADOW_OFFSET_Y = 5
SHADOW_COLOR = (50, 50, 50, 20)  # Gray color with transparency
CARD_WIDTH = 70
CARD_HEIGHT = 100

class PaintingCard:
    def __init__(self, card, x, y, is_face_up=True):
        self.card = card  # The class now accepts an object of the Card class
        self.x = x
        self.y = y
        self.width = CARD_WIDTH
        self.height = CARD_HEIGHT
        self.radius = 10
        self.points_font = pygame.font.Font(None, 24)  # Font size for points
        self.angles_font = pygame.font.Font(None, 15)  # Font size for corners
        self.font = pygame.font.Font(None, 36)  # Main font size
        self.number_font = pygame.font.Font('font/CroissantOne-Regular.ttf', 30)  # Font for card number
        self.background_color = WHITE  # Background color
        self.is_face_up = is_face_up  # Is the card face up?

        # Setting the points and color
        self.points = self.card.points  # Using a method from the Card class
        self._find_color()

    def _find_color(self):
        # Setting the color based on the number of points
        if self.points == 7:
            self.color = PURPLE
        elif self.points == 5:
            self.color = RED
        elif self.points == 3:
            self.color = BLUE
        elif self.points == 2:
            self.color = GREEN
        else:
            self.color = GRAY

    def draw_backside(self, surface):
        # Draw the backside of the card
        pygame.draw.rect(surface, GREEN, (self.x, self.y, self.width, self.height))
        pygame.draw.circle(surface, RED, (self.x + self.width // 2, self.y + self.height // 2), self.width // 4)
        pygame.draw.line(surface, BLUE, (self.x, self.y), (self.x + self.width, self.y + self.height), 3)
        pygame.draw.line(surface, BLUE, (self.x + self.width, self.y), (self.x, self.y + self.height), 3)

    def draw_diagonal_stripe(self, surface, y_offset, length, angle, color):
        # Draw a diagonal stripe at the given location, length, and angle
        start_x = self.x + (self.width - length) / 2
        start_y = self.y + self.height / 2 + y_offset
        end_x = start_x + length * math.cos(math.radians(angle))
        end_y = start_y + length * math.sin(math.radians(angle))
        line_thickness = self.height // 3
        pygame.draw.line(surface, color, (start_x, start_y), (end_x, end_y), line_thickness)

    def draw_shadow(self, surface):
        # Draw the card's shadow
        pygame.draw.rect(surface, SHADOW_COLOR, (self.x + SHADOW_OFFSET_X, self.y + self.radius + SHADOW_OFFSET_Y, self.width, self.height - 2 * self.radius))
        pygame.draw.rect(surface, SHADOW_COLOR, (self.x + self.radius + SHADOW_OFFSET_X, self.y + SHADOW_OFFSET_Y, self.width - 2 * self.radius, self.height))
        pygame.draw.circle(surface, SHADOW_COLOR, (self.x + self.radius + SHADOW_OFFSET_X, self.y + self.radius + SHADOW_OFFSET_Y), self.radius)
        pygame.draw.circle(surface, SHADOW_COLOR, (self.x + self.width - self.radius + SHADOW_OFFSET_X, self.y + self.radius + SHADOW_OFFSET_Y), self.radius)
        pygame.draw.circle(surface, SHADOW_COLOR, (self.x + self.radius + SHADOW_OFFSET_X, self.y + self.height - self.radius + SHADOW_OFFSET_Y), self.radius)
        pygame.draw.circle(surface, SHADOW_COLOR, (self.x + self.width - self.radius + SHADOW_OFFSET_X, self.y + self.height - self.radius + SHADOW_OFFSET_Y), self.radius)

    def draw(self, surface):
        """Draw the card on the given surface."""

        # Draw the backside if the card is not face up
        if not self.is_face_up:
            self.draw_backside(surface)
            return

        # Special drawing for a zero-valued card
        if self.card.value == 0:
            dash_length = 10
            gap_length = 5
            color = BLACK  # Outline color

            # Draw dashed rectangle
            for i in range(0, self.width, dash_length + gap_length):
                pygame.draw.line(surface, color, (self.x + i, self.y), (self.x + min(i + dash_length, self.width), self.y))
                pygame.draw.line(surface, color, (self.x + i, self.y + self.height), (self.x + min(i + dash_length, self.width), self.y + self.height))

            for i in range(0, self.height, dash_length + gap_length):
                pygame.draw.line(surface, color, (self.x, self.y + i), (self.x, self.y + min(i + dash_length, self.height)))
                pygame.draw.line(surface, color, (self.x + self.width, self.y + i), (self.x + self.width, self.y + min(i + dash_length, self.height)))

            # Draw diagonal lines
            pygame.draw.line(surface, color, (self.x, self.y), (self.x + self.width, self.y + self.height))
            pygame.draw.line(surface, color, (self.x + self.width, self.y), (self.x, self.y + self.height))

        else:
            # Draw standard card

            # Draw card shadow
            self.draw_shadow(surface)

            # Draw card background
            pygame.draw.rect(surface, self.background_color, (self.x, self.y + self.radius, self.width, self.height - 2 * self.radius))
            pygame.draw.rect(surface, self.background_color, (self.x + self.radius, self.y, self.width - 2 * self.radius, self.height))
            pygame.draw.circle(surface, self.background_color, (self.x + self.radius, self.y + self.radius), self.radius)
            pygame.draw.circle(surface, self.background_color, (self.x + self.width - self.radius, self.y + self.radius), self.radius)
            pygame.draw.circle(surface, self.background_color, (self.x + self.radius, self.y + self.height - self.radius), self.radius)
            pygame.draw.circle(surface, self.background_color, (self.x + self.width - self.radius, self.y + self.height - self.radius), self.radius)

            # Draw corner numbers
            number_surface = self.angles_font.render(str(self.card.value), True, BLACK)
            surface.blit(number_surface, (self.x + 5, self.y + 5))  # Top-left
            surface.blit(number_surface, (self.x + self.width - number_surface.get_width() - 5, self.y + 5))  # Top-right

            rotated_surface = pygame.transform.rotate(number_surface, 180)
            surface.blit(rotated_surface, (self.x + 5, self.y + self.height - 5 - rotated_surface.get_height()))  # Bottom-left
            surface.blit(rotated_surface, (self.x + self.width - 5 - rotated_surface.get_width(), self.y + self.height - 5 - rotated_surface.get_height()))  # Bottom-right

            # Draw diagonal stripe
            self.draw_diagonal_stripe(surface, -self.height // 12, self.width - 10, 15, self.color)

            # Draw points
            points_string = '*' * self.points
            points_surface = self.points_font.render(points_string, True, BLACK)
            surface.blit(points_surface, (self.x + self.width // 2 - points_surface.get_width() // 2, self.y + self.height - 30))

            # Draw central number
            number_surface = self.number_font.render(str(self.card.value), True, BLACK)
            number_surface.set_colorkey(WHITE)

            number_x = self.x + (self.width - number_surface.get_width()) // 2
            number_y = self.y + (self.height - number_surface.get_height()) // 2

            outline_thickness = 1
            for offset_x in range(-outline_thickness, outline_thickness + 1):
                for offset_y in range(-outline_thickness, outline_thickness + 1):
                    surface.blit(number_surface, (number_x + offset_x, number_y + offset_y))

            number_surface_fill = self.number_font.render(str(self.card.value), True, WHITE)
            surface.blit(number_surface_fill, (number_x, number_y))


    @property
    def surface(self):
        """Returns the surface with the card drawing."""
        card_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw(card_surface)
        return card_surface
