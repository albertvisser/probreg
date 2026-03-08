"""unittests for ./probreg/main.py
"""
import types
import pytest
from probreg import main as testee


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
    def set_tabfocus(self, number):
        """stub
        """
        print(f'called MainWindow.set_tabfocus({number})')
    def enable_all_book_tabs(self, value):
        """stub
        """
        print(f'call MainWindow.enable_all_book_tabs({value})')
    def enable_book_navigation(self, *args, **kwargs):
        """stub
        """
        print('called MainWindow.enable_book_navigation() with args', args, kwargs)
    def enable_all_other_tabs(self, value):
        """stub
        """
        print(f'called MainWindow.enable_all_other_tabs() with arg `{value}`')


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
    def create_actions(self, actiondefs):
        """stub
        """
        print(f'called MainGui.create_actions with arg {actiondefs}')
    def enable_settingsmenu(self):
        """stub
        """
        print('called MainGui.enable_settingsmenu()')
    def set_page(self, *args):
        """stub
        """
        print('called MainGui.set_page with args', args)
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
        print(f'called MainGui.set_tab_titles({titles}')
    def set_page_title(self, *args):
        """stub
        """
        print('called MainGui.set_page_title() with args', args)
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
    def add_buttons(self, *args):
        """stub
        """
        print('called PageGui.add_buttons with args', args)
        if args:
            return [x[0] for x in args[0]]
    def add_combobox_line(self, *args):
        print('called PageGui.add_combobox_line with args', args)
        return args[0]
    def add_combobox_choice(self, *args):
        """stub
        """
        print('called PageGui.add_combobox_choice with args', args)
    def add_keybind(self, *args, **kwargs):
        print('called PageGui.add_keybind with args', args, kwargs)
    def add_first_listitem(self, *args):
        """stub
        """
        print('called PageGui.add_first_listitem with args', args)
    def add_item_to_list(self, *args):
        """stub
        """
        print('called PageGui.add_item_to_list() with args', args)
    def add_list(self, *args):
        """stub
        """
        print('called PageGui.add_list with args', args)
        return types.SimpleNamespace()
    def add_listitem(self, *args):
        """stub
        """
        print('called PageGui.add_listitem with args', args)
    def add_pushbutton_line(self, *args):
        print('called PageGui.add_pushbutton_line with args', args)
        return args[0], args[1]
    def add_textbox_line(self, *args):
        print('called PageGui.add_textbox_line with args', args)
        return args[0]
    def add_textentry_line(self, *args):
        print('called PageGui.add_textentry_line with args', args)
        return args[0]
    def clear_combobox(self, *args):
        """stub
        """
        print('called PageGui.clear_combobox with args', args)
    def clear_list(self, *args):
        """stub
        """
        print('called PageGui.clear_list with args', args)
    def clear_textfield(self, *args):
        """stub
        """
        print('called PageGui.clear_textfield with args', args)
    def create_buttons(self, *args):
        """stub
        """
        print('called PageGui.create_buttons with args', args)
        return [x[0] for x in args[0]]
    def create_new_listitem(self, *args):
        """stub
        """
        print('called PageGui.create_new_listitem() with args', args)
    def create_list(self):
        print('called PageGui.create_list')
        return 'list'
    def create_textfield(self, *args):
        print('called PageGui.create_textfield with args', args)
        return 'text1'
    def create_text_field(self, *args):
        """stub
        """
        print('called PageGui.create_text_field with args', args)
        return 'text1'
    def create_toolbar(self, *args):
        """stub
        """
        print('called PageGui.create_toolbar with args', args)
        return 'toolbar'
    def enable_widget(self, *args):
        """stub
        """
        print('called PageGui.enable_widget with args', args)
    def enable_sorting(self, *args):
        """stub
        """
        print('called PageGui.enable_sorting with args', args)
    def enable_toolbar(self, *args):
        """stub
        """
        print('call PageGui.enable_toolbar with args', args)
    def ensure_visible(self, *args):
        """stub
        """
        print('called PageGui.ensure_visible with args', args)
    def finish_display(self):
        print('called PageGui.finish_display')
    def get_choice_data(self, *args):
        """stub
        """
        print('called PageGui.get_choice_data with args', args)
        return args[0], 'x'
    def get_choice_index(self, *args):
        """stub
        """
        print('called PageGui.get_choice_index with args', args)
        return len(args[0])
    def get_first_item(self, *args):
        """stub
        """
        print('called PageGui.get_first_item() with args', args)
        return 'first_item'
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
    def get_item_by_id(self, *args):
        """stub
        """
        print('called PageGui.get_item_by_id() with args', args)
        return 'item_by_id'
    def get_listitem_text(self, in_):
        """stub
        """
        print('called PageGui.get_listitem_text()')
        return in_
    def get_list_row(self):
        """stub
        """
    def get_list_rowcount(self):
        """stub
        """
    def get_selected_action(self, listbox):
        """stub
        """
        print('called PageGui.get_selected_action with arg', listbox)
        return '1'
    def get_text(self, *args):
        """stub
        """
        print(f'called PageGui.get_field_text() with args {args}')
        return 'the text of the item'
    def get_textbox_value(self, *args):
        print('call PageGui.get_textbox_value with args', args)
        return args[0]
    def get_textarea_contents(self, *args):
        """stub
        """
        print('call PageGui.get_textarea_contents with args', args)
        return 'text'
    def get_textfield_contents(self, *args):
        """stub
        """
        print('called PageGui.get_textfield_contents with args', args)
        return 'text'
    def get_textfield_value(self, *args):
        print("called PageGui.get_textfield_value with args", args)
        return args[0]
    def init_fields(self, *args):
        """stub
        """
        print('called PageGui.init_fields()')
    def init_list(self, text):
        """stub
        """
        print(f'called PageGui.init_list() with text `{text}`')
    def init_textfield(self):
        """stub
        """
        print('called PageGui.init_textfield()')
    def is_enabled(self, arg):
        print(f"called PageGui.is_enabled with arg '{arg}'")
        return False
    def move_cursor_to_end(self, *args):
        """stub
        """
        print('call PageGui.move_cursor_to_end with args', args)
    def protect_textfield(self, *args):
        """stub
        """
        print('called PageGui.protect_textfield with args', args)
    def set_button_text(self, *args):
        print('called PageGui.set_button_text with args', args)
    def set_choice(self, *args):
        """stub
        """
        print('called PageGui.set_choice() with args', args)
    def set_focus_to_field(self, field):
        """stub
        """
        print(f'called PageGui.set_focus_to_field({field})')
    def set_item_text(self, *args):
        """stub
        """
        print('called PageGui.set_item_text() with args', args)
    def set_label_value(self, *args):
        print('called PageGui.set_label_value with args', args)
    def set_list_callbacks(self, *args):
        """stub
        """
        print('called PageGui.init_set_list_callbacks with args', args)
    def set_list_row(self, *args):
        """stub
        """
        print('called PageGui.set_list_row with args', args)
    def set_listitem_data(self, *args):
        """stub
        """
        print('called PageGui.set_listitem_data() with args', args)
    def set_listitem_text(self, *args):
        """stub
        """
        print('called PageGui.set_listitem_text() with args', args)
    def set_listitem_values(self, *args):
        """stub
        """
        print('called PageGui.set_listitem_values() with args', args)
    def set_selection(self, *args):
        """stub
        """
        print('called PageGui.set_selection with args', args)
    def set_textarea_contents(self, *args):
        """stub
        """
        print('call PageGui.set_textarea_contents with args', args)
    def set_textbox_value(self, *args):
        print('called PageGui.set_textbox_value with args', args)
    def set_textfield_value(self, *args):
        print('called PageGui.set_textfield_value with args', args)
    def set_text_readonly(self, *args):
        """stub
        """
        print('called PageGui.set_text_readonly with args', args)
    def show_button(self, *args):
        print('called PageGui.show_button with args', args)
    def start_display(self):
        print('called PageGui.start_display')
        return 'sizer'
    # def build_newbuf(self):
    #     """stub
    #     """
    #     print('called PageGui.build_newbuf()')
    #     return 'newbuf'
    def can_saveandgo(self):
        """stub
        """
    def set_archive_button_text(self, text):
        """stub
        """
        print(f'called PageGui.set_archive_button_text(`{text}`)')
    def get_field_text(self, *args):
        """stub
        """
        print(f'called PageGui.get_field_text() with args {args}')
        return 'the text of the item'
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
    def convert_text(self, in_, to='plain'):
        """stub
        """
        print(f'called PageGui.convert_text() with args `{in_}`, to=`{to}`')
        return in_
    # def set_oldbuf(self):
    #     """stub
    #     """
    #     return 'oldbuf'
    def set_text(self, fieldname, text):
        """stub
        """
        print(f'called PageGui.set_text() for field `{fieldname}` text `{text}`')


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


class MockOptionsParent:
    """stub for MainWindow in the role of parent of Options classes
    """
    def __init__(self):
        self.book = types.SimpleNamespace(tabs={1: '1 eerste', 3: '3 derde', 2: '2 tweede'},
                stats={1: ('opgepakt', '1'), 2: ('afgehandeld', '2'), 0: ('gemeld', '0')},
                cats={1: ('probleem', 'P'), 2: ('wens', 'W'), 0: ('Onbekend', ' ')})
    def save_settings(self, *args):
        print("called MainWindow.save_settings() with args", args)


