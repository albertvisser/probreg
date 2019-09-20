#! /usr/bin/env python3
"""Startprogramma voor probreg gui versie

importeert module probreg uit package probreg
roept de main routine daarin aan met als sys.argv[1] als argument
tenzij deze 'sql' is, dan wordt overgeschakeld naar de SQL versie
of als deze niet aanwezig is, dan gaat er een leeg argument mee
waardoor de gui wordt opgestart met een file chooser dialoog
als je een bekende projectnaam opgeeft wordt overgeschakeld naar de SQL versie
"""
import sys
from probreg.main import main
fn = "" if len(sys.argv) <= 1 else sys.argv[1]
if len(sys.argv) > 1 and sys.argv[1] == 'sql':
    main()
else:
    main(fn)
