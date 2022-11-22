"""
habit.py covers the habit functionalities. (create,delete,reset,mark complete, change)
It imports necessary db.py functionalities and other libaries used.
"""
from datetime import date, timedelta, datetime
import questionary
from db import add_new_habit_to_table_complete, delete_habit_from_table, update_name, update_periodicity, \
    update_due_date, update_start_date, update_completed_date, update_current_streak, \
    update_longest_streak, get_due_on, get_completed_on, get_current_streak, get_longest_streak,\
    verify_habit_exists, get_periodicity, update_created_date, update_progress_data
"""
Definition of the Habit class.

Included methods are: 
create(self,db)
    creates a new habit
delete(self,db)
    deletes a habit from database
change_habit(self,db)
    changes periodicity or name of a habit
reset_habit(db, name)
    resets data of a habit
habit_completed(self,db)
    marks a habit as completed
"""

# Class definition of Habit
class Habit:

    def __init__(self, name: str, periodicity: str, created_on: str, started_on: str, completed_on: str,
                 due_on: str, current_streak: str, longest_streak: str,):
        """
        Parameters
        :param: name = the name of the habit
        :param: periodicity = periodicity of the habit ('weekly or 'daily')
        :param: created_on = creation date of the habit
        :param: started_on = start date of the habit
        :param: completed_on = last completion date of the habit
        :param: due_on = next due date of the habit
        :param: current_streak = current streak of the habit
        :param: longest_streak = longest streak of the habit
        """
        self.name = name
        self.periodicity = periodicity
        self.created_on = created_on
        self.started_on = started_on
        self.completed_on = completed_on
        self.due_on = due_on
        self.current_streak = current_streak
        self.longest_streak = longest_streak

    # Create method. user creates a new habit if not exists yet. Initialization with placeholder values if needed.
    # Will print successful or failed text.
    def create(self, db,):
        """
        param: self.name = user input of the new name
        param: self.periodicity = user input of periodicity (Daily or Weekly)
        param: self.created_on = datetime creation is now
        param: self.started_on = datetime start is now (Placeholder to be overwritten once completed)
        param: self.completed_on = datetime completion is yesterday (Placeholder to be overwritten once completed)
        param: self.due_on = datetime due is yesterday (ensures reset streak and overwriting start date once first
                            completed)
        param: self.current_streak = set to 0
        param: self.longest_streak = set to 0
        """
        self.name = questionary.text("Name of your new habit?").ask()
        self.periodicity = questionary.select("Define the periodicity of the new habit", ["Daily", "Weekly", ]).ask()
        self.created_on = datetime.today()
        self.started_on = datetime.today()
        self.completed_on = datetime.today() - timedelta(days=1)
        self.due_on = datetime.today() - timedelta(days=1)
        self.current_streak = 0
        self.longest_streak = 0

        # Calls function in db.py add_new_habit_to_table_complete with init values defined above. If returnvalue from
        # method = 1 unique name error occured in the database. (habit already exists).
        returnvalue = add_new_habit_to_table_complete(db, self.name, self.periodicity, self.created_on, self.started_on,
                    self.completed_on, self.due_on, self.current_streak, self.longest_streak, )
        if returnvalue == 1:
            print(f"There is already a habit with the name {self.name} created. Please choose another name or delete "
                  f"the habit")
        else:
            print(f"The Habit: {self.name} with {self.periodicity} periodicity has been created")

    # Delete method. Delete an existing habit from the database. Will print successfull deletion or failed.
    def delete(self, db):
        """
        :param: self.name = user input which habit is to be deleted
        """
        self.name = questionary.text("Which habit do you want to delete?").ask()
        # calls method in db.py verify_habit_exists. if no name is returned habit does not exist and therefore can not
        # be deleted.
        return_verify = verify_habit_exists(db, self.name, )
        choice = questionary.select(f"Are you sure you want to delete the habit {self.name}?",
                                    choices=["YES", "NO", ]).ask()
        if choice == "YES":
            if return_verify is None:
                print(f"The Habit: {self.name} does not exist and therefore can not be deleted")
            else:
                delete_habit_from_table(db, self.name, )
                print(f"The Habit: {self.name} has been deleted successfully")

    # Change habit method. Periodicity or name can be changed. Will print change result or failed.
    def change_habit(self, db,):
        """
        param: self.name = user input of the name of the habit to be changed.
        """
        self.name = questionary.text("Whats the name of the habit you want to change?").ask()
        choice_change = questionary.select("what do you want to do?", choices=["Name", "Periodicity", ]).ask()

        # change habit name. verify existence (verify_habit_exists). then change habit name to new unique name
        if choice_change == "Name":
            return_verify = verify_habit_exists(db, self.name, )
            if return_verify is None:
                print(f"The Habit: {self.name} does not exist and therefore can not be changed")
            else:
                new_name = questionary.text("Whats the new name of the habit?").ask()
                verify_not_exist = verify_habit_exists(db, new_name, )
                if verify_not_exist is None:
                    update_name(db, self.name, new_name, )
                    print(f"The Habit: {self.name} name has been successfully changed to {new_name}")
                else:
                    print(f"The is already a habit with the name {new_name}. Please choose another name!")

        # change periodicity. verify existence (verify_habit_exists). then change habit periodicity to new user input
        # also call reset_habit method for resetting the habit data in database
        if choice_change == "Periodicity":
            verify = verify_habit_exists(db, self.name, )
            if verify is None:
                print(f"The Habit: {self.name} does not exist and therefore can not be changed")
            else:
                confirm = questionary.select("Warning! A change of periodicity will reset the habit creation / start /"
                                             " due and completion dates including all streaks. Are you sure you want to"
                                             "continue?",
                                             choices=["YES", "NO", ]).ask()
                if confirm == "YES":
                    new_periodicity = questionary.select("Define the new periodicity of the habit",
                                                      ["Daily", "Weekly", ]).ask()
                    update_periodicity(db, self.name, new_periodicity, )
                    Habit.reset_habit(db, self.name, )
                    print(f"The Habit: {self.name} periodictiy has been successfully changed to {new_periodicity}")

    # reset_habit method. called from change_habit(periodicity) method. resets database values of the habit.
    def reset_habit(db, name,):
        """
        param: db = db link
        param: name = input name of the habit that has to be reseted
        """
        # calls db.py queries(varia) for setting new placeholder values for dates and streaks.
        write_new_created_on = datetime.today()
        update_created_date(db, name, write_new_created_on, )
        write_new_due_on = datetime.today() - timedelta(days=1)
        update_due_date(db, name, write_new_due_on, )
        write_new_completed_on = datetime.today() - timedelta(days=1)
        update_completed_date(db, name, write_new_completed_on, )
        write_new_started_on = datetime.today() - timedelta(days=1)
        update_start_date(db, name, write_new_started_on, )
        write_new_current_streak = 0
        update_current_streak(db, name, write_new_current_streak, )
        write_new_longest_streak = 0
        update_longest_streak(db, name, write_new_longest_streak, )

    # habit_completed method. mark a habit as completed if exists. calculate new streaks and new dates.
    def habit_completed(self, db, ):
        """
        param: self.name = user input of the name of the habit to be completed.
        """
        self.name = questionary.text("Which habit do you want to mark as completed?").ask()
        return_verify = verify_habit_exists(db, self.name, )

        # check existence habit and call db.py for all the read queries.
        if return_verify is None:
            print(f"The Habit: {self.name} does not exist and therefore can not be marked as completed")
        else:
            return_completed_on = get_completed_on(db, self.name, )
            return_due_on = get_due_on(db, self.name, )
            return_periodicity = get_periodicity(db, self.name, )
            return_current_streak = get_current_streak(db, self.name, )
            return_longest_streak = get_longest_streak(db, self.name, )

            # convert return values for calculation in this method.
            return_completed_on = datetime.strptime(return_completed_on, '%Y-%m-%d %H:%M:%S.%f')
            return_due_on = datetime.strptime(return_due_on, '%Y-%m-%d %H:%M:%S.%f')

            # Calculation as followed:
            # 1. new completed date = today
            # 2. (due date <= today) = (new current streak + 1)
            # 3. (due date > today) = (new current streak = 0)
            # 4. (new current streak = 0) = (new start date = today)
            # 5. (longest streak => current streak) = (longest streak = longest streak)
            # 6. (longest streak < current streak) = (new longest streak = current streak)
            # 7. (periodicity = Daily) = (new due date = due date + 1(day))
            # 8. (periodicity = Weekly) = (new due date = due date + 7(days))

            if return_completed_on.date() == date.today():
                print("This habit has already been completed today")
            else:

                if return_due_on < datetime.today():
                    write_new_current_streak = 0
                    update_current_streak(db, self.name, write_new_current_streak, )
                    return_current_streak = get_current_streak(db, self.name, )
                else:
                    write_new_current_streak = return_current_streak + 1
                    update_current_streak(db, self.name, write_new_current_streak, )
                    return_current_streak = get_current_streak(db, self.name, )

                write_new_completed_on = datetime.today()
                update_completed_date(db, self.name, write_new_completed_on, )
                update_progress_data(db, self.name, write_new_completed_on, )
                print(f"The habit {self.name} has been marked as completed")

                if return_current_streak > return_longest_streak:
                    update_longest_streak(db, self.name, return_current_streak, )
                if return_periodicity == ("Daily"):
                    write_new_due_on = datetime.today() + timedelta(days=1)
                    update_due_date(db, self.name, write_new_due_on, )
                if return_periodicity == ("Weekly"):
                    write_new_due_on = datetime.today() + timedelta(days=7)
                    update_due_date(db, self.name, write_new_due_on, )
                if return_current_streak == 0:
                    write_new_started_on = datetime.today()
                    update_start_date(db, self.name, write_new_started_on, )
                    print(f"Great! You just started the new habit {self.name}. Lets make a streak out of this!")
                else:
                    print(f"Great! Your current streak for this habit is {return_current_streak}.")