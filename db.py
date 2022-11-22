"""
db.py covers building of the database main.db. create the tables habits_data & completion_data.
defines all necessary methods for reading and writing queries to and from the database.
database is build with sqlite3.
"""

import sqlite3


# get_db method create database and connections with sqlite3
def get_db(name="main.db"):
    db = sqlite3.connect(name)
    create_tables(db)
    return db


# create_tables method. create tables habits_data and completion_data if not exists.
def create_tables(db):
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS habits_data (
        name TEXT PRIMARY KEY,
        periodicity TEXT,
        created_on DATETIME,
        started_on DATETIME,
        completed_on DATETIME,
        due_on DATETIME,
        current_streak INTEGER,
        longest_streak INTEGER
        )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS completion_data (
            name TEXT,
            periodicity TEXT,
            completed_on DATETIME
            )""")
    db.commit()


# Write to DB methods
"""
Included methods are: 
add_new_habit_to_table_complete(db, name, periodicity, created_on, started_on, completed_on, due_on, current_streak,
                                    longest_streak, )
    adds new habit to habits_data
delete_habit_from_table(db, name, )
    deletes a habit from habits_data
update_name(db, name, newname, )
    updates name of a habit in habits_data
update_periodicity(db, name, periodicity, )
    updates periodicity of a habit in habits_data     
update_created_date(db, name, created_on, )
    updates created date of a habit in habits_data
update_due_date(db, name, due_on, )
    update due date of a habit in habits_data   
update_start_date(db, name, start_on, )
    update start date of  a habit in habits_data
update_completed_date(db, name, completed_on, )
    update completed date of a habit in habits_data
update_progress_data(db, name, completed_on, )
    update progress data in progress_data
update_current_streak(db, name, current_streak, )
    update current streak of a habit in habits_data
update_longest_streak(db, name, longest_streak, )
    update longest streak of a  habit in habits_data
