import numpy as np
import random
from library.torchmodel import CustomModel
from library.replayMemory import ReplayMemory
import torch.optim as optim
import torch
import torch.nn as nn

# Hyperparameters
GAMMA = 0.95
EPSILON = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.995
LEARNING_RATE = 0.001
BATCH_SIZE = 1
MEMORY_SIZE = 200000


class DDQNAgent:
    """DDQNAgent class for reinforcement learning."""

    def __init__(self):
        """
        Initialize DDQNAgent.
        """
        # Initialize hyperparameters
        self.gamma = GAMMA
        self.epsilon = EPSILON
        self.epsilon_min = EPSILON_MIN
        self.epsilon_decay = EPSILON_DECAY
        self.learning_rate = LEARNING_RATE
        self.batch_size = BATCH_SIZE

        # Initialize replay memory
        self.memory = ReplayMemory(MEMORY_SIZE)

        # Initialize training and target models
        self.model = CustomModel()
        self.target_model = CustomModel()

        # Optimizer and loss function
        optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        criterion = nn.CrossEntropyLoss()

        self.model.optimizer = optimizer
        self.model.criterion = criterion

    def update_target_model(self):
        """
        Update weights of the target model.
        """
        self.target_model.load_state_dict(self.model.state_dict())

    def remember(self, state, action, reward, next_state, done):
        """
        Store gameplay experience.
        """
        self.memory.push(state, action, reward, next_state, done)

    def _random_act(self, mask):
        """
        Select random action based on mask.
        """
        one_indices = np.where(mask == 1)[0]
        return random.choice(one_indices)

    def act(self, state):
        """
        Choose action by the agent.
        """
        if np.random.rand() <= self.epsilon:
            indices = np.where(state[1] == 1)[0]
            random_index = np.random.choice(indices)
            return random_index
        q_values = self.model.predict(np.array([state[0]]), np.array([state[1]]))
        return np.argmax(q_values)

    def replay(self):
        """
        Train the model using experience replay.
        """
        if len(self.memory) < self.batch_size:
            return

        minibatch = self.memory.sample(self.batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                next_action = np.argmax(self.model.predict(np.array([next_state[0]]), np.array([next_state[1]])))
                target_q_values = self.target_model.predict(np.array([next_state[0]]), np.array([next_state[1]]))
                target += self.gamma * target_q_values[0][next_action]

            current_q_values = self.model.predict(np.array([state[0]]), np.array([state[1]]))
            current_q_values[0][action] = target
            self.model.train_on_batch(np.array([state[0]]), np.array([state[1]]), np.array(current_q_values))

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def adjust_epsilon(self):
        """
        Adjust the epsilon parameter.
        """
        self.epsilon *= self.epsilon_decay
        if self.epsilon < self.epsilon_min:
            self.epsilon = self.epsilon_min

    def save_model(self, path):
        """
        Save the trained model.
        """
        torch.save(self.model.state_dict(), path)

    def load_model(self, path):
        """
        Load a pre-trained model.
        """
        self.model.load_state_dict(torch.load(path))
        self.update_target_model()
