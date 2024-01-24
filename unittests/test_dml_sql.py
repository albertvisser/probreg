"""unittests for ./probreg/@@@.py
"""
"""Unit tests for SQL dml
"""
import sys
import os
import datetime as dt
import pytest
# import probreg.dml_sql as dml

def list(self):
    """stub
    """
    "uitlijsten gegevens van actie object"
    print(self.soort, self.status)
    pp.pprint(self.settings.__dict__)
    logger.info("%s %s gemeld op %s status %s %s" % (self.get_soorttext(),
                                                     self.id,
                                                     self.datum,
                                                     self.status,
                                                     self.get_statustext()))
    logger.info("Titel: {} - {}".format(self.over, self.titel))
    logger.info("Melding: {}".format(self.melding))
    logger.info("Oorzaak: {}".format(self.oorzaak))
    logger.info("Oplossing: {}".format(self.oplossing))
    logger.info("Vervolg: {}".format(self.vervolg))
    logger.info("Verslag:")
    for x, y in self.events:
        logger.info("\t {0} - {1}".format(x, y))
    if self.arch:
        logger.info("  Actie is gearchiveerd.")


def _test_get_acties(fnaam, op1, op2):
    """unittest for @@@.get_acties
    """
    "test routine"
    logger.info('test get_acties voor {} {} {}'.format(fnaam, op1, op2))
    h = get_acties(fnaam, op1, op2)
    i = 0
    for item in h:
        i += 1
        logger.info('  {} {} - {}'.format(item[0], item[6], item[7]))
    logger.info("  {} records\n".format(i))


def _test_settings(fnaam=None, obj=None):
    """unittest for @@@.settings
    """
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


def _test_wijzigsettings(item, soort, key, tekst, waarde, data=None, update=False):
    """unittest for @@@.wijzigsettings
    """
    logger.info('test wijzigsettings voor {} {} {} {} {} {} {}'.format(
        item, soort, key, tekst, waarde, data, update))
    h = item
    if soort == 'stat':
        h.stat[key] = (tekst, waarde, data)
    elif soort == 'cat':
        h.cat[key] = (tekst, waarde, data)
    elif soort == 'kop':
        h.kop[key] = (tekst, waarde)
    test_settings(obj=h)
    if update:
        h.write(soort)
    return h


def _test_actie(fnaam="", id='', obj=None):
    """unittest for @@@.actie
    """
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


def _test_wijzig_actie(obj, soort, data, update=False):
    """unittest for @@@.wijzig_actie
    """
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
