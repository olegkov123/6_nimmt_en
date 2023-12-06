# Initialize constants for screen and card dimensions
SCREEN_WIDTH = 1920  # Screen width in pixels
SCREEN_HEIGHT = 1080  # Screen height in pixels
CARD_WIDTH = 70  # Card width in pixels
CARD_HEIGHT = 100  # Card height in pixels
CARD_MARGIN = 20  # Margin between cards in pixels
COLUMN_MARGIN = 150  # Margin between columns in pixels

# Initialize constants for colors
WHITE = (255, 255, 255)  # White color
DARK_GREEN = (0, 100, 0)  # Dark green color

# Initialize constants for table structure
NUM_COLUMNS = 4  # Number of columns for cards on the table
MAX_CARDS_IN_COLUMN = 4  # Maximum number of cards in a single column

# Initialize constants for distance between cards and rows
CARD_GAP = 5  # Distance between cards and between rows in pixels

# Calculate the total width and height for displaying all cards, including gaps between them
TOTAL_CARDS_WIDTH = NUM_COLUMNS * CARD_WIDTH + (NUM_COLUMNS - 1) * CARD_GAP  # Total width in pixels
TOTAL_CARDS_HEIGHT = MAX_CARDS_IN_COLUMN * CARD_HEIGHT + (MAX_CARDS_IN_COLUMN - 1) * CARD_GAP  # Total height in pixels

# Calculate the starting coordinates to center the block of cards on the screen
START_X = (SCREEN_WIDTH - TOTAL_CARDS_WIDTH) // 2  # Starting X-coordinate
START_Y = (SCREEN_HEIGHT - TOTAL_CARDS_HEIGHT) // 2  # Starting Y-coordinate
