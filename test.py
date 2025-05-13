list_right_click_menu = []
inner_menu = ['&Delete', '&Edit', '&Clear Streak']
for habit in ['shr', 'fff', 'kdfjisbfg']:
    list_right_click_menu += [habit, inner_menu]
    print(list_right_click_menu)
    
list_right_click_menu = [''] + [list_right_click_menu]
print(list_right_click_menu)