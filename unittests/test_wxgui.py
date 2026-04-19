"""unittests for ./probreg/wxgui.py
"""
import types
import pytest
from probreg import wxgui as testee
from mockgui import mockwxwidgets as mockwx


def test_show_message(monkeypatch, capsys):
    """unittest for gui_wx.show_message
    """
    monkeypatch.setattr(testee.shared, 'app_title', 'apptitle')
    monkeypatch.setattr(testee.wx, 'MessageBox', mockwx.mock_messagebox)
    testee.show_message('win', 'message')
    assert capsys.readouterr().out == (
            "called wx.MessageBox with args ('message', 'apptitle', 2048) {'parent': 'win'}\n")
    testee.show_message('win', 'message', title='xxxx')
    assert capsys.readouterr().out == (
            "called wx.MessageBox with args ('message', 'xxxx', 2048) {'parent': 'win'}\n")


def test_show_error(monkeypatch, capsys):
    """unittest for gui_wx.show_message
    """
    monkeypatch.setattr(testee.shared, 'app_title', 'apptitle')
    monkeypatch.setattr(testee.wx, 'MessageBox', mockwx.mock_messagebox)
    testee.show_error('win', 'message')
    assert capsys.readouterr().out == (
            "called wx.MessageBox with args ('message', 'apptitle', 512) {'parent': 'win'}\n")
    testee.show_error('win', 'message', title='xxxx')
    assert capsys.readouterr().out == (
            "called wx.MessageBox with args ('message', 'xxxx', 512) {'parent': 'win'}\n")


def test_get_open_filename(monkeypatch, capsys, tmp_path):
    """unittest for gui_wx.get_open_filename
    """
    monkeypatch.setattr(testee.shared, 'app_title', 'apptitle')
    monkeypatch.setattr(testee.wx, 'LoadFileSelector', mockwx.mock_loadfileselector)
    curdir = testee.os.getcwd()
    testee.os.chdir(str(tmp_path))
    assert testee.get_open_filename('win') == "xxxx"
    assert capsys.readouterr().out == (
            "called wx.LoadFileSelector with args"
            " ('apptitle - kies een gegevensbestand',"
            " 'XML files (*.xml)|*.xml|all files (*.*)|*.*')"
            f" {{'default_name': '{tmp_path}', 'parent': 'win'}}\n")
    assert testee.get_open_filename('win', start='here') == "xxxx"
    assert capsys.readouterr().out == (
            "called wx.LoadFileSelector with args"
            " ('apptitle - kies een gegevensbestand',"
            " 'XML files (*.xml)|*.xml|all files (*.*)|*.*')"
            " {'default_name': 'here', 'parent': 'win'}\n")
    testee.os.chdir(curdir)


def test_get_save_filename(monkeypatch, capsys, tmp_path):
    """unittest for gui_wx.get_save_filename
    """
    monkeypatch.setattr(testee.shared, 'app_title', 'apptitle')
    monkeypatch.setattr(testee.wx, 'SaveFileSelector', mockwx.mock_savefileselector)
    curdir = testee.os.getcwd()
    testee.os.chdir(str(tmp_path))
    assert testee.get_save_filename('win') == "xxxx"
    assert capsys.readouterr().out == (
            "called wx.SaveFileSelector with args"
            " ('apptitle - nieuw gegevensbestand',"
            " 'XML files (*.xml)|*.xml|all files (*.*)|*.*')"
            f" {{'default_name': '{tmp_path}', 'parent': 'win'}}\n")
    assert testee.get_save_filename('win', start='here') == "xxxx"
    assert capsys.readouterr().out == (
            "called wx.SaveFileSelector with args"
            " ('apptitle - nieuw gegevensbestand',"
            " 'XML files (*.xml)|*.xml|all files (*.*)|*.*')"
            " {'default_name': 'here', 'parent': 'win'}\n")
    testee.os.chdir(curdir)


def test_get_choice_item(monkeypatch, capsys):
    """unittest for gui_wx.get_choice_item
    """
    def mock_show(self):
        print('called ChoiceDialog.ShowModal')
        return testee.wx.ID_OK
    monkeypatch.setattr(testee.wx, 'SingleChoiceDialog', mockwx.MockChoiceDialog)
    assert testee.get_choice_item('win', 'caption', 'choices') == ''
    assert capsys.readouterr().out == (
            "called ChoiceDialog.__init__ with args ('Actiereg', 'caption', 'choices')\n"
            "called ChoiceDialog.SetSelection with arg '0'\n"
            "called ChoiceDialog.ShowModal\n")
    monkeypatch.setattr(mockwx.MockChoiceDialog, 'ShowModal', mock_show)
    assert testee.get_choice_item('win', 'caption', 'choices', current=1) == 'selected value'
    assert capsys.readouterr().out == (
            "called ChoiceDialog.__init__ with args ('Actiereg', 'caption', 'choices')\n"
            "called ChoiceDialog.SetSelection with arg '1'\n"
            "called ChoiceDialog.ShowModal\n"
            "called ChoiceDialog.GetStringSelection\n")


def test_ask_question(monkeypatch, capsys):
    """unittest for wxgui.ask_question
    """
    def mock_show(self):
        print('called MessageDialog.ShowModal')
        return testee.wx.ID_NO
    def mock_show_2(self):
        print('called MessageDialog.ShowModal')
        return testee.wx.ID_YES
    monkeypatch.setattr(testee.wx, 'MessageDialog', mockwx.MockMessageDialog)
    monkeypatch.setattr(mockwx.MockMessageDialog, 'ShowModal', mock_show)
    assert not testee.ask_question('win', 'message')
    assert capsys.readouterr().out == (
            "called MessageDialog.__init__ with args ('win', 'message', 'Actiereg', 1034) {}\n"
            "called MessageDialog.ShowModal\n")
    monkeypatch.setattr(testee.wx, 'MessageDialog', mockwx.MockMessageDialog)
    monkeypatch.setattr(mockwx.MockMessageDialog, 'ShowModal', mock_show_2)
    assert testee.ask_question('win', 'message')
    assert capsys.readouterr().out == (
            "called MessageDialog.__init__ with args ('win', 'message', 'Actiereg', 1034) {}\n"
            "called MessageDialog.ShowModal\n")


def test_ask_cancel_question(monkeypatch, capsys):
    """unittest for gui_wx.ask_cancel_question
    """
    def mock_show(self):
        print('called MessageDialog.ShowModal')
        return testee.wx.ID_NO
    def mock_show_2(self):
        print('called MessageDialog.ShowModal')
        return testee.wx.ID_YES
    def mock_show_3(self):
        print('called MessageDialog.ShowModal')
        return testee.wx.ID_CANCEL
    monkeypatch.setattr(testee.wx, 'MessageDialog', mockwx.MockMessageDialog)
    monkeypatch.setattr(mockwx.MockMessageDialog, 'ShowModal', mock_show)
    assert testee.ask_cancel_question('win', 'message') == (False, False)
    assert capsys.readouterr().out == (
            "called MessageDialog.__init__ with args ('win', 'message', 'Actiereg', 1050) {}\n"
            "called MessageDialog.ShowModal\n")
    monkeypatch.setattr(testee.wx, 'MessageDialog', mockwx.MockMessageDialog)
    monkeypatch.setattr(mockwx.MockMessageDialog, 'ShowModal', mock_show_2)
    assert testee.ask_cancel_question('win', 'message') == (True, False)
    assert capsys.readouterr().out == (
            "called MessageDialog.__init__ with args ('win', 'message', 'Actiereg', 1050) {}\n"
            "called MessageDialog.ShowModal\n")
    monkeypatch.setattr(testee.wx, 'MessageDialog', mockwx.MockMessageDialog)
    monkeypatch.setattr(mockwx.MockMessageDialog, 'ShowModal', mock_show_3)
    assert testee.ask_cancel_question('win', 'message') == (False, True)
    assert capsys.readouterr().out == (
            "called MessageDialog.__init__ with args ('win', 'message', 'Actiereg', 1050) {}\n"
            "called MessageDialog.ShowModal\n")


# def _test_show_dialog(monkeypatch, capsys):
#     """unittest for gui_wx.show_dialog
#     """
#     assert testee.show_dialog(win, cls, args=None) == "expected_result"
#     assert capsys.readouterr().out == ("")


def test_show_dialog(monkeypatch, capsys):
    """unittest for wxgui.show_dialog_new
    """
    def mock_show():
        print('called Dialog.ShoeModal')
        return testee.wx.ID_CANCEL
    def mock_show_2():
        print('called Dialog.ShoeModal')
        return testee.wx.ID_OK
    def mock_accept():
        "print dlg.accept"
        nonlocal counter
        counter += 1
        if counter > 1:
            return True
        return False
    dlg = mockwx.MockDialog('parent')
    assert capsys.readouterr().out == "called Dialog.__init__ with args () {}\n"
    dlg.ShowModal = mock_show
    dlg.accept = mock_accept
    assert not testee.show_dialog(dlg)
    assert capsys.readouterr().out == "called Dialog.ShoeModal\n"
    dlg.ShowModal = mock_show_2
    counter = 0
    assert testee.show_dialog(dlg)
    assert capsys.readouterr().out == ("called Dialog.ShoeModal\n"
                                       "called Dialog.ShoeModal\n")


def test_setup_accels(monkeypatch, capsys):
    """unittest for gui_wx.setup_accels
    """
    def mock_bind(self, *args):
        print("called Frame.Bind with args", args[:2])
    def mock_fromstring(self, *args):
        print('called AcceleratorEntry.FromString with args', args)
        return False
    monkeypatch.setattr(testee.wx, 'MenuItem', mockwx.MockMenuItem)
    monkeypatch.setattr(testee.wx, 'AcceleratorEntry', mockwx.MockAcceleratorEntry)
    monkeypatch.setattr(testee.wx, 'AcceleratorTable', mockwx.MockAcceleratorTable)
    monkeypatch.setattr(mockwx.MockFrame, 'Bind', mock_bind)
    win = mockwx.MockFrame()
    assert capsys.readouterr().out == "called frame.__init__ with args () {}\n"
    results = testee.setup_accels(win, [])
    assert results == []
    assert capsys.readouterr().out == (
            "called AcceleratorTable.__init__ with 0 AcceleratorEntries\n"
            "called Frame.SetAcceleratorTable\n")
    results = testee.setup_accels(win, [('xx', 'yy', 'zz'), ('aa', 'bb', 'cc')])
    assert len(results) == 2
    for item in results:
        assert isinstance(item, mockwx.MockMenuItem)
    assert capsys.readouterr().out == (
            "called MenuItem.__init__ with args (None, -1, 'xx') {}\n"
            f"called Frame.Bind with args ({testee.wx.EVT_MENU}, 'yy')\n"
            "called menuitem.GetId\n"
            "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
            "called AcceleratorEntry.FromString with args ('zz',)\n"
            "called MenuItem.__init__ with args (None, -1, 'aa') {}\n"
            f"called Frame.Bind with args ({testee.wx.EVT_MENU}, 'bb')\n"
            "called menuitem.GetId\n"
            "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
            "called AcceleratorEntry.FromString with args ('cc',)\n"
            "called AcceleratorTable.__init__ with 2 AcceleratorEntries\n"
            "called Frame.SetAcceleratorTable\n")
    results = testee.setup_accels(win, [('xx', 'yy', 'zz')])
    assert len(results) == 1
    for item in results:
        assert isinstance(item, mockwx.MockMenuItem)
    assert capsys.readouterr().out == (
            "called MenuItem.__init__ with args (None, -1, 'xx') {}\n"
            f"called Frame.Bind with args ({testee.wx.EVT_MENU}, 'yy')\n"
            "called menuitem.GetId\n"
            "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
            "called AcceleratorEntry.FromString with args ('zz',)\n"
            "called AcceleratorTable.__init__ with 1 AcceleratorEntries\n"
            "called Frame.SetAcceleratorTable\n")
    monkeypatch.setattr(mockwx.MockAcceleratorEntry, 'FromString', mock_fromstring)
    results = testee.setup_accels(win, [('xx', 'yy', 'zz')])
    assert len(results) == 1
    for item in results:
        assert isinstance(item, mockwx.MockMenuItem)
    assert capsys.readouterr().out == (
            "called MenuItem.__init__ with args (None, -1, 'xx') {}\n"
            f"called Frame.Bind with args ({testee.wx.EVT_MENU}, 'yy')\n"
            "called menuitem.GetId\n"
            "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
            "called AcceleratorEntry.FromString with args ('zz',)\n"
            "called AcceleratorTable.__init__ with 0 AcceleratorEntries\n"
            "called Frame.SetAcceleratorTable\n")


