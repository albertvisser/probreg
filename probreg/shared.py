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
import os
import enum
import logging
import pathlib
from datetime import datetime
import probreg.dml_django as dmls
import probreg.dml_xml as dmlx
import probreg.dml_mongo as dmlm
ROOT = pathlib.Path("/home/albert/projects/actiereg/actiereg")
DataType = enum.Enum('DataType', 'XML SQL MNG')
get_acties = {DataType.XML: dmlx.get_acties, DataType.SQL: dmls.get_acties,
              DataType.MNG: dmlm.get_acties}
Actie = {DataType.XML: dmlx.Actie, DataType.SQL: dmls.Actie, DataType.MNG: dmlm.Actie}
Settings = {DataType.XML: dmlx.Settings, DataType.SQL: dmls.Settings, DataType.MNG: dmlm.Settings}
DataError = {DataType.XML: dmlx.DataError, DataType.SQL: dmls.DataError,
             DataType.MNG: dmlm.DataError}
Order = enum.Enum('Order', 'A D')
logfile = pathlib.Path('/tmp') / 'logs' / 'probreg.log'
logfile.parent.mkdir(exist_ok=True)
logging.basicConfig(filename=logfile, level=logging.DEBUG,
                    format='%(asctime)s %(module)s: %(message)s')
app_title = 'Actiereg'


def log(msg, *args, **kwargs):
    "schrijf logregel indien debuggen gewenst"
    if 'DEBUG' in os.environ and os.environ['DEBUG']:
        logging.info(msg, *args, **kwargs)


def get_dts():
    "routine om een geformatteerd date/time stamp te verkrijgen"
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def data2str(data):
    "compatibility Python 2 / 3: turn PyQt data object into Python string"
    if sys.version < "3":
        return str(data.toPyObject())
    return str(data)


def data2int(data):
    "compatibility Python 2 / 3: turn PyQt data object into Python integer"
    if sys.version < "3":
        return int(data.toPyObject())
    return int(data)


def tabsize(pointsize):
    "pointsize omrekenen in pixels t.b.v. (gemiddelde) tekenbreedte"
    x, y = divmod(pointsize * 8, 10)
    return x * 4 if y < 5 else (x + 1) * 4


# verhuisd naar dmlx
# kopdict = {
#     "0": ("Lijst", 'index'),
#     "1": ("Titel/Status", 'detail'),
#     "2": ("Probleem/Wens", 'meld'),
#     "3": ("Oorzaak/Analyse", 'oorz'),
#     "4": ("Oplossing/SvZ", 'opl'),
#     "5": ("Vervolgactie", 'verv'),
#     "6": ("Voortgang", 'voortg')
# }
#
# statdict = {
#     "0": ("gemeld", 0, -1),
#     "1": ("in behandeling", 1, -1),
#     "2": ("oplossing controleren", 2, -1),
#     "3": ("nog niet opgelost", 3, -1),
#     "4": ("afgehandeld", 4, -1),
#     "5": ("afgehandeld - vervolg", 5, -1)
# }
#
# catdict = {
#     "P": ("probleem", 1, -1),
#     "W": ("wens", 2, -1),
#     " ": ("onbekend", 0, -1),
#     "V": ("vraag", 3, -1),
#     "I": ("idee", 4, -1),
#     "F": ("div. informatie", 5, -1)
# }
#
#
# class DataError(ValueError):    # Exception):
#     "Eigen all-purpose exception - maakt resultaat testen eenvoudiger"
#     pass
