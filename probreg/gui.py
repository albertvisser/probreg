"""Actie (was: problemen) Registratie, GUI versie

redirect gui-insensitive import to gui-sensitive module
"""
from .toolkit import toolkit
if toolkit == 'qt':
    from .gui_qt import MainGui
elif toolkit == 'wx':
    from .gui_wx import MainGui
else:
    raise ValueError('Unknown GUI-toolkit specified')
