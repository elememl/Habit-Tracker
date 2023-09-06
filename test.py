import copy
from datetime import timedelta, date
from pathlib import Path

import pytest
from freezegun import freeze_time

from analysis import get_longest_streak, get_broken_habits, get_days_left
from database import Database
from habit import Habit

CURRENT_DAY = date(2023, 8, 19) + timedelta(28)  # 4 weeks after creation date


@pytest.fixture
def test_database():
    """
    Create a test database for use in tests.

    Returns:
        Database: A test database.
    """
    p = Path('test_database.json')
    test_database = Database()
    test_database.load_habits(path=p)
    return test_database


@pytest.fixture
def daily(test_database):
    """
    Fixture for a daily habit from the test database.

    Args:
        test_database (Database): The test database.

    Returns:
        Habit: The daily habit.
    """
    return test_database.habits['cooking']


@pytest.fixture
def weekly_broken(test_database):
    """
    Fixture for a weekly habit with broken streak from the test database.

    Args:
        test_database (Database): The test database.

    Returns:
        Habit: The weekly habit with a broken streak.
    """
    return test_database.habits['yoga']


@pytest.fixture
def monthly(test_database):
    """
    Fixture for a monthly habit from the test database.

    Args:
        test_database (Database): The test database.

    Returns:
        Habit: The monthly habit.
    """
    return test_database.habits['therapy']


@pytest.fixture
def monthly_empty(test_database):
    """
    Fixture for an empty monthly habit from the test database.

    Args:
        test_database (Database): The test database.

    Returns:
        Habit: The empty monthly habit.
    """
    return test_database.habits['pilates']


@pytest.fixture
def weekly(test_database):
    """
    Fixture for a weekly habit from the test database.

    Args:
        test_database (Database): The test database.

    Returns:
        Habit: The weekly habit.
    """
    return test_database.habits['cleaning']


def test_longest_streak(daily):
    """
    Test the function to calculate the longest streak of completing a habit.

    Args:
        daily (Habit): The daily habit for testing.
    """
    habit = daily
    exp_0 = 3
    res_0 = get_longest_streak(habit)
    assert res_0 == exp_0


@freeze_time(CURRENT_DAY)
def test_get_broken_habits(daily, monthly_empty, weekly_broken):
    """
    Test the function to calculate broken habits.

    Args:
        daily (Habit): The daily habit for testing.
        monthly_empty (Habit): The empty monthly habit for testing.
        weekly_broken (Habit): The weekly habit with a broken streak for testing.
    """
    exp_1 = (13, 28)
    exp_2 = (0, 0)
    exp_3 = (3, 4)
    days_range = 28
    res_1 = get_broken_habits(daily, days_range)
    res_2 = get_broken_habits(monthly_empty, days_range)
    res_3 = get_broken_habits(weekly_broken, days_range)
    assert res_1 == exp_1
    assert res_2 == exp_2
    assert res_3 == exp_3


@freeze_time(CURRENT_DAY)
def test_get_broken_over_time(daily):
    """
    Test the function to calculate broken habits over a longer time range.

    Args:
        daily (Habit): The daily habit for testing.
    """
    exp_1 = (13, 28)
    days_range = 50
    res_1 = get_broken_habits(daily, days_range)
    assert res_1 == exp_1


def test_habit_init():
    """
    Test the initialization of a Habit object.
    """
    habit = Habit('fishing', 'monthly')
    exp = date.today()
    res = habit.creation_date
    assert res == exp


@freeze_time(CURRENT_DAY)
def test_complete_progress(monthly_empty, weekly_broken):
    """
    Test marking habits as completed for the current period.

    Args:
        monthly_empty (Habit): The empty monthly habit for testing.
        weekly_broken (Habit): The weekly habit with a broken streak for testing.
    """
    monthly_empty.complete()
    weekly_broken.complete()
    exp_1 = [0]
    exp_2 = [0, 1, 4]
    res_1 = monthly_empty.progress
    res_2 = weekly_broken.progress
    assert res_1 == exp_1
    assert res_2 == exp_2


