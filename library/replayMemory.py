import random
import os
import pickle


class ReplayMemory:
    # Constructor for the ReplayMemory class
    def __init__(self, capacity, file_path='tmp/memory.pkl'):
        self.capacity = capacity  # Maximum memory size
        self.file_path = file_path  # File path to store experiences

        # If a file with saved experiences exists, load it into memory
        if os.path.exists(self.file_path):
            with open(self.file_path, 'rb') as f:
                try:
                    self.buffer = pickle.load(f)
                except EOFError:
                    self.buffer = []
        else:
            # If the file does not exist, create an empty list and store it on disk
            self.buffer = []
            with open(self.file_path, 'wb') as f:
                pickle.dump(self.buffer, f)

        # Position for storing the next experience
        self.position = len(self.buffer) % self.capacity

    def push(self, state, action, reward, next_state, done):
        """Store an experience (state, action, reward, next_state, done) in memory."""
        if len(self.buffer) < self.capacity:
            self.buffer.append(None)
        self.buffer[self.position] = (state, action, reward, next_state, done)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        """Returns a random sample of experiences with size batch_size."""
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        """Returns the current size of the memory."""
        return len(self.buffer)

    def save_to_disk(self, state, action, reward, next_state, done):
        """Appends a specific experience to the disk file."""
        with open(self.file_path, 'ab') as f:
            pickle.dump((state, action, reward, next_state, done), f)
