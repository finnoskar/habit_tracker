"""
Page used to store functions for main.py

load_habits(habit_dict)
-- Loads habits from data.txt file and writes them to habit_dict

build_list_right_click_menu(habit_dict)
-- Builds the menu for the listbox right click menu given the habits in the listbox
-- return the menu layout

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
import re


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
                habitandinfo = line.split(">>") # split the line habit>>info into [habit, info]
                habit, info = habitandinfo
                desc, count, prevdate, progress = info.split('^^') # split the info (desc^^streak^^prevdate^^progress) into vars desc, streak, prevdate, progress
                desc = desc.replace('||', '\n') # turns the saved || into newlines
                if prevdate != 'None':
                    prevdate = datetime.date.fromisoformat(prevdate)
                else:
                    prevdate = None
                habit_dict[habit] = [desc, int(count), prevdate, int(progress)]


def build_list_right_click_menu(habit_dict):
    """A function to build the right-click menu of the listbox. takes in the habit dictionary, returns the menu layout"""
    list_right_click_menu = [] # The list the menu will be held in
    inner_template = ['🗑 &Delete', '🖌 &Edit', '↺ &Clear Streak'] # The different options
    print('habit_dict.keys(): ' + str(habit_dict.keys()))
    if not habit_dict.keys():
        return ['', ['!EMPTY']]
    for habit in habit_dict.keys():# For each habit in the dictionary
        print('they are making the menu')
        inner_menu = []
        for item in inner_template: # For each options
            inner_menu.append(f'{item} {habit}') # Add each option + habit name into a string (menu option), with all disabled
        list_right_click_menu += [habit, inner_menu] # Place the [Submenu Title, [Submenu]]
    # They will be added together as: [Submenu Title1, [Submenu1], Submenu Title 2, [Submenu2]]
    list_right_click_menu = [''] + [list_right_click_menu] # wrap that in the final layout context: ['unused base string', [menu layout]]
    print('we got this far')
    return list_right_click_menu # return the menu layout


def build_win(habit_dict):# Build the Window initially
    """
    Builds the layout of the GUI and returns the Window object in question.

    Args:
    habit_dict --- the habit dictionary object that the habit data is stored in

    Returns:
    window - The Window object that the user interacts with
    """
    # CONSTANTS

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

    # DIFFERENT MENU LAYOUTS

    habit_menu = [
        '⋮', ['!🗑 Delete', '!🖌 Edit', '!↺ Clear Streak'] # the layout for the habit options meny
    ]
    begin_right_click_habit_menu = [
        '', ['!🗑 &Delete', '!🖌 &Edit', '!↺ &Clear Streak'] # The layout for the right click menu on the view / selected habit column
    ]
    list_right_click_menu = build_list_right_click_menu(habit_dict) # build the list right click menu

    add_column = sg.Column([# The column where the GUI to add a habit is held
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
                  enable_events=True,
                  key='-ADD HABIT NAME-')],
        [sg.Multiline(size=(33, 20), 
                      font=DEFAULT_FONT,
                      enable_events=True,
                      key='-ADD DESC-')]
    ])

    listbox_column = sg.Column([ # The column where habits are displayed and selected from a listbox
        [sg.Text('View Habits', 
                 font=H3_FONT,
                 right_click_menu=begin_right_click_habit_menu,
                 key='-VIEW HABIT TEXT-')],
        [sg.Listbox(enable_events=True, 
                    values=habit_dict.keys(), 
                    select_mode="LISTBOX_SELECT_MODE_SINGLE", 
                    size=(20, 20), 
                    font=DEFAULT_FONT,
                    right_click_menu=list_right_click_menu, 
                    key='-HABIT LIST-')]
    ])

    selected_column = sg.Column([ # The column that shows the selected habit's details
        [
            sg.Text('Selected Habit', 
                    font=H3_FONT,
                    right_click_menu=begin_right_click_habit_menu,
                    key='-SELECTED HABIT TEXT-'),
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
                                   right_click_menu=begin_right_click_habit_menu,
                                   key='-VIEW HABIT NAME-')]],
                  right_click_menu=begin_right_click_habit_menu,
                  key='-HABIT FRAME-'
                 )],

        [sg.Frame('Habit Description', 
                  layout=[[sg.Text('No Habit Selected', 
                                   font=DEFAULT_FONT, 
                                   size=(28, 20), 
                                   right_click_menu=begin_right_click_habit_menu,
                                   key='-VIEW DESC-')]],
                  right_click_menu=begin_right_click_habit_menu,
                  key='-HABIT DESC FRAME-'
                 )]
    ])

    streak_column = sg.Column([ # The column with the streak data of the selected habit
        [sg.Button('Mark as Done', 
                   enable_events=True, 
                   size=20, 
                   font=BUTTON_FONT,
                   right_click_menu=begin_right_click_habit_menu, 
                   key='-INC STREAK-')],
        [sg.Frame('Streak', 
                  layout=[[sg.Text('No Habit Selected', 
                                   font=DEFAULT_FONT, 
                                   size=133, 
                                   right_click_menu=begin_right_click_habit_menu,
                                   key='-VIEW STREAK-')]],
                  right_click_menu=begin_right_click_habit_menu,
                  key='-STREAK FRAME-'
                 )],
        [sg.ProgressBar(orientation='vertical',
                        border_width=2,
                        max_value=7, 
                        size=(8, 106),
                        bar_color=('green', '#A8CFDD'),
                        right_click_menu=begin_right_click_habit_menu, 
                        key='-PROGRESS-')],
        [sg.Frame('', 
                  layout=[[sg.Text('You are at \n0/7 days of \ncommitment for \nthis habit', 
                                   font=DEFAULT_FONT, 
                                   right_click_menu=begin_right_click_habit_menu,
                                   key='-STREAK MESSAGE-')]], 
                  size=(115, 133),
                  right_click_menu=begin_right_click_habit_menu,
                  key='-STREAK MESSAGE FRAME-')]
    ])

    editing_column = sg.Column([ # The column that appears when the Edit button is pressed (or edit option on right click menus)
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
                  enable_events=True,
                  key='-EDIT HABIT NAME-')],

        [sg.Multiline(size=(33, 20), 
                      font=DEFAULT_FONT, 
                      enable_events=True,
                      key='-EDIT DESC-')]

    ], visible=False, key='-EDITING COLUMN-')

    top_bar = [# The top bar, with the header and nav buttons
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
            sg.Button(' ABOUT ', 
                      disabled=False, 
                      pad=(20, 0),
                      expand_x=True, 
                      key='-ABOUT-')
        ]
    
    options_page = sg.Column([# The page with the options and info about the app
        [sg.Text('Welcome to my Habit Tracking App!', 
                  font=H3_FONT)],
        [sg.Text('This is a habit tracking app developed by me for students to use in order to organize themselves for school, home, and other habitual activities.\nHopefully, this will help you to develop useful habits', 
                  font=DEFAULT_FONT)],
        [sg.Text('How to Use the App', 
                  font=H3_FONT)],
        [sg.Text('Add habits to the system by using the inputs on the left portion of the app and pressing the "Add Habit" button.\nThe habits in the system are displayed in the box to the right. \nUse right click or the small three dots next to the name of the habit selected to Delete, Edit, or Clear the Streak of a habit. \nThe green progress bar on the right is a representative of how many days you have committed to this habit (out of 7, for a week)', 
                  font=DEFAULT_FONT)]
], expand_x=True, visible=False, key='-ABOUT PAGE-')

    layout = [# The final layout
        [top_bar],
        [sg.HSeparator()],
        [sg.pin(sg.Column([[
                        sg.pin(sg.Column(layout=[
                            [
                                sg.pin(add_column), 
                                sg.VSeparator(), 
                                sg.pin(listbox_column), 
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

def open_editing_column(window, habit, desc):
    window['-EDITING COLUMN-'].update(visible=True)
    window['-SELECTED HABIT COLUMN-'].update(visible=False)
    window['-EDIT HABIT NAME-'].update(habit)
    window['-EDIT DESC-'].update(desc)

def filter_input(window,
                 input_key,
                 UNACCEPTED_CHARS):
    input_text = window[input_key].get() # Access the text to be filtered
    if input_text == '': # If it is empty, return it
        return input_text
    
    filtered_text = re.sub(UNACCEPTED_CHARS, '', input_text) # remove all the unaccepted characters
    if filtered_text != input_text: # if we have made changes 
        window[input_key].update(filtered_text) # update GUI

    return filtered_text if filtered_text != input_text else input_text # if we have made changes, return the changed, if we haven't, return the original text

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
    ITEMS_WITH_RIGHT_CLICK_MENU = ['-VIEW HABIT TEXT-', '-SELECTED HABIT TEXT-', '-HABIT FRAME-', '-VIEW HABIT NAME-', '-HABIT DESC FRAME-', '-VIEW DESC-', '-INC STREAK-', '-VIEW STREAK-', '-STREAK FRAME-', '-PROGRESS-', '-STREAK MESSAGE FRAME-', '-STREAK MESSAGE-']
    list_right_click_menu = build_list_right_click_menu(habit_dict) # create the listbox right click menu
    window['-HABIT LIST-'].set_right_click_menu(list_right_click_menu) # update the listbox right click menu
    window['-HABIT LIST-'].update(values=habit_dict.keys()) # update the content of the listbox
    window['-VIEW HABIT NAME-'].update(selected_habit)# update the habit name of the habit in the selected habit text box
    
    
    if selected_habit != 'No Habit Selected': # If there is a habit selected:
        window['-HABIT OPTIONS-'].update(menu_definition=['⋮', ['🗑 &Delete', '🖌 &Edit', '↺ &Clear Streak']])
        for element in ITEMS_WITH_RIGHT_CLICK_MENU: # For every element that has a right click menu
            window[element].set_right_click_menu(['', ['🗑 &Delete', '🖌 &Edit', '↺ &Clear Streak']]) # set the enabled right click menu
        window['-VIEW DESC-'].update(habit_dict[selected_habit][0]) # update description 
        window['-VIEW STREAK-'].update(habit_dict[selected_habit][1]) # update streak
        window['-STREAK MESSAGE-'].update(f'You are at \n{habit_dict[selected_habit][3]}/7 days of \ncommitment for \nthis habit')
        window['-PROGRESS-'].update(current_count=habit_dict[selected_habit][3], 
                                    bar_color=('#00FF00', '#A8CFDD')) # update the progress bar

    else: # if there isn't a habit selected
        window['-HABIT OPTIONS-'].update(menu_definition=['⋮', ['!🗑 &Delete', '!🖌 &Edit', '!↺ &Clear Streak']]) # disable the habit options
        window['-VIEW DESC-'].update('No Habit Selected')
        window['-VIEW STREAK-'].update('No Habit Selected')
        window['-PROGRESS-'].update(current_count=0, 
                                    bar_color=('#00FF00', '#A8CFDD')) # -------------------->     reset the progress bar 
        window['-STREAK MESSAGE-'].update('You are at \n0/7 days of \ncommitment for \nthis habit') # and streak message
        for element in ITEMS_WITH_RIGHT_CLICK_MENU:# For every element that has a right click menu
            window[element].set_right_click_menu(['', ['!🗑 &Delete', '!🖌 &Edit', '!↺ &Clear Streak']]) # set the disabled right click menu
    


def save_habits(habit_dict):# save all tasks as rawtext to data.txt params: habit_dict is Habits.habit_dict, 
    """
    Loads the habit data from the habit_dict and writes them to data.txt in format:
    habit_name>>description^^streak_count^^last_completed_date

    Args:
    habit_dict --- the habit dictionary that stores the habit_data
    """
    with open('data.txt', 'w') as data: #opening or creating data.txt to save stuff in
        for habit in habit_dict:# for every habit in the habit_dict (dictionary of vals), get the key
            desc, count, prevdate, progress = habit_dict[habit] # separate the habit_dict values (as a list) into description and count of habit
            desc = desc.replace('\n', '||') # replace all newlines with ||: helps not break data, but preserves the newlines. Will be decoded in load_habits
            data.write(f'{habit}>>{desc}^^{count}^^{prevdate}^^{progress}\n')# Save that data in the form "habit>>desc^^count^^prevdate^^progress", which can be unpacked with split method in load_habits()