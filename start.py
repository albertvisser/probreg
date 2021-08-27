#! /usr/bin/env python3
"""Startprogramma voor probreg gui versie
"""
import sys
from probreg.main import main
if len(sys.argv) > 1:
    main(sys.argv[1])
else:
    main()
