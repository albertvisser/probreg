"""fixture functions for unittests/dml_xml.py
"""
import pytest
import probreg.dml_xml as dml


@pytest.fixture
def get_acties_fixture(tmp_path):
    """creates sample XML file for get_acties unittest
    """
    testfilepath = tmp_path / 'testprobregdml.xml'
    testroot = dml.Element('acties')
    sett = dml.SubElement(testroot, 'settings')
    stats = dml.SubElement(sett, 'stats')
    stat = dml.SubElement(stats, 'stat', attrib={'value': "0", 'order': '0'})
    stat.text = 'gemeld'
    stat = dml.SubElement(stats, 'stat', attrib={'value': "1", 'order': '1'})
    stat.text = 'In behandeling'
    cats = dml.SubElement(sett, 'cats')
    cat = dml.SubElement(cats, 'cat', attrib={'value': 'P', 'order': '1'})
    cat.text = 'Probleem'
    cat = dml.SubElement(cats, 'cat', attrib={'value': 'W', 'order': '2'})
    cat.text = 'Wens'
    actie = dml.SubElement(testroot, 'actie', attrib={'id': '1', 'soort': 'P', 'status': '0'})
    titel = dml.SubElement(actie, 'titel')
    titel.text = 'Een actie'
    actie = dml.SubElement(testroot, 'actie', attrib={'id': '2', 'soort': 'P', 'status': '1',
                                                      'datum': '1', 'updated': '2', 'arch': 'arch'})
    titel = dml.SubElement(actie, 'titel')
    titel.text = 'Nog een actie'
    actie = dml.SubElement(testroot, 'actie', attrib={'id': '3', 'soort': 'W', 'status': '0',
                                                      'datum': '1', 'updated': '2', 'arch': 'herl'})
    titel = dml.SubElement(actie, 'titel')
    titel.text = 'Een andere actie'
    actie = dml.SubElement(testroot, 'actie', attrib={'id': '4', 'soort': 'P', 'status': '1',
                                                      'datum': '1', 'updated': '2', 'arch': ''})
    titel = dml.SubElement(actie, 'titel')
    titel.text = 'Ook een actie'
    actie = dml.SubElement(testroot, 'actie', attrib={'id': '5', 'soort': 'W', 'status': '0',
                                                      'datum': '1', 'updated': '2', 'arch': 'arch'})
    titel = dml.SubElement(actie, 'titel')
    titel.text = 'Geen actie'
    actie = dml.SubElement(testroot, 'actie', attrib={'id': '6', 'soort': 'W', 'status': '1',
                                                      'datum': '1', 'updated': '2', 'arch': 'herl'})
    titel = dml.SubElement(actie, 'titel')
    # titel.text = 'Iets heel anders'
    titel.text = ''
    dml.ElementTree(testroot).write(str(testfilepath))
    return testfilepath


@pytest.fixture
def settings_fixture(tmp_path):
    """creates sample Settings object for read unittest via class, so we have options
    """
    yield SettingsFixture(tmp_path)


class SettingsFixture:
    """create sample XML file from one of 4 possibilities:
    - nosett: a file with just a root element
    - justsett: a file with only the settings element under the root
    - toplevels: a file with the settings element and its attributes + the elements directly under it
    - all_levels: a complete settings element
    """
    def __init__(self, tmp_path):
        self.path = tmp_path / 'testprobregdml.xml'

    def nosett(self):
        "create XML in memory: only the root"
        self.root = dml.Element('acties')
        return self.finish()

    def justsett(self):
        "create XML in memory: root and settings element"
        self.root = dml.Element('acties')
        dml.SubElement(self.root, 'settings')
        return self.finish()

    def toplevels(self):
        "create XML in memory: all but the lowest level"
        self.root = dml.Element('acties')
        sett = dml.SubElement(self.root, 'settings')
        sett.set('imagecount', '5')
        sett.set('startitem', '15')
        dml.SubElement(sett, 'stats')
        dml.SubElement(sett, 'cats')
        dml.SubElement(sett, 'koppen')
        return self.finish()

    def all_levels(self):
        "create the complete XML in memory"
        self.root = dml.Element('acties')
        sett = dml.SubElement(self.root, 'settings')
        sett.set('imagecount', '5')
        sett.set('startitem', '15')
        stats = dml.SubElement(sett, 'stats')
        stat = dml.SubElement(stats, 'stat', attrib={'value': "0", 'order': '0'})
        stat.text = 'gemeld'
        stat = dml.SubElement(stats, 'stat', attrib={'value': "1", 'order': '1'})
        stat.text = 'In behandeling'
        cats = dml.SubElement(sett, 'cats')
        cat = dml.SubElement(cats, 'cat', attrib={'value': 'P', 'order': '1'})
        cat.text = 'Probleem'
        cat = dml.SubElement(cats, 'cat', attrib={'value': 'W', 'order': '2'})
        cat.text = 'Wens'
        headings = dml.SubElement(sett, 'koppen')
        head = dml.SubElement(headings, 'kop', attrib={'value': '0'})
        head.text = 'Overzicht'
        head = dml.SubElement(headings, 'kop', attrib={'value': '1'})
        head.text = 'Details'
        return self.finish()

    def finish(self):
        """write the XML to a file and create & return the Settings structure
        """
        dml.ElementTree(self.root).write(str(self.path))
        # return dml.Settings(self.path)
        return self.path


