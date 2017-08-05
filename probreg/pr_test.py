#! /usr/bin/env python
"""stupid test program (just to see how it starts up)
"""
## from probreg import main
from probreg_qt import main

if __name__ == '__main__':
    ## main() # sql versie
    ## main(None, log=True) # sql versie met logging (qt versie)
    ## main('') # xml versie
    ## main('todo.xml', log=True) # xml versie met logging (qt versie)
    main('todo.xml')  # xml versie
    ## main('todo.xml', log=True) # xml versie met logging (qt versie)
