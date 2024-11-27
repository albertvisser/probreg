"""unittests for ./probreg/main.py
"""
import types
import pytest
from probreg import main as testee


def test_dbstat2bookstat():
    """unittest for main.dbstat2bookstat
    """
    assert testee.db_stat_to_book_stat('x', (1, 2)) == [1, 'x']


def test_dbcat2bookcat():
    """unittest for main.dbcat2bookcat
    """
    assert testee.db_cat_to_book_cat('x', (1, 2)) == [1, 'x']


def test_dbhead2bookhead():
    """unittest for main.dbhead2bookhead
    """
    assert testee.db_head_to_book_head('1', ('text',)) == '1 Text'


def test_dbdate2listdate():
    """unittest for main.dbdate2listdate
    """
    assert testee.dbdate2listdate('2020-01-01 00:00:00') == '01-01-2020 00:00:00'
    assert testee.dbdate2listdate('y') == 'y'


def test_listdate2dbdate():
    """unittest for main.listdate2dbdate
    """
    assert testee.listdate2dbdate('01-01-2020 00:00:00') == '2020-01-01 00:00:00'
    assert testee.listdate2dbdate('y') == 'y'


class MockBook:
    """stub for MainWindow.book (choicebook/tabwidget object)
    """


class MockMainWindow:
    """stub for MainWindow object
    """
    def __init__(self, *args):  # , parent, name):
        print('called MainWindow.__init__() with args', args)
        # self.parent = parent
        self.gui = MockMainGui(self)
    def enable_settingsmenu(self):
        """stub
        """
        print('call MainWindow.enable_settingsmenu()')
    def set_windowtitle(self, title):
        """stub
        """
        print(f'call MainWindow.set_windowtitle({title})')
    def set_statusmessage(self, message=''):
        """stub
        """
        print(f'call MainWindow.set_statusmessage({message})')
    def enable_all_book_tabs(self, value):
        """stub
        """
        print(f'call MainWindow.enable_all_book_tabs({value})')


class MockMainGui:
    """stub for gui.MainGui object
    """
    def __init__(self, master):
        print('called MainGui.__init__()')
    def go(self):
        """stub
        """
        print('called MainGui.go()')
    def create_menu(self):
        """stub
        """
        print('called MainGui.create_menu()')
    def create_actions(self):
        """stub
        """
        print('called MainGui.create_actions()')
    def enable_book_tabs(self, *args, **kwargs):
        """stub
        """
        print('called MainGui.enable_book_tabs() with args', args, kwargs)
    def enable_all_other_tabs(self, value):
        """stub
        """
        print(f'called MainGui.enable_all_other_tabs() with arg `{value}`')
    def enable_settingsmenu(self):
        """stub
        """
        print('called MainGui.enable_settingsmenu()')
    def set_page(self, number):
        """stub
        """
        print(f'called MainGui.set_page({number})')
    def select_first_tab(self):
        """stub
        """
        print('called MainGui.select_first_tab()')
    def set_window_title(self, *args):
        """stub
        """
        print('called MainGui.set_window_title() with args', args)
    def set_tab_titles(self, titles):
        """stub
        """
        print(f'called MainGui.set_tab_titles([{titles}]')
    def set_page_title(self, *args):
        """stub
        """
        print('called MainGui.set_page_title() with args', args)
    def set_tabfocus(self, number):
        """stub
        """
        print(f'called MainGui.set_tabfocus({number})')
    def set_statusmessage(self, msg):
        """stub
        """
        print(f'called MainGui.set_statusmessage(`{msg}`)')
    def show_username(self, msg):
        """stub
        """
        print(f'called MainGui.show_username(`{msg}`)')
    def get_bookwidget(self):
        """stub
        """
        print('called MainGui.get_bookwidget()')
        return MockBook()
    def add_book_tab(self, *args):
        """stub
        """
        print('called MainGui.add_book_tab with args', args)
    def refresh_page(self):
        """stub
        """
        print('called MainGui.refresh_page()')
    def preview(self):
        """stub
        """
        print('called MainGui.preview()')
    def exit(self):
        """stub
        """
        print('called MainGui.exit()')


class MockPage:
    """stub for Page object
    """
    def __init__(self, *args, **kwargs):
        print('called Page.__init__() with args', args, kwargs)
        self.gui = MockPageGui()


class MockPageGui:
    """stub for gui.PageGui object
    """
    def __init__(self, *args, **kwargs):
        print('called PageGui.__init__() with args', args, kwargs)
        self.cat_choice = 'cat'
        self.stat_choice = 'stat'
    def enable_buttons(self, *args):
        """stub
        """
        print('called PageGui.enable_buttons() with args', args)
    def enable_fields(self, *args):
        """stub
        """
        print('called PageGui.enable_fields() with args', args)
    def enable_sorting(self, value):
        """stub
        """
        print(f'called PageGui.enable_sorting({value})')
    def init_fields(self, *args):
        """stub
        """
        print('called PageGui.init_fields()')
    def set_textarea_contents(self, text):
        """stub
        """
        print(f'call PageGui.set_textarea_contents({text})')
    def set_text_readonly(self, value):
        """stub
        """
        print(f'call PageGui.set_text_readonly({value})')
    def enable_toolbar(self, user):
        """stub
        """
        print(f'call PageGui.enable_toolbar({user})')
    def get_textarea_contents(self):
        """stub
        """
        print('call PageGui.get_textarea_contents()')
        return 'text'
    def move_cursor_to_end(self):
        """stub
        """
        print('call PageGui.move_cursor_to_end()')
    def set_focus(self):
        """stub
        """
        print('called PageGui.set_focus()')
    def build_newbuf(self):
        """stub
        """
        print('called PageGui.build_newbuf()')
        return 'newbuf'
    def can_saveandgo(self):
        """stub
        """
    def set_selection(self):
        """stub
        """
        print('called PageGui.set_selection()')
    def get_selected_action(self):
        """stub
        """
        print('called PageGui.get_selected_action()')
        return '1'
    def set_archive_button_text(self, text):
        """stub
        """
        print(f'called PageGui.set_archive_button_text(`{text}`)')
    def ensure_visible(self, item):
        """stub
        """
        print(f'called PageGui.ensure_visible(`{item}`)')
    def get_items(self):
        """stub
        """
        print('called PageGui.get_items()')
        return ['all', 'the', 'items']
    def get_item_text(self, *args):
        """stub
        """
        print(f'called PageGui.get_item_text() with args {args}')
        return 'the text of the item'
    def set_item_text(self, *args):
        """stub
        """
        print('called PageGui.set_item_text() with args', args)
    def get_text(self, *args):
        """stub
        """
        print(f'called PageGui.get_field_text() with args {args}')
        return 'the text of the item'
    def get_field_text(self, *args):
        """stub
        """
        print(f'called PageGui.get_field_text() with args {args}')
        return 'the text of the item'
    def init_textfield(self):
        """stub
        """
        print('called PageGui.init_textfield()')
    def clear_list(self):
        """stub
        """
        print('called PageGui.clear_list()')
    def add_listitem(self, item):
        """stub
        """
        print(f'called PageGui.add_listitem(`{item}`)')
    def set_listitem_values(self, *args):
        """stub
        """
        print('called PageGui.set_listitem_values() with args', args)
    def clear_textfield(self):
        """stub
        """
        print('called PageGui.clear_textfield()')
    def clear_stats(self):
        """stub
        """
        print('called PageGui.clear_stats()')
    def add_stat_choice(self, *args):
        """stub
        """
        print(f'called PageGui.add_stat_choice() using args {args}')
    def clear_cats(self):
        """stub
        """
        print('called PageGui.clear_cats()')
    def add_cat_choice(self, *args):
        """stub
        """
        print(f'called PageGui.add_cat_choice() using args {args}')
    def get_choice_data(self, *args):
        """stub
        """
        print(f'called PageGui.get_choice_data() using args {args}')
    def get_list_row(self):
        """stub
        """
    def get_list_rowcount(self):
        """stub
        """
    def set_list_row(self, row):
        """stub
        """
        print(f'called PageGui.set_list_row({row})')
    def get_textfield_contents(self):
        """stub
        """
        print('called PageGui.get_textfield_contents()')
        return 'text'
    def convert_text(self, in_, to='plain'):
        """stub
        """
        print(f'called PageGui.convert_text() with args `{in_}`, to=`{to}`')
        return in_
    def get_listitem_text(self, in_):
        """stub
        """
        print('called PageGui.get_listitem_text()')
        return in_
    def set_listitem_text(self, item, in_):
        """stub
        """
        print(f'called PageGui.set_listitem_text() with args `{item}` `{in_}`')
    def set_listitem_data(self, item):
        """stub
        """
        print(f'called PageGui.set_listitem_data() with args `{item}`')
    def add_new_item_to_list(self, *args):
        """stub
        """
        print('called PageGui.add_new_item_to_list() with args', args)
    def init_list(self, text):
        """stub
        """
        print(f'called PageGui.init_list() with text `{text}`')
    def add_item_to_list(self, index, text):
        """stub
        """
        print(f'called PageGui.add_item_to_list() with args `{index}` `{text}`')
    def set_list_callback(self):
        """stub
        """
        print('called PageGui.init_set_list_callback()')
    def set_oldbuf(self):
        """stub
        """
        return 'oldbuf'
    def set_text(self, fieldname, text):
        """stub
        """
        print(f'called PageGui.set_text() for field `{fieldname}` text `{text}`')
    def set_choice(self, *args):
        """stub
        """
        print('called PageGui.set_choice() with args', args)
    def get_item_by_id(self, *args):
        """stub
        """
        print('called PageGui.get_item_by_id() with args', args)
        return 'item_by_id'
    def get_first_item(self, *args):
        """stub
        """
        print('called PageGui.get_first_item() with args', args)
        return 'first_item'


class MockActie:
    """stub for dml#.Actie object
    """
    def __init__(self, *args):
        self.id = 'xx'
        self.titel = "titel"
        self.over = 'over'
        self.arch = True
        self.melding = 'mld'
        self.oorzaak = 'ozk'
        self.oplossing = 'opl'
        self.vervolg = 'vv'
    def add_event(self, *args):
        print('called Actie.add_event() with args', args)
    def cleanup(self):
        print('called Actie.cleanup()')
    def write(self, *args):
        print('called Actie.write() with args', args)
    def read(self, *args):
        print('called Actie.read()')
    def get_soorttext(self):
        return 'soorttext'
    def get_statustext(self):
        return 'statustext'


class MockSortOpts:
    """stub for SortOptions object as used by Django/SQL data backend
    """
    def __init__(self, *args):
        print('called dmls.SortOptions() with args', args)


def test_main(monkeypatch, capsys):
    """unittest for main entry point
    """
    monkeypatch.setattr(testee, 'MainWindow', MockMainWindow)
    testee.main()
    assert capsys.readouterr().out == ('called MainWindow.__init__() with args (None, None)\n'
                                       'called MainGui.__init__()\n'
                                       'called MainGui.go()\n')
    testee.main('filenaam')
    assert capsys.readouterr().out == ("called MainWindow.__init__() with args (None, 'filenaam')\n"
                                       'called MainGui.__init__()\n'
                                       'called MainGui.go()\n')


def test_page_init(monkeypatch, capsys):
    """unittest for main.Page.init
    """
    appbase = MockMainWindow()
    parent = MockBook()
    parent.parent = appbase
    assert capsys.readouterr().out == ('called MainWindow.__init__() with args ()\n'
                                       'called MainGui.__init__()\n')
    monkeypatch.setattr(testee.gui, 'PageGui', MockPageGui)
    testobj = testee.Page(parent, 'pageno')
    assert testobj.parent == parent
    assert testobj.appbase == appbase
    assert testobj.pageno == 'pageno'
    assert testobj.is_text_page
    assert hasattr(testobj, 'gui')
    assert capsys.readouterr().out == (f"called PageGui.__init__() with args ({parent}, {testobj})"
                                       " {}\n")

    testobj = testee.Page(parent, 'pageno', standard=False)
    assert testobj.parent == parent
    assert testobj.pageno == 'pageno'
    assert not testobj.is_text_page
    assert not hasattr(testobj, 'gui')
    assert capsys.readouterr().out == ''


def setup_page(monkeypatch, capsys):
    def mock_init_page(self):
        print('called Page.__init__()')
    monkeypatch.setattr(testee.Page, '__init__', mock_init_page)
    testobj = testee.Page()
    testobj.parent = types.SimpleNamespace(tabs={0: "0 start", 1: "1 vervolg", 2: "rest"},
                                           pagedata=MockActie(), count=lambda *x: 3,
                                           fnaam='testfile')
    testobj.appbase = MockMainWindow()
    testobj.gui = MockPageGui()
    assert capsys.readouterr().out == ("called Page.__init__()\n"
                                       "called MainWindow.__init__() with args ()\n"
                                       "called MainGui.__init__()\n"
                                       'called PageGui.__init__() with args () {}\n')
    return testobj


def test_page_get_toolbar_data(monkeypatch, capsys):
    """unittest for main.Page.get_toolbar_data
    """
    testobj = setup_page(monkeypatch, capsys)
    assert testobj.get_toolbar_data(types.SimpleNamespace(text_bold='B', update_bold='UB',
        text_italic='I', update_italic='UI', text_underline='U', update_underline='UU',
        text_strikethrough='S', enlarge_text='ET', shrink_text='ST', case_lower='LC',
        case_upper='UC', indent_more='IM', indent_less='IL', increase_paragraph_spacing='IPS',
        decrease_paragraph_spacing='DPS')) == (
                ('&Bold', 'Ctrl+B', 'icons/sc_bold', 'Toggle Bold', 'B', 'UB'),
                ('&Italic', 'Ctrl+I', 'icons/sc_italic', 'Toggle Italic', 'I', 'UI'),
                ('&Underline', 'Ctrl+U', 'icons/sc_underline', 'Toggle Underline', 'U', 'UU'),
                ('Strike&through', 'Ctrl+~', 'icons/sc_strikethrough', 'Toggle Strikethrough', 'S'),
                (),
                ("&Enlarge text", 'Ctrl+Up', 'icons/sc_grow', 'Use bigger letters', 'ET'),
                ("&Shrink text", 'Ctrl+Down', 'icons/sc_shrink', 'Use smaller letters', 'ST'),
                (),
                ('To &Lower Case', 'Shift+Ctrl+L', 'icons/sc_changecasetolower',
                 'Use lower case letters', 'LC'),
                ('To &Upper Case', 'Shift+Ctrl+U', 'icons/sc_changecasetoupper',
                 'Use upper case letters', 'UC'),
                (),
                ("Indent &More", 'Ctrl+]', 'icons/sc_incrementindent', 'Increase indentation', 'IM'),
                ("Indent &Less", 'Ctrl+[', 'icons/sc_decrementindent', 'Decrease indentation', 'IL'),
                (),
                ("Increase Paragraph &Spacing", '', 'icons/sc_paraspaceincrease',
                 'Increase spacing between paragraphs', 'IPS'),
                ("Decrease &Paragraph Spacing", '', 'icons/sc_paraspacedecrease',
                 'Decrease spacing between paragraphs', 'DPS'))
    assert capsys.readouterr().out == ""


def test_page_vulp(monkeypatch, capsys):
    """unittest for main.Page.vulp
    """
    def mock_enable_buttons(self, state):
        """stub
        """
        print(f'call Page.enable_buttons({state})')
    def mock_get_pagetext(self):
        """stub
        """
        print('call Page.get_pagetext()')
        return 'pagetext'
    monkeypatch.setattr(testee.Page, 'enable_buttons', mock_enable_buttons)
    monkeypatch.setattr(testee.Page, 'get_pagetext', mock_get_pagetext)
    testobj = setup_page(monkeypatch, capsys)
    testobj.seltitel = 'hallo'
    testobj.appbase.is_user = True
    testobj.appbase.title = 'aha'
    testobj.parent.current_tab = 0
    testobj.vulp()
    assert capsys.readouterr().out == ('call MainWindow.set_windowtitle(aha | hallo)\n'
                                       'call MainWindow.set_statusmessage()\n')
    testobj = setup_page(monkeypatch, capsys)
    testobj.seltitel = 'hallo'
    testobj.appbase.is_user = True
    testobj.appbase.title = 'aha'
    testobj.parent.current_tab = 1
    testobj.parent.newitem = True
    testobj.appbase.use_separate_subject = False
    testobj.vulp()
    assert capsys.readouterr().out == ('call Page.enable_buttons(True)\n'
                                       'call MainWindow.set_windowtitle(aha | xx titel)\n'
                                       'call MainWindow.set_statusmessage()\n')
    testobj = setup_page(monkeypatch, capsys)
    testobj.seltitel = 'hallo'
    testobj.appbase.is_user = True
    testobj.appbase.title = 'aha'
    testobj.parent.current_tab = 1
    testobj.parent.newitem = False
    testobj.appbase.use_separate_subject = False
    testobj.vulp()
    assert capsys.readouterr().out == ('call Page.enable_buttons(False)\n'
                                       'call MainWindow.set_windowtitle(aha | xx titel)\n'
                                       'call MainWindow.set_statusmessage()\n')
    testobj = setup_page(monkeypatch, capsys)
    testobj.parent.count = lambda *x: 6
    testobj.parent.pagedata.arch = False
    testobj.seltitel = 'hallo'
    testobj.appbase.title = 'aha'
    testobj.appbase.is_user = False
    testobj.parent.current_tab = 2
    testobj.parent.newitem = False
    testobj.appbase.use_separate_subject = False
    testobj.vulp()
    assert capsys.readouterr().out == ('call Page.enable_buttons(False)\n'
                                       'call MainWindow.set_windowtitle(aha | xx titel)\n'
                                       'call MainWindow.set_statusmessage()\n'
                                       "call Page.get_pagetext()\n"
                                       'call PageGui.set_textarea_contents(pagetext)\n'
                                       'call PageGui.set_text_readonly(True)\n'
                                       'call PageGui.enable_toolbar(False)\n'
                                       'call PageGui.get_textarea_contents()\n'
                                       'call PageGui.move_cursor_to_end()\n')
    # pagedata = types.SimpleNamespace(id='xx', titel="titel", over='over', arch=True)
    # mock_book = types.SimpleNamespace(parent=MockMainWindow(),
    #                                   tabs={0: "0 start", 1: "1 vervolg", 2: "rest"},
    #                                   pagedata=pagedata, count=lambda *x: 6)
    # assert capsys.readouterr().out == 'called MainWindow.__init__()\n'
    testobj = setup_page(monkeypatch, capsys)
    testobj.seltitel = 'hallo'
    monkeypatch.setattr(testobj.parent, 'count', lambda *x: 3)
    testobj.appbase.title = ''
    testobj.appbase.is_user = True
    testobj.parent.current_tab = 2
    testobj.parent.newitem = False
    testobj.appbase.use_separate_subject = True
    testobj.vulp()
    assert capsys.readouterr().out == ('call Page.enable_buttons(False)\n'
                                       'call MainWindow.set_windowtitle(xx over - titel)\n'
                                       'call MainWindow.set_statusmessage()\n')


def test_page_get_pagetext(monkeypatch, capsys):
    """unittest for main.Page.get_pagetext
    """
    testobj = setup_page(monkeypatch, capsys)
    testobj.parent.current_tab = 2
    assert testobj.get_pagetext() == 'mld'
    testobj.parent.current_tab = 3
    assert testobj.get_pagetext() == 'ozk'
    testobj.parent.current_tab = 4
    assert testobj.get_pagetext() == 'opl'
    testobj.parent.current_tab = 5
    assert testobj.get_pagetext() == 'vv'


def test_page_readp(monkeypatch, capsys):
    """unittest for main.Page.readp
    """
    class MockActie2:
        """stub, nog uitzoeken hoe dit gecombineerd kan worden met de andere MockActie
        """
        def __init__(self, *args):
            print('called Actie.__init__() with args', args)
            self.id = '1'
            self.imagelist = ['1', '2']
    testobj = setup_page(monkeypatch, capsys)
    monkeypatch.setattr(testee.shared, 'Actie', {'X': MockActie2})
    testobj.parent.fnaam = 'fnaam'
    testobj.appbase.datatype = 'X'
    testobj.appbase.user = 'user1'
    testobj.readp('15')
    assert testobj.appbase.imagelist == ['1', '2']
    assert testobj.parent.old_id == '1'
    assert not testobj.parent.newitem
    assert capsys.readouterr().out == ('called Actie.cleanup()\n'
                                       "called Actie.__init__() with args ('fnaam', '15', 'user1')\n")


