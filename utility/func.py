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

def build_list_right_click_menu(habit_dict):
    list_right_click_menu = []
    inner_menu = ['&Delete', '&Edit', '&Clear Streak']
    for habit in habit_dict.keys(): # [A, B, C, F]
        this_inner_menu = inner_menu # [D, E, CS]
        for item in this_inner_menu: # [D, E, CS]
            this_inner_menu[this_inner_menu.index(item)] += ' ' + habit   # 
        list_right_click_menu += [habit, this_inner_menu]
    
    list_right_click_menu = [''] + [list_right_click_menu]
    return list_right_click_menu

def build_win(habit_dict):# Build the Window initially
    """
    Builds the layout of the GUI and returns the Window object in question.

    Args:
    habit_dict --- the habit dictionary object that the habit data is stored in

    Returns:
    window - The Window object that the user interacts with
    """
    WIN_HEIGHT = 400
    WIN_LENGTH = 800

    H1_FONT = ('Calibri', 24, 'bold')
    H2_FONT = ('Calibri', 20)
    H3_FONT = ('Calibri', 16)
    H4_FONT = ('Calibri', 14)
    BUTTON_FONT = ('Calibri', 12)
    DEFAULT_FONT = ('Calibri', 9)
    
    THEMES = ('LightBlue3', 'LightGrey1', 'Reds')
    DEFAULT_THEME = 'LightBlue3'

    habit_menu = [
        '⋮', ['&Delete', '&Edit', '&Clear Streak'] # the layout for 
    ]
    right_click_habit_menu = [
        '', ['&Delete', '&Edit', '&Clear Streak']
    ]
    list_right_click_menu = build_list_right_click_menu(habit_dict)

    column1 = sg.Column([
        [
            sg.Text('Add Habit', 
                    font=H3_FONT), 
            sg.Push(), 
            sg.Button('Add Habit', 
                      enable_events=True, 
                      font=BUTTON_FONT, 
                      key='-ADD HABIT-')
        ],
        [sg.Input(size=(35, 1), 
                  font=DEFAULT_FONT, 
                  key='-ADD HABIT NAME-')],
        [sg.Multiline(size=(33, 20), 
                      font=DEFAULT_FONT, 
                      key='-ADD DESC-')]
    ])

    column2 = sg.Column([
        [sg.Text('View Habits', 
                 font=H3_FONT,
                 right_click_menu=right_click_habit_menu)],
        [sg.Listbox(enable_events=True, 
                    values=habit_dict.keys(), 
                    select_mode="LISTBOX_SELECT_MODE_SINGLE", 
                    size=(20, 20), 
                    font=DEFAULT_FONT,
                    right_click_menu=list_right_click_menu, 
                    key='-HABIT LIST-')]
    ], right_click_menu=right_click_habit_menu)

    selected_column = sg.Column([
        [
            sg.Text('Selected Habit', 
                    font=H3_FONT,
                   right_click_menu=right_click_habit_menu),
            sg.Push(), 
            sg.ButtonMenu('⋮', 
                          habit_menu, 
                          font=BUTTON_FONT, 
                          button_color=('#000000', '#A8CFDD'), 
                          border_width=0, 
                          key='-HABIT OPTIONS-')
        ],
        [sg.Frame('Habit', 
                  layout=[[sg.Text('No Habit Selected', 
                                   font=DEFAULT_FONT, 
                                   size=28, 
                                   key='-VIEW HABIT NAME-')]],
                  right_click_menu=right_click_habit_menu
                 )],

        [sg.Frame('Habit Description', 
                  layout=[[sg.Text('No Habit Selected', 
                                   font=DEFAULT_FONT, 
                                   size=(28, 20), 
                                   key='-VIEW DESC-')]],
                  right_click_menu=right_click_habit_menu
                 )]
    ], right_click_menu=right_click_habit_menu)

    streak_column = sg.Column([
        [sg.Button('Mark as Done', 
                   enable_events=True, 
                   size=20, 
                   font=BUTTON_FONT,
                   right_click_menu=right_click_habit_menu, 
                   key='-INC STREAK-')],
        [sg.Frame('Streak', 
                  layout=[[sg.Text('No Habit Selected', 
                                   font=DEFAULT_FONT, 
                                   size=133, 
                                   key='-VIEW STREAK-')]],
                  right_click_menu=right_click_habit_menu
                 )],
        [sg.ProgressBar(orientation='vertical',
                        border_width=2,
                        max_value=7, 
                        size=(8, 106),
                        bar_color=('green', '#A8CFDD'),
                        right_click_menu=right_click_habit_menu, 
                        key='-PROGRESS-')],
        [sg.Frame('Good Work Bit', 
                  layout=[[sg.Text('Yup', 
                                   font=H3_FONT)]], 
                  size=(115, 133),
                  right_click_menu=right_click_habit_menu)]
    ], right_click_menu=right_click_habit_menu)

    editing_column = sg.Column([
        [
            sg.Text('Edit Habit', 
                    font=H3_FONT), 
            sg.Push(), 
            sg.Button('Update Habit', 
                      enable_events=True, 
                      font=BUTTON_FONT, 
                      key='-UPDATE HABIT-')
        ],
        [sg.Input(size=(35, 1), 
                  font=DEFAULT_FONT, 
                  key='-EDIT HABIT NAME-')],

        [sg.Multiline(size=(33, 20), 
                      font=DEFAULT_FONT, 
                      key='-EDIT DESC-')]

    ], visible=False, key='-EDITING COLUMN-')

    top_bar = [
            sg.Text("StreakIt", 
                    font=H1_FONT,
                    pad=((15, 0), (0, 0)), 
                    expand_x=True), 
            sg.Text('A HABIT TRACKING APP', 
                    pad=(30, 0), 
                    font=H4_FONT,
                    expand_x=True), 
            sg.Push(), 
            sg.Button('HOME', 
                      disabled=True, 
                      pad=(8, 0),
                      expand_x=True, 
                      key='-HOME-'),    
            sg.Button('OPTIONS', 
                      disabled=False, 
                      pad=(20, 0),
                      expand_x=True, 
                      key='-OPTIONS-')
        ]
    
    options_page = sg.Column([
        [
            sg.Push(background_color='orange')
        ],
    ], expand_x=True, visible=False, key='-OPTIONS PAGE-')

    layout = [
        [top_bar],
        [sg.HSeparator()],
        [sg.pin(sg.Column([[
                        sg.pin(sg.Column(layout=[
                            [
                                sg.pin(column1), 
                                sg.VSeparator(), 
                                sg.pin(column2), 
                                sg.VSeparator(), 
                                sg.pin(sg.Column(layout=[[selected_column, streak_column]], 
                                                key='-SELECTED HABIT COLUMN-')), 
                                sg.pin(editing_column)
                            ]]))
                        ]], key='-HOME PAGE-'))],
        [sg.pin(options_page)]
    ]
    return sg.Window('Habit Tracker', 
                     layout, 
                     border_depth=1, 
                     finalize=True, 
                     size=(WIN_LENGTH, WIN_HEIGHT))

def update_win(window, 
               habit_dict, 
               selected_habit):
    """
    Updates the window text values constantly

    Args:
    window --- the Window object that holds the GUI and the user interacts with.
    habit_dict --- the habit dictionary object that stores the habit data.
    selected_habit --- the last habit to be selected in the Habit Listbox / the status ('No Habit Selected' if the habit last selected was deleted etc.)
    
    Updates the listbox and habit text values so it reflects the habit data properly
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