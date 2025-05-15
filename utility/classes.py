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
        new_habit = new_habit.lower().strip()
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
        if new_habit not in self.habit_dict.keys():# If it is not present in the habit_dict
            if re.search(self.UNACCEPTED_CHARS, new_habit + desc):# If the regex of unaccepted characters matches the habit_name or the description
                list_of_unaccepted_chars = re.findall(self.UNACCEPTED_CHARS, new_habit + desc)# get a list of those characters
                list_of_unaccepted_chars = list(set(list_of_unaccepted_chars)) # remove duplicates from the list
                unaccepted_chars_message = 'Uh oh! Your habit nam and/or description contains unsupported characters!\nThe characters in question are:\n' # base error message for unaccepted chars
                unaccepted_chars_message += list_of_unaccepted_chars.pop(0) # remove the first item of the unaccepted chars and add to the message: this is to ensure char, char, char, not , char, char, char
                for char in list_of_unaccepted_chars:
                    unaccepted_chars_message += ', ' + char# add every other char to the list as ', char'
                sg.popup(unaccepted_chars_message, keep_on_top=True)
                return 'THROW_UNACCEPTED_CHARS'
            else:
                self.habit_dict[new_habit] = [desc, count, None]
                return 0
        else: 
            sg.popup(f'Habit "{new_habit}" already in system. Edit habit data to change existing ')
    
    def update_habit(self, habit, new_habit_name, desc):# update the stuff about a habit
            new_habit_name = new_habit_name.lower().strip()
            count = self.habit_dict[habit][1] # keep the count the same, because otherwise this can be farmed.
            prevdate = self.habit_dict[habit][2] # prevdate is same, because I'm not letting people exploit this
            if len(new_habit_name) < 4:# If the name is too short
                sg.popup(f'Habit name "{new_habit_name}" too short. \nMust have 4-25 characters', keep_on_top=True)
                return habit
            if len(new_habit_name) > 25:# If the name is too long
                sg.popup(f'Habit name "{new_habit_name}" too long. \nMust have 4-25 characters', keep_on_top=True)
                return habit
            if new_habit_name == 'no habit selected':
                sg.popup(f'Habit name {new_habit_name} illegal. Try again', keep_on_top=True)
                return habit
            if re.search(self.UNACCEPTED_CHARS, new_habit_name + desc):# If the regex of unaccepted characters matches the habit_name or the description
                list_of_unaccepted_chars = re.findall(self.UNACCEPTED_CHARS, new_habit_name + desc)# get a list of those characters
                list_of_unaccepted_chars = list(set(list_of_unaccepted_chars)) # remove duplicates from the list
                unaccepted_chars_message = 'Uh oh! Your habit name and/or description contains unsupported characters!\nThe characters in question are:\n' # base error message for unaccepted chars
                unaccepted_chars_message += list_of_unaccepted_chars.pop(0) # remove the first item of the unaccepted chars and add to the message: this is to ensure char, char, char, not , char, char, char
                for char in list_of_unaccepted_chars:
                    unaccepted_chars_message += ', ' + char # Add every other character to the list as ', <char>'
                sg.popup(unaccepted_chars_message, keep_on_top=True)
                return habit
            new_habit_name = new_habit_name.lower().strip()
            desc = desc.strip()
            self.habit_dict.pop(habit) # remove the old habit
            if new_habit_name in self.habit_dict:
                sg.popup(f'Habit name "{new_habit_name}" is already taken.\nChoose a new name')
                self.habit_dict[habit] = [desc, count, prevdate] # Add the new info under the old habit_name
                return habit
            self.habit_dict[new_habit_name] = [desc, count, prevdate] # fill into habit_dict as in {habit: [desc, count, prevdate]}
            return new_habit_name # Return the new name so selected_habit works
                
    def inc_habit(self, habit):# Increment the usage of a habit
        habit = habit.lower().strip()
        if habit in self.habit_dict.keys():
            if self.habit_dict[habit][2] == None:# If the last done date is None (just initialized)
                self.habit_dict[habit][1] = 1# Set streak to one
                self.habit_dict[habit][2] = datetime.date.today()# Set last done date to today
            else:
                end_streak_date = self.habit_dict[habit][2] + datetime.timedelta(days=1)
                if end_streak_date < datetime.date.today():
                    self.habit_dict[habit][1] = 1 # make streak 1: resetted
                    self.habit_dict[habit][2] = datetime.date.today()# add last time was streaked
                    sg.popup('Oh NO! You lost your streak for this habit!\nNext time, make sure you mark this as done EVERY DAY!\nCheers!', keep_on_top=True)
                else:
                    self.habit_dict[habit][1] += 1 # increment streak
                    self.habit_dict[habit][2] = datetime.date.today()
    

    def del_habit(self, habit):
        habit = habit.lower().strip()
        self.habit_dict.pop(habit)


    def print_habits(self):# print to the user all of the habits
        print('All habits logged: ')
        for key in self.habit_dict:
            desc = self.habit_dict[key][0]
            count = self.habit_dict[key][1]
            prevdate = self.habit_dict[key][2]
            print(f'  * Habit; {key} \n   > Description: {desc}\n   > Streak: {count}\n   >Last Done: {prevdate}')