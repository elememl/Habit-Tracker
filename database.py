import json
from pathlib import Path
from habit import Habit
DEFAULT_PATH = Path(__file__).parent / 'database.json'


class Database:
    def __init__(self):
        self.habits = {}

    def add_habit(self, habit: Habit) -> None:
        """
        Add a habit to the database.

        Args:
            habit (Habit): The Habit object to add.

        Raises:
            RuntimeError: If the habit with the same name already exists in the database.
        """
        if self.habits.get(habit.name):
            raise RuntimeError()
        self.habits[habit.name] = habit

    def delete_habit(self, delete_habit: str):
        """
        Delete a habit from the database.

        Args:
            delete_habit (str): The name of the habit to delete.

        Raises:
            KeyError: If the habit is not found in the database.
        """
        del self.habits[delete_habit]

    def save_habits(self, path: Path = DEFAULT_PATH):
        """
        Save the habits in the database to a JSON file.

        Args:
            path (Path): The path to the JSON file.
        """
        habits_json = {}
        for key, val in self.habits.items():
            habits_json[key] = val.to_dictionary()
        with open(path, 'w') as f:
            json.dump(habits_json, f)

    def load_habits(self, path: Path = DEFAULT_PATH):
        """
        Load habits from a JSON file into the database.

        Args:
            path (Path): The path to the JSON file.
        """
        with open(path, 'r') as f:
            habits_json = json.load(f)
        self.habits = {}
        for key, val in habits_json.items():
            self.habits[key] = Habit.from_dictionary(val)