@pytest.fixture
def settings_output():
    """expected output from the Settings.write() method with the monkeypatchings in place
    """
    return {'new': ("called Settings()\n"
                    "called Element() with args ('acties',)\n"
                    "called Element.__setattr__() with args ('tag', 'acties')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called ElementTree.__init__()\n"
                    "called Element.find() with args ('settings',)\n"
                    "called SubElement() with args  ['parent', 'settings'] {}\n"
                    "called Element() with args ('settings',)\n"
                    "called Element.__setattr__() with args ('tag', 'settings')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.set() with args ('imagecount', '5')\n"
                    "called Element.set() with args ('startitem', '15')\n"
                    "called SubElement() with args  ['parent', 'stats'] {}\n"
                    "called Element() with args ('stats',)\n"
                    "called Element.__setattr__() with args ('tag', 'stats')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called SubElement() with args  ['parent', 'cats'] {}\n"
                    "called Element() with args ('cats',)\n"
                    "called Element.__setattr__() with args ('tag', 'cats')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called SubElement() with args  ['parent', 'koppen'] {}\n"
                    "called Element() with args ('koppen',)\n"
                    "called Element.__setattr__() with args ('tag', 'koppen')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called shutil.copyfile with args ('anything_goes', 'anything_goes.old')\n"
                    "called ElementTree.write() with args ('anything_goes',)"
                    " {'encoding': 'utf-8', 'xml_declaration': True}\n"),
            'existing': ("called Settings()\n"
                         "called ElementTree.__init__()\n"
                         "called ElementTree.getroot()\n"
                         "called Element() with args ('acties',)\n"
                         "called Element.__setattr__() with args ('tag', 'acties')\n"
                         "called Element.__setattr__() with args ('attrs', {})\n"
                         "called Element.find() with args ('settings',)\n"
                         "called Element() with args ('settings',)\n"
                         "called Element.__setattr__() with args ('tag', 'settings')\n"
                         "called Element.__setattr__() with args ('attrs', {})\n"
                         "called Element.set() with args ('imagecount', '5')\n"
                         "called Element.set() with args ('startitem', '15')\n"
                         "called Element() with args ('stats',)\n"
                         "called Element.__setattr__() with args ('tag', 'stats')\n"
                         "called Element.__setattr__() with args ('attrs', {})\n"
                         "called Element() with args ('cats',)\n"
                         "called Element.__setattr__() with args ('tag', 'cats')\n"
                         "called Element.__setattr__() with args ('attrs', {})\n"
                         "called Element() with args ('koppen',)\n"
                         "called Element.__setattr__() with args ('tag', 'koppen')\n"
                         "called Element.__setattr__() with args ('attrs', {})\n"
                         "called Element() with args ('xxx',)\n"
                         "called Element.__setattr__() with args ('tag', 'xxx')\n"
                         "called Element.__setattr__() with args ('attrs', {})\n"
                         "called Element.remove() for subelement stats\n"
                         "called Element.remove() for subelement cats\n"
                         "called Element.remove() for subelement koppen\n"
                         "called SubElement() with args  ['parent', 'stats'] {}\n"
                         "called Element() with args ('stats',)\n"
                         "called Element.__setattr__() with args ('tag', 'stats')\n"
                         "called Element.__setattr__() with args ('attrs', {})\n"
                         "called SubElement() with args  ['parent', 'stat'] {'value': '0'}\n"
                         "called Element() with args ('stat',)\n"
                         "called Element.__setattr__() with args ('tag', 'stat')\n"
                         "called Element.__setattr__() with args ('attrs', {})\n"
                         "called Element.set() with args ('order', '0')\n"
                         "called Element.__setattr__() with args ('text', 'this')\n"
                         "called SubElement() with args  ['parent', 'stat'] {'value': '1'}\n"
                         "called Element() with args ('stat',)\n"
                         "called Element.__setattr__() with args ('tag', 'stat')\n"
                         "called Element.__setattr__() with args ('attrs', {})\n"
                         "called Element.set() with args ('order', '1')\n"
                         "called Element.__setattr__() with args ('text', 'that')\n"
                         "called SubElement() with args  ['parent', 'cats'] {}\n"
                         "called Element() with args ('cats',)\n"
                         "called Element.__setattr__() with args ('tag', 'cats')\n"
                         "called Element.__setattr__() with args ('attrs', {})\n"
                         "called SubElement() with args  ['parent', 'cat'] {'value': 'a'}\n"
                         "called Element() with args ('cat',)\n"
                         "called Element.__setattr__() with args ('tag', 'cat')\n"
                         "called Element.__setattr__() with args ('attrs', {})\n"
                         "called Element.set() with args ('order', '0')\n"
                         "called Element.__setattr__() with args ('text', 'something')\n"
                         "called SubElement() with args  ['parent', 'cat'] {'value': 'b'}\n"
                         "called Element() with args ('cat',)\n"
                         "called Element.__setattr__() with args ('tag', 'cat')\n"
                         "called Element.__setattr__() with args ('attrs', {})\n"
                         "called Element.set() with args ('order', '1')\n"
                         "called Element.__setattr__() with args ('text', 'anything')\n"
                         "called SubElement() with args  ['parent', 'koppen'] {}\n"
                         "called Element() with args ('koppen',)\n"
                         "called Element.__setattr__() with args ('tag', 'koppen')\n"
                         "called Element.__setattr__() with args ('attrs', {})\n"
                         "called SubElement() with args  ['parent', 'kop'] {'value': '1'}\n"
                         "called Element() with args ('kop',)\n"
                         "called Element.__setattr__() with args ('tag', 'kop')\n"
                         "called Element.__setattr__() with args ('attrs', {})\n"
                         "called Element.__setattr__() with args ('text', 'ook')\n"
                         "called SubElement() with args  ['parent', 'kop'] {'value': '2'}\n"
                         "called Element() with args ('kop',)\n"
                         "called Element.__setattr__() with args ('tag', 'kop')\n"
                         "called Element.__setattr__() with args ('attrs', {})\n"
                         "called Element.__setattr__() with args ('text', 'eek')\n"
                         "called shutil.copyfile with args ('anything_goes', 'anything_goes.old')\n"
                         "called ElementTree.write() with args ('anything_goes',)"
                         " {'encoding': 'utf-8', 'xml_declaration': True}\n")}


