#! /usr/bin/env python
"""Startprogramma voor probreg gui sql versie

importeert module probreg uit package probreg (probreg_sql is vervallen)
roept de main routine daarin aan zonder argumenten
daardoor schakelt deze over naar de sql versie
deze kijkt naar de verzameling projecten die de django versie ook gebruikt
"""

import sys, os
from probreg import probreg
probreg.main()
