"""configuration items and shared/gui-independent routines

definieert een aantal constanten en de default waarden voor de settings dictionaries:
DBLOC - waar de database staat
USER - default userid om in te vullen waar nodig
APPS - waar de lijst met apps staat
kopdict - dictionary van tabs in de vorm                 volgorde: (tab titel,  link naam)
statdict: dictionary van mogelijke statussen in de vorm  volgorde: (omschrijving, code, id in tabel)
catdict: dictionary van mogelijke soorten in de vorm     volgorde: (omschrijving, code, id in tabel)
"""
import sys
import pathlib
ROOT = pathlib.Path("/home/albert/projects/actiereg/actiereg")
sys.path.append(str(ROOT))
from settings import DATABASES
DBLOC = DATABASES['default']['NAME']    # str(ROOT / "actiereg.db")
USER = 2
APPS = ROOT / "apps.dat"

kopdict = {
    "0": ("Lijst", 'index'),
    "1": ("Titel/Status", 'detail'),
    "2": ("Probleem/Wens", 'meld'),
    "3": ("Oorzaak/Analyse", 'oorz'),
    "4": ("Oplossing/SvZ", 'opl'),
    "5": ("Vervolgactie", 'verv'),
    "6": ("Voortgang", 'voortg')
}

statdict = {
    "0": ("gemeld", 0, -1),
    "1": ("in behandeling", 1, -1),
    "2": ("oplossing controleren", 2, -1),
    "3": ("nog niet opgelost", 3, -1),
    "4": ("afgehandeld", 4, -1),
    "5": ("afgehandeld - vervolg", 5, -1)
}

catdict = {
    "P": ("probleem", 1, -1),
    "W": ("wens", 2, -1),
    " ": ("onbekend", 0, -1),
    "V": ("vraag", 3, -1),
    "I": ("idee", 4, -1),
    "F": ("div. informatie", 5, -1)
}


class DataError(ValueError):    # Exception):
    "Eigen all-purpose exception - maakt resultaat testen eenvoudiger"
    pass


def get_projnames():
    data = []
    with APPS.open() as f_in:
        for line in f_in:
            sel, naam, titel, oms = line.strip().split(";")
            if sel == "X":
                data.append((naam.capitalize(), titel.capitalize(), oms))
    data = data
    return sorted(data)