@pytest.fixture
def actie_fixture(tmp_path):
    """creates sample Actie object for read unittest via class, so we have options
    """
    yield ActieFixture(tmp_path)


class ActieFixture:
    """create sample XML file from one of 4 possibilities:
    - justaroot: a file with just a root element
    - justsett: a file with only the settings element under the root
    - toplevels: a file with the settings element and its attributes + the elements directly under it
    - all_levels: a complete settings element
    """
    def __init__(self, tmp_path):
        self.path = tmp_path / 'testprobregdml.xml'

    def justaroot(self):
        "create XML in memory: only the root"
        self.root = dml.Element('acties')
        return self.finish()

    def wrongaction(self):
        self.root = dml.Element('acties')
        dml.SubElement(self.root, 'actie', id='15')
        return self.finish()

    def incomplete(self):
        self.root = dml.Element('acties')
        actie = dml.SubElement(self.root, 'actie', id='1', status='1', soort='P')
        dml.SubElement(actie, 'titel')
        dml.SubElement(actie, 'melding')
        dml.SubElement(actie, 'oorzaak')
        dml.SubElement(actie, 'oplossing')
        dml.SubElement(actie, 'vervolg')
        dml.SubElement(actie, 'events')
        dml.SubElement(actie, 'image')  # wrong type of element
        return self.finish()

    def incomplete_2(self):
        self.root = dml.Element('acties')
        actie = dml.SubElement(self.root, 'actie', id='1', status='1', soort='P')
        dml.SubElement(actie, 'titel')
        dml.SubElement(actie, 'melding')
        dml.SubElement(actie, 'oorzaak')
        dml.SubElement(actie, 'oplossing')
        dml.SubElement(actie, 'vervolg')
        dml.SubElement(actie, 'events')
        dml.SubElement(actie, 'images')
        return self.finish()

    def complete(self):
        self.root = dml.Element('acties')
        actie = dml.SubElement(self.root, 'actie', id='1', datum='x', status='1', soort='P',
                               arch='arch', updated='y')
        dml.SubElement(actie, 'titel').text = 'Dit'
        dml.SubElement(actie, 'melding').text = 'Dat'
        dml.SubElement(actie, 'oorzaak').text = 'Iets'
        dml.SubElement(actie, 'oplossing').text = 'Iets anders'
        dml.SubElement(actie, 'vervolg').text = 'Nog iets'
        ev = dml.SubElement(actie, 'events')
        dml.SubElement(ev, 'event', id='now').text = 'hello'
        dml.SubElement(ev, 'event', id='then').text = 'sailor'
        im = dml.SubElement(actie, 'images')
        dml.SubElement(im, 'image', filename='/tmp/x.img').text = '"stuffing"'
        return self.finish()

    def finish(self):
        """write the XML to a file and create & return the Actie structure
        """
        dml.ElementTree(self.root).write(str(self.path))
        # return dml.Actie(self.path)
        return self.path


