ProbReg
=======

ProbReg stands for Problem Registration, which is what this tool was originally
developed for. It's actually a port of a mainframe application I built over twenty
years ago after a colleague's design, in which our team meant to keep track of
various issues occurring with the applications we maintained.

This application was built using Python with wxPython for the GUI bit and
ElementTree XML processing for the data handling bit.
A while ago I made a web version using the Django framework (see
`ActieReg </avisser/actiereg/>`_ , switching to Sqlite
for the data stuff and adding some user management.

I also adapted this version to work with the same data as the Django version.
Starting the application with or without an argument determines which version
is used, but both versions have a startup script.


Usage
-----

Call ``pr_start.py`` from the top directory. Use a filename or an empty string as
first argument to indicate you want the xml version.

Requirements
------------

- Python (including ElementTree, and Sqlite for the sql version)
- wxPython
- PocketPyGUI for a PocketPC version.