"""


# add_new_habit_to_table_complete method. tries to add new habit to table habits_data. returns 1 if habit already exists
def add_new_habit_to_table_complete(db, name, periodicity, created_on, started_on, completed_on, due_on, current_streak,
                                    longest_streak, ):
    """
    :param db: db link
    :param name: name of the new habit
    :param periodicity: periodicity of the new habit (Daily or Weekly)
    :param created_on: Created on date of the new habit
    :param started_on: Started on date of the new habit
    :param completed_on: Completed on date of the new habit
    :param due_on: Due on of the new habit
    :param current_streak: Current streak of the new habit
    :param longest_streak: Longest streak of the new habit
    :return: successfull = 0 / failed = 1 (habit name already exists)
    """
    try:
        cur = db.cursor()
        cur.execute("INSERT INTO habits_data VALUES (?,?,?,?,?,?,?,?)",
                    (name, periodicity, created_on, started_on, completed_on, due_on, current_streak, longest_streak, ))
        db.commit()
    except sqlite3.Error:
        return 1


# delete_habit_from_table method. deletes an existing habit from habits_data.
def delete_habit_from_table(db, name, ):
    """
    :param db: db link
    :param name: name of the habit to be deleted from habits_data
    :return: N/A
    """
    cur = db.cursor()
    cur.execute(f"DELETE FROM habits_data WHERE name = '{name}'")
    db.commit()


# update_name method. updates the name of an existing habit in habits_data.
def update_name(db, name, newname, ):
    """
    :param db: db link
    :param name: existing name of the habit to be changed in habits_data
    :param newname: new name of the habit
    :return: N/A
    """
    cur = db.cursor()
    cur.execute(f"UPDATE habits_data set name = '{newname}' WHERE name = '{name}'")
    db.commit()


# update_periodicity method. updates periodicity of an existing habit in habits_data.
def update_periodicity(db, name, periodicity, ):
    """
    :param db: db link
    :param name: name of the habit in habits_data
    :param periodicity: new periodicity of the habit (Daily or Weekly)
    :return: N/A
    """
    cur = db.cursor()
    cur.execute(f"UPDATE habits_data set periodicity = '{periodicity}' WHERE name = '{name}'")
    db.commit()


# update_created_date method. updates created date of a habit in habits_data.
def update_created_date(db, name, created_on, ):
    """
    :param db: db link
    :param name: name of the habit to be updated in habits_data
    :param created_on: new created_on date.
    :return: N/A
    """
    cur = db.cursor()
    cur.execute(f"UPDATE habits_data set created_on = '{created_on}' WHERE name = '{name}'")
    db.commit()


# update_due_date method. updates due date of an existing habit in habits_data.
def update_due_date(db, name, due_on, ):
    """
    :param db: db link
    :param name: name of the habit to be updated in habits_data
    :param due_on: new due_on date
    :return: N/A
    """
    cur = db.cursor()
    cur.execute(f"UPDATE habits_data set due_on = '{due_on}' WHERE name = '{name}'")
    db.commit()


# update_start_date method. updates start date of an existing habit in habits_data.
def update_start_date(db, name, start_on, ):
    """
    :param db: db link
    :param name: name of the habit to be updated in habits_data
    :param start_on: new start_on date.
    :return: N/A
    """
    cur = db.cursor()
    cur.execute(f"UPDATE habits_data set started_on = '{start_on}' WHERE name = '{name}'")
    db.commit()


# update_completed_date method. updates completed date of an existing habit in habits_data.
def update_completed_date(db, name, completed_on, ):
    """
    :param db: db link
    :param name: name of the habit to be updated in habits_data
    :param completed_on: new completed_on date.
    :return: N/A
    """
    cur = db.cursor()
    cur.execute(f"UPDATE habits_data set completed_on = '{completed_on}' WHERE name = '{name}'")


# update_progress_data method. creates new entry in progress_data after it fetches periodicity from habits_data.
def update_progress_data(db, name, completed_on, ):
    """
    :param db: db link
    :param name: name of the habit for which a completion entry has to be created in progress_data.
    :param completed_on: completed_on date for entry in progress_data
    :return: N/A
    """
    cur = db.cursor()
    cur.execute(f"SELECT periodicity FROM habits_data WHERE name = '{name}'")
    periodicity = ''.join(cur.fetchone())
    cur.execute("INSERT INTO completion_data VALUES (?,?,?)",
                (name, periodicity, completed_on, ))

    db.commit()


# update_current_streak method. updates current streak for a habit in habits_data.
def update_current_streak(db, name, current_streak, ):
    """
    :param db: db link
    :param name: name of the habit for which the current streak has to be updated in habits_data
    :param current_streak: new current streak for the habit
    :return: N/A
    """
    cur = db.cursor()
    cur.execute(f"UPDATE habits_data set current_streak = '{current_streak}' WHERE name = '{name}'")
    db.commit()


# update_longest_streak method. updates longest streak for a habit in habits_data.
def update_longest_streak(db, name, longest_streak, ):
    """
    :param db: db link
    :param name: name of the habit for which the longest streak has to be updated in habits_data
    :param longest_streak: new longest streak for the habit
    :return: N/A
    """
    cur = db.cursor()
    cur.execute(f"UPDATE habits_data set longest_streak = '{longest_streak}' WHERE name = '{name}'")
    db.commit()


# Read from DB methods
"""
Included methods are: 
verify_habit_exists(db, name, )
    verifies a habit exists in habits_data
get_periodicity(db, name, )
    get periodicity of a habit in habits_data
get_start_on(db, name, )
    get start on date of a habit in habits_data
get_due_on(db, name, )
    get due on date a habit in habits_data
get_completed_on(db, name, )
    get completed on date a habit in habits_data
get_created_on(db, name, )
    get created on date a habit in habits_data
get_current_streak(db, name, )
    get current streak a habit in habits_data
get_longest_streak(db, name, )
    get longest streak a habit in habits_data
get_current_active_habits(db, cutoff_date, )
    return a list of all currently active habits in habits_data
get_record_streak_from_all_habits(db, )
    get record streak from all habits in habits_data
get_all_longest_streaks(db, )
    return all longest streaks for all habits in habits_data
get_all_habits_with_periodicity(db, periodicity, )
    return all habits with a periodicity (Daily or Weekly) from habits_data.
get_all_habit_data(db, )
    returns all habits data form habits_data.
get_all_completion_data(db, )
    returns all progression data from completion_data
get_all_specific_data(db, name, )
    returns all data for a specific habit in habits_data.
