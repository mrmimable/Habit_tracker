"""
This block is the responsible for the user navigation. It displays the navigation to the different functionalities the
user can choose and calls the responsible methods for execution.
Import of blocks and functions
"""

import questionary
from db import get_db
from habit import Habit
import analyse


# Cli function is defined to handle user navigation. Questionary provides predefined choices that are available
def cli():
    db = get_db()
    questionary.confirm("Welcome to the Habit Tracker. Let's start tracking your habits?").ask()

    stop = False
    while not stop:
        choice = questionary.select(
            "what do you want to do?",
            choices=["Create a habit", "Mark a habit as completed", "Delete a habit", "Change a habit",
                     "Analyse your habits", "Exit the habit tracker", ]).ask()

        if choice == "Create a habit":
            Habit.create(Habit, db, )
        elif choice == "Delete a habit":
            Habit.delete(Habit, db, )
        elif choice == "Change a habit":
            Habit.change_habit(Habit, db, )
        elif choice == "Mark a habit as completed":
            Habit.habit_completed(analyse, db, )
        elif choice == "Analyse your habits":
            analyse.analyse_habits(analyse, db, )
        else:
            print("bye")
            stop = True


if __name__ == '__main__':
    cli()