class TestMainGui:
    """unittest for gui_wx.MainGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.MainGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called MainGui.__init__ with args', args)
        monkeypatch.setattr(testee.MainGui, '__init__', mock_init)
        testobj = testee.MainGui('master')
        testobj.master = types.SimpleNamespace(book=types.SimpleNamespace())
        assert capsys.readouterr().out == "called MainGui.__init__ with args ('master',)\n"
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for MainGui.__init__
        """
        class MockEasyPrinter:
            def __init__(self):
                print('called EasyPrinter.__init__')
        monkeypatch.setattr(testee.wx, 'App', mockwx.MockApp)
        monkeypatch.setattr(testee.wx, 'Icon', mockwx.MockIcon)
        monkeypatch.setattr(testee.wx, 'Panel', mockwx.MockPanel)
        monkeypatch.setattr(testee, 'EasyPrinter', MockEasyPrinter)
        monkeypatch.setattr(testee, 'HERE', '/here/')
        monkeypatch.setattr(testee.wx.Frame, '__init__', mockwx.MockFrame.__init__)
        monkeypatch.setattr(testee.wx.Frame, 'CreateStatusBar', mockwx.MockFrame.CreateStatusBar)
        monkeypatch.setattr(testee.wx.Frame, 'SetIcon', mockwx.MockFrame.SetIcon)
        master = types.SimpleNamespace(title='title')
        monkeypatch.setattr(testee, 'LIN', True)
        testobj = testee.MainGui(master)
        assert isinstance(testobj.app, testee.wx.App)
        assert isinstance(testobj.printer, MockEasyPrinter)
        assert testobj.toolbar is None
        assert capsys.readouterr().out == (
                "called app.__init__ with args ()\n"
                "called EasyPrinter.__init__\n"
                "called frame.__init__ with args () {'parent': None, 'title': 'title',"
                " 'pos': (2, 2), 'size': (1000, 1000), 'style': 541072960}\n"
                "called Frame.CreateStatusBar\n"
                "called StatusBar.__init__ with args ()\n"
                "called statusbar.SetFieldsCount with args (2,)\n"
                "called Icon.__init__ with args ('/here/icons/task.png', 15)\n"
                "called Frame.SetIcon with args (Icon created from '/here/icons/task.png',)\n"
                f"called Panel.__init__ with args ({testobj}, -1) {{}}\n")
        monkeypatch.setattr(testee, 'LIN', False)
        testobj = testee.MainGui(master)
        assert isinstance(testobj.app, testee.wx.App)
        assert isinstance(testobj.printer, MockEasyPrinter)
        assert isinstance(testobj.pnl, testee.wx.Panel)
        assert testobj.toolbar is None
        assert capsys.readouterr().out == (
                "called app.__init__ with args ()\n"
                "called EasyPrinter.__init__\n"
                "called frame.__init__ with args () {'parent': None, 'title': 'title',"
                " 'pos': (20, 32), 'size': (588, 594), 'style': 541072960}\n"
                "called Frame.CreateStatusBar\n"
                "called StatusBar.__init__ with args ()\n"
                "called statusbar.SetFieldsCount with args (2,)\n"
                "called Icon.__init__ with args ('/here/icons/task.png', 15)\n"
                "called Frame.SetIcon with args (Icon created from '/here/icons/task.png',)\n"
                f"called Panel.__init__ with args ({testobj}, -1) {{}}\n")

    def test_create_menu(self, monkeypatch, capsys):
        """unittest for MainGui.create_menu
        """
        def mock_get():
            print("called MainWindow.get_menu_data")
            return []
        def mock_get_2():
            print('called MainWindow.get_menu_data')
            return [('top menu', [('xx', 'callback1', '', ''),
                                  ('yy', 'callback2', 'Ctrl+O', 'yadayada'),
                                  ('',),
                                  ('sub menu', [('zz', 'callback3', 'x', 'bladibla'),
                                                (),
                                                ('&Data', [])])])]
        # deze was bedoeld voor de tabmenus, maar dat gebruik ik hier niet meer
        # def mock_get_3():
        #     print('called MainWindow.get_menu_data')
        #     return [('&View', [('xx', 'callback1', '', ''),
        #                        ('yy', 'callback2', '', '')])]
        def mock_newid():
            return 'new ID'
        monkeypatch.setattr(testee.wx, 'MenuBar', mockwx.MockMenuBar)
        monkeypatch.setattr(testee.wx, 'Menu', mockwx.MockMenu)
        monkeypatch.setattr(testee.wx, 'NewId', mock_newid)
        monkeypatch.setattr(testee.wx.Frame, 'SetMenuBar', mockwx.MockFrame.SetMenuBar)
        monkeypatch.setattr(testee.wx.Frame, 'Bind', mockwx.MockFrame.Bind)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(get_menu_data=mock_get)
        testobj.create_menu()
        assert capsys.readouterr().out == ("called MenuBar.__init__ with args ()\n"
                                           "called MainWindow.get_menu_data\n"
                                           "called Frame.SetMenuBar with args (A MenuBar,)\n")

        testobj.master = types.SimpleNamespace(get_menu_data=mock_get_2)
        testobj.create_menu()
        assert isinstance(testobj.settingsmenu[0], testee.wx.Menu)
        assert testobj.settingsmenu[1] == 'new ID'
        assert capsys.readouterr().out == (
                "called MenuBar.__init__ with args ()\n"
                "called MainWindow.get_menu_data\n"
                "called Menu.__init__ with args ()\n"
                "called menu.Append with args (-1, 'xx', '')\n"
                f"called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback1')\n"
                "called menu.Append with args (-1, 'yy\\tCtrl+O', 'yadayada')\n"
                f"called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback2')\n"
                "called menu.AppendSeparator with args ()\n"
                "called Menu.__init__ with args ()\n"
                "called menu.Append with args (-1, 'zz\\tx', 'bladibla')\n"
                f"called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback3')\n"
                "called Menu.__init__ with args ()\n"
                "called menu.AppendSubMenu with args (A Menu, '&Data')\n"
                "called menu.AppendSubMenu with args (A Menu, 'sub menu')\n"
                "called menubar.Append with args (A Menu, 'top menu')\n"
                "called Frame.SetMenuBar with args (A MenuBar,)\n")
        # testobj.master = types.SimpleNamespace(get_menu_data=mock_get_3)
        # testobj.create_menu()
        # assert capsys.readouterr().out == (
        #         "called MenuBar.__init__ with args ()\n"
        #         "called MainWindow.get_menu_data\n"
        #         "called Menu.__init__ with args ()\n"
        #         "called menubar.Append with args (A Menu, 'separator')\n"
        #         "called Menu.__init__ with args ()\n"
        #         "called menu.Append with args (-1, 'k\\ty', 's')\n"
        #         f"called Frame.Bind with args ({testee.wx.EVT_MENU}, 'e')\n"
        #         "called menubar.Append with args (A Menu, 'menuitem')\n"
        #         "called Menu.__init__ with args ()\n"
        #         "called menu.Append with args (-1, 'cap', 'tip')\n"
        #         f"called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callb')\n"
        #         "called menubar.Append with args (A Menu, 'submenu')\n"
        #         "called Menu.__init__ with args ()\n"
        #         "called menu.Append with args (-1, 'aa\\tcc', 'dd')\n"
        #         f"called Frame.Bind with args ({testee.wx.EVT_MENU}, 'bb')\n"
        #         "called menubar.Append with args (A Menu, '&Data')\n"
        #         "called Frame.SetMenuBar with args (A MenuBar,)\n")

    def test_create_actions(self, monkeypatch, capsys):
        """unittest for MainGui.create_actions
        """
        def mock_setup(*args):
            print('called setup_accels with args', args)
        monkeypatch.setattr(testee, 'setup_accels', mock_setup)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.create_actions([])
        assert capsys.readouterr().out == (
                f"called setup_accels with args ({testobj}, [])\n")
        testobj.create_actions([('xxx', 'callback1'), ('yyy', 'callback2')])
        assert capsys.readouterr().out == (
                "called setup_accels with args"
                f" ({testobj}, [('xxx', 'callback1', 'xxx'), ('yyy', 'callback2', 'yyy')])\n")

    def test_get_bookwidget(self, monkeypatch, capsys):
        """unittest for MainGui.get_bookwidget
        """
        monkeypatch.setattr(testee.wx, 'Notebook', mockwx.MockNoteBook)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockwx.MockPanel()
        assert capsys.readouterr().out == "called Panel.__init__ with args () {}\n"
        assert capsys.readouterr().out == ("")
        assert isinstance(testobj.get_bookwidget(), testee.wx.Notebook)
        assert capsys.readouterr().out == (
                f"called NoteBook.__init__ with args ({testobj.pnl},) {{'size': (580, 570)}}\n"
                f"called NoteBook.Bind with args"
                f" ({testee.wx.EVT_LEFT_UP}, {testobj.on_left_release})\n"
                "called NoteBook.Bind with args"
                f" ({testee.wx.EVT_NOTEBOOK_PAGE_CHANGED}, {testobj.on_page_changed})\n"
                "called NoteBook.Bind with args"
                f" ({testee.wx.EVT_NOTEBOOK_PAGE_CHANGING}, {testobj.on_page_changing})\n")

    def test_go(self, monkeypatch, capsys):
        """unittest for MainGui.go
        """
        monkeypatch.setattr(testee.wx.Frame, 'Bind', mockwx.MockFrame.Bind)
        monkeypatch.setattr(testee.wx.Frame, 'Show', mockwx.MockFrame.Show)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockwx.MockPanel()
        testobj.app = mockwx.MockApp()
        assert capsys.readouterr().out == ("called Panel.__init__ with args () {}\n"
                                           "called app.__init__ with args ()\n")
        testobj.master.exit_app = 'MainWindow.exit_app'
        testobj.go()
        assert isinstance(testobj.exit_button, testee.wx.Button)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (8,)\n"
                "called BoxSizer.__init__ with args (4,)\n"
                "called hori sizer.Add with args SimpleNamespace (1, 8192)\n"
                "called vert sizer.Add with args MockBoxSizer (1, 8192)\n"
                "called BoxSizer.__init__ with args (8,)\n"
                f"called Button.__init__ with args ({testobj.pnl},) {{'id': 5006}}\n"
                f"called Frame.Bind with args ({testee.wx.EVT_BUTTON}, 'MainWindow.exit_app')\n"
                "called vert sizer.Add with args MockButton (0, 256)\n"
                "called vert sizer.Add with args MockBoxSizer (0, 8192)\n"
                "called Panel.SetSizer with args (vert sizer,)\n"
                "called Panel.SetAutoLayout with args (True,)\n"
                f"called vert sizer.Fit with args ({testobj.pnl},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj.pnl},)\n"
                "called Panel.Layout with args ()\n"
                "called frame.Show with args (True,)\n"
                "called app.MainLoop\n")

    def test_refresh_page(self, monkeypatch, capsys):
        """unittest for MainGui.refresh_page
        """
        def mock_changed(*args, **kwargs):
            print('called MainGui.on_page_changed with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.on_page_changed = mock_changed
        testobj.refresh_page()
        assert capsys.readouterr().out == (
                "called MainGui.on_page_changed with args () {'newtabnum': 0}\n")

    def test_on_page_changing(self, monkeypatch, capsys):
        """unittest for MainGui.on_page_changing
        """
        def mock_get_old():
            print('called event.getOldSelection')
            return -1
        def mock_get_old_2():
            print('called event.getOldSelection')
            return 1
        def mock_set(*args):
            print('called Book.SetSelection with args', args)
        def mock_leavep(old):
            print(f'called Page.leavep with arg {old}')
            return False
        def mock_leavep_2(old):
            print(f'called Page.leavep with arg {old}')
            return True
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.book.fnaam = ''
        testobj.master.multiple_files = True
        testobj.master.multiple_projects = False
        testobj.master.book.current_tab = 0
        testobj.master.book.pages = {0: types.SimpleNamespace(leavep=mock_leavep)}
        testobj.master.book.SetSelection = mock_set
        testobj.master.book.data = ''
        testobj.master.book.newitem = ''
        testobj.master.current_item = -1
        event = mockwx.MockEvent()
        event.GetOldSelection = mock_get_old
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        testobj.master.initializing = True
        testobj.on_page_changing(event)
        assert capsys.readouterr().out == ""
        testobj.master.initializing = False
        testobj.on_page_changing(event)
        assert capsys.readouterr().out == ("called event.getOldSelection\n"
                                           "called event.Skip\n")
        event.GetOldSelection = mock_get_old_2
        testobj.on_page_changing(event)
        assert capsys.readouterr().out == ("called event.getOldSelection\n"
                                           "called Page.leavep with arg 1\n"
                                           "called Book.SetSelection with args (0,)\n"
                                           "called event.Veto\n")
        testobj.master.book.pages[0].leavep = mock_leavep_2
        testobj.on_page_changing(event)
        assert capsys.readouterr().out == ("called event.getOldSelection\n"
                                           "called Page.leavep with arg 1\n"
                                           "called event.Skip\n")

    def _test_on_page_changed(self, monkeypatch, capsys):
        """unittest for MainGui.on_page_changed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_page_changed(event=None, newtabnum=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_add_book_tab(self, monkeypatch, capsys):
        """unittest for MainGui.add_book_tab
        """
        def mock_add(*args):
            print('called book.AddPage with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.book.AddPage = mock_add
        tab = types.SimpleNamespace(gui='PageGui')
        testobj.add_book_tab(testobj.master.book, tab, 'title')
        assert capsys.readouterr().out == ("called book.AddPage with args ('PageGui', 'title')\n")

    def _test_enable_tab(self, monkeypatch, capsys):
        "unittest for MainGui.enable_tab"
        # not finished: not implemented

    def test_get_tab_count(self, monkeypatch, capsys):
        """unittest for MainGui.get_tab_count
        """
        def mock_count(*args):
            print('called book.GetRowCount')
            return 'tabcount'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.book.GetRowCount = mock_count
        assert testobj.get_tab_count(testobj.master.book) == "tabcount"
        assert capsys.readouterr().out == ("called book.GetRowCount\n")

    def test_exit(self, monkeypatch, capsys):
        """unittest for MainGui.exit
        """
        monkeypatch.setattr(testee.MainGui, 'Close', mockwx.MockFrame.Close)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.exit()
        assert capsys.readouterr().out == ("called Frame.Close with arg True\n")

    def test_Close(self, monkeypatch, capsys):
        """unittest for MainGui.Close
        """
        def mock_save():
            print('called MainWindow.save_startitem_on_exit')
        monkeypatch.setattr(testee.wx.Frame, 'Close', mockwx.MockFrame.Close)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.save_startitem_on_exit = mock_save
        testobj.Close('args')
        assert capsys.readouterr().out == ("called MainWindow.save_startitem_on_exit\n"
                                           "called Frame.Close with arg args\n")

    def test_set_page(self, monkeypatch, capsys):
        """unittest for MainGui.set_page
        """
        def mock_set(arg):
            print(f'called Book.SetSelection with arg {arg}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.book.pages = ['x', 'y']
        testobj.master.book.SetSelection = mock_set
        testobj.set_page(testobj.master.book, -1)
        assert capsys.readouterr().out == ""
        testobj.set_page(testobj.master.book, 0)
        assert capsys.readouterr().out == "called Book.SetSelection with arg 0\n"
        testobj.set_page(testobj.master.book, 1)
        assert capsys.readouterr().out == "called Book.SetSelection with arg 1\n"
        testobj.set_page(testobj.master.book, 2)
        assert capsys.readouterr().out == "called Book.SetSelection with arg 2\n"
        testobj.set_page(testobj.master.book, 3)
        assert capsys.readouterr().out == ""

    def test_set_page_title(self, monkeypatch, capsys):
        """unittest for MainGui.set_page_title
        """
        def mock_set(*args):
            print('called Book.SetPageText with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.book.SetPageText = mock_set
        testobj.set_page_title(testobj.master.book, 'num', 'text')
        assert capsys.readouterr().out == "called Book.SetPageText with args ('num', 'text')\n"

    def test_get_page(self, monkeypatch, capsys):
        """unittest for MainGui.get_page
        """
        def mock_get():
            print('called Book.GetSelection')
            return 'xxx'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.book.GetSelection = mock_get
        assert testobj.get_page(testobj.master.book) == 'xxx'
        assert capsys.readouterr().out == ("called Book.GetSelection\n")

    def test_set_tabfocus(self, monkeypatch, capsys):
        """unittest for MainGui.set_tabfocus
        """
        def mock_get(arg):
            print(f'called Book.GetSelection with arg {arg}')
            return newtab
        newtab = mockwx.MockControl()
        assert capsys.readouterr().out == "called Control.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.get_focus_widget_for_tab = mock_get
        testobj.set_tabfocus('tabno')
        assert capsys.readouterr().out == ("called Book.GetSelection with arg tabno\n"
                                           "called Control.SetFocus\n")

    # def _test_go_to(self, monkeypatch, capsys):
    #     """unittest for MainGui.go_to
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.go_to(page, event) == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def test_preview(self, monkeypatch, capsys):
        """unittest for MainGui.preview
        """
        class MockTemplate:
            def __init__(self, **kwargs):
                print('called Template.__init__ with args', kwargs)
            def render(self, **kwargs):
                print('called Template.render with args', kwargs)
        def mock_print(*args):
            print('called Printer.print with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.printdict = {}
        testobj.master.hdr = 'xxx'
        testobj.printer = types.SimpleNamespace(print=mock_print)
        monkeypatch.setattr(testee, 'Template', MockTemplate)
        here = testee.os.path.join(testee.os.path.dirname(testee.__file__), 'actie.tpl')
        testobj.preview()
        assert capsys.readouterr().out == (
                f"called Template.__init__ with args {{'filename': '{here}'}}\n"
                "called Template.render with args {'hdr': 'xxx'}\n"
                "called Printer.print with args (None, 'xxx')\n")

    def test_enable_settingsmenu(self, monkeypatch, capsys):
        """unittest for MainGui.enable_settingsmenu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.settingsmenu = (mockwx.MockMenu(), 'id')
        testobj.master.is_admin = 'is_admin'
        testobj.enable_settingsmenu()
        assert capsys.readouterr().out == ("called Menu.__init__ with args ()\n"
                                           "called menu.Enable with args ('id', 'is_admin')\n")

    def test_set_statusmessage(self, monkeypatch, capsys):
        """unittest for MainGui.set_statusmess age
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.wx.Frame, 'GetStatusBar', mockwx.MockFrame.GetStatusBar)
        testobj.set_statusmessage()
        assert capsys.readouterr().out == ("called Frame.GetStatusBar\n"
                                           "called StatusBar.__init__ with args ()\n"
                                           "called statusbar.SetStatusText with args ('',)\n")
        testobj.set_statusmessage('message')
        assert capsys.readouterr().out == ("called Frame.GetStatusBar\n"
                                           "called StatusBar.__init__ with args ()\n"
                                           "called statusbar.SetStatusText with args ('message',)\n")

    def test_set_window_title(self, monkeypatch, capsys):
        """unittest for MainGui.set_window_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.wx.Frame, 'SetTitle', mockwx.MockFrame.SetTitle)
        testobj.set_window_title('text')
        assert capsys.readouterr().out == "called Frame.SetTitle with args ('text',)\n"

    def test_show_username(self, monkeypatch, capsys):
        """unittest for MainGui.show_username
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.wx.Frame, 'GetStatusBar', mockwx.MockFrame.GetStatusBar)
        testobj.show_username('msg')
        assert capsys.readouterr().out == ("called Frame.GetStatusBar\n"
                                           "called StatusBar.__init__ with args ()\n"
                                           "called statusbar.SetStatusText with args ('msg', 1)\n")

    def test_on_left_release(self, monkeypatch, capsys):
        """unittest for MainGui.on_left_release
        """
        def mock_set(*args):
            print('called MainGui.set_tabfocus with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_tabfocus = mock_set
        testobj.master.book.current_tab = 'current tab'
        event = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        testobj.on_left_release()
        assert capsys.readouterr().out == "called MainGui.set_tabfocus with args ('current tab',)\n"
        testobj.on_left_release(event)
        assert capsys.readouterr().out == ("called MainGui.set_tabfocus with args ('current tab',)\n"
                                           "called event.Skip\n")


class TestPageGui:
    """unittest for gui_wx.PageGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.PageadGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called PageGui.__init__ with args', args)
        monkeypatch.setattr(testee.PageGui, '__init__', mock_init)
        testobj = testee.PageGui()
        assert capsys.readouterr().out == 'called PageGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for PageGui.__init__
        """
        monkeypatch.setattr(testee.wx.Panel, '__init__', mockwx.MockPanel.__init__)
        parent = types.SimpleNamespace(parent="appbase")
        testobj = testee.PageGui(parent, 'master')
        assert testobj.parent == parent
        assert testobj.master == 'master'
        assert testobj.appbase == 'appbase'
        assert capsys.readouterr().out == f"called Panel.__init__ with args ({parent},) {{}}\n"

    def test_start_display(self, monkeypatch, capsys):
        """unittest for PageGui.start_display
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx.Panel, 'SetAutoLayout', mockwx.MockPanel.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Panel, 'SetSizer', mockwx.MockPanel.SetSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert isinstance(testobj.start_display(), mockwx.MockBoxSizer)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (8,)\n"
                "called Panel.SetAutoLayout with args (True,)\n"
                "called Panel.SetSizer with args (vert sizer,)\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n")

    def test_create_text_field(self, monkeypatch, capsys):
        """unittest for PageGui.create_text_field
        """
        def mock_init(self, *args, **kwargs):
            print('called Control.__init__ with args', args, kwargs)
        def mock_repr(self):
            return 'Size(x, y)'
        monkeypatch.setattr(testee.wx.Panel, 'Bind', mockwx.MockPanel.Bind)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(mockwx.MockSize, '__repr__', mock_repr)
        monkeypatch.setattr(testee.wx, 'Size', mockwx.MockSize)
        monkeypatch.setattr(testee, 'EditorPanel', mockwx.MockTextCtrl)
        monkeypatch.setattr(mockwx.MockControl, '__init__', mock_init)
        monkeypatch.setattr(testee, 'EditorPanelRt', mockwx.MockControl)
        sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.appbase = types.SimpleNamespace(use_rt=False)
        result = testobj.create_text_field(sizer, 'width', 'height', 'callback')
        assert isinstance(result, testee.EditorPanel)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called Size.__init__ with args ('width', 'height')\n"
                f"called TextCtrl.__init__ with args ({testobj},) {{'size': Size(x, y)}}\n"
                f"called Panel.Bind with args ({testee.wx.EVT_TEXT}, 'callback')\n"
                "called hori sizer.Add with args MockTextCtrl (1, 8432, 10)\n"
                "called  sizer.Add with args MockBoxSizer (1, 8192)\n")
        testobj.appbase.use_rt = True
        result = testobj.create_text_field(sizer, 'width', 'height', 'callback')
        assert isinstance(result, testee.EditorPanelRt)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called Size.__init__ with args ('width', 'height')\n"
                f"called Control.__init__ with args ({testobj},) {{'size': Size(x, y)}}\n"
                f"called Panel.Bind with args ({testee.wx.EVT_TEXT}, 'callback')\n"
                "called hori sizer.Add with args MockControl (1, 8432, 10)\n"
                "called  sizer.Add with args MockBoxSizer (1, 8192)\n")

    def _test_create_toolbar(self, monkeypatch, capsys):
        """unittest for PageGui.create_toolbar
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.create_toolbar(parent=None, textfield=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_create_buttons(self, monkeypatch, capsys):
        """unittest for PageGui.create_buttons
        """
        def mock_keybind(*args):
            print('called PageGui.add_keybind with args', args)
        monkeypatch.setattr(testee.wx.Panel, 'Bind', mockwx.MockPanel.Bind)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        sizer = mockwx.MockBoxSizer(testee.wx.VERTICAL)
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args (8,)\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_keybind = mock_keybind
        with pytest.raises(AttributeError):
            testobj.create_buttons([])
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args (4,)\n"
        testobj.vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        assert testobj.create_buttons([]) == []
        assert capsys.readouterr().out == ("called BoxSizer.__init__ with args (4,)\n"
                                           "called  sizer.Add with args MockBoxSizer (0, 256, 0)\n")

        result = testobj.create_buttons([('xx', 'callback1'), ('yy (a-b)', 'callback2')])
        assert len(result) == 2
        assert isinstance(result[0], testee.wx.Button)
        assert isinstance(result[1], testee.wx.Button)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'xx'}}\n"
                f"called Panel.Bind with args ({testee.wx.EVT_BUTTON}, 'callback1')\n"
                "called hori sizer.Add with args MockButton ()\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'yy (a-b)'}}\n"
                f"called Panel.Bind with args ({testee.wx.EVT_BUTTON}, 'callback2')\n"
                "called PageGui.add_keybind with args ('a+b', 'callback2', 'yy')\n"
                "called hori sizer.Add with args MockButton ()\n"
                "called  sizer.Add with args MockBoxSizer (0, 256, 0)\n")
        result = testobj.create_buttons([('xx', 'callback1'), ('yy (a-b)', 'callback2')], sizer)
        assert len(result) == 2
        assert isinstance(result[0], testee.wx.Button)
        assert isinstance(result[1], testee.wx.Button)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'xx'}}\n"
                f"called Panel.Bind with args ({testee.wx.EVT_BUTTON}, 'callback1')\n"
                "called hori sizer.Add with args MockButton ()\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'yy (a-b)'}}\n"
                f"called Panel.Bind with args ({testee.wx.EVT_BUTTON}, 'callback2')\n"
                "called PageGui.add_keybind with args ('a+b', 'callback2', 'yy')\n"
                "called hori sizer.Add with args MockButton ()\n"
                "called vert sizer.Add with args MockBoxSizer (0, 256, 0)\n")

    def test_add_keybind(self, monkeypatch, capsys):
        """unittest for PageGui.add_keybind
        """
        def mock_accels(*args):
            print('called setup_accels with args', args)
        monkeypatch.setattr(testee, 'setup_accels', mock_accels)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.accel_data = []
        testobj.add_keybind('keydef', 'callback', 'text')
        assert testobj.accel_data == [('text', 'callback', 'keydef')]
        assert capsys.readouterr().out == ""
        testobj.accel_data = []
        testobj.add_keybind('keydef', 'callback', last=True)
        assert testobj.accel_data == [('keydef', 'callback', 'keydef')]
        assert capsys.readouterr().out == (
                f"called setup_accels with args ({testobj}, [('keydef', 'callback', 'keydef')])\n")

    def test_choose_font(self, monkeypatch, capsys):
        """unittest for PageGui.choose_font
        """
        def mock_font(*args):
            print('called textfield.text_font with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.text1 = types.SimpleNamespace(text_font=mock_font)
        testobj.choose_font('event')
        assert capsys.readouterr().out == "called textfield.text_font with args ('event',)\n"

    def _test_reset_font(self, monkeypatch, capsys):
        """unittest for PageGui.reset_font
        """
        # niet geïmlementeerd, geen unittest

    def test_enable_widget(self, monkeypatch, capsys):
        """unittest for PageGui.enable_button
        """
        widget = mockwx.MockControl()
        assert capsys.readouterr().out == "called Control.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.enable_widget(widget, 'state')
        assert capsys.readouterr().out == ("called Control.Enable with arg state\n")

    def test_move_cursor_to_end(self, monkeypatch, capsys):
        """unittest for PageGui.move_cursor_to_end
        """
        def mock_move():
            print('called textfield.MoveEnd')
        def mock_move_2():
            print('called textfield.MoveEnd')
            raise AttributeError
        def mock_set():
            print('called textfield.SetInsertionPointEnd')
        textfield = types.SimpleNamespace(MoveEnd=mock_move, SetInsertionPointEnd=mock_set)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.move_cursor_to_end(textfield)
        assert capsys.readouterr().out == "called textfield.MoveEnd\n"
        textfield.MoveEnd = mock_move_2
        testobj.move_cursor_to_end(textfield)
        assert capsys.readouterr().out == ("called textfield.MoveEnd\n"
                                           "called textfield.SetInsertionPointEnd\n")

    def test_set_textarea_contents(self, monkeypatch, capsys):
        """unittest for PageGui.set_textarea_contents
        """
        def mock_set(*args):
            print('called textfield.set_contents with args', args)
        textfield = types.SimpleNamespace(set_contents=mock_set)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_textarea_contents(textfield, 'data')
        assert capsys.readouterr().out == "called textfield.set_contents with args ('data',)\n"

    def test_get_textarea_contents(self, monkeypatch, capsys):
        """unittest for PageGui.get_textarea_contents
        """
        def mock_get(*args):
            print('called textfield.get_contents with args', args)
        textfield = types.SimpleNamespace(get_contents=mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_textarea_contents(textfield)
        assert capsys.readouterr().out == "called textfield.get_contents with args ()\n"

    def test_enable_toolbar(self, monkeypatch, capsys):
        """unittest for PageGui.enable_toolbar
        """
        def mock_enable(*args):
            print('called toolbar.Enable with args', args)
        toolbar = types.SimpleNamespace(Enable=mock_enable)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.enable_toolbar(toolbar, 'value')
        assert capsys.readouterr().out == "called toolbar.Enable with args ('value',)\n"

    def test_set_text_readonly(self, monkeypatch, capsys):
        """unittest for PageGui.set_text_readonly
        """
        def mock_set(*args):
            print('called textfield.SetEditable with args', args)
        textfield = types.SimpleNamespace(SetEditable=mock_set)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_text_readonly(textfield, 'value')
        assert capsys.readouterr().out == "called textfield.SetEditable with args (False,)\n"

    def test_is_enabled(self, monkeypatch, capsys):
        """unittest for PageGui.is_enabled
        """
        def mock_is(*args):
            print('called widget.IsEnabled with args', args)
            return 'Is'
        widget = types.SimpleNamespace(IsEnabled=mock_is)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.is_enabled(widget) == "Is"
        assert capsys.readouterr().out == "called widget.IsEnabled with args ()\n"

    def test_set_focus_to_field(self, monkeypatch, capsys):
        """unittest for PageGui.set_text_focus_to_field
        """
        def mock_set(*args):
            print('called widget.SetFocus with args', args)
            return 'Is'
        widget = types.SimpleNamespace(SetFocus=mock_set)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus_to_field(widget)
        assert capsys.readouterr().out == "called widget.SetFocus with args ()\n"


class TestEditorPanel:
    """unittest for gui_wx.EditorPanel
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.EditorPanel object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called EditorPanel.__init__ with args', args)
        monkeypatch.setattr(testee.EditorPanel, '__init__', mock_init)
        testobj = testee.EditorPanel()
        assert capsys.readouterr().out == 'called EditorPanel.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for EditorPanel.__init__
        """
        monkeypatch.setattr(testee.wx.TextCtrl, '__init__', mockwx.MockTextCtrl.__init__)
        testobj = testee.EditorPanel('parent')
        assert capsys.readouterr().out == ("called TextCtrl.__init__ with args"
                                           " ('parent',) {'size': (400, 200), 'style': 32865}\n")

    def test_set_contents(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_contents
        """
        monkeypatch.setattr(testee.wx.TextCtrl, 'SetValue', mockwx.MockTextCtrl.SetValue)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_contents('data')
        assert capsys.readouterr().out == "called text.SetValue with args ('data',)\n"

    def test_get_contents(self, monkeypatch, capsys):
        """unittest for EditorPanel.get_contents
        """
        monkeypatch.setattr(testee.wx.TextCtrl, 'GetValue', mockwx.MockTextCtrl.GetValue)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_contents() == "value from textctrl"
        assert capsys.readouterr().out == "called text.GetValue\n"

    def test_check_dirty(self, monkeypatch, capsys):
        """unittest for EditorPanel._check_dirty
        """
        monkeypatch.setattr(testee.wx.TextCtrl, 'IsModified', mockwx.MockTextCtrl.IsModified)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj._check_dirty() == "modified"
        assert capsys.readouterr().out == "called text.IsModified\n"

    def test_mark_dirty(self, monkeypatch, capsys):
        """unittest for EditorPanel._mark_dirty
        """
        monkeypatch.setattr(testee.wx.TextCtrl, 'SetModified', mockwx.MockTextCtrl.SetModified)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._mark_dirty('value')
        assert capsys.readouterr().out == "called text.SetModified with arg False\n"

    def test_openup(self, monkeypatch, capsys):
        """unittest for EditorPanel._openup
        """
        monkeypatch.setattr(testee.wx.TextCtrl, 'Enable', mockwx.MockTextCtrl.Enable)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._openup('value')
        assert capsys.readouterr().out == "called text.Enable with arg value\n"


class TestEditorPanelRt:
    """unittest for gui_wx.EditorPanelRt
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.EditorPanelRt object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called EditorPanelRt.__init__ with args', args)
        monkeypatch.setattr(testee.EditorPanelRt, '__init__', mock_init)
        testobj = testee.EditorPanelRt()
        assert capsys.readouterr().out == 'called EditorPanelRt.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.__init__
        """
        monkeypatch.setattr(testee.wxrt.RichTextCtrl, '__init__', mockwx.MockTextCtrl.__init__)
        testobj = testee.EditorPanelRt('parent')
        assert isinstance(testobj.textAttr, testee.wxrt.RichTextAttr)
        assert capsys.readouterr().out == (
                "called TextCtrl.__init__ with args"
                " ('parent',) {'size': (400, 200), 'style': -1071644672}\n")

    def test_set_contents(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.set_contents
        """
        monkeypatch.setattr(testee.wxrt, 'RichTextXMLHandler', mockwx.MockHandler)
        monkeypatch.setattr(testee.wxrt.RichTextCtrl, 'Clear', mockwx.MockTextCtrl.Clear)
        monkeypatch.setattr(testee.wxrt.RichTextCtrl, 'SetValue', mockwx.MockTextCtrl.SetValue)
        monkeypatch.setattr(testee.wxrt.RichTextCtrl, 'Refresh', mockwx.MockTextCtrl.Refresh)
        monkeypatch.setattr(testee.wxrt.RichTextCtrl, 'GetBuffer', mockwx.MockTextCtrl.GetBuffer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_contents('data')
        assert capsys.readouterr().out == ("called text.Clear\n"
                                           "called text.SetValue with args ('data',)\n"
                                           "called text.Refresh\n")
        handler, buffer, tmpfilename = testobj.set_contents('<?xml>data<data>')
        assert capsys.readouterr().out == (
                "called text.Clear\n"
                "called RichTextXMLHandler.__init__\n"
                "called text.GetBuffer\n"
                "called RichTextBuffer.__init__\n"
                f"called RichTextBuffer.AddHandler with args ({handler},)\n"
                f"called RichTextXMLHandler.LoadFile with args ({buffer}, '{tmpfilename}')\n"
                "called text.Refresh\n")

    def test_get_contents(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.get_contents
        """
        def mock_save(self, *args):
            print('called RichTextXMLHandler.SaveFile with args', args)
            with open(args[1], 'w') as out:
                out.write('value from textctrl')
        monkeypatch.setattr(testee.wxrt, 'RichTextXMLHandler', mockwx.MockHandler)
        monkeypatch.setattr(testee.wxrt.RichTextCtrl, 'GetBuffer', mockwx.MockTextCtrl.GetBuffer)
        monkeypatch.setattr(mockwx.MockHandler, 'SaveFile', mock_save)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_contents() == "value from textctrl"
        handler, buffer, tmpfilename = testobj.teststuff
        assert capsys.readouterr().out == (
                "called RichTextXMLHandler.__init__\n"
                "called text.GetBuffer\n"
                "called RichTextBuffer.__init__\n"
                f"called RichTextBuffer.AddHandler with args ({handler},)\n"
                f"called RichTextXMLHandler.SaveFile with args ({buffer}, '{tmpfilename}')\n")

    def test_text_bold(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.text_bold
        """
        def mock_focus():
            print('called EditorPanel.HasFocus')
            return False
        def mock_focus_2():
            print('called EditorPanel.HasFocus')
            return True
        def mock_apply():
            print('called EditorPanel.ApplyBoldToSelection')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.HasFocus = mock_focus
        testobj.ApplyBoldToSelection = mock_apply
        testobj.text_bold('event')
        assert capsys.readouterr().out == ("called EditorPanel.HasFocus\n")
        testobj.HasFocus = mock_focus_2
        testobj.text_bold('event')
        assert capsys.readouterr().out == ("called EditorPanel.HasFocus\n"
                                           "called EditorPanel.ApplyBoldToSelection\n")

    def test_text_italic(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.text_italic
        """
        def mock_focus():
            print('called EditorPanel.HasFocus')
            return False
        def mock_focus_2():
            print('called EditorPanel.HasFocus')
            return True
        def mock_apply():
            print('called EditorPanel.ApplyItalicToSelection')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.HasFocus = mock_focus
        testobj.ApplyItalicToSelection = mock_apply
        testobj.text_italic('event')
        assert capsys.readouterr().out == ("called EditorPanel.HasFocus\n")
        testobj.HasFocus = mock_focus_2
        testobj.text_italic('event')
        assert capsys.readouterr().out == ("called EditorPanel.HasFocus\n"
                                           "called EditorPanel.ApplyItalicToSelection\n")

    def test_text_underline(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.text_underline
        """
        def mock_focus():
            print('called EditorPanel.HasFocus')
            return False
        def mock_focus_2():
            print('called EditorPanel.HasFocus')
            return True
        def mock_apply():
            print('called EditorPanel.ApplyUnderlineToSelection')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.HasFocus = mock_focus
        testobj.ApplyUnderlineToSelection = mock_apply
        testobj.text_underline('event')
        assert capsys.readouterr().out == ("called EditorPanel.HasFocus\n")
        testobj.HasFocus = mock_focus_2
        testobj.text_underline('event')
        assert capsys.readouterr().out == ("called EditorPanel.HasFocus\n"
                                           "called EditorPanel.ApplyUnderlineToSelection\n")

    def _test_text_strikethrough(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.text_strikethrough
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.text_strikethrough('event') == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_case_lower(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.case_lower
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.case_lower('event') == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_case_upper(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.case_upper
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.case_upper('event') == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_indent_more(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.indent_more
        """
        def mock_change(arg):
            print(f'called EditorPanel.change_indent with arg {arg}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.change_indent = mock_change
        testobj.indent_more('event')
        assert capsys.readouterr().out == "called EditorPanel.change_indent with arg 100\n"

    def test_indent_less(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.indent_less
        """
        def mock_change(arg):
            print(f'called EditorPanel.change_indent with arg {arg}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.change_indent = mock_change
        testobj.indent_less('event')
        assert capsys.readouterr().out == "called EditorPanel.change_indent with arg -100\n"

    def test_change_indent(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.change_indent
        """
        def mock_hasfocus():
            print('called text.HasFocus')
            return False
        def mock_hasfocus_2():
            print('called text.HasFocus')
            return True
        def mock_getstyle(*args):
            print('called text.GetStyle with args', args)
            return False
        def mock_getstyle_2(*args):
            print('called text.GetStyle with args', args)
            return True
        def mock_getpoint(*args):
            print('called text.GetInsertionPoint with args', args)
            return 'Point'
        def mock_has_sel():
            print('called text.HasSelection')
            return False
        def mock_has_sel_2():
            print('called text.HasSelection')
            return True
        def mock_getrange(*args):
            print('called text.GetSelectionRange')
            return 'Range'
        def mock_setstyle(*args):
            print('called text.SetStyle with args', args)
        monkeypatch.setattr(testee.wxrt, 'RichTextAttr', mockwx.MockTextAttr)
        monkeypatch.setattr(testee.wxrt, 'RichTextRange', mockwx.MockTextRange)

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.HasFocus = mock_hasfocus
        testobj.GetStyle = mock_getstyle
        testobj.GetInsertionPoint = mock_getpoint
        testobj.HasSelection = mock_has_sel
        testobj.GetSelectionRange = mock_getrange
        testobj.SetStyle = mock_setstyle
        testobj.change_indent('amount')
        assert capsys.readouterr().out == "called text.HasFocus\n"
        testobj.HasFocus = mock_hasfocus_2
        testobj.change_indent('amount')
        assert capsys.readouterr().out == (
                "called text.HasFocus\n"
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (256,)\n"
                "called text.GetInsertionPoint with args ()\n"
                "called text.GetStyle with args ('Point', richtextattr)\n")
        testobj.GetStyle = mock_getstyle_2
        testobj.change_indent('amount')
        assert capsys.readouterr().out == (
                "called text.HasFocus\n"
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (256,)\n"
                "called text.GetInsertionPoint with args ()\n"
                "called text.GetStyle with args ('Point', richtextattr)\n"
                "called RichTextRange.__init__ with args ('Point', 'Point')\n"
                "called text.HasSelection\n"
                "called RichTextAttr.GetLeftIndent\n"
                "called RichTextAttr.SetLeftIndent with args ('leftindentamount',)\n"
                "called RichTextAttr.SetFlags with args (256,)\n"
                "called text.SetStyle with args (richtextrange, richtextattr)\n")
        testobj.HasSelection = mock_has_sel_2
        testobj.change_indent('amount')
        assert capsys.readouterr().out == (
                "called text.HasFocus\n"
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (256,)\n"
                "called text.GetInsertionPoint with args ()\n"
                "called text.GetStyle with args ('Point', richtextattr)\n"
                "called RichTextRange.__init__ with args ('Point', 'Point')\n"
                "called text.HasSelection\n"
                "called text.GetSelectionRange\n"
                "called RichTextAttr.GetLeftIndent\n"
                "called RichTextAttr.SetLeftIndent with args ('leftindentamount',)\n"
                "called RichTextAttr.SetFlags with args (256,)\n"
                "called text.SetStyle with args ('Range', richtextattr)\n")

    def test_text_font(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.text_font
        """
        def mock_getrange(*args):
            print('called text.GetSelectionRange')
            return 'Range'
        def mock_getpoint(*args):
            print('called text.GetInsertionPoint with args', args)
            return 'Point'
        def mock_getstyle(*args):
            print('called text.GetStyle with args', args)
            return False
        def mock_getstyle_2(*args):
            print('called text.GetStyle with args', args)
            return True
        def mock_setstyle(*args):
            print('called text.SetStyle with args', args)
        def mock_show(self):
            print('called FontDialog.ShowModal')
            return testee.wx.ID_OK
        def mock_getfont(self):
            print('called FontData.GetChosenFont')
            return 'chosenfont'
        def mock_setfocus():
            print('called text.SetFocus')
        monkeypatch.setattr(testee.wx, 'FontData', mockwx.MockFontData)
        monkeypatch.setattr(testee.wx, 'FontDialog', mockwx.MockFontDialog)
        monkeypatch.setattr(testee.wxrt, 'RichTextAttr', mockwx.MockTextAttr)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.GetSelectionRange = mock_getrange
        testobj.GetInsertionPoint = mock_getpoint
        testobj.GetStyle = mock_getstyle
        testobj.SetStyle = mock_setstyle
        testobj.SetFocus = mock_setfocus
        testobj.text_font('event')
        assert capsys.readouterr().out == (
                "called text.GetSelectionRange\n"
                "called FontData.__init__\n"
                "called FontData.EnableEffects with arg False\n"
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (503316604,)\n"
                "called text.GetInsertionPoint with args ()\n"
                "called text.GetStyle with args ('Point', richtextattr)\n"
                "called FontDialog.__init__ with args ()\n"
                "called FontDialog.ShowModal\n"
                "called text.SetFocus\n")
        testobj.GetStyle = mock_getstyle_2
        testobj.text_font('event')
        assert capsys.readouterr().out == (
                "called text.GetSelectionRange\n"
                "called FontData.__init__\n"
                "called FontData.EnableEffects with arg False\n"
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (503316604,)\n"
                "called text.GetInsertionPoint with args ()\n"
                "called text.GetStyle with args ('Point', richtextattr)\n"
                "called RichTextAttr.GetFont\n"
                "called FontData.SetInitialFont with args ('Font',)\n"
                "called FontDialog.__init__ with args ()\n"
                "called FontDialog.ShowModal\n"
                "called text.SetFocus\n")
        monkeypatch.setattr(mockwx.MockFontDialog, 'ShowModal', mock_show)
        testobj.text_font('event')
        assert capsys.readouterr().out == (
                "called text.GetSelectionRange\n"
                "called FontData.__init__\n"
                "called FontData.EnableEffects with arg False\n"
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (503316604,)\n"
                "called text.GetInsertionPoint with args ()\n"
                "called text.GetStyle with args ('Point', richtextattr)\n"
                "called RichTextAttr.GetFont\n"
                "called FontData.SetInitialFont with args ('Font',)\n"
                "called FontDialog.__init__ with args ()\n"
                "called FontDialog.ShowModal\n"
                "called FontDialog.GetFontData\n"
                "called FontData.__init__\n"
                "called FontData.GetChosenFont\n"
                "called text.SetFocus\n")
        monkeypatch.setattr(mockwx.MockFontData, 'GetChosenFont', mock_getfont)
        testobj.text_font('event')
        assert capsys.readouterr().out == (
                "called text.GetSelectionRange\n"
                "called FontData.__init__\n"
                "called FontData.EnableEffects with arg False\n"
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (503316604,)\n"
                "called text.GetInsertionPoint with args ()\n"
                "called text.GetStyle with args ('Point', richtextattr)\n"
                "called RichTextAttr.GetFont\n"
                "called FontData.SetInitialFont with args ('Font',)\n"
                "called FontDialog.__init__ with args ()\n"
                "called FontDialog.ShowModal\n"
                "called FontDialog.GetFontData\n"
                "called FontData.__init__\n"
                "called FontData.GetChosenFont\n"
                "called RichTextAttr.SetFlags with args (503316604,)\n"
                "called RichTextAttr.SetFont with args ('chosenfont',)\n"
                "called text.SetStyle with args ('Range', richtextattr)\n"
                "called text.SetFocus\n")

    # def _test_text_family(self, monkeypatch, capsys):
    #     """unittest for EditorPanelRt.text_family
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.text_family(event, family) == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def _test_enlarge_text(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.enlarge_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enlarge_text('event') == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_shrink_text(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.shrink_textvalue from textctrl
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.shrink_text('event') == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_linespacing_1(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.linespacing_1
        """
        def mock_set(amount):
            print(f'called EditorPanel.set_linespacing with arg {amount}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_linespacing = mock_set
        testobj.linespacing_1('event')
        assert capsys.readouterr().out == "called EditorPanel.set_linespacing with arg 10\n"

    def test_linespacing_15(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.linespacing_15
        """
        def mock_set(amount):
            print(f'called EditorPanel.set_linespacing with arg {amount}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_linespacing = mock_set
        testobj.linespacing_15('event')
        assert capsys.readouterr().out == "called EditorPanel.set_linespacing with arg 15\n"

    def test_linespacing_2(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.linespacing_2
        """
        def mock_set(amount):
            print(f'called EditorPanel.set_linespacing with arg {amount}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_linespacing = mock_set
        testobj.linespacing_2('event')
        assert capsys.readouterr().out == "called EditorPanel.set_linespacing with arg 20\n"

    def test_set_linespacing(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.set_linespacing
        """
        def mock_hasfocus():
            print('called text.HasFocus')
            return False
        def mock_hasfocus_2():
            print('called text.HasFocus')
            return True
        def mock_getstyle(*args):
            print('called text.GetStyle with args', args)
            return False
        def mock_getstyle_2(*args):
            print('called text.GetStyle with args', args)
            return True
        def mock_getpoint(*args):
            print('called text.GetInsertionPoint with args', args)
            return 'Point'
        def mock_has_sel():
            print('called text.HasSelection')
            return False
        def mock_has_sel_2():
            print('called text.HasSelection')
            return True
        def mock_getrange(*args):
            print('called text.GetSelectionRange')
            return 'Range'
        def mock_setstyle(*args):
            print('called text.SetStyle with args', args)
        monkeypatch.setattr(testee.wxrt, 'RichTextAttr', mockwx.MockTextAttr)
        monkeypatch.setattr(testee.wxrt, 'RichTextRange', mockwx.MockTextRange)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.HasFocus = mock_hasfocus
        testobj.GetStyle = mock_getstyle
        testobj.GetInsertionPoint = mock_getpoint
        testobj.HasSelection = mock_has_sel
        testobj.GetSelectionRange = mock_getrange
        testobj.SetStyle = mock_setstyle
        testobj.set_linespacing('amount')
        assert capsys.readouterr().out == "called text.HasFocus\n"
        testobj.HasFocus = mock_hasfocus_2
        testobj.set_linespacing('amount')
        assert capsys.readouterr().out == (
                "called text.HasFocus\n"
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (8192,)\n"
                "called text.GetInsertionPoint with args ()\n"
                "called text.GetStyle with args ('Point', richtextattr)\n")
        testobj.GetStyle = mock_getstyle_2
        testobj.set_linespacing('amount')
        assert capsys.readouterr().out == (
                "called text.HasFocus\n"
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (8192,)\n"
                "called text.GetInsertionPoint with args ()\n"
                "called text.GetStyle with args ('Point', richtextattr)\n"
                "called RichTextRange.__init__ with args ('Point', 'Point')\n"
                "called text.HasSelection\n"
                "called RichTextAttr.SetFlags with args (8192,)\n"
                "called RichTextAttr.SetLineSpacing with args ('amount',)\n"
                "called text.SetStyle with args (richtextrange, richtextattr)\n")
        testobj.HasSelection = mock_has_sel_2
        testobj.set_linespacing('amount')
        assert capsys.readouterr().out == (
                "called text.HasFocus\n"
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (8192,)\n"
                "called text.GetInsertionPoint with args ()\n"
                "called text.GetStyle with args ('Point', richtextattr)\n"
                "called RichTextRange.__init__ with args ('Point', 'Point')\n"
                "called text.HasSelection\n"
                "called text.GetSelectionRange\n"
                "called RichTextAttr.SetFlags with args (8192,)\n"
                "called RichTextAttr.SetLineSpacing with args ('amount',)\n"
                "called text.SetStyle with args ('Range', richtextattr)\n")

    def test_increase_paragraph_spacing(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.increase_paragraph_spacing
        """
        def mock_focus():
            print('called EditorPanel.HasFocus')
            return False
        def mock_focus_2():
            print('called EditorPanel.HasFocus')
            return True
        def mock_set(**kwargs):
            print('called EditorPanel.set_paragraph_spacing with args', kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_paragraph_spacing = mock_set
        testobj.HasFocus = mock_focus
        testobj.increase_paragraph_spacing('event')
        assert capsys.readouterr().out == "called EditorPanel.HasFocus\n"
        testobj.HasFocus = mock_focus_2
        testobj.increase_paragraph_spacing('event')
        assert capsys.readouterr().out == (
                "called EditorPanel.HasFocus\n"
                "called EditorPanel.set_paragraph_spacing with args {'more': True}\n")

    def test_decrease_paragraph_spacing(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.decrease_paragraph_spacing
        """
        def mock_focus():
            print('called EditorPanel.HasFocus')
            return False
        def mock_focus_2():
            print('called EditorPanel.HasFocus')
            return True
        def mock_set(**kwargs):
            print('called EditorPanel.set_paragraph_spacing with args', kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_paragraph_spacing = mock_set
        testobj.HasFocus = mock_focus
        testobj.decrease_paragraph_spacing('event')
        assert capsys.readouterr().out == "called EditorPanel.HasFocus\n"
        testobj.HasFocus = mock_focus_2
        testobj.decrease_paragraph_spacing('event')
        assert capsys.readouterr().out == (
                "called EditorPanel.HasFocus\n"
                "called EditorPanel.set_paragraph_spacing with args {'less': True}\n")

    def test_set_paragraph_spacing(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.set_paragraph_spacing
        """
        def mock_getstyle(*args):
            print('called text.GetStyle with args', args)
            return False
        def mock_getstyle_2(*args):
            print('called text.GetStyle with args', args)
            return True
        def mock_getpoint(*args):
            print('called text.GetInsertionPoint with args', args)
            return 'Point'
        def mock_has_sel():
            print('called text.HasSelection')
            return False
        def mock_has_sel_2():
            print('called text.HasSelection')
            return True
        def mock_getrange(*args):
            print('called text.GetSelectionRange')
            return 'Range'
        def mock_setstyle(*args):
            print('called text.SetStyle with args', args)
        def mock_getspacing(self):
            print('called RichTextAttr.GetParagraphSpacingAfter')
            return 20
        def mock_getspacing_2(self):
            print('called RichTextAttr.GetParagraphSpacingAfter')
            return 19
        monkeypatch.setattr(testee.wxrt, 'RichTextAttr', mockwx.MockTextAttr)
        monkeypatch.setattr(testee.wxrt, 'RichTextRange', mockwx.MockTextRange)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.GetStyle = mock_getstyle
        testobj.GetInsertionPoint = mock_getpoint
        testobj.HasSelection = mock_has_sel
        testobj.GetSelectionRange = mock_getrange
        testobj.SetStyle = mock_setstyle
        testobj.set_paragraph_spacing()
        assert capsys.readouterr().out == "called RichTextAttr.__init__\n"
        testobj.set_paragraph_spacing(more=True)
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.GetParagraphSpacingAfter\n"
                "called RichTextAttr.SetFlags with args (2048,)\n"
                "called text.GetInsertionPoint with args ()\n"
                "called text.GetStyle with args ('Point', richtextattr)\n")
        testobj.GetStyle = mock_getstyle_2
        testobj.set_paragraph_spacing(more=True)
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.GetParagraphSpacingAfter\n"
                "called RichTextAttr.SetFlags with args (2048,)\n"
                "called text.GetInsertionPoint with args ()\n"
                "called text.GetStyle with args ('Point', richtextattr)\n"
                "called RichTextRange.__init__ with args ('Point', 'Point')\n"
                "called text.HasSelection\n"
                "called RichTextAttr.SetParagraphSpacingAfter with args (120,)\n"
                "called RichTextAttr.SetFlags with args (2048,)\n"
                "called text.SetStyle with args (richtextrange, richtextattr)\n")
        testobj.set_paragraph_spacing(less=True)
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.GetParagraphSpacingAfter\n"
                "called RichTextAttr.GetParagraphSpacingAfter\n"
                "called RichTextAttr.SetFlags with args (2048,)\n"
                "called text.GetInsertionPoint with args ()\n"
                "called text.GetStyle with args ('Point', richtextattr)\n"
                "called RichTextRange.__init__ with args ('Point', 'Point')\n"
                "called text.HasSelection\n"
                "called RichTextAttr.SetParagraphSpacingAfter with args (80,)\n"
                "called RichTextAttr.SetFlags with args (2048,)\n"
                "called text.SetStyle with args (richtextrange, richtextattr)\n")
        testobj.HasSelection = mock_has_sel_2
        testobj.set_paragraph_spacing(less=True)
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.GetParagraphSpacingAfter\n"
                "called RichTextAttr.GetParagraphSpacingAfter\n"
                "called RichTextAttr.SetFlags with args (2048,)\n"
                "called text.GetInsertionPoint with args ()\n"
                "called text.GetStyle with args ('Point', richtextattr)\n"
                "called RichTextRange.__init__ with args ('Point', 'Point')\n"
                "called text.HasSelection\n"
                "called text.GetSelectionRange\n"
                "called RichTextAttr.SetParagraphSpacingAfter with args (80,)\n"
                "called RichTextAttr.SetFlags with args (2048,)\n"
                "called text.SetStyle with args ('Range', richtextattr)\n")
        monkeypatch.setattr(testee.wxrt.RichTextAttr, 'GetParagraphSpacingAfter', mock_getspacing)
        testobj.set_paragraph_spacing(less=True)
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.GetParagraphSpacingAfter\n"
                "called RichTextAttr.GetParagraphSpacingAfter\n"
                "called RichTextAttr.SetFlags with args (2048,)\n"
                "called text.GetInsertionPoint with args ()\n"
                "called text.GetStyle with args ('Point', richtextattr)\n"
                "called RichTextRange.__init__ with args ('Point', 'Point')\n"
                "called text.HasSelection\n"
                "called text.GetSelectionRange\n"
                "called RichTextAttr.SetParagraphSpacingAfter with args (0,)\n"
                "called RichTextAttr.SetFlags with args (2048,)\n"
                "called text.SetStyle with args ('Range', richtextattr)\n")
        monkeypatch.setattr(testee.wxrt.RichTextAttr, 'GetParagraphSpacingAfter', mock_getspacing_2)
        testobj.set_paragraph_spacing(less=True)
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.GetParagraphSpacingAfter\n")

    def _test_text_size(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.text_size
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.text_size('size') == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_font_changed(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.font_changed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.font_changed('font') == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_update_bold(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.update_bold
        """
        def mock_is():
            print('called EditorWidget.IsSelectionBold')
            return 'Is'
        evt = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.IsSelectionBold = mock_is
        testobj.update_bold(evt)
        assert capsys.readouterr().out == ("called EditorWidget.IsSelectionBold\n"
                                           "called event.Check with args ('Is',)\n")

    def test_update_italic(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.update_italic
        """
        def mock_is():
            print('called EditorWidget.IsSelectionItalics')
            return 'Is'
        evt = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.IsSelectionItalics = mock_is
        testobj.update_italic(evt)
        assert capsys.readouterr().out == ("called EditorWidget.IsSelectionItalics\n"
                                           "called event.Check with args ('Is',)\n")

    def test_update_underline(self, monkeypatch, capsys):
        """unittest for EditorPanelRt.update_underline
        """
        def mock_is():
            print('called EditorWidget.IsSelectionUnderlined')
            return 'Is'
        evt = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.IsSelectionUnderlined = mock_is
        testobj.update_underline(evt)
        assert capsys.readouterr().out == ("called EditorWidget.IsSelectionUnderlined\n"
                                           "called event.Check with args ('Is',)\n")

    def test_check_dirty(self, monkeypatch, capsys):
        """unittest for EditorPanelRt._check_dirty
        """
        monkeypatch.setattr(testee.wxrt.RichTextCtrl, 'IsModified', mockwx.MockTextCtrl.IsModified)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj._check_dirty() == "modified"
        assert capsys.readouterr().out == "called text.IsModified\n"

    def test_mark_dirty(self, monkeypatch, capsys):
        """unittest for EditorPanelRt._mark_dirty
        """
        monkeypatch.setattr(testee.wxrt.RichTextCtrl, 'SetModified', mockwx.MockTextCtrl.SetModified)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._mark_dirty('value')
        assert capsys.readouterr().out == "called text.SetModified with arg False\n"

    def test_openup(self, monkeypatch, capsys):
        """unittest for EditorPanelRt._openup
        """
        monkeypatch.setattr(testee.wxrt.RichTextCtrl, 'Enable', mockwx.MockTextCtrl.Enable)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._openup('value')
        assert capsys.readouterr().out == "called text.Enable with arg value\n"


class TestPage0Gui:
    """unittest for gui_wx.Page0Gui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.Page0Gui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Page0Gui.__init__ with args', args)
        monkeypatch.setattr(testee.Page0Gui, '__init__', mock_init)
        testobj = testee.Page0Gui()
        testobj.parent = types.SimpleNamespace(data='data')
        testobj.imglist = 'imagelist'
        assert capsys.readouterr().out == 'called Page0Gui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Page0Gui.__init__
        """
        class MockImageList:
            def __init__(self, *args):
                print('called ImageList.__init__ with args', args)
            def Add(self, *args):
                print('called ImageList.Add with args', args)
                return str(args[0])
        class MockImage:
            def __init__(self, *args):
                print('called Image.__init__ with args', args)
                self._name = testee.os.path.basename(args[0])
            def __repr__(self):
                return self._name
        class MockBitmap:
            def __init__(self, *args):
                print('called Bitmap.__init__ with args', *args)
                self._name = str(args[0])
            def __repr__(self):
                return self._name
        def mock_init(self, *args):
            print('called PageGui.__init__ with args', args)
        def mock_mixinit(self, *args):
            print('called ColumnSorterMixin.__init__ with args', args)
        monkeypatch.setattr(testee.PageGui, '__init__', mock_init)
        monkeypatch.setattr(testee.listmix.ColumnSorterMixin, '__init__', mock_mixinit)
        monkeypatch.setattr(testee.wx, 'ImageList', MockImageList)
        monkeypatch.setattr(testee.wx, 'Image', MockImage)
        monkeypatch.setattr(testee.wx, 'Bitmap', MockBitmap)
        testobj = testee.Page0Gui('parent', 'master')
        assert isinstance(testobj.imglist, testee.wx.ImageList)
        assert testobj.up_arrow == 'up.png'
        assert testobj.down_arrow == 'down.png'
        assert capsys.readouterr().out == (
                "called PageGui.__init__ with args ('parent', 'master')\n"
                "called ImageList.__init__ with args (16, 16)\n"
                "called Image.__init__ with args"
                f" ('{testee.os.path.dirname(testee.__file__)}/icons/up.png', 15)\n"
                "called Bitmap.__init__ with args up.png\n"
                "called ImageList.Add with args (up.png,)\n"
                "called Image.__init__ with args"
                f" ('{testee.os.path.dirname(testee.__file__)}/icons/down.png', 15)\n"
                "called Bitmap.__init__ with args down.png\n"
                "called ImageList.Add with args (down.png,)\n")

    def test_add_list(self, monkeypatch, capsys):
        """unittest for Page0Gui.add_list
        """
        def mock_mixinit(self, *args):
            print('called ColumnSorterMixin.__init__ with args', args)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.listmix.ColumnSorterMixin, '__init__', mock_mixinit)
        monkeypatch.setattr(testee.listmix.ColumnSorterMixin, 'SortListItems',
                            mockwx.MockListCtrl.SortListItems)
        monkeypatch.setattr(testee, 'MyListCtrl', mockwx.MockListCtrl)
        monkeypatch.setattr(testee.PageGui, 'Bind', mockwx.MockPanel.Bind)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vsizer = mockwx.MockBoxSizer(testee.wx.VERTICAL)
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args (8,)\n"
        result = testobj.add_list(['xx', 'yy'], [10, 20])
        assert isinstance(result, testee.MyListCtrl)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called ListCtrl.__init__ with args ({testobj},) {{'style': 134225952}}\n"
                "called ListCtrl.SetImageList with args ('imagelist', 1)\n"
                "called ColumnSorterMixin.__init__ with args (2,)\n"
                "called ListCtrl.InsertColumn with args (0, 'xx')\n"
                "called ListCtrl.SetColumnWidth with args (0, 10)\n"
                "called ListCtrl.InsertColumn with args (1, 'yy')\n"
                "called ListCtrl.SetColumnWidth with args (1, 20)\n"
                "called ListCtrl.SortListItems with args (0,)\n"
                "called Panel.Bind with args"
                f" ({testee.wx.EVT_LIST_ITEM_SELECTED}, {testobj.on_change_selected})\n"
                "called Panel.Bind with args"
                f" ({testee.wx.EVT_LIST_ITEM_ACTIVATED}, {testobj.on_activate_item})\n"
                "called ListCtrl.Bind with args"
                f" ({testee.wx.EVT_LEFT_DCLICK}, {testobj.on_doubleclick})\n"
                "called hori sizer.Add with args MockListCtrl (1, 8432, 2)\n"
                "called vert sizer.Add with args MockBoxSizer (1, 8432, 5)\n")

    # def _test_add_buttons(self, monkeypatch, capsys):
    #     """unittest for Page0Gui.add_buttons
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.add_buttons(buttondefs) == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def test_finish_display(self, monkeypatch, capsys):
        """unittest for Page0Gui.finish_display
        """
        def mock_setup(*args):
            print('called setup_accels with args', args)
        monkeypatch.setattr(testee, 'setup_accels', mock_setup)
        monkeypatch.setattr(testee.PageGui, 'SetAutoLayout', mockwx.MockPanel.SetAutoLayout)
        monkeypatch.setattr(testee.PageGui, 'SetSizer', mockwx.MockPanel.SetSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vsizer = mockwx.MockBoxSizer(testee.wx.VERTICAL)
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args (8,)\n"
        testobj.accel_data = 'acceldata'
        testobj.sizer = mockwx.MockBoxSizer()
        testobj.finish_display()
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args ()\n"
                # f"called setup_accels with args ({testobj}, 'acceldata')\n"
                "called Panel.SetAutoLayout with args (True,)\n"
                "called Panel.SetSizer with args (vert sizer,)\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n")

    def _test_enable_sorting(self, monkeypatch, capsys):
        """unittest for Page0Gui.enable_sorting
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_sorting('value') == "expected_result"
        assert capsys.readouterr().out == ("")

    # def _test_enable_button(self, monkeypatch, capsys):
    #     """unittest for Page0Gui.enable_button
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.enable_button(button, state) == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def test_GetListCtrl(self, monkeypatch, capsys):
        """unittest for Page0Gui.GetListCtrl
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        # testobj.master = types.SimpleNamespace(p0list='p0list')
        testobj.p0list = 'p0list'
        assert testobj.GetListCtrl() == 'p0list'
        assert capsys.readouterr().out == ""

    def test_GetSortImages(self, monkeypatch, capsys):
        """unittest for Page0Gui.GetSortImages
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.up_arrow = 'up'
        testobj.down_arrow = 'down'
        assert testobj.GetSortImages() == ('down', 'up')
        assert capsys.readouterr().out == ""

    def test_on_change_selected(self, monkeypatch, capsys):
        """unittest for Page0Gui.on_change_selected
        """
        def mock_change(*args):
            print('called Page0.change_selected with args', args)
        event = types.SimpleNamespace(Index='eventindex')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(change_selected=mock_change)
        testobj.on_change_selected(event)
        assert capsys.readouterr().out == (
                "called Page0.change_selected with args ('eventindex',)\n")

    def test_on_activate_item(self, monkeypatch, capsys):
        """unittest for Page0Gui.on_activate_item
        """
        def mock_activate():
            print('called Page0.activate_item')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(activate_item=mock_activate)
        testobj.on_activate_item('event')
        assert capsys.readouterr().out == "called Page0.activate_item\n"

    def test_on_doubleclick(self, monkeypatch, capsys):
        """unittest for Page0Gui.on_doubleclick(
        """
        def mock_goto():
            print('called Page0.goto_actie')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(goto_actie=mock_goto)
        testobj.on_doubleclick('event')
        assert capsys.readouterr().out == "called Page0.goto_actie\n"

    def test_clear_list(self, monkeypatch, capsys):
        """unittest for Page0Gui.clear_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj.clear_list(p0list)
        assert not p0list.has_selection
        assert capsys.readouterr().out == "called ListCtrl.DeleteAllItems\n"

    def test_add_listitem(self, monkeypatch, capsys):
        """unittest for Page0Gui.add_listitem
        """
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_listitem(p0list, '10-20') == "itemindex"
        assert capsys.readouterr().out == (
                "called ListCtrl.GetItemCount\n"
                "called ListCtrl.InsertItem with args (2, '10-20')\n"
                "called ListCtrl.SetItemData with args ('itemindex', 1020)\n")

    # def _test_set_listitem_values(self, monkeypatch, capsys):
    #     """unittest for Page0Gui.set_listitem_values
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.set_listitem_values(itemindex, data) == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def test_get_items(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_items
        """
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        # assert testobj.get_items(p0list) == ['item 0', 'item 1']
        result = testobj.get_items(p0list)
        # assert result == ['item 0', 'item 1']
        assert len(result) == 2
        assert str(result[0]) == 'item 0'
        assert str(result[1]) == 'item 1'
        assert capsys.readouterr().out == ("called ListCtrl.GetItemCount\n"
                                           "called ListCtrl.GetItem with args (0,)\n"
                                           "called ListCtrl.GetItem with args (1,)\n")

    def test_get_item_text(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_item_text
        """
        p0list = mockwx.MockListCtrl()
        item_or_index = mockwx.MockListItem()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_item_text(p0list, 1, 2) == 1
        assert capsys.readouterr().out == "called ListCtrl.GetItemText with args (1, 2)\n"
        assert testobj.get_item_text(p0list, "1", 2) == '1'
        assert capsys.readouterr().out == ("called ListCtrl.GetItemText with args ('1', 2)\n")
        assert testobj.get_item_text(p0list, item_or_index, 'column') == "id"
        assert capsys.readouterr().out == (
                "called item.GetId\n"
                "called ListCtrl.GetItemText with args ('id', 'column')\n")

    def test_set_item_text(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_item_text
        """
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_item_text(p0list, 'item_or_index', 'column', 'text')
        assert capsys.readouterr().out == (
                "called ListCtrl.SetItem with args ('item_or_index', 'column', 'text')\n")

    def test_get_first_item(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_first_item
        """
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_first_item(p0list) == 0
        assert capsys.readouterr().out == ""

    # def _test_get_item_by_index(self, monkeypatch, capsys):
    #     """unittest for Page0Gui.get_item_by_index
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.get_item_by_index(item_n) == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def test_get_item_by_id(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_item_by_id
        """
        def mock_get(*args):
            print('called ListCtrl.GetItemText with args', args)
            return args[0]
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_item_by_id(p0list, 0) == 0
        assert capsys.readouterr().out == ("called ListCtrl.GetItemCount\n"
                                           "called ListCtrl.GetItemText with args (0, 0)\n")
        assert testobj.get_item_by_id(p0list, 1) == 1
        assert capsys.readouterr().out == ("called ListCtrl.GetItemCount\n"
                                           "called ListCtrl.GetItemText with args (0, 0)\n"
                                           "called ListCtrl.GetItemText with args (1, 0)\n")
        assert testobj.get_item_by_id(p0list, 2) is None
        assert capsys.readouterr().out == ("called ListCtrl.GetItemCount\n"
                                           "called ListCtrl.GetItemText with args (0, 0)\n"
                                           "called ListCtrl.GetItemText with args (1, 0)\n")

    # def _test_has_selection(self, monkeypatch, capsys):
    #     """unittest for Page0Gui.has_selection
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.has_selection() == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def test_set_selection(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_selection
        """
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(current_item='')
        testobj.set_selection(p0list)
        assert capsys.readouterr().out == ""
        testobj.parent.current_item = 'xxx'
        testobj.set_selection(p0list)
        assert capsys.readouterr().out == "called ListCtrl.Select with args ('xxx',)\n"

    def test_get_selection(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_selection
        """
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_selection(p0list) == -1
        assert capsys.readouterr().out == "called ListCtrl.GetFirstSelected\n"

    def test_ensure_visible(self, monkeypatch, capsys):
        """unittest for Page0Gui.ensure_visible
        """
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ensure_visible(p0list, '')
        assert capsys.readouterr().out == ""
        testobj.ensure_visible(p0list, 'xxx')
        assert capsys.readouterr().out == "called ListCtrl.EnsureVisible with args ('xxx',)\n"

    def test_set_button_text(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_archive_button_text
        """
        button = mockwx.MockButton()
        assert capsys.readouterr().out == "called Button.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_button_text(button, 'text')
        assert capsys.readouterr().out == "called Button.SetLabel with arg 'text'\n"

    def test_get_selected_action(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_selected_action
        """
        def mock_get(self, *args):
            print('called ListCtrl.GetItemData with args', args)
            return 12345678
        monkeypatch.setattr(mockwx.MockListCtrl, 'GetItemData', mock_get)
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_selected_action(p0list) == "1234-5678"
        assert capsys.readouterr().out == ("called ListCtrl.GetFirstSelected\n"
                                           "called ListCtrl.GetItemData with args (-1,)\n")

    def test_get_list_row(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_list_row
        """
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_list_row(p0list) == -1
        assert capsys.readouterr().out == "called ListCtrl.GetFirstSelected\n"

    def test_set_list_row(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_list_row
        """
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_list_row(p0list, 'num')
        assert capsys.readouterr().out == ("called ListCtrl.Select with args ('num',)\n")


class TestMyListCtrl:
    """unittest for gui_wx.MyListCtrl
    """
    # def setup_testobj(self, monkeypatch, capsys):
    #     """stub for gui_wx.MyListCtrl object

    #     create the object skipping the normal initialization
    #     intercept messages during creation
    #     return the object so that other methods can be monkeypatched in the caller
    #     """
    #     def mock_init(self, *args):
    #         """stub
    #         """
    #         print('called MyListCtrl.__init__ with args', args)
    #     testobj = testee.MyListCtrl()
    #     assert capsys.readouterr().out == 'called MyListCtrl.__init__ with args ()\n'
    #     return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for MyListCtrl.__init__
        """
        monkeypatch.setattr(testee.wx, 'ListCtrl', mockwx.MockListCtrl)
        monkeypatch.setattr(testee.listmix, 'ListCtrlAutoWidthMixin',
                            mockwx.MockListCtrlAutoWidthMixin)
        testobj = testee.MyListCtrl('parent')
        assert not testobj.has_selection
        assert capsys.readouterr().out == (
                "called ListCtrl.__init__ with args"
                " ('parent',) {'pos': wx.Point(-1, -1), 'size': wx.Size(-1, -1), 'style': 0}\n"
                "called ListCtrlAutoWidthMixin.__init__ with args () {}\n")
        testobj = testee.MyListCtrl('parent', pos='pos', size='size', style='style')
        assert not testobj.has_selection
        assert capsys.readouterr().out == (
                "called ListCtrl.__init__ with args"
                " ('parent',) {'pos': 'pos', 'size': 'size', 'style': 'style'}\n"
                "called ListCtrlAutoWidthMixin.__init__ with args () {}\n")


class TestPage1Gui:
    """unittest for gui_wx.Page1Gui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.Page1Gui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Page1Gui.__init__ with args', args)
        monkeypatch.setattr(testee.Page1Gui, '__init__', mock_init)
        testobj = testee.Page1Gui()
        assert capsys.readouterr().out == 'called Page1Gui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Page1Gui.__init__
        """
        def mock_init(self, *args):
            print('called PageGui.__init__ with args', args)
        monkeypatch.setattr(testee.PageGui, '__init__', mock_init)
        monkeypatch.setattr(testee.PageGui, 'SetAutoLayout', mockwx.MockPanel.SetAutoLayout)
        monkeypatch.setattr(testee.PageGui, 'SetSizer', mockwx.MockPanel.SetSizer)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'GridBagSizer', mockwx.MockGridSizer)
        testobj = testee.Page1Gui('parent', 'master')
        assert testobj.master == 'master'
        assert testobj.row == 0
        assert isinstance(testobj.vsizer, testee.wx.BoxSizer)
        assert isinstance(testobj.gsizer, testee.wx.GridBagSizer)
        assert capsys.readouterr().out == (
                "called PageGui.__init__ with args ('parent', 'master')\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called GridSizer.__init__ with args (3, 12) {}\n"
                "called vert sizer.Add with args MockGridSizer ()\n"
                "called Panel.SetAutoLayout with args (True,)\n"
                "called Panel.SetSizer with args (vert sizer,)\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n")

    def test_add_textentry_line(self, monkeypatch, capsys):
        """unittest for Page1Gui.add_textentry_line
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.row = 0
        monkeypatch.setattr(testobj, 'Bind', mockwx.MockPanel.Bind)
        testobj.gsizer = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        result = testobj.add_textentry_line('labeltext', 'width')
        assert isinstance(result, testee.wx.TextCtrl)
        assert testobj.row == 1
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'labeltext'}}\n"
                "called GridSizer.Add with args"
                " MockStaticText ((1, 0),) {'flag': 240, 'border': 10}\n"
                f"called TextCtrl.__init__ with args ({testobj},) {{'size': ('width', -1)}}\n"
                "called GridSizer.Add with args MockTextCtrl ((1, 1),) {'flag': 2048}\n")
        testobj.row = 0
        result = testobj.add_textentry_line('labeltext', 'width', 'callback')
        assert isinstance(result, testee.wx.TextCtrl)
        assert testobj.row == 1
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'labeltext'}}\n"
                "called GridSizer.Add with args"
                " MockStaticText ((1, 0),) {'flag': 240, 'border': 10}\n"
                f"called TextCtrl.__init__ with args ({testobj},) {{'size': ('width', -1)}}\n"
                "called GridSizer.Add with args MockTextCtrl ((1, 1),) {'flag': 2048}\n"
                f"called Panel.Bind with args ('callback', {result})\n")

    def test_add_combobox_line(self, monkeypatch, capsys):
        """unittest for Page1Gui.add_combobox_line
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(testee.wx, 'ComboBox', mockwx.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.row = 0
        monkeypatch.setattr(testobj, 'Bind', mockwx.MockPanel.Bind)
        testobj.gsizer = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        result = testobj.add_combobox_line('labeltext', 'width', '')
        assert isinstance(result, testee.wx.ComboBox)
        assert testobj.row == 1
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'labeltext'}}\n"
                "called GridSizer.Add with args"
                " MockStaticText ((1, 0),) {'flag': 240, 'border': 10}\n"
                "called ComboBox.__init__ with args"
                f" ({testobj},) {{'size': ('width', -1), 'style': 48}}\n"
                "called GridSizer.Add with args MockComboBox ((1, 1),) {'flag': 2048}\n")
        testobj.row = 0
        result = testobj.add_combobox_line('labeltext', 'width', 'callback')
        assert isinstance(result, testee.wx.ComboBox)
        assert testobj.row == 1
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'labeltext'}}\n"
                "called GridSizer.Add with args"
                " MockStaticText ((1, 0),) {'flag': 240, 'border': 10}\n"
                "called ComboBox.__init__ with args"
                f" ({testobj},) {{'size': ('width', -1), 'style': 48}}\n"
                f"called Panel.Bind with args ('callback', {result})\n"
                "called GridSizer.Add with args MockComboBox ((1, 1),) {'flag': 2048}\n")

    def test_add_pushbutton_line(self, monkeypatch, capsys):
        """unittest for Page1Gui.add_pushbutton_line
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.row = 0
        monkeypatch.setattr(testobj, 'Bind', mockwx.MockPanel.Bind)
        testobj.gsizer = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        result = testobj.add_pushbutton_line('labeltext', 'buttontext', 'callback')
        assert isinstance(result[0], testee.wx.StaticText)
        assert isinstance(result[1], testee.wx.Button)
        assert testobj.row == 2
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': ''}}\n"
                "called GridSizer.Add with args MockStaticText"
                " ((1, 1),) {'flag': 2240, 'border': 10}\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'buttontext'}}\n"
                f"called Panel.Bind with args ('callback', {result[1]})\n"
                "called GridSizer.Add with args MockButton ((2, 1),) {'flag': 2112, 'border': 5}\n")

    def test_add_textbox_line(self, monkeypatch, capsys):
        """unittest for Page1Gui.add_textbox_line
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.row = 0
        monkeypatch.setattr(testobj, 'Bind', mockwx.MockPanel.Bind)
        testobj.gsizer = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        result = testobj.add_textbox_line('labeltext', 'callback')
        assert isinstance(result, testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
               f"called StaticText.__init__ with args ({testobj},) {{'label': 'labeltext'}}\n"
               "called GridSizer.Add with args"
               " MockStaticText ((1, 0),) {'flag': 192, 'border': 10}\n"
               "called BoxSizer.__init__ with args (4,)\n"
               "called TextCtrl.__init__ with args"
               f" ({testobj},) {{'size': (800, 200), 'style': 32865}}\n"
               f"called Panel.Bind with args ('callback', {result})\n"
               "called hori sizer.Add with args MockTextCtrl ()\n"
               "called GridSizer.Add with args"
               " MockBoxSizer ((1, 1),) {'span': (1, 2), 'flag': 192, 'border': 10}\n")

    def test_show_button(self, monkeypatch, capsys):
        """unittest for Page1Gui.show_button
        """
        button = mockwx.MockButton()
        assert capsys.readouterr().out == "called Button.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.show_button(button, True)
        assert capsys.readouterr().out == ("called Button.Show\n")
        testobj.show_button(button, False)
        assert capsys.readouterr().out == ("called Button.Hide\n")

    def test_set_textfield_value(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_textfield_value
        """
        field = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_textfield_value(field, 'value')
        assert capsys.readouterr().out == "called text.SetValue with args ('value',)\n"

    def test_set_label_value(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_label_value
        """
        field = mockwx.MockStaticText()
        assert capsys.readouterr().out == "called StaticText.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_label_value(field, 'value')
        assert capsys.readouterr().out == "called StaticText.SetLabel with args ('value',) {}\n"

    def test_set_textbox_value(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_textbox_value
        """
        field = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_textbox_value(field, 'value')
        assert capsys.readouterr().out == "called text.SetValue with args ('value',)\n"

    def test_get_textfield_value(self, monkeypatch, capsys):
        """unittest for Page1Gui.get_textfield_value
        """
        field = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textfield_value(field) == "value from textctrl"
        assert capsys.readouterr().out == "called text.GetValue\n"

    # def test_get_label_value(self, monkeypatch, capsys):
    #     """unittest for Page1Gui.get_label_value
    #     """
    #     field = mockwx.MockStaticText()
    #     assert capsys.readouterr().out == "called StaticText.__init__ with args () {}\n"
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.get_label_value(field) == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def test_get_textbox_value(self, monkeypatch, capsys):
        """unittest for Page1Gui.get_textbox_value
        """
        field = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textbox_value(field) == "value from textctrl"
        assert capsys.readouterr().out == "called text.GetValue\n"

    def test_set_choice(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_choice
        """
        def mock_get(self, *args):
            print('called combobox.GetClientData with args', args)
            return ('x', 'y', 'z')[args[0]]
        monkeypatch.setattr(mockwx.MockComboBox, 'GetClientData', mock_get)
        field = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_choice(field, ['x', 'y'], 'value')
        assert capsys.readouterr().out == ("called combobox.GetClientData with args (0,)\n"
                                           "called combobox.GetClientData with args (1,)\n")
        testobj.set_choice(field, ['x', 'y'], 'y')
        assert capsys.readouterr().out == ("called combobox.GetClientData with args (0,)\n"
                                           "called combobox.GetClientData with args (1,)\n"
                                           "called combobox.SetSelection with args (1,)\n")

    def test_get_choice_index(self, monkeypatch, capsys):
        """unittest for Page1Gui.get_choice_index
        """
        field = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_choice_index(field) == "selection"
        assert capsys.readouterr().out == "called combobox.GetSelection\n"

    def test_get_choice_data(self, monkeypatch, capsys):
        """unittest for Page1Gui.get_choice_data
        """
        field = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_choice_data(field) == ('selection', 'current text')
        assert capsys.readouterr().out == ("called combobox.GetSelection\n"
                                           "called combobox.GetClientData with args ('selection',)\n"
                                           "called combobox.GetStringSelection\n")

    def test_set_button_text(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_archive_button_text
        """
        button = mockwx.MockButton()
        assert capsys.readouterr().out == "called Button.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_button_text(button, 'value')
        assert capsys.readouterr().out == "called Button.SetLabel with arg 'value'\n"

    # def _test_enable_widget(self, monkeypatch, capsys):
    #     """unittest for Page1Gui.enable_widget
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.enable_widget(widget, state) == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def test_clear_combobox(self, monkeypatch, capsys):
        """unittest for Page1Gui.clear_combobox
        """
        combobox = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.clear_combobox(combobox)
        assert capsys.readouterr().out == "called combobox.clear\n"

    # def _test_clear_stats(self, monkeypatch, capsys):
    #     """unittest for Page1Gui.clear_stats
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.clear_stats() == "expected_result"
    #     assert capsys.readouterr().out == ("")

    # def _test_clear_cats(self, monkeypatch, capsys):
    #     """unittest for Page1Gui.clear_cats
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.clear_cats() == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def test_add_combobox_choice(self, monkeypatch, capsys):
        """unittest for Page1Gui.add_combobox_choice
        """
        combobox = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_combobox_choice(combobox, 'text', 'value')
        assert capsys.readouterr().out == "called combobox.Append with args ('text', 'value')\n"

    # def _test_add_cat_choice(self, monkeypatch, capsys):
    #     """unittest for Page1Gui.add_cat_choice
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.add_cat_choice(text, value) == "expected_result"
    #     assert capsys.readouterr().out == ("")

    # def _test_add_stat_choice(self, monkeypatch, capsys):
    #     """unittest for Page1Gui.add_stat_choice
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.add_stat_choice(text, value) == "expected_result"
    #     assert capsys.readouterr().out == ("")

    # def _test_set_focus(self, monkeypatch, capsys):
    #     """unittest for Page1Gui.set_focus
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.set_focus() == "expected_result"
    #     assert capsys.readouterr().out == ("")


class TestPage6Gui:
    """unittest for gui_wx.Page6Gui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.Page6Gui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Page6Gui.__init__ with args', args)
        monkeypatch.setattr(testee.Page6Gui, '__init__', mock_init)
        testobj = testee.Page6Gui()
        assert capsys.readouterr().out == 'called Page6Gui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Page6Gui.__init__
        """
        def mock_init(self, *args):
            print('called PageGui.__init__ with args', args)
        monkeypatch.setattr(testee.PageGui, '__init__', mock_init)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'SplitterWindow', mockwx.MockSplitter)
        testobj = testee.Page6Gui('parent', 'master')
        assert testobj.master == 'master'
        assert isinstance(testobj.vsizer, testee.wx.BoxSizer)
        assert isinstance(testobj.pnl, testee.wx.SplitterWindow)
        assert testobj.accel_data == []
        assert capsys.readouterr().out == (
                "called PageGui.__init__ with args ('parent', 'master')\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called Splitter.__init__ with args"
                f" ({testobj},) {{'size': (500, 400), 'style': 128}}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called vert sizer.Add with args MockSplitter (1, 8432, 4)\n"
                "called vert sizer.Add with args MockBoxSizer (1, 8432, 8)\n")

    def test_create_list(self, monkeypatch, capsys):
        """unittest for Page6Gui.create_listGetClientData
        """
        assert capsys.readouterr().out == ("")
        monkeypatch.setattr(testee, 'MyListCtrl', mockwx.MockListCtrl)
        monkeypatch.setattr(testee.PageGui, 'Bind', mockwx.MockPanel.Bind)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.appbase = types.SimpleNamespace(work_with_user=True)
        testobj.master = types.SimpleNamespace(goto_prev='goto_prev', goto_next='goto_next')
        testobj.pnl = mockwx.MockSplitter()
        testobj.accel_data = []
        assert isinstance(testobj.create_list(), testee.MyListCtrl)
        assert testobj.accel_data == [('goto-prev', 'goto_prev', 'Shift+Ctrl+Up'),
                                      ('goto-next', 'goto_next', 'Shift+Ctrl+Down')]
        assert capsys.readouterr().out == (
                "called Splitter.__init__ with args () {}\n"
                "called ListCtrl.__init__ with args"
                f" ({testobj.pnl},) {{'size': (250, -1), 'style': 8225}}\n"
                "called Panel.Bind with args"
                f" ({testee.wx.EVT_LIST_ITEM_SELECTED}, {testobj.on_select_item})\n"
                "called Panel.Bind with args"
                f" ({testee.wx.EVT_LIST_ITEM_DESELECTED}, {testobj.on_deselect_item})\n"
                "called ListCtrl.InsertColumn with args (0, 'Momenten')\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.appbase = types.SimpleNamespace(work_with_user=False)
        testobj.master = types.SimpleNamespace(goto_prev='goto_prev', goto_next='goto_next')
        testobj.pnl = mockwx.MockSplitter()
        testobj.accel_data = []
        assert isinstance(testobj.create_list(), testee.MyListCtrl)
        assert testobj.accel_data == [('new-item', testobj.on_activate_item, 'Shift-Ctrl-N'),
                                      ('goto-prev', 'goto_prev', 'Shift+Ctrl+Up'),
                                      ('goto-next', 'goto_next', 'Shift+Ctrl+Down')]
        assert capsys.readouterr().out == (
                "called Splitter.__init__ with args () {}\n"
                "called ListCtrl.__init__ with args"
                f" ({testobj.pnl},) {{'size': (250, -1), 'style': 8225}}\n"
                "called Panel.Bind with args"
                f" ({testee.wx.EVT_LIST_ITEM_ACTIVATED}, {testobj.on_activate_item})\n"
                "called Panel.Bind with args"
                f" ({testee.wx.EVT_LIST_ITEM_SELECTED}, {testobj.on_select_item})\n"
                "called Panel.Bind with args"
                f" ({testee.wx.EVT_LIST_ITEM_DESELECTED}, {testobj.on_deselect_item})\n"
                "called ListCtrl.InsertColumn with args (0, 'Momenten')\n")

    def test_create_textfield(self, monkeypatch, capsys):
        """unittest for Page6Gui.create_textfield
        """
        def mock_create(self, *args, **kwargs):
            print('called PageGui.create_text_field with args', args, kwargs)
            return 'ptext'
        def mock_get(*args):
            print('called MainWindow.get_toolbar_data with args', args)
            return 'toolbardata'
        def mock_create_tb(self, *args, **kwargs):
            print('called PageGui.create_toolbar with args', args, kwargs)
            return 'tbar'
        monkeypatch.setattr(testee.PageGui, 'create_text_field', mock_create)
        monkeypatch.setattr(testee.PageGui, 'create_toolbar', mock_create_tb)
        monkeypatch.setattr(testee.wx, 'Panel', mockwx.MockPanel)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(get_toolbar_data=mock_get)
        testobj.pnl = mockwx.MockSplitter()
        assert capsys.readouterr().out == "called Splitter.__init__ with args () {}\n"
        testobj.appbase = types.SimpleNamespace(use_rt=False)
        assert testobj.create_textfield('width', 'height', 'callback') == "ptext"
        assert isinstance(testobj.textpanel, testee.wx.Panel)
        assert capsys.readouterr().out == (
                f"called Panel.__init__ with args ({testobj.pnl},) {{}}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called PageGui.create_text_field with args"
                f" (vert sizer, 'width', 'height', 'callback') {{'parent': {testobj.textpanel}}}\n"
                "called Panel.SetAutoLayout with args (True,)\n"
                "called Panel.SetSizer with args (vert sizer,)\n"
                f"called vert sizer.Fit with args ({testobj.textpanel},)\n")
        testobj.appbase = types.SimpleNamespace(use_rt=True)
        assert testobj.create_textfield('width', 'height', 'callback') == "ptext"
        assert capsys.readouterr().out == (
                f"called Panel.__init__ with args ({testobj.pnl},) {{}}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called PageGui.create_text_field with args"
                f" (vert sizer, 'width', 'height', 'callback') {{'parent': {testobj.textpanel}}}\n"
                "called MainWindow.get_toolbar_data with args ('ptext',)\n"
                "called PageGui.create_toolbar with args"
                f" (vert sizer, 'ptext', 'toolbardata') {{'parent': {testobj.textpanel}}}\n"
                "called Panel.SetAutoLayout with args (True,)\n"
                "called Panel.SetSizer with args (vert sizer,)\n"
                f"called vert sizer.Fit with args ({testobj.textpanel},)\n")

    # def _test_add_buttons(self, monkeypatch, capsys):
    #     """unittest for Page6Gui.add_buttons
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.add_buttons() == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def test_finish_display(self, monkeypatch, capsys):
        """unittest for Page6Gui.finish_display
        """
        def mock_setup(*args):
            print('called setup_accels with args', args)
        monkeypatch.setattr(testee, 'setup_accels', mock_setup)
        monkeypatch.setattr(testee.PageGui, 'SetAutoLayout', mockwx.MockPanel.SetAutoLayout)
        monkeypatch.setattr(testee.PageGui, 'SetSizer', mockwx.MockPanel.SetSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(progress_list='plist')
        testobj.accel_data = ['accel', 'data']
        testobj.pnl = mockwx.MockSplitter()
        testobj.textpanel = 'textpanel'
        testobj.vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == ("called Splitter.__init__ with args () {}\n"
                                           "called BoxSizer.__init__ with args ()\n")
        testobj.finish_display()
        assert capsys.readouterr().out == (
                f"called setup_accels with args ({testobj}, ['accel', 'data'])\n"
                "called splitter.SplitHorizontally with args ('plist', 'textpanel')\n"
                "called splitter.SetSashPosition with args (250,)\n"
                "called Panel.SetAutoLayout with args (True,)\n"
                "called Panel.SetSizer with args ( sizer,)\n"
                f"called  sizer.Fit with args ({testobj},)\n"
                f"called  sizer.SetSizeHints with args ({testobj},)\n")

    def test_on_activate_item(self, monkeypatch, capsys):
        """unittest for Page6Gui.on_activate_item
        """
        def mock_init():
            print('called Page6.initialize_new_event')
        event = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(initialize_new_event=mock_init)
        event.Index = 1
        testobj.on_activate_item(event)
        assert capsys.readouterr().out == ""
        event.Index = 0
        testobj.on_activate_item(event)
        assert capsys.readouterr().out == "called Page6.initialize_new_event\n"

    def test_on_deselect_item(self, monkeypatch, capsys):
        """unittest for Page6Gui.on_deselect_item
        """
        # def mock_index():
        #     print('called event.Index')
        #     return 0
        # def mock_index_2():
        #     print('called event.Index')
        #     return 1
        def mock_get(*args):
            print('called Page6Gui.get_textfield_contents with args', args)
            return mock_text
        evt = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        evt.Index = 0  # mock_index
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_textfield_contents = mock_get
        testobj.master = types.SimpleNamespace(event_list=['datum0', 'datum1'],
                                               event_data=['event0', 'event1'],
                                               oldtext='oldtext',
                                               progress_list=mockwx.MockListCtrl(),
                                               progress_text=mockwx.MockTextCtrl())
        assert capsys.readouterr().out == ("called ListCtrl.__init__ with args () {}\n"
                                           "called TextCtrl.__init__ with args () {}\n")
        mock_text = 'oldtext'
        testobj.on_deselect_item(evt)
        assert testobj.master.event_data == ['event0', 'event1']
        assert testobj.master.oldtext == 'oldtext'
        assert capsys.readouterr().out == ""
        evt.Index = 1  # mock_index_2
        testobj.on_deselect_item(evt)
        assert testobj.master.event_data == ['event0', 'event1']
        assert testobj.master.oldtext == 'oldtext'
        assert capsys.readouterr().out == ("called Page6Gui.get_textfield_contents with args"
                                           f" ({testobj.master.progress_text},)\n"
                                           "called event.Skip\n")
        mock_text = 'newtext'
        testobj.on_deselect_item(evt)
        assert testobj.master.event_data == ['newtext', 'event1']
        assert testobj.master.oldtext == 'newtext'
        assert capsys.readouterr().out == (
                "called Page6Gui.get_textfield_contents with args"
                f" ({testobj.master.progress_text},)\n"
                "called ListCtrl.SetItem with args (1, 0, 'datum0 - newtext')\n"
                "called ListCtrl.SetItemData with args (1, 0)\n"
                "called event.Skip\n")
        testobj.master.oldtext = 'oldtext'
        testobj.master.event_data = ['event0', 'event1']
        mock_text = 'oldtext' + 8 * '1234567890'
        testobj.on_deselect_item(evt)
        assert testobj.master.event_data == [mock_text, 'event1']
        assert testobj.master.oldtext == mock_text
        assert capsys.readouterr().out == (
                "called Page6Gui.get_textfield_contents with args"
                f" ({testobj.master.progress_text},)\n"
                f"called ListCtrl.SetItem with args (1, 0, 'datum0 - {mock_text[:80] + '...'}')\n"
                "called ListCtrl.SetItemData with args (1, 0)\n"
                "called event.Skip\n")

    def test_on_select_item(self, monkeypatch, capsys):
        """unittest for Page6Gui.on_select_item
        """
        def mock_set(*args):
            print('called Page6Gui.set_textfield_contents with args', args)
        event = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        event.Index = 0
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_textfield_contents = mock_set
        testobj.master = types.SimpleNamespace(event_list=['datum0', 'datum1'],
                                               event_data=['event0', 'event1'],
                                               oldtext='oldtext',
                                               progress_text=mockwx.MockTextCtrl())
        testobj.parent = types.SimpleNamespace(pagedata=types.SimpleNamespace(arch=True))
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj.on_select_item(event)
        assert testobj.current_item == 0
        assert capsys.readouterr().out == ""
        event.Index = 1
        testobj.on_select_item(event)
        assert testobj.current_item == 1
        assert testobj.master.oldtext == 'event0'
        assert not testobj.master.initializing
        assert capsys.readouterr().out == (
                "called text.SetEditable with arg False\n"
                "called Page6Gui.set_textfield_contents with args"
                f" ({testobj.master.progress_text}, 'event0')\n"
                "called text.Enable with arg True\n"
                "called text.SetFocus\n")
        testobj.parent.pagedata.arch = False
        testobj.on_select_item(event)
        assert testobj.current_item == 1
        assert testobj.master.oldtext == 'event0'
        assert not testobj.master.initializing
        assert capsys.readouterr().out == (
                "called text.SetEditable with arg False\n"
                "called text.SetEditable with arg True\n"
                "called Page6Gui.set_textfield_contents with args"
                f" ({testobj.master.progress_text}, 'event0')\n"
                "called text.Enable with arg True\n"
                "called text.SetFocus\n")

    def test_create_new_listitem(self, monkeypatch, capsys):
        """unittest for Page6Gui.create_new_listitem
        """
        def mock_set(*args):
            print('called testfield.set_contents with args', args)
        listbox = mockwx.MockListBox()
        textfield = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == ("called ListBox.__init__ with args () {}\n"
                                           "called TextCtrl.__init__ with args () {}\n")
        textfield.set_contents = mock_set
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.create_new_listitem(listbox, textfield, 'datum', 'oldtext')
        assert capsys.readouterr().out == (
                "called ListBox.InsertItem with args (1, 'datum - oldtext')\n"
                "called listbox.SetSelection with args (1,)\n"
                "called testfield.set_contents with args ('oldtext',)\n"
                "called text.SetEditable with arg True\n"
                "called text.SetFocus\n")

    def test_clear_list(self, monkeypatch, capsys):
        """unittest for Page6Gui.clear_list
        """
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.clear_list(listbox)
        assert capsys.readouterr().out == ("called ListCtrl.DeleteAllItems\n")

    def test_add_first_listitem(self, monkeypatch, capsys):
        """unittest for Page6Gui.add_first_listitem
        """
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_first_listitem(listbox, 'text')
        assert capsys.readouterr().out == (
                "called ListCtrl.InsertItem with args (0, 'text')\n"
                "called ListCtrl.SetItem with args ('itemindex', 0, 'text')\n"
                "called ListCtrl.SetItemData with args ('itemindex', -1)\n")

    def test_add_item_to_list(self, monkeypatch, capsys):
        """unittest for Page6Gui.add_item_to_list
        """
        def mock_convert(*args, **kwargs):
            print('called Page6Gui.convert_text with args', args, kwargs)
            return conv_text
        listbox = mockwx.MockListCtrl()
        textfield = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == ("called ListCtrl.__init__ with args () {}\n"
                                           "called TextCtrl.__init__ with args () {}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(event_data=['xxx', 'yyy'])
        testobj.convert_text = mock_convert
        conv_text = None
        testobj.add_item_to_list(listbox, textfield, 1, 'datum')
        assert capsys.readouterr().out == (
                f"called Page6Gui.convert_text with args ({textfield}, 'yyy') {{'to': 'plain'}}\n"
                f"called ListCtrl.InsertItem with args ({testee.sys.maxsize}, 'datum')\n"
                "called ListCtrl.SetItem with args ('itemindex', 0, 'datum - ')\n"
                "called ListCtrl.SetItemData with args ('itemindex', 1)\n")
        conv_text = 'converted'
        testobj.add_item_to_list(listbox, textfield, 1, 'eejj-mm-dd hh:mm:ss')
        assert capsys.readouterr().out == (
                f"called Page6Gui.convert_text with args ({textfield}, 'yyy') {{'to': 'plain'}}\n"
                f"called ListCtrl.InsertItem with args ({testee.sys.maxsize},"
                " 'eejj-mm-dd hh:mm:ss')\n"
                "called ListCtrl.SetItem with args"
                " ('itemindex', 0, 'eejj-mm-dd hh:mm:ss - converted')\n"
                "called ListCtrl.SetItemData with args ('itemindex', 1)\n")
        conv_text = 'converted' + 8 * '1234567890'
        testobj.add_item_to_list(listbox, textfield, 1, 'eejj-mm-dd hh:mm:ss xxxxx')
        assert capsys.readouterr().out == (
                f"called Page6Gui.convert_text with args ({textfield}, 'yyy') {{'to': 'plain'}}\n"
                f"called ListCtrl.InsertItem with args ({testee.sys.maxsize},"
                " 'eejj-mm-dd hh:mm:ss xxxxx')\n"
                "called ListCtrl.SetItem with args"
                f" ('itemindex', 0, 'eejj-mm-dd hh:mm:ss - {conv_text[:80] + '...'}')\n"
                "called ListCtrl.SetItemData with args ('itemindex', 1)\n")

    def test_set_list_callbacks(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_list_callback
        """
        def mock_bind(*args):
            print('called Panel.Bind with args', args)
        def mock_unbind(*args):
            print('called Panel.Unbind with args', args)
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.Bind = mock_bind
        testobj.Unbind = mock_unbind
        testobj.appbase = types.SimpleNamespace(is_user=True)
        testobj.set_list_callbacks(listbox, 'callback0', 'callback1')
        assert capsys.readouterr().out == (
                "called Panel.Bind with args"
                f" ({testee.wx.EVT_LIST_ITEM_ACTIVATED}, 'callback0', {listbox})\n"
                f"called ListCtrl.Bind with args ({testee.wx.EVT_LEFT_UP}, 'callback0')\n")
        testobj.appbase.is_user = False
        testobj.set_list_callbacks(listbox, 'callback0', 'callback1')
        assert capsys.readouterr().out == (
                f"called Panel.Unbind with args ({testee.wx.EVT_LIST_ITEM_ACTIVATED}, {listbox})\n"
                f"called ListCtrl.Unbind with args ({testee.wx.EVT_LEFT_UP},)\n")

    def test_set_listitem_text(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_listitem_text
        """
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_listitem_text(listbox, 'itemindex', 'text')
        assert capsys.readouterr().out == (
                "called ListCtrl.SetItemText with args ('itemindex', 'text')\n")

    def test_set_listitem_data(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_listitem_data
        """
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_listitem_data(listbox, 1)
        assert capsys.readouterr().out == ("called ListCtrl.SetItemData with args (1, 0)\n")

    def test_get_listitem_text(self, monkeypatch, capsys):
        """unittest for Page6Gui.get_listitem_text
        """
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_listitem_text(listbox, 'itemindex')
        assert capsys.readouterr().out == (
                "called ListCtrl.GetItemText with args ('itemindex', 0)\n")

    def test_get_list_row(self, monkeypatch, capsys):
        """unittest for Page6Gui.get_list_row
        """
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_list_row(listbox) == -1
        assert capsys.readouterr().out == ("called ListCtrl.GetFirstSelected\n")

    def test_set_list_row(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_list_row
        """
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_list_row(listbox, 'num')
        assert capsys.readouterr().out == ("called ListCtrl.Select with args ('num',)\n")

    def test_get_list_rowcount(self, monkeypatch, capsys):
        """unittest for Page6Gui.get_list_rowcount
        """
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_list_rowcount(listbox) == 2
        assert capsys.readouterr().out == ("called ListCtrl.GetItemCount\n")

    def test_clear_textfield(self, monkeypatch, capsys):
        """unittest for Page6Gui.clear_textfield
        """
        textfield = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.clear_textfield(textfield)
        assert capsys.readouterr().out == ("called text.Clear\n")

    # def _test_protect_textfield(self, monkeypatch, capsys):
    #     """unittest for Page6Gui.protect_textfield
    #     """
    #     textfield = mockwx.MockTextCtrl()
    #     assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.protect_textfield(value=True) == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def test_get_textfield_contents(self, monkeypatch, capsys):
        """unittest for Page6Gui.get_textfield_contents
        """
        def mock_get():
            print('called textfield.get_contents')
            return 'contents'
        textfield = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        textfield.get_contents = mock_get
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textfield_contents(textfield) == "contents"
        assert capsys.readouterr().out == ("called textfield.get_contents\n")

    def test_set_textfield_contents(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_textfield_contents
        """
        def mock_set(*args):
            print('called textfield.set_contents with args', *args)
        textfield = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        textfield.set_contents = mock_set
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_textfield_contents(textfield, 'text')
        assert capsys.readouterr().out == ("called textfield.set_contents with args text\n")

    def test_move_cursor_to_end(self, monkeypatch, capsys):
        """unittest for Page6Gui.move_cursor_to_end
        """
        textfield = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.move_cursor_to_end(textfield)
        assert capsys.readouterr().out == ("called text.MoveEnd\n")

    # def _test_set_focus_to_textfield(self, monkeypatch, capsys):
    #     """unittest for Page6Gui.set_focus_to_textfield
    #     """
    #     textfield = mockwx.MockTextCtrl()
    #     assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.set_focus_to_textfield() == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def test_convert_text(self, monkeypatch, capsys):
        """unittest for Page6Gui.convert_text
        """
        def mock_get():
            print('called textfield.get_contents')
            return 'contents'
        def mock_set(*args):
            print('called textfield.set_contents with args', *args)
        textfield = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        textfield.get_contents = mock_get
        textfield.set_contents = mock_set
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.convert_text(textfield, 'text', 'rich') == "contents"
        assert capsys.readouterr().out == ("called textfield.set_contents with args text\n"
                                           "called textfield.get_contents\n")
        assert testobj.convert_text(textfield, 'text', 'plain') == "text"
        assert capsys.readouterr().out == ""
        assert testobj.convert_text(textfield, 'text', 'other') == ""
        assert capsys.readouterr().out == ""


class TestEasyPrinter:
    """unittest for gui_wx.EasyPrinter
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.EasyPrinter object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called EasyPrinter.__init__')
        monkeypatch.setattr(testee.wx.html.HtmlEasyPrinting, '__init__', mock_init)
        testobj = testee.EasyPrinter()
        assert capsys.readouterr().out == 'called EasyPrinter.__init__\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for EasyPrinter.__init__
        """
        monkeypatch.setattr(testee.wx.html, 'HtmlEasyPrinting', mockwx.MockEasyPrinting)
        testobj = testee.EasyPrinter()
        assert capsys.readouterr().out == "called HtmlEasyPrinting.__init__\n"

    def test_print(self, monkeypatch, capsys):
        """unittest for EasyPrinter.print_
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.wx.html.HtmlEasyPrinting, 'SetHeader',
                            mockwx.MockEasyPrinting.SetHeader)
        monkeypatch.setattr(testee.wx.html.HtmlEasyPrinting, 'PreviewText',
                            mockwx.MockEasyPrinting.PreviewText)
        testobj.print('text', 'doc_name')
        assert capsys.readouterr().out == (
                "called HtmlEasyPrinting.SetHeader with args ('doc_name',)\n"
                "called HtmlEasyPrinting.PreviewText with args ('text',)\n")


class TestSortOptionsDialogGui:
    """unittest for gui_wx.SortOptionsDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.SortOptionsDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SortOptionsDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.SortOptionsDialogGui, '__init__', mock_init)
        testobj = testee.SortOptionsDialogGui()
        assert capsys.readouterr().out == 'called SortOptionsDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.__init__
        """
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'GridBagSizer', mockwx.MockGridSizer)
        parent = types.SimpleNamespace(gui='SortOptionsDialogGui')
        testobj = testee.SortOptionsDialogGui('master', parent, 'title')
        assert testobj.master == 'master'
        assert isinstance(testobj.sizer, testee.wx.BoxSizer)
        assert isinstance(testobj.grid, testee.wx.GridBagSizer)
        testobj.row = 0
        assert capsys.readouterr().out == (
                f"called Dialog.__init__ with args"
                " () {'title': 'title', 'pos': wx.Point(-1, -1), 'style': 536877120}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called GridSizer.__init__ with args (2, 2) {}\n"
                "called vert sizer.Add with args MockGridSizer (0, 2288, 5)\n"
                "called dialog.SetSizer with args (vert sizer,)\n"
                "called dialog.SetAutoLayout with args (True,)\n"
                f"called vert sizer.Fit with args ({testobj},)\n")

    def test_add_checkbox_line(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.add_checkbox_line
        """
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj.row = 0
        result = testobj.add_checkbox_line('tekst', 'checked', 'callback')
        assert isinstance(result, testee.wx.CheckBox)
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ({testobj},) {{'label': 'tekst'}}\n"
                "called CheckBox.Bind with args"
                f" ({testee.wx.EVT_CHECKBOX}, {testobj.enable_fields}) {{}}\n"
                "called GridSizer.Add with args MockCheckBox ((0, 0), (1, 4))\n"
                "called GridSizer.AddGrowableCol with args (1,)\n")

    def test_add_seqnumtext_to_list(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.add_seqnumtext_to_list
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj.row = 0
        assert isinstance(testobj.add_seqnumtext_to_list('label'), testee.wx.StaticText)
        assert capsys.readouterr().out == (
                "called StaticText.__init__ with args"
                f" ({testobj},) {{'label': ' {testobj.row}.'}}\n"
                "called GridSizer.Add with args MockStaticText ((1, 0),) {'flag': 2048}\n")

    def test_add_colnameselector_to_list(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.add_colnameselector_to_list
        """
        monkeypatch.setattr(testee.wx, 'ComboBox', mockwx.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj.row = 0
        result = testobj.add_colnameselector_to_list('name', ['lijst'])
        assert isinstance(result, testee.wx.ComboBox)
        assert capsys.readouterr().out == (
                "called ComboBox.__init__ with args"
                f" ({testobj},) {{'size': (90, -1), 'choices': ['lijst'], 'style': 32}}\n"
                "called combobox.SetSelection with args (0,)\n"
                "called GridSizer.Add with args MockComboBox ((0, 1),)\n")

    def test_add_radiobuttons_to_line(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.add_radiobuttons_to_line
        """
        monkeypatch.setattr(testee.wx, 'RadioButton', mockwx.MockRadioButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj.row = 0
        result = testobj.add_radiobuttons_to_line([('Asc', 'x', True), ('Desc', 'y', False)])
        assert len(result) == 2
        assert isinstance(result[0], testee.wx.RadioButton)
        assert isinstance(result[1], testee.wx.RadioButton)
        assert capsys.readouterr().out == (
                "called RadioButton.__init__ with args"
                f" ({testobj},) {{'label': 'Asc', 'style': 4}}\n"
                "called radiobutton.SetValue with args (True,)\n"
                "called GridSizer.Add with args MockRadioButton ((0, 2),) {'flag': 2048}\n"
                f"called RadioButton.__init__ with args ({testobj},) {{'label': 'Desc'}}\n"
                "called radiobutton.SetValue with args (False,)\n"
                "called GridSizer.Add with args MockRadioButton ((0, 3),) {'flag': 2048}\n")

    def test_add_okcancel_buttonbox(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.add_okcancel_buttonbox
        """
        monkeypatch.setattr(testee.wx.Dialog, 'CreateButtonSizer',
                            mockwx.MockDialog.CreateButtonSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_okcancel_buttonbox()
        assert capsys.readouterr().out == (
                "called dialog.CreateButtonSizer with args (20,)\n"
                "called BoxSizer.__init__ with args ()\n"
                "called  sizer.Add with args MockBoxSizer (0, 2544, 5)\n")

    def test_enable_fields(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.enable_fields
        """
        def mock_get(self):
            print('called event.GetEventWidget')
            return cb
        monkeypatch.setattr(mockwx.MockEvent, 'GetEventWidget', mock_get)
        event = mockwx.MockEvent()
        lbl = mockwx.MockControl()
        cmb = mockwx.MockControl()
        rba = mockwx.MockControl()
        rbd = mockwx.MockControl()
        cb = mockwx.MockCheckBox()
        assert capsys.readouterr().out == ("called event.__init__ with args ()\n"
                                           "called Control.__init__\n"
                                           "called Control.__init__\n"
                                           "called Control.__init__\n"
                                           "called Control.__init__\n"
                                           "called CheckBox.__init__ with args () {}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(widgets=[(lbl, cmb, [rba, rbd])])
        testobj.enable_fields(event)
        assert capsys.readouterr().out == (
                "called event.GetEventWidget\n"
                "called checkbox.GetValue\n"
                "called Control.Enable with arg value from checkbox\n"
                "called Control.Enable with arg value from checkbox\n"
                "called Control.Enable with arg value from checkbox\n"
                "called Control.Enable with arg value from checkbox\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.accept
        """
        def mock_confirm():
            print('called SortOptionsDialog.confirm')
            return True
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        assert testobj.accept()
        assert capsys.readouterr().out == "called SortOptionsDialog.confirm\n"

    def test_get_combobox_value(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.get_combobox_value
        """
        cmb = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_combobox_value(cmb) == "current text"
        assert capsys.readouterr().out == ("called combobox.GetStringSelection\n")

    def test_get_rbgroup_value(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.get_rbgroup_value
        """
        def mock_get(self):
            nonlocal counter
            print('called RadioButton.GetValue')
            counter += 1
            return counter > 1
        monkeypatch.setattr(mockwx.MockRadioButton, 'GetValue', mock_get)
        rba = mockwx.MockRadioButton()
        rbd = mockwx.MockRadioButton()
        assert capsys.readouterr().out == ("called RadioButton.__init__ with args () {}\n"
                                           "called RadioButton.__init__ with args () {}\n")
        rbg = []
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_rbgroup_value(rbg) is None
        rbg = [rba, rbd]
        testobj = self.setup_testobj(monkeypatch, capsys)
        counter = 0
        assert testobj.get_rbgroup_value(rbg) == 2
        assert capsys.readouterr().out == ("called RadioButton.GetValue\n"
                                           "called RadioButton.GetValue\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.get_checkbox_value
        """
        cb = mockwx.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_checkbox_value(cb) == "value from checkbox"
        assert capsys.readouterr().out == ("called checkbox.IsChecked\n")


class TestSelectOptionsDialogGui:
    """unittests for wxgui.SelectOptionsDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.SelectOptionsDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called SelectOptionsDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.SelectOptionsDialogGui, '__init__', mock_init)
        testobj = testee.SelectOptionsDialogGui()
        assert capsys.readouterr().out == 'called SelectOptionsDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.__init__
        """
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        parent = types.SimpleNamespace(gui='SelectOptionsDialogGui')
        testobj = testee.SelectOptionsDialogGui('master', parent, 'title')
        assert isinstance(testobj.sizer, testee.wx.BoxSizer)
        assert isinstance(testobj.grid, testee.wx.FlexGridSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args"
                " () {'title': 'Selecteren', 'style': 536877120}\n")

    def test_add_checkbox_to_grid(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.add_checkbox_to_grid
        """
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockwx.MockFlexGridSizer()
        assert capsys.readouterr().out == "called FlexGridSizer.__init__ with args () {}\n"
        result = testobj.add_checkbox_to_grid('title', 'row', 'col')
        assert isinstance(result, testee.wx.CheckBox)
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ({testobj},) {{'label': 'title'}}\n"
                "called FlexGridSizer.Add with args MockCheckBox (0, 64, 10)\n")

    def test_start_optionsblock(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.start_optionsblock
        """
        monkeypatch.setattr(testee.wx, 'FlexGridSizer', mockwx.MockFlexGridSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockwx.MockFlexGridSizer()
        assert capsys.readouterr().out == "called FlexGridSizer.__init__ with args () {}\n"
        assert isinstance(testobj.start_optionsblock(), testee.wx.FlexGridSizer)
        assert capsys.readouterr().out == "called FlexGridSizer.__init__ with args (2, 2, 2) {}\n"

    def test_add_textentry_line_to_block(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.add_textentry_line_to_block
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        block = mockwx.MockFlexGridSizer()
        assert capsys.readouterr().out == "called FlexGridSizer.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'Bind', mockwx.MockPanel.Bind)
        result = testobj.add_textentry_line_to_block(block, 'labeltext', 'callback')
        assert isinstance(result, testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                "called StaticText.__init__ with args"
                f" ({testobj},) {{'label': 'labeltext', 'size': (90, -1)}}\n"
                "called TextCtrl.__init__ with args"
                f" ({testobj},) {{'value': '', 'size': (153, -1)}}\n"
                f"called Panel.Bind with args ('callback', {result})\n"
                "called FlexGridSizer.AddMany with args"
                " MockStaticText, (0, 192, 10), MockTextCtrl, (0, 192, 5)\n")
        result = testobj.add_textentry_line_to_block(block, 'labeltext', 'callback', first=True)
        assert isinstance(result, testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                "called StaticText.__init__ with args"
                f" ({testobj},) {{'label': 'labeltext', 'size': (90, -1)}}\n"
                "called TextCtrl.__init__ with args"
                f" ({testobj},) {{'value': '', 'size': (153, -1)}}\n"
                f"called Panel.Bind with args ('callback', {result})\n"
                "called FlexGridSizer.AddMany with args"
                " MockStaticText, (0, 64, 10), MockTextCtrl, (0, 64, 5)\n")

    def test_add_radiobuttonrow_to_block(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.add_radiobuttonrow_to_block
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(testee.wx, 'RadioButton', mockwx.MockRadioButton)
        block = mockwx.MockFlexGridSizer()
        assert capsys.readouterr().out == "called FlexGridSizer.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'Bind', mockwx.MockPanel.Bind)
        result = testobj.add_radiobuttonrow_to_block(block, ['button', 'defs'], 'callback')
        assert len(result) == 2
        assert isinstance(result[0], testee.wx.RadioButton)
        assert isinstance(result[1], testee.wx.RadioButton)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called RadioButton.__init__ with args"
                f" ({testobj},) {{'label': 'button', 'style': 4}}\n"
                f"called Panel.Bind with args ('callback', {result[0]})\n"
                "called hori sizer.Add with args MockRadioButton (0, 2048)\n"
                "called RadioButton.__init__ with args"
                f" ({testobj},) {{'label': 'defs'}}\n"
                f"called Panel.Bind with args ('callback', {result[1]})\n"
                "called hori sizer.Add with args MockRadioButton (0, 2048)\n"
                "called StaticText.__init__ with args"
                f" ({testobj},) {{'label': '', 'size': (70, -1)}}\n"
                "called FlexGridSizer.AddMany with args"
                f" MockBoxSizer, (0,), MockStaticText, (0,)\n")
        result = testobj.add_radiobuttonrow_to_block(block, ['button', 'defs'], alignleft=False)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called RadioButton.__init__ with args"
                f" ({testobj},) {{'label': 'button', 'style': 4}}\n"
                "called hori sizer.Add with args MockRadioButton (0, 2048)\n"
                "called RadioButton.__init__ with args"
                f" ({testobj},) {{'label': 'defs'}}\n"
                "called hori sizer.Add with args MockRadioButton (0, 2048)\n"
                "called FlexGridSizer.Add with args MockBoxSizer (0, 64, 10)\n")

    def test_add_checkboxlist_to_block(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.add_checkboxlist_to_block
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(testee.wx, 'CheckListBox', mockwx.MockCheckListBox)
        block = mockwx.MockFlexGridSizer()
        assert capsys.readouterr().out == "called FlexGridSizer.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'Bind', mockwx.MockPanel.Bind)
        result = testobj.add_checkboxlist_to_block(block, ['xx', 'yy', 'zz'], 'callback')
        assert isinstance(result, testee.wx.CheckListBox)
        assert capsys.readouterr().out == (
                "called CheckListBox.__init__ with args"
                f" ({testobj},) {{'size': (-1, 120), 'choices': ['xx', 'yy', 'zz']}}\n"
                f"called Panel.Bind with args ('callback', {result})\n"
                "called StaticText.__init__ with args"
                f" ({testobj},) {{'label': 'selecteer\\neen of meer:', 'size': (70, -1)}}\n"
                "called FlexGridSizer.Add with args MockStaticText (0, 448, 5)\n"
                "called FlexGridSizer.Add with args MockCheckListBox (0, 448, 5)\n")

    def test_finish_block(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.finish_block
        """
        block = mockwx.MockFlexGridSizer()
        assert capsys.readouterr().out == "called FlexGridSizer.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockwx.MockFlexGridSizer()
        assert capsys.readouterr().out == "called FlexGridSizer.__init__ with args () {}\n"
        testobj.finish_block(block, 'row', 'col')
        assert capsys.readouterr().out == (
                "called FlexGridSizer.Add with args MockFlexGridSizer ('row', 'col')\n")

    def test_add_okcancel_buttonbar(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.add_okcancel_buttonbar
        """
        monkeypatch.setattr(testee.wx.Dialog, 'CreateButtonSizer',
                            mockwx.MockDialog.CreateButtonSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_okcancel_buttonbar()
        assert capsys.readouterr().out == (
                "called dialog.CreateButtonSizer with args (20,)\n"
                "called BoxSizer.__init__ with args ()\n"
                "called  sizer.Add with args MockBoxSizer (0, 2544, 5)\n")

    def test_finalize_display(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.finalize_display
        """
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.finalize_display()
        assert capsys.readouterr().out == ("called dialog.SetSizer with args ( sizer,)\n"
                                           "called dialog.SetAutoLayout with args (True,)\n"
                                           f"called  sizer.Fit with args ({testobj},)\n")

    def test_set_textentry_value(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.set_textentry_value
        """
        textentry = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_textentry_value(textentry, 'value')
        assert capsys.readouterr().out == "called text.SetValue with args ('value',)\n"

    def test_set_radiobutton_value(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.set_radiobutton_value
        """
        radiobutton = mockwx.MockRadioButton()
        assert capsys.readouterr().out == "called RadioButton.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_radiobutton_value(radiobutton, 'value')
        assert capsys.readouterr().out == "called radiobutton.SetValue with args ('value',)\n"

    def test_set_checkbox_value(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.set_checkbox_value
        """
        checkbox = mockwx.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_checkbox_value(checkbox, 'value')
        assert capsys.readouterr().out == "called checkbox.SetValue with args ('value',)\n"

    # def _test_set_default_values(self, monkeypatch, capsys):
    #     """unittest for SelectOptionsDialogGui.set_default_values
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.set_default_values(sel_args) == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def test_on_text(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.on_text
        """
        def mock_get():
            print('called event.GetEventObject')
            return testobj.master.text_gt
        def mock_get_2():
            print('called event.GetEventObject')
            return testobj.master.text_lt
        def mock_get_3():
            print('called event.GetEventObject')
            return testobj.master.text_zoek
        def mock_get_4():
            print('called event.GetEventObject')
            return testobj.master.text_zoek2
        def mock_getstring():
            print('called event.GetString')
            return ''
        event = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(text_gt=mockwx.MockTextCtrl(),
                                               text_lt=mockwx.MockTextCtrl(),
                                               text_zoek=mockwx.MockTextCtrl(),
                                               text_zoek2=mockwx.MockTextCtrl(),
                                               cb_actie=mockwx.MockCheckBox(),
                                               cb_text=mockwx.MockCheckBox())
        assert capsys.readouterr().out == ("called TextCtrl.__init__ with args () {}\n"
                                           "called TextCtrl.__init__ with args () {}\n"
                                           "called TextCtrl.__init__ with args () {}\n"
                                           "called TextCtrl.__init__ with args () {}\n"
                                           "called CheckBox.__init__ with args () {}\n"
                                           "called CheckBox.__init__ with args () {}\n")
        with pytest.raises(UnboundLocalError):
            testobj.on_text(event)
        assert capsys.readouterr().out == ("called event.GetEventObject\n"
                                           "called event.GetString\n")
        event.GetEventObject = mock_get
        assert testobj.on_text(event) == testobj.master.cb_actie
        assert capsys.readouterr().out == ("called event.GetEventObject\n"
                                           "called event.GetString\n"
                                           "called checkbox.SetValue with args (True,)\n")
        event.GetEventObject = mock_get_2
        assert testobj.on_text(event) == testobj.master.cb_actie
        assert capsys.readouterr().out == ("called event.GetEventObject\n"
                                           "called event.GetString\n"
                                           "called checkbox.SetValue with args (True,)\n")
        event.GetEventObject = mock_get_3
        assert testobj.on_text(event) == testobj.master.cb_text
        assert capsys.readouterr().out == ("called event.GetEventObject\n"
                                           "called event.GetString\n"
                                           "called checkbox.SetValue with args (True,)\n")
        event.GetEventObject = mock_get_4
        assert testobj.on_text(event) == testobj.master.cb_text
        assert capsys.readouterr().out == ("called event.GetEventObject\n"
                                           "called event.GetString\n"
                                           "called checkbox.SetValue with args (True,)\n")
        event.GetString = mock_getstring
        event.GetEventObject = mock_get
        assert testobj.on_text(event) == testobj.master.cb_actie
        assert capsys.readouterr().out == ("called event.GetEventObject\n"
                                           "called event.GetString\n"
                                           "called checkbox.SetValue with args (False,)\n")
        event.GetEventObject = mock_get_2
        assert testobj.on_text(event) == testobj.master.cb_actie
        assert capsys.readouterr().out == ("called event.GetEventObject\n"
                                           "called event.GetString\n"
                                           "called checkbox.SetValue with args (False,)\n")
        event.GetEventObject = mock_get_3
        assert testobj.on_text(event) == testobj.master.cb_text
        assert capsys.readouterr().out == ("called event.GetEventObject\n"
                                           "called event.GetString\n"
                                           "called checkbox.SetValue with args (False,)\n")
        event.GetEventObject = mock_get_4
        assert testobj.on_text(event) == testobj.master.cb_text
        assert capsys.readouterr().out == ("called event.GetEventObject\n"
                                           "called event.GetString\n"
                                           "called checkbox.SetValue with args (False,)\n")

    def test_on_cb_checked(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.on_cb_checked
        """
        def mock_get():
            print('called event.GetEventObject')
            return testobj.master.clb_soort
        def mock_get_2():
            print('called event.GetEventObject')
            return testobj.master.clb_stat
        def mock_is(self, arg):
            print(f'called CheckListBox.IsChecked with arg {arg}')
            return False
        event = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(clb_soort=mockwx.MockCheckListBox(),
                                               clb_stat=mockwx.MockCheckListBox(),
                                               cb_soort=mockwx.MockCheckBox(),
                                               cb_status=mockwx.MockCheckBox())
        assert capsys.readouterr().out == ("called CheckListBox.__init__ with args () {}\n"
                                           "called CheckListBox.__init__ with args () {}\n"
                                           "called CheckBox.__init__ with args () {}\n"
                                           "called CheckBox.__init__ with args () {}\n")
        with pytest.raises(AttributeError):
            testobj.on_cb_checked(event)
        assert capsys.readouterr().out == ("called event.GetSelection\n"
                                           "called event.GetEventObject\n")
        event.GetEventObject = mock_get
        assert testobj.on_cb_checked(event) == testobj.master.cb_soort
        assert capsys.readouterr().out == (
                "called event.GetSelection\n"
                "called event.GetEventObject\n"
                "called CheckListBox.SetSelection with args ('index',)\n"
                "called CheckListBox.GetCount\n"
                "called CheckListBox.IsChecked with arg 0\n"
                "called checkbox.SetValue with args (True,)\n")
        event.GetEventObject = mock_get_2
        assert testobj.on_cb_checked(event) == testobj.master.cb_status
        assert capsys.readouterr().out == (
                "called event.GetSelection\n"
                "called event.GetEventObject\n"
                "called CheckListBox.SetSelection with args ('index',)\n"
                "called CheckListBox.GetCount\n"
                "called CheckListBox.IsChecked with arg 0\n"
                "called checkbox.SetValue with args (True,)\n")
        monkeypatch.setattr(mockwx.MockCheckListBox, 'IsChecked', mock_is)
        event.GetEventObject = mock_get
        assert testobj.on_cb_checked(event) == testobj.master.cb_soort
        assert capsys.readouterr().out == (
                "called event.GetSelection\n"
                "called event.GetEventObject\n"
                "called CheckListBox.SetSelection with args ('index',)\n"
                "called CheckListBox.GetCount\n"
                "called CheckListBox.IsChecked with arg 0\n"
                "called CheckListBox.IsChecked with arg 1\n"
                "called checkbox.SetValue with args (False,)\n")
        event.GetEventObject = mock_get_2
        assert testobj.on_cb_checked(event) == testobj.master.cb_status
        assert capsys.readouterr().out == (
                "called event.GetSelection\n"
                "called event.GetEventObject\n"
                "called CheckListBox.SetSelection with args ('index',)\n"
                "called CheckListBox.GetCount\n"
                "called CheckListBox.IsChecked with arg 0\n"
                "called CheckListBox.IsChecked with arg 1\n"
                "called checkbox.SetValue with args (False,)\n")

    def test_on_rb_checked(self, monkeypatch, capsys):
        """unittest for selectoptionsdialoggui.on_rb_checked
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(cb_arch=mockwx.MockCheckBox())
        testobj.on_rb_checked()
        assert capsys.readouterr().out == ("called CheckBox.__init__ with args () {}\n"
                                           "called checkbox.SetValue with args (True,)\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.accept
        """
        def mock_confirm():
            print('called SelectOptionsDialog.confirm')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == ("called SelectOptionsDialog.confirm\n")

    def test_get_textentry_value(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.get_textentry_value
        """
        textentry = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textentry_value(textentry) == "value from textctrl"
        assert capsys.readouterr().out == "called text.GetValue\n"

    def test_get_radiobutton_value(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.get_radiobutton_value
        """
        radiobutton = mockwx.MockRadioButton()
        assert capsys.readouterr().out == "called RadioButton.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_radiobutton_value(radiobutton) == "value from radiobutton"
        assert capsys.readouterr().out == "called radiobutton.GetValue\n"

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.get_checkbox_value
        """
        checkbox = mockwx.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_checkbox_value(checkbox) == "value from checkbox"
        assert capsys.readouterr().out == "called checkbox.IsChecked\n"

    def test_set_focus_to(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.set_focus_to
        """
        widget = mockwx.MockControl()
        assert capsys.readouterr().out == "called Control.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus_to(widget)
        assert capsys.readouterr().out == "called Control.SetFocus\n"


class TestSettOptionsDialogGui:
    """unittests for wxgui.SettOptionsDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.SettOptionsDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called SettOptionsDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.SettOptionsDialogGui, '__init__', mock_init)
        testobj = testee.SettOptionsDialogGui()
        assert capsys.readouterr().out == 'called SettOptionsDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.__init__
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        parent = types.SimpleNamespace(gui='SettptionsDialogGui')
        testobj = testee.SettOptionsDialogGui('master', parent, 'title')
        assert testobj.master == 'master'
        assert isinstance(testobj.sizer, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {'title': 'title', 'size': (300, 300)}\n"
                "called BoxSizer.__init__ with args (8,)\n")

    def test_add_listbox_with_buttons(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.add_listbox_with_buttons
        """
        monkeypatch.setattr(testee.wx.adv, 'EditableListBox', mockwx.MockEditableListBox)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        result = testobj.add_listbox_with_buttons('titel', ['da', 'ta'], {})
        assert isinstance(result, testee.wx.adv.EditableListBox)
        assert capsys.readouterr().out == (
                f"called EditableListBox.__init__ with args ({testobj},)"
                " {'label': 'titel', 'pos': (50, 50), 'size': (250, 250), 'style': 512}\n"
                "called EditableListBox.SetStrings with args (['da', 'ta'],)\n"
                "called BoxSizer.__init__ with args (4,)\n"
                "called hori sizer.Add with args MockEditableListBox (0, 2544, 5)\n"
                "called  sizer.Add with args MockBoxSizer (0, 240, 5)\n")
        result = testobj.add_listbox_with_buttons('titel', ['da', 'ta'], {'can_add_remove': False})
        assert isinstance(result, testee.wx.adv.EditableListBox)
        assert capsys.readouterr().out == (
                f"called EditableListBox.__init__ with args ({testobj},)"
                " {'label': 'titel', 'pos': (50, 50), 'size': (250, 250), 'style': 512}\n"
                "called EditableListBox.SetStrings with args (['da', 'ta'],)\n"
                "called BoxSizer.__init__ with args (4,)\n"
                "called hori sizer.Add with args MockEditableListBox (0, 2544, 5)\n"
                "called  sizer.Add with args MockBoxSizer (0, 240, 5)\n")
        result = testobj.add_listbox_with_buttons('titel', ['da', 'ta'], {'can_add_remove': True})
        assert isinstance(result, testee.wx.adv.EditableListBox)
        assert capsys.readouterr().out == (
                f"called EditableListBox.__init__ with args ({testobj},)"
                " {'label': 'titel', 'pos': (50, 50), 'size': (250, 250), 'style': 1792}\n"
                "called EditableListBox.SetStrings with args (['da', 'ta'],)\n"
                "called BoxSizer.__init__ with args (4,)\n"
                "called hori sizer.Add with args MockEditableListBox (0, 2544, 5)\n"
                "called  sizer.Add with args MockBoxSizer (0, 240, 5)\n")

    def test_add_label(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.add_label
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(testee.wx, 'StaticLine', mockwx.MockStaticLine)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_label(['info', 'text'])
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called StaticText.__init__ with args ({testobj}, -1, 'info\\ntext') {{}}\n"
                "called hori sizer.Add with args MockStaticText (0, 240, 5)\n"
                "called  sizer.Add with args MockBoxSizer (0, 8432, 5)\n"
                "called StaticLine.__init__ with args"
                f" ({testobj}, -1) {{'size': (20, -1), 'style': 4}}\n"
                "called  sizer.Add with args MockStaticLine (0, 8288, 5)\n")

    def test_add_okcancel_buttonbox(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.add_okcancel_buttonbox
        """
        monkeypatch.setattr(testee.wx.Dialog, 'CreateButtonSizer',
                            mockwx.MockDialog.CreateButtonSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_okcancel_buttonbox()
        assert capsys.readouterr().out == (
                "called dialog.CreateButtonSizer with args (20,)\n"
                "called BoxSizer.__init__ with args ()\n"
                "called  sizer.Add with args MockBoxSizer (0, 240, 5)\n")

    def test_finish_display(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.finish_display
        """
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.finish_display()
        assert capsys.readouterr().out == ("called dialog.SetSizer with args ( sizer,)\n"
                                           "called dialog.SetAutoLayout with args (True,)\n"
                                           f"called  sizer.Fit with args ({testobj},)\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.accept
        """
        def mock_confirm():
            print('called SettOptionsDialog.confirm')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == ("called SettOptionsDialog.confirm\n")

    def test_read_listbox_data(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.read_listbox_data
        """
        elb = mockwx.MockEditableListBox()
        assert capsys.readouterr().out == "called EditableListBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.read_listbox_data(elb) == ['strings', 'from', 'elb']
        assert capsys.readouterr().out == "called EditableListBox.GetStrings\n"


class TestLoginBoxGui:
    """unittests for wxgui.LoginBoxGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.LoginBoxGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called LoginBoxGui.__init__ with args', args)
        monkeypatch.setattr(testee.LoginBoxGui, '__init__', mock_init)
        testobj = testee.LoginBoxGui()
        assert capsys.readouterr().out == 'called LoginBoxGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for LoginBoxGui.__init__
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'GridBagSizer', mockwx.MockGridSizer)
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        parent = types.SimpleNamespace(gui='LoginBoxGui')
        testobj = testee.LoginBoxGui('master', parent)
        assert isinstance(testobj.vbox, testee.wx.BoxSizer)
        assert testobj.row == -1
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called GridSizer.__init__ with args () {}\n"
                "called vert sizer.Add with args MockGridSizer (0, 240, 4)\n")

    def test_add_textinput_line(self, monkeypatch, capsys):
        """unittest for LoginBoxGui.add_textinput_line
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj.row = 0
        result = testobj.add_textinput_line('text')
        assert isinstance(result, testee.wx.TextCtrl)
        assert testobj.row == 1
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'Userid'}}\n"
                "called GridSizer.Add with args MockStaticText ((1, 0),) {'flag': 2048}\n"
                f"called TextCtrl.__init__ with args ({testobj},) {{'size': (120, -1)}}\n"
                "called GridSizer.Add with args MockTextCtrl"
                " ((1, 1),) {'flag': 16, 'border': 2}\n")
        testobj.row = 0
        result = testobj.add_textinput_line('text', hide=True)
        assert isinstance(result, testee.wx.TextCtrl)
        assert testobj.row == 1
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'Userid'}}\n"
                "called GridSizer.Add with args MockStaticText ((1, 0),) {'flag': 2048}\n"
                "called TextCtrl.__init__ with args"
                f" ({testobj},) {{'size': (120, -1), 'style': 2048}}\n"
                "called GridSizer.Add with args"
                " MockTextCtrl ((1, 1),) {'flag': 16, 'border': 2}\n")

    def test_add_okcancel_buttonbox(self, monkeypatch, capsys):
        """unittest for LoginBoxGui.add_okcancel_buttonbox
        """
        monkeypatch.setattr(testee.wx.Dialog, 'CreateButtonSizer',
                            mockwx.MockDialog.CreateButtonSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_okcancel_buttonbox()
        assert capsys.readouterr().out == (
                "called dialog.CreateButtonSizer with args (20,)\n"
                "called BoxSizer.__init__ with args ()\n"
                "called  sizer.Add with args MockBoxSizer (0, 256)\n")

    def test_finish_display(self, monkeypatch, capsys):
        """unittest for LoginBoxGui.finish_display
        """
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.finish_display()
        assert capsys.readouterr().out == ("called dialog.SetSizer with args ( sizer,)\n"
                                           "called dialog.SetAutoLayout with args (True,)\n"
                                           f"called  sizer.Fit with args ({testobj},)\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for LoginBoxGui.accept
        """
        def mock_confirm():
            print('called SettOptionsDialog.confirm')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == ("called SettOptionsDialog.confirm\n")

    def test_get_textinput_value(self, monkeypatch, capsys):
        """unittest for LoginBoxGui.get_textinput_value
        """
        field = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textinput_value(field) == "value from textctrl"
        assert capsys.readouterr().out == ("called text.GetValue\n")
