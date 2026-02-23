"""Actie (was: problemen) Registratie, GUI versie

redirect gui-insensitive import to gui-sensitive module
"""
from .toolkit import toolkit
if toolkit == 'qt':
    from .qtgui import (MainGui, PageGui, Page0Gui, Page1Gui, Page6Gui, LoginBoxGui,
                         SortOptionsDialogGui, SelectOptionsDialogGui, SettOptionsDialogGui,
                         show_dialog, show_message, show_error, ask_question, ask_cancel_question,
                         get_open_filename, get_save_filename, get_choice_item)
elif toolkit == 'wx':
    from .wxgui import (MainGui, PageGui, Page0Gui, Page1Gui, Page6Gui, LoginBoxGui,
                         SortOptionsDialogGui, SelectOptionsDialogGui, SettOptionsDialogGui,
                         show_dialog, show_message, show_error, ask_question, ask_cancel_question,
                         get_open_filename, get_save_filename, get_choice_item)
else:
    raise ValueError('Unknown GUI-toolkit specified')