def test_page_nieuwp(monkeypatch, capsys):
    """unittest for main.Page.nieuwp
    """
    class MockActieN:
        """stub for dml.Actie
        """
        def __init__(self, *args):
            print('called Actie.__init__() with args', args)
            self.id = '1'
            self.imagelist = ['1', '2']
        def add_event(self, *args):
            print('called Actie.add_event() with args', args)
    def mock_vulp(self):
        """stub
        """
        print('called Page.vulp()')
    def mock_goto_page(self, *args, **kwargs):
        """stub
        """
        print('called Page.goto_page() with args', args, kwargs)
    monkeypatch.setattr(testee.Page, 'vulp', mock_vulp)
    monkeypatch.setattr(testee.Page, 'goto_page', mock_goto_page)
    testobj = setup_page(monkeypatch, capsys)
    monkeypatch.setattr(testee.shared, 'Actie', {'X': MockActieN})
    testobj.parent.fnaam = 'fnaam'
    testobj.appbase.datatype = 'X'
    testobj.appbase.user = 'user1'
    monkeypatch.setattr(testobj, 'leavep', lambda *x: False)
    testobj.nieuwp()
    assert not testobj.parent.newitem
    assert capsys.readouterr().out == ''

    monkeypatch.setattr(testobj, 'leavep', lambda *x: True)
    testobj.parent.current_tab = 0
    testobj.nieuwp()
    assert testobj.parent.newitem
    assert capsys.readouterr().out == ("called MainGui.enable_book_tabs() with args (True,)"
                                       " {'tabfrom': 1}\n"
                                       "called Actie.__init__() with args ('fnaam', 0, 'user1')\n"
                                       "called Actie.add_event() with args ('Actie opgevoerd',)\n"
                                       "called Page.goto_page() with args (1,) {'check': False}\n")

    testobj.parent.current_tab = 1
    testobj.nieuwp()
    assert testobj.parent.newitem
    assert capsys.readouterr().out == ("called Actie.__init__() with args ('fnaam', 0, 'user1')\n"
                                       "called Actie.add_event() with args ('Actie opgevoerd',)\n"
                                       "called Page.vulp()\ncalled PageGui.set_focus()\n")


def test_page_leavep(monkeypatch, capsys):
    """unittest for main.Page.leavep
    """
    def mock_show_message(cls, msg, title):
        """stub
        """
        print(f'called gui.show_message with args `{title}` `{msg}`')
    def mock_ask_question(cls, msg):
        """stub
        """
        print(f'called gui.ask_cancel_question with arg `{msg}`')
        return True, False
    def mock_ask_question_no(cls, msg):
        """stub
        """
        print(f'called gui.ask_cancel_question with arg `{msg}`')
        return False, False
    def mock_ask_question_cancel(cls, msg):
        """stub
        """
        print(f'called gui.ask_cancel_question with arg `{msg}`')
        return False, True
    monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
    testobj = setup_page(monkeypatch, capsys)
    testobj.parent.current_tab = 0
    testobj.appbase.exiting = True
    assert testobj.leavep()
    testobj.appbase.exiting = False
    testobj.parent.fnaam = ''
    testobj.appbase.multiple_files = True
    assert not testobj.leavep()
    assert capsys.readouterr().out == ('called gui.show_message with args `Navigatie niet toegestaan`'
                                       ' `Kies eerst een bestand om mee te werken`\n')
    testobj.appbase.multiple_files = False
    testobj.appbase.multiple_projects = True
    assert not testobj.leavep()
    assert capsys.readouterr().out == ('called gui.show_message with args `Navigatie niet toegestaan`'
                                       ' `Kies eerst een project om mee te werken`\n')
    testobj.parent.fnaam = 'something'
    testobj.parent.data = {}
    testobj.parent.newitem = False
    assert not testobj.leavep()
    assert capsys.readouterr().out == ('called gui.show_message with args `Navigatie niet toegestaan`'
                                       ' `Voer eerst één of meer acties op`\n')
    testobj.parent.data = 'anything'
    testobj.parent.current_item = -1
    assert not testobj.leavep()
    assert capsys.readouterr().out == ('called gui.show_message with args `Navigatie niet toegestaan`'
                                       ' `Selecteer eerst een actie`\n')
    testobj.parent.current_item = 1
    assert testobj.leavep()
    assert capsys.readouterr().out == ''

    testobj.parent.current_tab = 1
    testobj.oldbuf = ['x']
    testobj.parent.changed_item = False
    assert testobj.leavep()
    assert capsys.readouterr().out == ''

    testobj.parent.changed_item = True
    monkeypatch.setattr(testee.gui, 'ask_cancel_question', mock_ask_question)
    monkeypatch.setattr(testobj, 'savep', lambda *x: True)
    assert testobj.leavep()
    assert capsys.readouterr().out == ('called gui.ask_cancel_question with arg '
                                       '`De gegevens op de pagina zijn gewijzigd,\n'
                                       'wilt u de wijzigingen opslaan voordat u verder gaat?`\n'
                                       'called MainGui.enable_all_other_tabs() with arg `True`\n')

    monkeypatch.setattr(testee.gui, 'ask_cancel_question', mock_ask_question_no)
    assert testobj.leavep()
    assert capsys.readouterr().out == ('called gui.ask_cancel_question with arg '
                                       '`De gegevens op de pagina zijn gewijzigd,\n'
                                       'wilt u de wijzigingen opslaan voordat u verder gaat?`\n'
                                       'called MainGui.enable_all_other_tabs() with arg `True`\n')

    monkeypatch.setattr(testee.gui, 'ask_cancel_question', mock_ask_question_cancel)
    assert not testobj.leavep()
    assert capsys.readouterr().out == ('called gui.ask_cancel_question with arg '
                                       '`De gegevens op de pagina zijn gewijzigd,\n'
                                       'wilt u de wijzigingen opslaan voordat u verder gaat?`\n')


def test_page_savep(monkeypatch, capsys):
    """unittest for main.Page.savep
    """
    def mock_enable_buttons(self, value):
        """stub
        """
        print(f'called Page.enable_buttons({value})')
    def mock_update_actie(self):
        """stub
        """
        print('called Page.update_actie()')
    monkeypatch.setattr(testee.Page, 'enable_buttons', mock_enable_buttons)
    monkeypatch.setattr(testee.Page, 'update_actie', mock_update_actie)
    testobj = setup_page(monkeypatch, capsys)
    testobj.gui.can_save = False
    assert not testobj.savep()
    assert capsys.readouterr().out == ''

    testobj.gui.can_save = True
    testobj.parent.current_tab = 0
    assert not testobj.savep()
    assert capsys.readouterr().out == 'called Page.enable_buttons(False)\n'

    testobj.parent.current_tab = 1
    assert not testobj.savep()
    assert capsys.readouterr().out == 'called Page.enable_buttons(False)\n'

    testobj.parent.current_tab = 6
    assert not testobj.savep()
    assert capsys.readouterr().out == 'called Page.enable_buttons(False)\n'

    testobj.parent.current_tab = 2
    testobj.appbase.use_text_panels = False
    assert not testobj.savep()
    assert capsys.readouterr().out == 'called Page.enable_buttons(False)\n'

    testobj.appbase.use_text_panels = True
    testobj.oldbuf = ''
    monkeypatch.setattr(testobj.gui, 'get_textarea_contents',
                        lambda *x: testobj.parent.pagedata.melding)
    assert testobj.savep()   # niet saven, wel true?
    assert testobj.oldbuf == ''
    assert capsys.readouterr().out == 'called Page.enable_buttons(False)\n'
    monkeypatch.setattr(testobj.gui, 'get_textarea_contents', lambda *x: 'new text')
    assert testobj.savep()
    assert testobj.oldbuf == 'new text'
    assert capsys.readouterr().out == ('called Page.enable_buttons(False)\n'
                                       "called Actie.add_event() with"
                                       " args ('Meldingtekst aangepast',)\n"
                                       'called Page.update_actie()\n')

    testobj.parent.current_tab = 3
    testobj.oldbuf = ''
    monkeypatch.setattr(testobj.gui, 'get_textarea_contents',
                        lambda *x: testobj.parent.pagedata.oorzaak)
    assert testobj.savep()   # niet saven, wel true?
    assert testobj.oldbuf == ''
    assert capsys.readouterr().out == 'called Page.enable_buttons(False)\n'
    monkeypatch.setattr(testobj.gui, 'get_textarea_contents', lambda *x: 'new text')
    assert testobj.savep()
    assert testobj.oldbuf == 'new text'
    assert capsys.readouterr().out == ('called Page.enable_buttons(False)\n'
                                       "called Actie.add_event() with"
                                       " args ('Beschrijving oorzaak aangepast',)\n"
                                       'called Page.update_actie()\n')

    testobj.parent.current_tab = 4
    testobj.oldbuf = ''
    monkeypatch.setattr(testobj.gui, 'get_textarea_contents',
                        lambda *x: testobj.parent.pagedata.oplossing)
    assert testobj.savep()   # niet saven, wel true?
    assert testobj.oldbuf == ''
    assert capsys.readouterr().out == 'called Page.enable_buttons(False)\n'
    monkeypatch.setattr(testobj.gui, 'get_textarea_contents', lambda *x: 'new text')
    assert testobj.savep()
    assert testobj.oldbuf == 'new text'
    assert capsys.readouterr().out == ('called Page.enable_buttons(False)\n'
                                       "called Actie.add_event() with"
                                       " args ('Beschrijving oplossing aangepast',)\n"
                                       'called Page.update_actie()\n')

    testobj.parent.current_tab = 5
    testobj.oldbuf = ''
    monkeypatch.setattr(testobj.gui, 'get_textarea_contents',
                        lambda *x: testobj.parent.pagedata.vervolg)
    assert testobj.savep()   # niet saven, wel true?
    assert testobj.oldbuf == ''
    assert capsys.readouterr().out == 'called Page.enable_buttons(False)\n'
    monkeypatch.setattr(testobj.gui, 'get_textarea_contents', lambda *x: 'new text')
    assert testobj.savep()
    assert testobj.oldbuf == 'new text'
    assert capsys.readouterr().out == ('called Page.enable_buttons(False)\n'
                                       "called Actie.add_event() with"
                                       " args ('Tekst vervolgactie aangepast',)\n"
                                       'called Page.update_actie()\n')


def test_page_savepgo(monkeypatch, capsys):
    """unittest for main.Page.savepgo
    """
    class MockActie:
        """stub
        """
    def mock_savep(self):
        """stub
        """
        print('called Page.savep()')
        return True
    def mock_goto_next(self):
        """stub
        """
        print('called Page.goto_next()')
    def mock_enable_buttons(self, value=False):
        """stub
        """
        print(f'called Page.enable_buttons({value})')
    monkeypatch.setattr(testee.Page, 'enable_buttons', mock_enable_buttons)
    monkeypatch.setattr(testee.Page, 'savep', mock_savep)
    monkeypatch.setattr(testee.Page, 'goto_next', mock_goto_next)
    testobj = setup_page(monkeypatch, capsys)
    monkeypatch.setattr(testobj.gui, 'can_saveandgo', lambda *x: False)
    testobj.savepgo()
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(testobj.gui, 'can_saveandgo', lambda *x: True)
    testobj.savepgo()
    assert capsys.readouterr().out == ('called Page.savep()\n'
                                       'called Page.goto_next()\n')
    monkeypatch.setattr(testobj, 'savep', lambda *x: False)
    testobj.savepgo()
    assert capsys.readouterr().out == 'called Page.enable_buttons(False)\n'


def test_page_restorep(monkeypatch, capsys):
    """unittest for main.Page.restorep
    """
    def mock_reset_font(*args):
        """stub
        """
        print('called PageGui.reset_font()')
    def mock_vulp(*args):
        """stub
        """
        print('called Page.vulp()')
    monkeypatch.setattr(testee.Page, 'vulp', mock_vulp)
    testobj = setup_page(monkeypatch, capsys)
    testobj.gui.reset_font = mock_reset_font
    testobj.appbase.use_rt = True
    testobj.parent.pagedata.status = '1'
    testobj.parent.current_tab = 1
    testobj.restorep()
    assert testobj.parent.pagedata.status == '1'
    assert capsys.readouterr().out == 'called Page.vulp()\n'
    testobj.parent.current_tab = 2
    testobj.status_auto_changed = False
    testobj.restorep()
    assert testobj.parent.pagedata.status == '1'
    assert capsys.readouterr().out == 'called PageGui.reset_font()\ncalled Page.vulp()\n'
    testobj.appbase.use_rt = False
    testobj.restorep()
    assert testobj.parent.pagedata.status == '1'
    assert capsys.readouterr().out == 'called Page.vulp()\n'
    testobj.status_auto_changed = True
    testobj.parent.current_tab = 1
    testobj.restorep()
    assert testobj.parent.pagedata.status == '1'
    assert capsys.readouterr().out == 'called Page.vulp()\n'
    testobj.parent.current_tab = 2
    testobj.restorep()
    assert testobj.parent.pagedata.status == '0'
    assert capsys.readouterr().out == 'called Page.vulp()\n'


def test_page_on_text(monkeypatch, capsys):
    """unittest for main.Page.on_text
    """
    def mock_enable_buttons(self, value=False):
        """stub
        """
        print(f'called Page.enable_buttons({value})')
    class MockActie:
        """stub
        """
    monkeypatch.setattr(testee.Page, 'enable_buttons', mock_enable_buttons)
    testobj = setup_page(monkeypatch, capsys)
    testobj.initializing = True
    testobj.on_text()
    assert capsys.readouterr().out == ''
    testobj.initializing = False
    testobj.oldbuf = 'oldbuf'
    testobj.on_text()
    assert capsys.readouterr().out == ('called PageGui.build_newbuf()\n'
                                       'called Page.enable_buttons(True)\n')
    testobj.oldbuf = 'newbuf'
    testobj.on_text()
    assert capsys.readouterr().out == ('called PageGui.build_newbuf()\n'
                                       'called Page.enable_buttons(False)\n')


def test_page_update_actie(monkeypatch, capsys):
    """unittest for main.Page.update_actie
    """
    class MockPageGui:
        """stub
        """
        def __init__(self, pageno):
            self.pageno = pageno
        def get_text(self, *args):
            """stub
            """
            print(f'called Page{self.pageno}Gui.get_text() with args', args)
            return args[0]
        def get_choice_data(self, *args):
            """stub
            """
            print(f'called Page{self.pageno}Gui.get_choice_data() with args', args)
            return args[0]
        def set_item_text(self, *args):
            """stub
            """
            print(f'called Page{self.pageno}Gui.set_item_text() with args', args)
        def add_listitem(self, *args):
            """stub
            """
            print(f'called Page{self.pageno}Gui.add_listitem() with args', args)
            return 'new listitem'
        def set_selection(self, *args):
            """stub
            """
            print(f'called Page{self.pageno}Gui.set_selection() with args', args)
        def get_selection(self):
            """stub
            """
            print(f'called Page{self.pageno}Gui.get_selection()')
            return 'selection'
    class MockPage0:
        """stub
        """
        def __init__(self):
            self.gui = MockPageGui(0)
    class MockPage1:
        """stub
        """
        def __init__(self):
            self.gui = MockPageGui(1)
    testobj = setup_page(monkeypatch, capsys)

    image_count = 9
    testobj.appbase.imagecount = image_count
    testobj.appbase.imagelist = ['image', 'list']
    testobj.parent.pagedata.id = 1
    testobj.parent.pagedata.status = '0'
    testobj.parent.pagedata.updated = 'now'
    testobj.parent.pagedata.over = 'about'
    testobj.parent.pagedata.titel = 'title'
    testobj.parent.stats = {0: ('Started', '0'), 1: ('Accepted', '1')}
    testobj.appbase.use_text_panels = False
    testobj.parent.current_tab = 0
    testobj.appbase.work_with_user = False
    testobj.parent.newitem = True
    testobj.parent.data = {}
    testobj.parent.pages = [MockPage0(), MockPage1()]

    testobj.update_actie()
    assert testobj.parent.pagedata.imagecount == image_count
    assert testobj.parent.pagedata.imagelist == ['image', 'list']
    assert testobj.parent.data == {0: ('date', 'proc - desc', 's', 'c', 'id')}
    assert testobj.parent.current_item == 'new listitem'
    assert not testobj.parent.newitem
    assert testobj.parent.rereadlist
    assert capsys.readouterr().out == ('called Actie.write() with args ()\n'
                                       'called Actie.read()\n'
                                       "called Page1Gui.get_text() with args ('date',)\n"
                                       "called Page1Gui.get_text() with args ('proc',)\n"
                                       "called Page1Gui.get_text() with args ('desc',)\n"
                                       "called Page1Gui.get_choice_data() with args ('stat',)\n"
                                       "called Page1Gui.get_choice_data() with args ('cat',)\n"
                                       "called Page1Gui.get_text() with args ('id',)\n"
                                       "called Page0Gui.add_listitem() with args ('date',)\n"
                                       'called Page0Gui.set_selection() with args ()\n')

    testobj.appbase.imagecount = image_count
    testobj.appbase.imagelist = ['image', 'list']
    testobj.parent.pagedata.status = '1'
    testobj.appbase.use_text_panels = True
    testobj.parent.current_tab = 2
    testobj.appbase.work_with_user = True
    testobj.appbase.user = 'my_user'
    testobj.parent.newitem = False
    testobj.appbase.use_separate_subject = False

    testobj.update_actie()
    assert testobj.parent.pagedata.imagecount == image_count
    assert testobj.parent.pagedata.imagelist == ['image', 'list']
    assert capsys.readouterr().out == (
                        "called Actie.write() with args ('my_user',)\n"
                        "called Actie.read()\n"
                        "called Page0Gui.get_selection()\n"
                        "called Page0Gui.set_item_text() with args ('selection', 1, 'S')\n"
                        "called Page0Gui.set_item_text() with args ('selection', 2, 'statustext')\n"
                        "called Page0Gui.set_item_text() with args ('selection', 3, 'now')\n"
                        "called Page0Gui.set_item_text() with args ('selection', 4, 'title')\n")

    testobj.appbase.imagecount = image_count
    testobj.appbase.imagelist = ['image', 'list']
    testobj.parent.pagedata.status = '0'
    testobj.appbase.use_text_panels = True
    testobj.parent.current_tab = 3
    testobj.appbase.work_with_user = True
    testobj.appbase.user = 'my_user'
    testobj.parent.newitem = False
    testobj.appbase.use_separate_subject = True

    testobj.update_actie()
    assert testobj.parent.pagedata.imagecount == image_count
    assert testobj.parent.pagedata.imagelist == ['image', 'list']
    assert capsys.readouterr().out == (
                        'called Actie.add_event() with args (\'Status gewijzigd in "Accepted"\',)\n'
                        "called Actie.write() with args ('my_user',)\n"
                        "called Actie.read()\n"
                        "called Page0Gui.get_selection()\n"
                        "called Page0Gui.set_item_text() with args ('selection', 1, 'S')\n"
                        "called Page0Gui.set_item_text() with args ('selection', 2, 'statustext')\n"
                        "called Page0Gui.set_item_text() with args ('selection', 3, 'now')\n"
                        "called Page0Gui.set_item_text() with args ('selection', 4, 'about')\n"
                        "called Page0Gui.set_item_text() with args ('selection', 5, 'title')\n")


def test_page_enable_buttons(monkeypatch, capsys):
    """unittest for main.Page.enable_buttons
    """
    class MockActie:
        """stub
        """
    testobj = setup_page(monkeypatch, capsys)
    testobj.parent.current_tab = 0
    testobj.enable_buttons(True)
    assert testobj.parent.changed_item
    assert capsys.readouterr().out == 'called PageGui.enable_buttons() with args (True,)\n'
    testobj.parent.current_tab = 1
    testobj.enable_buttons(False)
    assert not testobj.parent.changed_item
    assert capsys.readouterr().out == ('called PageGui.enable_buttons() with args (False,)\n'
                                       'called MainGui.enable_all_other_tabs() with arg `True`\n')


def test_page_goto_actie(monkeypatch, capsys):
    """unittest for main.Page.goto_actie
    """
    def mock_goto_page(self, value=False):
        """stub
        """
        print(f'called Page.goto_page({value})')
    class MockActie:
        """stub
        """
    monkeypatch.setattr(testee.Page, 'goto_page', mock_goto_page)
    testobj = setup_page(monkeypatch, capsys)
    testobj.goto_actie()
    assert capsys.readouterr().out == ('called Page.goto_page(1)\n')


def test_page_goto_next(monkeypatch, capsys):
    """unittest for main.Page.goto_next
    """
    class MockActie:
        """stub
        """
    testobj = setup_page(monkeypatch, capsys)
    testobj.parent.current_tab = 2
    testobj.parent.pages = [0, 1, 2]
    monkeypatch.setattr(testobj, 'leavep', lambda *x: False)
    testobj.goto_next()
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(testobj, 'leavep', lambda *x: True)
    testobj.goto_next()
    assert capsys.readouterr().out == 'called MainGui.set_page(0)\n'
    testobj.parent.current_tab = 0
    testobj.goto_next()
    assert capsys.readouterr().out == 'called MainGui.set_page(1)\n'


