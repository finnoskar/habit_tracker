"""
Page used to store 'Habits' class
Supports main.py
"""
import PySimpleGUI as sg
import datetime
import re

class Habits:

    def __init__(self):# intitiate Habits 
        self.habit_dict = {} # define the dict
        self.UNACCEPTED_CHARS = re.compile(r'[^a-zA-Z0-9!$%()\-=+?\/\'":;,. \r?\n]')
    
    def add_habit(self, new_habit, desc):
        """
        METHOD to add a habit to the habit dictionary
        PARAMS
        new_habit
        -- 
        """
        count = 0
        progress = 0
        new_habit = new_habit.strip()
        if not new_habit:
            sg.popup('No habit input. Please add a habit name', keep_on_top=True)
            return 'THROW_NO_HABIT_NAME'
        if len(new_habit) < 4: # habit name too short (<3 characters)
            sg.popup(f'Habit {new_habit} too short. \nMust have 4-25 characters', keep_on_top=True)
            return 'THROW_HABIT_TOO_SHORT'
        if len(new_habit) > 25: # Habit name too long (>15 characters)
            sg.popup(f'Habit {new_habit} too long. \nMust have 4-25 characters', keep_on_top=True)
            return 'THROW_HABIT_TOO_LONG'
        if new_habit == 'no habit selected':
            sg.popup(f'Habit {new_habit} illegal. Try again.', keep_on_top=True)
            return 'THROW_ILLEGAL_NAME'
        lowered_keys = [list(self.habit_dict.keys())[i].lower() for i in range(len(self.habit_dict))]
        if new_habit.lower() not in lowered_keys:# If it is not present in the habit_dict (checking as lower case to remove case duplicates)
            self.habit_dict[new_habit] = [desc, count, None, progress]
            return 0
        else: 
            sg.popup(f'Habit "{new_habit}" already in system. Edit habit data to change existing ')
    
    def update_habit(self, habit, new_habit_name, desc):# update the stuff about a habit
            new_habit_name = new_habit_name.strip()
            count = self.habit_dict[habit][1] # keep the count the same, because otherwise this can be farmed.
            prevdate = self.habit_dict[habit][2] # prevdate is same, because I'm not letting people exploit this
            progress = self.habit_dict[habit][3]
            if len(new_habit_name) < 4:# If the name is too short
                sg.popup(f'Habit name "{new_habit_name}" too short. \nMust have 4-25 characters', keep_on_top=True)
                return habit
            if len(new_habit_name) > 25:# If the name is too long
                sg.popup(f'Habit name "{new_habit_name}" too long. \nMust have 4-25 characters', keep_on_top=True)
                return habit
            if new_habit_name == 'no habit selected':
                sg.popup(f'Habit name {new_habit_name} illegal. Try again', keep_on_top=True)
                return habit
            desc = desc.strip()
            self.habit_dict.pop(habit) # remove the old habit
            lowered_keys = [list(self.habit_dict.keys())[i].lower() for i in range(len(self.habit_dict))]
            if new_habit_name.lower() in lowered_keys:
                sg.popup(f'Habit name "{new_habit_name}" is already in system.\nChoose a new name')
                self.habit_dict[habit] = [desc, count, prevdate, progress] # Add the new info under the old habit_name
                return habit
            self.habit_dict[new_habit_name] = [desc, count, prevdate, progress] # fill into habit_dict as in {habit: [desc, count, prevdate, progress]}
            return new_habit_name # Return the new name so selected_habit works
                
    def inc_habit(self, habit):# Increment the usage of a habit
        habit = habit.strip()
        if habit in self.habit_dict.keys():
            if self.habit_dict[habit][2] == None:# If the last done date is None (just initialized)
                self.habit_dict[habit][1] = 1# Set streak to one
                self.habit_dict[habit][2] = datetime.date.today()# Set last done date to today
                self.habit_dict[habit][3] = 1
            else:
                end_streak_date = self.habit_dict[habit][2] + datetime.timedelta(days=1)
                if end_streak_date < datetime.date.today():
                    self.habit_dict[habit][1] = 1 # make streak 1: resetted
                    self.habit_dict[habit][2] = datetime.date.today()# add last time was streaked
                    sg.popup('You lost your streak for this habit!\nNext time, make sure you mark this as done every day in order to maintain your streak', keep_on_top=True)
                else:
                    self.habit_dict[habit][1] += 1 # increment streak
                    if self.habit_dict[habit][3] == 7:
                        self.habit_dict[habit][3] = 1
                    elif self.habit_dict[habit][3] < 7:
                        self.habit_dict[habit][3] += 1
                    self.habit_dict[habit][2] = datetime.date.today()
    

    def del_habit(self, habit):
        habit = habit.strip()
        self.habit_dict.pop(habit)


    def print_habits(self):# print to the user all of the habits
        print('All habits logged: ')
        for key in self.habit_dict:
            desc = self.habit_dict[key][0]
            count = self.habit_dict[key][1]
            prevdate = self.habit_dict[key][2]
            print(f'  * Habit; {key} \n   > Description: {desc}\n   > Streak: {count}\n   >Last Done: {prevdate}')