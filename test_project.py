"""
test_project.py covers the testing of the habit tracker methods.
Importing of methods from db.py an analyse.py, libaries and necessary extensions: freezegun.
"""

import analyse
import db
from db import get_db
from datetime import datetime, timedelta
from freezegun import freeze_time


# Test class. This class is defined to get the methods called by pytest when running the test scenario.
# the assert function is run at the end of each test scenario to compare expected output to actual output.

"""
Included methods are:
setup_method(self)
    establish db connection.
test_init(self)
    initialize loading functions of predefined data from csv into database.
test_time_freeze(self)
    verify time freeze extension is running
test_show_daily_habits(self)
    testcase show all daily habits
test_show_weekly_habits(self)
    testcase show all weekly habits
test_current_active_habits(self)
    testcase show all currently active habits
test_show_max_streak_of_all_habits(self)
    testcase show record max streak of all habits
test_show_all_max_streaks(self)
    testcase show all longest streaks of all habits
test_get_longest_streak_specific(self)
    testcase get longest streak of a specific habit
test_show_all_specific_data(self)
    testcase show all specific habit data of a habit
test_show_all_habit_data(self)
    testcase show all habit data
test_create_new_habit(self)
    testcase create a new habit
test_delete_habit(self)
    testcase delete an existing habit
"""


