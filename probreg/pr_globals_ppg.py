# -*- coding: UTF-8 -*-
"""Probreg constants for menu items and other stuff - pocketPyGUI version - not maintained
"""

ID_FILE=("&File",)
ID_NEW=("&New (Ctrl-N)"," Create a new file")
ID_OPEN=("&Open (Ctrl-O)"," Open a new file")
ID_PRINT=("&Print (Ctrl-P)"," Print scherminhoud of actie")
ID_PRINTS=("Dit &Scherm"," ")
ID_PRINTA=("Deze &Actie"," ")
ID_EXIT=("&Quit (Ctrl-Q)"," Terminate the program")
ID_SETTINGS=("&Settings",)
ID_SETAPPL=("&Applicatie"," Settings voor de hele applicatie")
ID_SETFONT=("&Lettertype"," Change the size and font of the text")
ID_SETCOLR=("&Kleuren"," Change the colours of various items")
ID_SETKEYS=("S&neltoetsen"," Change shortcut keys")
ID_SETDATA=("&Data"," Settings voor dit specifieke meldingenbestand")
ID_SETTABS=("  &Tabs"," Change the titles of the tabs")
ID_SETCATS=("  &Soorten"," Add/change type categories")
ID_SETSTATS=("  St&atussen"," Add/change status categories")
ID_SETFOLLY=("&Het leven"," Change the way you look at life")
ID_HELP=("&Help",)
ID_ABOUT=("&About"," Information about this program")
ID_KEYS=("&Keys"," List of shortcut keys")
ID_SORT = 130
ID_ZOEK = 131
ID_GANAAR = 132
ID_MELD = 133
ID_ARCH = 134
ID_T1A = 140
ID_T1B = 141
ID_CL2 = 142
ID_CL3 = 143
ID_T4 = 144
ID_RB5A = 145
ID_RB5B = 146
helpinfo = """=== Albert's actiebox ===
            "Keyboard shortcuts:
            "    Alt left/right: verder - terug
            "    Alt-0 t/m Alt-5: naar betreffende pagina
            "    Alt-S op tab 1: Sorteren
            "    Alt-F op tab 1: Filteren
            "    Alt-G of Enter op tab 1: Ga naar aangegeven actie
            "    Alt-N op elke tab: Nieuwe actie opvoeren
            "    Ctrl-O: open een (ander) actiebestand
            "    Ctrl-N: maak een nieuw actiebestand
            "    Ctrl-P: printen (scherm of actie)
            "    Ctrl-Q: quit actiebox
            "    Ctrl-H: help (dit scherm)"
            "    Ctrl-S: gegevens in het scherm opslaan
            "    Ctrl-G: oplaan en door naar volgende tab
            "    Ctrl-Z: wijzigingen ongedaan maken"""
tabtitel = "Tab titels"
tabhelp = ["De tab titels worden getoond in de volgorde",
            "zoals ze van links naar rechts staan.",
            "Er kunnen geen tabs worden verwijderd of",
            "toegevoegd."
            ]
stattitel = "Status codes en waarden"
stathelp = [
            "De waarden voor de status worden getoond in",
            "dezelfde volgorde als waarin ze in de combobox",
            "staan.",
            "Vóór de dubbele punt staat de code, erachter",
            "de waarde.",
            "Denk erom dat als je codes wijzigt of statussen",
            "verwijdert, deze ook niet meer getoond en",
            "gebruikt kunnen worden in de registratie."
            ]
cattitel = "Soort codes en waarden"
cathelp = ["De waarden voor de soorten worden getoond in",
            "dezelfde volgorde als waarin ze in de combobox",
            "staan.",
            "Vóór de dubbele punt staat de code, erachter",
            "de waarde.",
            "Denk erom dat als je codes wijzigt of statussen",
            "verwijdert, deze ook niet meer getoond en",
            "gebruikt kunnen worden in de registratie."
            ]
pagehelp = ["Overzicht van alle acties",        "Identificerende gegevens van de actie",        "Beschrijving van het probleem of wens",        "Analyse van het probleem of wens",        "Voorgestelde oplossing",        "Eventuele vervolgactie(s)",        "Overzicht stand van zaken"]
