import pygame
import torch
import os

from library.card import Card
from settings.settings import *
from library.paintingCard import PaintingCard

# Initialize the font for displaying points
points_font_size = 100
points_font = pygame.font.Font(None, points_font_size)

# Function to display cards on the table
def display_cards(screen, desk):
    y = START_Y
    for oneline in desk.desklines:
        x = START_X
        for card in oneline.card_values:
            if card is None:
                card_to_draw = PaintingCard(Card(0), x, y, is_face_up=True)
            else:
                card_to_draw = PaintingCard(Card(card), x, y)
            card_to_draw.draw(screen)
            x += CARD_WIDTH + CARD_GAP
        y += CARD_HEIGHT + CARD_GAP

# Function to display player cards
def display_player_cards(screen, players, events, display_partners=True):
    card_clicked = None

    # For the player at the bottom
    x = (SCREEN_WIDTH - CARD_WIDTH * 10 - CARD_GAP * 11) / 2
    y = SCREEN_HEIGHT - CARD_HEIGHT - CARD_GAP
    for card in players[0].hand:
        if card == 0 or card is None:
            card_to_draw = PaintingCard(Card(0), x, y)
        else:
            card_to_draw = PaintingCard(Card(card), x, y)
        card_to_draw.draw(screen)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if x < mouse_x < x + CARD_WIDTH and y < mouse_y < y + CARD_HEIGHT:
                    card_clicked = card
        x += CARD_WIDTH + CARD_GAP

    # Display points for the player at the bottom
    points_surface = points_font.render(str(players[0].points), True, (255, 255, 255))
    screen.blit(points_surface, ((SCREEN_WIDTH - points_surface.get_width()) / 2, y - CARD_GAP - points_surface.get_height()))

    # For the player on the left
    x = CARD_GAP
    y = SCREEN_HEIGHT - CARD_HEIGHT * 10 - CARD_GAP * 11
    for card in players[1].hand:
        if card == 0 or card is None:
            card_to_draw = PaintingCard(Card(0), x, y)
        else:
            card_to_draw = PaintingCard(Card(card), x, y, display_partners)
        card_to_draw.draw(screen)
        y += CARD_HEIGHT + CARD_GAP

    # Display points for the player on the left
    points_surface = points_font.render(str(players[1].points), True, (255, 255, 255))
    screen.blit(points_surface, (x + CARD_WIDTH + CARD_GAP, SCREEN_HEIGHT / 2 - points_surface.get_height() / 2))

    # For the player at the top
    x = (SCREEN_WIDTH - CARD_WIDTH * 10 - CARD_GAP * 11) / 2
    y = CARD_GAP
    for card in players[2].hand:
        if card == 0 or card is None:
            card_to_draw = PaintingCard(Card(0), x, y)
        else:
            card_to_draw = PaintingCard(Card(card), x, y, display_partners)
        card_to_draw.draw(screen)
        x += CARD_WIDTH + CARD_GAP

    # Display points for the player at the top
    points_surface = points_font.render(str(players[2].points), True, (255, 255, 255))
    screen.blit(points_surface, ((SCREEN_WIDTH - points_surface.get_width()) / 2, y + CARD_HEIGHT + CARD_GAP))

    # For the player on the right
    x = SCREEN_WIDTH - CARD_WIDTH - CARD_GAP
    y = SCREEN_HEIGHT - CARD_HEIGHT * 10 - CARD_GAP * 11
    for card in players[3].hand:
        if card == 0 or card is None:
            card_to_draw = PaintingCard(Card(0), x, y)
        else:
            card_to_draw = PaintingCard(Card(card), x, y, display_partners)
        card_to_draw.draw(screen)
        y += CARD_HEIGHT + CARD_GAP

    # Display points for the player on the right
    points_surface = points_font.render(str(players[3].points), True, (255, 255, 255))
    screen.blit(points_surface, (x - CARD_GAP - points_surface.get_width(), SCREEN_HEIGHT / 2 - points_surface.get_height() / 2))

    return card_clicked

def create_state_after_reset(part1, part2):
    res = []
    for item in part2:
        res.append([torch.from_numpy(part1).numpy(), torch.from_numpy(item).numpy()])
    return res

# Function to display the next game button
def display_next_game_button(screen):
    button_x, button_y, button_w, button_h = 300, 400, 200, 60
    shadow_offset = 5

    # Shadow
    pygame.draw.rect(screen, (0, 0, 0), (button_x + shadow_offset, button_y + shadow_offset, button_w, button_h))

    # Main button
    pygame.draw.rect(screen, (0, 128, 255), (button_x, button_y, button_w, button_h))

    font = pygame.font.Font(None, 36)
    text_surface = font.render('Next Game', True, (255, 255, 255))
    screen.blit(text_surface, (button_x + 30, button_y + 15))

# Function to display the settings window
def display_settings_window(screen, show_partners_cards, selected_model, current_model_index):
    pygame.draw.rect(screen, (100, 100, 100), (1400, 400, 400, 450))
    font = pygame.font.Font(None, 36)

    # Title
    text_surface = font.render('Settings', True, (255, 255, 255))
    screen.blit(text_surface, (1450, 420))

    # Option "Show partners cards"
    text_surface = font.render('Show partners cards:', True, (255, 255, 255))
    screen.blit(text_surface, (1410, 470))
    status_text = "Yes" if show_partners_cards else "No"
    text_surface = font.render(status_text, True, (255, 0, 0))
    screen.blit(text_surface, (1670, 470))

    # Option "Model Selection"
    text_surface = font.render('Model Selection:', True, (255, 255, 255))
    screen.blit(text_surface, (1410, 520))

    # List of available models (sorted from newest to oldest)
    model_files = sorted(os.listdir('models/'), key=lambda x: os.path.getmtime(os.path.join('models/', x)), reverse=True)
    for i, model_file in enumerate(model_files[:5]):
        text_color = (255, 0, 0) if i == current_model_index else (255, 255, 255)
        text_surface = font.render(f"{i+1}. {model_file}", True, text_color)
        screen.blit(text_surface, (1410, 570 + i*40))

def check_next_game_button_click(events):
    button_x, button_y, button_w, button_h = 300, 400, 200, 60
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if button_x <= mouse_x <= button_x + button_w and button_y <= mouse_y <= button_y + button_h:
                return True
    return False