@freeze_time(CURRENT_DAY)
def test_complete_error(daily):
    """
    Test marking a habit as completed when it's already completed.

    Args:
        daily (Habit): The daily habit for testing.
    """
    with pytest.raises(RuntimeError):
        daily.complete()


def test_to_dictionary(weekly):
    """
    Test converting a Habit object to a dictionary.

    Args:
        weekly (Habit): The weekly habit for testing.
    """
    exp = {"name": "cleaning", "periodicity": "weekly", "progress": [0, 1, 2, 3],
           "creation_date": {"y": 2023, "m": 8, "d": 19}}
    res = weekly.to_dictionary()
    assert res == exp


def test_from_dictionary():
    """
    Test creating a Habit object from a dictionary.
    """
    habit_dictionary = {"name": "yoga", "periodicity": "weekly", "progress": [0, 1], "creation_date": {"y": 2023, "m": 8, "d": 19}}
    habit = Habit.from_dictionary(habit_dictionary)
    assert habit.name == 'yoga'
    assert habit.periodicity == 'weekly'
    assert habit.progress == [0, 1]
    assert habit.creation_date == date(2023, 8, 19)


def test_from_dictionary_invalid_input():
    """
    Test creating a Habit object from an invalid dictionary input.
    """
    habit = Habit('scrolling', 'daily')
    with pytest.raises(KeyError):
        habit.from_dictionary({'name': 'scrolling', 'periodicity': 'weekly'})


def test_from_dictionary_missing_key():
    """
    Test creating a Habit object from a dictionary with a missing key.
    """
    habit_dictionary = {'name': 'ritual', 'periodicity': 'daily', 'progress': []}
    with pytest.raises(KeyError):
        Habit.from_dictionary(habit_dictionary)


def test_add_habit(test_database):
    """
    Test adding a habit to the test database.

    Args:
        test_database (Database): The test database for testing.
    """
    habit = Habit('shower', 'daily')
    test_database.add_habit(habit)
    exp = habit
    res = test_database.habits[habit.name]
    assert res == exp
    with pytest.raises(RuntimeError):
        test_database.add_habit(habit)


def test_save_load_habits(tmp_path):
    """
    Test saving and loading habits from a file.

    Args:
        tmp_path: Temporary directory for testing.
    """
    path = tmp_path / "for_test.json"
    habit = Habit('volunteering', 'daily')
    creation_date = date.today()
    habit.creation_date = creation_date
    habit.progress = [0, 1]
    habit_other = copy.deepcopy(habit)
    habit_other.name = 'nap'
    database = Database()
    database.add_habit(habit)
    database.add_habit(habit_other)
    database.save_habits(path)
    database_loaded = Database()
    database_loaded.load_habits(path)
    for name, habit in database.habits.items():
        assert habit.creation_date == database_loaded.habits[name].creation_date
        assert habit.progress == database_loaded.habits[name].progress
        assert habit.periodicity == database_loaded.habits[name].periodicity


def test_delete_habit(test_database):
    """
    Test deleting a habit from the test database.

    Args:
        test_database (Database): The test database for testing.
    """
    names = list(test_database.habits.keys())
    test_database.delete_habit(names[0])
    left_habits = list(test_database.habits.keys())
    assert len(names) - 1 == len(left_habits)
    assert names[0] not in left_habits
    with pytest.raises(KeyError):
        test_database.delete_habit(names[0])


@freeze_time(CURRENT_DAY)
def test_days_left(weekly_broken, monthly_empty, daily):
    """
    Test calculating the number of days left to complete habits for the current period.

    Args:
        weekly_broken (Habit): The weekly habit with a broken streak for testing.
        monthly_empty (Habit): The empty monthly habit for testing.
        daily (Habit): The daily habit for testing.
    """
    exp_1 = 7
    exp_2 = 2
    exp_3 = 1
    res_1 = get_days_left(weekly_broken)
    res_2 = get_days_left(monthly_empty)
    res_3 = get_days_left(daily)
    assert res_1 == exp_1
    assert res_2 == exp_2
    assert res_3 == exp_3
