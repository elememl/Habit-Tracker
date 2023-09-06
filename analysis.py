from datetime import date, timedelta
from typing import Tuple
from habit import Habit


def get_longest_streak(habit: Habit) -> int:
    """
    Calculate the longest streak of completing a habit.

    Args:
        habit (Habit): The Habit object.

    Returns:
        int: The longest streak of completing the habit.
    """
    if len(habit.progress) == 0:
        return 0
    else:
        streaks = []
        streak = 0
        for i in range(len(habit.progress) - 1):
            diff = habit.progress[i + 1] - habit.progress[i]
            if diff == 1:
                streak += 1
            else:
                streaks.append(streak)
                streak = 0
        streaks.append(streak)
        max_streak = max(streaks) + 1
        return max_streak


def get_broken_habits(habit: Habit, days_range: int) -> Tuple[int, int]:
    """
    Calculate the completeness of a habit and the number of periods wanted.

    Args:
        habit (Habit): The Habit object.
        days_range (int): The number of days to consider for completeness.

    Returns:
        Tuple[int, int]: A tuple containing completeness and periods wanted.
    """
    now = date.today()
    all_days = now - habit.creation_date
    periodicity = {'daily': 1, 'weekly': 7, 'monthly': 30}

    periods_elapsed = all_days.days // periodicity[habit.periodicity]
    periods_wanted = days_range // periodicity[habit.periodicity]

    if all_days.days < days_range:
        ideal = list(range(0, periods_elapsed))
        fails = 0
        for i in ideal:
            if i not in habit.progress:
                fails += 1
        completeness = periods_elapsed - fails
        return completeness, periods_elapsed

    periods_to_skip = periods_elapsed - periods_wanted
    ideal = list(range(periods_to_skip, periods_elapsed))
    fails = 0
    for i in ideal:
        if i not in habit.progress:
            fails += 1

    completeness = periods_wanted - fails

    return completeness, periods_wanted


def get_days_left(habit: Habit) -> int:
    """
    Calculate the number of days left to complete a habit for the current period.

    Args:
        habit (Habit): The Habit object.

    Returns:
        int: The number of days left to complete the habit.
    """
    now = date.today()
    periodicity = {'daily': 1, 'weekly': 7, 'monthly': 30}
    current_period = (now - habit.creation_date).days // periodicity[habit.periodicity]

    next_period_start = habit.creation_date + timedelta(days=(current_period + 1) * periodicity[habit.periodicity])
    days_left = (next_period_start - now).days

    return days_left
