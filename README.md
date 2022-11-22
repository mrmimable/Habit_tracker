# My Habit Tracker App

The habit tracker enables you to track your own habits.

## General

It is an object oriented backend programmed in python that's usable via the terminal console.

It enables you to create, delete, change, complete your individual habits.
If a user completes a habit multiple times in a row it will be counted as a streak.

If more information is needed there are numerous analytical functions implemented that return
important information for the user.

## Installation information
### Technical requirements:
Install Python 3.7 or later on your computer.

### First setup
In order to run the tracker properly please do the following first.
In your terminal console please install the necessary requirements packages via:

```shell
pip install -r requirements.txt
```
This will install the following required packages for the tracker:

- questionary (user questionary and choices)

- pytest (testing extension)

- freezegun (time freezing for testing)

## Usage information

The tracker can be started by typing the following command in your terminal console:
```shell
python main.py
```
Simply follow the instructions in the terminal.

## Functionalities
### 1. Create a new habit
User can create a new habit from scratch. 
- The user needs to input a new unique name for the habit and define
a periodicity of either Daily or Weekly for the habit.
---
### 2. Delete a habit
Delete an existing habit. 
- User inputs name of the habit to be deleted.

---
### 3. Change a habit
User inputs the name of the habit to be changed. Then chooses if name or periodicity has to be changed.
#### 3.1 Name change
- User defines new unique name for the habit.
#### 3.2 Periodicity change
- Warning this will reset the habit data. (dates and streaks are reset to 0)
- If confirmed: User defines new periodicity (Daily or Weekly).

---
### 4. Complete a habit
- User inputs name of the habit to be marked as completed.

- If a habit has been completed multiple times in the defined periodicity it will be count as a streak.

- A streak will be broken if a due date is missed and the habit therefore was not marked as completed in the given time
period.

- Tracker will automatically update necessary dates and streaks if applicable.

---

Exit habit tracker will close the tracker application.

---
### 5. Analyse your habits
Will open new menu with following functions:

#### 5.1 List all currently active habits
- Displays a list of currently active habits.
#### 5.2 List all habits with a periodicity
- Displays all habits with the periodicity Daily or Weekly. 
- User inputs periodicity chosen.
#### 5.3 Show overall record streak
- Shows the longest streak of all habits and the habit that achieved it
#### 5.4 Longest streak for all habits
- Displays all habits and their longest streaks. 
#### 5.5 Longest streak for a specific habit
- Displays the longest streak for a specific habit. 
- User inputs name of the habit.
#### 5.6 Show all habit data
- Shows all available habit data
#### 5.7 Show all data for a specific habit
- Shows all habit data for a specific habit. 
- User inputs name of the habit to be displayed. 
#### 5.8 Show all completion data
- Shows all completion data.
#### 5.9 Load predefined data
- User can manually load predefined habits and progress data into tracker.
#### 5.10 Return to menu
- Return to main menu.

---
## Test habit tracker with pytest
If needed a testing function can be run for the tracker to check the functionality of the tracker.

### Important notice:
To run this test successfully you first have to manually delete the file "main.db" from the project.

This will delete all your new habits and data from the project and database. This cannot be undone.

Once "main.db" file has been deleted input the following command in the console terminal.
```shell
pytest
```

For more information please consider looking into the test_project.py code descriptions.

## Additional information
To understand the code and logic better have a look at the UML file: "Habit_tracker_UML" in the project folder.

For more specific information feel free to have a look into the code and commands and descriptions.