def test_page_goto_prev(monkeypatch, capsys):
    """unittest for main.Page.goto_prev
    """
    class MockActie:
        """stub
        """
    testobj = setup_page(monkeypatch, capsys)
    testobj.parent.current_tab = 2
    testobj.parent.pages = [0, 1, 2]
    monkeypatch.setattr(testobj, 'leavep', lambda *x: False)
    testobj.goto_prev()
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(testobj, 'leavep', lambda *x: True)
    testobj.goto_prev()
    assert capsys.readouterr().out == 'called MainGui.set_page(1)\n'
    testobj.parent.current_tab = 0
    testobj.goto_prev()
    assert capsys.readouterr().out == 'called MainGui.set_page(2)\n'


def test_goto_page(monkeypatch, capsys):
    """unittest for main.Page.goto_page
    """
    class MockActie:
        """stub
        """
    testobj = setup_page(monkeypatch, capsys)
    testobj.parent.pages = [0, 1, 2]
    testobj.goto_page(1, check=False)
    assert capsys.readouterr().out == 'called MainGui.set_page(1)\n'
    monkeypatch.setattr(testobj, 'leavep', lambda *x: False)
    testobj.goto_page(1)
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(testobj, 'leavep', lambda *x: True)
    testobj.goto_page(1)
    assert capsys.readouterr().out == 'called MainGui.set_page(1)\n'
    testobj.goto_page(-1)
    assert capsys.readouterr().out == ''
    testobj.goto_page(3)
    assert capsys.readouterr().out == ''


def test_page_get_textarea_contents(monkeypatch, capsys):
    """unittest for main.Page.get_textarea_contents
    """
    class MockActie:
        """stub
        """
    testobj = setup_page(monkeypatch, capsys)
    assert testobj.get_textarea_contents() == 'text'
    assert capsys.readouterr().out == 'call PageGui.get_textarea_contents()\n'


def test_page0_init(monkeypatch, capsys):
    """unittest for main.Page0.init
    """
    # monkeypatch.setattr(main, 'Page', MockPage)  # lijkt niet te werken
    monkeypatch.setattr(testee.gui, 'Page0Gui', MockPageGui)
    monkeypatch.setattr(testee.dmls, 'SortOptions', MockSortOpts)
    appbase = MockMainWindow()
    parent = MockBook()
    appbase.use_separate_subject = False
    appbase.work_with_user = False
    appbase.is_user = False
    parent.parent = appbase
    testobj = testee.Page0(parent)
    assert testobj.parent == parent
    assert testobj.selection == 'excl. gearchiveerde'
    assert testobj.sel_args == {}
    assert testobj.sorted == (0, "A")
    assert not testobj.sort_via_options
    assert testobj.saved_sortopts is None
    assert capsys.readouterr().out == (
        "called MainWindow.__init__() with args ()\ncalled MainGui.__init__()\n"
        f"called PageGui.__init__() with args ({parent}, {testobj}, [122, 24, 146, 100]) {{}}\n"
        "called PageGui.enable_buttons() with args ()\n")

    appbase = MockMainWindow()
    parent = MockBook()
    appbase.use_separate_subject = True
    appbase.work_with_user = True
    appbase.is_user = True
    appbase.filename = 'fnaam'
    parent.parent = appbase
    testobj = testee.Page0(parent)
    assert testobj.parent == parent
    assert testobj.selection == 'excl. gearchiveerde'
    assert testobj.sel_args == {}
    assert testobj.sorted == (0, "A")
    assert not testobj.sort_via_options
    assert testobj.saved_sortopts is None
    assert capsys.readouterr().out == (
        "called MainWindow.__init__() with args ()\ncalled MainGui.__init__()\n"
        f"called PageGui.__init__() with args ({parent}, {testobj}, [122, 24, 146, 100, 90]) {{}}\n"
        "called PageGui.enable_buttons() with args ()\n")

    appbase = MockMainWindow()
    parent = MockBook()
    monkeypatch.setattr(testee, 'LIN', False)
    appbase.use_separate_subject = False
    appbase.work_with_user = True
    appbase.is_user = False
    parent.parent = appbase
    testobj = testee.Page0(parent)
    assert testobj.parent == parent
    assert testobj.selection == 'excl. gearchiveerde'
    assert testobj.sel_args == {}
    assert testobj.sorted == (0, "A")
    assert not testobj.sort_via_options
    assert testobj.saved_sortopts is None
    assert capsys.readouterr().out == (
        "called MainWindow.__init__() with args ()\ncalled MainGui.__init__()\n"
        f"called PageGui.__init__() with args ({parent}, {testobj}, [64, 24, 114, 72]) {{}}\n"
        "called PageGui.enable_buttons() with args ()\n")

    appbase = MockMainWindow()
    parent = MockBook()
    appbase.use_separate_subject = True
    appbase.work_with_user = False
    appbase.is_user = True
    appbase.filename = 'fnaam'
    parent.parent = appbase
    testobj = testee.Page0(parent)
    assert testobj.parent == parent
    assert testobj.selection == 'excl. gearchiveerde'
    assert testobj.sel_args == {}
    assert testobj.sorted == (0, "A")
    assert not testobj.sort_via_options
    assert testobj.saved_sortopts is None
    assert capsys.readouterr().out == (
        "called MainWindow.__init__() with args ()\ncalled MainGui.__init__()\n"
        f"called PageGui.__init__() with args ({parent}, {testobj}, [64, 24, 114, 72, 72]) {{}}\n"
        "called PageGui.enable_buttons() with args ()\n")


def setup_page0(monkeypatch, capsys):
    def mock_init_page(self):
        print('called Page.__init__()')
    monkeypatch.setattr(testee.Page0, '__init__', mock_init_page)
    testobj = testee.Page0()
    testobj.parent = types.SimpleNamespace(pagedata=MockActie(), count=lambda *x: 3,
                                           fnaam='testfile')
    testobj.appbase = MockMainWindow()
    testobj.gui = MockPageGui()
    assert capsys.readouterr().out == ('called Page.__init__()\n'
                                       'called MainWindow.__init__() with args ()\n'
                                       'called MainGui.__init__()\n'
                                       'called PageGui.__init__() with args () {}\n')
    return testobj


def test_page0_vulp(monkeypatch, capsys):
    """unittest for main.Page0.vulp
    """
    # class MockActie:
    #     """stub
    #     """
    def mock_super_vulp(self):
        """stub
        """
        print('called Page.vulp()')
    class MockSortOptions:
        """stub
        """
        def load_options(self):
            """stub
            """
            return {}
    class MockSortOptions2:
        """stub
        """
        def load_options(self):
            """stub
            """
            return {'sort': 'options'}
    def mock_populate_list():
        """stub
        """
        print('called Page0.populate_list()')
        return 'list populated'
    monkeypatch.setattr(testee.Page, 'vulp', mock_super_vulp)
    testobj = setup_page0(monkeypatch, capsys)

    testobj.appbase.work_with_user = False
    testobj.sort_via_options = False
    testobj.parent.rereadlist = False
    testobj.gui.has_selection = lambda *x: False
    testobj.vulp()
    assert testobj.selection == ''
    assert testobj.seltitel == 'alle meldingen '
    assert capsys.readouterr().out == ('called PageGui.enable_sorting(True)\n'
                                       'called Page.vulp()\n'
                                       'call MainWindow.enable_all_book_tabs(False)\n'
                                       'called PageGui.enable_buttons() with args ()\n'
                                       'call MainWindow.set_statusmessage()\n')

    testobj.appbase.work_with_user = True
    testobj.parent.rereadlist = True
    testobj.saved_sortopts = {}
    testobj.selection = ''
    testobj.appbase.startitem = ''
    monkeypatch.setattr(testobj, 'populate_list', mock_populate_list)
    testobj.vulp()
    assert testobj.selection == ''
    assert testobj.seltitel == 'alle meldingen '
    assert capsys.readouterr().out == ('called PageGui.enable_sorting(True)\n'
                                       'called Page.vulp()\n'
                                       'called Page0.populate_list()\n'
                                       'called PageGui.get_first_item() with args ()\n'
                                       'call MainWindow.enable_all_book_tabs(False)\n'
                                       'called PageGui.enable_buttons() with args ()\n'
                                       "call MainWindow.set_statusmessage(list populated)\n")

    testobj.saved_sortopts = MockSortOptions()
    testobj.vulp()
    assert testobj.selection == 'volgens user gedefinieerde selectie'
    assert testobj.seltitel == 'alle meldingen volgens user gedefinieerde selectie'
    assert capsys.readouterr().out == ('called PageGui.enable_sorting(False)\n'
                                       'called Page.vulp()\n'
                                       'call MainWindow.enable_all_book_tabs(False)\n'
                                       'called PageGui.enable_buttons() with args ()\n'
                                       'call MainWindow.set_statusmessage()\n')

    testobj.parent.rereadlist = True
    testobj.saved_sortopts = MockSortOptions2()
    testobj.gui.has_selection = lambda *x: True
    testobj.appbase.startitem = 'startitem'
    testobj.vulp()
    assert testobj.selection == 'volgens user gedefinieerde selectie'
    assert testobj.seltitel == 'alle meldingen volgens user gedefinieerde selectie'
    assert capsys.readouterr().out == ('called PageGui.enable_sorting(False)\n'
                                       'called Page.vulp()\n'
                                       'called Page0.populate_list()\n'
                                       "called PageGui.get_item_by_id() with args ('startitem',)\n"
                                       'call MainWindow.enable_all_book_tabs(False)\n'
                                       'called PageGui.enable_buttons() with args ()\n'
                                       'call MainWindow.enable_all_book_tabs(True)\n'
                                       'called PageGui.set_selection()\n'
                                       'called PageGui.ensure_visible(`item_by_id`)\n'
                                       "call MainWindow.set_statusmessage(list populated)\n")


def test_page0_populate_list(monkeypatch, capsys):
    """unittest for main.Page0.populate_list
    """
    # class MockActie:
    #     """stub
    #     """
    def mock_get_acties_7(*args):
        """stub
        """
        print('called dml.get_acties with args', args)
        return [['x0', 'y', ('0', 'cat0'), ('0', 'stat0'), 'q', 'r', 'arch'],
                ['x1', 'y', ('0', 'cat0'), ('0', 'stat0'), 'q', 'r', '']]
    def mock_get_acties_8(*args):
        """stub
        """
        print('called dml.get_acties with args', args)
        return [['x0', 'y', '1', '1', 'q', 'r', 's', True],
                ['x1', 'y', '1', '1', 'q', 'r', 's', False]]
    def mock_get_acties_10(*args):
        """stub
        """
        print('called dml.get_acties with args', args)
        return [['x0', 'y', '0', '0', 'a', 'b', 'q', 'r', 's', True],
                ['x1', 'y', '0', '0', 'a', 'b', 'q', 'r', 's', False]]
    testobj = setup_page0(monkeypatch, capsys)

    monkeypatch.setattr(testee.shared, 'get_acties', {'7': mock_get_acties_7, '8': mock_get_acties_8,
                                                    '10': mock_get_acties_10})
    testobj.parent.stats = {0: ('first', '1'), 1: ('second', '2')}
    testobj.parent.cats = {0: ('start', '1'), 1: ('next', '2')}
    testobj.appbase.user = 'me'

    testobj.sel_args = {}
    testobj.appbase.datatype = '7'
    testobj.populate_list()
    assert testobj.parent.data == {0: ('x0', 'y', 'stat0.0', 'cat0.0', 'r', 'q', True),
                                   1: ('x1', 'y', 'stat0.0', 'cat0.0', 'r', 'q', False)}
    assert capsys.readouterr().out == ("called PageGui.clear_list()\n"
                                       "called dml.get_acties with args ('testfile', {}, '', 'me')\n"
                                       "called PageGui.add_listitem(`x0`)\n"
                                       "called PageGui.set_listitem_values() with args"
                                       " (None, ['x0', 'stat0.0', 'cat0.0', 'r', 'q', True])\n"
                                       "called PageGui.add_listitem(`x1`)\n"
                                       "called PageGui.set_listitem_values() with args"
                                       " (None, ['x1', 'stat0.0', 'cat0.0', 'r', 'q', False])\n")

    testobj.sel_args = {'arch': 'yes'}
    testobj.appbase.datatype = '8'
    testobj.populate_list()
    assert testobj.parent.data == {0: ('x0', 'y', '1.start', '1.first', 'q', 'r', 's', True),
                                   1: ('x1', 'y', '1.start', '1.first', 'q', 'r', 's', False)}
    assert capsys.readouterr().out == (
            "called PageGui.clear_list()\n"
            "called dml.get_acties with args ('testfile', {}, 'yes', 'me')\n"
            "called PageGui.add_listitem(`x0`)\n"
            "called PageGui.set_listitem_values() with args"
            " (None, ['x0', '1.start', '1.first', 'q', 'r', 's', True])\n"
            "called PageGui.add_listitem(`x1`)\n"
            "called PageGui.set_listitem_values() with args"
            " (None, ['x1', '1.start', '1.first', 'q', 'r', 's', False])\n")

    testobj.sel_args = {'sel': 'args'}
    testobj.appbase.datatype = '10'
    testobj.populate_list()
    assert testobj.parent.data == {0: ('x0', 'y', 'b.a', '0.0', 's', 'q', 'r', True),
                                   1: ('x1', 'y', 'b.a', '0.0', 's', 'q', 'r', False)}
    assert capsys.readouterr().out == (
            "called PageGui.clear_list()\n"
            "called dml.get_acties with args ('testfile', {'sel': 'args'}, '', 'me')\n"
            "called PageGui.add_listitem(`x0`)\n"
            "called PageGui.set_listitem_values() with args"
            " (None, ['x0', 'b.a', '0.0', 's', 'q', 'r', True])\n"
            "called PageGui.add_listitem(`x1`)\n"
            "called PageGui.set_listitem_values() with args"
            " (None, ['x1', 'b.a', '0.0', 's', 'q', 'r', False])\n")


def test_page0_change_selected(monkeypatch, capsys):
    """unittest for main.Page0.change_selected
    """
    # class MockActie:
    #     """stub
    #     """
    def mock_readp(self, itemno):
        """stub
        """
        print(f'called Page0.readp(`{itemno}`)')
    monkeypatch.setattr(testee.Page0, 'readp', mock_readp)
    testobj = setup_page0(monkeypatch, capsys)
    testobj.parent.newitem = True
    testobj.parent.pagedata.arch = False
    testobj.change_selected('1')
    assert testobj.parent.current_item == '1'
    assert capsys.readouterr().out == ('called PageGui.set_selection()\n'
                                       'called PageGui.set_archive_button_text(`&Archiveer`)\n')
    testobj.parent.newitem = False
    testobj.parent.pagedata.arch = True
    testobj.change_selected('1')
    assert testobj.parent.current_item == '1'
    assert capsys.readouterr().out == ('called PageGui.set_selection()\n'
                                       'called PageGui.get_selected_action()\n'
                                       'called Page0.readp(`1`)\n'
                                       'called PageGui.set_archive_button_text(`&Herleef`)\n')


def test_page0_activate_item(monkeypatch, capsys):
    """unittest for main.Page0.activate_item
    """
    class MockActie:
        """stub
        """
    def mock_goto_actie(self):
        """stub
        """
        print('called Page0.goto_actie()')
    monkeypatch.setattr(testee.Page0, 'goto_actie', mock_goto_actie)
    testobj = setup_page0(monkeypatch, capsys)
    testobj.activate_item()
    assert capsys.readouterr().out == 'called Page0.goto_actie()\n'


def test_page0_select_items(monkeypatch, capsys):
    """unittest for main.Page0.select_items
    """
    # class MockActie:
    #     """stub
    #     """
    class MockSelectOptions:
        """stub
        """
        def __init__(self, *args):
            pass
        def load_options(self):
            """stub
            """
            return {'nummer': [('aaa', 'GT'), ('en',), ('zzz', 'LT')], 'this': 'that'}
    def mock_show_message(win, msg):
        """stub
        """
        print(f'called gui.show_message(`{msg}`)')
    def mock_show_dialog(win, dlg, *args):
        """stub
        """
        print('called gui.show_dialog() for SelectOptions with selargs', args[0][0])
    def mock_show_dialog_ok(win, dlg, *args):
        """stub
        """
        print('called gui.show_dialog() for SelectOptions with selargs', args[0][0])
        return True
    counter = 0
    def mock_vulp():
        """stub
        """
        nonlocal counter
        counter += 1
        print('called Page0.vulp()')
        if counter == 1:
            raise AttributeError('got a data error')
    testobj = setup_page0(monkeypatch, capsys)
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
    testobj.appbase.use_separate_subject = False
    testobj.appbase.work_with_user = False
    testobj.sel_args = {'sel': 'args'}
    testobj.select_items()
    assert capsys.readouterr().out == ('called gui.show_dialog() for SelectOptions'
                                       " with selargs {'sel': 'args'}\n")

    testobj.appbase.use_separate_subject = True
    testobj.appbase.work_with_user = True
    testobj.appbase.user = 'me'
    monkeypatch.setattr(testee.shared, 'DataError', {'X': AttributeError})
    testobj.appbase.datatype = 'X'
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog_ok)
    monkeypatch.setattr(testee.dmls, 'SelectOptions', MockSelectOptions)
    monkeypatch.setattr(testobj, 'vulp', mock_vulp)
    testobj.select_items()
    assert capsys.readouterr().out == ('called gui.show_dialog() for SelectOptions with selargs'
                                       " {'idgt': 'aaa', 'id': 'and', 'idlt': 'zzz',"
                                       " 'this': 'that'}\n"
                                       'called Page0.vulp()\n'
                                       "called gui.show_message(`got a data error`)\n"
                                       'called gui.show_dialog() for SelectOptions with selargs'
                                       " {'idgt': 'aaa', 'id': 'and', 'idlt': 'zzz',"
                                       " 'this': 'that'}\n"
                                       'called Page0.vulp()\n')

    monkeypatch.setattr(MockSelectOptions, 'load_options', lambda *x: {'nummer': [('aaa', 'GT'),
                                                                                  ('of',),
                                                                                  ('zzz', 'LT')]})
    monkeypatch.setattr(testee.dmls, 'SelectOptions', MockSelectOptions)
    testobj.select_items()
    assert capsys.readouterr().out == ('called gui.show_dialog() for SelectOptions with selargs'
                                       " {'idgt': 'aaa', 'id': 'or', 'idlt': 'zzz'}\n"
                                       'called Page0.vulp()\n')


def test_page0_sort_items(monkeypatch, capsys):
    """unittest for main.Page0.sort_items
    """
    # class MockActie:
    #     """stub
    #     """
    class MockSortOptions:
        """stub
        """
        def load_options(self):
            """stub
            """
            return {}
    class MockSortOptions2:
        """stub
        """
        def load_options(self):
            """stub
            """
            return {'sort': 'options'}
    def mock_show_message(win, msg):
        """stub
        """
        print(f'called gui.show_message(`{msg}`)')
    def mock_show_dialog(win, dlg, *args):
        """stub
        """
        print('called gui.show_dialog() for SelectOptions with sortargs', args[0])
    def mock_show_dialog_ok(win, dlg, *args):
        """stub
        """
        print('called gui.show_dialog() for SelectOptions with sortargs', args[0])
        return True
    def mock_vulp():
        """stub
        """
        print('called Page0.vulp()')
    def mock_vulp_err():
        """stub
        """
        print('called Page0.vulp()')
        raise AttributeError('got a data error')
    testobj = setup_page0(monkeypatch, capsys)
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
    testobj.saved_sortopts = False
    testobj.sort_items()
    assert capsys.readouterr().out == ('called gui.show_message('
                                       '`Sorry, multi-column sorteren werkt nog niet`)\n')

    testobj.saved_sortopts = MockSortOptions()
    monkeypatch.setattr(testee.dmls.my, 'SORTFIELDS', [])
    testobj.parent.ctitels = ['dit', 'dat']
    testobj.sort_items()
    assert capsys.readouterr().out == ('called gui.show_dialog() for SelectOptions with sortargs'
                                       " ({}, ['(geen)', 'dit', 'Soort'])\n")

    testobj.saved_sortopts = MockSortOptions2()
    testobj.sort_via_options = False
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog_ok)
    monkeypatch.setattr(testee.dmls.my, 'SORTFIELDS', [('col0', 0), ('col1', 1)])
    testobj.sort_items()
    assert capsys.readouterr().out == ("called gui.show_dialog() for SelectOptions with sortargs"
                                       " ({'sort': 'options'}, ['(geen)', 'col0', 'col1'])\n"
                                       'called PageGui.enable_sorting(True)\n')

    testobj.sort_via_options = True
    monkeypatch.setattr(testobj, 'vulp', mock_vulp)
    testobj.sort_items()
    assert capsys.readouterr().out == ("called gui.show_dialog() for SelectOptions with sortargs"
                                       " ({'sort': 'options'}, ['(geen)', 'col0', 'col1'])\n"
                                       'called PageGui.enable_sorting(False)\n'
                                       'called Page0.vulp()\n')

    monkeypatch.setattr(testobj, 'vulp', mock_vulp_err)
    monkeypatch.setattr(testee.shared, 'DataError', {'X': AttributeError})
    testobj.appbase.datatype = 'X'
    testobj.sort_items()
    assert capsys.readouterr().out == ("called gui.show_dialog() for SelectOptions with sortargs"
                                       " ({'sort': 'options'}, ['(geen)', 'col0', 'col1'])\n"
                                       'called PageGui.enable_sorting(False)\n'
                                       'called Page0.vulp()\n'
                                       'called gui.show_message(`got a data error`)\n')


