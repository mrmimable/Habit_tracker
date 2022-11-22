"""
analyse.py covers the user navigation for the analyse functionalities.
It imports necessary db.py functionalities and other libaries used.
"""
import questionary
from datetime import datetime
from db import get_record_streak_from_all_habits, get_longest_streak, get_all_specific_data, \
    get_all_longest_streaks, get_all_habits_with_periodicity, verify_habit_exists, get_all_habit_data, \
    get_current_active_habits, load_predefined_habits, get_all_completion_data, load_completion_data


# analyse_habits method. user navigation and calling of db.py methods for returning and printing possible
# user analysing functions.
def analyse_habits(self, db, ):
    choice = questionary.select("What do you want to do?",
                                 choices=["List all currently active habits", "List all habits with a specific "
                                          "periodicity", "Record streak of all habits", "Longest streak of all habits",
                                          "Longest streak for a specific habit", "Show all the data for a specific habit",
                                          "Show all habit data", "Show all completion data", "Load predefined data",
                                           "Return to menu", ]).ask()

    if choice == "List all currently active habits":
        cutoff_date = datetime.today()
        returnval = get_current_active_habits(db, cutoff_date, )
        print(f" The following habits are currently active:")
        print(returnval)
    elif choice == "List all habits with a specific periodicity":
        periodicity = questionary.select("Which periodicity of habits you want to be shown?", ["Daily", "Weekly", ]).ask()
        returnval = get_all_habits_with_periodicity(db, periodicity, )
        print(f" The following habits have a {periodicity} periodicity:")
        print(returnval)
    elif choice == "Record streak of all habits":
        returnval = get_record_streak_from_all_habits(db,)
        print(f"The overall max streak of a habit is: {returnval}")
    elif choice == "Longest streak of all habits":
        returnval = get_all_longest_streaks(db,)
        print("Following are all habits including their max streaks:")
        print(returnval)
    elif choice == "Longest streak for a specific habit":
        name = questionary.text("Whats the name of the habit?").ask()
        verify = verify_habit_exists(db, name, )
        if verify is None:
            print(f"The Habit: {name} does not exist and therefore has no streak associated")
        else:
            returnval = get_longest_streak(db, name,)
            print(f" The longest streak for the habit {name} is: {returnval}")
    elif choice == "Show all habit data":
        returnval = get_all_habit_data(db, )
        for all in returnval:
            print(all)
    elif choice == "Show all the data for a specific habit":
        name = questionary.text("Whats the name of the habit?").ask()
        verify = verify_habit_exists(db, name, )
        if verify is None:
            print(f"The Habit: {name} does not exist and therefore has no streak associated")
        else:
            returnval = get_all_specific_data(db, name, )
            print(f"{name} : {returnval}")
    elif choice == "Load predefined data":
        load_predefined_habits(db, )
        load_completion_data(db, )
    elif choice == "Show all completion data":
        returnval = get_all_completion_data(db, )
        for all in returnval:
            print(all)
    elif choice == "Return to menu":
        print("Welcome back")
