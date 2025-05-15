"""
Python App: Habit Tracker

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
    sg.theme('LightBlue3')
    habit_data = Habits() # Instantiate habit_data
    func.load_habits(habit_data.habit_dict)# Load tasks from file, save into habit_data.habit_dict
    window = func.build_win(habit_data.habit_dict) # Build and return the Window object (GUI)
    selected_habit = 'No Habit Selected' # The default habit; gives context
    while True:
        event, values = window.read()# Get events and values
        if event == sg.WIN_CLOSED:# If the window is closed, break the loop
            break
        elif event == '-HABIT LIST-':# If an element is selected in the Habit List
            if str(event) == 'None':
                continue
            if window[event].Values == []:
                continue
            if isinstance(values[event], list):# if values[habit list] is a list (if there is anything selected because on the first selection it is an empty string)
                selected_habit = values[event][0] # selection_mode: single means that only one val will be selected, so vals[listbox] is [x]. finding vals[listbox][0] means we find x in it's original form
        elif event == '-ADD HABIT-':# If you want to add a habit
            add_habit_error = habit_data.add_habit(values['-ADD HABIT NAME-'].strip(), values['-ADD DESC-'].strip())# Add that to habit_data.habit_dict and save the error that is thrown by the function as add_habit_error
            print('error:', add_habit_error)
            if not add_habit_error: # If no error was thrown
                window['-ADD HABIT NAME-'].update('')
                window['-ADD DESC-'].update('')
        elif event == '-HABIT OPTIONS-':
            if values[event] == 'Edit':
                if selected_habit == 'No Habit Selected':
                    sg.popup('No Habit Selected. \nSelect a habit to edit!', keep_on_top=True)
                else:
                    window['-EDITING COLUMN-'].update(visible=True)
                    window['-SELECTED HABIT COLUMN-'].update(visible=False)
                    window['-EDIT HABIT NAME-'].update(selected_habit)
                    window['-EDIT DESC-'].update(habit_data.habit_dict[selected_habit][0])
            if values[event] == 'Delete':
                if selected_habit != 'No Habit Selected':
                    habit_data.del_habit(selected_habit)
                    selected_habit = 'No Habit Selected'
                    window['-EDIT HABIT NAME-'].update('')
                    window['-EDIT DESC-'].update('')
                    window['-EDITING COLUMN-'].update(visible=False)
                else:
                    sg.popup('Select a habit to delete', keep_on_top=True)
            if values[event] == 'Clear Streak':
                habit_data.habit_dict[selected_habit][1] = 0
        elif event == '-EDIT HABIT-':
            if selected_habit == 'No Habit Selected':
                sg.popup('No Habit Selected. \nSelect a habit to edit!', keep_on_top=True)
            else:
                window['-EDITING COLUMN-'].update(visible=True)
                window['-SELECTED HABIT COLUMN-'].update(visible=False)
                window['-EDIT HABIT NAME-'].update(selected_habit)
                window['-EDIT DESC-'].update(habit_data.habit_dict[selected_habit][0])
        elif event == '-UPDATE HABIT-':
            window['-EDITING COLUMN-'].update(visible=False)
            window['-SELECTED HABIT COLUMN-'].update(visible=True)
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
                    sg.popup('Yuu have already marked this habit as done today! \nWait till tomorrow to increase your streak and gain more points!', keep_on_top=True)
        elif event == '-DEL HABIT-':
            if selected_habit != 'No Habit Selected':
                habit_data.del_habit(selected_habit)
                selected_habit = 'No Habit Selected'
                window['-EDIT HABIT NAME-'].update('')
                window['-EDIT DESC-'].update('')
                window['-EDITING COLUMN-'].update(visible=False)
            else:
                sg.popup('Select a habit to delete', keep_on_top=True)
        elif event == '-OPTIONS-':
            window['-HOME-'].update(disabled=False)
            window[event].update(disabled=True)
            window['-HOME PAGE-'].update(visible=False)
            window['-OPTIONS PAGE-'].update(visible=True)
        elif event == '-HOME-':
            window['-OPTIONS-'].update(disabled=False)
            window[event].update(disabled=True)
            window['-HOME PAGE-'].update(visible=True)
            window['-OPTIONS PAGE-'].update(visible=False)
            print('home')
        elif 'Delete ' in event:
            print(habit_data.habit_dict)
            habit_data.del_habit(event.split(' ', 1)[1])
            selected_habit = 'No Habit Selected'
            window['-EDIT HABIT NAME-'].update('')
            window['-EDIT DESC-'].update('')
            window['-EDITING COLUMN-'].update(visible=False)
        elif 'Edit ' in event:
            selected_habit = event.split(' ', 1)[1]
            window['-EDITING COLUMN-'].update(visible=True)
            window['-SELECTED HABIT COLUMN-'].update(visible=False)
            window['-EDIT HABIT NAME-'].update(selected_habit)
            window['-EDIT DESC-'].update(habit_data.habit_dict[selected_habit][0])
        elif 'Clear Streak ' in event:
            selected_habit = event.split(' ', 2)[2]
            habit_data.habit_dict[selected_habit][1] = 0
        window['-PROGRESS-'].update(current_count=3, bar_color=('#00FF00', '#A8CFDD'))
        func.update_win(window, habit_data.habit_dict, selected_habit)# fill in window, update constantly to GUI from habit_data.habit_dict

    func.save_habits(habit_data.habit_dict)# save habits hack to data.txt

main()