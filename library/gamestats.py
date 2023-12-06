import sqlite3
from datetime import datetime


class GameStats:
    def __init__(self, db_path="db/game_stats.db"):
        """
        Initialize the GameStats class.

        :param db_path: Path to the SQLite database.
        """
        self.db_path = db_path
        self.create_tables()

    def create_tables(self):
        """
        Creates the table 'game_sessions' if it doesn't exist.
        """
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_time DATETIME,
                    player_0 INTEGER,
                    player_1 INTEGER,
                    player_2 INTEGER,
                    player_3 INTEGER
                )
            """)
            connection.commit()

    def start_session(self, player_scores):
        """
        Adds a new game session to the 'game_sessions' table.

        :param player_scores: List of player scores.
        """
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO game_sessions (start_time, player_0, player_1, player_2, player_3) 
                VALUES (?, ?, ?, ?, ?)
            """, (start_time, player_scores[0], player_scores[1], player_scores[2], player_scores[3]))
            connection.commit()