class TestMainWindow:
    """unittests for main.MainWindow
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.MainWindow object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called MainWindow.__init__ with args', args)
        monkeypatch.setattr(testee.MainWindow, '__init__', mock_init)
        testobj = testee.MainWindow()
        testobj.filename = testobj.dirname = ''
        testobj.projnames = [('django', 'project'), ('basic', 'another_project')]
        testobj.gui = MockMainGui(self)
        testobj.book = types.SimpleNamespace()
        assert capsys.readouterr().out == ('called MainWindow.__init__ with args ()\n'
                                           'called MainGui.__init__()\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for MainWindow.__init__
        """
        def mock_get():
            """stub
            """
            print('called dmls.get_projnames')
            return []
        def mock_get_2():
            """stub
            """
            print('called dmls.get_projnames')
            return ['xxx', 'yyy']
        def mock_determine(self, name):
            """stub
            """
            print(f"called MainWindow.determine_datatype_from_filename with arg '{name}'")
            self.datatype = testee.shared.DataType.XML
        def mock_determine_2(self, name):
            """stub
            """
            print(f"called MainWindow.determine_datatype_from_filename with arg '{name}'")
            self.datatype = None
        def mock_select_datatype_x(self):
            """stub
            """
            print("called MainWindow.select_datatype")
            self.datatype = testee.shared.DataType.XML
        def mock_select_datatype_x_f(self):
            """stub
            """
            print("called MainWindow.select_datatype")
            self.datatype = testee.shared.DataType.XML
            self.filename = 'something'
        def mock_select_datatype_s(self):
            """stub
            """
            print("called MainWindow.select_datatype")
            self.datatype = testee.shared.DataType.SQL
        def mock_select_datatype_m(self):
            """stub
            """
            print("called MainWindow.select_datatype")
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
        monkeypatch.setattr(testee.dmls, 'get_projnames', mock_get)
        monkeypatch.setattr(testee.MainWindow, 'determine_datatype_from_filename', mock_determine)
        monkeypatch.setattr(testee.MainWindow, 'select_datatype', mock_select_datatype_x)
        monkeypatch.setattr(testee.gui, 'MainGui', MockMainGui)
        monkeypatch.setattr(testee.MainWindow, 'create_book', mock_create_book)
        monkeypatch.setattr(testee.MainWindow, 'create_book_pages', mock_create_book_pages)
        monkeypatch.setattr(testee.MainWindow, 'open_xml', mock_open_xml)
        monkeypatch.setattr(testee.MainWindow, 'startfile', mock_startfile)
        monkeypatch.setattr(testee.MainWindow, 'open_sql', mock_open_sql)
        monkeypatch.setattr(testee.MainWindow, 'open_mongo', mock_open_mongo)
        testobj = testee.MainWindow('parent', 'some name')
        assert testobj.parent == 'parent'
        assert testobj.title == 'Actieregistratie'
        # de uitkomst van deze is altijd hetzelfde
        assert not testobj.initializing
        assert not testobj.exiting
        assert testobj.oldsort == -1
        assert testobj.idlist == []
        assert testobj.actlist == []
        assert testobj.alist == []
        assert hasattr(testobj, 'gui')
        # de uitkomst van deze is verschillend per aansturing
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
        assert capsys.readouterr().out == (
                "called dmls.get_projnames\n"
                "called MainWindow.determine_datatype_from_filename with arg 'some name'\n"
                'called MainGui.__init__()\n'
                'called.MainWindow.create_book()\n'
                'called MainGui.create_menu()\n'
                'called MainGui.enable_settingsmenu()\n'
                "called MainGui.create_actions with arg"
                f" [('Ctrl+P', {testobj.print_something}), ('Alt+Left', {testobj.goto_prev}),"
                f" ('Alt+Right', {testobj.goto_next})]\n"
                'called.MainWindow.create_book_pages()\n'
                'called.MainWindow.open_xml()\n')
        monkeypatch.setattr(testee.MainWindow, 'determine_datatype_from_filename', mock_determine_2)
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
        assert capsys.readouterr().out == (
                "called dmls.get_projnames\n"
                'called MainGui.__init__()\n'
                'called MainWindow.select_datatype\n'
                'called.MainWindow.create_book()\n'
                'called MainGui.create_menu()\n'
                'called MainGui.enable_settingsmenu()\n'
                "called MainGui.create_actions with arg"
                f" [('Ctrl+P', {testobj.print_something}), ('Alt+Left', {testobj.goto_prev}),"
                f" ('Alt+Right', {testobj.goto_next})]\n"
                'called.MainWindow.create_book_pages()\n'
                'called.MainWindow.startfile()\n')
        monkeypatch.setattr(testee.MainWindow, 'select_datatype', mock_select_datatype_s)
        testobj = None
        with pytest.raises(SystemExit) as exc:
            testobj = testee.MainWindow('parent')
        assert str(exc.value) == "No projects found; add one ior more in the webapp first"
        assert capsys.readouterr().out == ("called dmls.get_projnames\n"
                                           'called MainGui.__init__()\n'
                                           'called MainWindow.select_datatype\n')
        monkeypatch.setattr(testee.dmls, 'get_projnames', mock_get_2)
        testobj = testee.MainWindow('parent')
        assert testobj.datatype == testee.shared.DataType.SQL
        assert testobj.work_with_user
        assert testobj.user is None
        assert not testobj.is_user
        assert not testobj.is_admin
        assert not testobj.multiple_files
        assert testobj.multiple_projects
        assert not testobj.use_text_panels
        assert not testobj.use_rt
        assert testobj.use_separate_subject
        assert capsys.readouterr().out == (
                "called dmls.get_projnames\n"
                'called MainGui.__init__()\n'
                'called MainWindow.select_datatype\n'
                'called.MainWindow.create_book()\n'
                'called MainGui.create_menu()\n'
                'called MainGui.enable_settingsmenu()\n'
                'called MainGui.create_actions with arg'
                f" [('Ctrl+P', {testobj.print_something}), ('Alt+Left', {testobj.goto_prev}),"
                f" ('Alt+Right', {testobj.goto_next})]\n"
                'called.MainWindow.create_book_pages()\n'
                'called.MainWindow.open_sql() with arg True\n')
        monkeypatch.setattr(testee.MainWindow, 'select_datatype', mock_select_datatype_m)
        testobj = testee.MainWindow('parent')
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
        assert capsys.readouterr().out == (
                "called dmls.get_projnames\n"
                'called MainGui.__init__()\n'
                'called MainWindow.select_datatype\n'
                'called.MainWindow.create_book()\n'
                'called MainGui.create_menu()\n'
                'called MainGui.enable_settingsmenu()\n'
                'called MainGui.create_actions with arg'
                f" [('Ctrl+P', {testobj.print_something}), ('Alt+Left', {testobj.goto_prev}),"
                f" ('Alt+Right', {testobj.goto_next})]\n"
                'called.MainWindow.create_book_pages()\n'
                'called.MainWindow.open_mongo()\n')

    def test_determine_datatype_from_filename(self, monkeypatch, capsys):
        """unittest for MainWindow.determine_datatype_from_filename
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.determine_datatype_from_filename('xml')
        assert testobj.datatype == testee.shared.DataType.XML
        assert (testobj.dirname, testobj.filename) == ('', '')

        monkeypatch.setattr(testee.os.path, 'exists', lambda x: True)
        monkeypatch.setattr(testee.os.path, 'isfile', lambda x: True)
        testobj.datatype = None
        testobj.determine_datatype_from_filename('path/to/file/filename')
        assert testobj.datatype == testee.shared.DataType.XML
        assert (testobj.dirname, testobj.filename) == (testee.pathlib.Path('path/to/file'), 'filename')

        monkeypatch.setattr(testee.os.path, 'exists', lambda x: False)
        testobj.datatype = None
        testobj.dirname = ''
        testobj.filename = ''
        testobj.determine_datatype_from_filename('path/to/file/filename')
        assert not testobj.datatype
        assert (testobj.dirname, testobj.filename) == ('', '')

        monkeypatch.setattr(testee.os.path, 'exists', lambda x: True)
        monkeypatch.setattr(testee.os.path, 'isfile', lambda x: False)
        testobj.datatype = None
        testobj.determine_datatype_from_filename('path/to/file/filename')
        assert not testobj.datatype
        assert (testobj.dirname, testobj.filename) == ('', '')

        testobj.datatype = None
        testobj.determine_datatype_from_filename('sql')
        assert testobj.datatype == testee.shared.DataType.SQL
        assert (testobj.dirname, testobj.filename) == ('', '')

        testobj.datatype = None
        testobj.determine_datatype_from_filename('django')
        assert testobj.datatype == testee.shared.DataType.SQL
        assert (testobj.dirname, testobj.filename) == ('', '')

        testobj.datatype = None
        testobj.projnames = {'xxx': ('Xxx', 'yyyy')}
        testobj.determine_datatype_from_filename('qqq')
        assert testobj.datatype is None
        assert (testobj.dirname, testobj.filename) == ('', '')

        testobj.datatype = None
        testobj.determine_datatype_from_filename('xxx')
        assert testobj.datatype == testee.shared.DataType.SQL
        assert (testobj.dirname, testobj.filename) == ('', 'xxx')

        testobj.datatype = None
        testobj.determine_datatype_from_filename('Xxx')
        assert testobj.datatype == testee.shared.DataType.SQL
        assert (testobj.dirname, testobj.filename) == ('', 'Xxx')

        testobj.datatype = None
        testobj.filename = ''
        testobj.determine_datatype_from_filename('mongo')
        assert testobj.datatype == testee.shared.DataType.MNG
        assert (testobj.dirname, testobj.filename) == ('', '')

        testobj.datatype = None
        testobj.determine_datatype_from_filename('mongodb')
        assert testobj.datatype == testee.shared.DataType.MNG
        assert (testobj.dirname, testobj.filename) == ('', '')

    def test_select_datatype(self, monkeypatch, capsys):
        """unittest for MainWindow.select_datatype
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.select_datatype()
        assert testobj.datatype == testee.shared.DataType.XML
        testobj.select_datatype()
        assert testobj.datatype == testee.shared.DataType.SQL
        testobj.select_datatype()
        assert testobj.datatype == testee.shared.DataType.MNG
        with pytest.raises(SystemExit) as exc:
            testobj.select_datatype()
        assert str(exc.value) == 'No datatype selected'

    def test_get_menu_data(self, monkeypatch, capsys):
        """unittest for MainWindow.get_menu_data
        """
        def mock_goto(*args):
            """stub
            """
            return str(args)
        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_create_book(self, monkeypatch, capsys):
        """unittest for MainWindow.create_book
        """
        def mock_lees_settings(self):
            """stub
            """
            print('called MainWindow.lees_settings()')
        monkeypatch.setattr(testee.MainWindow, 'lees_settings', mock_lees_settings)
        testobj = self.setup_testobj(monkeypatch, capsys)
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
        assert not testobj.book.changed_item
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
        assert not testobj.book.changed_item
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
        assert not testobj.book.changed_item
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
        assert not testobj.book.changed_item
        assert testobj.book.pagedata is None
        assert capsys.readouterr().out == ('called MainGui.get_bookwidget()\n'
                                           'called MainWindow.lees_settings()\n')

    def test_create_book_pages(self, monkeypatch, capsys):
        """unittest for MainWindow.create_book_pages
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
        monkeypatch.setattr(testee.MainWindow, 'enable_all_book_tabs', mock_enable_all_book_tabs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book = types.SimpleNamespace(pages=[])
        testobj.book.tabs = ['nulde', 'eerste', 'laatste']
        testobj.use_text_panels = False
        testobj.create_book_pages()
        assert testobj.book.pages == ['0', '1', '6']
        assert capsys.readouterr().out == (
                'called Page0.__init__()\n'
                'called Page1.__init__()\n'
                'called Page6.__init__()\n'
                f"called MainGui.add_book_tab with args ({testobj.book}, '0', '&nulde')\n"
                f"called MainGui.add_book_tab with args ({testobj.book}, '1', '&eerste')\n"
                f"called MainGui.add_book_tab with args ({testobj.book}, '6', '&laatste')\n"
                'called MainWindow.enable_all_book_tabs(False)\n')
        testobj.book.pages = []
        testobj.book.tabs = ['nulde', 'eerste', 'tweede', 'derde', 'vierde', 'vijfde', 'laatste']
        testobj.use_text_panels = True
        testobj.create_book_pages()
        assert testobj.book.pages == ['0', '1', '2', '3', '4', '5', '6']
        assert capsys.readouterr().out == (
                'called Page0.__init__()\n'
                'called Page1.__init__()\n'
                'called Page.__init__() for page 2\n'
                'called Page.__init__() for page 3\n'
                'called Page.__init__() for page 4\n'
                'called Page.__init__() for page 5\n'
                'called Page6.__init__()\n'
                f"called MainGui.add_book_tab with args ({testobj.book}, '0', '&nulde')\n"
                f"called MainGui.add_book_tab with args ({testobj.book}, '1', '&eerste')\n"
                f"called MainGui.add_book_tab with args ({testobj.book}, '2', '&tweede')\n"
                f"called MainGui.add_book_tab with args ({testobj.book}, '3', '&derde')\n"
                f"called MainGui.add_book_tab with args ({testobj.book}, '4', '&vierde')\n"
                f"called MainGui.add_book_tab with args ({testobj.book}, '5', '&vijfde')\n"
                f"called MainGui.add_book_tab with args ({testobj.book}, '6', '&laatste')\n"
                'called MainWindow.enable_all_book_tabs(False)\n')

    def test_not_implemented_message(self, monkeypatch, capsys):
        """unittest for MainWindow.not_implemented_message
        """
        def mock_show_message(self, mld):
            """stub
            """
            print(f'called MainWindow.show_message(`{mld}`)')
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.not_implemented_message()
        assert capsys.readouterr().out == 'called MainWindow.show_message(`Sorry, werkt nog niet`)\n'

    def test_new_file(self, monkeypatch, capsys):
        """unittest for MainWindow.new_file
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
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        monkeypatch.setattr(testee.gui, 'get_save_filename', mock_get_save_filename)
        monkeypatch.setattr(testee.MainWindow, 'enable_all_book_tabs', mock_enable_all_book_tabs)
        monkeypatch.setattr(testee.MainWindow, 'startfile', mock_startfile)
        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_open_xml(self, monkeypatch, capsys):
        """unittest for MainWindow.open_xml
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
        monkeypatch.setattr(testee.MainWindow, 'startfile', mock_startfile)
        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_new_project(self, monkeypatch, capsys):
        """unittest for MainWindow.new_project
        """
        def mock_show_message(self, mld):
            """stub
            """
            print(f'called MainWindow.show_message(`{mld}`)')
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.new_project()
        assert capsys.readouterr().out == (
                'called MainWindow.show_message('
                '`Voor deze functie moet u de ActieReg webapplicatie gebruiken`)\n')

    def test_open_sql(self, monkeypatch, capsys):
        """unittest for MainWindow.open_sql
        """
        def mock_get_choice_item(*args):
            """stub
            """
            print('called gui.get_choice_item with args', args)
            return 'xxxx'
        def mock_get_choice_item_2(*args):
            """stub
            """
            print('called gui.get_choice_item with args', args)
            return ''
        def mock_startfile(self):
            """stub
            """
            print('called MainWindow.startfile()')

        monkeypatch.setattr(testee.MainWindow, 'startfile', mock_startfile)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.projnames = {'xxxx': ('xxxx', 'xxxxxx xxxxxxx'), 'yyyy': ('yyyy', 'yyyy yyyyyyy')}

        monkeypatch.setattr(testee.gui, 'get_choice_item', mock_get_choice_item)
        testobj.filename = 'xxxx'
        testobj.open_sql()
        assert testobj.filename == 'xxxx'
        assert capsys.readouterr().out == (
                f"called gui.get_choice_item with args ({testobj.gui},"
                " 'Kies een project om te openen', ['xxxx: xxxxxx xxxxxxx', 'yyyy: yyyy yyyyyyy'], 0)\n"
                'called MainWindow.startfile()\n')

        testobj.filename = ''
        testobj.open_sql()
        assert testobj.filename == 'xxxx'
        assert capsys.readouterr().out == (
                f"called gui.get_choice_item with args ({testobj.gui},"
                " 'Kies een project om te openen', ['xxxx: xxxxxx xxxxxxx', 'yyyy: yyyy yyyyyyy'], 1)\n"
                'called MainWindow.startfile()\n')

        monkeypatch.setattr(testee.gui, 'get_choice_item', mock_get_choice_item_2)
        testobj.filename = 'xxxx'
        testobj.open_sql()
        assert testobj.filename == 'xxxx'
        assert capsys.readouterr().out == (
                f"called gui.get_choice_item with args ({testobj.gui},"
                " 'Kies een project om te openen', ['xxxx: xxxxxx xxxxxxx', 'yyyy: yyyy yyyyyyy'], 0)\n")

        testobj.filename = ''
        testobj.open_sql()
        assert testobj.filename == ''
        assert capsys.readouterr().out == (
                f"called gui.get_choice_item with args ({testobj.gui},"
                " 'Kies een project om te openen', ['xxxx: xxxxxx xxxxxxx', 'yyyy: yyyy yyyyyyy'], 1)\n")

        monkeypatch.setattr(testee.gui, 'get_choice_item', mock_get_choice_item)
        testobj.filename = '_basic'
        testobj.open_sql(do_sel=False)
        assert testobj.filename == 'xxxx'  # uitkomst van selector
        assert capsys.readouterr().out == (
                f"called gui.get_choice_item with args ({testobj.gui},"
                " 'Kies een project om te openen', ['xxxx: xxxxxx xxxxxxx', 'yyyy: yyyy yyyyyyy'], 0)\n"
                'called MainWindow.startfile()\n')

        testobj.filename = 'yyyy'
        testobj.open_sql(do_sel=False)
        assert testobj.filename == 'yyyy'
        assert capsys.readouterr().out == 'called MainWindow.startfile()\n'

    def test_open_mongo(self, monkeypatch, capsys):
        """unittest for MainWindow.open_mongo
        """
        def mock_startfile(self):
            """stub
            """
            print('called MainWindow.startfile()')

        monkeypatch.setattr(testee.MainWindow, 'startfile', mock_startfile)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.open_mongo()
        assert testobj.filename == 'default'
        assert capsys.readouterr().out == 'called MainWindow.startfile()\n'

    def test_print_something(self, monkeypatch, capsys):
        """unittest for MainWindow.print_something
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

        monkeypatch.setattr(testee.MainWindow, 'print_scherm', mock_print_scherm)
        monkeypatch.setattr(testee.MainWindow, 'print_actie', mock_print_actie)
        monkeypatch.setattr(testee.gui, 'get_choice_item', mock_get_choice_item)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.print_something()
        assert capsys.readouterr().out == 'called MainWindow.print_scherm()\n'
        testobj.print_something()
        assert capsys.readouterr().out == 'called MainWindow.print_actie()\n'

    def test_print_scherm(self, monkeypatch, capsys):
        """unittest for MainWindow.print_scherm
        """
        def mock_get_items(*args):
            """stub
            """
            print('called Page.get_items with args', args)
            return ['item0', 'item1', 'item2']
        def mock_get_item_text(*args):
            """stub
            """
            print('called Page.get_item_text with args', args)
            data = {'item0': ('actie1', 'I', '0', 'eerder', 'titel'),
                    'item1': ('actie2', 'A', '1', 'later', 'titel2'),
                    'item2': ('actie3', 'X', '2', '', 'titel3')}
            return data[args[1]][args[2]]
        def mock_get_item_text_2(*args):
            """stub
            """
            print('called Page.get_item_text with args', args)
            data = {'item0': ('actie1', 'I', 'new', 'eens', 'onderwerp1', 'titel1'),
                    'item1': ('actie2', 'A', 'old', 'ooit', 'onderwerp2', 'titel2'),
                    'item2': ('actie3', 'X', 'old', '', 'onderwerp3', 'titel3')}
            return data[args[1]][args[2]]
        def mock_get_field_text(fieldname):
            """stub
            """
            return fieldname + '_text'
        def mock_get_textarea_contents():
            """stub
            """
            return 'textarea_contents'

        # monkeypatch.setattr(testee.MainWindow, 'xxx', mock_xxx)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.filename = 'Filename'
        testobj.book.pages = [MockPage()] * 7
        assert capsys.readouterr().out == ('called Page.__init__() with args () {}\n'
                                           'called PageGui.__init__() with args () {}\n')
        testobj.book.tabs = {0: '0 nul', 1: '1 een', 2: '2 twee', 3: '3 drie', 4: '4 vier', 5: '5 vijf',
                             6: '6 zes'}
        testobj.book.cats = {0: ['this', 'I'], 1: ['that', 'A']}
        testobj.book.stats = {0: ['new', 0], 1: ['old', 1]}
        testobj.book.pagedata = types.SimpleNamespace(id='this', titel='action', datum='startdate')

        testobj.book.current_tab = 0
        testobj.use_separate_subject = False
        monkeypatch.setattr(testobj.book.pages[0].gui, 'get_items', mock_get_items)
        monkeypatch.setattr(testobj.book.pages[0].gui, 'get_item_text', mock_get_item_text)
        testobj.book.pages[0].p0list = 'p0list'
        testobj.print_scherm()
        assert testobj.printdict == {'actie': [],
                                     'events': [],
                                     'lijst': [('actie1', 'titel', 'this', 'startdate',
                                                'status: 0, laatst behandeld op eerder'),
                                               ('actie2', 'titel2', 'that', 'startdate',
                                                'status: 1, laatst behandeld op later'),
                                               ('actie3', 'titel3', 'X', 'startdate', 'status: 2')],
                                     'sections': [], }
        assert testobj.hdr == 'Overzicht acties uit Filename'
        assert capsys.readouterr().out == (
                "called Page.get_items with args ('p0list',)\n"
                "called Page.get_item_text with args ('p0list', 'item0', 0)\n"
                "called Page.get_item_text with args ('p0list', 'item0', 1)\n"
                "called Page.get_item_text with args ('p0list', 'item0', 2)\n"
                "called Page.get_item_text with args ('p0list', 'item0', 3)\n"
                "called Page.get_item_text with args ('p0list', 'item0', 4)\n"
                "called Page.get_item_text with args ('p0list', 'item1', 0)\n"
                "called Page.get_item_text with args ('p0list', 'item1', 1)\n"
                "called Page.get_item_text with args ('p0list', 'item1', 2)\n"
                "called Page.get_item_text with args ('p0list', 'item1', 3)\n"
                "called Page.get_item_text with args ('p0list', 'item1', 4)\n"
                "called Page.get_item_text with args ('p0list', 'item2', 0)\n"
                "called Page.get_item_text with args ('p0list', 'item2', 1)\n"
                "called Page.get_item_text with args ('p0list', 'item2', 2)\n"
                "called Page.get_item_text with args ('p0list', 'item2', 3)\n"
                "called Page.get_item_text with args ('p0list', 'item2', 4)\n"
                'called MainGui.preview()\n')
        testobj.use_separate_subject = True
        monkeypatch.setattr(testobj.book.pages[0].gui, 'get_item_text', mock_get_item_text_2)
        testobj.print_scherm()
        assert testobj.printdict == {'actie': [],
                                     'events': [],
                                     'lijst': [('actie1 - onderwerp1', 'titel1', 'this', 'startdate',
                                                'status: new op startdate'),
                                               ('actie2 - onderwerp2', 'titel2', 'that', 'startdate',
                                                'status: old, laatst behandeld op ooit'),
                                               ('actie3 - onderwerp3', 'titel3', 'X', 'startdate',
                                                'status: old')],
                                     'sections': [], }
        assert testobj.hdr == 'Overzicht acties uit Filename'
        assert capsys.readouterr().out == (
                "called Page.get_items with args ('p0list',)\n"
                "called Page.get_item_text with args ('p0list', 'item0', 0)\n"
                "called Page.get_item_text with args ('p0list', 'item0', 1)\n"
                "called Page.get_item_text with args ('p0list', 'item0', 2)\n"
                "called Page.get_item_text with args ('p0list', 'item0', 3)\n"
                "called Page.get_item_text with args ('p0list', 'item0', 4)\n"
                "called Page.get_item_text with args ('p0list', 'item0', 5)\n"
                "called Page.get_item_text with args ('p0list', 'item1', 0)\n"
                "called Page.get_item_text with args ('p0list', 'item1', 1)\n"
                "called Page.get_item_text with args ('p0list', 'item1', 2)\n"
                "called Page.get_item_text with args ('p0list', 'item1', 3)\n"
                "called Page.get_item_text with args ('p0list', 'item1', 4)\n"
                "called Page.get_item_text with args ('p0list', 'item1', 5)\n"
                "called Page.get_item_text with args ('p0list', 'item2', 0)\n"
                "called Page.get_item_text with args ('p0list', 'item2', 1)\n"
                "called Page.get_item_text with args ('p0list', 'item2', 2)\n"
                "called Page.get_item_text with args ('p0list', 'item2', 3)\n"
                "called Page.get_item_text with args ('p0list', 'item2', 4)\n"
                "called Page.get_item_text with args ('p0list', 'item2', 5)\n"
                'called MainGui.preview()\n')

        testobj.book.current_tab = 1
        testobj.book.pages[1].id_text = 'id_text'
        testobj.book.pages[1].date_text = 'date_text'
        testobj.book.pages[1].proc_entry = 'proc_entry'
        testobj.book.pages[1].desc_entry = 'desc_entry'
        testobj.book.pages[1].cat_choice = 'cat_choice'
        testobj.book.pages[1].stat_choice = 'stat_choice'
        testobj.book.pages[1].summary_entry = 'summary_entry'
        # monkeypatch.setattr(testobj.book.pages[1].gui, 'get_field_text', mock_get_field_text)
        testobj.use_text_panels = True
        testobj.book.pages[-1].event_list = []
        testobj.book.pages[-1].event_data = []
        testobj.print_scherm()
        assert testobj.printdict == {'actie': 'id_text',
                                     'datum': 'date_text',
                                     'oms': 'proc_entry',
                                     'tekst': 'desc_entry',
                                     'soort': ('cat_choice', 'x'),
                                     'status': ('stat_choice', 'x'),
                                     'events': [],
                                     'lijst': [],
                                     'sections': []}
        assert testobj.hdr == 'Informatie over actie id_text: samenvatting'
        assert capsys.readouterr().out == (
                "called PageGui.get_textfield_value with args ('id_text',)\n"
                "called PageGui.get_textfield_value with args ('date_text',)\n"
                "called PageGui.get_textfield_value with args ('proc_entry',)\n"
                "called PageGui.get_textfield_value with args ('desc_entry',)\n"
                "called PageGui.get_choice_data with args ('cat_choice',)\n"
                "called PageGui.get_choice_data with args ('stat_choice',)\n"
                'called MainGui.preview()\n')
        testobj.use_text_panels = False
        testobj.print_scherm()
        assert testobj.printdict == {'actie': 'id_text',
                                     'datum': 'date_text',
                                     'oms': 'proc_entry',
                                     'tekst': 'desc_entry',
                                     'soort': ('cat_choice', 'x'),
                                     'status': ('stat_choice', 'x'),
                                     'melding': 'summary_entry',
                                     'events': [],
                                     'lijst': [],
                                     'sections': []}
        assert testobj.hdr == 'Informatie over actie id_text: samenvatting'
        assert capsys.readouterr().out == (
                "called PageGui.get_textfield_value with args ('id_text',)\n"
                "called PageGui.get_textfield_value with args ('date_text',)\n"
                "called PageGui.get_textfield_value with args ('proc_entry',)\n"
                "called PageGui.get_textfield_value with args ('desc_entry',)\n"
                "called PageGui.get_choice_data with args ('cat_choice',)\n"
                "called PageGui.get_choice_data with args ('stat_choice',)\n"
                "call PageGui.get_textbox_value with args ('summary_entry',)\n"
                'called MainGui.preview()\n')

        testobj.book.current_tab = 2
        # monkeypatch.setattr(testobj.book.pages[2].gui, 'get_textarea_contents', mock_get_textarea_contents)
        testobj.book.pages[2].text1 = 'text1'
        testobj.print_scherm()
        assert testobj.printdict == {'sections': [('twee', 'text')],
                                     'events': [],
                                     'lijst': [],
                                     'actie': []}
        assert testobj.hdr == 'Actie: this action'
        assert capsys.readouterr().out == (
                "call PageGui.get_textarea_contents with args ('text1',)\n"
                'called MainGui.preview()\n')

        testobj.book.current_tab = 5
        testobj.print_scherm()
        assert testobj.printdict == {'sections': [('vijf', 'text')],
                                     'events': [],
                                     'lijst': [],
                                     'actie': []}
        assert testobj.hdr == 'Actie: this action'
        assert capsys.readouterr().out == (
                "call PageGui.get_textarea_contents with args ('text1',)\n"
                'called MainGui.preview()\n')

        testobj.book.current_tab = 6
        testobj.book.pages[6].event_list = ['01-01-2001 01:01:01', '02-02-2002 02:02:02T12345']
        testobj.book.pages[6].event_data = ['event_text', 'another_event']
        testobj.print_scherm()
        assert testobj.printdict == {'events': [('01-01-2001 01:01:01', 'event_text'),
                                                ('02-02-2002 02:02:02T12345', 'another_event')],
                                     'actie': [],
                                     'lijst': [],
                                     'sections': []}
        assert testobj.hdr == 'Actie: this action'
        assert capsys.readouterr().out == 'called MainGui.preview()\n'

    def test_print_actie(self, monkeypatch, capsys):
        """unittest for MainWindow.print_actie
        """
        def mock_show_message(win, message):
            """stub
            """
            print(f'called gui.show_message(`{message}`)')

        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
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
        testobj.book.pagedata = types.SimpleNamespace(id='this', datum='today', soort='A', status=1,
                                                      titel='xxx: yyy', melding='zzzzzzzzzzzzzzz',
                                                      oorzaak='aaaa', oplossing='bbbb', vervolg='ccc',
                                                      events=[('time1', 'text1'), ('time2', 'text2')])
        testobj.print_actie()
        assert testobj.printdict == {'actie': 'this', 'datum': 'today',
                                     'events': [('time1', 'text1'), ('time2', 'text2')],
                                     'lijst': [], 'oms': 'xxx',
                                     'sections': [['twee', 'zzzzzzzzzzzzzzz'], ['drie', 'aaaa'],
                                                  ['vier', 'bbbb'], ['vijf', 'ccc']],
                                     'soort': 'that', 'status': 'old', 'tekst': 'yyy'}
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

    def test_exit_app(self, monkeypatch, capsys):
        """unittest for MainWindow.exit_app
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_sign_in(self, monkeypatch, capsys):
        """unittest for MainWindow.sign_in
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
        class MockLoginBox:
            def __init__(self, *args):
                print('called LoginBox.__init__ with args', args)
                self.gui = 'LoginBoxGui'
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
            if counter == 3:
                return 'me', True, False
            if counter == 4:
                return 'me', False, True
            if counter == 5:
                return 'me', False, False
            return 'me', True, True

        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog)
        monkeypatch.setattr(testee, 'LoginBox', MockLoginBox)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.dmls, 'validate_user', lambda *x: ('', False, False))
        testobj.sign_in()
        assert capsys.readouterr().out == (f"called LoginBox.__init__ with args ({testobj},)\n"
                                           'called gui.show_dialog() (for login dialog)\n')

        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog_ok)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        monkeypatch.setattr(testee.dmls, 'SortOptions', MockOptions)
        monkeypatch.setattr(testee.dmls, 'validate_user', mock_validate_user)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.filename = 'xxx'
        testobj.dialog_data = 'stuff'
        testobj.book.rereadlist = mock_rereadlist
        testobj.book.pages = [types.SimpleNamespace()]
        testobj.sign_in()
        assert (testobj.user, testobj.is_user, testobj.is_admin) == ('me', True, True)
        assert isinstance(testobj.book.pages[0].saved_sortopts, testee.dmls.SortOptions)
        assert capsys.readouterr().out == (f"called LoginBox.__init__ with args ({testobj},)\n"
                                           'called gui.show_dialog() (for login dialog)\n'
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
        assert capsys.readouterr().out == (f"called LoginBox.__init__ with args ({testobj},)\n"
                                           'called gui.show_dialog() (for login dialog)\n'
                                           'called dmls.validate_user()\n'
                                           'called gui.show_message(`Login accepted`)\n'
                                           'called MainGui.enable_settingsmenu()\n'
                                           'called dmls.SortOptions.__init__ with arg xxx\n'
                                           'called MainGui.refresh_page()\n')
        testobj.book.pages = [types.SimpleNamespace()]
        testobj.sign_in()
        assert (testobj.user, testobj.is_user, testobj.is_admin) == ('me', False, True)
        assert isinstance(testobj.book.pages[0].saved_sortopts, testee.dmls.SortOptions)
        assert capsys.readouterr().out == (f"called LoginBox.__init__ with args ({testobj},)\n"
                                           'called gui.show_dialog() (for login dialog)\n'
                                           'called dmls.validate_user()\n'
                                           'called gui.show_message(`Login accepted`)\n'
                                           'called MainGui.enable_settingsmenu()\n'
                                           'called dmls.SortOptions.__init__ with arg xxx\n'
                                           'called MainGui.refresh_page()\n')
        testobj.book.pages = [types.SimpleNamespace()]
        testobj.sign_in()
        assert (testobj.user, testobj.is_user, testobj.is_admin) == ('me', False, False)
        assert testobj.book.pages[0].saved_sortopts is None
        assert capsys.readouterr().out == (f"called LoginBox.__init__ with args ({testobj},)\n"
                                           'called gui.show_dialog() (for login dialog)\n'
                                           'called dmls.validate_user()\n'
                                           'called gui.show_message(`Login accepted`)\n'
                                           'called MainGui.enable_settingsmenu()\n'
                                           'called MainGui.refresh_page()\n')

    def test_tab_settings(self, monkeypatch, capsys):
        """unittest for MainWindow.tab_settings
        """
        def mock_show_dialog(*args):
            """stub
            """
            print('called gui.show_dialog.__init__ with args', args)
        class MockDialog:
            def __init__(self, *args):
                print('called SettOptionsDialog with args', args)
                self.gui = 'SettOptionsDialogGui'
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog)
        monkeypatch.setattr(testee, 'SettOptionsDialog', MockDialog)
        monkeypatch.setattr(testee, 'TabOptions', 'taboptions')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tab_settings()
        assert capsys.readouterr().out == (
                "called SettOptionsDialog with args"
                f" ({testobj}, 'taboptions', 'Wijzigen tab titels')\n"
                "called gui.show_dialog.__init__ with args ('SettOptionsDialogGui',)\n")

    def test_stat_settings(self, monkeypatch, capsys):
        """unittest for MainWindow.stat_settings
        """
        def mock_show_dialog(*args):
            """stub
            """
            print('called gui.show_dialog.__init__ with args', args)
        class MockDialog:
            def __init__(self, *args):
                print('called SettOptionsDialog with args', args)
                self.gui = 'SettOptionsDialogGui'
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog)
        monkeypatch.setattr(testee, 'SettOptionsDialog', MockDialog)
        monkeypatch.setattr(testee, 'StatOptions', 'statoptions')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.stat_settings()
        assert capsys.readouterr().out == (
                "called SettOptionsDialog with args"
                f" ({testobj}, 'statoptions', 'Wijzigen statussen')\n"
                "called gui.show_dialog.__init__ with args ('SettOptionsDialogGui',)\n")

    def test_cat_settings(self, monkeypatch, capsys):
        """unittest for MainWindow.cat_settings
        """
        def mock_show_dialog(*args):
            """stub
            """
            print('called gui.show_dialog.__init__ with args', args)
        class MockDialog:
            def __init__(self, *args):
                print('called SettOptionsDialog with args', args)
                self.gui = 'SettOptionsDialogGui'
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog)
        monkeypatch.setattr(testee, 'SettOptionsDialog', MockDialog)
        monkeypatch.setattr(testee, 'CatOptions', 'catoptions')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.cat_settings()
        assert capsys.readouterr().out == (
                "called SettOptionsDialog with args"
                f" ({testobj}, 'catoptions', 'Wijzigen categorieën')\n"
                "called gui.show_dialog.__init__ with args ('SettOptionsDialogGui',)\n")

    def test_font_settings(self, monkeypatch, capsys):
        """unittest for MainWindow.font_settings
        """
        def mock_show_message(self, mld):
            """stub
            """
            print(f'called MainWindow.show_message(`{mld}`)')

        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.font_settings()
        assert capsys.readouterr().out == 'called MainWindow.show_message(`Sorry, werkt nog niet`)\n'

    def test_colour_settings(self, monkeypatch, capsys):
        """unittest for MainWindow.colour_settings
        """
        def mock_show_message(self, mld):
            """stub
            """
            print(f'called MainWindow.show_message(`{mld}`)')
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.colour_settings()
        assert capsys.readouterr().out == 'called MainWindow.show_message(`Sorry, werkt nog niet`)\n'

    def test_hotkey_settings(self, monkeypatch, capsys):
        """unittest for MainWindow.hotkey_settings
        """
        def mock_show_message(self, mld):
            """stub
            """
            print(f'called MainWindow.show_message(`{mld}`)')

        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.hotkey_settings()
        assert capsys.readouterr().out == 'called MainWindow.show_message(`Sorry, werkt nog niet`)\n'

    def test_about_help(self, monkeypatch, capsys):
        """unittest for MainWindow.about_help
        """
        def mock_show_message(win, msg):
            """stub
            """
            print('called gui.show_message()')
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.about_help()
        assert capsys.readouterr().out == 'called gui.show_message()\n'

    def test_hotkey_help(self, monkeypatch, capsys):
        """unittest for MainWindow.hotkey_help
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

        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_silly_menu(self, monkeypatch, capsys):
        """unittest for MainWindow.silly_menu
        """
        def mock_show_message(win, msg):
            """stub
            """
            print('called gui.show_message()')

        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.silly_menu()
        assert capsys.readouterr().out == 'called gui.show_message()\n'

    def test_startfile(self, monkeypatch, capsys):
        """unittest for MainWindow.startfile
        """
        class MockBook:
            "voor deze test een expliciete klasse om de output goed te kunnen tonen"
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

        monkeypatch.setattr(testee.MainWindow, 'lees_settings', mock_lees_settings)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book = MockBook()
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
        # testobj.book.tabs = ['tab', 'titles']
        testobj.book.tabs = {1: 'tab', 2: 'titles'}
        testobj.book.pages = [types.SimpleNamespace(clear_selection=mock_clear_selection, vulp=mock_vulp),
                              types.SimpleNamespace(vul_combos=mock_vul_combos)]
        testobj.book.current_tab = -1
        assert testobj.startfile() == ''
        assert str(testobj.book.fnaam) == 'path/to/file.xml'
        assert testobj.title == 'path/to/file.xml'
        assert testobj.book.rereadlist
        assert testobj.book.sorter is None
        assert not testobj.book.changed_item
        assert testobj.book.current_tab == 0
        # deze output komt er niet lekker uit doordat testobj.book een SimpleNamespace is
        # die tussentijds gewijzigd wordt -
        assert capsys.readouterr().out == (
                "called MainWindow.lees_settings()\n"
                f"called MainGui.set_page_title() with args ({testobj.book}, 1, 'tab')\n"
                f"called MainGui.set_page_title() with args ({testobj.book}, 2, 'titles')\n"
                "called Page.clear_selection()\n"
                "called Page.vul_combos()\n"
                "called Page.vulp()\n")
        testobj.book.current_tab = 0
        assert testobj.startfile() == ''
        assert str(testobj.book.fnaam) == 'path/to/file.xml'
        assert testobj.title == 'path/to/file.xml'
        assert testobj.book.rereadlist
        assert testobj.book.sorter is None
        assert not testobj.book.changed_item
        assert testobj.book.current_tab == 0
        assert capsys.readouterr().out == (
                "called MainWindow.lees_settings()\n"
                f"called MainGui.set_page_title() with args ({testobj.book}, 1, 'tab')\n"
                f"called MainGui.set_page_title() with args ({testobj.book}, 2, 'titles')\n"
                "called Page.clear_selection()\n"
                "called Page.vul_combos()\n"
                "called Page.vulp()\n")
        testobj.multiple_files = False
        testobj.multiple_projects = True
        testobj.filename = 'Project'
        testobj.projnames = {'x': ('y', 'z'), 'project': ('Project', 'Demo Project')}
        testobj.book.current_tab = 1
        assert testobj.startfile() == ''
        assert testobj.book.fnaam == 'Project'
        assert testobj.title == 'Project'
        assert testobj.book.rereadlist
        assert testobj.book.sorter is None
        assert not testobj.book.changed_item
        assert testobj.book.current_tab == 1
        assert capsys.readouterr().out == (
                "called MainWindow.lees_settings()\n"
                f"called MainGui.set_page_title() with args ({testobj.book}, 1, 'tab')\n"
                f"called MainGui.set_page_title() with args ({testobj.book}, 2, 'titles')\n"
                "called Page.clear_selection()\n"
                "called Page.vul_combos()\n"
                # "called Page.vulp()\n")
                f"called MainGui.set_page with args ({testobj.book}, 0)\n")
        testobj.multiple_files = False
        testobj.multiple_projects = False
        testobj.filename = 'default'
        assert testobj.startfile() == ''
        assert testobj.book.fnaam == 'default'
        assert testobj.title == ''
        assert testobj.book.rereadlist
        assert testobj.book.sorter is None
        assert not testobj.book.changed_item
        assert capsys.readouterr().out == (
                "called MainWindow.lees_settings()\n"
                f"called MainGui.set_page_title() with args ({testobj.book}, 1, 'tab')\n"
                f"called MainGui.set_page_title() with args ({testobj.book}, 2, 'titles')\n"
                "called Page.clear_selection()\n"
                "called Page.vul_combos()\n"
                # "called Page.vulp()\n")
                f"called MainGui.set_page with args ({testobj.book}, 0)\n")
        # deze test bewust uitgezet om deze situatie niet ongemerkt langs te laten komen
        # testobj.multiple_files = False
        # testobj.multiple_projects = True
        # testobj.filename = 'default'
        # testobj.projnames = []
        # with pytest.raises(ValueError) as exception:
        #     testobj.startfile()
        # assert str(exception.value) == 'ProgrammingError: self.projnames should never be empty'

    def test_lees_settings(self, monkeypatch, capsys):
        """unittest for MainWindow.lees_settings
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.datatype = 'x'
        testobj.book.fnaam = 'y'
        monkeypatch.setattr(testee.shared, 'Settings', {'x': MockSettings})
        testobj.lees_settings()
        assert testobj.imagecount == 1
        assert testobj.startitem == '0'
        assert testobj.book.stats == {1: ['statitem', 1]}
        assert testobj.book.cats == {2: ['catitem', 2]}
        assert testobj.book.tabs == {3: '3 Kopitem'}

    def test_save_settings(self, monkeypatch, capsys):
        """unittest for MainWindow.save_settings
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
        monkeypatch.setattr(testee.gui.MainGui, 'set_page_title', mock_set_page_title)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.shared, 'Settings', {'x': MockSettings})
        testobj.datatype = 'x'
        testobj.book.fnaam = 'y'
        testobj.book.pages = ('page0', types.SimpleNamespace(vul_combos=mock_vul_combos))
        testobj.save_settings('tab', {'0': ('newkop', '0')})
        assert testobj.book.tabs == {0: '0 Newkop'}
        assert capsys.readouterr().out == (
                'called Settings.write()\n'
                f"called MainGui.set_page_title() with args ({testobj.book}, 0, 'newkop')\n"
                'called MainWindow.book.vul_combos()\n')

        testobj.save_settings('stat', {0: ('newstat', '0')})
        assert testobj.book.stats == {0: ['newstat', 0]}
        assert capsys.readouterr().out == (
                'called Settings.write()\n'
                'called MainWindow.book.vul_combos()\n')

        testobj.save_settings('cat', {0: ('newcat', '0')})
        assert testobj.book.cats == {0: ['newcat', 0]}
        assert capsys.readouterr().out == (
                'called Settings.write()\n'
                'called MainWindow.book.vul_combos()\n')
        monkeypatch.setattr(MockSettings, 'write', lambda *x: ('error', 'message'))
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj.save_settings('stat', 'x')
        assert capsys.readouterr().out == (
                'called gui.show_message(`Kan status message niet verwijderen,'
                ' wordt nog gebruikt in één of meer acties`\n')
        testobj.save_settings('cat', 'x')
        assert capsys.readouterr().out == (
                'called gui.show_message(`Kan soort message niet verwijderen,'
                ' wordt nog gebruikt in één of meer acties`\n')

    def test_save_startitem_on_exit(self, monkeypatch, capsys):
        """unittest for MainWindow.save_startitem_on_exit
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

        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_goto_next(self, monkeypatch, capsys):
        """unittest for MainWindow.goto_next
        """
        # def mock_goto_next(*args):
        #     """stub
        #     """
        #     print('called Page.goto_next() with args', args)
        class MockPage:
            """stub
            """
            def goto_next(self, *args):
                print('called Page.goto_next() with args', args)

        # monkeypatch.setattr(testee.Page, 'goto_next', mock_goto_next)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.pages = ['page0', MockPage()]
        testobj.book.current_tab = 1
        testobj.goto_next()
        assert capsys.readouterr().out == "called Page.goto_next() with args ()\n"

    def test_goto_prev(self, monkeypatch, capsys):
        """unittest for MainWindow.goto_prev
        """
        # def mock_goto_prev(*args):
        #     """stub
        #     """
        #     print('called Page.goto_prev() with args', args)
        class MockPage:
            """stub
            """
            def goto_prev(self, *args):
                print('called Page.goto_prev() with args', args)

        # monkeypatch.setattr(testee.Page, 'goto_prev', mock_goto_prev)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.pages = ['page0', MockPage()]
        testobj.book.current_tab = 1
        testobj.goto_prev()
        assert capsys.readouterr().out == "called Page.goto_prev() with args ()\n"

    def test_goto_page(self, monkeypatch, capsys):
        """unittest for MainWindow.goto_page
        """
        # def mock_goto_page(*args):
        #     """stub
        #     """
        #     print('called Page.goto_page() with args', args)
        class MockPage:
            """stub
            """
            def goto_page(self, *args):
                print('called Page.goto_page() with args', args)

        # monkeypatch.setattr(testee.Page, 'goto_page', mock_goto_page)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.pages = [MockPage(), 'page1']
        testobj.book.current_tab = 0
        testobj.goto_page(1)
        assert capsys.readouterr().out == "called Page.goto_page() with args (1,)\n"

    def test_enable_settingsmenu(self, monkeypatch, capsys):
        """unittest for MainWindow.enable_settingsmenu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.enable_settingsmenu()
        assert capsys.readouterr().out == 'called MainGui.enable_settingsmenu()\n'

    def test_set_windowtitle(self, monkeypatch, capsys):
        """unittest for MainWindow.set_windowtitle
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_windowtitle('some_text')
        assert capsys.readouterr().out == (
                "called MainGui.set_window_title() with args ('some_text',)\n")

    def test_set_statusmessage(self, monkeypatch, capsys):
        """unittest for MainWindow.set_statusmessage
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_get_focus_widget_for_tab(self, monkeypatch, capsys):
        """unittest for MainWindow.get_focus_widget_for_tab
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.use_text_panels = True
        page0 = MockPage()
        assert capsys.readouterr().out == ('called Page.__init__() with args () {}\n'
                                           'called PageGui.__init__() with args () {}\n')
        page0.p0list = 'p0list'
        page1 = MockPage()
        assert capsys.readouterr().out == ('called Page.__init__() with args () {}\n'
                                           'called PageGui.__init__() with args () {}\n')
        page1.proc_entry = 'proc_entry'
        page2 = MockPage()
        assert capsys.readouterr().out == ('called Page.__init__() with args () {}\n'
                                           'called PageGui.__init__() with args () {}\n')
        page2.text1 = 'text_page2'
        page3 = MockPage()
        assert capsys.readouterr().out == ('called Page.__init__() with args () {}\n'
                                           'called PageGui.__init__() with args () {}\n')
        page3.text1 = 'text_page3'
        page4 = MockPage()
        assert capsys.readouterr().out == ('called Page.__init__() with args () {}\n'
                                           'called PageGui.__init__() with args () {}\n')
        page4.text1 = 'text_page4'
        page5 = MockPage()
        assert capsys.readouterr().out == ('called Page.__init__() with args () {}\n'
                                           'called PageGui.__init__() with args () {}\n')
        page5.text1 = 'text_page5'
        page6 = MockPage()
        assert capsys.readouterr().out == ('called Page.__init__() with args () {}\n'
                                           'called PageGui.__init__() with args () {}\n')
        page6.progress_list = 'progress_list'
        testobj.book.pages = [page0, page1, page2, page3, page4, page5, page6]
        assert testobj.get_focus_widget_for_tab(0) == 'p0list'
        assert testobj.get_focus_widget_for_tab(1) == 'proc_entry'
        assert testobj.get_focus_widget_for_tab(2) == 'text_page2'
        assert testobj.get_focus_widget_for_tab(3) == 'text_page3'
        assert testobj.get_focus_widget_for_tab(4) == 'text_page4'
        assert testobj.get_focus_widget_for_tab(5) == 'text_page5'
        assert testobj.get_focus_widget_for_tab(6) == 'progress_list'
        testobj.use_text_panels = False
        page2.progress_list = 'progress_list'
        testobj.book.pages = [page0, page1, page2]
        assert testobj.get_focus_widget_for_tab(0) == 'p0list'
        assert testobj.get_focus_widget_for_tab(1) == 'proc_entry'
        assert testobj.get_focus_widget_for_tab(2) == 'progress_list'

    def test_enable_book_navigation(self, monkeypatch, capsys):
        """unittest for MainWindow.enable_book_navigation
        """
        def mock_get(*args):
            print('called MainGui.get_tab_count with args', args)
            return 2
        def mock_enable(*args):
            print('called MainGui.enable_tab with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.get_tab_count = mock_get
        testobj.gui.enable_tab = mock_enable
        testobj.enable_book_navigation('state')
        assert capsys.readouterr().out == (
                f"called MainGui.get_tab_count with args ({testobj.book},)\n"
                f"called MainGui.enable_tab with args ({testobj.book}, 0, 'state')\n"
                f"called MainGui.enable_tab with args ({testobj.book}, 1, 'state')\n")
        testobj.enable_book_navigation('state', tabfrom=1, tabto=3)
        assert capsys.readouterr().out == (
                f"called MainGui.enable_tab with args ({testobj.book}, 1, 'state')\n"
                f"called MainGui.enable_tab with args ({testobj.book}, 2, 'state')\n")

    def test_enable_all_book_tabs(self, monkeypatch, capsys):
        """unittest for MainWindow.enable_all_book_tabs
        """
        def mock_enable(*args, **kwargs):
            print('called MainGui.enable_book_navigation with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.enable_book_navigation = mock_enable
        testobj.enable_all_book_tabs(True)
        assert capsys.readouterr().out == (
                "called MainGui.enable_book_navigation with args (True,) {'tabfrom': 1}\n")

    def test_enable_all_other_tabs(self, monkeypatch, capsys):
        """unittest for MainWindow.enable_all_other_tabs
        """
        def mock_get(*args):
            print('called MainGui.get_tab_count with args', args)
            return 3
        def mock_enable(*args):
            print('called MainGui.enable_tab with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.get_tab_count = mock_get
        testobj.gui.enable_tab = mock_enable
        testobj.book.current_tab = 1
        testobj.enable_all_other_tabs('state')
        assert capsys.readouterr().out == (
                f"called MainGui.get_tab_count with args ({testobj.book},)\n"
                f"called MainGui.enable_tab with args ({testobj.book}, 0, 'state')\n"
                f"called MainGui.enable_tab with args ({testobj.book}, 2, 'state')\n")


class TestPage:
    """unittests for main.Page
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.Page object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Page.__init__ with args', args)
        monkeypatch.setattr(testee.Page, '__init__', mock_init)
        testobj = testee.Page()
        testobj.book = types.SimpleNamespace(tabs={0: "0 start", 1: "1 vervolg", 2: "2 rest"},
                                             pagedata=MockActie(), count=lambda *x: 3,
                                             fnaam='testfile', newitem=False)
        testobj.appbase = MockMainWindow()
        testobj.gui = MockPageGui()
        assert capsys.readouterr().out == ("called Page.__init__ with args ()\n"
                                           "called MainWindow.__init__() with args ()\n"
                                           "called MainGui.__init__()\n"
                                           'called PageGui.__init__() with args () {}\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Page.__init__
        """
        # def mock_create(self, *args):
        #     """stub
        #     """
        #     print('called PageGui.create_buttons with args', args)
        #     return 'savebutton', 'savepgobutton', 'cancelbutton'
        def mock_get(self, *args):
            print('called Page.get_toolbar_data with args', args)
            return 'toolbar data'
        appbase = MockMainWindow()
        parent = MockBook()
        parent.parent = appbase
        assert capsys.readouterr().out == ('called MainWindow.__init__() with args ()\n'
                                           'called MainGui.__init__()\n')
        # monkeypatch.setattr(MockPageGui, 'create_buttons', mock_create)
        monkeypatch.setattr(testee.gui, 'PageGui', MockPageGui)
        monkeypatch.setattr(testee.Page, 'get_toolbar_data', mock_get)
        appbase.use_rt = False
        testobj = testee.Page(parent, 'pageno')
        assert testobj.book == parent
        assert testobj.appbase == appbase
        assert testobj.pageno == 'pageno'
        assert testobj.is_text_page
        assert hasattr(testobj, 'gui')
        assert testobj.text1 == 'text1'
        assert not hasattr(testobj, 'toolbar')
        assert testobj.save_button == 'Sla wijzigingen op (Ctrl-S)'
        assert testobj.saveandgo_button == 'Sla op en ga verder (Ctrl-G)'
        assert testobj.cancel_button == 'Zet originele tekst terug (Alt-Ctrl-Z)'
        assert capsys.readouterr().out == (
            f"called PageGui.__init__() with args ({parent}, {testobj}) {{}}\n"
            "called PageGui.start_display\n"
            f"called PageGui.create_text_field with args ('sizer', 490, 330, {testobj.on_text})\n"
            "called PageGui.create_buttons with args"
            f" ([('Sla wijzigingen op (Ctrl-S)', {testobj.savep}),"
            f" ('Sla op en ga verder (Ctrl-G)', {testobj.savepgo}),"
            f" ('Zet originele tekst terug (Alt-Ctrl-Z)', {testobj.restorep})], 'sizer')\n"
            "called PageGui.add_keybind with args"
            f" ('Alt-N', {testobj.nieuwp}) {{'last': True}}\n")
        appbase.use_rt = True
        testobj = testee.Page(parent, 'pageno')
        assert testobj.book == parent
        assert testobj.appbase == appbase
        assert testobj.pageno == 'pageno'
        assert testobj.is_text_page
        assert hasattr(testobj, 'gui')
        assert testobj.toolbar == 'toolbar'
        assert testobj.save_button == 'Sla wijzigingen op (Ctrl-S)'
        assert testobj.saveandgo_button == 'Sla op en ga verder (Ctrl-G)'
        assert testobj.cancel_button == 'Zet originele tekst terug (Alt-Ctrl-Z)'
        assert capsys.readouterr().out == (
            f"called PageGui.__init__() with args ({parent}, {testobj}) {{}}\n"
            "called PageGui.start_display\n"
            f"called PageGui.create_text_field with args ('sizer', 490, 330, {testobj.on_text})\n"
            "called Page.get_toolbar_data with args ('text1',)\n"
            "called PageGui.create_toolbar with args ('sizer', 'text1', 'toolbar data')\n"
            "called PageGui.create_buttons with args"
            f" ([('Sla wijzigingen op (Ctrl-S)', {testobj.savep}),"
            f" ('Sla op en ga verder (Ctrl-G)', {testobj.savepgo}),"
            f" ('Zet originele tekst terug (Alt-Ctrl-Z)', {testobj.restorep})], 'sizer')\n"
            "called PageGui.add_keybind with args"
            f" ('Alt-N', {testobj.nieuwp}) {{'last': True}}\n")

        testobj = testee.Page(parent, 'pageno', standard=False)
        assert testobj.book == parent
        assert testobj.pageno == 'pageno'
        assert not testobj.is_text_page
        assert not hasattr(testobj, 'gui')
        assert capsys.readouterr().out == ''

    def test_get_toolbar_data(self, monkeypatch, capsys):
        """unittest for Page.get_toolbar_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
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

    def test_vulp(self, monkeypatch, capsys):
        """unittest for Page.vulp
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.seltitel = 'hallo'
        testobj.appbase.is_user = True
        testobj.appbase.title = 'aha'
        testobj.book.newitem = False
        testobj.book.current_tab = 0
        testobj.vulp()
        assert capsys.readouterr().out == (
                'call MainWindow.set_windowtitle(aha | hallo)\n'
                'call MainWindow.set_statusmessage()\n'
                'called MainWindow.enable_all_other_tabs() with arg `True`\n')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.seltitel = 'hallo'
        testobj.appbase.is_user = True
        testobj.appbase.title = 'aha'
        testobj.book.current_tab = 1
        testobj.book.newitem = True
        testobj.appbase.use_separate_subject = False
        testobj.vulp()
        assert capsys.readouterr().out == (
                'call MainWindow.set_windowtitle(aha | xx titel)\n'
                'call MainWindow.set_statusmessage()\n'
                'called MainWindow.enable_all_other_tabs() with arg `False`\n')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.seltitel = 'hallo'
        testobj.appbase.is_user = True
        testobj.appbase.title = 'aha'
        testobj.book.current_tab = 1
        testobj.book.newitem = False
        testobj.appbase.use_separate_subject = False
        testobj.vulp()
        assert capsys.readouterr().out == (
                'call MainWindow.set_windowtitle(aha | xx titel)\n'
                'call MainWindow.set_statusmessage()\n'
                'called MainWindow.enable_all_other_tabs() with arg `True`\n')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.pages = ['1', '2', '3', '4', '5', '6']
        testobj.book.pagedata.arch = False
        testobj.seltitel = 'hallo'
        testobj.appbase.title = 'aha'
        testobj.appbase.is_user = False
        testobj.appbase.use_rt = False
        testobj.book.current_tab = 2
        testobj.book.newitem = False
        testobj.appbase.use_separate_subject = False
        testobj.text1 = 'text1'
        testobj.toolbar = 'toolbar'
        testobj.vulp()
        assert capsys.readouterr().out == (
                'call MainWindow.set_windowtitle(aha | xx titel)\n'
                'call MainWindow.set_statusmessage()\n'
                "call Page.get_pagetext()\n"
                "call PageGui.set_textarea_contents with args ('text1', 'pagetext')\n"
                "called PageGui.set_text_readonly with args ('text1', True)\n"
                # "call PageGui.enable_toolbar with args ('toolbar', False)\n"
                "call PageGui.get_textarea_contents with args ('text1',)\n"
                "call PageGui.move_cursor_to_end with args ('text1',)\n"
                'called MainWindow.enable_all_other_tabs() with arg `True`\n')
        testobj.appbase.use_rt = True
        testobj.vulp()
        assert capsys.readouterr().out == (
                'call MainWindow.set_windowtitle(aha | xx titel)\n'
                'call MainWindow.set_statusmessage()\n'
                "call Page.get_pagetext()\n"
                "call PageGui.set_textarea_contents with args ('text1', 'pagetext')\n"
                "called PageGui.set_text_readonly with args ('text1', True)\n"
                "call PageGui.enable_toolbar with args ('toolbar', False)\n"
                "call PageGui.get_textarea_contents with args ('text1',)\n"
                "call PageGui.move_cursor_to_end with args ('text1',)\n"
                'called MainWindow.enable_all_other_tabs() with arg `True`\n')
        testobj.book.pagedata.arch = True
        testobj.vulp()
        assert capsys.readouterr().out == (
                'call MainWindow.set_windowtitle(aha | xx titel)\n'
                'call MainWindow.set_statusmessage()\n'
                "call Page.get_pagetext()\n"
                "call PageGui.set_textarea_contents with args ('text1', 'pagetext')\n"
                "called PageGui.set_text_readonly with args ('text1', True)\n"
                "call PageGui.enable_toolbar with args ('toolbar', False)\n"
                "call PageGui.get_textarea_contents with args ('text1',)\n"
                "call PageGui.move_cursor_to_end with args ('text1',)\n"
                'called MainWindow.enable_all_other_tabs() with arg `True`\n')
        testobj.book.pagedata = None
        testobj.vulp()
        assert capsys.readouterr().out == (
                "call MainWindow.set_windowtitle(aha | rest)\n"
                'call MainWindow.set_statusmessage()\n'
                "call PageGui.set_textarea_contents with args ('text1', '')\n"
                "called PageGui.set_text_readonly with args ('text1', True)\n"
                "call PageGui.enable_toolbar with args ('toolbar', False)\n"
                "call PageGui.get_textarea_contents with args ('text1',)\n"
                "call PageGui.move_cursor_to_end with args ('text1',)\n"
                'called MainWindow.enable_all_other_tabs() with arg `True`\n')
        # pagedata = types.SimpleNamespace(id='xx', titel="titel", over='over', arch=True)
        # mock_book = types.SimpleNamespace(parent=MockMainWindow(),
        #                                   tabs={0: "0 start", 1: "1 vervolg", 2: "rest"},
        #                                   pagedata=pagedata, count=lambda *x: 6)
        # assert capsys.readouterr().out == 'called MainWindow.__init__()\n'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.seltitel = 'hallo'
        testobj.book.pages = ['1', '2', '3']
        testobj.appbase.title = ''
        testobj.appbase.is_user = True
        testobj.book.current_tab = 2
        testobj.book.newitem = False
        testobj.appbase.use_separate_subject = True
        testobj.vulp()
        assert capsys.readouterr().out == (
                'call MainWindow.set_windowtitle(xx over - titel)\n'
                'call MainWindow.set_statusmessage()\n'
                'called MainWindow.enable_all_other_tabs() with arg `True`\n')

    def test_get_pagetext(self, monkeypatch, capsys):
        """unittest for Page.get_pagetext
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.current_tab = 2
        assert testobj.get_pagetext() == 'mld'
        testobj.book.current_tab = 3
        assert testobj.get_pagetext() == 'ozk'
        testobj.book.current_tab = 4
        assert testobj.get_pagetext() == 'opl'
        testobj.book.current_tab = 5
        assert testobj.get_pagetext() == 'vv'

    def test_readp(self, monkeypatch, capsys):
        """unittest for Page.readp
        """
        class MockActie2:
            """stub, nog uitzoeken hoe dit gecombineerd kan worden met de andere MockActie
            """
            def __init__(self, *args):
                print('called Actie.__init__() with args', args)
                self.id = '1'
                self.imagelist = ['1', '2']
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.shared, 'Actie', {'X': MockActie2})
        testobj.book.fnaam = 'fnaam'
        testobj.appbase.datatype = 'X'
        testobj.appbase.user = 'user1'
        testobj.readp('15')
        assert testobj.appbase.imagelist == ['1', '2']
        assert testobj.book.old_id == '1'
        assert not testobj.book.newitem
        assert capsys.readouterr().out == ('called Actie.cleanup()\n'
                                           "called Actie.__init__() with args ('fnaam', '15', 'user1')\n")
        testobj.book.pagedata = None
        testobj.readp('15')
        assert testobj.appbase.imagelist == ['1', '2']
        assert testobj.book.old_id == '1'
        assert not testobj.book.newitem
        assert capsys.readouterr().out == "called Actie.__init__() with args ('fnaam', '15', 'user1')\n"

    def test_nieuwp(self, monkeypatch, capsys):
        """unittest for Page.nieuwp
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
        def mock_show(*args):
            print('called gui.show_message with args', args)
        monkeypatch.setattr(testee.Page, 'vulp', mock_vulp)
        monkeypatch.setattr(testee.Page, 'goto_page', mock_goto_page)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.shared, 'Actie', {'X': MockActieN})
        testobj.book.fnaam = 'fnaam'
        testobj.appbase.datatype = 'X'
        testobj.appbase.is_user = False
        testobj.appbase.user = ''
        testobj.proc_entry = 'proc_entry'
        monkeypatch.setattr(testobj, 'leavep', lambda *x: False)
        testobj.nieuwp()
        assert not testobj.book.newitem
        assert capsys.readouterr().out == (
                "called gui.show_message with args"
                f" ({testobj.book}, 'Opvoeren niet toegestaan, u bent niet ingelogd',"
                " 'Navigatie niet toegestaan')\n")
        testobj.appbase.is_user = True
        testobj.appbase.user = 'user1'
        testobj.proc_entry = 'proc_entry'
        monkeypatch.setattr(testobj, 'leavep', lambda *x: False)
        testobj.nieuwp()
        assert not testobj.book.newitem
        assert capsys.readouterr().out == ''

        testobj.book.current_item = 'current_item'
        monkeypatch.setattr(testobj, 'leavep', lambda *x: True)
        testobj.book.current_tab = 0
        testobj.nieuwp()
        assert testobj.book.newitem
        assert testobj.book.oldselection == 'current_item'
        assert capsys.readouterr().out == (
                "called Actie.__init__() with args ('fnaam', 0, 'user1')\n"
                "called Actie.add_event() with args ('Actie opgevoerd',)\n"
                "called Page.goto_page() with args (1,) {'check': False}\n")

        testobj.book.current_tab = 1
        testobj.nieuwp()
        assert testobj.book.newitem
        assert capsys.readouterr().out == (
                "called Actie.__init__() with args ('fnaam', 0, 'user1')\n"
                "called Actie.add_event() with args ('Actie opgevoerd',)\n"
                "called Page.vulp()\n"
                "called PageGui.set_focus_to_field(proc_entry)\n")

    def test_leavep(self, monkeypatch, capsys):
        """unittest for Page.leavep
        """
        def mock_abort():
            print('called Page.abort_add')
        def mock_show_message(win, msg, title):
            """stub
            """
            print(f'called gui.show_message with args `{title}` `{msg}`')
        def mock_ask_question(win, msg):
            """stub
            """
            print(f'called gui.ask_cancel_question with arg `{msg}`')
            return True, False
        def mock_ask_question_no(win, msg):
            """stub
            """
            print(f'called gui.ask_cancel_question with arg `{msg}`')
            return False, False
        def mock_ask_question_cancel(win, msg):
            """stub
            """
            print(f'called gui.ask_cancel_question with arg `{msg}`')
            return False, True
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.abort_add = mock_abort
        testobj.book.current_tab = 0
        testobj.book.current_item = 0
        testobj.book.oldselection = 'old selection'
        testobj.appbase.title = 'apptitle'
        testobj.appbase.exiting = True
        assert testobj.leavep(1)
        testobj.appbase.exiting = False
        assert not testobj.leavep(1)
        assert capsys.readouterr().out == (
                'called gui.show_message with args `Navigatie niet toegestaan`'
                ' `Selecteer eerst een actie`\n')
        testobj.book.current_item = 1
        testobj.book.fnaam = ''
        testobj.appbase.multiple_files = True
        assert not testobj.leavep(1)
        assert capsys.readouterr().out == (
                'called gui.show_message with args `Navigatie niet toegestaan`'
                ' `Kies eerst een bestand om mee te werken`\n')
        testobj.appbase.multiple_files = False
        testobj.appbase.multiple_projects = True
        assert not testobj.leavep(1)
        assert capsys.readouterr().out == (
                'called gui.show_message with args `Navigatie niet toegestaan`'
                ' `Kies eerst een project om mee te werken`\n')
        # deze test bewust uitgezet om deze situatie niet ongemerkt langs te laten komen
        # testobj.appbase.multiple_projects = False
        # with pytest.raises(ValueError) as exception:
        #     testobj.leavep(1)
        # assert str(exception.value) == ('ProgrammingError: fnaam should only be empty'
        #                                  ' with multiple files or projects')
        # testobj.appbase.multiple_projects = True

        testobj.book.fnaam = 'something'
        testobj.book.data = {}
        testobj.book.newitem = False
        assert not testobj.leavep(1)
        assert capsys.readouterr().out == (
                'called gui.show_message with args `Navigatie niet toegestaan`'
                ' `Voer eerst één of meer acties op`\n')
        testobj.book.data = 'anything'
        testobj.book.current_item = -1
        assert not testobj.leavep(1)
        assert capsys.readouterr().out == (
                'called gui.show_message with args `Navigatie niet toegestaan`'
                ' `Selecteer eerst een actie`\n')
        testobj.book.current_item = 1
        assert testobj.leavep(1)
        assert capsys.readouterr().out == ''

        testobj.book.current_tab = 1
        testobj.book.newitem = True
        assert not testobj.leavep(0)
        assert capsys.readouterr().out == 'called Page.abort_add\n'
        assert testobj.leavep(1)
        assert capsys.readouterr().out == ''
        assert not testobj.leavep(2)
        assert capsys.readouterr().out == (
                "called gui.show_message with args"
                " `apptitle` `Nieuwe actie: navigatie naar vervolgpagina's niet toegestaan`\n")

        testobj.book.newitem = False
        testobj.oldbuf = ['x']
        testobj.book.changed_item = False
        assert testobj.leavep(1)
        assert capsys.readouterr().out == ''

        testobj.book.changed_item = True
        monkeypatch.setattr(testee.gui, 'ask_cancel_question', mock_ask_question)
        monkeypatch.setattr(testobj, 'savep', lambda *x: True)
        assert testobj.leavep(1)
        assert capsys.readouterr().out == (
                'called gui.ask_cancel_question with arg '
                '`De gegevens op de pagina zijn gewijzigd,\n'
                'wilt u de wijzigingen opslaan voordat u verder gaat?`\n'
                'called MainWindow.enable_all_other_tabs() with arg `True`\n')

        monkeypatch.setattr(testee.gui, 'ask_cancel_question', mock_ask_question_cancel)
        assert not testobj.leavep(1)
        assert capsys.readouterr().out == (
                'called gui.ask_cancel_question with arg '
                '`De gegevens op de pagina zijn gewijzigd,\n'
                'wilt u de wijzigingen opslaan voordat u verder gaat?`\n')

        monkeypatch.setattr(testee.gui, 'ask_cancel_question', mock_ask_question_no)
        assert testobj.leavep(1)
        assert capsys.readouterr().out == (
                'called gui.ask_cancel_question with arg '
                '`De gegevens op de pagina zijn gewijzigd,\n'
                'wilt u de wijzigingen opslaan voordat u verder gaat?`\n'
                'called MainWindow.enable_all_other_tabs() with arg `True`\n')

    def test_savep(self, monkeypatch, capsys):
        """unittest for Page.savep
        """
        def mock_is_enabled(arg):
            print(f"called PageGui.is_enabled with arg '{arg}'")
            return True
        def mock_enable_buttons(self, value):
            """stub
            """
            print(f'called Page.enable_buttons({value})')
        def mock_update_actie(self):
            """stub
            """
            print('called Page.update_actie()')
        def mock_get_melding(self, *args):
            print('call PageGui.get_textarea_contents with args', args)
            return testobj.book.pagedata.melding
        def mock_get_oorzaak(self, *args):
            print('call PageGui.get_textarea_contents with args', args)
            return testobj.book.pagedata.oorzaak
        def mock_get_oplossing(self, *args):
            print('call PageGui.get_textarea_contents with args', args)
            return testobj.book.pagedata.oplossing
        def mock_get_vervolg(self, *args):
            print('call PageGui.get_textarea_contents with args', args)
            return testobj.book.pagedata.vervolg
        monkeypatch.setattr(testee.Page, 'enable_buttons', mock_enable_buttons)
        monkeypatch.setattr(testee.Page, 'update_actie', mock_update_actie)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.save_button = 'save button'
        assert not testobj.savep()
        assert capsys.readouterr().out == "called PageGui.is_enabled with arg 'save button'\n"

        testobj.gui.is_enabled = mock_is_enabled
        testobj.book.current_tab = 0
        assert not testobj.savep()
        assert capsys.readouterr().out == ("called PageGui.is_enabled with arg 'save button'\n"
                                           'called Page.enable_buttons(False)\n')

        testobj.book.current_tab = 1
        assert not testobj.savep()
        assert capsys.readouterr().out == ("called PageGui.is_enabled with arg 'save button'\n"
                                           'called Page.enable_buttons(False)\n')

        testobj.book.current_tab = 6
        assert not testobj.savep()
        assert capsys.readouterr().out == ("called PageGui.is_enabled with arg 'save button'\n"
                                           'called Page.enable_buttons(False)\n')

        testobj.book.current_tab = 2
        testobj.appbase.use_text_panels = False
        assert not testobj.savep()
        assert capsys.readouterr().out == ("called PageGui.is_enabled with arg 'save button'\n"
                                           'called Page.enable_buttons(False)\n')

        testobj.appbase.use_text_panels = True
        testobj.oldbuf = ''
        testobj.text1 = 'text1'
        monkeypatch.setattr(testobj.gui, 'get_textarea_contents', mock_get_melding)
        assert testobj.savep()   # niet saven, wel true?
        assert testobj.oldbuf == ''
        assert capsys.readouterr().out == (
                "called PageGui.is_enabled with arg 'save button'\n"
                'called Page.enable_buttons(False)\n'
                "call PageGui.get_textarea_contents with args ()\n")
        monkeypatch.setattr(testobj.gui, 'get_textarea_contents', MockPageGui.get_textarea_contents)
        assert testobj.savep()
        assert testobj.oldbuf == 'text'
        assert capsys.readouterr().out == (
                "called PageGui.is_enabled with arg 'save button'\n"
                'called Page.enable_buttons(False)\n'
                "call PageGui.get_textarea_contents with args ()\n"
                "called Actie.add_event() with args ('Meldingtekst aangepast',)\n"
                'called Page.update_actie()\n')

        testobj.book.current_tab = 3
        testobj.oldbuf = ''
        monkeypatch.setattr(testobj.gui, 'get_textarea_contents', mock_get_oorzaak)
        assert testobj.savep()   # niet saven, wel true?
        assert testobj.oldbuf == ''
        assert capsys.readouterr().out == ("called PageGui.is_enabled with arg 'save button'\n"
                                           'called Page.enable_buttons(False)\n'
                                           "call PageGui.get_textarea_contents with args ()\n")
        monkeypatch.setattr(testobj.gui, 'get_textarea_contents', MockPageGui.get_textarea_contents)
        assert testobj.savep()
        assert testobj.oldbuf == 'text'
        assert capsys.readouterr().out == (
                "called PageGui.is_enabled with arg 'save button'\n"
                'called Page.enable_buttons(False)\n'
                "call PageGui.get_textarea_contents with args ()\n"
                "called Actie.add_event() with args ('Beschrijving oorzaak aangepast',)\n"
                'called Page.update_actie()\n')

        testobj.book.current_tab = 4
        testobj.oldbuf = ''
        monkeypatch.setattr(testobj.gui, 'get_textarea_contents', mock_get_oplossing)
        assert testobj.savep()   # niet saven, wel true?
        assert testobj.oldbuf == ''
        assert capsys.readouterr().out == ("called PageGui.is_enabled with arg 'save button'\n"
                                           'called Page.enable_buttons(False)\n'
                                           "call PageGui.get_textarea_contents with args ()\n")
        monkeypatch.setattr(testobj.gui, 'get_textarea_contents', MockPageGui.get_textarea_contents)
        assert testobj.savep()
        assert testobj.oldbuf == 'text'
        assert capsys.readouterr().out == (
                "called PageGui.is_enabled with arg 'save button'\n"
                'called Page.enable_buttons(False)\n'
                "call PageGui.get_textarea_contents with args ()\n"
                "called Actie.add_event() with args ('Beschrijving oplossing aangepast',)\n"
                'called Page.update_actie()\n')

        testobj.book.current_tab = 5
        testobj.oldbuf = ''
        monkeypatch.setattr(testobj.gui, 'get_textarea_contents', mock_get_vervolg)
        assert testobj.savep()   # niet saven, wel true?
        assert testobj.oldbuf == ''
        assert capsys.readouterr().out == ("called PageGui.is_enabled with arg 'save button'\n"
                                           'called Page.enable_buttons(False)\n'
                                           "call PageGui.get_textarea_contents with args ()\n")
        monkeypatch.setattr(testobj.gui, 'get_textarea_contents', MockPageGui.get_textarea_contents)
        assert testobj.savep()
        assert testobj.oldbuf == 'text'
        assert capsys.readouterr().out == (
                "called PageGui.is_enabled with arg 'save button'\n"
                'called Page.enable_buttons(False)\n'
                "call PageGui.get_textarea_contents with args ()\n"
                "called Actie.add_event() with args ('Tekst vervolgactie aangepast',)\n"
                'called Page.update_actie()\n')

    def test_savepgo(self, monkeypatch, capsys):
        """unittest for Page.savepgo
        """
        def mock_is_enabled(arg):
            print(f"called PageGui.is_enabled with arg '{arg}'")
            return True
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.saveandgo_button = 'saveandgo button'
        testobj.savepgo()
        assert capsys.readouterr().out == "called PageGui.is_enabled with arg 'saveandgo button'\n"
        monkeypatch.setattr(testobj.gui, 'is_enabled', mock_is_enabled)
        testobj.savepgo()
        assert capsys.readouterr().out == ("called PageGui.is_enabled with arg 'saveandgo button'\n"
                                           'called Page.savep()\n'
                                           'called Page.goto_next()\n')
        monkeypatch.setattr(testobj, 'savep', lambda *x: False)
        testobj.savepgo()
        assert capsys.readouterr().out == ("called PageGui.is_enabled with arg 'saveandgo button'\n"
                                           'called Page.enable_buttons(False)\n')

    def test_restorep(self, monkeypatch, capsys):
        """unittest for Page.restorep
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.reset_font = mock_reset_font
        testobj.appbase.use_rt = True
        testobj.book.pagedata.status = '1'
        testobj.book.current_tab = 1
        testobj.book.pages = ['1', '2', '3']
        testobj.restorep()
        assert testobj.book.pagedata.status == '1'
        assert capsys.readouterr().out == 'called Page.vulp()\n'
        testobj.book.current_tab = 2
        testobj.status_auto_changed = False
        testobj.restorep()
        assert testobj.book.pagedata.status == '1'
        assert capsys.readouterr().out == 'called PageGui.reset_font()\ncalled Page.vulp()\n'
        testobj.appbase.use_rt = False
        testobj.restorep()
        assert testobj.book.pagedata.status == '1'
        assert capsys.readouterr().out == 'called Page.vulp()\n'
        testobj.status_auto_changed = True
        testobj.book.current_tab = 1
        testobj.restorep()
        assert testobj.book.pagedata.status == '1'
        assert capsys.readouterr().out == 'called Page.vulp()\n'
        testobj.book.current_tab = 2
        testobj.restorep()
        assert testobj.book.pagedata.status == '0'
        assert capsys.readouterr().out == 'called Page.vulp()\n'

    def test_on_text(self, monkeypatch, capsys):
        """unittest for Page.on_text
        """
        def mock_build(self):
            print('called Page.build_newbuf')
            return self.oldbuf
        def mock_build_2(self):
            print('called Page.build_newbuf')
            return 'new text'
        def mock_enable_buttons(self, value=False):
            """stub
            """
            print(f'called Page.enable_buttons({value})')
        monkeypatch.setattr(testee.Page, 'enable_buttons', mock_enable_buttons)
        monkeypatch.setattr(testee.Page, 'build_newbuf', mock_build)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.initializing = True
        testobj.on_text()
        assert capsys.readouterr().out == ''
        testobj.initializing = False
        testobj.oldbuf = 'oldbuf'
        testobj.on_text()
        assert capsys.readouterr().out == ('called Page.build_newbuf\n'
                                           'called Page.enable_buttons(False)\n')
        monkeypatch.setattr(testee.Page, 'build_newbuf', mock_build_2)
        testobj.on_text()
        assert capsys.readouterr().out == ('called Page.build_newbuf\n'
                                           'called Page.enable_buttons(True)\n')

    def test_build_newbuf(self, monkeypatch, capsys):
        """unittest for Page.build_newbuf
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.text1 = 'text1'
        assert testobj.build_newbuf() == "text"
        assert capsys.readouterr().out == (
                "call PageGui.get_textarea_contents with args ('text1',)\n")

    def test_update_actie(self, monkeypatch, capsys):
        """unittest for Page.update_actie
        """
        class MockPageGui:
            """stub
            """
            def __init__(self, pageno):
                self.pageno = pageno
            def get_textfield_value(self, *args):
                """stub
                """
                print(f'called Page{self.pageno}Gui.get_textfield_value with args', args)
                return args[0]
            def get_choice_data(self, *args):
                """stub
                """
                print(f'called Page{self.pageno}Gui.get_choice_data with args', args)
                return args[0], ''
            def set_item_text(self, *args):
                """stub
                """
                print(f'called Page{self.pageno}Gui.set_item_text with args', args)
            def add_listitem(self, *args):
                """stub
                """
                print(f'called Page{self.pageno}Gui.add_listitem with args', args)
                return 'new listitem'
            def set_selection(self, *args):
                """stub
                """
                print(f'called Page{self.pageno}Gui.set_selection with args', args)
            def get_selection(self, *args):
                """stub
                """
                print(f'called Page{self.pageno}Gui.get_selection with args', args)
                return 'selection'
        class MockPage0:
            """stub
            """
            def __init__(self):
                self.gui = MockPageGui(0)
                self.p0list = 'p0list'
        class MockPage1:
            """stub
            """
            def __init__(self):
                self.gui = MockPageGui(1)

        testobj = self.setup_testobj(monkeypatch, capsys)

        image_count = 9
        testobj.appbase.imagecount = image_count
        testobj.appbase.imagelist = ['image', 'list']
        testobj.book.pagedata.id = 1
        testobj.book.pagedata.status = '0'
        testobj.book.pagedata.updated = 'now'
        testobj.book.pagedata.over = 'about'
        testobj.book.pagedata.titel = 'title'
        testobj.book.stats = {0: ('Started', '0'), 1: ('Accepted', '1')}
        testobj.appbase.use_text_panels = False
        testobj.book.current_tab = 0
        testobj.appbase.work_with_user = False
        testobj.book.newitem = True
        testobj.book.data = {}
        testobj.book.pages = [MockPage0(), MockPage1()]
        testobj.id_text = 'id'
        testobj.date_text = 'date'
        testobj.proc_entry = 'proc'
        testobj.desc_entry = 'desc'
        testobj.stat_choice = 'stat'
        testobj.cat_choice = 'cat'
        testobj.update_actie()
        assert testobj.book.pagedata.imagecount == image_count
        assert testobj.book.pagedata.imagelist == ['image', 'list']
        assert testobj.book.data == {0: ('date', 'proc - desc', 'stat', 'cat', 'id')}
        assert testobj.book.current_item == 'new listitem'
        assert not testobj.book.newitem
        assert testobj.book.rereadlist
        assert capsys.readouterr().out == (
                'called Actie.write() with args ()\n'
                'called Actie.read()\n'
                "called Page1Gui.get_textfield_value with args ('date',)\n"
                "called Page1Gui.get_textfield_value with args ('proc',)\n"
                "called Page1Gui.get_textfield_value with args ('desc',)\n"
                "called Page1Gui.get_choice_data with args ('stat',)\n"
                "called Page1Gui.get_choice_data with args ('cat',)\n"
                "called Page1Gui.get_textfield_value with args ('id',)\n"
                "called Page0Gui.add_listitem with args ('date',)\n"
                "called Page0Gui.set_selection with args ('p0list',)\n")

        testobj.appbase.imagecount = image_count
        testobj.appbase.imagelist = ['image', 'list']
        testobj.book.pagedata.status = '1'
        testobj.appbase.use_text_panels = True
        testobj.book.current_tab = 2
        testobj.appbase.work_with_user = True
        testobj.appbase.user = 'my_user'
        testobj.book.newitem = False
        testobj.appbase.use_separate_subject = False

        testobj.update_actie()
        assert testobj.book.pagedata.imagecount == image_count
        assert testobj.book.pagedata.imagelist == ['image', 'list']
        assert capsys.readouterr().out == (
                "called Actie.write() with args ('my_user',)\n"
                "called Actie.read()\n"
                "called Page0Gui.get_selection with args ('p0list',)\n"
                "called Page0Gui.set_item_text with args ('selection', 1, 'S')\n"
                "called Page0Gui.set_item_text with args ('selection', 2, 'statustext')\n"
                "called Page0Gui.set_item_text with args ('selection', 3, 'now')\n"
                "called Page0Gui.set_item_text with args ('selection', 4, 'title')\n")

        testobj.appbase.imagecount = image_count
        testobj.appbase.imagelist = ['image', 'list']
        testobj.book.pagedata.status = '0'
        testobj.appbase.use_text_panels = True
        testobj.book.current_tab = 3
        testobj.appbase.work_with_user = True
        testobj.appbase.user = 'my_user'
        testobj.book.newitem = False
        testobj.appbase.use_separate_subject = True

        testobj.update_actie()
        assert testobj.book.pagedata.imagecount == image_count
        assert testobj.book.pagedata.imagelist == ['image', 'list']
        assert capsys.readouterr().out == (
                'called Actie.add_event() with args (\'Status gewijzigd in "Accepted"\',)\n'
                "called Actie.write() with args ('my_user',)\n"
                "called Actie.read()\n"
                "called Page0Gui.get_selection with args ('p0list',)\n"
                "called Page0Gui.set_item_text with args ('selection', 1, 'S')\n"
                "called Page0Gui.set_item_text with args ('selection', 2, 'statustext')\n"
                "called Page0Gui.set_item_text with args ('selection', 3, 'now')\n"
                "called Page0Gui.set_item_text with args ('selection', 4, 'about')\n"
                "called Page0Gui.set_item_text with args ('selection', 5, 'title')\n")

    def test_enable_buttons(self, monkeypatch, capsys):
        """unittest for Page.enable_buttons
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.save_button = 'save'
        testobj.saveandgo_button = 'saveandgo'
        testobj.cancel_button = 'cancel'
        testobj.book.pages = ['Page0', 'Page1']
        testobj.book.current_tab = 0
        testobj.enable_buttons(True)
        assert testobj.book.changed_item
        assert capsys.readouterr().out == (
                "called PageGui.enable_widget with args ('save', True)\n"
                "called PageGui.enable_widget with args ('saveandgo', True)\n"
                "called PageGui.enable_widget with args ('cancel', True)\n")
        testobj.book.current_tab = 1
        testobj.enable_buttons(False)
        assert not testobj.book.changed_item
        assert capsys.readouterr().out == (
                "called PageGui.enable_widget with args ('save', False)\n"
                "called PageGui.enable_widget with args ('cancel', False)\n"
                'called MainWindow.enable_all_other_tabs() with arg `True`\n')

    def test_goto_actie(self, monkeypatch, capsys):
        """unittest for Page.goto_actie
        """
        def mock_goto_page(self, value=False):
            """stub
            """
            print(f'called Page.goto_page({value})')
        monkeypatch.setattr(testee.Page, 'goto_page', mock_goto_page)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.goto_actie()
        assert capsys.readouterr().out == ('called Page.goto_page(1)\n')

    def test_goto_next(self, monkeypatch, capsys):
        """unittest for Page.goto_next
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.current_tab = 2
        testobj.book.pages = [0, 1, 2]
        monkeypatch.setattr(testobj, 'leavep', lambda *x: False)
        testobj.goto_next()
        assert capsys.readouterr().out == ''
        monkeypatch.setattr(testobj, 'leavep', lambda *x: True)
        testobj.goto_next()
        assert capsys.readouterr().out == f'called MainGui.set_page with args ({testobj.book}, 0)\n'
        testobj.book.current_tab = 0
        testobj.goto_next()
        assert capsys.readouterr().out == f'called MainGui.set_page with args ({testobj.book}, 1)\n'

    def test_goto_prev(self, monkeypatch, capsys):
        """unittest for Page.goto_prev
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.current_tab = 2
        testobj.book.pages = [0, 1, 2]
        monkeypatch.setattr(testobj, 'leavep', lambda *x: False)
        testobj.goto_prev()
        assert capsys.readouterr().out == ''
        monkeypatch.setattr(testobj, 'leavep', lambda *x: True)
        testobj.goto_prev()
        assert capsys.readouterr().out == f'called MainGui.set_page with args ({testobj.book}, 1)\n'
        testobj.book.current_tab = 0
        testobj.goto_prev()
        assert capsys.readouterr().out == f'called MainGui.set_page with args ({testobj.book}, 2)\n'

    def test_goto_page(self, monkeypatch, capsys):
        """unittest for Page.goto_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.pages = [0, 1, 2]
        testobj.goto_page(1, check=False)
        assert capsys.readouterr().out == f'called MainGui.set_page with args ({testobj.book}, 1)\n'
        monkeypatch.setattr(testobj, 'leavep', lambda *x: False)
        testobj.goto_page(1)
        assert capsys.readouterr().out == ''
        monkeypatch.setattr(testobj, 'leavep', lambda *x: True)
        testobj.goto_page(1)
        assert capsys.readouterr().out == f'called MainGui.set_page with args ({testobj.book}, 1)\n'
        testobj.goto_page(-1)
        assert capsys.readouterr().out == ''
        testobj.goto_page(3)
        assert capsys.readouterr().out == ''

    def test_get_textarea_contents(self, monkeypatch, capsys):
        """unittest for Page.get_textarea_contents
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.text1 = 'text1'
        assert testobj.get_textarea_contents() == 'text'
        assert capsys.readouterr().out == "call PageGui.get_textarea_contents with args ('text1',)\n"

    def test_abort_add(self, monkeypatch, capsys):
        """unittest for Page.abort_add
        """
        def mock_ask(*args):
            print('called gui.ask_question with args', args)
            return False
        def mock_ask_2(*args):
            print('called gui.ask_question with args', args)
            return True
        monkeypatch.setattr(testee.gui, 'ask_question', mock_ask)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.newitem = True
        testobj.book.oldselection = 'old selection'
        assert not testobj.abort_add()
        assert testobj.book.newitem
        assert not hasattr(testobj.book, 'current_item')
        assert capsys.readouterr().out == (
                f"called gui.ask_question with args ({testobj.gui},"
                " 'Weet u zeker dat u het opvoeren van de actie wilt afbreken?')\n")
        monkeypatch.setattr(testee.gui, 'ask_question', mock_ask_2)
        assert testobj.abort_add()
        assert not testobj.book.newitem
        assert testobj.book.current_item == 'old selection'
        assert capsys.readouterr().out == (
                f"called gui.ask_question with args ({testobj.gui},"
                " 'Weet u zeker dat u het opvoeren van de actie wilt afbreken?')\n"
                "called MainWindow.enable_all_other_tabs() with arg `True`\n")


class TestPage0:
    """unittests for main.Page0
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.Page0 object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Page0.__init__ with args', args)
        monkeypatch.setattr(testee.Page0, '__init__', mock_init)
        testobj = testee.Page0()
        testobj.book = types.SimpleNamespace(pagedata=MockActie(), count=lambda *x: 3,
                                             fnaam='testfile')
        testobj.appbase = MockMainWindow()
        testobj.gui = MockPageGui()
        assert capsys.readouterr().out == ('called Page0.__init__ with args ()\n'
                                           'called MainWindow.__init__() with args ()\n'
                                           'called MainGui.__init__()\n'
                                           'called PageGui.__init__() with args () {}\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Page0.__init__
        """
        def mock_enable(self):
            print('called Page0.enable_buttons')
        # def mock_add(self):
        #     print('called PageGui.add_buttons with args', args)
        #     return 'sort', 'filter', 'goto', 'archive', 'new'
        monkeypatch.setattr(testee.gui, 'Page0Gui', MockPageGui)
        monkeypatch.setattr(testee.dmls, 'SortOptions', MockSortOpts)
        monkeypatch.setattr(testee.Page0, 'enable_buttons', mock_enable)
        appbase = MockMainWindow()
        parent = MockBook()
        assert capsys.readouterr().out == ("called MainWindow.__init__() with args ()\n"
                                           "called MainGui.__init__()\n")
        parent.ctitels = ['xxx', 'yyy']
        # p0list = types.SimpleNamespace()
        appbase.use_separate_subject = False
        appbase.work_with_user = False
        appbase.is_user = False
        parent.parent = appbase
        testobj = testee.Page0(parent)
        assert testobj.book == parent
        assert testobj.selection == 'excl. gearchiveerde'
        assert testobj.sel_args == {}
        assert testobj.sorted == (0, "A")
        assert not testobj.sort_via_options
        assert testobj.saved_sortopts is None
        assert isinstance(testobj.p0list, types.SimpleNamespace)
        assert testobj.buttons == ['S&Orteer', 'F&Ilter', '&Ga naar melding', '&Archiveer',
                                   'Voer &Nieuwe melding op']
        assert capsys.readouterr().out == (
            f"called PageGui.__init__() with args ({parent}, {testobj}) {{}}\n"
            "called PageGui.add_list with args (['xxx', 'yyy'], [122, 24, 146, 100, 300])\n"
            f"called PageGui.create_buttons with args"
            f" ([('S&Orteer', {testobj.sort_items}), ('F&Ilter', {testobj.select_items}),"
            f" ('&Ga naar melding', {testobj.goto_actie}), ('&Archiveer', {testobj.archiveer}),"
            f" ('Voer &Nieuwe melding op', {testobj.nieuwp})],)\n"
            "called PageGui.finish_display\n"
            "called Page0.enable_buttons\n")

        # appbase = MockMainWindow()
        # parent = MockBook()
        # assert capsys.readouterr().out == ("called MainWindow.__init__() with args ()\n"
        #                                    "called MainGui.__init__()\n")
        # parent.ctitels = ['xxx', 'yyy']
        # appbase.use_separate_subject = True
        # appbase.work_with_user = True
        # appbase.is_user = True
        appbase.filename = 'fnaam'
        # parent.parent = appbase
        testobj = testee.Page0(parent)
        assert testobj.book == parent
        assert testobj.selection == 'excl. gearchiveerde'
        assert testobj.sel_args == {}
        assert testobj.sorted == (0, "A")
        assert not testobj.sort_via_options
        assert testobj.saved_sortopts is None
        assert isinstance(testobj.p0list, types.SimpleNamespace)
        assert testobj.buttons == ['S&Orteer', 'F&Ilter', '&Ga naar melding', '&Archiveer',
                                   'Voer &Nieuwe melding op']
        assert capsys.readouterr().out == (
            f"called PageGui.__init__() with args ({parent}, {testobj}) {{}}\n"
            "called PageGui.add_list with args (['xxx', 'yyy'], [122, 24, 146, 100, 300])\n"
            f"called PageGui.create_buttons with args"
            f" ([('S&Orteer', {testobj.sort_items}), ('F&Ilter', {testobj.select_items}),"
            f" ('&Ga naar melding', {testobj.goto_actie}), ('&Archiveer', {testobj.archiveer}),"
            f" ('Voer &Nieuwe melding op', {testobj.nieuwp})],)\n"
            "called PageGui.finish_display\n"
            "called Page0.enable_buttons\n")

        monkeypatch.setattr(testee, 'LIN', False)
        # appbase = MockMainWindow()
        # parent = MockBook()
        # assert capsys.readouterr().out == ("called MainWindow.__init__() with args ()\n"
        #                                    "called MainGui.__init__()\n")
        # parent.ctitels = ['xxx', 'yyy']
        appbase.use_separate_subject = False
        # appbase.work_with_user = True
        appbase.is_user = False
        appbase.filename = ""
        # parent.parent = appbase
        testobj = testee.Page0(parent)
        assert testobj.book == parent
        assert testobj.selection == 'excl. gearchiveerde'
        assert testobj.sel_args == {}
        assert testobj.sorted == (0, "A")
        assert not testobj.sort_via_options
        assert testobj.saved_sortopts is None
        assert isinstance(testobj.p0list, types.SimpleNamespace)
        assert testobj.buttons == ['S&Orteer', 'F&Ilter', '&Ga naar melding', '&Archiveer',
                                   'Voer &Nieuwe melding op']
        assert capsys.readouterr().out == (
            f"called PageGui.__init__() with args ({parent}, {testobj}) {{}}\n"
            "called PageGui.add_list with args (['xxx', 'yyy'], [64, 24, 114, 72, 292])\n"
            f"called PageGui.create_buttons with args"
            f" ([('S&Orteer', {testobj.sort_items}), ('F&Ilter', {testobj.select_items}),"
            f" ('&Ga naar melding', {testobj.goto_actie}), ('&Archiveer', {testobj.archiveer}),"
            f" ('Voer &Nieuwe melding op', {testobj.nieuwp})],)\n"
            "called PageGui.finish_display\n"
            "called Page0.enable_buttons\n")

        # appbase = MockMainWindow()
        # parent = MockBook()
        # assert capsys.readouterr().out == ("called MainWindow.__init__() with args ()\n"
        #                                    "called MainGui.__init__()\n")
        # parent.ctitels = ['xxx', 'yyy']
        appbase.use_separate_subject = True
        appbase.work_with_user = False
        appbase.is_user = True
        appbase.filename = 'fnaam'
        # parent.parent = appbase
        testobj = testee.Page0(parent)
        assert testobj.book == parent
        assert testobj.selection == 'excl. gearchiveerde'
        assert testobj.sel_args == {}
        assert testobj.sorted == (0, "A")
        assert not testobj.sort_via_options
        assert testobj.saved_sortopts is None
        assert isinstance(testobj.p0list, types.SimpleNamespace)
        assert testobj.buttons == ['S&Orteer', 'F&Ilter', '&Ga naar melding', '&Archiveer',
                                   'Voer &Nieuwe melding op']
        assert capsys.readouterr().out == (
            f"called PageGui.__init__() with args ({parent}, {testobj}) {{}}\n"
            "called PageGui.add_list with args (['xxx', 'yyy'], [64, 24, 114, 100, 110, 220])\n"
            f"called PageGui.create_buttons with args"
            f" ([('S&Orteer', {testobj.sort_items}), ('F&Ilter', {testobj.select_items}),"
            f" ('&Ga naar melding', {testobj.goto_actie}), ('&Archiveer', {testobj.archiveer}),"
            f" ('Voer &Nieuwe melding op', {testobj.nieuwp})],)\n"
            "called PageGui.finish_display\n"
            "called Page0.enable_buttons\n")

    def test_enable_buttons(self, monkeypatch, capsys):
        """unittest for Page0.enable_buttons
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.buttons = ['sort', 'filter', 'go', 'archive', 'new']
        testobj.appbase.user = 'x'
        testobj.p0list = types.SimpleNamespace(has_selection=True)
        testobj.appbase.is_user = True
        testobj.appbase.filename = 'y'
        testobj.enable_buttons()
        assert capsys.readouterr().out == (
            "called PageGui.enable_widget with args ('filter', True)\n"
            "called PageGui.enable_widget with args ('go', True)\n"
            "called PageGui.enable_widget with args ('new', True)\n"
            "called PageGui.enable_widget with args ('sort', True)\n"
            "called PageGui.enable_widget with args ('archive', True)\n")
        testobj.appbase.user = ''
        testobj.p0list.has_selection = False
        testobj.appbase.is_user = False
        testobj.appbase.filename = 'y'
        testobj.enable_buttons()
        assert capsys.readouterr().out == (
            "called PageGui.enable_widget with args ('filter', False)\n"
            "called PageGui.enable_widget with args ('go', False)\n"
            "called PageGui.enable_widget with args ('new', False)\n"
            "called PageGui.enable_widget with args ('sort', False)\n"
            "called PageGui.enable_widget with args ('archive', False)\n")
        testobj.appbase.user = 'x'
        testobj.p0list.has_selection = True
        testobj.appbase.is_user = True
        testobj.appbase.filename = ''
        testobj.enable_buttons()
        assert capsys.readouterr().out == (
            "called PageGui.enable_widget with args ('filter', True)\n"
            "called PageGui.enable_widget with args ('go', True)\n"
            "called PageGui.enable_widget with args ('new', False)\n"
            "called PageGui.enable_widget with args ('sort', True)\n"
            "called PageGui.enable_widget with args ('archive', True)\n")

    def test_vulp(self, monkeypatch, capsys):
        """unittest for Page0.vulp
        """
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
        def mock_enable():
            print('called Page0.enable_buttons')
        monkeypatch.setattr(testee.Page, 'vulp', mock_super_vulp)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.enable_buttons = mock_enable
        testobj.p0list = types.SimpleNamespace(has_selection=False)

        testobj.appbase.work_with_user = False
        testobj.sort_via_options = False
        testobj.book.rereadlist = False
        testobj.vulp()
        assert testobj.selection == ''
        assert testobj.seltitel == 'alle meldingen '
        assert capsys.readouterr().out == (
                f'called PageGui.enable_sorting with args ({testobj.p0list}, True)\n'
                'called Page.vulp()\n'
                'call MainWindow.enable_all_book_tabs(False)\n'
                'called Page0.enable_buttons\n'
                'call MainWindow.set_statusmessage()\n')

        testobj.appbase.work_with_user = True
        testobj.book.rereadlist = True
        testobj.saved_sortopts = {}
        testobj.selection = ''
        testobj.appbase.startitem = ''
        monkeypatch.setattr(testobj, 'populate_list', mock_populate_list)
        testobj.vulp()
        assert testobj.selection == ''
        assert testobj.seltitel == 'alle meldingen '
        assert capsys.readouterr().out == (
                f'called PageGui.enable_sorting with args ({testobj.p0list}, True)\n'
                'called Page.vulp()\n'
                'called Page0.populate_list()\n'
                f'called PageGui.get_first_item() with args ({testobj.p0list},)\n'
                'call MainWindow.enable_all_book_tabs(False)\n'
                'called Page0.enable_buttons\n'
                "call MainWindow.set_statusmessage(list populated)\n")

        testobj.saved_sortopts = MockSortOptions()
        testobj.vulp()
        assert testobj.selection == 'volgens user gedefinieerde selectie'
        assert testobj.seltitel == 'alle meldingen volgens user gedefinieerde selectie'
        assert capsys.readouterr().out == (
                f'called PageGui.enable_sorting with args ({testobj.p0list}, False)\n'
                'called Page.vulp()\n'
                'call MainWindow.enable_all_book_tabs(False)\n'
                'called Page0.enable_buttons\n'
                'call MainWindow.set_statusmessage()\n')

        testobj.book.rereadlist = True
        testobj.saved_sortopts = MockSortOptions2()
        testobj.p0list.has_selection = lambda *x: True
        testobj.appbase.startitem = 'startitem'
        testobj.vulp()
        assert testobj.selection == 'volgens user gedefinieerde selectie'
        assert testobj.seltitel == 'alle meldingen volgens user gedefinieerde selectie'
        assert capsys.readouterr().out == (
                f'called PageGui.enable_sorting with args ({testobj.p0list}, False)\n'
                'called Page.vulp()\n'
                'called Page0.populate_list()\n'
                f"called PageGui.get_item_by_id() with args ({testobj.p0list}, 'startitem')\n"
                'call MainWindow.enable_all_book_tabs(False)\n'
                'called Page0.enable_buttons\n'
                'call MainWindow.enable_all_book_tabs(True)\n'
                f'called PageGui.set_selection with args ({testobj.p0list},)\n'
                f"called PageGui.ensure_visible with args ({testobj.p0list}, 'item_by_id')\n"
                "call MainWindow.set_statusmessage(list populated)\n")

    def test_populate_list(self, monkeypatch, capsys):
        """unittest for Page0.populate_list
        """
        class MockP0list:
            def __repr__(self):
                return "'p0list'"
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
        def mock_get_acties_other(*args):
            """stub
            """
            print('called dml.get_acties with args', args)
            return [[True],
                    [False]]
        def mock_set(*args):
            print('called Page0.set_listitem_values with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = MockP0list()

        monkeypatch.setattr(testee.shared, 'get_acties', {'7': mock_get_acties_7,
                                                          '8': mock_get_acties_8,
                                                          '10': mock_get_acties_10,
                                                          'other': mock_get_acties_other})
        testobj.set_listitem_values = mock_set
        testobj.book.stats = {0: ('first', '1'), 1: ('second', '2')}
        testobj.book.cats = {0: ('start', '1'), 1: ('next', '2')}
        testobj.appbase.user = 'me'

        testobj.sel_args = {}
        testobj.appbase.datatype = '7'
        testobj.populate_list()
        assert testobj.book.data == {0: ('x0', 'y', 'stat0.0', 'cat0.0', 'r', 'q', True),
                                     1: ('x1', 'y', 'stat0.0', 'cat0.0', 'r', 'q', False)}
        assert capsys.readouterr().out == (
                "called PageGui.clear_list with args ('p0list',)\n"
                "called dml.get_acties with args ('testfile', {}, '', 'me')\n"
                "called PageGui.add_listitem with args ('p0list', 'x0')\n"
                "called Page0.set_listitem_values with args"
                " ('p0list', None, ['x0', 'stat0.0', 'cat0.0', 'r', 'q', True])\n"
                "called PageGui.add_listitem with args ('p0list', 'x1')\n"
                "called Page0.set_listitem_values with args"
                " ('p0list', None, ['x1', 'stat0.0', 'cat0.0', 'r', 'q', False])\n")

        testobj.sel_args = {'arch': 'yes'}
        testobj.appbase.datatype = '8'
        testobj.populate_list()
        assert testobj.book.data == {0: ('x0', 'y', '1.start', '1.first', 'q', 'r', 's', True),
                                     1: ('x1', 'y', '1.start', '1.first', 'q', 'r', 's', False)}
        assert capsys.readouterr().out == (
                "called PageGui.clear_list with args ('p0list',)\n"
                "called dml.get_acties with args ('testfile', {}, 'yes', 'me')\n"
                "called PageGui.add_listitem with args ('p0list', 'x0')\n"
                "called Page0.set_listitem_values with args"
                " ('p0list', None, ['x0', '1.start', '1.first', 'q', 'r', 's', True])\n"
                "called PageGui.add_listitem with args ('p0list', 'x1')\n"
                "called Page0.set_listitem_values with args"
                " ('p0list', None, ['x1', '1.start', '1.first', 'q', 'r', 's', False])\n")

        testobj.sel_args = {'sel': 'args'}
        testobj.appbase.datatype = '10'
        testobj.populate_list()
        assert testobj.book.data == {0: ('x0', 'y', 'b.a', '0.0', 's', 'q', 'r', True),
                                     1: ('x1', 'y', 'b.a', '0.0', 's', 'q', 'r', False)}
        assert capsys.readouterr().out == (
                "called PageGui.clear_list with args ('p0list',)\n"
                "called dml.get_acties with args ('testfile', {'sel': 'args'}, '', 'me')\n"
                "called PageGui.add_listitem with args ('p0list', 'x0')\n"
                "called Page0.set_listitem_values with args"
                " ('p0list', None, ['x0', 'b.a', '0.0', 's', 'q', 'r', True])\n"
                "called PageGui.add_listitem with args ('p0list', 'x1')\n"
                "called Page0.set_listitem_values with args"
                " ('p0list', None, ['x1', 'b.a', '0.0', 's', 'q', 'r', False])\n")
        # deze test bewust uitgezet om deze situatie niet ongemerkt langs te laten komen
        # testobj.sel_args = {'sel': 'args'}
        # testobj.appbase.datatype = 'other'
        # with pytest.raises(ValueError) as exception:
        #     testobj.populate_list()
        # assert str(exception.value) == 'ProgrammingError: Unexpected length of pagedata item'
        # assert capsys.readouterr().out == (
        #         "called PageGui.clear_list()\n"
        #         "called dml.get_acties with args ('testfile', {'sel': 'args'}, '', 'me')\n")

    def test_set_listitem_values(self, monkeypatch, capsys):
        """unittest for Page0.set_listitem_values
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = types.SimpleNamespace()
        testobj.set_listitem_values(p0list, 'item', [])
        assert not p0list.has_selection
        assert capsys.readouterr().out == ""
        testobj.set_listitem_values(p0list, 'item', ('xxx', 'aaa.bbb', 'ccc.ddd', 'eee', False))
        assert p0list.has_selection
        p0list.has_selection = False  # restore pre-test situatie for display
        assert capsys.readouterr().out == (
                f"called PageGui.set_item_text() with args ({p0list}, 'item', 0, 'xxx')\n"
                f"called PageGui.set_item_text() with args ({p0list}, 'item', 1, 'B')\n"
                f"called PageGui.set_item_text() with args ({p0list}, 'item', 2, 'ddd')\n"
                f"called PageGui.set_item_text() with args ({p0list}, 'item', 3, 'eee')\n")
        testobj.set_listitem_values(p0list, 'item', ('yyy', 'p.q', 'r.s', 't', True))
        assert p0list.has_selection
        p0list.has_selection = False  # restore pre-test situatie for display
        assert capsys.readouterr().out == (
                f"called PageGui.set_item_text() with args ({p0list}, 'item', 0, 'yyy (A)')\n"
                f"called PageGui.set_item_text() with args ({p0list}, 'item', 1, 'Q')\n"
                f"called PageGui.set_item_text() with args ({p0list}, 'item', 2, 's')\n"
                f"called PageGui.set_item_text() with args ({p0list}, 'item', 3, 't')\n")

    def test_change_selected(self, monkeypatch, capsys):
        """unittest for Page0.change_selected
        """
        def mock_readp(self, itemno):
            """stub
            """
            print(f'called Page0.readp(`{itemno}`)')
        monkeypatch.setattr(testee.Page0, 'readp', mock_readp)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = 'p0list'
        testobj.book.newitem = True
        testobj.book.pagedata.arch = False
        testobj.buttons = ['xx', 'yy', 'zz', 'arch']
        testobj.change_selected('1')
        assert testobj.book.current_item == '1'
        assert capsys.readouterr().out == (
                "called PageGui.set_selection with args ('p0list',)\n"
                "called PageGui.set_button_text with args ('arch', '&Archiveer')\n")
        testobj.book.newitem = False
        testobj.book.pagedata.arch = True
        testobj.change_selected('1')
        assert testobj.book.current_item == '1'
        assert capsys.readouterr().out == (
                "called PageGui.set_selection with args ('p0list',)\n"
                'called PageGui.get_selected_action with arg p0list\n'
                'called Page0.readp(`1`)\n'
                "called PageGui.set_button_text with args ('arch', '&Herleef')\n")

    def test_activate_item(self, monkeypatch, capsys):
        """unittest for Page0.activate_item
        """
        def mock_goto_actie(self):
            """stub
            """
            print('called Page0.goto_actie()')
        monkeypatch.setattr(testee.Page0, 'goto_actie', mock_goto_actie)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.activate_item()
        assert capsys.readouterr().out == 'called Page0.goto_actie()\n'

    def test_select_items(self, monkeypatch, capsys):
        """unittest for Page0.select_items
        """
        class MockDialog:
            def __init__(self, *args):
                args2 = args[2] if args[2] is None else 'dmls.SelectOptions'
                print(f'called SelectOptionsDialog with args ({args[0]}, {args[1]}, {args2})')
                self.gui = 'SelectOptionsDialogGui'
        class MockSelectOptions:
            """stub
            """
            def __init__(self, *args):
                print('called dmls.SelectOptions.__init__ with args', args)
            def load_options(self):
                """stub
                """
                return {'nummer': [('aaa', 'GT'), ('en',), ('zzz', 'LT')], 'this': 'that'}
        def mock_show_message(win, msg):
            """stub
            """
            print(f'called gui.show_message(`{msg}`)')
        def mock_show_dialog(*args):
            """stub
            """
            print('called gui.show_dialog() with args', args)
            return False
        def mock_show_dialog_ok(*args):
            """stub
            """
            print('called gui.show_dialog() with args', args)
            return True
        counter = 0
        def mock_vulp():
            """stub
            """
            nonlocal counter
            counter += 1
            print('called page0.vulp()')
            if counter == 1:
                raise AttributeError('got a data error')
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog)
        monkeypatch.setattr(testee, 'SelectOptionsDialog', MockDialog)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj.appbase.use_separate_subject = False
        testobj.appbase.work_with_user = False
        testobj.book.parent = 'MainWindow'
        testobj.sel_args = {'sel': 'args'}
        testobj.select_items()
        assert capsys.readouterr().out == (
                "called SelectOptionsDialog with args (MainWindow, {'sel': 'args'}, None)\n"
                "called gui.show_dialog() with args ('SelectOptionsDialogGui',)\n")
        testobj.appbase.use_separate_subject = True
        testobj.appbase.work_with_user = True
        testobj.appbase.user = 'me'
        monkeypatch.setattr(testee.shared, 'DataError', {'x': AttributeError})
        testobj.appbase.datatype = 'x'
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog_ok)
        monkeypatch.setattr(testee.dmls, 'SelectOptions', MockSelectOptions)
        monkeypatch.setattr(testobj, 'vulp', mock_vulp)
        testobj.select_items()
        assert capsys.readouterr().out == (
            "called dmls.SelectOptions.__init__ with args ('testfile', 'me')\n"
            "called SelectOptionsDialog with args (MainWindow,"
            " {'idgt': 'aaa', 'id': 'and', 'idlt': 'zzz', 'this': 'that'}, dmls.SelectOptions)\n"
            "called gui.show_dialog() with args ('SelectOptionsDialogGui',)\n"
            'called page0.vulp()\n'
            "called gui.show_message(`got a data error`)\n"
            "called gui.show_dialog() with args ('SelectOptionsDialogGui',)\n"
            'called page0.vulp()\n')

        monkeypatch.setattr(MockSelectOptions, 'load_options', lambda *x: {'nummer': [('aaa', 'GT'),
                                                                                      ('of',),
                                                                                      ('zzz', 'LT')]})
        monkeypatch.setattr(testee.dmls, 'SelectOptions', MockSelectOptions)
        testobj.select_items()
        assert capsys.readouterr().out == (
                "called dmls.SelectOptions.__init__ with args ('testfile', 'me')\n"
                "called SelectOptionsDialog with args (MainWindow,"
                " {'idgt': 'aaa', 'id': 'or', 'idlt': 'zzz'}, dmls.SelectOptions)\n"
                "called gui.show_dialog() with args ('SelectOptionsDialogGui',)\n"
                'called page0.vulp()\n')
        # deze tests bewust uitgezet om deze situatie niet ongemerkt langs te laten komen
        # monkeypatch.setattr(MockSelectOptions, 'load_options', lambda *x: {'nummer': [('aaa', 'QQ')]})
        # monkeypatch.setattr(testee.dmls, 'SelectOptions', MockSelectOptions)
        # with pytest.raises(ValueError) as exc:
        #     testobj.select_items()
        # assert str(exc.value) == 'ProgrammingError: illegal value in select arguments'
        # monkeypatch.setattr(MockSelectOptions, 'load_options', lambda *x: {'xxx': []})
        # monkeypatch.setattr(testee.dmls, 'SelectOptions', MockSelectOptions)
        # with pytest.raises(ValueError) as exc:
        #     testobj.select_items()
        # assert str(exc.value) == 'ProgrammingError: illegal value in select arguments'

    def test_sort_items(self, monkeypatch, capsys):
        """unittest for Page0.sort_items
        """
        class MockDialog:
            def __init__(self, *args):
                print('called SortOptionsDialog with args', args)
                self.gui = 'SortOptionsDialogGui'
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
        def mock_show_dialog(*args):
            """stub
            """
            print('called gui.show_dialog() with args', args[0])
            return False
        def mock_show_dialog_ok(*args):
            """stub
            """
            print('called gui.show_dialog() with args', args[0])
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
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog)
        monkeypatch.setattr(testee, 'SortOptionsDialog', MockDialog)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.parent = 'MainWindow'
        testobj.saved_sortopts = False
        testobj.sort_items()
        assert capsys.readouterr().out == ('called gui.show_message('
                                           '`Sorry, multi-column sorteren werkt nog niet`)\n')

        testobj.saved_sortopts = MockSortOptions()
        monkeypatch.setattr(testee.dmls.my, 'SORTFIELDS', [])
        testobj.book.ctitels = ['dit', 'dat']
        testobj.sort_items()
        assert capsys.readouterr().out == (
                "called SortOptionsDialog with args"
                " ('MainWindow', {}, ['(geen)', 'dit', 'Soort'])\n"
                "called gui.show_dialog() with args SortOptionsDialogGui\n")

        testobj.saved_sortopts = MockSortOptions2()
        testobj.sort_via_options = False
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog_ok)
        monkeypatch.setattr(testee.dmls.my, 'SORTFIELDS', [('col0', 0), ('col1', 1)])
        testobj.sort_items()
        assert capsys.readouterr().out == (
                "called SortOptionsDialog with args"
                " ('MainWindow', {'sort': 'options'}, ['(geen)', 'col0', 'col1'])\n"
                "called gui.show_dialog() with args SortOptionsDialogGui\n"
                'called PageGui.enable_sorting with args (True,)\n')

        testobj.sort_via_options = True
        monkeypatch.setattr(testobj, 'vulp', mock_vulp)
        testobj.sort_items()
        assert capsys.readouterr().out == (
                "called SortOptionsDialog with args"
                " ('MainWindow', {'sort': 'options'}, ['(geen)', 'col0', 'col1'])\n"
                "called gui.show_dialog() with args SortOptionsDialogGui\n"
                'called PageGui.enable_sorting with args (False,)\n'
                'called Page0.vulp()\n')

        monkeypatch.setattr(testobj, 'vulp', mock_vulp_err)
        monkeypatch.setattr(testee.shared, 'DataError', {'X': AttributeError})
        testobj.appbase.datatype = 'X'
        testobj.sort_items()
        assert capsys.readouterr().out == (
                "called SortOptionsDialog with args"
                " ('MainWindow', {'sort': 'options'}, ['(geen)', 'col0', 'col1'])\n"
                "called gui.show_dialog() with args SortOptionsDialogGui\n"
                'called PageGui.enable_sorting with args (False,)\n'
                'called Page0.vulp()\n'
                'called gui.show_message(`got a data error`)\n')

    def test_archiveer(self, monkeypatch, capsys):
        """unittest for Page0.archiveer
        """
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = 'p0list'
        testobj.book.current_item = 'x'
        testobj.sel_args = {}
        testobj.book.pagedata.arch = False
        testobj.archiveer()
        assert testobj.book.pagedata.arch
        assert capsys.readouterr().out == (
                'called PageGui.get_selected_action with arg p0list\n'
                'called Page0.readp() using arch `1`\n'
                "called Actie.add_event() with args ('Actie gearchiveerd',)\n"
                'called Page0.update_actie()\n'
                'called Page0.vulp()\n'
                'called MainWindow.set_tabfocus(0)\n')
        testobj.archiveer()
        assert not testobj.book.pagedata.arch
        assert capsys.readouterr().out == (
                'called PageGui.get_selected_action with arg p0list\n'
                'called Page0.readp() using arch `1`\n'
                "called Actie.add_event() with args ('Actie herleefd',)\n"
                'called Page0.update_actie()\n'
                'called Page0.vulp()\n'
                'called MainWindow.set_tabfocus(0)\n')
        testobj.sel_args = {'arch': 'alles'}
        testobj.book.pagedata.arch = False
        testobj.archiveer()
        assert testobj.book.pagedata.arch
        assert capsys.readouterr().out == (
                'called PageGui.get_selected_action with arg p0list\n'
                'called Page0.readp() using arch `1`\n'
                "called Actie.add_event() with args ('Actie gearchiveerd',)\n"
                'called Page0.update_actie()\n'
                'called Page0.vulp()\n'
                'called MainWindow.set_tabfocus(0)\n'
                "called PageGui.ensure_visible with args ('p0list', 'x')\n"
                'called PageGui.set_archive_button_text(`&Herleef`)\n')
        testobj.archiveer()
        assert not testobj.book.pagedata.arch
        assert capsys.readouterr().out == (
                'called PageGui.get_selected_action with arg p0list\n'
                'called Page0.readp() using arch `1`\n'
                "called Actie.add_event() with args ('Actie herleefd',)\n"
                'called Page0.update_actie()\n'
                'called Page0.vulp()\n'
                'called MainWindow.set_tabfocus(0)\n'
                "called PageGui.ensure_visible with args ('p0list', 'x')\n"
                'called PageGui.set_archive_button_text(`&Archiveer`)\n')

    # def test_get_items(self, monkeypatch, capsys):
    #     """unittest for Page0.get_items
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.get_items() == ['all', 'the', 'items']
    #     assert capsys.readouterr().out == 'called PageGui.get_items()\n'

    # def _test_get_item_text(self, monkeypatch, capsys):
    #     """unittest for Page0.get_item_text
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.get_item_text(itemindicator, column) == "expected_result"
    #     assert capsys.readouterr().out == ("")
    #     """unittest for main.Page0.get_item_text
    #     """
    #     # class MockActie:
    #     #     """stub
    #     #     """
    #     testobj = setup_page0(monkeypatch, capsys)
    #     assert testobj.get_item_text('item', 'colno') == 'the text of the item'
    #     assert capsys.readouterr().out == "called PageGui.get_item_text() with args ('item', 'colno')\n"

    def test_clear_selection(self, monkeypatch, capsys):
        """unittest for Page0.clear_selection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.clear_selection()
        assert testobj.sel_args == {}


class TestPage1:
    """unittests for main.Page1
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.Page1 object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Page1.__init__ with args', args)
        monkeypatch.setattr(testee.Page1, '__init__', mock_init)
        testobj = testee.Page1()
        testobj.book = types.SimpleNamespace(pagedata=MockActie(), count=lambda *x: 3,
                                             pages=[testobj])
        testobj.appbase = MockMainWindow()
        testobj.gui = MockPageGui()
        assert capsys.readouterr().out == ('called Page1.__init__ with args ()\n'
                                           'called MainWindow.__init__() with args ()\n'
                                           'called MainGui.__init__()\n'
                                           'called PageGui.__init__() with args () {}\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Page1.__init__
        """
        monkeypatch.setattr(testee.gui, 'Page1Gui', MockPageGui)
        appbase = MockMainWindow()
        appbase.use_text_panels = False
        parent = MockBook()
        assert capsys.readouterr().out == ("called MainWindow.__init__() with args ()\n"
                                           "called MainGui.__init__()\n")
        parent.parent = appbase
        testobj = testee.Page1(parent)
        assert testobj.book == parent
        assert hasattr(testobj, 'gui')
        assert testobj.id_text == 'Actie-id'
        assert testobj.date_text == 'Datum/tijd:'
        assert testobj.proc_entry == 'Job/\ntransactie:'
        assert testobj.desc_entry == 'Melding/code/\nomschrijving:'
        assert testobj.cat_choice == 'Categorie:'
        assert testobj.stat_choice == 'Status:'
        assert testobj.archive_text == ''
        assert testobj.archive_button == 'Archiveren'
        assert testobj.summary_entry == 'Samenvatting van het issue:'
        assert testobj.abort_button == '&Breek opvoeren nieuwe actie af (Alt-0)'
        assert testobj.save_button == 'Sla wijzigingen op (Ctrl-S)'
        assert testobj.saveandgo_button == 'Sla op en ga verder (Ctrl-G)'
        assert testobj.cancel_button == 'Zet originele tekst terug (Alt-Ctrl-Z)'
        assert capsys.readouterr().out == (
                f"called PageGui.__init__() with args ({parent}, {testobj}) {{}}\n"
                "called PageGui.add_textentry_line with args ('Actie-id', 120)\n"
                "called PageGui.add_textentry_line with args ('Datum/tijd:', 150)\n"
                "called PageGui.add_textentry_line with args"
                f" ('Job/\\ntransactie:', 150, {testobj.on_text})\n"
                "called PageGui.add_textentry_line with args"
                f" ('Melding/code/\\nomschrijving:', 360, {testobj.on_text})\n"
                "called PageGui.add_combobox_line with args"
                f" ('Categorie:', 180, {testobj.on_text})\n"
                "called PageGui.add_combobox_line with args"
                f" ('Status:', 140, {testobj.on_text})\n"
                "called PageGui.add_pushbutton_line with args"
                f" ('', 'Archiveren', {testobj.archiveer})\n"
                "called PageGui.add_textbox_line with args"
                f" ('Samenvatting van het issue:', {testobj.on_text})\n"
                "called PageGui.create_buttons with args"
                f" ([('&Breek opvoeren nieuwe actie af (Alt-0)', {testobj.breekaf})],)\n"
                "called PageGui.create_buttons with args"
                f" ([('Sla wijzigingen op (Ctrl-S)', {testobj.savep}),"
                f" ('Sla op en ga verder (Ctrl-G)', {testobj.savepgo}),"
                f" ('Zet originele tekst terug (Alt-Ctrl-Z)', {testobj.restorep})],)\n"
                "called PageGui.add_keybind with args"
                f" ('Alt-N', {testobj.nieuwp}) {{'last': True}}\n")
        appbase.use_text_panels = True
        testobj = testee.Page1(parent)
        assert testobj.book == parent
        assert hasattr(testobj, 'gui')
        assert testobj.id_text == 'Actie-id'
        assert testobj.date_text == 'Datum/tijd:'
        assert testobj.proc_entry == 'Job/\ntransactie:'
        assert testobj.desc_entry == 'Melding/code/\nomschrijving:'
        assert testobj.cat_choice == 'Categorie:'
        assert testobj.stat_choice == 'Status:'
        assert testobj.archive_text == ''
        assert testobj.archive_button == 'Archiveren'
        assert not hasattr(testobj, 'summary_entry')
        assert testobj.abort_button == '&Breek opvoeren nieuwe actie af (Alt-0)'
        assert testobj.save_button == 'Sla wijzigingen op (Ctrl-S)'
        assert testobj.saveandgo_button == 'Sla op en ga verder (Ctrl-G)'
        assert testobj.cancel_button == 'Zet originele tekst terug (Alt-Ctrl-Z)'
        assert capsys.readouterr().out == (
                f"called PageGui.__init__() with args ({parent}, {testobj}) {{}}\n"
                "called PageGui.add_textentry_line with args ('Actie-id', 120)\n"
                "called PageGui.add_textentry_line with args ('Datum/tijd:', 150)\n"
                "called PageGui.add_textentry_line with args"
                f" ('Job/\\ntransactie:', 150, {testobj.on_text})\n"
                "called PageGui.add_textentry_line with args"
                f" ('Melding/code/\\nomschrijving:', 360, {testobj.on_text})\n"
                "called PageGui.add_combobox_line with args"
                f" ('Categorie:', 180, {testobj.on_text})\n"
                "called PageGui.add_combobox_line with args"
                f" ('Status:', 140, {testobj.on_text})\n"
                "called PageGui.add_pushbutton_line with args"
                f" ('', 'Archiveren', {testobj.archiveer})\n"
                "called PageGui.create_buttons with args"
                f" ([('&Breek opvoeren nieuwe actie af (Alt-0)', {testobj.breekaf})],)\n"
                "called PageGui.create_buttons with args"
                f" ([('Sla wijzigingen op (Ctrl-S)', {testobj.savep}),"
                f" ('Sla op en ga verder (Ctrl-G)', {testobj.savepgo}),"
                f" ('Zet originele tekst terug (Alt-Ctrl-Z)', {testobj.restorep})],)\n"
                "called PageGui.add_keybind with args"
                f" ('Alt-N', {testobj.nieuwp}) {{'last': True}}\n")

    def test_vulp(self, monkeypatch, capsys):
        """unittest for Page1.vulp
        """
        class MockActie:
            """stub
            """
            def __init__(self, new=False):
                self.id = '2000-0001'
                self.datum = 'datestring'
                if new:
                    return
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
        def mock_get():
            print('called Page1.get_fieldvalues')
            return ['field', 'values']
        def mock_enable(value):
            print(f'called Page1.enable_fields with arg {value}')
        monkeypatch.setattr(testee.Page, 'vulp', mock_super_vulp)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.id_text = 'id'
        testobj.date_text = 'date'
        testobj.proc_entry = 'proc'
        testobj.desc_entry = 'desc'
        testobj.cat_choice = 'cat'
        testobj.stat_choice = 'stat:'
        testobj.archive_text = 'text'
        testobj.archive_button = 'arch'
        testobj.summary_entry = 'summary'
        testobj.abort_button = 'abort'
        testobj.get_fieldvalues = mock_get
        testobj.enable_fields = mock_enable
        testobj.appbase.is_user = True
        testobj.book.pagedata = MockActie(new=True)
        testobj.book.newitem = True
        testobj.vulp()
        assert capsys.readouterr().out == (
                'called Page.super_vulp()\n'
                "called PageGui.show_button with args ('abort', False)\n"
                "called PageGui.set_textfield_value with args ('id', '2000-0001')\n"
                "called PageGui.set_textfield_value with args ('date', 'datestring')\n"
                "called Page1.get_fieldvalues\n"
                "called PageGui.set_label_value with args ('text', '')\n"
                "called PageGui.set_button_text with args ('arch', 'Archiveren')\n"
                'called Page1.enable_fields with arg True\n')

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.id_text = 'id'
        testobj.date_text = 'date'
        testobj.proc_entry = 'proc'
        testobj.desc_entry = 'desc'
        testobj.cat_choice = 'cat'
        testobj.stat_choice = 'stat'
        testobj.archive_text = 'text'
        testobj.archive_button = 'arch'
        testobj.summary_entry = 'summary'
        testobj.abort_button = 'abort'
        testobj.get_fieldvalues = mock_get
        testobj.enable_fields = mock_enable
        testobj.book.pagedata = MockActie()
        testobj.book.pages = [MockPage()]
        assert capsys.readouterr().out == ('called Page.__init__() with args () {}\n'
                                           'called PageGui.__init__() with args () {}\n')
        testobj.book.newitem = False
        testobj.book.cats = ['cats']
        testobj.book.stats = ['stats']
        testobj.appbase.use_separate_subject = True
        testobj.appbase.use_text_panels = True
        testobj.appbase.is_user = True
        testobj.vulp()
        assert capsys.readouterr().out == (
                'called Page.super_vulp()\n'
                "called PageGui.show_button with args ('abort', False)\n"
                "called PageGui.set_textfield_value with args ('id', '2000-0001')\n"
                "called PageGui.set_textfield_value with args ('date', 'datestring')\n"
                "called PageGui.set_textfield_value with args ('proc', 'subject')\n"
                "called PageGui.set_textfield_value with args ('desc', \"it's: the arts\")\n"
                "called PageGui.set_choice() with args ('stat', ['stats'], 0)\n"
                "called PageGui.set_choice() with args ('cat', ['cats'], 'I')\n"
                "called Page1.get_fieldvalues\n"
                "called PageGui.set_label_value with args ('text', 'Deze actie is gearchiveerd')\n"
                "called PageGui.set_button_text with args ('arch', 'Herleven')\n"
                'called Page1.enable_fields with arg False\n')

        testobj.book.pagedata.arch = False
        testobj.appbase.use_separate_subject = False
        testobj.appbase.use_text_panels = False
        testobj.appbase.is_user = True
        testobj.vulp()
        assert capsys.readouterr().out == (
                'called Page.super_vulp()\n'
                "called PageGui.show_button with args ('abort', False)\n"
                "called PageGui.set_textfield_value with args ('id', '2000-0001')\n"
                "called PageGui.set_textfield_value with args ('date', 'datestring')\n"
                "called PageGui.set_textfield_value with args ('proc', \"it's\")\n"
                "called PageGui.set_textfield_value with args ('desc', 'the arts')\n"
                "called PageGui.set_choice() with args ('stat', ['stats'], 0)\n"
                "called PageGui.set_choice() with args ('cat', ['cats'], 'I')\n"
                "called PageGui.set_textbox_value with args ('summary', 'in short: this')\n"
                "called Page1.get_fieldvalues\n"
                "called PageGui.set_label_value with args ('text', '')\n"
                "called PageGui.set_button_text with args ('arch', 'Archiveren')\n"
                'called Page1.enable_fields with arg True\n')

        testobj.book.pagedata.titel = 'onderwerp - beschrijving'
        testobj.appbase.use_separate_subject = False
        testobj.appbase.use_text_panels = False
        testobj.appbase.is_user = False
        testobj.vulp()
        assert capsys.readouterr().out == (
                'called Page.super_vulp()\n'
                "called PageGui.show_button with args ('abort', False)\n"
                "called PageGui.set_textfield_value with args ('id', '2000-0001')\n"
                "called PageGui.set_textfield_value with args ('date', 'datestring')\n"
                "called PageGui.set_textfield_value with args ('proc', 'onderwerp')\n"
                "called PageGui.set_textfield_value with args ('desc', 'beschrijving')\n"
                "called PageGui.set_choice() with args ('stat', ['stats'], 0)\n"
                "called PageGui.set_choice() with args ('cat', ['cats'], 'I')\n"
                "called PageGui.set_textbox_value with args ('summary', 'in short: this')\n"
                "called Page1.get_fieldvalues\n"
                "called PageGui.set_label_value with args ('text', '')\n"
                "called PageGui.set_button_text with args ('arch', 'Archiveren')\n"
                'called Page1.enable_fields with arg False\n')

        testobj.book.pagedata.titel = 'x'
        testobj.appbase.use_separate_subject = False
        testobj.appbase.use_text_panels = False
        testobj.appbase.is_user = False
        testobj.vulp()
        assert capsys.readouterr().out == (
                'called Page.super_vulp()\n'
                "called PageGui.show_button with args ('abort', False)\n"
                "called PageGui.set_textfield_value with args ('id', '2000-0001')\n"
                "called PageGui.set_textfield_value with args ('date', 'datestring')\n"
                "called PageGui.set_textfield_value with args ('proc', 'x')\n"
                "called PageGui.set_choice() with args ('stat', ['stats'], 0)\n"
                "called PageGui.set_choice() with args ('cat', ['cats'], 'I')\n"
                "called PageGui.set_textbox_value with args ('summary', 'in short: this')\n"
                "called Page1.get_fieldvalues\n"
                "called PageGui.set_label_value with args ('text', '')\n"
                "called PageGui.set_button_text with args ('arch', 'Archiveren')\n"
                'called Page1.enable_fields with arg False\n')
        # deze test bewust uitgezet om deze situatie niet ongemerkt langs te laten komen
        # testobj.book.pagedata.titel = ''
        # testobj.appbase.use_separate_subject = False
        # testobj.appbase.use_text_panels = False
        # testobj.appbase.is_user = False
        # with pytest.raises(ValueError) as exc:
        #     testobj.vulp()
        # assert str(exc.value) == 'ProgrammmingError: subject should not be empty'

    def test_enable_fields(self, monkeypatch, capsys):
        """unittest for Page1.enable_fields
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.id_text = 'id'
        testobj.date_text = 'date'
        testobj.proc_entry = 'proc'
        testobj.desc_entry = 'desc'
        testobj.cat_choice = 'cat'
        testobj.stat_choice = 'stat:'
        testobj.archive_button = 'arch'
        testobj.summary_entry = 'summary'
        testobj.abort_button = 'abort'
        testobj.book.newitem = False
        testobj.appbase = types.SimpleNamespace(use_text_panels=False, is_user=True)
        testobj.enable_fields('state')
        assert capsys.readouterr().out == (
                "called PageGui.enable_widget with args ('id', False)\n"
                "called PageGui.enable_widget with args ('date', False)\n"
                "called PageGui.enable_widget with args ('proc', 'state')\n"
                "called PageGui.enable_widget with args ('desc', 'state')\n"
                "called PageGui.enable_widget with args ('cat', 'state')\n"
                "called PageGui.enable_widget with args ('stat:', 'state')\n"
                "called PageGui.enable_widget with args ('arch', True)\n"
                "called PageGui.enable_widget with args ('summary', 'state')\n")
        testobj.book.newitem = True
        # testobj.appbase.is_user = True
        testobj.appbase.use_text_panels = True
        testobj.enable_fields('state')
        assert capsys.readouterr().out == (
                "called PageGui.enable_widget with args ('id', False)\n"
                "called PageGui.enable_widget with args ('date', False)\n"
                "called PageGui.enable_widget with args ('proc', 'state')\n"
                "called PageGui.enable_widget with args ('desc', 'state')\n"
                "called PageGui.enable_widget with args ('cat', 'state')\n"
                "called PageGui.enable_widget with args ('stat:', 'state')\n"
                "called PageGui.enable_widget with args ('arch', False)\n"
                "called PageGui.show_button with args ('abort', True)\n")
        testobj.book.newitem = False
        testobj.appbase.is_user = False
        # testobj.appbase.use_text_panels = True
        testobj.enable_fields('state')
        assert capsys.readouterr().out == (
                "called PageGui.enable_widget with args ('id', False)\n"
                "called PageGui.enable_widget with args ('date', False)\n"
                "called PageGui.enable_widget with args ('proc', 'state')\n"
                "called PageGui.enable_widget with args ('desc', 'state')\n"
                "called PageGui.enable_widget with args ('cat', 'state')\n"
                "called PageGui.enable_widget with args ('stat:', 'state')\n"
                "called PageGui.enable_widget with args ('arch', False)\n")

    def test_savep(self, monkeypatch, capsys):
        """unittest for Page1.savep
        """
        class MockActie:
            """zcstub
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
        def mock_super_savep(self):
            print('called Page.super_savep()')
        def mock_super_savep_2(self):
            print('called Page.super_savep()')
            return True
        def mock_show_message(cls, msg, title=''):
            print(f'called gui.show_message with args `{title}` `{msg}`')
        def mock_get():
            print('called Page.get_fieldvalues')
            return testobj.oldbuf
        def mock_get_2():
            print('called Page.get_fieldvalues')
            return ['y', 'z']
        def mock_get_3():
            print('called Page.get_fieldvalues')
            return ['y', 'z', '']
        def mock_get_4():
            print('called Page.get_fieldvalues')
            return ['y', 'z', 'q']
        def mock_check_pd(*args):
            print('called Page1.check_proc_desc_gewijzigd with args', args)
            return 'xxxx'
        def mock_check_pd_2(*args):
            print('called Page1.check_proc_desc_gewijzigd with args', args)
            return ''
        def mock_check_stat():
            print('called Page1.check_stat_gewijzigd')
        def mock_check_cat():
            print('called Page1.check_cat_gewijzigd')
        def mock_update_actie():
            """stubo
            """
            print('called Page.update_actie()')
        def mock_enable(arg):
            print(f'called Page.enable_buttons with arg {arg}')
        monkeypatch.setattr(testee.Page, 'savep', mock_super_savep)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_fieldvalues = mock_get
        testobj.enable_buttons = mock_enable
        testobj.check_proc_desc_gewijzigd = mock_check_pd
        testobj.check_stat_gewijzigd = mock_check_stat
        testobj.check_cat_gewijzigd = mock_check_cat
        testobj.update_actie = mock_update_actie
        testobj.parch = False
        testobj.oldbuf = ['x', 'y']
        testobj.appbase.use_text_panels = True
        testobj.book.pagedata = MockActie()
        assert not testobj.savep()
        assert capsys.readouterr().out == 'called Page.super_savep()\n'
        monkeypatch.setattr(testee.Page, 'savep', mock_super_savep_2)
        assert not testobj.savep()
        assert capsys.readouterr().out == (
                'called Page.super_savep()\n'
                'called Page.get_fieldvalues\n')
        testobj.get_fieldvalues = mock_get_2
        assert not testobj.savep()
        assert capsys.readouterr().out == (
                'called Page.super_savep()\n'
                'called Page.get_fieldvalues\n'
                "called Page1.check_proc_desc_gewijzigd with args ('y', 'z')\n"
                "called gui.show_message with args `` `xxxx`\n")
        testobj.check_proc_desc_gewijzigd = mock_check_pd_2
        testobj.savep()
        assert capsys.readouterr().out == (
                'called Page.super_savep()\n'
                'called Page.get_fieldvalues\n'
                "called Page1.check_proc_desc_gewijzigd with args ('y', 'z')\n"
                "called Page1.check_stat_gewijzigd\n"
                "called Page1.check_cat_gewijzigd\n"
                "called Page.update_actie()\n"
                "called Page.get_fieldvalues\n"
                "called Page.enable_buttons with arg False\n")
        testobj.parch = True
        testobj.oldbuf = ['x', 'y']
        testobj.savep()
        assert testobj.book.pagedata.arch
        assert testobj.oldbuf == ['y', 'z']
        assert capsys.readouterr().out == (
                'called Page.super_savep()\n'
                'called Page.get_fieldvalues\n'
                "called Page1.check_proc_desc_gewijzigd with args ('y', 'z')\n"
                "called Page1.check_stat_gewijzigd\n"
                "called Page1.check_cat_gewijzigd\n"
                "called Actie.add_event with text `Actie gearchiveerd`\n"
                "called Page.update_actie()\n"
                "called Page.get_fieldvalues\n"
                "called Page.enable_buttons with arg False\n")
        testobj.appbase.use_text_panels = False
        testobj.get_fieldvalues = mock_get_3
        testobj.parch = False
        testobj.oldbuf = ['x', 'y']
        testobj.savep()
        assert not testobj.book.pagedata.arch
        assert testobj.book.pagedata.melding == ''
        assert testobj.oldbuf == ['y', 'z', '']
        assert capsys.readouterr().out == (
                'called Page.super_savep()\n'
                'called Page.get_fieldvalues\n'
                "called Page1.check_proc_desc_gewijzigd with args ('y', 'z')\n"
                "called Page1.check_stat_gewijzigd\n"
                "called Page1.check_cat_gewijzigd\n"
                "called Actie.add_event with text `Actie herleefd`\n"
                "called Page.update_actie()\n"
                "called Page.get_fieldvalues\n"
                "called Page.enable_buttons with arg False\n")
        testobj.get_fieldvalues = mock_get_4
        testobj.oldbuf = ['x', 'y']
        testobj.savep()
        assert not testobj.book.pagedata.arch
        assert testobj.book.pagedata.melding == 'q'
        assert testobj.oldbuf == ['y', 'z', 'q']
        assert capsys.readouterr().out == (
                'called Page.super_savep()\n'
                'called Page.get_fieldvalues\n'
                "called Page1.check_proc_desc_gewijzigd with args ('y', 'z')\n"
                "called Page1.check_stat_gewijzigd\n"
                "called Page1.check_cat_gewijzigd\n"
                "called Actie.add_event with text `Meldingtekst aangepast`\n"
                "called Page.update_actie()\n"
                "called Page.get_fieldvalues\n"
                "called Page.enable_buttons with arg False\n")

    def test_check_proc_desc_gewijzigd(self, monkeypatch, capsys):
        """unittest for Page1.check_proc_desc_gewijzigd
        """
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
        def mock_enable_buttons(value):
            """stub
            """
            print(f'called Page.enable_buttons({value})')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.enable_buttons = mock_enable_buttons
        testobj.book.pagedata = MockActie()
        assert testobj.check_proc_desc_gewijzigd('xxx', '') == (
                "Beide tekstrubrieken moeten worden ingevuld")
        assert capsys.readouterr().out == ""
        assert testobj.check_proc_desc_gewijzigd('', 'yyy') == (
                "Beide tekstrubrieken moeten worden ingevuld")
        assert capsys.readouterr().out == ""
        testobj.appbase.use_separate_subject = False
        testobj.book.pagedata.titel = 'x - y'
        assert testobj.check_proc_desc_gewijzigd('x', 'y') == ""
        assert testobj.book.pagedata.titel == 'x - y'
        assert capsys.readouterr().out == ""
        assert testobj.check_proc_desc_gewijzigd('x', 'yyy') == ""
        assert testobj.book.pagedata.titel == 'x - yyy'
        assert capsys.readouterr().out == (
                "called PageGui.set_textfield_value with args ('proc', 'X - yyy')\n"
                "called Actie.add_event with text `Titel gewijzigd in \"x - yyy\"`\n")
        testobj.book.pagedata.titel = 'x - y'
        assert testobj.check_proc_desc_gewijzigd('xxx', 'y') == ""
        assert testobj.book.pagedata.titel == 'xxx - y'
        assert capsys.readouterr().out == (
                "called PageGui.set_textfield_value with args ('proc', 'Xxx - y')\n"
                "called Actie.add_event with text `Titel gewijzigd in \"xxx - y\"`\n")
        testobj.book.pagedata.titel = 'x - y'
        assert testobj.check_proc_desc_gewijzigd('xxx', 'yyy') == ""
        assert testobj.book.pagedata.titel == 'xxx - yyy'
        assert capsys.readouterr().out == (
                "called PageGui.set_textfield_value with args ('proc', 'Xxx - yyy')\n"
                "called Actie.add_event with text `Titel gewijzigd in \"xxx - yyy\"`\n")
        testobj.appbase.use_separate_subject = True
        testobj.book.pagedata.over = 'x'
        testobj.book.pagedata.titel = 'y'
        assert testobj.check_proc_desc_gewijzigd('x', 'yyy') == ""
        assert testobj.book.pagedata.over == 'x'
        assert testobj.book.pagedata.titel == 'yyy'
        assert capsys.readouterr().out == (
                "called PageGui.set_textfield_value with args ('proc', 'X')\n"
                "called Actie.add_event with text `Titel gewijzigd in \"yyy\"`\n")
        testobj.book.pagedata.over = 'x'
        testobj.book.pagedata.titel = 'y'
        assert testobj.check_proc_desc_gewijzigd('xxx', 'y') == ""
        assert testobj.book.pagedata.over == 'xxx'
        assert testobj.book.pagedata.titel == 'y'
        assert capsys.readouterr().out == (
                "called PageGui.set_textfield_value with args ('proc', 'Xxx')\n"
                "called Actie.add_event with text `Onderwerp gewijzigd in \"xxx\"`\n")
        testobj.book.pagedata.over = 'x'
        testobj.book.pagedata.titel = 'y'
        assert testobj.check_proc_desc_gewijzigd('xxx', 'yyy') == ""
        assert testobj.book.pagedata.over == 'xxx'
        assert testobj.book.pagedata.titel == 'yyy'
        assert capsys.readouterr().out == (
                "called PageGui.set_textfield_value with args ('proc', 'Xxx')\n"
                "called Actie.add_event with text `Onderwerp gewijzigd in \"xxx\"`\n"
                "called Actie.add_event with text `Titel gewijzigd in \"yyy\"`\n")

    def test_check_stat_gewijzigd(self, monkeypatch, capsys):
        """unittest for Page1.check_stat_gewijzigd
        """
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
        def mock_get(*args):
            print('called PageGui.get_choice_data with args', args)
            return 0, 'q'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.pagedata = MockActie()
        testobj.stat_choice = 'stat'
        testobj.book.newitem = False
        testobj.check_stat_gewijzigd()
        assert testobj.book.pagedata.status == 'stat'
        assert capsys.readouterr().out == (
                "called PageGui.get_choice_data with args ('stat',)\n"
                "called Actie.add_event with text `Status gewijzigd in \"x\"`\n")
        testobj.book.newitem = True
        testobj.book.pagedata.status = 0
        testobj.check_stat_gewijzigd()
        assert testobj.book.pagedata.status == 'stat'
        assert capsys.readouterr().out == (
                "called PageGui.get_choice_data with args ('stat',)\n"
                "called Actie.add_event with text `Status is \"x\"`\n")
        testobj.gui.get_choice_data = mock_get
        testobj.book.pagedata.status = 0
        testobj.check_stat_gewijzigd()
        assert testobj.book.pagedata.status == 0
        assert capsys.readouterr().out == (
                "called PageGui.get_choice_data with args ('stat',)\n"
                "called Actie.add_event with text `Status is \"q\"`\n")
        testobj.book.newitem = False
        testobj.book.pagedata.status = 0
        testobj.check_stat_gewijzigd()
        assert testobj.book.pagedata.status == 0
        assert capsys.readouterr().out == (
                "called PageGui.get_choice_data with args ('stat',)\n")

    def test_check_cat_gewijzigd(self, monkeypatch, capsys):
        """unittest for Page1.check_cat_gewijzigd
        """
        class MockActie:
            """stub
            """
            def __init__(self):
                self.titel = ''
                self.over = ''
                self.status = 0
                self.soort = 'p'
                self.arch = False
                self.melding = ''
            def add_event(self, text):
                """stub
                """
                print(f'called Actie.add_event with text `{text}`')
        def mock_get(*args):
            print('called PageGui.get_choice_data with args', args)
            return 'p', 'q'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.pagedata = MockActie()
        testobj.cat_choice = 'cat'
        testobj.book.newitem = False
        testobj.check_cat_gewijzigd()
        assert testobj.book.pagedata.soort == 'cat'
        assert capsys.readouterr().out == (
                "called PageGui.get_choice_data with args ('cat',)\n"
                "called Actie.add_event with text `Categorie gewijzigd in \"x\"`\n")
        testobj.book.newitem = True
        testobj.book.pagedata.soort = 'p'
        testobj.check_cat_gewijzigd()
        assert testobj.book.pagedata.soort == 'cat'
        assert capsys.readouterr().out == (
                "called PageGui.get_choice_data with args ('cat',)\n"
                "called Actie.add_event with text `Categorie is \"x\"`\n")
        testobj.gui.get_choice_data = mock_get
        testobj.book.pagedata.soort = 'p'
        testobj.check_cat_gewijzigd()
        assert testobj.book.pagedata.soort == 'p'
        assert capsys.readouterr().out == (
                "called PageGui.get_choice_data with args ('cat',)\n"
                "called Actie.add_event with text `Categorie is \"q\"`\n")
        testobj.book.newitem = False
        testobj.book.pagedata.soort = 'p'
        testobj.check_cat_gewijzigd()
        assert testobj.book.pagedata.soort == 'p'
        assert capsys.readouterr().out == (
                "called PageGui.get_choice_data with args ('cat',)\n")

    def test_build_newbuf(self, monkeypatch, capsys):
        """unittest for Page1.build_newbuf
        """
        def mock_get():
            print('called Page6.get_fieldvalues')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_fieldvalues = mock_get
        testobj.build_newbuf()
        assert capsys.readouterr().out == "called Page6.get_fieldvalues\n"

    def test_get_fieldvalues(self, monkeypatch, capsys):
        """unittest for Page1.get_fieldvalues
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.proc_entry = 'proc'
        testobj.desc_entry = 'desc'
        testobj.stat_choice = 'stat'
        testobj.cat_choice = 'cat'
        testobj.summary_entry = 'summary'
        testobj.appbase.use_text_panels = False
        assert testobj.get_fieldvalues() == ['proc', 'desc', 4, 3, 'summary']
        assert capsys.readouterr().out == (
                "called PageGui.get_textfield_value with args ('proc',)\n"
                "called PageGui.get_textfield_value with args ('desc',)\n"
                "called PageGui.get_choice_index with args ('stat',)\n"
                "called PageGui.get_choice_index with args ('cat',)\n"
                "call PageGui.get_textbox_value with args ('summary',)\n")
        testobj.appbase.use_text_panels = True
        assert testobj.get_fieldvalues() == ['proc', 'desc', 4, 3]
        assert capsys.readouterr().out == (
                "called PageGui.get_textfield_value with args ('proc',)\n"
                "called PageGui.get_textfield_value with args ('desc',)\n"
                "called PageGui.get_choice_index with args ('stat',)\n"
                "called PageGui.get_choice_index with args ('cat',)\n")

    def test_archiveer(self, monkeypatch, capsys):
        """unittest for Page1.archiveer
        """
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
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parch = False
        testobj.archiveer()
        assert testobj.parch
        assert capsys.readouterr().out == ('called Page1.savep()\ncalled Page1.vulp()\n')

    def test_vul_combos(self, monkeypatch, capsys):
        """unittest for Page1.vul_combos
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.cat_choice = 'cat'
        testobj.stat_choice = 'stat'
        testobj.book.stats = {'2': ('text2', 'II', 2), '1': ('text1', 'I')}
        testobj.book.cats = {'2': ('cat2', '02', 2), '1': ('cat1', '01')}
        testobj.vul_combos()
        assert capsys.readouterr().out == (
                "called PageGui.clear_combobox with args ('stat',)\n"
                "called PageGui.add_combobox_choice with args ('stat', 'text1', 'I')\n"
                "called PageGui.add_combobox_choice with args ('stat', 'text2', 'II')\n"
                "called PageGui.clear_combobox with args ('cat',)\n"
                "called PageGui.add_combobox_choice with args ('cat', 'cat1', '01')\n"
                "called PageGui.add_combobox_choice with args ('cat', 'cat2', '02')\n")

    def test_breekaf(self, monkeypatch, capsys):
        """unittest for Page1.breekaf
        """
        def mock_abort():
            print('called Page1.abort_add')
        def mock_goto(page):
            print(f'called Page.goto_page with arg {page}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.abort_add = mock_abort
        testobj.goto_page = mock_goto
        testobj.breekaf()
        assert capsys.readouterr().out == ("called Page1.abort_add\n"
                                           "called Page.goto_page with arg 0\n")


class TestPage6:
    """unittests for main.Page6
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.Page6 object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Page6.__init__ with args', args)
        monkeypatch.setattr(testee.Page6, '__init__', mock_init)
        testobj = testee.Page6()
        testobj.book = types.SimpleNamespace(pagedata=MockActie(), count=lambda *x: 3,
                                             pages=[testobj])
        testobj.appbase = MockMainWindow()
        testobj.gui = MockPageGui()
        assert capsys.readouterr().out == ('called Page6.__init__ with args ()\n'
                                           'called MainWindow.__init__() with args ()\n'
                                           "called MainGui.__init__()\n"
                                           'called PageGui.__init__() with args () {}\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Page6.__init__
        """
        monkeypatch.setattr(testee.gui, 'Page6Gui', MockPageGui)
        appbase = MockMainWindow()
        parent = MockBook()
        assert capsys.readouterr().out == ("called MainWindow.__init__() with args ()\n"
                                           "called MainGui.__init__()\n")
        parent.parent = appbase
        testobj = testee.Page6(parent)
        # assert testobj.parent == 'parent'  # parent associatie via de superklasse
        assert testobj.current_item == 0
        assert testobj.oldtext == ""
        assert (testobj.event_list, testobj.event_data, testobj.old_list, testobj.old_data) == (
                [], [], [], [])
        assert not testobj.status_auto_changed
        assert isinstance(testobj.gui, testee.gui.Page6Gui)
        assert testobj.progress_list
        assert testobj.progress_text
        assert capsys.readouterr().out == (
                f"called PageGui.__init__() with args ({parent}, {testobj}) {{}}\n"
                "called PageGui.create_list\n"
                f"called PageGui.create_textfield with args (490, 330, {testobj.on_text})\n"
                "called PageGui.create_buttons with args"
                f" ([('Sla wijzigingen op (Ctrl-S)', {testobj.savep}),"
                f" ('Zet originele tekst terug (Alt-Ctrl-Z)', {testobj.restorep})],)\n"
                "called PageGui.finish_display\n")

    def test_vulp(self, monkeypatch, capsys):
        """unittest for Page6.vulp
        """
        def mock_super_vulp(self):
            """stub
            """
            print('called Page.super_vulp()')
        def mock_callback():
            "reference to callback"
        def mock_item(arg):
            return f'item{arg}'
        monkeypatch.setattr(testee.Page, 'vulp', mock_super_vulp)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.appbase.work_with_user = False
        testobj.appbase.is_user = True

        testobj.progress_list = 'listbox'
        testobj.progress_text = 'textfield'
        testobj.book.pagedata.events = []
        testobj.old_list, testobj.old_data = [], []
        testobj.vulp()
        assert testobj.event_list == []
        assert testobj.old_list == []
        assert testobj.event_data == []
        assert testobj.old_data == []
        assert testobj.oldbuf == ([], [])
        assert testobj.oldtext == ''
        assert capsys.readouterr().out == (
                'called Page.super_vulp()\n'
                "called PageGui.clear_list with args ('listbox',)\n"
                'called PageGui.add_first_listitem with args'
                " ('listbox', '-- doubleclick or press Shift-Ctrl-N to add new item --')\n"
                "called PageGui.clear_textfield with args ('textfield',)\n"
                "called PageGui.set_text_readonly with args ('textfield', True)\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.pagedata.events = []
        testobj.appbase.work_with_user = True
        testobj.appbase.is_user = False
        testobj.progress_list = types.SimpleNamespace(item=mock_item)
        testobj.progress_text = 'textfield'
        testobj.gui.on_activate_item = mock_callback
        testobj.vulp()
        assert testobj.oldbuf == ([], [])
        assert testobj.oldtext == ''
        assert capsys.readouterr().out == (
                'called Page.super_vulp()\n'
                f"called PageGui.clear_list with args ({testobj.progress_list},)\n"
                'called PageGui.add_first_listitem with args'
                f" ({testobj.progress_list}, '-- adding new items is disabled --')\n"
                "called PageGui.init_set_list_callbacks with args"
                f" ({testobj.progress_list}, {mock_callback},"
                f" functools.partial({mock_callback}, 'item0'))\n"
                "called PageGui.clear_textfield with args ('textfield',)\n"
                "called PageGui.set_text_readonly with args ('textfield', True)\n")

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.pagedata.events = [('2001-01-01 01:10:10', 'first event'),
                                        ('2010-01-01 10:10:10', 'next event')]
        testobj.appbase.work_with_user = True
        testobj.appbase.is_user = True
        testobj.progress_list = types.SimpleNamespace(item=mock_item)
        testobj.progress_text = 'textfield'
        testobj.gui.on_activate_item = mock_callback
        testobj.vulp()
        assert testobj.oldbuf == (['01-01-2010 10:10:10', '01-01-2001 01:10:10'],
                                  ['next event', 'first event'])
        assert testobj.oldtext == ''
        assert capsys.readouterr().out == (
                'called Page.super_vulp()\n'
                f"called PageGui.clear_list with args ({testobj.progress_list},)\n"
                f'called PageGui.add_first_listitem with args ({testobj.progress_list},'
                " '-- doubleclick or press Shift-Ctrl-N to add new item --')\n"
                "called PageGui.add_item_to_list() with args"
                f" ({testobj.progress_list}, 'textfield', 0, '01-01-2010 10:10:10')\n"
                "called PageGui.add_item_to_list() with args"
                f" ({testobj.progress_list}, 'textfield', 1, '01-01-2001 01:10:10')\n"
                "called PageGui.init_set_list_callbacks with args"
                f" ({testobj.progress_list}, {mock_callback},"
                f" functools.partial({mock_callback}, 'item0'))\n"
                "called PageGui.clear_textfield with args ('textfield',)\n"
                "called PageGui.set_text_readonly with args ('textfield', True)\n")
        # deze test bewust uitgezet om deze situatie niet ongemerkt langs te laten komen
        # testobj.book.pagedata = None
        # with pytest.raises(ValueError) as exception:
        #     testobj.vulp()
        # assert str(exception.value) == 'ProgrammingError: page data should not be empty'

    def test_savep(self, monkeypatch, capsys):
        """unittest for Page6.savep
        """
        def mock_super_savep(self):
            """stub
            """
            print('called Page.super_savep()')
            return False
        def mock_super_savep_2(self):
            """stub
            """
            print('called Page.super_savep()')
            return True
        def mock_get(self, *args):
            """stub
            """
            print('called PageGui.get_textfield_contents with args', args)
            return f"{20 * 'text'}\naaabbb"
        def mock_get2(self, *args):
            """stub
            """
            print('called PageGui.get_textfield_contents with args', args)
            return f"{20 * 'text'}a\naabbb"
        def mock_update_actie(*args):
            """stub
            """
            print('called Page.update_actie()')
        monkeypatch.setattr(testee.Page, 'savep', mock_super_savep)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_text = 'progress_text'
        testobj.book.pagedata.events = [('date1', 'not_text'), ('date2', 'text')]
        testobj.book.pagedata.updated = True
        testobj.update_actie = mock_update_actie

        testobj.old_list = testobj.event_list = ['date1', 'date2']
        testobj.old_data = testobj.event_data = ['not text', 'text']
        testobj.current_item = 2
        assert not testobj.savep()
        assert capsys.readouterr().out == 'called Page.super_savep()\n'
        monkeypatch.setattr(testee.Page, 'savep', mock_super_savep_2)
        assert testobj.savep()
        assert capsys.readouterr().out == (
                'called Page.super_savep()\n'
                "called PageGui.get_textfield_contents with args ('progress_text',)\n")
        monkeypatch.setattr(MockPageGui, 'get_textfield_contents', mock_get)
        testobj.current_item = 0
        testobj.book.current_item = 'parentitem'  # for tab 0
        testobj.old_data = ['not_text', 'text']
        assert testobj.savep()
        assert capsys.readouterr().out == (
                'called Page.super_savep()\n'
                "called PageGui.get_textfield_contents with args ('progress_text',)\n"
                f"called PageGui.set_listitem_text() with args (1, 'date1 - {20 * 'text'}')\n"
                'called PageGui.set_listitem_data() with args (1,)\n'
                'called Page.update_actie()\n'
                "called PageGui.set_item_text() with args ('parentitem', 3, True)\n")
        assert testobj.book.pagedata.events == [('date2', 'text'),
                                                ('date1', f"{20 * 'text'}\naaabbb")]
        assert testobj.oldbuf == (['date1', 'date2'], [f"{20 * 'text'}\naaabbb", 'text'])

        monkeypatch.setattr(MockPageGui, 'get_textfield_contents', mock_get2)
        testobj.current_item = 3
        testobj.event_list = ['date1', 'date2', 'date3']
        testobj.old_list = testobj.event_list[:-1]
        testobj.event_data = ['not text', 'text', 'newtext']
        testobj.old_data = testobj.event_data[:-1]
        assert testobj.savep()
        assert capsys.readouterr().out == (
                'called Page.super_savep()\n'
                "called PageGui.get_textfield_contents with args ('progress_text',)\n"
                f"called PageGui.set_listitem_text() with args (3, 'date3 - {20 * 'text'}...')\n"
                'called PageGui.set_listitem_data() with args (3,)\n'
                'called Page.update_actie()\n'
                "called PageGui.set_item_text() with args ('parentitem', 3, True)\n")
        assert testobj.book.pagedata.events == [('date3', f"{20 * 'text'}a\naabbb"),
                                                ('date2', 'text'), ('date1', 'not text')]
        assert testobj.oldbuf == (['date1', 'date2', 'date3'],
                                  ['not text', 'text', f"{20 * 'text'}a\naabbb"])

    def test_goto_prev(self, monkeypatch, capsys):
        """unittest for Page6.goto_prev
        """
        monkeypatch.setattr(MockPageGui, 'get_list_row', lambda *x: 1)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_list = 'p0list'
        testobj.goto_prev()
        assert capsys.readouterr().out == ''
        monkeypatch.setattr(MockPageGui, 'get_list_row', lambda *x: 2)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_list = 'p0list'
        testobj.goto_prev()
        assert capsys.readouterr().out == "called PageGui.set_list_row with args ('p0list', 1)\n"

    def test_goto_next(self, monkeypatch, capsys):
        """unittest for Page6.goto_next
        """
        monkeypatch.setattr(MockPageGui, 'get_list_row', lambda *x: 1)
        monkeypatch.setattr(MockPageGui, 'get_list_rowcount', lambda *x: 2)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_list = 'p0list'
        testobj.goto_next()
        assert capsys.readouterr().out == ''
        monkeypatch.setattr(MockPageGui, 'get_list_row', lambda *x: 0)
        monkeypatch.setattr(MockPageGui, 'get_list_rowcount', lambda *x: 2)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_list = 'p0list'
        testobj.goto_next()
        assert capsys.readouterr().out == "called PageGui.set_list_row with args ('p0list', 1)\n"

    def test_on_text(self, monkeypatch, capsys):
        """unittest for Page6.on_text
        """
        def mock_enable_buttons():
            """stub
            """
            print('called Page6.enable_buttons()')
        monkeypatch.setattr(MockPageGui, 'get_list_row', lambda *x: 0)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_text = 'progress_text'
        testobj.initializing = True
        testobj.on_text()
        assert capsys.readouterr().out == ''

        testobj.initializing = False
        testobj.oldtext = 'text'
        testobj.on_text()
        assert capsys.readouterr().out == (
                "called PageGui.get_textfield_contents with args ('progress_text',)\n")

        testobj.oldtext = 'oldtext'
        testobj.appbase.is_user = False
        testobj.on_text()
        assert capsys.readouterr().out == (
                "called PageGui.get_textfield_contents with args ('progress_text',)\n"
                'called PageGui.convert_text() with args `text`, to=`plain`\n')

        monkeypatch.setattr(MockPageGui, 'get_list_row', lambda *x: 1)
        monkeypatch.setattr(MockPageGui, 'get_listitem_text', lambda *x: 'datestring - textstring')
        monkeypatch.setattr(MockPageGui, 'convert_text', lambda *x, **y: 'text\nwith linebreak')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_text = 'progress_text'
        testobj.initializing = False
        testobj.oldtext = 'oldtext'
        testobj.event_data = ['date', 'text']
        testobj.appbase.is_user = True
        monkeypatch.setattr(testobj, 'enable_buttons', mock_enable_buttons)
        testobj.on_text()
        assert capsys.readouterr().out == (
                "called PageGui.get_textfield_contents with args ('progress_text',)\n"
                'called Page6.enable_buttons()\n'
                "called PageGui.set_listitem_text() with args (1, 'datestring - text')\n")

        monkeypatch.setattr(MockPageGui, 'get_list_row', lambda *x: 1)
        monkeypatch.setattr(MockPageGui, 'get_listitem_text', lambda *x: 'datestring - textstring')
        monkeypatch.setattr(MockPageGui, 'convert_text', lambda *x, **y:
                            'text exceeding a certain amount of characters so that it gets chopped off')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_text = 'progress_text'
        testobj.initializing = False
        testobj.oldtext = 'oldtext'
        testobj.event_data = ['date', 'text']
        testobj.appbase.is_user = False
        testobj.enable_buttons = mock_enable_buttons
        # monkeypatch.setattr(testobj, 'enable_buttons', mock_enable_buttons)
        testobj.on_text()
        assert capsys.readouterr().out == (
                "called PageGui.get_textfield_contents with args ('progress_text',)\n"
                'called PageGui.set_listitem_text() with args'
                " (1, 'datestring - text exceeding a certain amount of characters"
                " so that it gets chopp...')\n")

    def test_initialize_new_event(self, monkeypatch, capsys):
        """unittest for Page6.initialize_new_event
        """
        def mock_get_dts():
            """stub
            """
            print('called shared.get_dts()')
            return 'datestring'
        def mock_enable_buttons():
            """stub
            """
            print('called Page6.enable_buttons()')
        monkeypatch.setattr(testee.shared, 'get_dts', mock_get_dts)
        monkeypatch.setattr(MockPageGui, 'get_list_row', lambda *x: 0)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_list = 'p0list'
        testobj.progress_text = 'prtext'
        testobj.enable_buttons = mock_enable_buttons
        testobj.book.stats = {1: ('Aangenomen', '1')}
        testobj.appbase.is_user = False
        testobj.initialize_new_event()
        assert capsys.readouterr().out == ''

        testobj.appbase.is_user = True
        testobj.event_list = ['existing']
        testobj.event_data = ['item']
        testobj.book.pagedata.status = '1'
        testobj.initialize_new_event()
        assert testobj.event_list == ['datestring', 'existing']
        assert testobj.event_data == ['', 'item']
        assert testobj.oldtext == ''
        assert capsys.readouterr().out == ('called shared.get_dts()\n'
                                           "called PageGui.create_new_listitem() with args"
                                           " ('p0list', 'prtext', 'datestring', '')\n"
                                           'called Page6.enable_buttons()\n')

        testobj.event_list = []
        testobj.event_data = []
        testobj.book.pagedata.status = '0'
        testobj.appbase.use_text_panels = True
        testobj.book.current_tab = 2
        testobj.initialize_new_event()
        assert testobj.event_list == ['datestring']
        assert testobj.event_data == ['']
        assert testobj.oldtext == ''
        assert capsys.readouterr().out == ('called shared.get_dts()\n'
                                           "called PageGui.create_new_listitem() with args"
                                           " ('p0list', 'prtext', 'datestring', '')\n"
                                           'called Page6.enable_buttons()\n')

        testobj.event_list = []
        testobj.event_data = []
        testobj.book.pagedata.status = '0'
        testobj.appbase.use_text_panels = False
        testobj.book.current_tab = 1
        testobj.initialize_new_event()
        assert testobj.event_list == ['datestring']
        assert testobj.event_data == ['']
        assert testobj.oldtext == ''
        assert capsys.readouterr().out == ('called shared.get_dts()\n'
                                           "called PageGui.create_new_listitem() with args"
                                           " ('p0list', 'prtext', 'datestring', '')\n"
                                           'called Page6.enable_buttons()\n')

        testobj.event_list = []
        testobj.event_data = []
        testobj.book.pagedata.status = '0'
        testobj.appbase.use_text_panels = True
        testobj.book.current_tab = 3
        testobj.initialize_new_event()
        assert testobj.book.pagedata.status == '1'
        assert testobj.status_auto_changed
        assert testobj.event_list == ['datestring', 'datestring']
        assert testobj.event_data == ['', 'Status gewijzigd in "Aangenomen"']
        assert testobj.oldtext == ''
        assert capsys.readouterr().out == (
                'called shared.get_dts()\n'
                "called PageGui.create_new_listitem() with args"
                " ('p0list', 'prtext', 'datestring', 'Status gewijzigd in \"Aangenomen\"')\n"
                'called shared.get_dts()\n'
                "called PageGui.create_new_listitem() with args"
                " ('p0list', 'prtext', 'datestring', '')\n"
                'called Page6.enable_buttons()\n')

        testobj.event_list = []
        testobj.event_data = []
        testobj.book.pagedata.status = '0'
        testobj.appbase.use_text_panels = False
        testobj.book.current_tab = 2
        testobj.initialize_new_event()
        assert testobj.book.pagedata.status == '1'
        assert testobj.status_auto_changed
        assert testobj.event_list == ['datestring', 'datestring']
        assert testobj.event_data == ['', 'Status gewijzigd in "Aangenomen"']
        assert testobj.oldtext == ''
        assert capsys.readouterr().out == (
                'called shared.get_dts()\n'
                "called PageGui.create_new_listitem() with args"
                " ('p0list', 'prtext', 'datestring', 'Status gewijzigd in \"Aangenomen\"')\n"
                'called shared.get_dts()\n'
                "called PageGui.create_new_listitem() with args"
                " ('p0list', 'prtext', 'datestring', '')\n"
                'called Page6.enable_buttons()\n')

    def test_build_newbuf(self, monkeypatch, capsys):
        """unittest for Page6.build_newbuf
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.event_list = ['x']
        testobj.event_data = ['y']
        assert testobj.build_newbuf() == (['x'], ['y'])


class TestTabOptions:
    """unittests for main.TabOptions
    """
    # def setup_testobj(self, monkeypatch, capsys):
    #     """stub for main.TabOptions object

    #     create the object skipping the normal initialization
    #     intercept messages during creation
    #     return the object so that other methods can be monkeypatched in the caller
    #     """
    #     def mock_init(self, *args):
    #         """stub
    #         """
    #         print('called TabOptions.__init__ with args', args)
    #     monkeypatch.setattr(testee.TabOptions, '__init__', mock_init)
    #     testobj = testee.TabOptions()
    #     assert capsys.readouterr().out == 'called TabOptions.__init__ with args ()\n'
    #     return testobj

    def test_initstuff(self, monkeypatch, capsys):
        """unittest for TabOptions.initstuff
        """
        # testobj = self.setup_testobj(monkeypatch, capsys)
        testobj = testee.TabOptions()
        parent = MockOptionsParent()
        result = testobj.initstuff(parent)
        assert result[0] == 'Tab titels'
        assert result[1] == ['eerste', 'tweede', 'derde']
        assert result[2] == {'can_add_remove': False, 'can_reorder': False}
        assert result[3] == ["De tab titels worden getoond in de volgorde",
                             "zoals ze van links naar rechts staan.",
                             "Er kunnen geen tabs worden verwijderd of toegevoegd."]

    def test_leesuit(self, monkeypatch, capsys):
        """unittest for TabOptions.leesuit
        """
        # testobj = self.setup_testobj(monkeypatch, capsys)
        testobj = testee.TabOptions()
        parent = MockOptionsParent()
        testobj.leesuit(parent, ['een', 'twee', 'drie'])
        assert testobj.newtabs == {'0': 'een', '1': 'twee', '2': 'drie'}
        assert capsys.readouterr().out == ("called MainWindow.save_settings() with args"
                                           " ('tab', {'0': 'een', '1': 'twee', '2': 'drie'})\n")


class TestStatOptions:
    """unittests for main.StatOptions
    """
    # def setup_testobj(self, monkeypatch, capsys):
    #     """stub for main.StatOptions object

    #     create the object skipping the normal initialization
    #     intercept messages during creation
    #     return the object so that other methods can be monkeypatched in the caller
    #     """
    #     def mock_init(self, *args):
    #         """stub
    #         """
    #         print('called StatOptions.__init__ with args', args)
    #     monkeypatch.setattr(testee.StatOptions, '__init__', mock_init)
    #     testobj = testee.StatOptions()
    #     assert capsys.readouterr().out == 'called StatOptions.__init__ with args ()\n'
    #     return testobj

    def test_initstuff(self, monkeypatch, capsys):
        """unittest for StatOptions.initstuff
        """
        # testobj = self.setup_testobj(monkeypatch, capsys)
        testobj = testee.StatOptions()
        parent = MockOptionsParent()
        result = testobj.initstuff(parent)
        assert result[0] == 'Status codes en waarden'
        assert result[1] == ['0: gemeld', '1: opgepakt', '2: afgehandeld']
        assert result[2] == {'can_add_remove': True, 'can_reorder': True}
        assert result[3] == ["De waarden voor de status worden getoond in dezelfde volgorde",
                             "als waarin ze in de combobox staan.",
                             "Vóór de dubbele punt staat de code, erachter de waarde.",
                             "Denk erom dat als je codes wijzigt of statussen verwijdert, deze",
                             "ook niet meer getoond en gebruikt kunnen worden in de registratie.",
                             "Omschrijvingen kun je rustig aanpassen"]

    def test_leesuit(self, monkeypatch, capsys):
        """unittest for StatOptions.leesuit
        """
        # testobj = self.setup_testobj(monkeypatch, capsys)
        testobj = testee.StatOptions()
        parent = MockOptionsParent()
        assert testobj.leesuit(parent, ['nocolon']) == 'Foutieve waarde: bevat geen dubbele punt'
        assert testobj.leesuit(parent, ['1: een', '2: twee', '3: drie']) == ''
        assert testobj.newstats == {'1': ('een', 0), '2': ('twee', 1), '3': ('drie', 2)}
        assert capsys.readouterr().out == (
                "called MainWindow.save_settings() with args"
                " ('stat', {'1': ('een', 0), '2': ('twee', 1), '3': ('drie', 2)})\n")


class TestCatOptions:
    """unittests for main.CatOptions
    """
    # def setup_testobj(self, monkeypatch, capsys):
    #     """stub for main.CatOptions object

    #     create the object skipping the normal initialization
    #     intercept messages during creation
    #     return the object so that other methods can be monkeypatched in the caller
    #     """
    #     def mock_init(self, *args):
    #         """stub
    #         """
    #         print('called CatOptions.__init__ with args', args)
    #     monkeypatch.setattr(testee.CatOptions, '__init__', mock_init)
    #     testobj = testee.CatOptions()
    #     assert capsys.readouterr().out == 'called CatOptions.__init__ with args ()\n'
    #     return testobj

    def test_initstuff(self, monkeypatch, capsys):
        """unittest for CatOptions.initstuff
        """
        # testobj = self.setup_testobj(monkeypatch, capsys)
        testobj = testee.CatOptions()
        parent = MockOptionsParent()
        result = testobj.initstuff(parent)
        assert result[0] == 'Soort codes en waarden'
        assert result[1] == [' : Onbekend', 'P: probleem', 'W: wens']
        assert result[2] == {'can_add_remove': True, 'can_reorder': True}
        assert result[3] == ["De waarden voor de soorten worden getoond in dezelfde volgorde",
                             "als waarin ze in de combobox staan.",
                             "Vóór de dubbele punt staat de code, erachter de waarde.",
                             "Denk erom dat als je codes wijzigt of soorten verwijdert, deze",
                             "ook niet meer getoond en gebruikt kunnen worden in de registratie.",
                             "Omschrijvingen kun je rustig aanpassen"]
        assert capsys.readouterr().out == ""

    def test_leesuit(self, monkeypatch, capsys):
        """unittest for CatOptions.leesuit
        """
        # testobj = self.setup_testobj(monkeypatch, capsys)
        testobj = testee.CatOptions()
        parent = MockOptionsParent()
        assert testobj.leesuit(parent, ['nocolon']) == 'Foutieve waarde: bevat geen dubbele punt'
        testobj.leesuit(parent, ['1: een', '2: twee', '3: drie'])
        assert testobj.newcats == {'1': ('een', 0), '2': ('twee', 1), '3': ('drie', 2)}
        assert capsys.readouterr().out == (
                "called MainWindow.save_settings() with args"
                " ('cat', {'1': ('een', 0), '2': ('twee', 1), '3': ('drie', 2)})\n")


class TestSortOptionsDialog:
    """unittests for main.SortOptionsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.SortOptionsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SortOptionsDialog.__init__ with args', args)
        monkeypatch.setattr(testee.SortOptionsDialog, '__init__', mock_init)
        testobj = testee.SortOptionsDialog()
        assert capsys.readouterr().out == 'called SortOptionsDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SortOptionsDialog.__init__
        """
        class MockGui:
            def __init__(self, *args):
                print('called SortOptionsDialogGui.__init__ with args', args)
            def add_checkbox_line(self, *args):
                print('called SortOptionsDialogGui.add_checkbox_line with args', args)
            def add_seqnumtext_to_line(self, text):
                print(f"called SortOptionsDialogGui.add_seqnumtext_to_line with arg '{text}'")
                return f'lbl_{text}'
            def add_colnameselector_to_line(self, *args):
                print('called SortOptionsDialogGui.add_colnameselector_to_line with args', args)
                return f'cmb_{args[1]}'
            def add_radiobuttons_to_line(self, *args):
                print('called SortOptionsDialogGui.add_radiobuttons_to_line with args', args)
                return 'rbg'
            def add_okcancel_buttonbox(self):
                print('called SortOptionsDialogGui.add_okcancel_buttonbox')
            def enable_fields(self):
                "emty function, callback reference"
        monkeypatch.setattr(testee.gui, 'SortOptionsDialogGui', MockGui)
        parent = types.SimpleNamespace(master=types.SimpleNamespace(saved_sortopts=False),
                                       sort_via_options='sortoptions')
        testobj = testee.SortOptionsDialog(parent, [('a', 'asc'), ('b', 'desc')], ['a', 'b'])
        assert testobj.parent == parent
        assert testobj.sortopts == [('a', 'asc'), ('b', 'desc')]
        assert testobj.widgets == [('lbl_  0.', 'cmb_a', 'rbg'), ('lbl_  1.', 'cmb_b', 'rbg')]
        assert capsys.readouterr().out == (
                "called SortOptionsDialogGui.__init__ with args"
                f" ({testobj}, {testobj.parent}, 'Sorteren op meer dan 1 kolom')\n"
                "called SortOptionsDialogGui.add_checkbox_line with args"
                f" ('Multi-sorteren mogelijk', 'sortoptions', {testobj.gui.enable_fields})\n"
                "called SortOptionsDialogGui.add_seqnumtext_to_line with arg '  0.'\n"
                "called SortOptionsDialogGui.add_colnameselector_to_line with args"
                " (['a', 'b'], 'a')\n"
                "called SortOptionsDialogGui.add_radiobuttons_to_line with args"
                " ([(' Asc ', 1, True), ('Desc', 2, False)],)\n"
                "called SortOptionsDialogGui.add_seqnumtext_to_line with arg '  1.'\n"
                "called SortOptionsDialogGui.add_colnameselector_to_line with args"
                " (['a', 'b'], 'b')\n"
                "called SortOptionsDialogGui.add_radiobuttons_to_line with args"
                " ([(' Asc ', 1, False), ('Desc', 2, True)],)\n"
                "called SortOptionsDialogGui.add_okcancel_buttonbox\n")
        # Waarschtijnlijk zijn de volgende twee situaties niet mogelijk:
        testobj = testee.SortOptionsDialog(parent, [], ['a', 'b'])
        assert testobj.parent == parent
        assert testobj.sortopts == []
        assert testobj.widgets == [('lbl_  0.', 'cmb_a', 'rbg'), ('lbl_  1.', 'cmb_b', 'rbg')]
        assert capsys.readouterr().out == (
                "called SortOptionsDialogGui.__init__ with args"
                f" ({testobj}, {testobj.parent}, 'Sorteren op meer dan 1 kolom')\n"
                "called SortOptionsDialogGui.add_checkbox_line with args"
                f" ('Multi-sorteren mogelijk', 'sortoptions', {testobj.gui.enable_fields})\n"
                "called SortOptionsDialogGui.add_seqnumtext_to_line with arg '  0.'\n"
                "called SortOptionsDialogGui.add_colnameselector_to_line with args"
                " (['a', 'b'], 'a')\n"
                "called SortOptionsDialogGui.add_radiobuttons_to_line with args"
                " ([(' Asc ', 1, True), ('Desc', 2, False)],)\n"
                "called SortOptionsDialogGui.add_seqnumtext_to_line with arg '  1.'\n"
                "called SortOptionsDialogGui.add_colnameselector_to_line with args"
                " (['a', 'b'], 'b')\n"
                "called SortOptionsDialogGui.add_radiobuttons_to_line with args"
                " ([(' Asc ', 1, True), ('Desc', 2, False)],)\n"
                "called SortOptionsDialogGui.add_okcancel_buttonbox\n")
        testobj = testee.SortOptionsDialog(parent, [('a', 'asc'), ('b', 'desc')], [])
        assert testobj.parent == parent
        assert testobj.sortopts == [('a', 'asc'), ('b', 'desc')]
        assert testobj.widgets == []
        assert capsys.readouterr().out == (
                "called SortOptionsDialogGui.__init__ with args"
                f" ({testobj}, {testobj.parent}, 'Sorteren op meer dan 1 kolom')\n"
                "called SortOptionsDialogGui.add_checkbox_line with args"
                f" ('Multi-sorteren mogelijk', 'sortoptions', {testobj.gui.enable_fields})\n"
                "called SortOptionsDialogGui.add_okcancel_buttonbox\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for SortOptionsDialog.confirm
        """
        class MockGui:
            def get_combobox_value(self, *args):
                print('called SortOptionsDialogGui.get_combobox_value with args', args)
                return args[0]
            def get_rbgroup_value(self, *args):
                print('called SortOptionsDialogGui.get_rbgroup_value with args', args)
                return int(args[0][3])
            def get_checkbox_value(self, *args):
                print('called SortOptionsDialogGui.get_checkbox_value with args', args)
                return False
        def mock_show(*args):
            print('called gui.show.message with args', args)
        def mock_save(*args):
            print('called saved_sortopts.save_options with args', args)
        def mock_get(*args):
            print('called SortOptionsDialogGui.get_checkbox_value with args', args)
            return True
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(master=types.SimpleNamespace(sort_via_options=False),
                                               saved_sortopts=None)
        testobj.gui = MockGui()
        testobj.widgets = []
        testobj.on_off = 'on_off'
        testobj.sortopts = {}
        assert not testobj.confirm()
        assert not testobj.parent.master.sort_via_options
        assert capsys.readouterr().out == (
                "called SortOptionsDialogGui.get_checkbox_value with args ('on_off',)\n"
                "called gui.show.message with args"
                f" ({testobj.gui}, 'Probreg', 'U heeft niets gewijzigd')\n")
        testobj.parent.master.sort_via_options = True
        assert testobj.confirm()
        assert not testobj.parent.master.sort_via_options
        assert capsys.readouterr().out == (
                "called SortOptionsDialogGui.get_checkbox_value with args ('on_off',)\n")
        testobj.parent.master.sort_via_options = True
        testobj.gui.get_checkbox_value = mock_get
        assert not testobj.confirm()
        assert testobj.parent.master.sort_via_options
        assert capsys.readouterr().out == (
                "called SortOptionsDialogGui.get_checkbox_value with args ('on_off',)\n"
                "called gui.show.message with args"
                f" ({testobj.gui}, 'Probreg', 'U heeft niets gewijzigd')\n")
        testobj.parent.master.sort_via_options = False
        testobj.parent.saved_sortopts = types.SimpleNamespace(save_options=mock_save)
        assert testobj.confirm()
        assert testobj.parent.master.sort_via_options
        assert capsys.readouterr().out == (
                "called SortOptionsDialogGui.get_checkbox_value with args ('on_off',)\n"
                "called saved_sortopts.save_options with args ({},)\n")
        testobj.widgets = [('ww', '', 'rbg1'), ('xx', 'combo1', 'rbg1'), ('yy', 'combo2', 'rbg2'),
                           ('zz', '(geen)', 'rbg1')]
        assert testobj.confirm()
        assert testobj.parent.master.sort_via_options
        assert capsys.readouterr().out == (
                "called SortOptionsDialogGui.get_combobox_value with args ('',)\n"
                "called SortOptionsDialogGui.get_rbgroup_value with args ('rbg1',)\n"
                "called SortOptionsDialogGui.get_combobox_value with args ('combo1',)\n"
                "called SortOptionsDialogGui.get_rbgroup_value with args ('rbg1',)\n"
                "called SortOptionsDialogGui.get_combobox_value with args ('combo2',)\n"
                "called SortOptionsDialogGui.get_rbgroup_value with args ('rbg2',)\n"
                "called SortOptionsDialogGui.get_combobox_value with args ('(geen)',)\n"
                "called SortOptionsDialogGui.get_rbgroup_value with args ('rbg1',)\n"
                "called SortOptionsDialogGui.get_checkbox_value with args ('on_off',)\n"
                "called saved_sortopts.save_options with args"
                " ({1: ('combo1', 'asc'), 2: ('combo2', 'desc')},)\n")


class TestSelectOptionsDialog:
    """unittests for main.SelectOptionsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.SelectOptionsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SelectOptionsDialog.__init__ with args', args)
        monkeypatch.setattr(testee.SelectOptionsDialog, '__init__', mock_init)
        testobj = testee.SelectOptionsDialog()
        assert capsys.readouterr().out == 'called SelectOptionsDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.__init__
        """
        class MockGui:
            "stub"
            def __init__(self, *args):
                print('called SelectOptionsDialogGui.__init__ with args', args)
            def add_checkbox_to_grid(self, *args):
                print('called SelectOptionsDialogGui.add_checkbox_to_grid with args', args)
                return args[0]
            def start_optionsblock(self, *args):
                print('called SelectOptionsDialogGui.start_optionsblock with args', args)
                return 'block'
            def add_textentry_line_to_block(self, *args):
                print('called SelectOptionsDialogGui.add_textentry_line_to_block with args', args)
                return args[1]
            def add_radiobuttonrow_to_block(self, *args, **kwargs):
                print('called SelectOptionsDialogGui.add_radiobuttonrow_to_block with args',
                      args, kwargs)
                return args[1][0]
            def add_checkboxlist_to_block(self, *args):
                print('called SelectOptionsDialogGui.add_checkboxlist_to_block with args', args)
                return args[1][0]
            def finish_block(self, *args):
                print('called SelectOptionsDialogGui.finish_block with args', args)
            def add_okcancel_buttonbar(self):
                print('called SelectOptionsDialogGui.add_okcancel_buttonbar')
            def finalize_display(self):
                print('called SelectOptionsDialogGui.finalize_display')
            def on_text(self):
                "empty function, callback reference"
            def on_cb_checked(self):
                "empty function, callback reference"
            def on_rb_checked(self):
                "empty function, callback reference"
        def mock_set(self, *args):
            "stub"
            print('called SelectOptionsDialog.set_default_values with args', args)
        monkeypatch.setattr(testee.gui, 'SelectOptionsDialogGui', MockGui)
        monkeypatch.setattr(testee.SelectOptionsDialog, 'set_default_values', mock_set)
        parent = types.SimpleNamespace(use_separate_subject=False)
        parent.book = types.SimpleNamespace(
            ctitels=['actie', 'soort', 'status', '', 'titel'],
            cats={2: 'b', 1: 'a'}, stats={1: 'x', 2: 'y'})
        testobj = testee.SelectOptionsDialog(parent, {'sel': 'args'}, {'sel': 'data'})
        assert testobj.row == 4
        assert testobj.cb_actie == 'actie   -'
        assert testobj.action_gt == 'groter dan:'
        assert testobj.action_andor == 'and'
        assert testobj.action_lt == 'kleiner dan:'
        assert testobj.cb_soort == 'soort   -'
        assert testobj.check_cats == 'a'
        assert testobj.cb_status == 'status   -'
        assert testobj.check_stats == 'x'
        assert testobj.cb_zoek == 'titel   -'
        assert testobj.text_zoek == 'zoek naar:'
        # assert testobj.zoek_andor == 'and'
        # assert testobj.text_zoek == ''
        assert testobj.cb_arch == 'Archief    -'
        assert testobj.radio_arch == 'Alleen gearchiveerd'
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.__init__ with args"
                f" ({testobj}, {testobj.parent}, 'Selecteren')\n"
                "called SelectOptionsDialogGui.add_checkbox_to_grid with args"
                " ('actie   -', 0, 0)\n"
                "called SelectOptionsDialogGui.start_optionsblock with args ()\n"
                "called SelectOptionsDialogGui.add_textentry_line_to_block with args"
                f" ('block', 'groter dan:', {testobj.gui.on_text})\n"
                "called SelectOptionsDialogGui.add_radiobuttonrow_to_block with args"
                " ('block', ['and', 'or']) {}\n"
                "called SelectOptionsDialogGui.add_textentry_line_to_block with args"
                f" ('block', 'kleiner dan:', {testobj.gui.on_text})\n"
                "called SelectOptionsDialogGui.finish_block with args ('block', 0, 1)\n"
                "called SelectOptionsDialogGui.add_checkbox_to_grid with args"
                " ('soort   -', 1, 0)\n"
                "called SelectOptionsDialogGui.start_optionsblock with args ()\n"
                "called SelectOptionsDialogGui.add_checkboxlist_to_block with args"
                f" ('block', ['a', 'b'], {testobj.gui.on_cb_checked})\n"
                "called SelectOptionsDialogGui.finish_block with args ('block', 1, 1)\n"
                "called SelectOptionsDialogGui.add_checkbox_to_grid with args"
                " ('status   -', 2, 0)\n"
                "called SelectOptionsDialogGui.start_optionsblock with args ()\n"
                "called SelectOptionsDialogGui.add_checkboxlist_to_block with args"
                f" ('block', ['x', 'y'], {testobj.gui.on_cb_checked})\n"
                "called SelectOptionsDialogGui.finish_block with args ('block', 2, 1)\n"
                "called SelectOptionsDialogGui.add_checkbox_to_grid with args"
                " ('titel   -', 3, 0)\n"
                "called SelectOptionsDialogGui.start_optionsblock with args ()\n"
                "called SelectOptionsDialogGui.add_textentry_line_to_block with args"
                f" ('block', 'zoek naar:', {testobj.gui.on_text})\n"
                "called SelectOptionsDialogGui.finish_block with args ('block', 3, 1)\n"
                "called SelectOptionsDialogGui.add_checkbox_to_grid with args"
                " ('Archief    -', 4, 0)\n"
                "called SelectOptionsDialogGui.start_optionsblock with args ()\n"
                "called SelectOptionsDialogGui.add_radiobuttonrow_to_block with args"
                " ('block', ['Alleen gearchiveerd', 'gearchiveerd en lopend'],"
                f" {testobj.gui.on_rb_checked}) {{'alignleft': False}}\n"
                "called SelectOptionsDialogGui.finish_block with args ('block', 4, 1)\n"
                "called SelectOptionsDialogGui.add_okcancel_buttonbar\n"
                "called SelectOptionsDialogGui.finalize_display\n"
                "called SelectOptionsDialog.set_default_values with args ({'sel': 'args'},)\n")
        parent.use_separate_subject = True
        parent.book.ctitels = ['actie', 'soort', 'status', '', 'betreft', 'omschrijving']
        testobj = testee.SelectOptionsDialog(parent, {'sel': 'args'}, {'sel': 'data'})
        assert testobj.row == 4
        assert testobj.cb_actie == 'actie   -'
        assert testobj.action_gt == 'groter dan:'
        assert testobj.action_andor == 'and'
        assert testobj.action_lt == 'kleiner dan:'
        assert testobj.cb_soort == 'soort   -'
        assert testobj.check_cats == 'a'
        assert testobj.cb_status == 'status   -'
        assert testobj.check_stats == 'x'
        assert testobj.cb_zoek == 'zoek in   -'
        assert testobj.text_zoek == 'betreft'
        assert testobj.zoek_andor == 'and'
        assert testobj.text_zoek2 == 'omschrijving'
        assert testobj.cb_arch == 'Archief    -'
        assert testobj.radio_arch == 'Alleen gearchiveerd'
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.__init__ with args"
                f" ({testobj}, {testobj.parent}, 'Selecteren')\n"
                "called SelectOptionsDialogGui.add_checkbox_to_grid with args"
                " ('actie   -', 0, 0)\n"
                "called SelectOptionsDialogGui.start_optionsblock with args ()\n"
                "called SelectOptionsDialogGui.add_textentry_line_to_block with args"
                f" ('block', 'groter dan:', {testobj.gui.on_text})\n"
                "called SelectOptionsDialogGui.add_radiobuttonrow_to_block with args"
                " ('block', ['and', 'or']) {}\n"
                "called SelectOptionsDialogGui.add_textentry_line_to_block with args"
                f" ('block', 'kleiner dan:', {testobj.gui.on_text})\n"
                "called SelectOptionsDialogGui.finish_block with args ('block', 0, 1)\n"
                "called SelectOptionsDialogGui.add_checkbox_to_grid with args"
                " ('soort   -', 1, 0)\n"
                "called SelectOptionsDialogGui.start_optionsblock with args ()\n"
                "called SelectOptionsDialogGui.add_checkboxlist_to_block with args"
                f" ('block', ['a', 'b'], {testobj.gui.on_cb_checked})\n"
                "called SelectOptionsDialogGui.finish_block with args ('block', 1, 1)\n"
                "called SelectOptionsDialogGui.add_checkbox_to_grid with args"
                " ('status   -', 2, 0)\n"
                "called SelectOptionsDialogGui.start_optionsblock with args ()\n"
                "called SelectOptionsDialogGui.add_checkboxlist_to_block with args"
                f" ('block', ['x', 'y'], {testobj.gui.on_cb_checked})\n"
                "called SelectOptionsDialogGui.finish_block with args ('block', 2, 1)\n"
                "called SelectOptionsDialogGui.add_checkbox_to_grid with args"
                " ('zoek in   -', 3, 0)\n"
                "called SelectOptionsDialogGui.start_optionsblock with args ()\n"
                "called SelectOptionsDialogGui.add_textentry_line_to_block with args"
                f" ('block', 'betreft', {testobj.gui.on_text})\n"
                "called SelectOptionsDialogGui.add_radiobuttonrow_to_block with args"
                " ('block', ['and', 'or']) {}\n"
                "called SelectOptionsDialogGui.add_textentry_line_to_block with args"
                f" ('block', 'omschrijving', {testobj.gui.on_text})\n"
                "called SelectOptionsDialogGui.finish_block with args ('block', 3, 1)\n"
                "called SelectOptionsDialogGui.add_checkbox_to_grid with args"
                f" ('Archief    -', 4, 0)\n"
                "called SelectOptionsDialogGui.start_optionsblock with args ()\n"
                "called SelectOptionsDialogGui.add_radiobuttonrow_to_block with args"
                " ('block', ['Alleen gearchiveerd', 'gearchiveerd en lopend'],"
                f" {testobj.gui.on_rb_checked}) {{'alignleft': False}}\n"
                "called SelectOptionsDialogGui.finish_block with args ('block', 4, 1)\n"
                "called SelectOptionsDialogGui.add_okcancel_buttonbar\n"
                "called SelectOptionsDialogGui.finalize_display\n"
                "called SelectOptionsDialog.set_default_values with args ({'sel': 'args'},)\n")

    def test_set_default_values(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.set_default_values
        """
        class MockGui:
            def set_textentry_value(self, *args):
                print('called SelectOptionsDialogGui.set_textentry_value with args', args)
            def set_radiobutton_value(self, *args):
                print('called SelectOptionsDialogGui.set_radiobutton_value with args', args)
            def set_checkbox_value(self, *args):
                print('called SelectOptionsDialogGui.set_checkbox_value with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(parent=types.SimpleNamespace(
            use_separate_subject=False, cats={'0': ('x', 'a'), '1': ('y', 'b'), '2': ('z', 'c')},
            stats={'0': ('a', 'x'), '1': ('b', 'y'), '2': ('c', 'z')}))
        testobj.gui = MockGui()
        testobj.cb_actie = 'actie'
        testobj.text_gt = 'text_gt'
        testobj.action_andor = ['text_and', 'text_or']
        testobj.text_lt = 'text_lt'
        testobj.cb_soort = 'soort'
        testobj.check_cats = ['cat1', 'cat2', 'cat3']
        testobj.cb_status = 'status'
        testobj.check_stats = ['stat1', 'stat2', 'stat3']
        testobj.cb_zoek = 'zoek'
        testobj.text_zoek = 'zoek'
        testobj.zoek_andor = ['zoek_1', 'zoek_2']
        testobj.text_zoek2 = 'zoek2'
        testobj.cb_arch = 'arch'
        testobj.radio_arch = ['arch1', 'arch2']
        testobj.set_default_values({})
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.set_checkbox_value with args ('actie', False)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('soort', False)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('status', False)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('zoek', False)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('arch', False)\n")
        testobj.set_default_values({'idlt': 'xxx', 'soort': ('b', 'c'), 'status': ('x', 'y'),
                                    'titel': 'yyy', 'arch': 'arch'})
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.set_textentry_value with args ('text_lt', 'xxx')\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('actie', True)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('cat2', True)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('cat3', True)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('soort', True)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('stat1', True)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('stat2', True)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('status', True)\n"
                "called SelectOptionsDialogGui.set_textentry_value with args ('zoek', 'yyy')\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('zoek', True)\n"
                "called SelectOptionsDialogGui.set_radiobutton_value with args ('arch1', True)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('arch', True)\n")
        testobj.parent.parent.use_separate_subject = True
        testobj.set_default_values({'idgt': 'qqq', 'id': 'and', 'idlt': 'xxx',
                                    'soort': ('a',), 'status': ('z',),
                                    'titel': [('about', 'yyy')], 'arch': 'alles'})
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.set_textentry_value with args ('text_gt', 'qqq')\n"
                "called SelectOptionsDialogGui.set_radiobutton_value with args ('text_and', True)\n"
                "called SelectOptionsDialogGui.set_textentry_value with args ('text_lt', 'xxx')\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('actie', True)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('cat1', True)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('soort', True)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('stat3', True)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('status', True)\n"
                "called SelectOptionsDialogGui.set_textentry_value with args ('zoek', 'yyy')\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('zoek', True)\n"
                "called SelectOptionsDialogGui.set_radiobutton_value with args ('arch2', True)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('arch', True)\n")
        testobj.set_default_values({'idgt': 'qqq', 'id': 'or', 'idlt': 'xxx',
                                    'soort': (), 'status': (),
                                    'titel': [('about', 'yyy'), ('of', ''), ('title', 'zzz')]})
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.set_textentry_value with args ('text_gt', 'qqq')\n"
                "called SelectOptionsDialogGui.set_radiobutton_value with args ('text_or', True)\n"
                "called SelectOptionsDialogGui.set_textentry_value with args ('text_lt', 'xxx')\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('actie', True)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('soort', False)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('status', False)\n"
                "called SelectOptionsDialogGui.set_textentry_value with args ('zoek', 'yyy')\n"
                "called SelectOptionsDialogGui.set_radiobutton_value with args ('zoek_1', True)\n"
                "called SelectOptionsDialogGui.set_textentry_value with args ('zoek2', 'zzz')\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('zoek', True)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('arch', False)\n")
        testobj.set_default_values({'titel': [('about', 'yyy'), ('en', ''), ('title', 'zzz')]})
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.set_checkbox_value with args ('actie', False)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('soort', False)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('status', False)\n"
                "called SelectOptionsDialogGui.set_textentry_value with args ('zoek', 'yyy')\n"
                "called SelectOptionsDialogGui.set_radiobutton_value with args ('zoek_2', True)\n"
                "called SelectOptionsDialogGui.set_textentry_value with args ('zoek2', 'zzz')\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('zoek', True)\n"
                "called SelectOptionsDialogGui.set_checkbox_value with args ('arch', False)\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.confirm
        """
        def mock_show(*args):
            print('called gui.show_error with args', args)
        def mock_get(*args):
            print('called SelectOptionsDialogGui.get_checkbox_value with args', args)
            return False
        def mock_get_2(*args):
            print('called SelectOptionsDialogGui.get_checkbox_value with args', args)
            return True
        def mock_set(*args):
            print('called SelectOptionsDialogGui.set_focus_to with args', args)
        def mock_get_actie():
            print('called SelectOptionsDialog.get_actie_selargs')
            return False, {}
        def mock_get_actie_2():
            print('called SelectOptionsDialog.get_actie_selargs')
            return True, {'actie': 'xxx'}
        def mock_get_cat():
            print('called SelectOptionsDialog.get_cat_selargs')
            return []
        def mock_get_cat_2():
            print('called SelectOptionsDialog.get_cat_selargs')
            return ['x']
        def mock_get_stat():
            print('called SelectOptionsDialog.get_stat_selargs')
            return []
        def mock_get_stat_2():
            print('called SelectOptionsDialog.get_stat_selargs')
            return ['y']
        def mock_get_search():
            print('called SelectOptionsDialog.get_search_selargs')
            return False, {}
        def mock_get_search_2():
            print('called SelectOptionsDialog.get_search_selargs')
            return True, {'search': 'xxx'}
        def mock_get_arch(*args):
            print('called SelectOptionsDialog.get_arch_selargs with args', args)
            return '', ''
        def mock_get_arch_2(*args):
            print('called SelectOptionsDialog.get_arch_selargs with args', args)
            return 'xxx', 'yyy'
        def mock_save(*args):
            print('called SelOptions.save with args', args)
        monkeypatch.setattr(testee.gui, 'show_error', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.cb_actie = 'cb_actie'
        testobj.action_andor = ('actie_andor', '')
        testobj.cb_soort = 'cb_soort'
        testobj.cb_status = 'cb_status'
        testobj.zoek_andor = ('zoek_andor', '')
        testobj.cb_zoek = 'cb_zoek'
        testobj.cb_arch = 'cb_arch'
        testobj.gui = types.SimpleNamespace(get_checkbox_value=mock_get, set_focus_to=mock_set)
        testobj.get_actie_selargs = mock_get_actie
        testobj.get_cat_selargs = mock_get_cat
        testobj.get_stat_selargs = mock_get_stat
        testobj.get_search_selargs = mock_get_search
        testobj.get_arch_selargs = mock_get_arch
        testobj.parent = types.SimpleNamespace(parent=types.SimpleNamespace())
        testobj._data = None
        assert testobj.confirm()
        assert testobj.parent.selection == 'excl. gearchiveerde'
        assert testobj.parent.sel_args == {}
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_checkbox_value with args ('cb_actie',)\n"
                "called SelectOptionsDialogGui.get_checkbox_value with args ('cb_soort',)\n"
                "called SelectOptionsDialogGui.get_checkbox_value with args ('cb_status',)\n"
                "called SelectOptionsDialogGui.get_checkbox_value with args ('cb_zoek',)\n"
                "called SelectOptionsDialogGui.get_checkbox_value with args ('cb_arch',)\n")
        testobj.gui.get_checkbox_value = mock_get_2
        testobj._data = types.SimpleNamespace(save_options=mock_save)
        assert not testobj.confirm()
        assert testobj.parent.selection == 'excl. gearchiveerde'
        assert testobj.parent.sel_args == {}
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_checkbox_value with args ('cb_actie',)\n"
                "called SelectOptionsDialog.get_actie_selargs\n"
                "called gui.show_error with args"
                f" ({testobj.gui}, 'Kies een verbindende conditie voor actie selecties')\n"
                "called SelectOptionsDialogGui.set_focus_to with args ('actie_andor',)\n")
        testobj.get_actie_selargs = mock_get_actie_2
        assert not testobj.confirm()
        assert testobj.parent.selection == 'excl. gearchiveerde'
        assert testobj.parent.sel_args == {}
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_checkbox_value with args ('cb_actie',)\n"
                "called SelectOptionsDialog.get_actie_selargs\n"
                "called SelectOptionsDialogGui.get_checkbox_value with args ('cb_soort',)\n"
                "called SelectOptionsDialog.get_cat_selargs\n"
                "called SelectOptionsDialogGui.get_checkbox_value with args ('cb_status',)\n"
                "called SelectOptionsDialog.get_stat_selargs\n"
                "called SelectOptionsDialogGui.get_checkbox_value with args ('cb_zoek',)\n"
                "called SelectOptionsDialog.get_search_selargs\n"
                "called gui.show_error with args"
                f" ({testobj.gui}, 'Kies een verbindende conditie voor zoekargumenten')\n"
                "called SelectOptionsDialogGui.set_focus_to with args ('zoek_andor',)\n")
        testobj.get_cat_selargs = mock_get_cat_2
        testobj.get_stat_selargs = mock_get_stat_2
        testobj.get_search_selargs = mock_get_search_2
        assert testobj.confirm()
        assert testobj.parent.selection == ''
        assert testobj.parent.sel_args == {'actie': 'xxx', 'soort': ['x'], 'status': ['y'],
                                           'search': 'xxx'}
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_checkbox_value with args ('cb_actie',)\n"
                "called SelectOptionsDialog.get_actie_selargs\n"
                "called SelectOptionsDialogGui.get_checkbox_value with args ('cb_soort',)\n"
                "called SelectOptionsDialog.get_cat_selargs\n"
                "called SelectOptionsDialogGui.get_checkbox_value with args ('cb_status',)\n"
                "called SelectOptionsDialog.get_stat_selargs\n"
                "called SelectOptionsDialogGui.get_checkbox_value with args ('cb_zoek',)\n"
                "called SelectOptionsDialog.get_search_selargs\n"
                "called SelectOptionsDialogGui.get_checkbox_value with args ('cb_arch',)\n"
                "called SelectOptionsDialog.get_arch_selargs with args ('(gefilterd)',)\n"
                "called SelOptions.save with args"
                " ({'actie': 'xxx', 'soort': ['x'], 'status': ['y'], 'search': 'xxx'},)\n")
        testobj.get_arch_selargs = mock_get_arch_2
        assert testobj.confirm()
        assert testobj.parent.selection == 'xxx'
        assert testobj.parent.sel_args == {'actie': 'xxx', 'soort': ['x'], 'status': ['y'],
                                           'search': 'xxx', 'arch': 'yyy'}
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_checkbox_value with args ('cb_actie',)\n"
                "called SelectOptionsDialog.get_actie_selargs\n"
                "called SelectOptionsDialogGui.get_checkbox_value with args ('cb_soort',)\n"
                "called SelectOptionsDialog.get_cat_selargs\n"
                "called SelectOptionsDialogGui.get_checkbox_value with args ('cb_status',)\n"
                "called SelectOptionsDialog.get_stat_selargs\n"
                "called SelectOptionsDialogGui.get_checkbox_value with args ('cb_zoek',)\n"
                "called SelectOptionsDialog.get_search_selargs\n"
                "called SelectOptionsDialogGui.get_checkbox_value with args ('cb_arch',)\n"
                "called SelectOptionsDialog.get_arch_selargs with args ('(gefilterd)',)\n"
                "called SelOptions.save with args ({'actie': 'xxx',"
                " 'soort': ['x'], 'status': ['y'], 'search': 'xxx', 'arch': 'yyy'},)\n")

    def test_get_actie_selargs(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.get_actie_selargs
        """
        def mock_get_text(*args):
            print('called SelectOptionsDialogGui.get_textentry_value with args', args)
            return ''
        def mock_get_text_2(*args):
            print('called SelectOptionsDialogGui.get_textentry_value with args', args)
            return args[0] if args[0] == 'text_gt' else ''
        def mock_get_text_3(*args):
            print('called SelectOptionsDialogGui.get_textentry_value with args', args)
            return args[0] if args[0] == 'text_lt' else ''
        def mock_get_text_4(*args):
            print('called SelectOptionsDialogGui.get_textentry_value with args', args)
            return args[0]
        def mock_get_rb(*args):
            print('called SelectOptionsDialogGui.get_radiobutton_value with args', args)
            return False
        def mock_get_rb_2(*args):
            print('called SelectOptionsDialogGui.get_radiobutton_value with args', args)
            return args[0] == 'and'
        def mock_get_rb_3(*args):
            print('called SelectOptionsDialogGui.get_radiobutton_value with args', args)
            return args[0] == 'or'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.text_gt = 'text_gt'
        testobj.text_andor = ('and', 'or')
        testobj.text_lt = 'text_lt'
        testobj.gui = types.SimpleNamespace(get_textentry_value=mock_get_text,
                                            get_radiobutton_value=mock_get_rb)
        assert testobj.get_actie_selargs() == (True, {})
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_textentry_value with args ('text_gt',)\n"
                "called SelectOptionsDialogGui.get_textentry_value with args ('text_lt',)\n")
        testobj.gui.get_textentry_value = mock_get_text_2
        assert testobj.get_actie_selargs() == (True, {'idgt': 'text_gt'})
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_textentry_value with args ('text_gt',)\n"
                "called SelectOptionsDialogGui.get_textentry_value with args ('text_lt',)\n")
        testobj.gui.get_textentry_value = mock_get_text_3
        assert testobj.get_actie_selargs() == (True, {'idlt': 'text_lt'})
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_textentry_value with args ('text_gt',)\n"
                "called SelectOptionsDialogGui.get_textentry_value with args ('text_lt',)\n")
        testobj.gui.get_textentry_value = mock_get_text_4
        assert testobj.get_actie_selargs() == (False, {})
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_textentry_value with args ('text_gt',)\n"
                "called SelectOptionsDialogGui.get_textentry_value with args ('text_lt',)\n"
                "called SelectOptionsDialogGui.get_radiobutton_value with args ('and',)\n"
                "called SelectOptionsDialogGui.get_radiobutton_value with args ('or',)\n")
        testobj.gui.get_radiobutton_value = mock_get_rb_2
        assert testobj.get_actie_selargs() == (True,
                                               {'idgt': 'text_gt', 'idlt': 'text_lt', 'id': 'and'})
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_textentry_value with args ('text_gt',)\n"
                "called SelectOptionsDialogGui.get_textentry_value with args ('text_lt',)\n"
                "called SelectOptionsDialogGui.get_radiobutton_value with args ('and',)\n")
        testobj.gui.get_radiobutton_value = mock_get_rb_3
        assert testobj.get_actie_selargs() == (True,
                                               {'idgt': 'text_gt', 'idlt': 'text_lt', 'id': 'or'})
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_textentry_value with args ('text_gt',)\n"
                "called SelectOptionsDialogGui.get_textentry_value with args ('text_lt',)\n"
                "called SelectOptionsDialogGui.get_radiobutton_value with args ('and',)\n"
                "called SelectOptionsDialogGui.get_radiobutton_value with args ('or',)\n")

    def test_get_cat_selargs(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.get_cat_selargs
        """
        def mock_get(arg):
            print('called SelectOptionsDialogGui.get_checkbox_value with arg', arg)
            return False
        def mock_get_2(arg):
            print('called SelectOptionsDialogGui.get_checkbox_value with arg', arg)
            return True
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(parent=types.SimpleNamespace(cats={}))
        testobj.gui = types.SimpleNamespace(get_checkbox_value=mock_get)
        testobj.check_cats = []
        assert testobj.get_cat_selargs() == []
        assert capsys.readouterr().out == ""
        testobj.check_cats = ['cat1', 'cat2']
        assert testobj.get_cat_selargs() == []
        assert capsys.readouterr().out == ""
        testobj.parent.parent.cats = {0: ('yyy', 'sel_y')}
        assert testobj.get_cat_selargs() == []
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_checkbox_value with arg cat1\n")
        testobj.gui = types.SimpleNamespace(get_checkbox_value=mock_get_2)
        assert testobj.get_cat_selargs() == ['sel_y']
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_checkbox_value with arg cat1\n")
        testobj.parent.parent.cats = {0: ('yyy', 'sel_y'), 1: ('xxx', 'sel_x')}
        assert testobj.get_cat_selargs() == ['sel_y', 'sel_x']
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_checkbox_value with arg cat1\n"
                "called SelectOptionsDialogGui.get_checkbox_value with arg cat2\n")
        testobj.parent.parent.cats = {0: ('yyy', 'sel_y'), 1: ('xxx', 'sel_x'), 2: ('zzz', 'sel_z')}
        with pytest.raises(IndexError):
            testobj.get_cat_selargs()

    def test_get_stat_selargs(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.get_stat_selargs
        """
        def mock_get(arg):
            print('called SelectOptionsDialogGui.get_checkbox_value with arg', arg)
            return False
        def mock_get_2(arg):
            print('called SelectOptionsDialogGui.get_checkbox_value with arg', arg)
            return True
        testobj = self.setup_testobj(monkeypatch, capsys)
        # assert testobj.get_stat_selargs() == "expected_result"
        # assert capsys.readouterr().out == ("")
        testobj.parent = types.SimpleNamespace(parent=types.SimpleNamespace(stats={}))
        testobj.gui = types.SimpleNamespace(get_checkbox_value=mock_get)
        testobj.check_stats = []
        assert testobj.get_stat_selargs() == []
        assert capsys.readouterr().out == ""
        testobj.check_stats = ['stat1', 'stat2']
        assert testobj.get_stat_selargs() == []
        assert capsys.readouterr().out == ""
        testobj.parent.parent.stats = {0: ('yyy', 'sel_y')}
        assert testobj.get_stat_selargs() == []
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_checkbox_value with arg stat1\n")
        testobj.gui = types.SimpleNamespace(get_checkbox_value=mock_get_2)
        assert testobj.get_stat_selargs() == ['sel_y']
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_checkbox_value with arg stat1\n")
        testobj.parent.parent.stats = {0: ('yyy', 'sel_y'), 1: ('xxx', 'sel_x')}
        assert testobj.get_stat_selargs() == ['sel_y', 'sel_x']
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_checkbox_value with arg stat1\n"
                "called SelectOptionsDialogGui.get_checkbox_value with arg stat2\n")
        testobj.parent.parent.stats = {0: ('yyy', 'sel_y'), 1: ('xxx', 'sel_x'), 2: ('zzz', 'sel_z')}
        with pytest.raises(IndexError):
            testobj.get_stat_selargs()

    def test_get_search_selargs(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.get_search_selargs
        """
        def mock_get_text(*args):
            print('called SelectOptionsDialogGui.get_textentry_value with args', args)
            return ''
        def mock_get_text_2(*args):
            print('called SelectOptionsDialogGui.get_textentry_value with args', args)
            return args[0] if args[0] == 'zoek' else ''
        def mock_get_text_3(*args):
            print('called SelectOptionsDialogGui.get_textentry_value with args', args)
            return args[0] if args[0] == 'zoek2' else ''
        def mock_get_text_4(*args):
            print('called SelectOptionsDialogGui.get_textentry_value with args', args)
            return args[0]
        def mock_get_rb(*args):
            print('called SelectOptionsDialogGui.get_radiobutton_value with args', args)
            return False
        def mock_get_rb_2(*args):
            print('called SelectOptionsDialogGui.get_radiobutton_value with args', args)
            return args[0] == 'and'
        def mock_get_rb_3(*args):
            print('called SelectOptionsDialogGui.get_radiobutton_value with args', args)
            return args[0] == 'or'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(
                parent=types.SimpleNamespace(use_separate_subject=False))
        testobj.text_zoek = 'zoek'
        testobj.zoek_andor = ('and', 'or')
        testobj.text_zoek2 = 'zoek2'
        testobj.gui = types.SimpleNamespace(get_textentry_value=mock_get_text,
                                            get_radiobutton_value=mock_get_rb)
        assert testobj.get_search_selargs() == (True, {})
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_textentry_value with args ('zoek',)\n")
        testobj.gui.get_textentry_value = mock_get_text_2
        assert testobj.get_search_selargs() == (True, {'titel': 'zoek'})
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_textentry_value with args ('zoek',)\n")
        testobj.parent.parent.use_separate_subject = True
        testobj.gui.get_textentry_value = mock_get_text
        assert testobj.get_search_selargs() == (True, {})
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_textentry_value with args ('zoek',)\n"
                "called SelectOptionsDialogGui.get_textentry_value with args ('zoek2',)\n")
        testobj.gui.get_textentry_value = mock_get_text_2
        assert testobj.get_search_selargs() == (True, {'titel': [('about', 'zoek')]})
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_textentry_value with args ('zoek',)\n"
                "called SelectOptionsDialogGui.get_textentry_value with args ('zoek2',)\n")
        testobj.gui.get_textentry_value = mock_get_text_3
        assert testobj.get_search_selargs() == (True, {'titel': [('title', 'zoek2')]})
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_textentry_value with args ('zoek',)\n"
                "called SelectOptionsDialogGui.get_textentry_value with args ('zoek2',)\n")
        testobj.gui.get_textentry_value = mock_get_text_4
        assert testobj.get_search_selargs() == (False, {})
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_textentry_value with args ('zoek',)\n"
                "called SelectOptionsDialogGui.get_textentry_value with args ('zoek2',)\n"
                "called SelectOptionsDialogGui.get_radiobutton_value with args ('and',)\n"
                "called SelectOptionsDialogGui.get_radiobutton_value with args ('or',)\n")
        testobj.gui.get_radiobutton_value = mock_get_rb_2
        assert testobj.get_search_selargs() == (True, {'titel': [('about', 'zoek'),
                                                                 ('title', 'zoek2'), ('and',)]})
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_textentry_value with args ('zoek',)\n"
                "called SelectOptionsDialogGui.get_textentry_value with args ('zoek2',)\n"
                "called SelectOptionsDialogGui.get_radiobutton_value with args ('and',)\n")
        testobj.gui.get_radiobutton_value = mock_get_rb_3
        assert testobj.get_search_selargs() == (True, {'titel': [('about', 'zoek'),
                                                                 ('title', 'zoek2'), ('or',)]})
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_textentry_value with args ('zoek',)\n"
                "called SelectOptionsDialogGui.get_textentry_value with args ('zoek2',)\n"
                "called SelectOptionsDialogGui.get_radiobutton_value with args ('and',)\n"
                "called SelectOptionsDialogGui.get_radiobutton_value with args ('or',)\n")

    def test_get_arch_selargs(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.get_arch_selargs
        """
        def mock_get_rb(*args):
            print('called SelectOptionsDialogGui.get_radiobutton_value with args', args)
            return False
        def mock_get_rb_2(*args):
            print('called SelectOptionsDialogGui.get_radiobutton_value with args', args)
            return args[0] == 'arch'
        def mock_get_rb_3(*args):
            print('called SelectOptionsDialogGui.get_radiobutton_value with args', args)
            return args[0] == 'all'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.radio_arch = ['arch', 'all']
        testobj.gui = types.SimpleNamespace(get_radiobutton_value=mock_get_rb)
        assert testobj.get_arch_selargs('(gefilterd)') == ('(gefilterd)', '')
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_radiobutton_value with args ('arch',)\n"
                "called SelectOptionsDialogGui.get_radiobutton_value with args ('all',)\n")
        assert testobj.get_arch_selargs('xxxxx') == ('xxxxx', '')
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_radiobutton_value with args ('arch',)\n"
                "called SelectOptionsDialogGui.get_radiobutton_value with args ('all',)\n")
        testobj.gui.get_radiobutton_value = mock_get_rb_2
        assert testobj.get_arch_selargs('(gefilterd)') == ('(gefilterd)', 'arch')
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_radiobutton_value with args ('arch',)\n")
        assert testobj.get_arch_selargs('xxxxx') == ('(gearchiveerd)', 'arch')
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_radiobutton_value with args ('arch',)\n")
        testobj.gui.get_radiobutton_value = mock_get_rb_3
        assert testobj.get_arch_selargs('(gefilterd)') == ('(gefilterd)', 'alles')
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_radiobutton_value with args ('arch',)\n"
                "called SelectOptionsDialogGui.get_radiobutton_value with args ('all',)\n")
        assert testobj.get_arch_selargs('xxxxx') == ('', 'alles')
        assert capsys.readouterr().out == (
                "called SelectOptionsDialogGui.get_radiobutton_value with args ('arch',)\n"
                "called SelectOptionsDialogGui.get_radiobutton_value with args ('all',)\n")


