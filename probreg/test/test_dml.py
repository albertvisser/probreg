import os
import sys
from logbook import Logger, FileHandler
logger = Logger('dmlxml')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
## from dml import DataError, get_nieuwetitel, get_acties, Actie, Settings
from dml_single_codebase import get_nieuwetitel, get_config_objects
for key, value in get_config_objects(sql=False).items():
    globals()[key] = value

xmlfile = "/home/albert/probreg/jvs.xml" # todo.xml"

def test_laatste():
    try:
        h = get_nieuwetitel(xmlfile)
    except DataError as meld:
        logger.info(meld)
    else:
        logger.info(h)

def test_acties(arch=None, select=None):
    logger.info('test get_acties voor {} {}'.format(arch, select))
    try:
        if arch is not None:
            lijst = get_acties(xmlfile, arch=arch)
        elif select is not None:
            lijst = get_acties(xmlfile, select=select)
        else:
            lijst = get_acties()
    except DataError as meld:
        logger.info(meld)
        return
    if len(lijst) == 0:
        logger.info("(nog) geen acties gemeld")
    else:
        for x in lijst:
            logger.info(x)

def test_actie(sleutel=None):
    if sleutel is None:
        h = Actie(xmlfile, 0)
        logger.info("na init")
        h.list()
        h.titel = "er ging nog iets mis"
        h.probleem = "dit is dit keer het probleem"
        h.oorzaak = "het kwam ditmaal hierdoor"
        h.oplossing  = "we hebben het weer zo opgelost"
        h.vervolg = "uitzoeken of er een verband is"
        h.stand = "net begonnen"
        h.events = [("eerste","hallo"), ("tweede","daar")]
        h.list()
        h.write()
        return h.id
    h = Actie(xmlfile, sleutel)
    logger.info(h.meld)
    if h.exists:
        h.list()
    else:
        logger.info("geen item met deze sleutel bekend")
        #~ h = Actie(fn,0)
        #~ logger.info "na init"
        #~ h.list()
        #~ h.setStatus(2)
        h.set_status("in behandeling")
        #~ h.setSoort("P")
        h.set_soort("wens")
        #~ h.titel = "er ging iets mis"
        #~ h.probleem = "dit is het probleem"
        #~ h.oorzaak = "het kwam hierdoor"
        #~ h.oplossing  = "we hebben het zo opgelost"
        #~ h.vervolg = "maar er moet nog een vervolg komen"
        #~ h.list()
        #~ h.write()

def test_settings():
    h = Settings(xmlfile)
    logger.info("-- na init ----------------")
    for x in list(h.__dict__.items()):
        logger.info(x)
    logger.info("stat: ")
    for x in h.stat:
        logger.info("\t", x, h.stat[x], sep=" ")
    logger.info("cat: ")
    for x in h.cat:
        logger.info("\t", x, h.cat[x], sep=" ")
    logger.info("kop: ")
    for x in h.kop:
        logger.info("\t", x, h.kop[x], sep=" ")
    return
    stats = {}
    cats = {}
    tabs = {}
    for x in list(h.stat.keys()):
        stats[h.stat[x][1]] = (x, h.stat[x][0])
    for x in list(h.cat.keys()):
        cats[h.cat[x][1]] = (x, h.cat[x][0])
    for x in list(h.kop.keys()):
        tabs[x] = h.kop[x]
    logger.info(stats)
    logger.info(cats)
    logger.info(tabs)
    #~ try:
        #~ h.set("test")
        #~ h.set("cat")
        #~ h.set("stat")
        #~ h.set("cat", "test")
        #~ h.set("stat", "test")
        #~ h.set("cat", "V", "vraag")
        #~ h.set("stat", "4", "onoplosbaar")
        #~ h.set("cat", "", "o niks")
        #~ h.set("stat", "3", "opgelost")
        #~ logger.info h.get("test")
        #~ logger.info h.get("cat")
        #~ logger.info h.get("stat", "x")
        #~ logger.info h.get("cat", "x")
        #~ logger.info h.get("stat", "1")
        #~ logger.info h.get("cat", "")
        #~ logger.info h.get("kop", "1")
        #~ logger.info h.get("stat", 3)
        #~ logger.info h.get("cat", 3)
        #~ logger.info h.get("kop", 1)
    #~ except DataError as meld:
        #~ logger.info meld
        #~ return
    #~ logger.info "-- na set -----------------"
    #~ for x in h.__dict__.items():
        #~ logger.info x
    for x in list(h.stat.keys()):
        h.set("stat", x, (h.stat[x][0], x))
    i = 0
    for x in list(h.cat.keys()):
        h.set("cat", x, (h.cat[x][0], str(i)))
        i += 1
    logger.info("-- na bijwerken -----------")
    logger.info("stat: ", h.stat, sep=" ")
    logger.info("cat:", h.cat, sep=" ")
    h.set("cat", "V", ("vraag", "5"))
    h.set("stat", "4", ("onoplosbaar", "7"))
    h.set("kop", "7", "bonuspagina")
    h.set("cat", "", ("o niks", "8"))
    h.set("stat", "3", ("opgelost", "15"))
    h.set("kop", "2", "opmerking")
    logger.info("-- na sets -----------------")
    logger.info("stat: ", h.stat, sep=" ")
    logger.info("cat:", h.cat, sep=" ")
    logger.info("kop:", h.kop, sep=" ")
    h.write()

def test_archiveren():
    h = Actie(xmlfile, "2006-0001")
    logger.info(h.meld)
    if h.exists:
        h.list()
        h.setArch(True)
        h.write()
        h.read()
        h.list()

if __name__ == "__main__":
    log_handler = FileHandler('get_acties_xml_1.log', mode='w')
    with log_handler.applicationbound():
        test_acties(arch='')
        test_acties(select={"idgt": "2006-0010"})
        test_acties(select={"idlt":  "2005-0019"})
        test_acties(select={"idgt": "2005-0019" , "idlt": "2006-0010"})
        test_acties(select={"idgt": "2005-0019" , "idlt": "2006-0010",  "id": "and" })
        test_acties(select={"idgt": "2006-0010" , "idlt": "2005-0019",  "id": "or" })
        test_acties(select={"status": ("0", "1", "3")})
        test_acties(select={"soort": ("W", "P")})
        test_acties(select={"titel": ("tekst")})
    ## log_handler = FileHandler('settings_xml_1.log', mode='w')
    ## with log_handler.applicationbound():
        ## test_settings()
    ## log_handler = FileHandler('actie_xml_1.log', mode='w')
    ## with log_handler.applicationbound():
        ## test_laatste()
        ## test_actie("2007-0001")
        ## test_actie("1")
        ## test_archiveren()
