from library.environment import Environment
from library.agent import DDQNAgent
import torch

# Number of episodes for agent training
EPISODES = 1_000_000

# Path to the saved model
MODEL_PATH = "models/main_model"

# Number of players in the game
NUM_PLAYERS = 4

# Function to create initial state after environment reset
def create_initial_state(part1, part2):
    result = []
    for item in part2:
        result.append([torch.from_numpy(part1).numpy(), torch.from_numpy(item).numpy()])
    return result

# Main function for running agent training
def main():
    env = Environment(NUM_PLAYERS)  # Initialize the environment with 4 players
    agent = DDQNAgent()  # Initialize the agent
    agent.load_model(MODEL_PATH)  # Load the saved model
    episode_count = 0  # Counter for tracking progress

    for episode in range(EPISODES):  # Main loop for training
        input_shape, masks = env.reset()  # Reset the environment
        states = create_initial_state(input_shape, masks)  # Create initial state
        done = False  # Flag for episode completion
        episode_count += 1  # Increment episode counter

        while not done:  # Interaction loop between agent and environment
            actions = []  # List to store chosen actions

            for i in range(NUM_PLAYERS):  # Select an action for each player
                actions.append(agent.act(states[i]))

            # Execute a step in the environment
            input_shape, masks, rewards, done, _ = env.step(actions)
            new_states = create_initial_state(input_shape, masks)  # Create new state

            # Store experience in agent's memory
            for i in range(NUM_PLAYERS):
                agent.remember(states[i], actions[i], rewards[i], new_states[i], done)

            agent.replay()  # Train the agent
            states = new_states  # Update the state

            if done:  # Check for episode completion
                break

            agent.adjust_epsilon()  # Adjust the epsilon parameter

        # Print progress
        if episode_count % 1_000 == 0:
            print(episode_count)

        # Save the model
        if episode_count % 100_000 == 0:
            filename = f"{MODEL_PATH}"
            agent.save_model(filename)

    # Save the final model
    agent.save_model(MODEL_PATH)

# Run the main function
if __name__ == '__main__':
    print("Start training")
    main()