def test_page0_archiveer(monkeypatch, capsys):
    """unittest for main.Page0.archiveer
    """
    # class MockActie:
    #     """stub
    #     """
    #     def __init__(self):
    #         pass
    #     def add_event(self, *args):
    #         """stub
    #         """
    #         print('called Actie.add_event() with args', args)
    def mock_readp(self, action):
        """stub
        """
        print(f'called Page0.readp() using arch `{action}`')
    def mock_update_actie(self):
        """stub
        """
        print('called Page0.update_actie()')
    def mock_vulp(self):
        """stub
        """
        print('called Page0.vulp()')
    monkeypatch.setattr(testee.Page0, 'readp', mock_readp)
    monkeypatch.setattr(testee.Page0, 'update_actie', mock_update_actie)
    monkeypatch.setattr(testee.Page0, 'vulp', mock_vulp)
    testobj = setup_page0(monkeypatch, capsys)
    testobj.parent.current_item = 'x'
    testobj.sel_args = {}
    testobj.parent.pagedata.arch = False
    testobj.archiveer()
    assert testobj.parent.pagedata.arch
    assert capsys.readouterr().out == ('called PageGui.get_selected_action()\n'
                                       'called Page0.readp() using arch `1`\n'
                                       "called Actie.add_event() with args ('Actie gearchiveerd',)\n"
                                       'called Page0.update_actie()\n'
                                       'called Page0.vulp()\n'
                                       'called MainGui.set_tabfocus(0)\n')
    testobj.archiveer()
    assert not testobj.parent.pagedata.arch
    assert capsys.readouterr().out == ('called PageGui.get_selected_action()\n'
                                       'called Page0.readp() using arch `1`\n'
                                       "called Actie.add_event() with args ('Actie herleefd',)\n"
                                       'called Page0.update_actie()\n'
                                       'called Page0.vulp()\n'
                                       'called MainGui.set_tabfocus(0)\n')
    testobj.sel_args = {'arch': 'alles'}
    testobj.parent.pagedata.arch = False
    testobj.archiveer()
    assert testobj.parent.pagedata.arch
    assert capsys.readouterr().out == ('called PageGui.get_selected_action()\n'
                                       'called Page0.readp() using arch `1`\n'
                                       "called Actie.add_event() with args ('Actie gearchiveerd',)\n"
                                       'called Page0.update_actie()\n'
                                       'called Page0.vulp()\n'
                                       'called MainGui.set_tabfocus(0)\n'
                                       'called PageGui.ensure_visible(`x`)\n'
                                       'called PageGui.set_archive_button_text(`&Herleef`)\n')
    testobj.archiveer()
    assert not testobj.parent.pagedata.arch
    assert capsys.readouterr().out == ('called PageGui.get_selected_action()\n'
                                       'called Page0.readp() using arch `1`\n'
                                       "called Actie.add_event() with args ('Actie herleefd',)\n"
                                       'called Page0.update_actie()\n'
                                       'called Page0.vulp()\n'
                                       'called MainGui.set_tabfocus(0)\n'
                                       'called PageGui.ensure_visible(`x`)\n'
                                       'called PageGui.set_archive_button_text(`&Archiveer`)\n')


def test_page0_enable_buttons(monkeypatch, capsys):
    """unittest for main.Page0.enable_buttons
    """
    # class MockActie:
    #     """stub
    #     """
    testobj = setup_page0(monkeypatch, capsys)
    testobj.enable_buttons()
    assert capsys.readouterr().out == 'called PageGui.enable_buttons() with args ()\n'
    testobj.enable_buttons('value')
    assert capsys.readouterr().out == "called PageGui.enable_buttons() with args ('value',)\n"


def test_page0_get_items(monkeypatch, capsys):
    """unittest for main.Page0.get_items
    """
    # class MockActie:
    #     """stub
    #     """
    testobj = setup_page0(monkeypatch, capsys)
    assert testobj.get_items() == ['all', 'the', 'items']
    assert capsys.readouterr().out == 'called PageGui.get_items()\n'


def test_page0_get_item_text(monkeypatch, capsys):
    """unittest for main.Page0.get_item_text
    """
    # class MockActie:
    #     """stub
    #     """
    testobj = setup_page0(monkeypatch, capsys)
    assert testobj.get_item_text('item', 'colno') == 'the text of the item'
    assert capsys.readouterr().out == "called PageGui.get_item_text() with args ('item', 'colno')\n"


def test_page0_clear_selection(monkeypatch, capsys):
    """unittest for main.Page0.clear_selection
    """
    # class MockActie:
    #     """stub
    #     """
    testobj = setup_page0(monkeypatch, capsys)
    testobj.clear_selection()
    assert testobj.sel_args == {}


def test_page1_init(monkeypatch, capsys):
    """unittest for main.Page1.init
    """
    # monkeypatch.setattr(main, 'Page', MockPage)  # lijkt niet te werken
    monkeypatch.setattr(testee.gui, 'Page1Gui', MockPageGui)
    appbase = MockMainWindow()
    parent = MockBook()
    parent.parent = appbase
    testobj = testee.Page1(parent)
    assert testobj.parent == parent
    assert hasattr(testobj, 'gui')
    assert capsys.readouterr().out == (
            "called MainWindow.__init__() with args ()\ncalled MainGui.__init__()\n"
            f"called PageGui.__init__() with args ({parent}, {testobj}) {{}}\n")


def setup_page1(monkeypatch, capsys):
    def mock_init_page(self):
        print('called Page.__init__()')
    monkeypatch.setattr(testee.Page1, '__init__', mock_init_page)
    testobj = testee.Page1()
    testobj.parent = types.SimpleNamespace(pagedata=MockActie(), count=lambda *x: 3,
                                           pages=[testobj])
    testobj.appbase = MockMainWindow()
    testobj.gui = MockPageGui()
    assert capsys.readouterr().out == ('called Page.__init__()\n'
                                       'called MainWindow.__init__() with args ()\n'
                                       'called MainGui.__init__()\n'
                                       'called PageGui.__init__() with args () {}\n')
    return testobj


def test_page1_vulp(monkeypatch, capsys):
    """unittest for main.Page1.vulp
    """
    class MockActie:
        """stub
        """
        def __init__(self):
            self.id = '2000-0001'
            self.datum = 'datestring'
            self.arch = True
            self.over = 'subject'
            self.titel = "it's: the arts"
            self.status = 0
            self.soort = 'I'
            self.melding = 'in short: this'
    def mock_super_vulp(self):
        """stub
        """
        print('called Page.super_vulp()')
    monkeypatch.setattr(testee.Page, 'vulp', mock_super_vulp)
    testobj = setup_page1(monkeypatch, capsys)
    testobj.appbase.is_user = True
    testobj.parent.pagedata = None
    testobj.vulp()
    assert capsys.readouterr().out == ('called Page.super_vulp()\n'
                                       'called PageGui.init_fields()\n'
                                       'called PageGui.set_text() for field `arch` text ``\n'
                                       'called PageGui.set_archive_button_text(`Archiveren`)\n'
                                       'called PageGui.enable_fields() with args (True,)\n')

    testobj = setup_page1(monkeypatch, capsys)
    testobj.parent.pagedata = MockActie()
    testobj.parent.pages = [MockPage()]
    assert capsys.readouterr().out == ('called Page.__init__() with args () {}\n'
                                       'called PageGui.__init__() with args () {}\n')
    testobj.parent.cats = []
    testobj.parent.stats = []
    testobj.appbase.use_separate_subject = True
    testobj.appbase.use_text_panels = True
    testobj.appbase.is_user = True
    testobj.vulp()
    assert capsys.readouterr().out == ('called Page.super_vulp()\n'
                      'called PageGui.init_fields()\n'
                      'called PageGui.set_text() for field `id` text `2000-0001`\n'
                      'called PageGui.set_text() for field `date` text `datestring`\n'
                      'called PageGui.set_text() for field `proc` text `subject`\n'
                      "called PageGui.set_text() for field `desc` text `it's: the arts`\n"
                      "called PageGui.set_choice() with args ([], 'stat', 0)\n"
                      "called PageGui.set_choice() with args ([], 'cat', 'I')\n"
                      'called PageGui.set_text() for field `arch` text `Deze actie is gearchiveerd`\n'
                      'called PageGui.set_archive_button_text(`Herleven`)\n'
                      'called PageGui.enable_fields() with args (False,)\n')

    testobj.parent.pagedata.arch = False
    testobj.appbase.use_separate_subject = False
    testobj.appbase.use_text_panels = False
    testobj.appbase.is_user = True
    testobj.vulp()
    assert capsys.readouterr().out == ('called Page.super_vulp()\n'
                      'called PageGui.init_fields()\n'
                      'called PageGui.set_text() for field `id` text `2000-0001`\n'
                      'called PageGui.set_text() for field `date` text `datestring`\n'
                      "called PageGui.set_text() for field `proc` text `it's`\n"
                      "called PageGui.set_text() for field `desc` text `the arts`\n"
                      "called PageGui.set_choice() with args ([], 'stat', 0)\n"
                      "called PageGui.set_choice() with args ([], 'cat', 'I')\n"
                      'called PageGui.set_text() for field `summary` text `in short: this`\n'
                      'called PageGui.set_text() for field `arch` text ``\n'
                      'called PageGui.set_archive_button_text(`Archiveren`)\n'
                      'called PageGui.enable_fields() with args (True,)\n')

    testobj.parent.pagedata.titel = 'onderwerp - beschrijving'
    testobj.appbase.use_separate_subject = False
    testobj.appbase.use_text_panels = False
    testobj.appbase.is_user = False
    testobj.vulp()
    assert capsys.readouterr().out == ('called Page.super_vulp()\n'
                      'called PageGui.init_fields()\n'
                      'called PageGui.set_text() for field `id` text `2000-0001`\n'
                      'called PageGui.set_text() for field `date` text `datestring`\n'
                      "called PageGui.set_text() for field `proc` text `onderwerp`\n"
                      "called PageGui.set_text() for field `desc` text `beschrijving`\n"
                      "called PageGui.set_choice() with args ([], 'stat', 0)\n"
                      "called PageGui.set_choice() with args ([], 'cat', 'I')\n"
                      'called PageGui.set_text() for field `summary` text `in short: this`\n'
                      'called PageGui.set_text() for field `arch` text ``\n'
                      'called PageGui.set_archive_button_text(`Archiveren`)\n'
                      'called PageGui.enable_fields() with args (False,)\n')


def test_page1_savep(monkeypatch, capsys):
    """unittest for main.Page1.savep
    """
    def mock_show_message(cls, msg, title=''):
        """stub
        """
        print(f'called gui.show_message with args `{title}` `{msg}`')
    class MockActie:
        """stub
        """
        def __init__(self):
            self.titel = ''
            self.over = ''
            self.status = 0
            self.soort = ''
            self.arch = False
            self.melding = ''
        def add_event(self, text):
            """stub
            """
            print(f'called Actie.add_event with text `{text}`')
    def mock_get_text(self, fieldname):
        """stub
        """
        if fieldname == 'proc':
            return ''
        if fieldname == 'desc':
            return 'desc'
        return fieldname
    def mock_get_text_2(self, fieldname):
        """stub
        """
        if fieldname == 'proc':
            return 'proc'
        if fieldname == 'desc':
            return ''
        return fieldname
    def mock_get_text_3(self, fieldname):
        """stub
        """
        if fieldname in ('proc', 'desc'):
            return fieldname
        return ''
    def mock_get_text_4(self, fieldname):
        """stub
        """
        return fieldname
    def mock_get_text_5(self, fieldname):
        """stub
        """
        if fieldname in ('proc', 'desc'):
            return fieldname.title()
        if fieldname == 'summary':
            return fieldname
        return ''
    def mock_get_choice_data(self, fieldname):
        """stub
        """
        if fieldname == 'stat':
            return 0, 'gemeld'
        if fieldname == 'cat':
            return '', 'onbekend'
        return None, None
    def mock_get_choice_data_2(self, fieldname):
        """stub
        """
        if fieldname == 'stat':
            return 1, 'Started'
        if fieldname == 'cat':
            return 'P', 'Problem'
        return None, None
    def mock_super_savep(self):
        """stub
        """
        print('called Page.super_savep()')
    def mock_enable_buttons(value):
        """stub
        """
        print(f'called Page.enable_buttons({value})')
    def mock_update_actie(self):
        """stub
        """
        print('called Page.update_actie()')

    monkeypatch.setattr(testee.Page, 'savep', mock_super_savep)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
    monkeypatch.setattr(MockPageGui, 'get_text', mock_get_text)
    monkeypatch.setattr(testee.Page1, 'update_actie', mock_update_actie)
    testobj = setup_page1(monkeypatch, capsys)
    testobj.enable_buttons = mock_enable_buttons
    assert not testobj.savep()
    assert capsys.readouterr().out == ('called Page.super_savep()\n'
                                       'called PageGui.set_text() for field `proc` text ``\n'
                                       'called Page.enable_buttons(False)\n'
                                       'called gui.show_message with args ``'
                                       ' `Beide tekstrubrieken moeten worden ingevuld`\n')

    monkeypatch.setattr(MockPageGui, 'get_text', mock_get_text_2)
    testobj = setup_page1(monkeypatch, capsys)
    testobj.enable_buttons = mock_enable_buttons
    assert not testobj.savep()
    assert capsys.readouterr().out == ('called Page.super_savep()\n'
                                       'called PageGui.set_text() for field `proc` text `Proc`\n'
                                       'called Page.enable_buttons(False)\n'
                                       'called gui.show_message with args ``'
                                       ' `Beide tekstrubrieken moeten worden ingevuld`\n')

    monkeypatch.setattr(MockPageGui, 'get_text', mock_get_text_3)
    monkeypatch.setattr(MockPageGui, 'get_choice_data', mock_get_choice_data)
    testobj.parch = False
    testobj.appbase.use_separate_subject = False
    testobj.appbase.use_text_panels = True
    testobj.parent.pagedata = MockActie()
    assert testobj.savep()
    assert capsys.readouterr().out == ('called Page.super_savep()\n'
                                       'called PageGui.set_text() for field `proc` text `Proc`\n'
                                       'called Page.enable_buttons(False)\n'
                                       'called Actie.add_event with text'
                                       ' `Titel gewijzigd in "proc - desc"`\n'
                                       'called Page.update_actie()\n')

    monkeypatch.setattr(MockPageGui, 'get_text', mock_get_text_4)
    monkeypatch.setattr(MockPageGui, 'get_choice_data', mock_get_choice_data_2)
    testobj.parch = True
    testobj.appbase.use_separate_subject = True
    testobj.appbase.use_text_panels = False
    assert testobj.savep()
    assert capsys.readouterr().out == ('called Page.super_savep()\n'
                                       'called PageGui.set_text() for field `proc` text `Proc`\n'
                                       'called Page.enable_buttons(False)\n'
                                       'called Actie.add_event with text'
                                       ' `Status gewijzigd in "Started"`\n'
                                       'called Actie.add_event with text'
                                       ' `Categorie gewijzigd in "Problem"`\n'
                                       'called Actie.add_event with text `Actie gearchiveerd`\n'
                                       'called Actie.add_event with text `Meldingtekst aangepast`\n'
                                       'called Page.update_actie()\n')

    monkeypatch.setattr(MockPageGui, 'get_text', mock_get_text_5)
    testobj.parch = False
    assert testobj.savep()
    assert capsys.readouterr().out == ('called Page.super_savep()\n'
                                       'called PageGui.set_text() for field `proc` text `Proc`\n'
                                       'called Page.enable_buttons(False)\n'
                                       'called Actie.add_event with text'
                                       ' `Onderwerp gewijzigd in "Proc"`\n'
                                       'called Actie.add_event with text'
                                       ' `Titel gewijzigd in "Desc"`\n'
                                       'called Actie.add_event with text `Actie herleefd`\n'
                                       'called Page.update_actie()\n')


def test_page1_archiveer(monkeypatch, capsys):
    """unittest for main.Page1.archiveer
    """
    # class MockActie:
    #     """stub
    #     """
    def mock_savep(self):
        """stub
        """
        print('called Page1.savep()')
    def mock_vulp(self):
        """stub
        """
        print('called Page1.vulp()')
    monkeypatch.setattr(testee.Page1, 'savep', mock_savep)
    monkeypatch.setattr(testee.Page1, 'vulp', mock_vulp)
    testobj = setup_page1(monkeypatch, capsys)
    testobj.parch = False
    testobj.archiveer()
    assert testobj.parch
    assert capsys.readouterr().out == ('called Page1.savep()\ncalled Page1.vulp()\n')


def test_page1_vul_combos(monkeypatch, capsys):
    """unittest for main.Page1.vul_combos
    """
    # class MockActie:
    #     """stub
    #     """
    testobj = setup_page1(monkeypatch, capsys)
    testobj.parent.stats = {'2': ('text2', 'II', 2), '1': ('text1', 'I')}
    testobj.parent.cats = {'2': ('cat2', '02', 2), '1': ('cat1', '01')}
    testobj.vul_combos()
    assert capsys.readouterr().out == ("called PageGui.clear_stats()\n"
                                       "called PageGui.clear_cats()\n"
                                       "called PageGui.add_stat_choice() using args ('text1', 'I')\n"
                                       "called PageGui.add_stat_choice() using args ('text2', 'II')\n"
                                       "called PageGui.add_cat_choice() using args ('cat1', '01')\n"
                                       "called PageGui.add_cat_choice() using args ('cat2', '02')\n")


def test_page1_field_text(monkeypatch, capsys):
    """unittest for main.Page1.field_text
    """
    # class MockActie:
    #     """stub
    #     """
    testobj = setup_page1(monkeypatch, capsys)
    assert testobj.get_field_text('item') == 'the text of the item'
    assert capsys.readouterr().out == "called PageGui.get_field_text() with args ('item',)\n"


def test_page6_init(monkeypatch, capsys):
    """unittest for main.Page6.init
    """
    # monkeypatch.setattr(main, 'Page', MockPage)  # lijkt niet te werken
    monkeypatch.setattr(testee.gui, 'Page6Gui', MockPageGui)
    appbase = MockMainWindow()
    parent = MockBook()
    parent.parent = appbase
    testobj = testee.Page6(parent)
    # assert testobj.parent == 'parent'  # parent associatie via de superklasse
    assert testobj.current_item == 0
    assert testobj.oldtext == ""
    assert (testobj.event_list, testobj.event_data, testobj.old_list, testobj.old_data) == (
            [], [], [], [])
    assert not testobj.status_auto_changed
    assert hasattr(testobj, 'gui')
    assert capsys.readouterr().out == (
            "called MainWindow.__init__() with args ()\ncalled MainGui.__init__()\n"
            f"called PageGui.__init__() with args ({parent}, {testobj}) {{}}\n")


def setup_page6(monkeypatch, capsys):
    def mock_init_page(self):
        print('called Page.__init__()')
    monkeypatch.setattr(testee.Page6, '__init__', mock_init_page)
    testobj = testee.Page6()
    testobj.parent = types.SimpleNamespace(pagedata=MockActie(), count=lambda *x: 3,
                                           pages=[testobj])
    testobj.appbase = MockMainWindow()
    testobj.gui = MockPageGui()
    assert capsys.readouterr().out == ('called Page.__init__()\n'
                                       'called MainWindow.__init__() with args ()\n'
                                       "called MainGui.__init__()\n"
                                       'called PageGui.__init__() with args () {}\n')
    return testobj


