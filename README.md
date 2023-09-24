# Habit Tracker

Habit Tracker is a Python application for tracking and managing your daily, weekly, and monthly habits. With this tool, you can create, delete, complete, and view habits, as well as analyse your progress and streaks.


## Features

- Create a new habit with chosen periodicity (daily, weekly, monthly).
- Delete existing habit.
- Mark habit as completed for the current period.
- View your habits, optionally filtered by periodicity.
- View the longest streak out of all habits or a specified habit.
- Identify habits that have been broken within a specified period of days.
- Check the number of days left to complete habits for the current period.

## Installation
1. Prerequisites:
- python >= 3.10.12 
- Install the required packages:
```shell
pip install -r requirements.text
```
2. Clone the repository:
```shell
git clone https://github.com/elememl/Habit-Tracker.git
```
3. Navigate to the project directory:
```shell
cd Habit-Tracker
```

## Usage

1. Run the application:

```shell
python interface.py
```
2. Use the menu options to interact with the application by entering a number of the option:
```shell
1.Create a habit
2.Delete a habit
3.View habits
4.Complete a habit
5.View longest streak
6.View broken habits
7.Days left to complete a habit
8.Exit 
```
3. Follow the on-screen instructions to perform your intended actions.

## Test

To run the tests for this habit tracker, you can use the following command:

```shell
pytest test.py
```


