#! /usr/bin/env python3
"""Startprogramma voor probreg gui sql versie

importeert module probreg uit package probreg (probreg_sql is vervallen)
roept de main routine daarin aan zonder argumenten
daardoor schakelt deze over naar de sql versie
deze kijkt naar de verzameling projecten die de django versie ook gebruikt
"""
from probreg import probreg
probreg.main()