def test_page6_vulp(monkeypatch, capsys):
    """unittest for main.Page6.vulp
    """
    def mock_super_vulp(self):
        """stub
        """
        print('called Page.super_vulp()')
    # class MockActie:
    #     """stub
    #     """
    monkeypatch.setattr(testee.Page, 'vulp', mock_super_vulp)
    testobj = setup_page6(monkeypatch, capsys)
    testobj.appbase.work_with_user = False
    testobj.appbase.is_user = True                  # eerder had ik deze niet nodig?
    testobj.parent.pagedata.events = []
    testobj.old_list, testobj.old_data = [], []
    testobj.vulp()
    assert testobj.oldbuf == ([], [])
    assert testobj.oldtext == ''
    assert capsys.readouterr().out == ('called Page.super_vulp()\n'
                                       'called PageGui.init_textfield()\n'
                                       'called PageGui.init_list() with text'
                                       ' `-- doubleclick or press Shift-Ctrl-N to add new item --`\n'
                                       'called PageGui.clear_textfield()\n')

    testobj = setup_page6(monkeypatch, capsys)
    testobj.parent.pagedata.events = []
    testobj.appbase.work_with_user = True
    testobj.appbase.is_user = False
    testobj.vulp()
    assert testobj.oldbuf == ([], [])
    assert testobj.oldtext == ''
    assert capsys.readouterr().out == ('called Page.super_vulp()\n'
                                       'called PageGui.init_textfield()\n'
                                       'called PageGui.init_list() with text'
                                       ' `-- adding new items is disabled --`\n'
                                       'called PageGui.init_set_list_callback()\n'
                                       'called PageGui.clear_textfield()\n')

    testobj = setup_page6(monkeypatch, capsys)
    testobj.parent.pagedata.events = [('2001-01-01 01:10:10', 'first event'),
                                      ('2010-01-01 10:10:10', 'next event')]
    testobj.appbase.work_with_user = True
    testobj.appbase.is_user = True
    testobj.vulp()
    assert testobj.oldbuf == (['01-01-2010 10:10:10', '01-01-2001 01:10:10'],
                              ['next event', 'first event'])
    assert testobj.oldtext == ''
    assert capsys.readouterr().out == ('called Page.super_vulp()\n'
                                       'called PageGui.init_textfield()\n'
                                       'called PageGui.init_list() with text'
                                       ' `-- doubleclick or press Shift-Ctrl-N to add new item --`\n'
                                       'called PageGui.add_item_to_list() with args'
                                       ' `0` `01-01-2010 10:10:10`\n'
                                       'called PageGui.add_item_to_list() with args'
                                       ' `1` `01-01-2001 01:10:10`\n'
                                       'called PageGui.init_set_list_callback()\n'
                                       'called PageGui.clear_textfield()\n')


def test_page6_savep(monkeypatch, capsys):
    """unittest for main.Page6.savep
    """
    def mock_super_savep(self):
        """stub
        """
        print('called Page.super_savep()')
    def mock_update_actie(*args):
        """stub
        """
        print('called Page.update_actie()')
    monkeypatch.setattr(testee.Page, 'savep', mock_super_savep)
    testobj = setup_page6(monkeypatch, capsys)
    testobj.parent.pagedata.events = [('date1', 'not_text'), ('date2', 'text')]
    testobj.parent.pagedata.updated = True
    testobj.update_actie = mock_update_actie

    testobj.old_list = testobj.event_list = ['date1', 'date2']
    testobj.old_data = testobj.event_data = ['not text', 'text']
    testobj.current_item = 2
    assert testobj.savep()
    assert capsys.readouterr().out == ('called Page.super_savep()\n'
                                       'called PageGui.get_textfield_contents()\n')
    testobj.current_item = 0
    testobj.parent.current_item = 'parentitem'  # for tab 0
    testobj.old_data = ['not_text', 'text']
    assert testobj.savep()
    assert capsys.readouterr().out == ('called Page.super_savep()\n'
                                       'called PageGui.get_textfield_contents()\n'
                                       'called PageGui.set_listitem_text() with args'
                                       ' `1` `date1 - text...`\n'
                                       'called PageGui.set_listitem_data() with args `1`\n'
                                       'called Page.update_actie()\n'
                                       "called PageGui.set_item_text() with args"
                                       " ('parentitem', 3, True)\n")
    assert testobj.parent.pagedata.events == [('date2', 'text'), ('date1', 'text')]
    assert testobj.oldbuf == (['date1', 'date2'], ['text', 'text'])

    testobj.current_item = 3
    testobj.event_list = ['date1', 'date2', 'date3']
    testobj.old_list = testobj.event_list[:-1]
    testobj.event_data = ['not text', 'text', 'newtext']
    testobj.old_data = testobj.event_data[:-1]
    assert testobj.savep()
    assert capsys.readouterr().out == ('called Page.super_savep()\n'
                                       'called PageGui.get_textfield_contents()\n'
                                       'called PageGui.set_listitem_text() with args'
                                       ' `3` `date3 - text...`\n'
                                       'called PageGui.set_listitem_data() with args `3`\n'
                                       'called Page.update_actie()\n'
                                       "called PageGui.set_item_text() with args"
                                       " ('parentitem', 3, True)\n")
    assert testobj.parent.pagedata.events == [('date3', 'text'), ('date2', 'text'),
                                              ('date1', 'not text')]
    assert testobj.oldbuf == (['date1', 'date2', 'date3'], ['not text', 'text', 'text'])


def test_page6_goto_prev(monkeypatch, capsys):
    """unittest for main.Page6.goto_prev
    """
    monkeypatch.setattr(MockPageGui, 'get_list_row', lambda *x: 1)
    testobj = setup_page6(monkeypatch, capsys)
    testobj.goto_prev()
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(MockPageGui, 'get_list_row', lambda *x: 2)
    testobj = setup_page6(monkeypatch, capsys)
    testobj.goto_prev()
    assert capsys.readouterr().out == 'called PageGui.set_list_row(1)\n'


def test_page6_goto_next(monkeypatch, capsys):
    """unittest for main.Page6.goto_next
    """
    monkeypatch.setattr(MockPageGui, 'get_list_row', lambda *x: 1)
    monkeypatch.setattr(MockPageGui, 'get_list_rowcount', lambda *x: 2)
    testobj = setup_page6(monkeypatch, capsys)
    testobj.goto_next()
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(MockPageGui, 'get_list_row', lambda *x: 0)
    monkeypatch.setattr(MockPageGui, 'get_list_rowcount', lambda *x: 2)
    testobj = setup_page6(monkeypatch, capsys)
    testobj.goto_next()
    assert capsys.readouterr().out == 'called PageGui.set_list_row(1)\n'


def test_page6_on_text(monkeypatch, capsys):
    """unittest for main.Page6.on_text
    """
    def mock_enable_buttons():
        """stub
        """
        print('called Page6.enable_buttons()')
    monkeypatch.setattr(MockPageGui, 'get_list_row', lambda *x: 0)
    testobj = setup_page6(monkeypatch, capsys)
    testobj.initializing = True
    testobj.on_text()
    assert capsys.readouterr().out == ''

    testobj.initializing = False
    testobj.oldtext = 'text'
    testobj.on_text()
    assert capsys.readouterr().out == 'called PageGui.get_textfield_contents()\n'

    testobj.oldtext = 'oldtext'
    testobj.appbase.is_user = False
    testobj.on_text()
    assert capsys.readouterr().out == ('called PageGui.get_textfield_contents()\n'
                                       'called PageGui.convert_text() with args `text`, to=`plain`\n')

    monkeypatch.setattr(MockPageGui, 'get_list_row', lambda *x: 1)
    monkeypatch.setattr(MockPageGui, 'get_listitem_text', lambda *x: 'datestring - textstring')
    monkeypatch.setattr(MockPageGui, 'convert_text', lambda *x, **y: 'text\nwith linebreak')
    testobj = setup_page6(monkeypatch, capsys)
    testobj.initializing = False
    testobj.oldtext = 'oldtext'
    testobj.event_data = ['date', 'text']
    testobj.appbase.is_user = True
    monkeypatch.setattr(testobj, 'enable_buttons', mock_enable_buttons)
    testobj.on_text()
    assert capsys.readouterr().out == ('called PageGui.get_textfield_contents()\n'
                                       'called Page6.enable_buttons()\n'
                                       'called PageGui.set_listitem_text() with args `1`'
                                       ' `datestring - text`\n')

    monkeypatch.setattr(MockPageGui, 'get_list_row', lambda *x: 1)
    monkeypatch.setattr(MockPageGui, 'get_listitem_text', lambda *x: 'datestring - textstring')
    monkeypatch.setattr(MockPageGui, 'convert_text', lambda *x, **y:
                        'text exceeding a certain amount of characters so that it gets chopped off')
    testobj = setup_page6(monkeypatch, capsys)
    testobj.initializing = False
    testobj.oldtext = 'oldtext'
    testobj.event_data = ['date', 'text']
    testobj.appbase.is_user = False
    monkeypatch.setattr(testobj, 'enable_buttons', mock_enable_buttons)
    testobj.on_text()
    assert capsys.readouterr().out == ('called PageGui.get_textfield_contents()\n'
                                       'called PageGui.set_listitem_text() with args `1`'
                                       ' `datestring - text exceeding a certain amount of characters'
                                       ' so that it gets chopp...`\n')


def test_page6_initialize_new_event(monkeypatch, capsys):
    """unittest for main.Page6.initialize_new_event
    """
    def mock_get_dts():
        """stub
        """
        print('called shared.get_dts()')
        return 'datestring'
    monkeypatch.setattr(testee.shared, 'get_dts', mock_get_dts)
    monkeypatch.setattr(MockPageGui, 'get_list_row', lambda *x: 0)
    testobj = setup_page6(monkeypatch, capsys)
    testobj.parent.stats = {1: ('Aangenomen', '1')}
    testobj.appbase.is_user = False
    testobj.initialize_new_event()
    assert capsys.readouterr().out == ''

    testobj.appbase.is_user = True
    testobj.event_list = ['existing']
    testobj.event_data = ['item']
    testobj.parent.pagedata.status = '1'
    testobj.initialize_new_event()
    assert testobj.event_list == ['datestring', 'existing']
    assert testobj.event_data == ['', 'item']
    assert testobj.oldtext == ''
    assert capsys.readouterr().out == ('called shared.get_dts()\n'
                                       "called PageGui.add_new_item_to_list() with args"
                                       " ('datestring', '')\n"
                                       'called PageGui.enable_buttons() with args ()\n')

    testobj.event_list = []
    testobj.event_data = []
    testobj.parent.pagedata.status = '0'
    testobj.appbase.use_text_panels = True
    testobj.parent.current_tab = 2
    testobj.initialize_new_event()
    assert testobj.event_list == ['datestring']
    assert testobj.event_data == ['']
    assert testobj.oldtext == ''
    assert capsys.readouterr().out == ('called shared.get_dts()\n'
                                       "called PageGui.add_new_item_to_list() with args"
                                       " ('datestring', '')\n"
                                       'called PageGui.enable_buttons() with args ()\n')

    testobj.event_list = []
    testobj.event_data = []
    testobj.parent.pagedata.status = '0'
    testobj.appbase.use_text_panels = False
    testobj.parent.current_tab = 1
    testobj.initialize_new_event()
    assert testobj.event_list == ['datestring']
    assert testobj.event_data == ['']
    assert testobj.oldtext == ''
    assert capsys.readouterr().out == ('called shared.get_dts()\n'
                                       "called PageGui.add_new_item_to_list() with args"
                                       " ('datestring', '')\n"
                                       'called PageGui.enable_buttons() with args ()\n')

    testobj.event_list = []
    testobj.event_data = []
    testobj.parent.pagedata.status = '0'
    testobj.appbase.use_text_panels = True
    testobj.parent.current_tab = 3
    testobj.initialize_new_event()
    assert testobj.parent.pagedata.status == '1'
    assert testobj.status_auto_changed
    assert testobj.event_list == ['datestring', 'datestring']
    assert testobj.event_data == ['', 'Status gewijzigd in "Aangenomen"']
    assert testobj.oldtext == ''
    assert capsys.readouterr().out == ('called shared.get_dts()\n'
                                       "called PageGui.add_new_item_to_list() with args"
                                       " ('datestring', 'Status gewijzigd in \"Aangenomen\"')\n"
                                       'called shared.get_dts()\n'
                                       "called PageGui.add_new_item_to_list() with args"
                                       " ('datestring', '')\n"
                                       'called PageGui.enable_buttons() with args ()\n')

    testobj.event_list = []
    testobj.event_data = []
    testobj.parent.pagedata.status = '0'
    testobj.appbase.use_text_panels = False
    testobj.parent.current_tab = 2
    testobj.initialize_new_event()
    assert testobj.parent.pagedata.status == '1'
    assert testobj.status_auto_changed
    assert testobj.event_list == ['datestring', 'datestring']
    assert testobj.event_data == ['', 'Status gewijzigd in "Aangenomen"']
    assert testobj.oldtext == ''
    assert capsys.readouterr().out == ('called shared.get_dts()\n'
                                       "called PageGui.add_new_item_to_list() with args"
                                       " ('datestring', 'Status gewijzigd in \"Aangenomen\"')\n"
                                       'called shared.get_dts()\n'
                                       "called PageGui.add_new_item_to_list() with args"
                                       " ('datestring', '')\n"
                                       'called PageGui.enable_buttons() with args ()\n')


class MockOptionsMaster:
    """stub for MainWindow in the role of master of MainGui parent of Options classes
    """
    def __init__(self):
        self.book = types.SimpleNamespace(tabs={1: '1 eerste', 3: '3 derde', 2: '2 tweede'},
                stats={1: ('opgepakt', '1'), 2: ('afgehandeld', '2'), 0: ('gemeld', '0')},
                cats={1: ('probleem', 'P'), 2: ('wens', 'W'), 0: ('Onbekend', ' ')})
    def save_settings(self, type_, data):
        """stub
        """
        print(f'called master.save_settings() with args `{type_}` `{data}`')


def test_taboptions_initstuff():
    """unittest for main.Taboptions.initstuff
    """
    testobj = testee.TabOptions()
    parent = types.SimpleNamespace(master=MockOptionsMaster())
    testobj.initstuff(parent)
    assert testobj.titel == 'Tab titels'
    assert testobj.data == ['eerste', 'tweede', 'derde']
    assert testobj.tekst == ["De tab titels worden getoond in de volgorde",
                             "zoals ze van links naar rechts staan.",
                             "Er kunnen geen tabs worden verwijderd of toegevoegd."]
    assert not testobj.editable


def test_taboptions_leesuit(capsys):
    """unittest for main.TabOptions.leesuit
    """
    testobj = testee.TabOptions()
    parent = types.SimpleNamespace(master=MockOptionsMaster())
    testobj.leesuit(parent, ['een', 'twee', 'drie'])
    assert testobj.newtabs == {'0': 'een', '1': 'twee', '2': 'drie'}
    assert capsys.readouterr().out == ("called master.save_settings() with args `tab`"
                                       " `{'0': 'een', '1': 'twee', '2': 'drie'}`\n")


def test_statoptions_initstuff():
    """unittest for main.StatOptions.initstuff
    """
    testobj = testee.StatOptions()
    parent = types.SimpleNamespace(master=MockOptionsMaster())
    testobj.initstuff(parent)
    assert testobj.titel == 'Status codes en waarden'
    assert testobj.data == ['0: gemeld', '1: opgepakt', '2: afgehandeld']
    assert testobj.tekst == ["De waarden voor de status worden getoond in dezelfde volgorde",
                             "als waarin ze in de combobox staan.",
                             "Vóór de dubbele punt staat de code, erachter de waarde.",
                             "Denk erom dat als je codes wijzigt of statussen verwijdert, deze",
                             "ook niet meer getoond en gebruikt kunnen worden in de registratie.",
                             "Omschrijvingen kun je rustig aanpassen"]
    assert testobj.editable


def test_statoptions_leesuit(capsys):
    """unittest for main.StatOptions.leesuit
    """
    testobj = testee.StatOptions()
    parent = types.SimpleNamespace(master=MockOptionsMaster())
    assert testobj.leesuit(parent, ['nocolon']) == 'Foutieve waarde: bevat geen dubbele punt'
    assert testobj.leesuit(parent, ['1: een', '2: twee', '3: drie']) == ''
    assert testobj.newstats == {'1': ('een', 0), '2': ('twee', 1), '3': ('drie', 2)}
    assert capsys.readouterr().out == ("called master.save_settings() with args `stat`"
                                       " `{'1': ('een', 0), '2': ('twee', 1), '3': ('drie', 2)}`\n")


def test_catoptions_initstuff():
    """unittest for main.CatOptions.initstuff
    """
    testobj = testee.CatOptions()
    parent = types.SimpleNamespace(master=MockOptionsMaster())
    testobj.initstuff(parent)
    assert testobj.titel == 'Soort codes en waarden'
    assert testobj.data == [' : Onbekend', 'P: probleem', 'W: wens']
    assert testobj.tekst == ["De waarden voor de soorten worden getoond in dezelfde volgorde",
                             "als waarin ze in de combobox staan.",
                             "Vóór de dubbele punt staat de code, erachter de waarde.",
                             "Denk erom dat als je codes wijzigt of soorten verwijdert, deze",
                             "ook niet meer getoond en gebruikt kunnen worden in de registratie.",
                             "Omschrijvingen kun je rustig aanpassen"]
    assert testobj.editable


def test_catoptions_leesuit(capsys):
    """unittest for main.CatOptions.leesuit
    """
    testobj = testee.CatOptions()
    parent = types.SimpleNamespace(master=MockOptionsMaster())
    assert testobj.leesuit(parent, ['nocolon']) == 'Foutieve waarde: bevat geen dubbele punt'
    testobj.leesuit(parent, ['1: een', '2: twee', '3: drie'])
    assert testobj.newcats == {'1': ('een', 0), '2': ('twee', 1), '3': ('drie', 2)}
    assert capsys.readouterr().out == ("called master.save_settings() with args `cat`"
                                       " `{'1': ('een', 0), '2': ('twee', 1), '3': ('drie', 2)}`\n")


def test_mainwindow_init(monkeypatch, capsys):
    """unittest for main.MainWindow.init
    """
    def mock_select_datatype_x(self):
        """stub
        """
        self.datatype = testee.shared.DataType.XML
    def mock_select_datatype_x_f(self):
        """stub
        """
        self.datatype = testee.shared.DataType.XML
        self.filename = 'something'
    def mock_select_datatype_s(self):
        """stub
        """
        self.datatype = testee.shared.DataType.SQL
    def mock_select_datatype_m(self):
        """stub
        """
        self.datatype = testee.shared.DataType.MNG
    def mock_create_book(self):
        """stub
        """
        print('called.MainWindow.create_book()')
    def mock_create_book_pages(self):
        """stub
        """
        print('called.MainWindow.create_book_pages()')
    def mock_open_xml(self):
        """stub
        """
        print('called.MainWindow.open_xml()')
    def mock_startfile(self):
        """stub
        """
        print('called.MainWindow.startfile()')
    def mock_open_sql(self, do_sel):
        """stub
        """
        print('called.MainWindow.open_sql() with arg', do_sel)
    def mock_open_mongo(self):
        """stub
        """
        print('called.MainWindow.open_mongo()')
    monkeypatch.setattr(testee.dmls, 'get_projnames', lambda *x: ['django', 'project'])
    monkeypatch.setattr(testee.MainWindow, 'determine_datatype_from_filename', lambda *x: None)
    monkeypatch.setattr(testee.MainWindow, 'select_datatype', mock_select_datatype_x)
    monkeypatch.setattr(testee.gui, 'MainGui', MockMainGui)
    monkeypatch.setattr(testee.MainWindow, 'create_book', mock_create_book)
    monkeypatch.setattr(testee.MainWindow, 'create_book_pages', mock_create_book_pages)
    monkeypatch.setattr(testee.MainWindow, 'open_xml', mock_open_xml)
    monkeypatch.setattr(testee.MainWindow, 'startfile', mock_startfile)
    monkeypatch.setattr(testee.MainWindow, 'open_sql', mock_open_sql)
    monkeypatch.setattr(testee.MainWindow, 'open_mongo', mock_open_mongo)
    testobj = testee.MainWindow('parent', 'xml')
    assert testobj.parent == 'parent'
    assert testobj.title == 'Actieregistratie'
    # altijd hetzelfde
    assert not testobj.initializing
    assert not testobj.exiting
    assert testobj.oldsort == -1
    assert testobj.idlist == []
    assert testobj.actlist == []
    assert testobj.alist == []
    assert hasattr(testobj, 'gui')
    # verschillend per aansturing
    assert testobj.datatype == testee.shared.DataType.XML
    assert not testobj.work_with_user
    assert testobj.user == 1
    assert testobj.is_user
    assert testobj.is_admin
    assert testobj.multiple_files
    assert not testobj.multiple_projects
    assert testobj.use_text_panels
    assert testobj.use_rt
    assert not testobj.use_separate_subject
    assert capsys.readouterr().out == ('called MainGui.__init__()\n'
                                       'called.MainWindow.create_book()\n'
                                       'called MainGui.create_menu()\n'
                                       'called MainGui.enable_settingsmenu()\n'
                                       'called MainGui.create_actions()\n'
                                       'called.MainWindow.create_book_pages()\n'
                                       'called.MainWindow.open_xml()\n')
    monkeypatch.setattr(testee.MainWindow, 'select_datatype', mock_select_datatype_x_f)
    testobj = testee.MainWindow('parent')
    assert testobj.datatype == testee.shared.DataType.XML
    assert not testobj.work_with_user
    assert testobj.user == 1
    assert testobj.is_user
    assert testobj.is_admin
    assert testobj.multiple_files
    assert not testobj.multiple_projects
    assert testobj.use_text_panels
    assert testobj.use_rt
    assert not testobj.use_separate_subject
    assert capsys.readouterr().out == ('called MainGui.__init__()\n'
                                       'called.MainWindow.create_book()\n'
                                       'called MainGui.create_menu()\n'
                                       'called MainGui.enable_settingsmenu()\n'
                                       'called MainGui.create_actions()\n'
                                       'called.MainWindow.create_book_pages()\n'
                                       'called.MainWindow.startfile()\n')
    monkeypatch.setattr(testee.MainWindow, 'select_datatype', mock_select_datatype_s)
    testobj = testee.MainWindow('parent', 'sql')
    assert testobj.datatype == testee.shared.DataType.SQL
    assert testobj.work_with_user
    assert testobj.user is None
    assert not testobj.is_user
    assert not testobj.is_admin
    assert not testobj.multiple_files
    assert testobj.multiple_projects
    assert testobj.use_text_panels
    assert not testobj.use_rt
    assert testobj.use_separate_subject
    assert capsys.readouterr().out == ('called MainGui.__init__()\n'
                                       'called.MainWindow.create_book()\n'
                                       'called MainGui.create_menu()\n'
                                       'called MainGui.enable_settingsmenu()\n'
                                       'called MainGui.create_actions()\n'
                                       'called.MainWindow.create_book_pages()\n'
                                       'called.MainWindow.open_sql() with arg True\n')
    monkeypatch.setattr(testee.MainWindow, 'select_datatype', mock_select_datatype_m)
    testobj = testee.MainWindow('parent', 'mongo')
    assert testobj.datatype == testee.shared.DataType.MNG
    assert not testobj.work_with_user
    assert testobj.user == 1
    assert testobj.is_user
    assert testobj.is_admin
    assert not testobj.multiple_files
    assert not testobj.multiple_projects
    assert not testobj.use_text_panels
    assert not testobj.use_rt
    assert testobj.use_separate_subject
    assert capsys.readouterr().out == ('called MainGui.__init__()\n'
                                       'called.MainWindow.create_book()\n'
                                       'called MainGui.create_menu()\n'
                                       'called MainGui.enable_settingsmenu()\n'
                                       'called MainGui.create_actions()\n'
                                       'called.MainWindow.create_book_pages()\n'
                                       'called.MainWindow.open_mongo()\n')


