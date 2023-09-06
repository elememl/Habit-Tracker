from habit import Habit
from analysis import get_longest_streak, get_broken_habits, get_days_left
from tabulate import tabulate
from database import Database
from datetime import date


def create_habit(database: Database) -> None:
    """
    Create a new habit and add it to the database.

    Args:
        database (Database): The database containing habits.
    """
    name = input("Enter habit name: ")
    keys = ['daily', 'weekly', 'monthly']
    periodicity = input("Choose periodicity (daily, weekly or monthly): ")
    if periodicity not in keys:
        print('wrong periodicity')
        return
    habit = Habit(name, periodicity)
    database.add_habit(habit)
    print(f"Habit {name} created.")


def delete_habit(database: Database):
    """
    Delete a habit from the database.

    Args:
        database (Database): The database containing habits.
    """
    name = input("Enter habit name to delete: ")
    try:
        database.delete_habit(name)
        print(f"Habit {name} deleted.")
    except KeyError:
        print(f"Habit {name} not found.")


def view_habits(database: Database):
    """
    View habits in the database, optionally filtered by periodicity.

    Args:
        database (Database): The database containing habits.
    """
    keys = ['daily', 'weekly', 'monthly', '']
    periodicity = input("Enter periodicity (leave blank for all habits): ")
    if periodicity not in keys:
        print('wrong periodicity')
        return
    elif periodicity == "":
        table = []
        for habit in database.habits.values():
            table.append([habit.name, habit.periodicity])
        print(tabulate(table, headers=["Name", "Periodicity"]))
    else:
        table = []
        for habit in database.habits.values():
            if periodicity == habit.periodicity:
                table.append([habit.name, habit.periodicity])
        if not table:
            print(f"There are no habits with {periodicity} periodicity.")
        else:
            print(tabulate(table, headers=["Name", "Periodicity"]))


def complete_habit(database: Database):
    """
    Mark a habit as completed for the current period.

    Args:
        database (Database): The database containing habits.
    """
    name = input("Enter habit name to complete: ")
    try:
        try:
            database.habits[name].complete()
        except KeyError:
            print(f"Habit {name} non exiting.")
            return
        print(f"Habit {name} completed.")
    except RuntimeError:
        print(f"Habit {name} already completed")


def view_longest_streak(database: Database):
    """
    View the longest streak of completing habits.

    Args:
        database (Database): The database containing habits.
    """
    name = input("Enter habit name (leave blank for all habits): ")
    if name == "":
        streaks = []
        names = []
        for habit in database.habits.values():
            streak = get_longest_streak(habit)
            streaks.append(streak)
            names.append(habit.name)
        longest = streaks.index(max(streaks))
        print(f"Longest streak of all habits: {streaks[longest]} for habit {names[longest]}")
    else:
        try:
            streak = get_longest_streak(database.habits[name])
            print(f"Longest streak of {name}: {streak}")
        except KeyError:
            print(f"Habit {name} not found.")


def view_broken_habits(database: Database):
    """
    View habits that have been broken within a specified days range.

    Args:
        database (Database): The database containing habits.
    """
    days_range = int(input("Enter days range: "))
    table = []
    for habit in database.habits.values():
        completeness, periods_wanted = get_broken_habits(habit, days_range)
        try:
            percentage = (completeness / periods_wanted) * 100
            table.append([habit.name, f"{completeness}/{periods_wanted}", f"{percentage:.2f}%"])
        except ZeroDivisionError:
            ...
    if len(table) == 0:
        print("No habits were broken.")
    else:
        print(tabulate(table, headers=["Name", "Completeness", "Percentage"]))


def view_days_left_table(database: Database):
    """
    View the number of days left to complete habits for the current period.

    Args:
        database (Database): The database containing habits.
    """
    now = date.today()
    periodicity = {'daily': 1, 'weekly': 7, 'monthly': 30}

    table = []
    for habit in database.habits.values():
        days_left = get_days_left(habit)

        current_period = (now - habit.creation_date).days // periodicity[habit.periodicity]
        if current_period in habit.progress:
            continue

        table.append([habit.name, days_left])

    if not table:
        print("No habits found.")
    else:
        print(tabulate(table, headers=["Habit Name", "Days Left"]))


def main():
    """
    The main function to run the habit tracker application.
    """
    database = Database()
    database.load_habits()
    while True:
        print("\nMenu:")
        print("1. Create a habit")
        print("2. Delete a habit")
        print("3. View habits")
        print("4. Complete a habit")
        print("5. View longest streak")
        print("6. View broken habits")
        print("7. Days left to complete a habit")
        print("8. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            create_habit(database)
        elif choice == 2:
            delete_habit(database)
        elif choice == 3:
            view_habits(database)
        elif choice == 4:
            complete_habit(database)
        elif choice == 5:
            view_longest_streak(database)
        elif choice == 6:
            view_broken_habits(database)
        elif choice == 7:
            view_days_left_table(database)
        elif choice == 8:
            database.save_habits()
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
