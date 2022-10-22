History of Probreg
==================

This application is actually a port of a mainframe application I built over twenty
years ago after my team-lead's design, in which our team meant to keep track of
various issues occurring with the applications we maintained. This was before we knew about
issue trackers and such (probably because there wasn't much on the market - we're talking the
Information Era's Iron Age here).

It was initially just for registering incidents and their solutions
in order to be able to research on solutions that had been applied before; 
the "events" part is an addition of my own to be able to also track new developments. 
Now that I think of it, on the mainframe we had a separate tool (also homegrown) for that
which was partly a means of referring to descriptions of changes in the design and the implementation.
This again was a separate application which was part of our software repository.

This last application is kind of the basis for my own documentation tool 
`DocTool/MyProjects <https://github.com/albertvisser/myprojects/>`_

----

The Probreg application was initially built using Python with wxPython for the GUI bit and
ElementTree XML processing for the data handling bit.

To make it work for Python 3 I had to switch to PyQt. This posed a bit of a challenge as I 
couldn't find a way to stop a page from advancing to another the way I had in the wxPython 
version, so instead I made the tabs inaccessible when appropriate.

This difference is deliberately kept intact now that I've also made a wxPhoenix version.

----

In the mean time I made a web version using the Django framework (see
`ActieReg <https://github.com/albertvisser/actiereg/>`_), switching to Sqlite for the data handling
and adding some user management.

It felt appropriate to adapt this program to work with the same data as the Django version, 
and have the same functionality as well as some extra features. 
Originally I rewrote the data handling part to use plain SQL but since you need Django anyway to create the database and such, I rewrote it again to reuse the stuff I built for ActieReg.

----

Then came the time I looked at the data design and wondered if a non-sql database might be better suited so I could a) not use XML and b) not have a rigid data definition schema and hoops to jump through in order to change things when needed. The wish to simplify the user interface (leave out the big text field panels) gave me the incentive to also implement a MongoDB version. 
