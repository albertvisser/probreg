#! /usr/bin/env python
"""Startprogramma voor probreg gui sql versie

importeert module probreg_sql uit package probreg
roept de main routine daarin aan
deze kijkt naar de verzameling projecten die de django versie ook gebruikt
"""

import sys, os
from probreg import probreg_sql
probreg_sql.main()
