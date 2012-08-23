ProbReg
=======

ProbReg stands for Problem Registration, which is what this tool was originally
developed for. It's actually a port of a mainframe application I built over twenty
years ago after a colleague's design, in which our team meant to keep track of
various issues occurring with the applications we maintained.

When I made the PC version, I added configurable categories and statuses,
and after some time using it for myself I decided I needed some more detailed
progress reporting so I added the rightmost panel.

This application was built using Python with wxPython for the GUI bit and
ElementTree XML processing for the data handling bit.
A while ago I made a web version using the Django framework, switching to Sqlite
for the data stuff and adding some user management.

Shortly after that I decided to modify the standalone version to be able to
communicate with the Django version, which meant some changes in the GUI and
switching from XML to SQL.
Since I still use the XML version for my personal task management at work, it
survived the makeover so this repository now contains both versions

Requirements
------------

Python (including ElementTree, Sqlite for the sql version)
wxPython
PocketPyGUI for a PocketPC version