def mock_init_mainwindow(self, *args):
    """stubi for setting up MainWindow object
    """
    self.filename = self.dirname = ''
    self.projnames = [('django', 'project'), ('basic', 'another_project')]
    self.gui = MockMainGui(self)
    self.book = types.SimpleNamespace()


def test_mainwindow_determine_datatype(monkeypatch):
    """unittest for main.MainWindow.determine_datatype
    """
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    testobj = testee.MainWindow()
    testobj.determine_datatype_from_filename('xml')
    assert testobj.datatype == testee.shared.DataType.XML
    assert (testobj.dirname, testobj.filename) == ('', '')
    monkeypatch.setattr(testee.os.path, 'exists', lambda x: True)
    monkeypatch.setattr(testee.os.path, 'isfile', lambda x: True)
    testobj = testee.MainWindow()
    testobj.determine_datatype_from_filename('path/to/file/filename')
    assert testobj.datatype == testee.shared.DataType.XML
    assert (testobj.dirname, testobj.filename) == (testee.pathlib.Path('path/to/file'), 'filename')
    monkeypatch.setattr(testee.os.path, 'exists', lambda x: False)
    testobj = testee.MainWindow()
    testobj.determine_datatype_from_filename('sql')
    assert testobj.datatype == testee.shared.DataType.SQL
    assert (testobj.dirname, testobj.filename) == ('', '')
    monkeypatch.setattr(testee.os.path, 'exists', lambda x: True)
    monkeypatch.setattr(testee.os.path, 'isfile', lambda x: False)
    testobj = testee.MainWindow()
    testobj.determine_datatype_from_filename('django')
    assert testobj.datatype == testee.shared.DataType.SQL
    assert (testobj.dirname, testobj.filename) == ('', 'django')
    monkeypatch.setattr(testee.os.path, 'exists', lambda x: False)
    testobj = testee.MainWindow()
    testobj.determine_datatype_from_filename('basic')
    assert testobj.datatype == testee.shared.DataType.SQL
    assert (testobj.dirname, testobj.filename) == ('', '_basic')
    testobj = testee.MainWindow()
    testobj.determine_datatype_from_filename('mongo')
    assert testobj.datatype == testee.shared.DataType.MNG
    assert (testobj.dirname, testobj.filename) == ('', '')
    testobj = testee.MainWindow()
    testobj.determine_datatype_from_filename('mongodb')
    assert testobj.datatype == testee.shared.DataType.MNG
    assert (testobj.dirname, testobj.filename) == ('', '')


def test_mainwindow_select_datatype(monkeypatch):
    """unittest for main.MainWindow.select_datatype
    """
    counter = 0
    def mock_get_choice(*args):
        """stub
        """
        nonlocal counter
        choice = ('XML', 'SQL', 'MNG', 'something else')[counter]
        print('called gui.get_choice_item()')
        counter += 1
        return choice
    monkeypatch.setattr(testee.gui, 'get_choice_item', mock_get_choice)
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    testobj = testee.MainWindow()
    testobj.select_datatype()
    assert testobj.datatype == testee.shared.DataType.XML
    testobj.select_datatype()
    assert testobj.datatype == testee.shared.DataType.SQL
    testobj.select_datatype()
    assert testobj.datatype == testee.shared.DataType.MNG
    with pytest.raises(SystemExit) as exc:
        testobj.select_datatype()
    assert str(exc.value) == 'No datatype selected'


def test_mainwindow_get_menu_data(monkeypatch):
    """unittest for main.MainWindow.get_menu_data
    """
    def mock_goto(*args):
        """stub
        """
        return str(args)
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    testobj = testee.MainWindow()
    for value in ('open_xml', 'new_file', 'print_scherm', 'print_actie', 'exit_app', 'sign_in',
                  'font_settings', 'colour_settings', 'tab_settings', 'cat_settings', 'stat_settings',
                  'silly_menu', 'about_help', 'hotkey_help', 'open_sql', 'new_project'):
        setattr(testobj, value, value)
    testobj.gui = types.SimpleNamespace(go_to=mock_goto)
    testobj.book = types.SimpleNamespace(tabs={'1': 'start', '2': 'finish'})
    testobj.work_with_user = testobj.multiple_projects = False
    testobj.multiple_files = True
    stuff = testobj.get_menu_data()
    viewstuff = stuff.pop(2)
    assert stuff == [('&File',
       [('&Open', 'open_xml', 'Ctrl+O', ' Open a new file'),
        ('&New', 'new_file', 'Ctrl+N', ' Create a new file'), ('',),
        ('&Print', (('Dit &Scherm', 'print_scherm', 'Shift+Ctrl+P',
         'Print the contents of the current screen'),
        ('Deze &Actie', 'print_actie', 'Alt+Ctrl+P', 'Print the contents of the current issue'))),
        ('',), ('&Quit', 'exit_app', 'Ctrl+Q', ' Terminate the program')]),
        ('&Settings', (('&Applicatie', (('&Lettertype', 'font_settings', '',
                                        ' Change the size and font of the text'),
         ('&Kleuren', 'colour_settings', '', ' Change the colours of various items'))),
                   ('&Data', (('&Tabs', 'tab_settings', '', ' Change the titles of the tabs'),
         ('&Soorten', 'cat_settings', '', ' Add/change type categories'),
                        ('St&atussen', 'stat_settings', '', ' Add/change status categories'))),
         ('&Het leven', 'silly_menu', '', ' Change the way you look at life'))),
        # ('&View', [('&start', main.functools.partial(mock_goto, 1), 'Alt+1', 'switch to tab'),
        #            ('&finish', main.functools.partial(mock_goto, 2), 'Alt+2', 'switch to tab')]),
        ('&Help', (('&About', 'about_help', 'F1', ' Information about this program'),
         ('&Keys', 'hotkey_help', 'Ctrl+H', ' List of shortcut keys')))]
    assert viewstuff[0] == '&View'
    assert (viewstuff[1][0][0], viewstuff[1][1][0]) == ('&start', '&finish')
    assert (viewstuff[1][0][2], viewstuff[1][1][2]) == ('Alt+1', 'Alt+2')
    assert (viewstuff[1][0][3], viewstuff[1][1][3]) == ('switch to tab', 'switch to tab')

    testobj.work_with_user = testobj.multiple_projects = True
    testobj.multiple_files = False
    stuff = testobj.get_menu_data()
    viewstuff = stuff.pop(3)
    assert stuff == [('&File',
       [('&Other project', 'open_sql', 'Ctrl+O', ' Select a project'),
        ('&New', 'new_project', 'Ctrl+N', ' Create a new project'), ('',),
        ('&Print', (('Dit &Scherm', 'print_scherm', 'Shift+Ctrl+P',
         'Print the contents of the current screen'),
        ('Deze &Actie', 'print_actie', 'Alt+Ctrl+P', 'Print the contents of the current issue'))),
        ('',), ('&Quit', 'exit_app', 'Ctrl+Q', ' Terminate the program')]),
        ('&User', [('&Login', 'sign_in', 'Ctrl+L', ' Sign in to the database')]),
        ('&Settings', (('&Applicatie', (('&Lettertype', 'font_settings', '',
                                        ' Change the size and font of the text'),
         ('&Kleuren', 'colour_settings', '', ' Change the colours of various items'))),
                    ('&Data', (('&Tabs', 'tab_settings', '', ' Change the titles of the tabs'),
         ('&Soorten', 'cat_settings', '', ' Add/change type categories'),
                        ('St&atussen', 'stat_settings', '', ' Add/change status categories'))),
         ('&Het leven', 'silly_menu', '', ' Change the way you look at life'))),
        # ('&View', [('&start', main.functools.partial(mock_goto, 1), 'Alt+1', 'switch to tab'),
        #            ('&finish', main.functools.partial(mock_goto, 2), 'Alt+2', 'switch to tab')]),
        ('&Help', (('&About', 'about_help', 'F1', ' Information about this program'),
         ('&Keys', 'hotkey_help', 'Ctrl+H', ' List of shortcut keys')))]
    assert viewstuff[0] == '&View'
    assert (viewstuff[1][0][0], viewstuff[1][1][0]) == ('&start', '&finish')
    assert (viewstuff[1][0][2], viewstuff[1][1][2]) == ('Alt+1', 'Alt+2')
    assert (viewstuff[1][0][3], viewstuff[1][1][3]) == ('switch to tab', 'switch to tab')

    testobj.work_with_user = testobj.multiple_projects = False
    testobj.multiple_files = False
    stuff = testobj.get_menu_data()
    viewstuff = stuff.pop(2)
    assert stuff == [('&File',
       [('&Print', (('Dit &Scherm', 'print_scherm', 'Shift+Ctrl+P',
         'Print the contents of the current screen'),
        ('Deze &Actie', 'print_actie', 'Alt+Ctrl+P', 'Print the contents of the current issue'))),
        ('',), ('&Quit', 'exit_app', 'Ctrl+Q', ' Terminate the program')]),
        ('&Settings', (('&Applicatie', (('&Lettertype', 'font_settings', '',
                                        ' Change the size and font of the text'),
         ('&Kleuren', 'colour_settings', '', ' Change the colours of various items'))),
                    ('&Data', (('&Tabs', 'tab_settings', '', ' Change the titles of the tabs'),
         ('&Soorten', 'cat_settings', '', ' Add/change type categories'),
                            ('St&atussen', 'stat_settings', '', ' Add/change status categories'))),
         ('&Het leven', 'silly_menu', '', ' Change the way you look at life'))),
        # ('&View', [('&start', main.functools.partial(mock_goto, 1), 'Alt+1', 'switch to tab'),
        #            ('&finish', main.functools.partial(mock_goto, 2), 'Alt+2', 'switch to tab')]),
        ('&Help', (('&About', 'about_help', 'F1', ' Information about this program'),
         ('&Keys', 'hotkey_help', 'Ctrl+H', ' List of shortcut keys')))]
    assert viewstuff[0] == '&View'
    assert (viewstuff[1][0][0], viewstuff[1][1][0]) == ('&start', '&finish')
    assert (viewstuff[1][0][2], viewstuff[1][1][2]) == ('Alt+1', 'Alt+2')
    assert (viewstuff[1][0][3], viewstuff[1][1][3]) == ('switch to tab', 'switch to tab')


def test_mainwindow_create_book(monkeypatch, capsys):
    """unittest for main.MainWindow.create_book
    """
    def mock_lees_settings(self):
        """stub
        """
        print('called MainWindow.lees_settings()')
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.MainWindow, 'lees_settings', mock_lees_settings)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.filename = ''
    testobj.multiple_projects = False
    testobj.use_separate_subject = False
    testobj.create_book()
    assert isinstance(testobj.book, MockBook)
    assert testobj.book.parent == testobj
    assert testobj.book.fnaam == ''
    assert testobj.book.current_item is None
    assert testobj.book.data == {}
    assert testobj.book.rereadlist
    assert testobj.book.ctitels == ["actie", " ", "status", "L.wijz.", "titel"]
    assert testobj.book.current_tab == -1
    assert testobj.book.pages == []
    assert not testobj.book.newitem
    assert testobj.book.changed_item
    assert testobj.book.pagedata is None
    assert capsys.readouterr().out == ('called MainGui.get_bookwidget()\n'
                                       'called MainWindow.lees_settings()\n')

    testobj.filename = ''
    testobj.multiple_projects = True
    testobj.use_separate_subject = True
    testobj.create_book()
    assert isinstance(testobj.book, MockBook)
    assert testobj.book.parent == testobj
    assert testobj.book.fnaam == ''
    assert testobj.book.current_item is None
    assert testobj.book.data == {}
    assert testobj.book.rereadlist
    assert testobj.book.ctitels == ["actie", " ", "status", "L.wijz.", "betreft", "omschrijving"]
    assert testobj.book.current_tab == -1
    assert testobj.book.pages == []
    assert not testobj.book.newitem
    assert testobj.book.changed_item
    assert testobj.book.pagedata is None
    assert capsys.readouterr().out == ('called MainGui.get_bookwidget()\n'
                                       'called MainWindow.lees_settings()\n')

    testobj.filename = 'this'
    testobj.multiple_projects = False
    testobj.use_separate_subject = True
    testobj.create_book()
    assert isinstance(testobj.book, MockBook)
    assert testobj.book.parent == testobj
    assert testobj.book.fnaam == ''
    assert testobj.book.current_item is None
    assert testobj.book.data == {}
    assert testobj.book.rereadlist
    assert testobj.book.ctitels == ["actie", " ", "status", "L.wijz.", "betreft", "omschrijving"]
    assert testobj.book.current_tab == -1
    assert testobj.book.pages == []
    assert not testobj.book.newitem
    assert testobj.book.changed_item
    assert testobj.book.pagedata is None
    assert capsys.readouterr().out == ('called MainGui.get_bookwidget()\n'
                                       'called MainWindow.lees_settings()\n')

    testobj.filename = 'this'
    testobj.multiple_projects = True
    testobj.use_separate_subject = False
    testobj.create_book()
    assert isinstance(testobj.book, MockBook)
    assert testobj.book.parent == testobj
    assert testobj.book.fnaam == 'this'
    assert testobj.book.current_item is None
    assert testobj.book.data == {}
    assert testobj.book.rereadlist
    assert testobj.book.ctitels == ["actie", " ", "status", "L.wijz.", "titel"]
    assert testobj.book.current_tab == -1
    assert testobj.book.pages == []
    assert not testobj.book.newitem
    assert testobj.book.changed_item
    assert testobj.book.pagedata is None
    assert capsys.readouterr().out == ('called MainGui.get_bookwidget()\n'
                                       'called MainWindow.lees_settings()\n')


def test_mainwindow_create_book_pages(monkeypatch, capsys):
    """unittest for main.MainWindow.create_book_pages
    """
    def mock_enable_all_book_tabs(self, state):
        """stub
        """
        print(f'called MainWindow.enable_all_book_tabs({state})')
    def mock_page(parent, pageno):
        """stub
        """
        print(f'called Page.__init__() for page {pageno}')
        return f'{pageno}'
    def mock_page0(parent):
        """stub
        """
        print('called Page0.__init__()')
        return '0'
    def mock_page1(parent):
        """stub
        """
        print('called Page1.__init__()')
        return '1'
    def mock_page6(parent):
        """stub
        """
        print('called Page6.__init__()')
        return '6'
    monkeypatch.setattr(testee, 'Page', mock_page)
    monkeypatch.setattr(testee, 'Page0', mock_page0)
    monkeypatch.setattr(testee, 'Page1', mock_page1)
    monkeypatch.setattr(testee, 'Page6', mock_page6)
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.MainWindow, 'enable_all_book_tabs', mock_enable_all_book_tabs)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.book = types.SimpleNamespace(pages=[])
    testobj.book.tabs = ['nulde', 'eerste', 'laatste']
    testobj.use_text_panels = False
    testobj.create_book_pages()
    assert testobj.book.pages == ['0', '1', '6']
    assert capsys.readouterr().out == ('called Page0.__init__()\n'
                                       'called Page1.__init__()\n'
                                       'called Page6.__init__()\n'
                                       "called MainGui.add_book_tab with args ('0', '&nulde')\n"
                                       "called MainGui.add_book_tab with args ('1', '&eerste')\n"
                                       "called MainGui.add_book_tab with args ('6', '&laatste')\n"
                                       'called MainWindow.enable_all_book_tabs(False)\n')
    testobj.book.pages = []
    testobj.book.tabs = ['nulde', 'eerste', 'tweede', 'derde', 'vierde', 'vijfde', 'laatste']
    testobj.use_text_panels = True
    testobj.create_book_pages()
    assert testobj.book.pages == ['0', '1', '2', '3', '4', '5', '6']
    assert capsys.readouterr().out == ('called Page0.__init__()\n'
                                       'called Page1.__init__()\n'
                                       'called Page.__init__() for page 2\n'
                                       'called Page.__init__() for page 3\n'
                                       'called Page.__init__() for page 4\n'
                                       'called Page.__init__() for page 5\n'
                                       'called Page6.__init__()\n'
                                       "called MainGui.add_book_tab with args ('0', '&nulde')\n"
                                       "called MainGui.add_book_tab with args ('1', '&eerste')\n"
                                       "called MainGui.add_book_tab with args ('2', '&tweede')\n"
                                       "called MainGui.add_book_tab with args ('3', '&derde')\n"
                                       "called MainGui.add_book_tab with args ('4', '&vierde')\n"
                                       "called MainGui.add_book_tab with args ('5', '&vijfde')\n"
                                       "called MainGui.add_book_tab with args ('6', '&laatste')\n"
                                       'called MainWindow.enable_all_book_tabs(False)\n')


def test_mainwindow_not_implemented_message(monkeypatch, capsys):
    """unittest for main.MainWindow.not_implemented_message
    """
    def mock_show_message(self, mld):
        """stub
        """
        print(f'called MainWindow.show_message(`{mld}`)')
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.not_implemented_message()
    assert capsys.readouterr().out == 'called MainWindow.show_message(`Sorry, werkt nog niet`)\n'


def test_mainwindow_new_file(monkeypatch, capsys):
    """unittest for main.MainWindow.new_file
    """
    def mock_get_save_filename(self, *args, **kwargs):
        """stub
        """
        return ''
    def mock_get_save_filename_2(self, *args, **kwargs):
        """stub
        """
        return 'filename'
    def mock_get_save_filename_3(self, *args, **kwargs):
        """stub
        """
        return 'filename.xml'
    def mock_show_message(self, mld):
        """stub
        """
        print(f'called MainWindow.show_message(`{mld}`)')
    def mock_enable_all_book_tabs(self, state):
        """stub
        """
        print(f'called MainWindow.enable_all_book_tabs({state})')
    def mock_startfile(self):
        """stub
        """
        print('called MainWindow.startfile()')
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
    monkeypatch.setattr(testee.gui, 'get_save_filename', mock_get_save_filename)
    monkeypatch.setattr(testee.MainWindow, 'enable_all_book_tabs', mock_enable_all_book_tabs)
    monkeypatch.setattr(testee.MainWindow, 'startfile', mock_startfile)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.new_file()
    assert capsys.readouterr().out == ''

    monkeypatch.setattr(testee.gui, 'get_save_filename', mock_get_save_filename_2)
    testobj.new_file()
    assert capsys.readouterr().out == ('called MainWindow.show_message('
                                       '`Naam voor nieuw file moet wel extensie .xml hebben`)\n')

    monkeypatch.setattr(testee.gui, 'get_save_filename', mock_get_save_filename_3)
    testobj.new_file()
    assert str(testobj.dirname) == '.'
    assert testobj.filename == 'filename.xml'
    assert capsys.readouterr().out == ('called MainWindow.startfile()\n'
                                       'called MainWindow.enable_all_book_tabs(False)\n')


