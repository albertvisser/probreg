"""Actie (was: problemen) Registratie, GUI versie

redirect gui-insensitive import to gui-sensitive module
"""
from .toolkit import toolkit
if toolkit == 'qt':
    from .gui_qt import MainGui, PageGui, Page0Gui, Page1Gui, \
        SortOptionsDialog, SelectOptionsDialog, LoginBox, \
        show_message, ask_cancel_question, get_open_filename, get_save_filename, \
        get_choice_item, show_dialog
elif toolkit == 'wx':
    from .gui_wx import MainGui, PageGui, Page0Gui, Page1Gui, \
        SortOptionsDialog, SelectOptionsDialog, LoginBox, \
        show_message, ask_cancel_question, get_open_filename, get_save_filename, \
        get_choice_item, show_dialog
else:
    raise ValueError('Unknown GUI-toolkit specified')
