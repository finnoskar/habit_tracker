"""
Yo Python App: Habit Tracker

INPUT: commit habits, note that you have completed habit
PROCESS: commits habits to rawtext saved in data.txt, so they save between sessions
OUTPUT: Tasks shown, digital interface
"""

import os
import datetime
from utility import func
from utility.classes import Habits
import PySimpleGUI as sg
import re

def main():
    """The Main Process Function"""
    sg.ChangeLookAndFeel('LightBlue3')
    habit_data = Habits() # Instantiate habit_data
    func.load_habits(habit_data.habit_dict)# Load tasks from file, save into habit_data.habit_dict
    window = func.build_win(habit_data.habit_dict) # Build and return the Window object (GUI)
    selected_habit = 'No Habit Selected' # The default habit; gives context
    while True:
        event, values = window.read()# Get events and values
        if event == sg.WIN_CLOSED:# If the window is closed, break the loop
            break
        elif event == '-HABIT LIST-':# If an element is selected in the Habit List
            print(values["-HABIT LIST-"])
            print(type(values["-HABIT LIST-"]))
            if values['-HABIT LIST-']:# if values[habit list] are not '' (if there is anything selected)
                selected_habit = values['-HABIT LIST-'][0] # selection_mode: single means that only one val will be selected, so vals[listbox] is [x]. finding vals[listbox][0] means we find x in it's original form
        elif event == '-ADD HABIT-':# If you want to add a habit
            habit_data.add_habit(values['-ADD HABIT NAME-'].strip(), values['-ADD DESC-'].strip())# Add that to habit_data.habit_dict
        elif event == '-EDIT HABIT-':
            if selected_habit == 'No Habit Selected':
                sg.popup('No Habit Selected. \nSelect a habit to edit!', keep_on_top=True)
            else:
                window['-EDITING COLUMN-'].update(visible=True)
                window['-EDIT HABIT NAME-'].update(selected_habit)
                window['-EDIT DESC-'].update(habit_data.habit_dict[selected_habit][0])
        elif event == '-UPDATE HABIT-':
            window['-EDITING COLUMN-'].update(visible=False)
            selected_habit = habit_data.update_habit(selected_habit, values['-EDIT HABIT NAME-'], values['-EDIT DESC-']) # Change selected_habit to teh new name
        elif event == '-INC STREAK-':
            if selected_habit == 'No Habit Selected':
                sg.popup('No Habit Selected; Select a habit to increment streak', keep_on_top=True)
            else:
                prevdate = habit_data.habit_dict[selected_habit][2]
                if prevdate == None:# if first time button been pressed
                    habit_data.inc_habit(selected_habit)
                    habit_data.habit_dict[selected_habit][2] = datetime.date.today()
                elif str(prevdate) != str(datetime.date.today()):
                    habit_data.inc_habit(selected_habit)
                    habit_data.habit_dict[selected_habit][2] = datetime.date.today()
                else:
                    sg.popup('YOu have already marked this habit as done today! \nWait till tomorrow to increase your streak and gain more points!', keep_on_top=True)
        elif event == '-DEL HABIT-':
            if selected_habit != 'No Habit Selected':
                habit_data.del_habit(selected_habit)
                selected_habit = 'No Habit Selected'
            else:
                sg.popup('Select a habit to delete', keep_on_top=True)
        func.update_win(window, habit_data.habit_dict, selected_habit)# fill in window, update constantly to GUI from habit_data.habit_dict
    
    habit_data.print_habits()
    func.save_habits(habit_data.habit_dict)# save habits hack to data.txt
    print('All Done') #check everything's done in console

main()