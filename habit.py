from datetime import date


class Habit:
    def __init__(self, name: str, periodicity: str):
        """
        Initialize a Habit object with a name, periodicity, progress, and creation date.

        Args:
            name (str): The name of the habit.
            periodicity (str): The periodicity of the habit (daily, weekly, or monthly).
        """
        self.name: str = name
        self.periodicity: str = periodicity
        self.progress: list = []
        self.creation_date: date = date.today()

    def complete(self):
        """
        Mark the habit as completed for the current period.

        Raises:
            RuntimeError: If the habit is already completed for the current period.
        """
        now = date.today()
        periodicity = {'daily': 1, 'weekly': 7, 'monthly': 30}
        current_period = (now - self.creation_date) // periodicity[self.periodicity]

        if current_period.days in self.progress:
            raise RuntimeError('habit already completed.')
        self.progress.append(current_period.days)

    def to_dictionary(self):
        """
        Convert the Habit object to a dictionary.

        Returns:
            dict: A dictionary representation of the habit.
        """
        creation_date = {'y': self.creation_date.year, 'm': self.creation_date.month, 'd': self.creation_date.day}
        habit_dictionary = {'name': self.name, 'periodicity': self.periodicity, 'progress': self.progress, 'creation_date': creation_date}
        return habit_dictionary

    @classmethod
    def from_dictionary(cls, habit_dictionary):
        """
        Create a Habit object from a dictionary.

        Args:
            habit_dictionary (dict): A dictionary representation of the habit.

        Returns:
            Habit: A Habit object created from the dictionary.
        """
        name = habit_dictionary['name']
        periodicity = habit_dictionary['periodicity']
        progress = habit_dictionary['progress']
        creation_date_d = habit_dictionary['creation_date']
        creation_date = date(creation_date_d['y'], creation_date_d['m'], creation_date_d['d'])
        habit = cls(name, periodicity)
        habit.progress = progress
        habit.creation_date = creation_date
        return habit

    def __str__(self):
        return f"{self.name} ({self.periodicity})"