class Test:

    # setup_method method. establishes db connection for testing.
    def setup_method(self):
        """
        :return:N/A
        """
        self.db = get_db()

    # test_init method. loads csv data into database tables.
    def test_init(self):
        """
        :return: N/A
        """
        db.load_predefined_habits(self.db, )
        db.load_completion_data(self.db, )

    # test_time_freeze method. verifies time freeze extension is running.
    @freeze_time("2022-10-28 09:11:11")
    def test_time_freeze(self):
        """
        :return: N/A
        """
        assert datetime.now() == datetime(2022, 10, 28, 9, 11, 11)

    # test_show_daily_habits method. shows all daily habits of test data and compares output to expectation.
    def test_show_daily_habits(self):
        """
        :return: returns true if successfull / false if failed.
        """
        all_daily_habits = ("Diary writing, Walking the dog")
        return_habits = analyse.get_all_habits_with_periodicity(self.db, "Daily", )
        assert all_daily_habits == return_habits

    # test_show_weekly_habits method. shows all weekly habits of test data and compares output ot expectation.
    def test_show_weekly_habits(self):
        """
        :return: returns true if successfull / false if failed.
        """
        all_weekly_habits = ("Jogging, Meditation, Plan your week, Singing")
        return_habits = analyse.get_all_habits_with_periodicity(self.db, "Weekly", )
        assert all_weekly_habits == return_habits

    # test_current_active_habits method. shows all currently active habits of test data and compares output to
    # expectation. Freezes time with freezegun to establish continious testing verification.
    @freeze_time("2022-10-28 09:11:11")
    def test_current_active_habits(self):
        """
        :return: returns true if successfull / false if failed.
        """
        cutoff_date = datetime.now()
        all_currently_active_habits = ("Diary writing, Jogging, Meditation, Walking the dog, Plan your week")
        return_currently_active_habits = analyse.get_current_active_habits(self.db, cutoff_date, )
        assert all_currently_active_habits == return_currently_active_habits

    # test_show_max_streak_of_all_habits method. shows overall record streak. compares output to expectation.
    def test_show_max_streak_of_all_habits(self):
        """
        :return: returns true if successfull / false if failed.
        """
        max_streak = ("28 from Diary writing")
        return_max_streak = analyse.get_record_streak_from_all_habits(self.db,)
        assert max_streak == return_max_streak

    # test_show_all_max_streaks method. shows all longest streaks for test data habits. compares return to expectation.
    def test_show_all_max_streaks(self):
        """
        :return: returns true if successfull / false if failed.
        """
        all_max_streak = "('Diary writing', 28), ('Jogging', 2), ('Meditation', 4), ('Walking the dog', 25), " \
                         "('Plan your week', 4), ('Singing', 2)"
        return_all_max_streaks = analyse.get_all_longest_streaks(self.db,)
        assert all_max_streak == return_all_max_streaks

    # test_get_longest_streak_specific method. get a specific longest streak of a habit. compares return to expectation.
    def test_get_longest_streak_specific(self):
        """
        :return: returns true if successfull / false if failed.
        """
        longest_streak = 4
        return_longest_streak = analyse.get_longest_streak(self.db, "Meditation", )
        assert longest_streak == return_longest_streak

    # test_show_all_specific_data method. shows all habit data for a specific habit. compares return to expectation.
    def test_show_all_specific_data(self):
        """
        :return: returns true if successfull / false if failed.
        """
        specific_data = "('Daily', '2022-10-01 16:14:39.215689', '2022-10-01 16:14:39.215689', " \
                        "'2022-28-10 16:14:39.215689', '2022-10-29 16:14:39.215689', 28, 28)"
        return_specific_data = analyse.get_all_specific_data(self.db, "Diary writing", )
        assert specific_data == return_specific_data

    # test_show_all_habit_data method. shows all habit data. compares return to expectation.
    def test_show_all_habit_data(self):
        """
        :return: returns true if successfull / false if failed.
        """
        all_data = [('Diary writing', 'Daily', '2022-10-01 16:14:39.215689', '2022-10-01 16:14:39.215689',
                     '2022-28-10 16:14:39.215689', '2022-10-29 16:14:39.215689', 28, 28),
                    ('Jogging', 'Weekly', '2022-10-02 16:14:39.215689', '2022-10-23 16:14:39.215689',
                     '2022-23-10 16:14:39.215689', '2022-10-30 16:14:39.215689', 1, 2),
                    ('Meditation', 'Weekly', '2022-10-01 16:14:39.215689', '2022-10-01 16:14:39.215689',
                     '2022-22-10 16:14:39.215689', '2022-10-29 16:14:39.215689', 4, 4),
                    ('Walking the dog', 'Daily', '2022-10-01 16:14:39.215689', '2022-10-27 16:14:39.215689',
                     '2022-28-10 16:14:39.215689', '2022-10-29 16:14:39.215689', 2, 25),
                    ('Plan your week', 'Weekly', '2022-10-01 16:14:39.215689', '2022-10-01 16:14:39.215689',
                     '2022-22-10 16:14:39.215689', '2022-10-29 16:14:39.215689', 4, 4),
                    ('Singing', 'Weekly', '2022-10-01 16:14:39.215689', '2022-20-01 16:14:39.215689',
                     '2022-20-10 16:14:39.215689', '2022-10-27 16:14:39.215689', 0, 2)]

        return_all_data = analyse.get_all_habit_data(self.db, )
        assert all_data == return_all_data

    # test_create_new_habit method. creates a new habit in test data. compares return show all to expectation.
    # time is froozen to run continiously fine with freezegun.
    @freeze_time("2022-10-28 09:11:11")
    def test_create_new_habit(self):
        """
        :return: returns true if successfull / false if failed.
        """
        name = "No drinking"
        periodicity = "Daily"
        created_on = datetime.today()
        started_on = datetime.today()
        completed_on = datetime.today()
        due_on = datetime.today() - timedelta(days=1)
        current_streak = 0
        longest_streak = 0
        db.add_new_habit_to_table_complete(self.db, name, periodicity, created_on, started_on, completed_on, due_on,
                                           current_streak, longest_streak, )

        new_all_data = [('Diary writing', 'Daily', '2022-10-01 16:14:39.215689', '2022-10-01 16:14:39.215689',
                     '2022-28-10 16:14:39.215689', '2022-10-29 16:14:39.215689', 28, 28),
                    ('Jogging', 'Weekly', '2022-10-02 16:14:39.215689', '2022-10-23 16:14:39.215689',
                     '2022-23-10 16:14:39.215689', '2022-10-30 16:14:39.215689', 1, 2),
                    ('Meditation', 'Weekly', '2022-10-01 16:14:39.215689', '2022-10-01 16:14:39.215689',
                     '2022-22-10 16:14:39.215689', '2022-10-29 16:14:39.215689', 4, 4),
                    ('Walking the dog', 'Daily', '2022-10-01 16:14:39.215689', '2022-10-27 16:14:39.215689',
                     '2022-28-10 16:14:39.215689', '2022-10-29 16:14:39.215689', 2, 25),
                    ('Plan your week', 'Weekly', '2022-10-01 16:14:39.215689', '2022-10-01 16:14:39.215689',
                     '2022-22-10 16:14:39.215689', '2022-10-29 16:14:39.215689', 4, 4),
                    ('Singing', 'Weekly', '2022-10-01 16:14:39.215689', '2022-20-01 16:14:39.215689',
                     '2022-20-10 16:14:39.215689', '2022-10-27 16:14:39.215689', 0, 2),
                    ('No drinking', 'Daily', '2022-10-28 09:11:11', '2022-10-28 09:11:11',
                     '2022-10-28 09:11:11', '2022-10-27 09:11:11', 0, 0)]

        return_all_data = analyse.get_all_habit_data(self.db, )

        assert return_all_data == new_all_data

    # test_delete_habit method. deletes habit in test data. compares return show all to expectation.
    # time is froozen to run continiously fine with freezegun.
    @freeze_time("2022-10-28 09:11:11")
    def test_delete_habit(self):
        """
        :return: returns true if successfull / false if failed.
        """
        name = "No drinking"
        db.delete_habit_from_table(self.db, name, )

        new_all_data = [('Diary writing', 'Daily', '2022-10-01 16:14:39.215689', '2022-10-01 16:14:39.215689',
                         '2022-28-10 16:14:39.215689', '2022-10-29 16:14:39.215689', 28, 28),
                        ('Jogging', 'Weekly', '2022-10-02 16:14:39.215689', '2022-10-23 16:14:39.215689',
                         '2022-23-10 16:14:39.215689', '2022-10-30 16:14:39.215689', 1, 2),
                        ('Meditation', 'Weekly', '2022-10-01 16:14:39.215689', '2022-10-01 16:14:39.215689',
                         '2022-22-10 16:14:39.215689', '2022-10-29 16:14:39.215689', 4, 4),
                        ('Walking the dog', 'Daily', '2022-10-01 16:14:39.215689', '2022-10-27 16:14:39.215689',
                         '2022-28-10 16:14:39.215689', '2022-10-29 16:14:39.215689', 2, 25),
                        ('Plan your week', 'Weekly', '2022-10-01 16:14:39.215689', '2022-10-01 16:14:39.215689',
                         '2022-22-10 16:14:39.215689', '2022-10-29 16:14:39.215689', 4, 4),
                        ('Singing', 'Weekly', '2022-10-01 16:14:39.215689', '2022-20-01 16:14:39.215689',
                         '2022-20-10 16:14:39.215689', '2022-10-27 16:14:39.215689', 0, 2)]

        return_all_data = analyse.get_all_habit_data(self.db, )

        assert return_all_data == new_all_data

