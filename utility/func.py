"""
Page used to store functions for main.py

load_habits(habit_dict)
-- Loads habits from data.txt file and writes them to habit_dict

build_win(habit_dict)
-- Builds the GUI layout
-- returns the Window object of the GUI

update_win(window, habit_dict, selected_habit)
-- updates the GUI with the habit information

save_habits(habit_dict)
-- loads habits from habit_dict, encodes them in rawtext and writes them to data.txt
"""

import os
import PySimpleGUI as sg
import datetime


def load_habits(habit_dict):# task at beginning
    """
    Loads habits from data.txt and writes them into the habit_dict
    Args:
    habit_dict --- the habit dictionary object that is storing the data.

    decodes the habit information from habit_name>>description^^streak_count^^last_completed_date
    into {habit_name: [description, streak_count, last_completed_date]}
    """
    if os.path.exists('data.txt'):# if file data.txt
        with open('data.txt', 'r') as data:# opening the file data.txt
            for line in data:# for every line in the task_data
                habitinfojoin = line.strip().split(">>") # split the line habit>>info into habit, info vars
                habit = habitinfojoin[0]
                info = habitinfojoin[1]
                desc, count, prevdate = info.split('^^') # split the info (desc^^streak^^prevdate) into vars desc, streak
                desc = desc.replace('||', '\n') # turns the saved || into newlines
                if prevdate != 'None':
                    prevdate = datetime.date.fromisoformat(prevdate)
                else:
                    prevdate = None
                habit_dict[habit] = [desc, int(count), prevdate]

def build_win(habit_dict):# Build the Window initially
    """
    Builds the layout of the GUI and returns the Window object in question.

    Args:
    habit_dict --- the habit dictionary object that the habit data is stored in

    Returns:
    window - The Window object that the user interacts with
    """
    WIN_HEIGHT = 450
    WIN_LENGTH = 1200

    H1_FONT = ('Calibri', 24, 'bold')
    H2_FONT = ('Calibri', 20)
    H3_FONT = ('Calibri', 16)
    BUTTON_FONT = ('Calibri', 12)
    DEFAULT_FONT = ('Calibri', 9)
    column1 = [
        [sg.Text('Add Habit', font=H3_FONT)],
        [sg.Input(size=(28, 1), font=DEFAULT_FONT, key='-ADD HABIT NAME-'), sg.Button('Add Habit', enable_events=True, font=BUTTON_FONT, key='-ADD HABIT-')],
        [sg.Multiline(size=(10, 20), font=DEFAULT_FONT, key='-ADD DESC-')]
    ]
    column2 = [
        [sg.Text('View Habits', font=H3_FONT)],
        [sg.Listbox(enable_events=True, values=habit_dict.keys(), select_mode="LISTBOX_SELECT_MODE_SINGLE", size=(20, 20), font=DEFAULT_FONT, key='-HABIT LIST-')]
    ]
    column3 = [
        [sg.Text('Selected Habit', font=H3_FONT), sg.Button('Edit Habit', enable_events=True, font=BUTTON_FONT, key='-EDIT HABIT-')],
        [sg.Frame('Habit', layout=[[sg.Text('No Habit Selected', font=DEFAULT_FONT, key='-VIEW HABIT NAME-')]]), sg.Button('Delete', font=BUTTON_FONT, enable_events= True, key='-DEL HABIT-')],
        [sg.Frame('Streak', layout=[[sg.Text('No Habit Selected', font=DEFAULT_FONT, key='-VIEW STREAK-'), sg.Button('+Streak', enable_events=True, font=BUTTON_FONT, key='-INC STREAK-')]])],
        [sg.Frame('Habit Description', layout=[[sg.Text('No Habit Selected', font=DEFAULT_FONT, size=(30, 10), key='-VIEW DESC-')]])]
    ]
    editing_column = [
        [sg.Text('Edit Habit', font=H3_FONT)],
        [sg.Input(size=(28, 1), font=DEFAULT_FONT, key='-EDIT HABIT NAME-'), sg.Button('UPDATE HABIT', enable_events=True, font=BUTTON_FONT, key='-UPDATE HABIT-')],
        [sg.Multiline(size=(10, 20), font=DEFAULT_FONT, key='-EDIT DESC-')]
    ]
    top_bar = [
        [sg.Text("Finn-Oskar's Habit Tracker App", pad=((50, 75), (20, 10)), font=H1_FONT), sg.Image(filename='./assets/banner.png', pad=((50, 75), (20, 10)))]
    ]
    layout = [
        [
            sg.pin(sg.Column(top_bar, element_justification='c'))
        ],
        [
            sg.HSeparator()
        ],
        [
            sg.pin(sg.Column(column1)), sg.pin(sg.VSeparator()), sg.pin(sg.Column(column2)), sg.pin(sg.VSeparator()), sg.pin(sg.Column(column3)), sg.pin(sg.VSeparator()), sg.pin(sg.Column(editing_column, visible=False, key='-EDITING COLUMN-'))
        ]
    ]
    return sg.Window('Habit Tracker', layout, size=(WIN_LENGTH, WIN_HEIGHT))

def update_win(window, habit_dict, selected_habit):
    """
    Updates the window text values constantly

    Args:
    window --- the Window object that holds the GUI and the user interacts with.
    habit_dict --- the habit dictionary object that stores the habit data.
    selected_habit --- the last habit to be selected in the Habit Listbox / the status ('No Habit Selected' if the habit last selected was deleted etc.)
    
    UPdates the listbox and habit text values so it reflects the habit data properly
    """
    window['-HABIT LIST-'].update(habit_dict.keys())
    window['-VIEW HABIT NAME-'].update(selected_habit)
    if selected_habit != 'No Habit Selected':
        window['-VIEW DESC-'].update(habit_dict[selected_habit][0])
        window['-VIEW STREAK-'].update(habit_dict[selected_habit][1])
    else:
        window['-VIEW DESC-'].update('No Habit Selected')
        window['-VIEW STREAK-'].update('No Habit Selected')


def save_habits(habit_dict):# save all tasks as rawtext to data.txt params: habit_dict is Habits.habit_dict, 
    """
    Loads the habit data from the habit_dict and writes them to data.txt in format:
    habit_name>>description^^streak_count^^last_completed_date

    Args:
    habit_dict --- the habit dictionary that stores the habit_data
    """
    with open('data.txt', 'w') as data: #opening or creating data.txt to save stuff in
        for key in habit_dict:# for every key (habit) in the habit_dict (dictionary of vals), get the key
            desc, count, prevdate = habit_dict[key] # separate the habit_dict values (as a list) into description and count of habit
            desc = desc.replace('\n', '||') # replace all newlines with ||: helps not break data, but preserves the newlines. Will be decoded in load_habits
            data.write(f'{key}>>{desc}^^{count}^^{prevdate}\n')# Save that data in the form "habit>>desc::count", which can be unpacked with split method in load_habits()