import sys
import os
from logbook import Logger, FileHandler
logger = Logger('dmlsql')
import pprint as pp
import datetime as dt
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dml_sql import get_acties, Settings, Actie

def list(self):
    "uitlijsten gegevens van actie object"
    print self.soort, self.status
    pp.pprint(self.settings.__dict__)
    logger.info(  "%s %s gemeld op %s status %s %s" % (
        self.get_soorttext(),
        self.id,
        self.datum,
        self.status,
        self.get_statustext()
        ))
    logger.info(  "Titel: {} - {}".format(self.over, self.titel))
    logger.info(  "Melding: {}".format(self.melding))
    logger.info(  "Oorzaak: {}".format(self.oorzaak))
    logger.info(  "Oplossing: {}".format(self.oplossing))
    logger.info(  "Vervolg: {}".format(self.vervolg))
    logger.info(  "Verslag:")
    for x, y in self.events:
        logger.info("\t {0} - {1}".format(x, y))
    if self.arch:
        logger.info("  Actie is gearchiveerd.")

def test_get_acties(fnaam, op1, op2):
    "test routine"
    logger.info('test get_acties voor {} {} {}'.format(fnaam, op1, op2))
    h = get_acties(fnaam, op1, op2)
    i = 0
    for item in h:
        i += 1
        logger.info('  {} {} - {}'.format(item[0], item[6], item[7]))
    logger.info("  {} records\n".format(i))

def test_settings(fnaam=None, obj=None):
    "test routine"
    if fnaam is not None:
        logger.info('test settings voor {}'.format(fnaam))
        h = Settings(fnaam)
    elif obj is not None:
        logger.info('test settings voor {}'.format(obj))
        h = obj
    else:
        logger.info('no filename, no object, nothing')
        return
    if h.meld:
        logger.info(h.meld)
    logger.info('  {}'.format(h.kop))
    logger.info('  {}'.format(h.stat))
    logger.info('  {}'.format(h.cat))
    return h

def test_wijzigsettings(item, soort, key, tekst, waarde, data=None,
        update=False):
    logger.info('test wijzigsettings voor {} {} {} {} {} {} {}'.format(item, soort,
        key, tekst, waarde, data, update))
    h = item
    if soort == 'stat':
        h.stat[key] = (tekst, waarde, data)
    elif soort == 'cat':
        h.cat[key] = (tekst, waarde, data)
    elif soort == 'kop':
        h.kop[key] = (tekst, waarde)
    test_settings(obj=h)
    if update:
        h.write()
    return h

def test_actie(fnaam="", id='', obj=None):
    "test routine"
    logger.info('test actie voor file {} id {} obj {}'.format(fnaam, id, obj))
    if obj:
        p = obj
    elif fnaam and id:
        p = Actie(fnaam, id)
    else:
        return
    ## for key, item in p.__dict__:
        ## logger.info('  {}: {}'.format(key, item))
    if not p.exists:
        logger.info('  actie bestaat niet')
    else:
        list(p)
    return p

def test_wijzig_actie(obj, soort, data, update=False):
    p = obj
    if soort == 'over':
        p.over = data
    elif soort == 'titel':
        p.titel = data
    elif soort == 'soort':
        p.set_soort(data)
    elif soort == 'status':
        p.set_status(data)
    elif soort == 'melding':
        p.melding = data
    elif soort == 'oorzaak':
        p.oorzaak = data
    elif soort == 'oplossing':
        p.oplossing = data
    elif soort == 'event':
        p.events.append((dt.datetime.today().isoformat(' ')[:19], data))
    elif soort == 'statuscode':
        p.status = data
    elif soort == 'arch':
        p.set_arch(data)
    list(p)
    if update:
        p.write()
    return p

if __name__ == "__main__":
    fnm = "afrift"
    log_handler = FileHandler('get_acties_sql.log', mode='w')
    with log_handler.applicationbound():
        ## test_get_acties(fnm, {}, "")
        ## test_get_acties(fnm, {"idlt": "2010", }, "")
        ## test_get_acties(fnm, {"idlt": "2010",  "id": "and",  "idgt": "2007-0003"}, "")
        ## test_get_acties(fnm, {"idgt": "2010",  "id": "or",  "idlt": "2007-0003"}, "")
        ## test_get_acties(fnm, {"idgt": "2007-0003",}, "")
        test_get_acties(fnm, {"status": ["1"]}, "")
        test_get_acties(fnm, {"status": ["1", "2"]}, "")
        test_get_acties(fnm, {"soort" : ["4"]}, '')
        test_get_acties(fnm, {"soort" : ["4", "2"]}, '')
        ## test_get_acties(fnm, {"titel": "en"}, "")
        ## test_get_acties(fnm, {}, "arch")
        ## test_get_acties(fnm, {}, "alles")
    fnm = "_basic"
    ## log_handler = FileHandler('settings_sql.log', mode='w')
    ## with log_handler.applicationbound():
        ## h = test_settings()
        ## h = test_settings(fnaam='bestaatniet')
        ## h = test_settings(fnaam=fnm)
        ## h = test_wijzigsettings(h, 'stat', '7', "Gloekgloekgloe", 15, -1)
        ## h = test_wijzigsettings(h, 'cat', "X", "Willen we niet weten", 6, -1)
        ## h = test_wijzigsettings(h, 'kop', '4', "Gargl", "opl")
        ## h = test_settings(obj=h)
        ## h = test_wijzigsettings(h, 'stat','7', "Gloekgloekgloe", 7, -1)
        ## h = test_wijzigsettings(h, 'cat', "X", "Ahum ahum", 7, -1)
        ## h = test_wijzigsettings(h, 'kop','4', "Oplossing/SvZ", "opl", update = True)
        ## h = test_settings(fnaam=fnm)
    ## log_handler = FileHandler('actie_sql.log', mode='w')
    ## with log_handler.applicationbound():
        ## p = test_actie(fnm, "2009-0002")
        ## p = test_actie(fnm, "2011-0002")
        ## p = test_actie(fnm, '0')
        ## p = test_wijzig_actie(p, 'over', "test")
        ## p = test_wijzig_actie(p, 'titel', "nieuwe actie")
        ## p = test_wijzig_actie(p, 'soort', "probleem")
        ## p = test_wijzig_actie(p, 'status', "in behandeling")
        ## p = test_actie(obj=p)
        ## p = test_wijzig_actie(p, 'melding', "Het is niet gebeurd")
        ## p = test_wijzig_actie(p, 'oorzaak', "Het leek maar alsof")
        ## p = test_wijzig_actie(p, 'oplossing', "Dus hebben we teruggedraaid wat we er aan gedaan hebben")
        ## p = test_wijzig_actie(p, 'event', "Beschrijving oplossing aangepast")
        ## p = test_wijzig_actie(p, 'statuscode', 2)
        ## p = test_wijzig_actie(p, 'arch', True, update=True)
        ## p = test_actie(fnm, p.nummer)