class TestSettOptionsDialog:
    """unittests for main.SettOptionsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.SettOptionsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SettOptionsDialog.__init__ with args', args)
        monkeypatch.setattr(testee.SettOptionsDialog, '__init__', mock_init)
        testobj = testee.SettOptionsDialog()
        assert capsys.readouterr().out == 'called SettOptionsDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.__init__
        """
        class MockSett:
            def initstuff(self, *args):
                print('called SettType.initstuff with args', args)
                return 'titel', 'data', 'actions', 'infotext'
        class MockGui:
            def __init__(self, *args):
                print('called MockSettOptionsDialogGui.__init__ with args', args)
            def add_listbox_with_buttons(self, *args):
                print('called MockSettOptionsDialogGui.add_listbox_with_buttons with args', args)
            def add_label(self, *args):
                print('called MockSettOptionsDialogGui.add_label with args', args)
            def add_okcancel_buttonbox(self):
                print('called MockSettOptionsDialogGui.add_okcancel_buttonbox')
            def finish_display(self):
                print('called MockSettOptionsDialogGui.finish_display')
        monkeypatch.setattr(testee.gui, 'SettOptionsDialogGui', MockGui)
        testobj = testee.SettOptionsDialog('parent', MockSett, 'title')
        testobj.gui = MockGui()
        assert capsys.readouterr().out == (
                "called MockSettOptionsDialogGui.__init__ with args"
                f" ({testobj}, 'parent', 'title')\n"
                "called SettType.initstuff with args ('parent',)\n"
                "called MockSettOptionsDialogGui.add_listbox_with_buttons with args"
                " ('titel', 'data', 'actions')\n"
                "called MockSettOptionsDialogGui.add_label with args ('infotext',)\n"
                "called MockSettOptionsDialogGui.add_okcancel_buttonbox\n"
                "called MockSettOptionsDialogGui.finish_display\n"
                "called MockSettOptionsDialogGui.__init__ with args ()\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.confirm
        """
        class MockSett:
            def leesuit(self, *args):
                print('called SettType.leesuit with args', args)
        class MockGui:
            def read_listbox_data(self, *args):
                print('called MockSettOptionsDialogGui.read_listbox_data with args', args)
                return 'new items'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = 'parent'
        testobj.settingtype = MockSett()
        testobj.gui = MockGui()
        testobj.elb = 'editable listbox'
        testobj.confirm()
        assert capsys.readouterr().out == (
                "called MockSettOptionsDialogGui.read_listbox_data with args ('editable listbox',)\n"
                "called SettType.leesuit with args ('parent', 'new items')\n")


class TestLoginBox:
    """unittests for main.LoginBox
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.LoginBox object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called LoginBox.__init__ with args', args)
        monkeypatch.setattr(testee.LoginBox, '__init__', mock_init)
        testobj = testee.LoginBox()
        assert capsys.readouterr().out == 'called LoginBox.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for LoginBox.__init__
        """
        class MockGui:
            def __init__(self, *args):
                print('called LoginBoxGui.__init__ with args', args)
            def add_textinput_line(self, *args, **kwargs):
                print('called LoginBoxGui.add_textinput_line with args', args)
                return args[0]
            def add_okcancel_buttonbox(self):
                print('called LoginBoxGui.add_okcancel_buttonbox')
            def finish_display(self):
                print('called LoginBoxGui.finish_display')
        monkeypatch.setattr(testee.gui, 'LoginBoxGui', MockGui)
        parent = types.SimpleNamespace()
        testobj = testee.LoginBox(parent)
        assert testobj.parent == parent
        assert testobj.parent.dialog_data == ()
        assert testobj.t_username == 'Userid'
        assert testobj.t_password == 'Password'
        assert capsys.readouterr().out == (
                f"called LoginBoxGui.__init__ with args ({testobj}, {testobj.parent})\n"
                "called LoginBoxGui.add_textinput_line with args ('Userid',)\n"
                "called LoginBoxGui.add_textinput_line with args ('Password',)\n"
                "called LoginBoxGui.add_okcancel_buttonbox\n"
                'called LoginBoxGui.finish_display\n')

    def test_confirm(self, monkeypatch, capsys):
        """unittest for LoginBox.confirm
        """
        def mock_get(arg):
            print('called LoginBoxGui.get_textinput_value with arg', arg)
            return arg
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.t_username = 'username'
        testobj.t_password = 'password'
        testobj.parent = types.SimpleNamespace(filename='xxxxx')
        testobj.gui = types.SimpleNamespace(get_textinput_value=mock_get)
        testobj.confirm()
        assert testobj.parent.dialog_data == ('username', 'password', 'xxxxx')
        assert capsys.readouterr().out == (
                "called LoginBoxGui.get_textinput_value with arg username\n"
                "called LoginBoxGui.get_textinput_value with arg password\n")


def test_db_stat_to_book_stat():
    """unittest for main.db_stat_to_book_stat
    """
    assert testee.db_stat_to_book_stat('x', (1, 2)) == [1, 'x']


def test_db_cat_to_book_cat():
    """unittest for main.db_cat_to_book_cat
    """
    assert testee.db_cat_to_book_cat('x', (1, 2)) == [1, 'x']


def test_db_head_to_book_head():
    """unittest for main.db_head_to_book_head
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
