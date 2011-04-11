#! /usr/bin/env python
"""Startprogramma voor probreg gui versie

importeert module probreg uit package probreg
roept de main routine daarin aan met als sys.argv[1] als argument
indien deze niet aanwezig is gaat er geen argument mee
waardoor de gui wordt opgestart met een file chooser dialoog
"""

import sys, os
from probreg import probreg
fn = "" if len(sys.argv) <= 1 else sys.argv[1]
probreg.main(fn)