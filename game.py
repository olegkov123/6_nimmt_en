import os
from library.environment import Environment
from library.functions import *
from library.torchmodel import CustomModel
from library.gamestats import GameStats
import pygame
import torch
import numpy as np

# Initialization
path_to_saved_weights = "models/main_model"
NUM_PLAYERS = 4
environment = Environment(NUM_PLAYERS)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game Board')
model = CustomModel()
model.load_state_dict(torch.load(path_to_saved_weights))

# Additional variable to store overall scores
game_stats = GameStats("db/game_stats.db")
save_data = False

# Main game loop variables
running = True
input_shape, masks = environment.reset()
states = create_state_after_reset(input_shape, masks)

is_paused = False
show_partner_cards = False  # This variable controls whether to show partner cards or not

selected_model = path_to_saved_weights  # This variable will store the selected model

# Dropdown menu lists
show_cards_options = ['Yes', 'No']
model_files = os.listdir('models/')

current_model_index = 0

# Main game loop
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            model_files = sorted(os.listdir('models/'), key=lambda x: os.path.getmtime(os.path.join('models/', x)), reverse=True)
            if event.key == pygame.K_F12:  # Check for F12 key
                is_paused = not is_paused  # Toggle pause state
            elif is_paused:
                if event.key == pygame.K_UP:
                    current_model_index = (current_model_index - 1) % len(model_files)
                elif event.key == pygame.K_DOWN:
                    current_model_index = (current_model_index + 1) % len(model_files)

                selected_model = model_files[current_model_index]
                model.load_state_dict(torch.load(os.path.join('models/', selected_model)))

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if is_paused:
                # For the "Show partners cards" option
                if 1670 <= mouse_x <= 1710 and 470 <= mouse_y <= 500:
                    show_partner_cards = not show_partner_cards

    if is_paused:
        display_settings_window(screen, show_partner_cards, selected_model, current_model_index)
    else:
        # Main game logic
        screen.fill(DARK_GREEN)
        display_cards(screen, environment.desk)
        card_clicked = display_player_cards(screen, environment.players, events, show_partner_cards)

        # Check if the round has ended
        round_ended = environment.players[0].cards_count  # Using the number of cards to determine end of round

        if not round_ended:
            # Display "Next Game" button and handle click
            display_next_game_button(screen)

            if check_next_game_button_click(events):
                input_shape, masks = environment.reset()
                states = create_state_after_reset(input_shape, masks)
                # Reset temporary round variables, if needed

        if card_clicked is not None:
            steps = [card_clicked]
            for i in range(1, NUM_PLAYERS):
                state = states[i]
                steps.append(model.predict_prod(np.array([state[0]]), np.array([state[1]]))[0])
            input_shape, masks, _, _, round_score = environment.step(steps)  # Assuming round_score is the score for this round
            states = create_state_after_reset(input_shape, masks)

    pygame.display.flip()

pygame.quit()
