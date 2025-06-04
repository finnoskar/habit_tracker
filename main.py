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
            if values[event] == []: # if the system does not  know what has been selected from teh listbox
                continue # end process
            if window[event].Values == []: # if the listbox is empty 
                continue # end process
            elif isinstance(values[event], list):# If values[habit list] is a list (if there is anything selected because on the first selection it is an empty string)
                selected_habit = values[event][0] # selection_mode: single means that only one val will be selected, so vals[listbox] is [x]. finding vals[listbox][0] means we find x in it's original form

                
        elif event == '-ADD HABIT-':# If you want to add a habit
            add_habit_error = habit_data.add_habit(values['-ADD HABIT NAME-'].strip(), 
                                                   values['-ADD DESC-'].strip())# Add that to habit_data.habit_dict and save the error that is thrown by the function as add_habit_error
            print('error:', add_habit_error)
            if not add_habit_error: # If no error was thrown
                window['-ADD HABIT NAME-'].update('')
                window['-ADD DESC-'].update('')
        elif event == '-HABIT OPTIONS-':
            if values[event] == 'Edit': # If the menu opton 'Edit' was selected
                if selected_habit == 'No Habit Selected':
                    sg.popup('No Habit Selected. \nSelect a habit to edit!', keep_on_top=True)
                else: # make the editing column visible and the view column invisible
                    window['-EDITING COLUMN-'].update(visible=True)
                    window['-SELECTED HABIT COLUMN-'].update(visible=False)
                    window['-EDIT HABIT NAME-'].update(selected_habit)
                    window['-EDIT DESC-'].update(habit_data.habit_dict[selected_habit][0])
            if values[event] == 'Delete': # If the menu option 'Delete' was selected
                if selected_habit != 'No Habit Selected': # IF there is a habit selected
                    habit_data.del_habit(selected_habit) 
                    selected_habit = 'No Habit Selected'  # reset habit
                    window['-EDIT HABIT NAME-'].update('') 
                    window['-EDIT DESC-'].update('')
                    window['-EDITING COLUMN-'].update(visible=False) # hide editing column
                else:
                    sg.popup('Select a habit to delete', keep_on_top=True)
            if values[event] == 'Clear Streak': # if the menu option 'Clear Streak' was selected
                if selected_habit != 'No Habit Selected':
                    habit_data.habit_dict[selected_habit][1] = 0 # set the selected habit streak to 0
                    habit_data.habit_dict[selected_habit][3] = 0
                else:
                    sg.popup('No Habit Selected', keep_on_top=True)
        elif event == '-UPDATE HABIT-':
            window['-EDITING COLUMN-'].update(visible=False) # Hide editing column
            window['-SELECTED HABIT COLUMN-'].update(visible=True) # Show viewing column
            selected_habit = habit_data.update_habit(selected_habit, 
                                                     values['-EDIT HABIT NAME-'], 
                                                     values['-EDIT DESC-']) # Change selected_habit to the new name
        elif event == '-INC STREAK-': # If the Mark as Done button is pressed
            if selected_habit == 'No Habit Selected':
                sg.popup('No Habit Selected; Select a habit to increment streak', keep_on_top=True)
            else:
                prevdate = habit_data.habit_dict[selected_habit][2] # save the last time the habit was marked as done
                if prevdate == None:# if first time button been pressed 
                    habit_data.inc_habit(selected_habit) # Increase streak
                elif str(prevdate) != str(datetime.date.today()): # If the last time the habit was marked is not today (i.e. marked before today)
                    habit_data.inc_habit(selected_habit)
                else:
                    sg.popup('You have already marked this habit as done today! \nWait till tomorrow to increase your streak!', keep_on_top=True)
        elif event == '-ABOUT-': # If the about nav button is selected
            window['-HOME-'].update(disabled=False) #        | MAke Home button active and About button inactive
            window['-ABOUT-'].update(disabled=True)
            window['-HOME PAGE-'].update(visible=False) #    | Hide the home page and make the About page visible
            window['-ABOUT PAGE-'].update(visible=True)
        elif event == '-HOME-':
            window['-ABOUT-'].update(disabled=False)    # Make ABOUT button active
            window['-HOME-'].update(disabled=True)        # Make Home button disables
            window['-HOME PAGE-'].update(visible=True)    # Make Home page visible
            window['-ABOUT PAGE-'].update(visible=False)# Make About page invisible
        elif 'Delete ' in event:# IF delete selected from listbox right click menu (format: 'Delete Habit')
            habit_data.del_habit(event.split(' ', 2)[2]) # Delete habit (access habit by splitting Delete Habit into [Delete, Habit])
            selected_habit = 'No Habit Selected'
            window['-EDIT HABIT NAME-'].update('')
            window['-EDIT DESC-'].update('')
            window['-EDITING COLUMN-'].update(visible=False)
            window['-SELECTED HABIT COLUMN-'].update(visible=True)
        elif 'Edit ' in event: # IF ERditselected from listbox right click menu (format: 'Edit Habit')
            selected_habit = event.split(' ', 2)[2]
            window['-EDITING COLUMN-'].update(visible=True)
            window['-SELECTED HABIT COLUMN-'].update(visible=False)
            window['-EDIT HABIT NAME-'].update(selected_habit)
            window['-EDIT DESC-'].update(habit_data.habit_dict[selected_habit][0])
        elif 'Clear Streak ' in event: # IF  Clear Streak elected from listbox right click menu (format: 'Clear Streak Habit')
            selected_habit = event.split(' ', 3)[3]
            habit_data.habit_dict[selected_habit][1] = 0
            habit_data.habit_dict[selected_habit][3] = 0
        elif event == '🖌 Edit': # If the menu opton 'Edit' was selected
            if selected_habit == 'No Habit Selected':
                sg.popup('No Habit Selected. \nSelect a habit to edit!', keep_on_top=True)
            else: # make the editing column visible and the view column invisible
                window['-EDITING COLUMN-'].update(visible=True)
                window['-SELECTED HABIT COLUMN-'].update(visible=False)
                window['-EDIT HABIT NAME-'].update(selected_habit)
                window['-EDIT DESC-'].update(habit_data.habit_dict[selected_habit][0])
        elif event == '🗑 Delete': # If the menu option 'Delete' was selected
            if selected_habit != 'No Habit Selected': # IF there is a habit selected
                habit_data.del_habit(selected_habit) 
                selected_habit = 'No Habit Selected'  # reset habit
                window['-EDIT HABIT NAME-'].update('') 
                window['-EDIT DESC-'].update('')
                window['-EDITING COLUMN-'].update(visible=False) # hide editing column
            else:
                sg.popup('Select a habit to delete', keep_on_top=True)
        elif event == '↺ Clear Streak': # if the menu option 'Clear Streak' was selected
            if selected_habit != 'No Habit Selected':
                habit_data.habit_dict[selected_habit][1] = 0 # set the selected habit streak to 0
                habit_data.habit_dict[selected_habit][3] = 0
            else:
                sg.popup('No Habit Selected. \nSelect a habit to clear the streak of.', keep_on_top=True)
        elif event in ['-ADD HABIT NAME-', '-ADD DESC-', '-EDIT HABIT NAME-', '-EDIT DESC-']:
            print(event + ' input stuff: ' + str(values[event]) + ': ' + str(list(values[event])))
            print(func.filter_input(window, 
                                    event, 
                                    habit_data.UNACCEPTED_CHARS))
        func.update_win(window, 
                        habit_data.habit_dict, 
                        selected_habit)# fill in window, update constantly to GUI from habit_data.habit_dict

    func.save_habits(habit_data.habit_dict)# save habits hack to data.txt

main()