"""


# verify_habit_exists method. checks if a habit exists in habits_data.
def verify_habit_exists(db, name, ):
    """
    :param db: link
    :param name: name of the habit to be checked for existence in habits_data
    :return: return name if exists. return None if not exists.
    """
    cur = db.cursor()
    cur.execute(f"SELECT name FROM habits_data WHERE name = '{name}'")
    return cur.fetchone()


# get_periodicity method. gets periodicity of a habit in habits_data.
def get_periodicity(db, name, ):
    """
    :param db: db link
    :param name: name of the habit to get periodicity in habits_data.
    :return: returns periodicity (Daily or Weekly).
    """
    cur = db.cursor()
    cur.execute(f"SELECT periodicity FROM habits_data WHERE name = '{name}'")
    returnval = ''.join(cur.fetchone())
    return returnval


# get_start_on method. gets start date of a habit in habits_data.
def get_start_on(db, name, ):
    """
    :param db: db link
    :param name: name of the habit to get started on date from in habits_data.
    :return: returns started on date.
    """
    cur = db.cursor()
    cur.execute(f"SELECT started_on FROM habits_data WHERE name = '{name}'")
    returnval = ''.join(cur.fetchone())
    return returnval


# get_due_on method. gets due on date of a habit in habits_data.
def get_due_on(db, name, ):
    """
    :param db: db link
    :param name: name of the habit to get due on date from in habits_data.
    :return: returns due on date.
    """
    cur = db.cursor()
    cur.execute(f"SELECT due_on FROM habits_data WHERE name = '{name}'")
    returnval = ''.join(cur.fetchone())
    return returnval


# get_completed_on method. gets completed on date of a habit in habits_data.
def get_completed_on(db, name, ):
    """
    :param db: db link
    :param name: name of the habit to get completed on date from in habits_data.
    :return: returns completed on date.
    """
    cur = db.cursor()
    cur.execute(f"SELECT completed_on FROM habits_data WHERE name = '{name}'")
    returnval = ''.join(cur.fetchone())
    return returnval


# get_created_on method. gets created on date of a habit in habits_data.
def get_created_on(db, name, ):
    """
    :param db: db link
    :param name: name of the habit to get created on date from in habits_data.
    :return: returns created on date.
    """
    cur = db.cursor()
    cur.execute(f"SELECT created_on FROM habits_data WHERE name = '{name}'")
    returnval = ''.join(cur.fetchone())
    return returnval


# get_current_streak method. gets current streak value of a habit in habits_data.
def get_current_streak(db, name, ):
    """
    :param db: db link
    :param name: name of the habit to get current streak value from in habits_data.
    :return: returns current streak value.
    """
    cur = db.cursor()
    cur.execute(f"SELECT current_streak FROM habits_data WHERE name = '{name}'")
    returnval = int(cur.fetchone()[0])
    return returnval


# get_longest_streak method. gets longest streak value of a habit in habits_data.
def get_longest_streak(db, name, ):
    """
    :param db: db link
    :param name: name of the habit to get longest streak value from in habits_data.
    :return: returns longest streak value.
    """
    cur = db.cursor()
    cur.execute(f"SELECT longest_streak FROM habits_data WHERE name = '{name}'")
    returnval = int(cur.fetchone()[0])
    return returnval


# get_current_active_habits method. gets a list of all currently active habits from habits_data. currently active
# means due date in habits_data bigger equal cutoff_date(today)
def get_current_active_habits(db, cutoff_date, ):
    """
    :param db: db link
    :param cutoff_date: cutoff date to consider when comparing to due dates in habits_data.
    :return: returns all habits that are currently active (due date >= cutoff date).
    """
    cur = db.cursor()
    cur.execute(f"SELECT name FROM habits_data WHERE due_on >= '{cutoff_date}'")
    returnvalue = cur.fetchall()
    returnvalue = ', '.join("%s" % tup for tup in returnvalue)
    return returnvalue


# get_record_streak_from_all_habits method. gets max value of longest streak for all habits in habits_data.
# returns record streak value and name of the habit.
def get_record_streak_from_all_habits(db, ):
    """
    :param db: db link
    :return: returns record streak and name of the habit form habits_data.
    """
    cur = db.cursor()
    cur.execute(f"SELECT max(longest_streak) FROM habits_data ")
    returnvalue = cur.fetchall()
    returnvalue = ', '.join("%s" % tup for tup in returnvalue)
    cur.execute(f"SELECT name FROM habits_data WHERE longest_streak = '{returnvalue}'")
    returnvalue2 = cur.fetchall()
    returnvalue2 = ', '.join("%s" % tup for tup in returnvalue2)
    returnvalue = str(returnvalue + " from " + returnvalue2)
    return returnvalue


# get_all_longest_streaks method. gets all names and longest streak for all habits in habits_data.
def get_all_longest_streaks(db, ):
    """
    :param db: db link
    :return: returns all habits and their longest streaks from habits_data.
    """
    cur = db.cursor()
    cur.execute(f"SELECT name,longest_streak FROM habits_data ")
    returnvalue = str(cur.fetchall())
    returnvalue = returnvalue.strip("[]'")
    return returnvalue


# get_all_habits_with_periodicity method. gets all habits name from habits_data where periodicity Daily or Weekly.
def get_all_habits_with_periodicity(db, periodicity, ):
    """
    :param db: db link
    :param periodicity: periodicity (Daily or Weekly) on which habits are returned from habits_data.
    :return: returns a list of all names of the habits with the periodicity defined from habits_data.
    """
    cur = db.cursor()
    cur.execute(f"SELECT name FROM habits_data WHERE periodicity = '{periodicity}'")
    returnvalue = cur.fetchall()
    returnvalue = ', '.join("%s" % tup for tup in returnvalue)
    return returnvalue


# get_all_habit_data method. gets all data from habits_data.
def get_all_habit_data(db, ):
    """
    :param db: db link
    :return: returns all habit data from habits_data.
    """
    cur = db.cursor()
    cur.execute(f"SELECT * FROM habits_data")
    names = ' ¦ '.join(list(map(lambda x: x[0], cur.description)))
    print(names)
    returnvalue = cur.fetchall()
    return returnvalue


# get_all_completion_data method. gets all data from completion_data.
def get_all_completion_data(db, ):
    """
    :param db: db link
    :return: returns all habit data from completion_data.
    """
    cur = db.cursor()
    cur.execute(f"SELECT * FROM completion_data")
    names = ' ¦ '.join(list(map(lambda x: x[0], cur.description)))
    print(names)
    returnvalue = cur.fetchall()
    return returnvalue


# get_all_specific_data method. gets all data for a specific habit in habits_data.
def get_all_specific_data(db, name, ):
    """
    :param db: db link
    :param name: name of the habit from which to get all data in habits_data.
    :return: returns all habits data from habits_data for the specified habit.
    """
    cur = db.cursor()
    cur.execute(f"SELECT * FROM habits_data")
    names = ' ¦ '.join(list(map(lambda x: x[0], cur.description)))

    print(names)
    cur.execute(f"SELECT periodicity, created_on, started_on, completed_on, due_on, current_streak, longest_streak"
                f" FROM habits_data WHERE name = '{name}'")
    returnval = ''.join(str(cur.fetchone()))
    return returnval


# Loading functions of csv data.
"""
Included methods are: 
load_completion_data(db, )
    loads completion data from completion_data.csv
load_predefined_habits(db, )
    loads predefined data from predefined_data.csv
"""


# load_completion_data method. loads all data from completion_data.csv into completion_data table.
def load_completion_data(db, ):
    """
    :param db: db link
    :return: returns error if data is already loaded into db.
    """
    import csv
    cur = db.cursor()

    with open('completion_data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        try:
            for row in csv_reader:
                cur.execute("INSERT INTO completion_data VALUES (?,?,?)",
                            (row[0], row[1], row[2], ))
                db.commit()

                print(row)

        except sqlite3.Error:
            print("Sqlite3 Error. Data is already loaded into db")


# load_predefined_habits method. loads predefined data from predefined_data.csv into habits_data.
def load_predefined_habits(db, ):
    """
    :param db: db link
    :return: returns error if data is already loaded into db.
    """
    import csv
    cur = db.cursor()

    with open('predefined_data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        try:
            for row in csv_reader:
                cur.execute("INSERT INTO habits_data (name,periodicity,created_on,started_on,completed_on,due_on,"
                            "current_streak,longest_streak) VALUES (?,?,?,?,?,?,?,?)",
                            (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
                db.commit()

                print(row)

        except sqlite3.Error:
            print("Sqlite3 Error. Predefined habits data is already loaded into db")
