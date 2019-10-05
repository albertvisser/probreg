ProbReg
=======

ProbReg stands for Problem Registration, which is what this tool was originally
developed for. It's actually a port of a mainframe application I built over twenty
years ago after a co-worker's design, in which our team meant to keep track of
various issues occurring with the applications we maintained. This was before we knew about
issue trackers and such (probably because there wasn't much on the market - we're talking the
Information Era's Iron Age here).

This application was initially built using Python with wxPython for the GUI bit and
ElementTree XML processing for the data handling bit.

To make it work for Python 3 I had to switch to PyQt. This posed a bit of a challenge as I 
couldn't find a way to stop a page from advancing to another the way I had in the wxPython 
version, so instead I made the tabs inaccessible when appropriate.

This difference is deliberately kept intact now that I've also made a wxPhoenix version.


In the mean time I made a web version using the Django framework (see
`ActieReg </avisser/actiereg/>`_ , switching to Sqlite for the data handling
and adding some user management.

It felt appropriate to adapted this program to work with the same data as the Django version, 
and have the same functionality. So there are also slight differences between the XML and the SQL version.


Usage
-----

Call ``start.py`` from the top directory.
Use a filename or an empty string as first argument to indicate you want the xml version.
Use a known project name or literal `sql`` to use the Django/SQL version. 

Requirements
------------

- Python (including ElementTree, and Sqlite for the sql version)
- wxPython or PyQt for the GUI part
- the XML version currently requires ElementTree from the stdlib, 
  the Django/SQL version won't work without installing the ActieReg project, since it uses its 
  components (not just Django itself) 
- PocketPyGUI for a PocketPC version (actually discontinued)