def test_mainwindow_open_xml(monkeypatch, capsys):
    """unittest for main.MainWindow.open_xml
    """
    def mock_get_open_filename(self, *args, **kwargs):
        """stub
        """
        print(f'called gui.get_open_filename starting at {kwargs["start"]}')
        return ''
    def mock_get_open_filename_2(self, *args, **kwargs):
        """stub
        """
        print(f'called gui.get_open_filename starting at {kwargs["start"]}')
        return 'filename.xml'
    def mock_startfile(self):
        """stub
        """
        print('called MainWindow.startfile()')
    monkeypatch.setattr(testee.gui, 'get_open_filename', mock_get_open_filename)
    monkeypatch.setattr(testee.os, 'getcwd', lambda: 'here')
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.MainWindow, 'startfile', mock_startfile)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.dirname = ''
    testobj.filename = ''
    testobj.open_xml()
    assert (str(testobj.dirname), testobj.filename) == ('here', '')
    assert capsys.readouterr().out == 'called gui.get_open_filename starting at here\n'

    monkeypatch.setattr(testee.gui, 'get_open_filename', mock_get_open_filename_2)
    testobj.dirname = 'dirname'
    testobj.open_xml()
    assert (str(testobj.dirname), testobj.filename) == ('.', 'filename.xml')
    assert capsys.readouterr().out == ('called gui.get_open_filename starting at dirname\n'
                                       'called MainWindow.startfile()\n')


def test_mainwindow_new_project(monkeypatch, capsys):
    """unittest for main.MainWindow.new_project
    """
    def mock_show_message(self, mld):
        """stub
        """
        print(f'called MainWindow.show_message(`{mld}`)')
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.new_project()
    assert capsys.readouterr().out == 'called MainWindow.show_message(`Sorry, werkt nog niet`)\n'


def test_mainwindow_open_sql(monkeypatch, capsys):
    """unittest for main.MainWindow.open_sql
    """
    projects = ['Demo: demo: sample project', 'unchanged: same: real project',
                'basic: basic: base project']
    counter = 0
    def mock_get_choice_item(*args):
        """stub
        """
        nonlocal counter
        counter += 1
        if counter == 1:
            return projects[0]
        if counter == 2:
            return projects[1]
        if counter == 3:
            return projects[2]
        return ''
    def mock_startfile(self):
        """stub
        """
        print('called MainWindow.startfile()')
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.MainWindow, 'startfile', mock_startfile)
    monkeypatch.setattr(testee.gui, 'get_choice_item', mock_get_choice_item)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'

    testobj.projnames = [x.split(': ') for x in projects]
    testobj.filename = testobj.projnames[0]
    testobj.open_sql()
    assert testobj.filename == '_basic'
    assert capsys.readouterr().out == 'called MainWindow.startfile()\n'

    testobj.filename = ''
    testobj.open_sql()
    assert testobj.filename == 'unchanged'
    assert capsys.readouterr().out == 'called MainWindow.startfile()\n'

    testobj.filename = ''
    testobj.open_sql()
    assert testobj.filename == '_basic'
    assert capsys.readouterr().out == 'called MainWindow.startfile()\n'

    testobj.filename = ''
    testobj.open_sql()
    assert testobj.filename == ''
    assert capsys.readouterr().out == ''

    testobj.filename = '_basic'
    testobj.open_sql(do_sel=False)
    assert testobj.filename == '_basic'
    assert capsys.readouterr().out == 'called MainWindow.startfile()\n'

    testobj.filename = 'unchanged'
    testobj.open_sql(do_sel=False)
    assert testobj.filename == 'unchanged'
    assert capsys.readouterr().out == 'called MainWindow.startfile()\n'


def test_mainwindow_open_mongo(monkeypatch, capsys):
    """unittest for main.MainWindow.open_mongo
    """
    def mock_startfile(self):
        """stub
        """
        print('called MainWindow.startfile()')
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.MainWindow, 'startfile', mock_startfile)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.open_mongo()
    assert testobj.filename == 'default'
    assert capsys.readouterr().out == 'called MainWindow.startfile()\n'


def test_mainwindow_print_something(monkeypatch, capsys):
    """unittest for main.MainWindow.print_something
    """
    counter = 0
    def mock_get_choice_item(*args):
        """stub
        """
        nonlocal counter
        counter += 1
        if counter == 1:
            return 'huidig scherm'
        # if counter == 2:
        return 'huidige actie'
    def mock_print_scherm(self):
        """stub
        """
        print('called MainWindow.print_scherm()')
    def mock_print_actie(self):
        """stub
        """
        print('called MainWindow.print_actie()')
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.MainWindow, 'print_scherm', mock_print_scherm)
    monkeypatch.setattr(testee.MainWindow, 'print_actie', mock_print_actie)
    monkeypatch.setattr(testee.gui, 'get_choice_item', mock_get_choice_item)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.print_something()
    assert capsys.readouterr().out == 'called MainWindow.print_scherm()\n'
    testobj.print_something()
    assert capsys.readouterr().out == 'called MainWindow.print_actie()\n'


def test_mainwindow_print_scherm(monkeypatch, capsys):
    """unittest for main.MainWindow.print_scherm
    """
    def mock_get_items():
        """stub
        """
        print('called Page.get_items()')
        return ['item0', 'item1', 'item2']
    def mock_get_item_text(row, column):
        """stub
        """
        print(f'called Page.get_item_text() for `{row}` column {column}`')
        data = {'item0': ('actie1', 'I', '0', 'eerder', 'titel'),
                'item1': ('actie2', 'A', '1', 'later', 'titel2'),
                'item2': ('actie3', 'X', '2', '', 'titel3')}
        return data[row][column]
    def mock_get_item_text_2(row, column):
        """stub
        """
        print(f'called Page.get_item_text() for `{row}` column {column}`')
        data = {'item0': ('actie1', 'I', 'new', 'eens', 'onderwerp1', 'titel1'),
                'item1': ('actie2', 'A', 'old', 'ooit', 'onderwerp2', 'titel2'),
                'item2': ('actie3', 'X', 'old', '', 'onderwerp3', 'titel3')}
        return data[row][column]
    def mock_get_field_text(fieldname):
        """stub
        """
        return fieldname + '_text'
    def mock_get_textarea_contents():
        """stub
        """
        return 'textarea_contents'
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    # monkeypatch.setattr(testee.MainWindow, 'xxx', mock_xxx)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.filename = 'Filename'
    testobj.book.pages = [MockPageGui()] * 7
    assert capsys.readouterr().out == 'called PageGui.__init__() with args () {}\n'
    testobj.book.tabs = {0: '0 nul', 1: '1 een', 2: '2 twee', 3: '3 drie', 4: '4 vier', 5: '5 vijf',
                         6: '6 zes'}
    testobj.book.cats = {0: ['this', 'I'], 1: ['that', 'A']}
    testobj.book.stats = {0: ['new', 0], 1: ['old', 1]}
    testobj.book.pagedata = types.SimpleNamespace(id='this', titel='action')

    testobj.book.current_tab = 0
    testobj.use_separate_subject = False
    monkeypatch.setattr(testobj.book.pages[0], 'get_items', mock_get_items)
    monkeypatch.setattr(testobj.book.pages[0], 'get_item_text', mock_get_item_text)
    testobj.print_scherm()
    assert testobj.printdict == {'actie': [],
                                 'events': [],
                                 'lijst': [('actie1', 'titel', 'this', '',
                                            'status: 0, laatst behandeld op eerder'),
                                           ('actie2', 'titel2', 'that', '',
                                            'status: 1, laatst behandeld op later'),
                                           ('actie3', 'titel3', 'X', '', 'status: 2')],
                                 'sections': [], }
    assert testobj.hdr == 'Overzicht acties uit Filename'
    assert capsys.readouterr().out == ('called Page.get_items()\n'
                                       'called Page.get_item_text() for `item0` column 0`\n'
                                       'called Page.get_item_text() for `item0` column 1`\n'
                                       'called Page.get_item_text() for `item0` column 2`\n'
                                       'called Page.get_item_text() for `item0` column 3`\n'
                                       'called Page.get_item_text() for `item0` column 4`\n'
                                       'called Page.get_item_text() for `item1` column 0`\n'
                                       'called Page.get_item_text() for `item1` column 1`\n'
                                       'called Page.get_item_text() for `item1` column 2`\n'
                                       'called Page.get_item_text() for `item1` column 3`\n'
                                       'called Page.get_item_text() for `item1` column 4`\n'
                                       'called Page.get_item_text() for `item2` column 0`\n'
                                       'called Page.get_item_text() for `item2` column 1`\n'
                                       'called Page.get_item_text() for `item2` column 2`\n'
                                       'called Page.get_item_text() for `item2` column 3`\n'
                                       'called Page.get_item_text() for `item2` column 4`\n'
                                       'called MainGui.preview()\n')
    testobj.use_separate_subject = True
    monkeypatch.setattr(testobj.book.pages[0], 'get_item_text', mock_get_item_text_2)
    testobj.print_scherm()
    assert testobj.printdict == {'actie': [],
                                 'events': [],
                                 'lijst': [('actie1 - onderwerp1', 'titel1', 'this', '',
                                            'status: new op eens'),
                                           ('actie2 - onderwerp2', 'titel2', 'that', '',
                                            'status: old, laatst behandeld op ooit'),
                                           ('actie3 - onderwerp3', 'titel3', 'X', '', 'status: old')],
                                 'sections': [], }
    assert testobj.hdr == 'Overzicht acties uit Filename'
    assert capsys.readouterr().out == ('called Page.get_items()\n'
                                       'called Page.get_item_text() for `item0` column 0`\n'
                                       'called Page.get_item_text() for `item0` column 1`\n'
                                       'called Page.get_item_text() for `item0` column 2`\n'
                                       'called Page.get_item_text() for `item0` column 3`\n'
                                       'called Page.get_item_text() for `item0` column 4`\n'
                                       'called Page.get_item_text() for `item0` column 5`\n'
                                       'called Page.get_item_text() for `item1` column 0`\n'
                                       'called Page.get_item_text() for `item1` column 1`\n'
                                       'called Page.get_item_text() for `item1` column 2`\n'
                                       'called Page.get_item_text() for `item1` column 3`\n'
                                       'called Page.get_item_text() for `item1` column 4`\n'
                                       'called Page.get_item_text() for `item1` column 5`\n'
                                       'called Page.get_item_text() for `item2` column 0`\n'
                                       'called Page.get_item_text() for `item2` column 1`\n'
                                       'called Page.get_item_text() for `item2` column 2`\n'
                                       'called Page.get_item_text() for `item2` column 3`\n'
                                       'called Page.get_item_text() for `item2` column 4`\n'
                                       'called Page.get_item_text() for `item2` column 5`\n'
                                       'called MainGui.preview()\n')

    testobj.book.current_tab = 1
    monkeypatch.setattr(testobj.book.pages[1], 'get_field_text', mock_get_field_text)
    testobj.print_scherm()
    assert testobj.printdict == {'actie': 'actie_text',
                                 'datum': 'datum_text',
                                 'oms': 'oms_text',
                                 'tekst': 'tekst_text',
                                 'soort': 'soort_text',
                                 'status': 'status_text',
                                 'events': [],
                                 'lijst': [],
                                 'sections': []}
    assert testobj.hdr == 'Informatie over actie actie_text: samenvatting'
    assert capsys.readouterr().out == 'called MainGui.preview()\n'

    testobj.book.current_tab = 2
    monkeypatch.setattr(testobj.book.pages[2], 'get_textarea_contents', mock_get_textarea_contents)
    testobj.print_scherm()
    assert testobj.printdict == {'sections': [('twee', 'textarea_contents')],
                                 'events': [],
                                 'lijst': [],
                                 'actie': []}
    assert testobj.hdr == 'Actie: this action'
    assert capsys.readouterr().out == 'called MainGui.preview()\n'

    testobj.book.current_tab = 5
    testobj.print_scherm()
    assert testobj.printdict == {'sections': [('vijf', 'textarea_contents')],
                                 'events': [],
                                 'lijst': [],
                                 'actie': []}
    assert testobj.hdr == 'Actie: this action'
    assert capsys.readouterr().out == 'called MainGui.preview()\n'

    testobj.book.current_tab = 6
    testobj.book.pages[6].event_list = ['01-01-2001 01:01:01', '02-02-2002 02:02:02T12345']
    testobj.book.pages[6].event_data = ['event_text', 'another_event']
    testobj.print_scherm()
    assert testobj.printdict == {'events': [('01-01-2001 01:01:01', 'event_text'),
                                            ('02-02-2002 02:02:02', 'another_event')],
                                 'actie': [],
                                 'lijst': [],
                                 'sections': []}
    assert testobj.hdr == 'Actie: this action'
    assert capsys.readouterr().out == 'called MainGui.preview()\n'


def test_mainwindow_print_actie(monkeypatch, capsys):
    """unittest for main.MainWindow.print_actie
    """
    def mock_show_message(win, message):
        """stub
        """
        print(f'called gui.show_message(`{message}`)')
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.book.pagedata = None
    testobj.print_actie()
    assert capsys.readouterr().out == ('called gui.show_message(`Wel eerst een actie kiezen'
                                       ' om te printen`)\n')
    testobj.book.pagedata = types.SimpleNamespace(id='this', datum='today',
                                                  titel='xxx - yyy', melding='zzzzzzzzzzzzzzz',
                                                  events=[('time1', 'text1'), ('time2', 'text2')])
    testobj.book.cats = {}
    testobj.book.stats = {}
    testobj.use_text_panels = False
    testobj.print_actie()
    assert testobj.printdict == {'actie': 'this', 'datum': 'today',
                                 'events': [('time1', 'text1'), ('time2', 'text2')],
                                 'lijst': [], 'oms': 'xxx',
                                 'sections': [['Probleem/wens', 'zzzzzzzzzzzzzzz']],
                                 'soort': '(onbekende soort)', 'status': '(onbekende status)',
                                 'tekst': 'yyy'}
    assert testobj.hdr == 'Actie: this xxx - yyy'
    assert capsys.readouterr().out == 'called MainGui.preview()\n'

    testobj.book.tabs = {0: '0 nul', 1: '1 een', 2: '2 twee', 3: '3 drie', 4: '4 vier', 5: '5 vijf',
                         6: '6 zes'}
    testobj.book.cats = {0: ['this', 'I'], 1: ['that', 'A']}
    testobj.book.stats = {0: ['new', 0], 1: ['old', 1]}
    testobj.use_text_panels = True
    testobj.book.pagedata = types.SimpleNamespace(id='this', datum='today', soort='I', status=0,
                                                  titel='xxx: yyy', melding='zzzzzzzzzzzzzzz',
                                                  oorzaak='aaaa', oplossing='bbbb', vervolg='ccc',
                                                  events=[('time1', 'text1'), ('time2', 'text2')])
    testobj.print_actie()
    assert testobj.printdict == {'actie': 'this', 'datum': 'today',
                                 'events': [('time1', 'text1'), ('time2', 'text2')],
                                 'lijst': [], 'oms': 'xxx',
                                 'sections': [['twee', 'zzzzzzzzzzzzzzz'], ['drie', 'aaaa'],
                                              ['vier', 'bbbb'], ['vijf', 'ccc']],
                                 'soort': 'this', 'status': 'new', 'tekst': 'yyy'}
    assert testobj.hdr == 'Actie: this xxx: yyy'
    assert capsys.readouterr().out == 'called MainGui.preview()\n'

    testobj.book.pagedata = types.SimpleNamespace(id='this', datum='today', soort='', status='0',
                                                  titel='gargl bargl', melding='',
                                                  oorzaak='', oplossing='', vervolg='',
                                                  events=[('time1', 'text1'), ('time2', 'text2')])
    testobj.book.cats = {}
    testobj.book.stats = {}
    testobj.print_actie()
    assert testobj.printdict == {'actie': 'this', 'datum': 'today',
                                 'events': [('time1', 'text1'), ('time2', 'text2')],
                                 'lijst': [], 'oms': '',
                                 'sections': [['twee', '(nog niet beschreven)'],
                                              ['drie', '(nog niet beschreven)'],
                                              ['vier', '(nog niet beschreven)']],
                                 'soort': '(onbekende soort)', 'status': '(onbekende status)',
                                 'tekst': 'gargl bargl'}
    assert testobj.hdr == 'Actie: this gargl bargl'
    assert capsys.readouterr().out == 'called MainGui.preview()\n'


def test_mainwindow_exit_app(monkeypatch, capsys):
    """unittest for main.MainWindow.exit_app
    """
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.book.current_tab = -1
    testobj.exit_app()
    assert capsys.readouterr().out == 'called MainGui.exit()\n'
    testobj.book.current_tab = 0
    testobj.book.pages = [types.SimpleNamespace(leavep=lambda *x: False)]
    testobj.exit_app()
    assert capsys.readouterr().out == ''
    testobj.book.current_tab = 0
    testobj.book.pages = [types.SimpleNamespace(leavep=lambda *x: True)]
    testobj.exit_app()
    assert capsys.readouterr().out == 'called MainGui.exit()\n'


#        "called dmls.SortOptions() with args ('fnaam',)\n")
def test_mainwindow_sign_in(monkeypatch, capsys):
    """unittest for main.MainWindow.sign_in
    """
    def mock_show_message(win, msg):
        """stub
        """
        print(f'called gui.show_message(`{msg}`)')
    def mock_show_dialog(*args):
        """stub
        """
        print('called gui.show_dialog() (for login dialog)')
    def mock_show_dialog_ok(*args):
        """stub
        """
        print('called gui.show_dialog() (for login dialog)')
        return True
    def mock_rereadlist(*args):
        """stub
        """
        print('called MainWindow.book.rereadlist()')
    class MockOptions:
        "stub"
        def __init__(self, filename):
            print(f'called dmls.SortOptions.__init__ with arg {filename}')
    counter = 0
    def mock_validate_user(*args):
        """stub
        """
        nonlocal counter
        print('called dmls.validate_user()')
        counter += 1
        if counter == 1:
            return '', False, False
        elif counter == 3:
            return 'me', True, False
        elif counter == 4:
            return 'me', False, True
        elif counter == 5:
            return 'me', False, False
        return 'me', True, True
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    monkeypatch.setattr(testee.dmls, 'validate_user', lambda *x: ('', False, False))
    testobj.sign_in()
    assert capsys.readouterr().out == 'called gui.show_dialog() (for login dialog)\n'

    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog_ok)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
    monkeypatch.setattr(testee.dmls, 'SortOptions', MockOptions)
    monkeypatch.setattr(testee.dmls, 'validate_user', mock_validate_user)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.filename = 'xxx'
    testobj.gui.dialog_data = 'stuff'
    testobj.book.rereadlist = mock_rereadlist
    testobj.book.pages = [types.SimpleNamespace()]
    testobj.sign_in()
    assert (testobj.user, testobj.is_user, testobj.is_admin) == ('me', True, True)
    assert isinstance(testobj.book.pages[0].saved_sortopts, testee.dmls.SortOptions)
    assert capsys.readouterr().out == ('called gui.show_dialog() (for login dialog)\n'
                                       'called dmls.validate_user()\n'
                                       'called gui.show_message(`Login failed`)\n'
                                       'called gui.show_dialog() (for login dialog)\n'
                                       'called dmls.validate_user()\n'
                                       'called gui.show_message(`Login accepted`)\n'
                                       'called MainGui.enable_settingsmenu()\n'
                                       'called dmls.SortOptions.__init__ with arg xxx\n'
                                       'called MainGui.refresh_page()\n')
    testobj.book.pages = [types.SimpleNamespace()]
    testobj.sign_in()
    assert (testobj.user, testobj.is_user, testobj.is_admin) == ('me', True, False)
    assert isinstance(testobj.book.pages[0].saved_sortopts, testee.dmls.SortOptions)
    assert capsys.readouterr().out == ('called gui.show_dialog() (for login dialog)\n'
                                       'called dmls.validate_user()\n'
                                       'called gui.show_message(`Login accepted`)\n'
                                       'called MainGui.enable_settingsmenu()\n'
                                       'called dmls.SortOptions.__init__ with arg xxx\n'
                                       'called MainGui.refresh_page()\n')
    testobj.book.pages = [types.SimpleNamespace()]
    testobj.sign_in()
    assert (testobj.user, testobj.is_user, testobj.is_admin) == ('me', False, True)
    assert isinstance(testobj.book.pages[0].saved_sortopts, testee.dmls.SortOptions)
    assert capsys.readouterr().out == ('called gui.show_dialog() (for login dialog)\n'
                                       'called dmls.validate_user()\n'
                                       'called gui.show_message(`Login accepted`)\n'
                                       'called MainGui.enable_settingsmenu()\n'
                                       'called dmls.SortOptions.__init__ with arg xxx\n'
                                       'called MainGui.refresh_page()\n')
    testobj.book.pages = [types.SimpleNamespace()]
    testobj.sign_in()
    assert (testobj.user, testobj.is_user, testobj.is_admin) == ('me', False, False)
    assert testobj.book.pages[0].saved_sortopts is None
    assert capsys.readouterr().out == ('called gui.show_dialog() (for login dialog)\n'
                                       'called dmls.validate_user()\n'
                                       'called gui.show_message(`Login accepted`)\n'
                                       'called MainGui.enable_settingsmenu()\n'
                                       'called MainGui.refresh_page()\n')


