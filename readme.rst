ProbReg
=======

ProbReg stands for Problem Registration, which is what this tool was originally developed for. 
We fixed problems in the nightly batch runs on the mainframe and registered them in this tool 
so we could research them when a similar problem occurred.

I tried to turn it into something that could be used as a tool for bug-tracking and new developments
to make my life easier when I maintained an application for migrating mainframe JCL.
And then I couldn't keep myself from trying to develop it further.

Similar to other projects of mine there is the possibilty to switch out 
the GUI toolkit the application uses and also the data backend; 
though the application's behaviour is slightly different related to which backend is used: 
the Django version has user support and the Mongo version has lesser panels.

Usage
-----

Call ``start.py`` from the top directory to start the application.

Use a filename or an empty string as first argument to indicate you want the xml version.

Use a known project name (registered in the Actiereg application) or literal `sql` 
to use the Django/SQL version. 

Use `mongo` or `mongodb` to start the version with only 3 tabs. 
It uses a single database, so no file- or project name needed.

Requirements
------------

- Python (including ElementTree for the XML version and Sqlite for the SQL/Django version)
- wxPython or PyQt for the GUI part
- the Django/SQL version won't work without Django but also not without installing
  my `ActieReg <https://github.com/albertvisser/actiereg/>`_ project, since it uses its components
- the MongoDB version needs MongoDB and PyMongo to work 