@pytest.fixture
def actie_output():
    return {'new': ("called Element() with args ('acties',)\n"
                    "called Element.__setattr__() with args ('tag', 'acties')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called SubElement() with args  ['parent', 'settings'] {}\n"
                    "called Element() with args ('settings',)\n"
                    "called Element.__setattr__() with args ('tag', 'settings')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.set() with args ('imagecount', '0')\n"
                    "called Element.set() with args ('startitem', '1')\n"
                    "called SubElement() with args  ['parent', 'actie'] {}\n"
                    "called Element() with args ('actie',)\n"
                    "called Element.__setattr__() with args ('tag', 'actie')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.set() with args ('id', '1')\n"
                    "called Element.set() with args ('datum', 'now')\n"
                    "called Element.set() with first arg updated\n"
                    "called Element.set() with args ('soort', 'P')\n"
                    "called Element.set() with args ('status', '0')\n"
                    "called Element.get() with args ('arch',)\n"
                    "called Element.find() with args ('titel',)\n"
                    "called SubElement() with args  ['parent', 'titel'] {}\n"
                    "called Element() with args ('titel',)\n"
                    "called Element.__setattr__() with args ('tag', 'titel')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.__setattr__() with args ('text', 'Paniek in de biertent')\n"
                    "called Element.find() with args ('melding',)\n"
                    "called SubElement() with args  ['parent', 'melding'] {}\n"
                    "called Element() with args ('melding',)\n"
                    "called Element.__setattr__() with args ('tag', 'melding')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.__setattr__() with args ('text', 'Er is iets gebeurd')\n"
                    "called Element.find() with args ('oorzaak',)\n"
                    "called SubElement() with args  ['parent', 'oorzaak'] {}\n"
                    "called Element() with args ('oorzaak',)\n"
                    "called Element.__setattr__() with args ('tag', 'oorzaak')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.__setattr__() with args ('text', 'Het kwam hierdoor')\n"
                    "called Element.find() with args ('oplossing',)\n"
                    "called SubElement() with args  ['parent', 'oplossing'] {}\n"
                    "called Element() with args ('oplossing',)\n"
                    "called Element.__setattr__() with args ('tag', 'oplossing')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.__setattr__() with args ('text', 'Dit hebben we eraan gedaan')\n"
                    "called Element.find() with args ('vervolg',)\n"
                    "called SubElement() with args  ['parent', 'vervolg'] {}\n"
                    "called Element() with args ('vervolg',)\n"
                    "called Element.__setattr__() with args ('tag', 'vervolg')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.__setattr__() with args ('text', 'Dit moet ook nog')\n"
                    "called Element.find() with args ('events',)\n"
                    "called SubElement() with args  ['parent', 'events'] {}\n"
                    "called Element() with args ('events',)\n"
                    "called Element.__setattr__() with args ('tag', 'events')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called SubElement() with args  ['parent', 'event'] {'id': 'ooit'}\n"
                    "called Element() with args ('event',)\n"
                    "called Element.__setattr__() with args ('tag', 'event')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.__setattr__() with args ('text', 'deden we dit')\n"
                    "called SubElement() with args  ['parent', 'event'] {'id': 'later'}\n"
                    "called Element() with args ('event',)\n"
                    "called Element.__setattr__() with args ('tag', 'event')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.__setattr__() with args ('text', 'deden we dit')\n"
                    "called Element.find() with args ('images',)\n"
                    "called SubElement() with args  ['parent', 'images'] {}\n"
                    "called Element() with args ('images',)\n"
                    "called Element.__setattr__() with args ('tag', 'images')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called ElementTree.__init__()\n"
                    "called shutil.copyfile with args ('/tmp/testactie.xml',"
                    " '/tmp/testactie.xml.old')\n"
                    "called ElementTree.write() with args ('/tmp/testactie.xml',)"
                    " {'encoding': 'utf-8', 'xml_declaration': True}\n"),
            'old': ("called ElementTree.__init__()\n"
                    "called ElementTree.getroot()\n"
                    "called Element() with args ()\n"
                    "called Element.__setattr__() with args ('tag', '')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.find() with args ('settings',)\n"
                    "called Element() with args ('settings',)\n"
                    "called Element.__setattr__() with args ('tag', 'settings')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.set() with args ('imagecount', '0')\n"
                    "called Element.set() with args ('startitem', '1')\n"
                    "called Element.findall() with args ('actie',)\n"
                    "called Element() with args ('actie',)\n"
                    "called Element.__setattr__() with args ('tag', 'actie')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element() with args ('actie',)\n"
                    "called Element.__setattr__() with args ('tag', 'actie')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.get() with args ('id',)\n"
                    "called Element.set() with first arg updated\n"
                    "called Element.set() with args ('soort', ' ')\n"
                    "called Element.set() with args ('status', '0')\n"
                    "called Element.set() with args ('arch', 'arch')\n"
                    "called Element.find() with args ('titel',)\n"
                    "called Element() with args ('titel',)\n"
                    "called Element.__setattr__() with args ('tag', 'titel')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.__setattr__() with args ('text', 'Paniek in de biertent')\n"
                    "called Element.find() with args ('melding',)\n"
                    "called Element() with args ('melding',)\n"
                    "called Element.__setattr__() with args ('tag', 'melding')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.__setattr__() with args ('text', 'Er is iets gebeurd')\n"
                    "called Element.find() with args ('oorzaak',)\n"
                    "called Element() with args ('oorzaak',)\n"
                    "called Element.__setattr__() with args ('tag', 'oorzaak')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.__setattr__() with args ('text', 'Het kwam hierdoor')\n"
                    "called Element.find() with args ('oplossing',)\n"
                    "called Element() with args ('oplossing',)\n"
                    "called Element.__setattr__() with args ('tag', 'oplossing')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.__setattr__() with args ('text', 'Dit hebben we eraan gedaan')\n"
                    "called Element.find() with args ('vervolg',)\n"
                    "called Element() with args ('vervolg',)\n"
                    "called Element.__setattr__() with args ('tag', 'vervolg')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.__setattr__() with args ('text', 'Dit moet ook nog')\n"
                    "called Element.find() with args ('events',)\n"
                    "called Element() with args ('events',)\n"
                    "called Element.__setattr__() with args ('tag', 'events')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.remove() for subelement events\n"
                    "called SubElement() with args  ['parent', 'events'] {}\n"
                    "called Element() with args ('events',)\n"
                    "called Element.__setattr__() with args ('tag', 'events')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called SubElement() with args  ['parent', 'event'] {'id': 'ooit'}\n"
                    "called Element() with args ('event',)\n"
                    "called Element.__setattr__() with args ('tag', 'event')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.__setattr__() with args ('text', 'deden we dit')\n"
                    "called SubElement() with args  ['parent', 'event'] {'id': 'later'}\n"
                    "called Element() with args ('event',)\n"
                    "called Element.__setattr__() with args ('tag', 'event')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.__setattr__() with args ('text', 'deden we dit')\n"
                    "called Element.find() with args ('images',)\n"
                    "called Element() with args ('images',)\n"
                    "called Element.__setattr__() with args ('tag', 'images')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called Element.remove() for subelement images\n"
                    "called SubElement() with args  ['parent', 'images'] {}\n"
                    "called Element() with args ('images',)\n"
                    "called Element.__setattr__() with args ('tag', 'images')\n"
                    "called Element.__setattr__() with args ('attrs', {})\n"
                    "called ElementTree.__init__()\n"
                    "called shutil.copyfile with args ('/tmp/testactie.xml',"
                    " '/tmp/testactie.xml.old')\n"
                    "called ElementTree.write() with args ('/tmp/testactie.xml',)"
                    " {'encoding': 'utf-8', 'xml_declaration': True}\n")
            }