def test_mainwindow_tab_settings(monkeypatch, capsys):
    """unittest for main.MainWindow.tab_settings
    """
    def mock_show_dialog(win, cls, args=None):
        """stub
        """
        print(f'called gui.show_dialog() with args `{cls}` `{args}`')
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog)
    monkeypatch.setattr(testee.gui, 'SettOptionsDialog', 'settoptionsdialog')
    monkeypatch.setattr(testee, 'TabOptions', 'taboptions')
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    # breakpoint()
    testobj.tab_settings()
    assert capsys.readouterr().out == ('called gui.show_dialog() with args `settoptionsdialog`'
                                       " `('taboptions', 'Wijzigen tab titels')`\n")


def test_mainwindow_stat_settings(monkeypatch, capsys):
    """unittest for main.MainWindow.stat_settings
    """
    def mock_show_dialog(win, cls, args=None):
        """stub
        """
        print(f'called gui.show_dialog() with args `{cls}` `{args}`')
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog)
    monkeypatch.setattr(testee.gui, 'SettOptionsDialog', 'settoptionsdialog')
    monkeypatch.setattr(testee, 'StatOptions', 'statoptions')
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    # breakpoint()
    testobj.stat_settings()
    assert capsys.readouterr().out == ('called gui.show_dialog() with args `settoptionsdialog`'
                                       " `('statoptions', 'Wijzigen statussen')`\n")


def test_mainwindow_cat_settings(monkeypatch, capsys):
    """unittest for main.MainWindow.cat_settings
    """
    def mock_show_dialog(win, cls, args=None):
        """stub
        """
        print(f'called gui.show_dialog() with args `{cls}` `{args}`')
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog)
    monkeypatch.setattr(testee.gui, 'SettOptionsDialog', 'settoptionsdialog')
    monkeypatch.setattr(testee, 'CatOptions', 'catoptions')
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    # breakpoint()
    testobj.cat_settings()
    assert capsys.readouterr().out == ('called gui.show_dialog() with args `settoptionsdialog`'
                                       " `('catoptions', 'Wijzigen categorieën')`\n")


def test_mainwindow_font_settings(monkeypatch, capsys):
    """unittest for main.MainWindow.font_settings
    """
    def mock_show_message(self, mld):
        """stub
        """
        print(f'called MainWindow.show_message(`{mld}`)')
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.font_settings()
    assert capsys.readouterr().out == 'called MainWindow.show_message(`Sorry, werkt nog niet`)\n'


def test_mainwindow_colour_settings(monkeypatch, capsys):
    """unittest for main.MainWindow.colour_settings
    """
    def mock_show_message(self, mld):
        """stub
        """
        print(f'called MainWindow.show_message(`{mld}`)')
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.colour_settings()
    assert capsys.readouterr().out == 'called MainWindow.show_message(`Sorry, werkt nog niet`)\n'


def test_mainwindow_hotkey_settings(monkeypatch, capsys):
    """unittest for main.MainWindow.hotkey_settings
    """
    def mock_show_message(self, mld):
        """stub
        """
        print(f'called MainWindow.show_message(`{mld}`)')
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.hotkey_settings()
    assert capsys.readouterr().out == 'called MainWindow.show_message(`Sorry, werkt nog niet`)\n'


def test_mainwindow_about_help(monkeypatch, capsys):
    """unittest for main.MainWindow.about_help
    """
    def mock_show_message(win, msg):
        """stub
        """
        print('called gui.show_message()')
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.about_help()
    assert capsys.readouterr().out == 'called gui.show_message()\n'


def test_mainwindow_hotkey_help(monkeypatch, capsys):
    """unittest for main.MainWindow.hotkey_help
    """
    def mock_show_message(win, msg):
        """stub
        """
        print(f'called gui.show_message(`{msg}`)')
    helptext_dl1 = ("=== Albert's actiebox ===\n\nKeyboard shortcuts:\n"
                    "    Alt left/right:                verder - terug\n"
                    "    Alt-0 t/m Alt-6:               naar betreffende pagina\n"
                    "    Alt-O op tab 1:                S_o_rteren\n"
                    "    Alt-I op tab 1:                F_i_lteren\n"
                    "    Alt-G of Enter op tab 1:       _G_a naar aangegeven actie\n"
                    "    Alt-N op elke tab:             _N_ieuwe actie opvoeren\n")
    helptext_multif = ("    Ctrl-N:                       maak een _n_ieuw actiebestand\n"
                       "    Ctrl-O:                       _o_pen een (ander) actiebestand\n")
    helptext_multip = ("    Ctrl-N:                       start een _n_ieuw project\n"
                       "    Ctrl-O:                       selecteer een (ander) pr_o_ject\n")
    helptext_dl2 = ("    Ctrl-P:                        _p_rinten (scherm of actie)\n"
                    "    Shift-Ctrl-P:                  print scherm\n"
                    "    Alt-Ctrl-P:                    print actie\n"
                    "    Ctrl-Q:                        _q_uit actiebox\n"
                    "    Ctrl-H:                        _h_elp (dit scherm)\n"
                    "    Ctrl-S:                        gegevens in het scherm op_s_laan\n"
                    "    Ctrl-G:                        oplaan en _g_a door naar volgende tab\n"
                    "    Ctrl-Z in een tekstveld:       undo\n"
                    "    Shift-Ctrl-Z in een tekstveld: redo\n"
                    "    Alt-Ctrl-Z overal:             wijzigingen ongedaan maken\n"
                    "    Shift-Ctrl-N op laatste tab:   nieuwe regel opvoeren\n"
                    "    Ctrl-up/down op laatste tab:   omhoog/omlaag in list")
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.helptext = 'random'
    testobj.hotkey_help()
    assert capsys.readouterr().out == 'called gui.show_message(`random`)\n'
    testobj.helptext = ''
    testobj.multiple_files = True
    testobj.multiple_projects = False
    testobj.hotkey_help()
    text = helptext_dl1 + helptext_multif + helptext_dl2
    assert capsys.readouterr().out == f'called gui.show_message(`{text}`)\n'
    testobj.helptext = ''
    testobj.multiple_files = False
    testobj.multiple_projects = True
    testobj.hotkey_help()
    text = helptext_dl1 + helptext_multip + helptext_dl2
    assert capsys.readouterr().out == f'called gui.show_message(`{text}`)\n'
    testobj.helptext = ''
    testobj.multiple_files = False
    testobj.multiple_projects = False
    testobj.hotkey_help()
    text = helptext_dl1 + helptext_dl2
    assert capsys.readouterr().out == f'called gui.show_message(`{text}`)\n'


def test_mainwindow_silly_menu(monkeypatch, capsys):
    """unittest for main.MainWindow.silly_menu
    """
    def mock_show_message(win, msg):
        """stub
        """
        print('called gui.show_message()')
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.silly_menu()
    assert capsys.readouterr().out == 'called gui.show_message()\n'


def test_mainwindow_startfile(monkeypatch, capsys):
    """unittest for main.MainWindow.startfile
    """
    def mock_show_message(win, message):
        """stub
        """
        print(f'called gui.show_message(`{message}`)')
    def mock_lees_settings(self):
        """stub
        """
        print('called MainWindow.lees_settings()')
    def mock_clear_selection(*args):
        """stub
        """
        print('called Page.clear_selection()')
    def mock_vulp(*args):
        """stub
        """
        print('called Page.vulp()')
    def mock_vul_combos(*args):
        """stub
        """
        print('called Page.vul_combos()')
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.MainWindow, 'lees_settings', mock_lees_settings)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'

    testobj.multiple_files = True
    testobj.multiple_project = False
    testobj.dirname = testee.pathlib.Path('path/to')
    testobj.filename = 'file.xml'
    testobj.is_newfile = True
    monkeypatch.setattr(testee.dmlx, 'checkfile', lambda *x: 'checkfile() failed')
    monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
    assert testobj.startfile() == 'checkfile() failed'
    assert capsys.readouterr().out == 'called gui.show_message(`checkfile() failed`)\n'

    testobj.multiple_files = True
    testobj.multiple_projects = False
    monkeypatch.setattr(testee.dmlx, 'checkfile', lambda *x: '')
    testobj.book.tabs = ['tab', 'titles']
    testobj.book.pages = [types.SimpleNamespace(clear_selection=mock_clear_selection, vulp=mock_vulp),
                          types.SimpleNamespace(vul_combos=mock_vul_combos)]
    testobj.book.current_tab = 0
    assert testobj.startfile() == ''
    assert str(testobj.book.fnaam) == 'path/to/file.xml'
    assert testobj.title == 'file.xml'
    assert testobj.book.rereadlist
    assert testobj.book.sorter is None
    assert testobj.book.changed_item
    assert capsys.readouterr().out == ("called MainWindow.lees_settings()\n"
                                       "called MainGui.set_tab_titles([['tab', 'titles']]\n"
                                       "called Page.clear_selection()\n"
                                       "called Page.vul_combos()\n"
                                       "called Page.vulp()\n")
    testobj.multiple_files = False
    testobj.multiple_projects = True
    testobj.filename = 'project'
    testobj.projnames = (('x', 'y', 'z'), ('Project', 'Project', 'Demo Project'))
    testobj.book.current_tab = 1
    assert testobj.startfile() == ''
    assert testobj.book.fnaam == 'project'
    assert testobj.title == 'Project'
    assert testobj.book.rereadlist
    assert testobj.book.sorter is None
    assert testobj.book.changed_item
    assert capsys.readouterr().out == ("called MainWindow.lees_settings()\n"
                                       "called MainGui.set_tab_titles([['tab', 'titles']]\n"
                                       "called Page.clear_selection()\n"
                                       "called Page.vul_combos()\n"
                                       "called MainGui.select_first_tab()\n")
    testobj.multiple_files = False
    testobj.multiple_projects = False
    testobj.filename = 'default'
    assert testobj.startfile() == ''
    assert testobj.book.fnaam == 'default'
    assert testobj.title == ''
    assert testobj.book.rereadlist
    assert testobj.book.sorter is None
    assert testobj.book.changed_item
    assert capsys.readouterr().out == ("called MainWindow.lees_settings()\n"
                                       "called MainGui.set_tab_titles([['tab', 'titles']]\n"
                                       "called Page.clear_selection()\n"
                                       "called Page.vul_combos()\n"
                                       "called MainGui.select_first_tab()\n")


def test_mainwindow_lees_settings(monkeypatch, capsys):
    """unittest for main.MainWindow.lees_settings
    """
    class MockSettings:
        """stub
        """
        def __init__(self, fnaam):
            self.imagecount = 1
            self.startitem = '0'
            self.stat = {1: ('statitem', '1')}
            self.cat = {2: ('catitem', '2')}
            self.kop = {'3': ('kopitem', '3')}
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.datatype = 'x'
    testobj.book.fnaam = 'y'
    monkeypatch.setattr(testee.shared, 'Settings', {'x': MockSettings})
    testobj.lees_settings()
    assert testobj.imagecount == 1
    assert testobj.startitem == '0'
    assert testobj.book.stats == {1: ['statitem', 1]}
    assert testobj.book.cats == {2: ['catitem', 2]}
    assert testobj.book.tabs == {3: '3 Kopitem'}


def test_mainwindow_save_settings(monkeypatch, capsys):
    """unittest for main.MainWindow.save_settings
    """
    class MockSettings:
        """stub
        """
        def __init__(self, fnaam):
            self.imagecount = 1
            self.startitem = '0'
            self.stat = {1: ('statitem', '1')}
            self.cat = {2: ('catitem', '2')}
            self.kop = {'3': ('kopitem', '3')}
        def write(self):
            """stub
            """
            print('called Settings.write()')
    def mock_set_page_title(self, *args):
        """stub
        """
        print('called MainGui.set_page_title() with args', args)
    def mock_vul_combos(*args):
        """stub
        """
        print('called MainWindow.book.vul_combos()')
    def mock_show_message(win, message):
        """stub
        """
        print(f'called gui.show_message(`{message}`')
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.gui.MainGui, 'set_page_title', mock_set_page_title)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    monkeypatch.setattr(testee.shared, 'Settings', {'x': MockSettings})
    testobj.datatype = 'x'
    testobj.book.fnaam = 'y'
    testobj.book.pages = ('page0', types.SimpleNamespace(vul_combos=mock_vul_combos))
    testobj.save_settings('tab', {'0': ('newkop', '0')})
    assert testobj.book.tabs == {0: '0 Newkop'}
    assert capsys.readouterr().out == ('called Settings.write()\n'
                                       "called MainGui.set_page_title() with args (0, 'newkop')\n"
                                       'called MainWindow.book.vul_combos()\n')

    testobj.save_settings('stat', {0: ('newstat', '0')})
    assert testobj.book.stats == {0: ['newstat', 0]}
    assert capsys.readouterr().out == ('called Settings.write()\n'
                                       'called MainWindow.book.vul_combos()\n')

    testobj.save_settings('cat', {0: ('newcat', '0')})
    assert testobj.book.cats == {0: ['newcat', 0]}
    assert capsys.readouterr().out == ('called Settings.write()\n'
                                       'called MainWindow.book.vul_combos()\n')
    monkeypatch.setattr(MockSettings, 'write', lambda *x: ('error', 'message'))
    monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
    testobj.save_settings('stat', 'x')
    assert capsys.readouterr().out == ('called gui.show_message(`Kan status message niet verwijderen,'
                                       ' wordt nog gebruikt in één of meer acties`\n')
    testobj.save_settings('cat', 'x')
    assert capsys.readouterr().out == ('called gui.show_message(`Kan soort message niet verwijderen,'
                                       ' wordt nog gebruikt in één of meer acties`\n')


def test_mainwindow_save_startitem_on_exit(monkeypatch, capsys):
    """unittest for main.MainWindow.save_startitem_on_exit
    """
    class MockSettings:
        """stub
        """
        def __init__(self, fnaam):
            self.imagecount = 1
            self.startitem = '2'
            self.stat = {1: ('statitem', '1')}
            self.cat = {2: ('catitem', '2')}
            self.kop = {'3': ('kopitem', '3')}
        def write(self):
            """stub
            """
            print('called Settings.write()')
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    monkeypatch.setattr(testee.shared, 'Settings', {'x': MockSettings})
    testobj.datatype = 'x'
    testobj.book.fnaam = 'y'
    testobj.book.pagedata = {}
    testobj.save_startitem_on_exit()
    assert capsys.readouterr().out == ''

    testobj.book.pagedata = types.SimpleNamespace(id='1')
    testobj.save_startitem_on_exit()
    assert capsys.readouterr().out == 'called Settings.write()\n'

    testobj.book.pagedata = {}
    testobj.save_startitem_on_exit()
    assert capsys.readouterr().out == ''
    testobj.book.pagedata = types.SimpleNamespace(id='1')
    testobj.save_startitem_on_exit()
    assert capsys.readouterr().out == 'called Settings.write()\n'


def test_mainwindow_goto_next(monkeypatch, capsys):
    """unittest for main.MainWindow.goto_next
    """
    def mock_goto_next(*args):
        """stub
        """
        print('called Page.goto_next() with args', args)
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.Page, 'goto_next', mock_goto_next)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.book.pages = ['page0', 'page1']
    testobj.book.current_tab = 1
    testobj.goto_next()
    assert capsys.readouterr().out == "called Page.goto_next() with args ('page1',)\n"


def test_mainwindow_goto_prev(monkeypatch, capsys):
    """unittest for main.MainWindow.goto_prev
    """
    def mock_goto_prev(*args):
        """stub
        """
        print('called Page.goto_prev() with args', args)
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.Page, 'goto_prev', mock_goto_prev)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.book.pages = ['page0', 'page1']
    testobj.book.current_tab = 1
    testobj.goto_prev()
    assert capsys.readouterr().out == "called Page.goto_prev() with args ('page1',)\n"


def test_mainwindow_goto_page(monkeypatch, capsys):
    """unittest for main.MainWindow.goto_page
    """
    def mock_goto_page(*args):
        """stub
        """
        print('called Page.goto_page() with args', args)
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    monkeypatch.setattr(testee.Page, 'goto_page', mock_goto_page)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.book.pages = ['page0', 'page1']
    testobj.book.current_tab = 0
    testobj.goto_page(1)
    assert capsys.readouterr().out == "called Page.goto_page() with args ('page0', 1)\n"


def test_mainwindow_enable_settingsmenu(monkeypatch, capsys):
    """unittest for main.MainWindow.enable_settingsmenu
    """
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.enable_settingsmenu()
    assert capsys.readouterr().out == 'called MainGui.enable_settingsmenu()\n'


def test_mainwindow_set_windowtitle(monkeypatch, capsys):
    """unittest for main.MainWindow.set_windowtitle
    """
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.set_windowtitle('some_text')
    assert capsys.readouterr().out == "called MainGui.set_window_title() with args ('some_text',)\n"


def test_mainwindow_set_statusmessage(monkeypatch, capsys):
    """unittest for main.MainWindow.set_statusmessage
    """
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.work_with_user = True
    testobj.user = types.SimpleNamespace(username='me')
    testobj.set_statusmessage('hello')
    assert capsys.readouterr().out == ('called MainGui.set_statusmessage(`hello`)\n'
                                       'called MainGui.show_username(`Aangemeld als me`)\n')
    testobj.user = None
    testobj.set_statusmessage('message')
    assert capsys.readouterr().out == ('called MainGui.set_statusmessage(`message`)\n'
                                       'called MainGui.show_username(`Niet aangemeld`)\n')
    testobj.work_with_user = False
    testobj.book.pagehelp = ['help for page 0', 'help for page 1']
    testobj.book.data = ['0', '1', '2', '3']
    testobj.book.current_tab = 0
    testobj.set_statusmessage()
    assert capsys.readouterr().out == (
            'called MainGui.set_statusmessage(`help for page 0 - 4 items`)\n')
    testobj.book.current_tab = 1
    testobj.set_statusmessage()
    assert capsys.readouterr().out == 'called MainGui.set_statusmessage(`help for page 1`)\n'


def test_mainwindow_get_focus_widget_for_tab(monkeypatch, capsys):
    """unittest for main.MainWindow.get_focus_widget_for_tab
    """
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    page0 = MockPage()
    assert capsys.readouterr().out == ('called Page.__init__() with args () {}\n'
                                       'called PageGui.__init__() with args () {}\n')
    page0.gui = types.SimpleNamespace(p0list='p0list')
    page1 = MockPage()
    assert capsys.readouterr().out == ('called Page.__init__() with args () {}\n'
                                       'called PageGui.__init__() with args () {}\n')
    page1.gui = types.SimpleNamespace(proc_entry='proc_entry')
    page2 = MockPage()
    assert capsys.readouterr().out == ('called Page.__init__() with args () {}\n'
                                       'called PageGui.__init__() with args () {}\n')
    page2.gui = types.SimpleNamespace(text1='text_page2')
    page3 = MockPage()
    assert capsys.readouterr().out == ('called Page.__init__() with args () {}\n'
                                       'called PageGui.__init__() with args () {}\n')
    page3.gui = types.SimpleNamespace(text1='text_page3')
    page4 = MockPage()
    assert capsys.readouterr().out == ('called Page.__init__() with args () {}\n'
                                       'called PageGui.__init__() with args () {}\n')
    page4.gui = types.SimpleNamespace(text1='text_page4')
    page5 = MockPage()
    assert capsys.readouterr().out == ('called Page.__init__() with args () {}\n'
                                       'called PageGui.__init__() with args () {}\n')
    page5.gui = types.SimpleNamespace(text1='text_page5')
    page6 = MockPage()
    assert capsys.readouterr().out == ('called Page.__init__() with args () {}\n'
                                       'called PageGui.__init__() with args () {}\n')
    page6.gui = types.SimpleNamespace(progress_list='progress_list')
    testobj.book.pages = [page0, page1, page2, page3, page4, page5, page6]
    assert testobj.get_focus_widget_for_tab(0) == 'p0list'
    assert testobj.get_focus_widget_for_tab(1) == 'proc_entry'
    assert testobj.get_focus_widget_for_tab(2) == 'text_page2'
    assert testobj.get_focus_widget_for_tab(3) == 'text_page3'
    assert testobj.get_focus_widget_for_tab(4) == 'text_page4'
    assert testobj.get_focus_widget_for_tab(5) == 'text_page5'
    assert testobj.get_focus_widget_for_tab(6) == 'progress_list'


def test_mainwindow_enable_all_book_tabs(monkeypatch, capsys):
    """unittest for main.MainWindow.enable_all_book_tabs
    """
    monkeypatch.setattr(testee.MainWindow, '__init__', mock_init_mainwindow)
    testobj = testee.MainWindow()
    assert capsys.readouterr().out == 'called MainGui.__init__()\n'
    testobj.enable_all_book_tabs(True)
    assert capsys.readouterr().out == ("called MainGui.enable_book_tabs() with args (True,)"
                                       " {'tabfrom': 1}\n")
