"""unittests for ./probreg/gui_qt.py
"""
import pytest
import types
import copy
from mockgui import mockqtwidgets as mockqtw
from probreg import qtgui as testee
from output_fixtures import expected_output


class MockAppBase:
    """stub for main.MainWindow
    """
    def __init__(self):
        self.use_rt = False


class MockBook:
    """stub for main.MainWindow.book
    """
    def __init__(self):
        self.parent = MockAppBase()


class MockPage:
    """stub for main.Page
    """
    def __init__(self):
        print('called Page.__init__')
        self.book = MockBook()
        self.appbase = self.book.parent
    def sort_items(self):
        "dummy"
    def select_items(self):
        "dummy"
    def goto_actie(self):
        "dummy"
    def goto_prev(self):
        "dummy"
    def goto_next(self):
        "dummy"
    def archiveer(self):
        "dummy"
    def nieuwp(self):
        "dummy"
    def on_text(self):
        "dummy"
    def savep(self):
        "dummy"
    def savepgo(self):
        "dummy"
    def restorep(self):
        "dummy"
    def breekaf(self):
        "dummy"


class MockGui:
    """stub for gui_qt.MainGui
    """
    def __init__(self, *args):
        print('called Gui.__init__ with args', args)


class MockEditorPanel:
    """stub for gui.EditorPanel
    """
    def __init__(self, text):
        self._text = text

    def set_contents(self, data):
        print(f"called EditorWidget.set_contents with arg '{data}'")
        self._text = data

    def get_contents(self):
        print('called EditorWidget.get_contents')
        return self._text

    def setReadOnly(self, value):
        print(f'called EditorWidget.setReadOnly with arg {value}')

    def font_changed(self, value):
        print(f'called EditorWidget.font_changed with arg {value}')

    def font(self):
        print('called EditorWidget.font')
        return 'font'

    # dummy methods, needed for callback reference only
    def text_family(self):
        "stub"
    def text_size(self):
        "stub"


def test_show_message(monkeypatch, capsys):
    """unittest for gui_qt.show_message
    """
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    win = MockGui()
    assert capsys.readouterr().out == "called Gui.__init__ with args ()\n"
    testee.shared.app_title = 'xxx'
    testee.show_message(win, 'Message')
    assert capsys.readouterr().out == (
            f"called MessageBox.information with args `{win}` `xxx` `Message`\n")
    testee.show_message(win, 'Message', 'yyy')
    assert capsys.readouterr().out == (
            f"called MessageBox.information with args `{win}` `yyy` `Message`\n")


def test_show_error(monkeypatch, capsys):
    """unittest for gui_qt.show_message
    """
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    win = MockGui()
    assert capsys.readouterr().out == "called Gui.__init__ with args ()\n"
    testee.shared.app_title = 'xxx'
    testee.show_error(win, 'Message')
    assert capsys.readouterr().out == (
            f"called MessageBox.critical with args `{win}` `xxx` `Message`\n")
    testee.show_error(win, 'Message', 'yyy')
    assert capsys.readouterr().out == (
            f"called MessageBox.critical with args `{win}` `yyy` `Message`\n")


def test_get_open_filename(monkeypatch, capsys):
    """unittest for gui_qt.get_open_filename
    """
    monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
    monkeypatch.setattr(testee.pathlib.Path, 'cwd', testee.pathlib.Path.home)
    win = MockGui()
    assert capsys.readouterr().out == "called Gui.__init__ with args ()\n"
    testee.shared.app_title = 'xxx'
    assert testee.get_open_filename(win) == ''
    assert capsys.readouterr().out == (
            f"called FileDialog.getOpenFileName with args {win} ('xxx - kies een gegevensbestand',"
            f" '{testee.pathlib.Path.home()}', 'XML files (*.xml);;all files (*.*)') {{}}\n")
    assert testee.get_open_filename(win, start='qqq') == ""
    assert capsys.readouterr().out == (
            f"called FileDialog.getOpenFileName with args {win} ('xxx - kies een gegevensbestand',"
            f" 'qqq', 'XML files (*.xml);;all files (*.*)') {{}}\n")


def test_get_save_filename(monkeypatch, capsys):
    """unittest for gui_qt.get_save_filename
    """
    monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
    monkeypatch.setattr(testee.pathlib.Path, 'cwd', testee.pathlib.Path.home)
    win = MockGui()
    assert capsys.readouterr().out == "called Gui.__init__ with args ()\n"
    testee.shared.app_title = 'xxx'
    assert testee.get_save_filename(win) == ''
    assert capsys.readouterr().out == (
            f"called FileDialog.getSaveFileName with args {win} ('xxx - nieuw gegevensbestand',"
            f" '{testee.pathlib.Path.home()}', 'XML files (*.xml);;all files (*.*)') {{}}\n")
    assert testee.get_save_filename(win, start='qqq') == ""
    assert capsys.readouterr().out == (
            f"called FileDialog.getSaveFileName with args {win} ('xxx - nieuw gegevensbestand',"
            f" 'qqq', 'XML files (*.xml);;all files (*.*)') {{}}\n")


def test_get_choice_item(monkeypatch, capsys):
    """unittest for gui_qt.get_choice_item
    """
    def mock_get(*args, **kwargs):
        print('called InputDialog.getItem with args', args, kwargs)
        return 'aaa', True
    monkeypatch.setattr(testee.qtw, 'QInputDialog', mockqtw.MockInputDialog)
    win = MockGui()
    assert capsys.readouterr().out == "called Gui.__init__ with args ()\n"
    assert testee.get_choice_item(win, 'caption', ['choices']) == ""
    assert capsys.readouterr().out == (
            f"called InputDialog.getItem with args {win} ('xxx', 'caption', ['choices'])"
            " {'current': 0, 'editable': False}\n")
    monkeypatch.setattr(mockqtw.MockInputDialog, 'getItem', mock_get)
    assert testee.get_choice_item(win, 'caption', ['choices'], current=1) == "aaa"
    assert capsys.readouterr().out == (
            f"called InputDialog.getItem with args ({win}, 'xxx', 'caption', ['choices'])"
            " {'current': 1, 'editable': False}\n")


def test_ask_question(monkeypatch, capsys):
    """unittest for gui_qt.ask_cancel_question
    """
    def mock_ask(parent, caption, message, buttons):
        print(f'called MessageBox.question with args `{parent}` `{caption}` `{message}` `{buttons}`')
        return mockqtw.MockMessageBox.StandardButton.Yes
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    win = MockGui()
    assert capsys.readouterr().out == "called Gui.__init__ with args ()\n"
    testee.shared.app_title = 'xxx'
    assert not testee.ask_question(win, 'question')
    assert capsys.readouterr().out == ("called MessageBox.question with args"
                                       f" `{win}` `xxx` `question` `12`\n")
    monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_ask)
    assert testee.ask_question(win, 'question')
    assert capsys.readouterr().out == ("called MessageBox.question with args"
                                       f" `{win}` `xxx` `question` `12`\n")


def test_ask_cancel_question(monkeypatch, capsys):
    """unittest for gui_qt.ask_cancel_question
    """
    def mock_ask(parent, caption, message, buttons):
        print(f'called MessageBox.question with args `{parent}` `{caption}` `{message}` `{buttons}`')
        return mockqtw.MockMessageBox.StandardButton.Yes
    def mock_ask_2(parent, caption, message, buttons):
        print(f'called MessageBox.question with args `{parent}` `{caption}` `{message}` `{buttons}`')
        return mockqtw.MockMessageBox.StandardButton.Cancel
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    win = MockGui()
    assert capsys.readouterr().out == "called Gui.__init__ with args ()\n"
    testee.shared.app_title = 'xxx'
    assert testee.ask_cancel_question(win, 'question') == (False, False)
    assert capsys.readouterr().out == ("called MessageBox.question with args"
                                       f" `{win}` `xxx` `question` `14`\n")
    monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_ask)
    assert testee.ask_cancel_question(win, 'question') == (True, False)
    assert capsys.readouterr().out == ("called MessageBox.question with args"
                                       f" `{win}` `xxx` `question` `14`\n")
    monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_ask_2)
    assert testee.ask_cancel_question(win, 'question') == (False, True)
    assert capsys.readouterr().out == ("called MessageBox.question with args"
                                       f" `{win}` `xxx` `question` `14`\n")


def test_show_dialog(monkeypatch, capsys):
    """unittest for qtgui.show_dialog_new
    """
    def mock_exec():
        print('called Dialog.exec')
        return testee.qtw.QDialog.DialogCode.Rejected
    def mock_exec_2():
        print('called Dialog.exec')
        return testee.qtw.QDialog.DialogCode.Accepted
    dlg = types.SimpleNamespace(exec=mock_exec)
    assert not testee.show_dialog(dlg)
    assert capsys.readouterr().out == "called Dialog.exec\n"
    dlg = types.SimpleNamespace(exec=mock_exec_2)
    assert testee.show_dialog(dlg)
    assert capsys.readouterr().out == "called Dialog.exec\n"


class TestMainGui:
    """unittest for gui_qt.MainGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.MainGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called MainGui.__init__ with args', args)
        monkeypatch.setattr(testee.MainGui, '__init__', mock_init)
        testobj = testee.MainGui()
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for MainGui.__init__
        """
        master = MockAppBase()
        master.title = 'xxx'
        monkeypatch.setattr(testee.qtw, 'QApplication', mockqtw.MockApplication)
        monkeypatch.setattr(testee.qtw.QMainWindow, '__init__', mockqtw.MockMainWindow.__init__)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setWindowTitle',
                            mockqtw.MockMainWindow.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setWindowIcon',
                            mockqtw.MockMainWindow.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'move', mockqtw.MockMainWindow.move)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'resize', mockqtw.MockMainWindow.resize)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'statusBar', mockqtw.MockMainWindow.statusBar)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setCentralWidget',
                            mockqtw.MockMainWindow.setCentralWidget)
        monkeypatch.setattr(testee.gui, 'QIcon', mockqtw.MockIcon)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee, 'HERE', 'here')
        monkeypatch.setattr(testee, 'LIN', True)
        testobj = testee.MainGui(master)
        assert isinstance(testobj.app, testee.qtw.QApplication)
        assert isinstance(testobj.sbar, mockqtw.MockStatusBar)
        assert isinstance(testobj.statusmessage, testee.qtw.QLabel)
        assert isinstance(testobj.showuser, testee.qtw.QLabel)
        assert isinstance(testobj.pnl, testee.qtw.QFrame)
        assert testobj.toolbar is None
        assert capsys.readouterr().out == expected_output['maingui'].format(testobj=testobj)
        monkeypatch.setattr(testee, 'LIN', False)
        testobj = testee.MainGui(master)
        assert isinstance(testobj.app, testee.qtw.QApplication)
        assert isinstance(testobj.sbar, mockqtw.MockStatusBar)
        assert isinstance(testobj.statusmessage, testee.qtw.QLabel)
        assert isinstance(testobj.showuser, testee.qtw.QLabel)
        assert isinstance(testobj.pnl, testee.qtw.QFrame)
        assert testobj.toolbar is None
        assert capsys.readouterr().out == expected_output['maingui2'].format(testobj=testobj)

    def test_create_menu(self, monkeypatch, capsys, expected_output):
        """unittest for MainGui.create_menu
        """
        def mock_menubar():
            print('called MainGui.menuBar')
            return mockqtw.MockMenuBar()
        def mock_menudata():
            print('called AppBase.get_menu_data')
            return []
        def mock_menudata_2():
            print('called AppBase.get_menu_data')
            return [('top menu', [('xx', callback1, '', ''),
                                  ('yy', callback2, 'Ctrl+O', 'yadayada'),
                                  ('',),
                                  ('sub menu', [('zz', callback3, 'x', 'bladibla'),
                                                (),
                                                ('&Data', [])])])]
        # deze was bedoeld voor de tabmenus, maar dat gebruik ik hier niet meer
        # def mock_menudata_3():
        #     print('called AppBase.get_menu_data')
        #     return [('&View', [('xx', callback1, '', ''),
        #                        ('yy', callback2, '', '')])]
        def callback1():
            return 1
        def callback2():
            return 2
        def callback3():
            return 3
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.menuBar = mock_menubar
        testobj.master = types.SimpleNamespace(get_menu_data=mock_menudata, tabmenus=[])
        testobj.create_menu()
        assert not testobj.master.tabmenus
        assert capsys.readouterr().out == expected_output['mainmenu']
        testobj.master = types.SimpleNamespace(get_menu_data=mock_menudata_2, tabmenus=[])
        testobj.create_menu()
        assert not testobj.master.tabmenus
        assert capsys.readouterr().out == expected_output['mainmenu2'].format(
                callbacks=[callback1, callback2, callback3])
        # testobj.master = types.SimpleNamespace(get_menu_data=mock_menudata_3, tabmenus=[])
        # testobj.create_menu()
        # # assert len(testobj.master.tabmenus) == 2
        # # assert isinstance(testobj.master.tabmenus[0], mockqtw.MockAction)
        # # assert isinstance(testobj.master.tabmenus[1], mockqtw.MockAction)
        # assert capsys.readouterr().out == (
        #         "called MainGui.menuBar\ncalled MenuBar.__init__\ncalled AppBase.get_menu_data\n"
        #         "called MenuBar.addMenu with arg  &View\n"
        #         "called Menu.__init__ with args ('&View',)\n"
        #         "called Menu.addAction with args `xx` None\n"
        #         "called Action.__init__ with args ('xx', None)\n"
        #         f"called Signal.connect with args ({callback1},)\n"
        #         "called Menu.addAction with args `yy` None\n"
        #         "called Action.__init__ with args ('yy', None)\n"
        #         f"called Signal.connect with args ({callback2},)\n")

    def test_create_actions(self, monkeypatch, capsys):
        """unittest for MainGui.create_actions
        """
        monkeypatch.setattr(testee.gui, 'QShortcut', mockqtw.MockShortcut)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.create_actions([])
        assert capsys.readouterr().out == ""
        testobj.create_actions([('xxx', 'callback1'), ('yyy', 'callback2')])
        assert capsys.readouterr().out == (
                "called Shortcut.__init__ with args"
                f" ('xxx', {testobj}, 'callback1')\n"
                "called Shortcut.__init__ with args"
                f" ('yyy', {testobj}, 'callback2')\n")

    def test_get_bookwidget(self, monkeypatch, capsys):
        """unittest for MainGui.get_bookwidget
        """
        monkeypatch.setattr(testee.qtw, 'QTabWidget', mockqtw.MockTabWidget)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = 'panel'
        result = testobj.get_bookwidget()
        assert isinstance(result, testee.qtw.QTabWidget)
        assert result.sorter is None
        assert capsys.readouterr().out == (
                "called TabWidget.__init__\n"
                "called TabWidget.resize with args (300, 300)\n"
                f"called Signal.connect with args ({testobj.on_page_changing},)\n")

    def test_go(self, monkeypatch, capsys, expected_output):
        """unittest for MainGui.go
        """
        def mock_show():
            print('called MainGui.show')
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(exit_app=lambda: 'exit', book='book')
        testobj.pnl = mockqtw.MockFrame()
        testobj.bookwidget = mockqtw.MockTabWidget()
        testobj.app = mockqtw.MockApplication()
        assert capsys.readouterr().out == ("called Frame.__init__\ncalled TabWidget.__init__\n"
                                           "called Application.__init__\n")
        testobj.show = mock_show
        with pytest.raises(SystemExit):
            testobj.go()
        assert capsys.readouterr().out == (
                "called VBox.__init__\n"
                "called VBox.addWidget with arg 'book'\n"
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called PushButton.__init__ with args ('&Quit', {testobj.pnl}) {{}}\n"
                f"called Signal.connect with args ({testobj.master.exit_app},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n"
                "called Frame.setLayout with arg MockVBoxLayout\n"
                "called MainGui.show\n"
                "called Application.exec\n")

    def test_refresh_page(self, monkeypatch, capsys):
        """unittest for MainGui.refresh_page
        """
        def mock_change(**kwargs):
            print('called mainGui.on_page_changing with args', kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.on_page_changing = mock_change
        testobj.refresh_page()
        assert capsys.readouterr().out == (
                "called mainGui.on_page_changing with args {'newtabnum': 0}\n")

    def test_on_page_changing(self, monkeypatch, capsys):
        """unittest for MainGui.on_page_changing
        """
        def mock_get(*args):
            print('called Page.get_list_row with args', args)
            return 'item'
        def mock_set(*args):
            print('called Page.set_list_row with args', args)
        def mock_get_page(arg):
            print(f'called MainGui.get_page with arg {arg}')
            return 0
        def mock_enable(value):
            print(f'called MainWindow.enable_all_other_tabs with arg {value}')
        def mock_set_tabfocus(item):
            print(f'called MainGui.set_tabfocus with arg {item}')
        class MockPage:
            "stub"
            def __init__(self):
                self.gui = types.SimpleNamespace(get_list_row=mock_get, set_list_row=mock_set)
            def vulp(self):
                print('called Page.vulp')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(
                book=types.SimpleNamespace(pages=[MockPage(), MockPage(), MockPage(), MockPage(),
                                                  MockPage(), MockPage(), MockPage()]))
        testobj.master.book.pages[0].p0list = 'page0list'
        testobj.master.book.pages[-1].progress_list = 'page6list'
        testobj.get_page = mock_get_page
        testobj.master.enable_all_other_tabs = mock_enable
        testobj.set_tabfocus = mock_set_tabfocus
        testobj.LIN = True
        testobj.master.book.current_tab = -1
        testobj.master.origbook = copy.copy(testobj.master.book)
        testobj.on_page_changing()
        assert capsys.readouterr().out == (
                f"called MainGui.get_page with arg {testobj.master.origbook}\n")
        testobj.on_page_changing(0)
        assert capsys.readouterr().out == (
                "called MainWindow.enable_all_other_tabs with arg True\n"
                "called Page.get_list_row with args ('page0list',)\n"
                "called Page.vulp\n"
                "called Page.set_list_row with args ('page0list', 'item')\n"
                "called MainGui.set_tabfocus with arg 0\n")

        testobj.master.book.current_tab = 1
        testobj.on_page_changing(0)
        assert capsys.readouterr().out == (
                "called MainWindow.enable_all_other_tabs with arg True\n"
                "called Page.vulp\n"
                "called MainGui.set_tabfocus with arg 0\n")

        testobj.master.book.current_tab = 0
        testobj.on_page_changing(0)
        assert capsys.readouterr().out == (
                "called MainWindow.enable_all_other_tabs with arg True\n"
                "called Page.get_list_row with args ('page0list',)\n"
                "called Page.vulp\n"
                "called Page.set_list_row with args ('page0list', 'item')\n"
                "called MainGui.set_tabfocus with arg 0\n")

        testobj.master.book.current_tab = 1
        testobj.on_page_changing(2)
        assert capsys.readouterr().out == (
                "called MainWindow.enable_all_other_tabs with arg True\n"
                "called Page.vulp\n"
                "called MainGui.set_tabfocus with arg 2\n")

        testobj.master.book.current_tab = 0
        testobj.on_page_changing(6)
        assert capsys.readouterr().out == (
                "called MainWindow.enable_all_other_tabs with arg True\n"
                "called Page.vulp\n"
                "called MainGui.set_tabfocus with arg 6\n")

        testobj.master.book.current_tab = 6
        testobj.on_page_changing(6)
        assert capsys.readouterr().out == (
                "called MainWindow.enable_all_other_tabs with arg True\n"
                "called Page.get_list_row with args ('page6list',)\n"
                "called Page.vulp\n"
                "called Page.set_list_row with args ('page6list', 'item')\n"
                "called MainGui.set_tabfocus with arg 6\n")

    # def test_enable_navigation_via_menu(self, monkeypatch, capsys):
    #     """unittest for MainGui.enable_navigation_via_menu
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.master = types.SimpleNamespace()
    #     action1 = mockqtw.MockAction()
    #     action2 = mockqtw.MockAction()
    #     testobj.master.tabmenus = [action1, action2]
    #     assert capsys.readouterr().out == ("called Action.__init__ with args ()\n"
    #                                        "called Action.__init__ with args ()\n")
    #     testobj.enable_navigation_via_menu(0, True)
    #     assert capsys.readouterr().out == "called Action.setEnabled with arg `True`\n"
    #     testobj.enable_navigation_via_menu(1, False)
    #     assert capsys.readouterr().out == "called Action.setEnabled with arg `False`\n"

    def test_add_book_tab(self, monkeypatch, capsys):
        """unittest for MainGui.add_book_tab
        """
        def mock_doe():
            print('called PageGui.doelayout')
        testobj = self.setup_testobj(monkeypatch, capsys)
        bookwidget = mockqtw.MockTabWidget()
        assert capsys.readouterr().out == "called TabWidget.__init__\n"
        tab = types.SimpleNamespace(gui=types.SimpleNamespace(doelayout=mock_doe))
        testobj.add_book_tab(bookwidget, tab, 'title')
        assert capsys.readouterr().out == f"called TabWidget.addTab with args `{tab.gui}` `title`\n"

    def test_enable_tab(self, monkeypatch, capsys):
        """unittest for MainGui.enable_tab
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        bookwidget = mockqtw.MockTabWidget()
        testobj.enable_tab(bookwidget, 'tabno', 'state')
        assert capsys.readouterr().out == (
                "called TabWidget.__init__\n"
                "called TabWidget.setTabEnabled with args ('tabno', 'state')\n")

    def test_get_tab_count(self, monkeypatch, capsys):
        """unittest for MainGui.get_tab_count
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        bookwidget = mockqtw.MockTabWidget()
        assert testobj.get_tab_count(bookwidget) == "number of tabs"
        assert capsys.readouterr().out == ("called TabWidget.__init__\n"
                                           "called TabWidget.count\n")

    def test_exit(self, monkeypatch, capsys):
        """unittest for MainGui.exit
        """
        def mock_close():
            print('called MainGui.close')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.close = mock_close
        testobj.exit()
        assert capsys.readouterr().out == ("called MainGui.close\n")

    def test_close(self, monkeypatch, capsys):
        """unittest for MainGui.close
        """
        def mock_save():
            print('called Main.save_startitem_on_exit')
        monkeypatch.setattr(testee.qtw.QWidget, 'close', mockqtw.MockWidget.close)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(save_startitem_on_exit=mock_save)
        testobj.close()
        assert capsys.readouterr().out == ("called Main.save_startitem_on_exit\n"
                                           "called Widget.close\n")

    def test_set_page(self, monkeypatch, capsys):
        """unittest for MainGui.set_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        bookwidget = mockqtw.MockTabWidget()
        assert capsys.readouterr().out == "called TabWidget.__init__\n"
        testobj.set_page(bookwidget, 'num')
        assert capsys.readouterr().out == "called TabWidget.setCurrentIndex with arg `num`\n"

    def test_set_page_title(self, monkeypatch, capsys):
        """unittest for MainGui.set_page_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        bookwidget = mockqtw.MockTabWidget()
        assert capsys.readouterr().out == "called TabWidget.__init__\n"
        testobj.set_page_title(bookwidget, 'num', 'text')
        assert capsys.readouterr().out == "called TabWidget.setTabText with args ('num', 'text')\n"

    def test_get_page(self, monkeypatch, capsys):
        """unittest for MainGui.get_page
        """
        def mock_index():
            print('called Book.currentIndex')
            return 1
        testobj = self.setup_testobj(monkeypatch, capsys)
        bookwidget = mockqtw.MockTabWidget()
        bookwidget.currentIndex = mock_index
        assert capsys.readouterr().out == "called TabWidget.__init__\n"
        assert testobj.get_page(bookwidget) == 1
        assert capsys.readouterr().out == "called Book.currentIndex\n"

    def test_set_tabfocus(self, monkeypatch, capsys):
        """unittest for MainGui.set_tabfocus
        """
        def mock_get(arg):
            print(f'called Page.get_focus_widget_for_tab with arg {arg}')
            return widget
        def mock_set():
            print('called widget.setFocus')
        testobj = self.setup_testobj(monkeypatch, capsys)
        Page0 = types.SimpleNamespace(gui=types.SimpleNamespace(p0list=mockqtw.MockListBox()))
        Page1 = types.SimpleNamespace(gui=types.SimpleNamespace(proc_entry=mockqtw.MockLineEdit()))
        Page2 = types.SimpleNamespace(gui=types.SimpleNamespace(text1=mockqtw.MockEditorWidget()))
        Page3 = types.SimpleNamespace(gui=types.SimpleNamespace(text1=mockqtw.MockEditorWidget()))
        Page4 = types.SimpleNamespace(gui=types.SimpleNamespace(text1=mockqtw.MockEditorWidget()))
        Page5 = types.SimpleNamespace(gui=types.SimpleNamespace(text1=mockqtw.MockEditorWidget()))
        Page6 = types.SimpleNamespace(gui=types.SimpleNamespace(progress_list=mockqtw.MockListBox()))
        assert capsys.readouterr().out == ("called List.__init__\n"
                                           "called LineEdit.__init__ with args ()\n"
                                           "called Editor.__init__\ncalled Editor.__init__\n"
                                           "called Editor.__init__\ncalled Editor.__init__\n"
                                           "called List.__init__\n")
        testobj.master = types.SimpleNamespace(book=types.SimpleNamespace())
        testobj.master.use_text_panels = True
        testobj.master.book.pages = [Page0, Page1, Page2, Page3, Page4, Page5, Page6]
        widget = types.SimpleNamespace(setFocus=mock_set)
        testobj.master.get_focus_widget_for_tab = mock_get
        testobj.set_tabfocus(5)
        assert capsys.readouterr().out == ("called Page.get_focus_widget_for_tab with arg 5\n"
                                           "called widget.setFocus\n")
        testobj.master.use_text_panels = False
        testobj.master.book.pages = [Page0, Page1, Page6]
        testobj.set_tabfocus(1)
        assert capsys.readouterr().out == ("called Page.get_focus_widget_for_tab with arg 1\n"
                                           "called widget.setFocus\n")

    # def test_print_(self, monkeypatch, capsys):
    #     """unittest for MainGui.print_
    #     """
    #     def mock_get_choice(*args):
    #         print('called get_choice_item with args', args)
    #         return args[2][0]
    #     def mock_get_choice_2(*args):
    #         print('called get_choice_item with args', args)
    #         return args[2][1]
    #     def mock_scherm():
    #         print('called Main.print_scherm')
    #     def mock_actie():
    #         print('called Main.print_actie')
    #     monkeypatch.setattr(testee, 'get_choice_item', mock_get_choice)
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.master = types.SimpleNamespace(print_scherm=mock_scherm, print_actie=mock_actie)
    #     testobj.print_()
    #     assert capsys.readouterr().out == (
    #             "called get_choice_item with args"
    #             f" ({testobj}, 'Wat wil je afdrukken?', ['huidig scherm', 'huidige actie'])\n"
    #             "called Main.print_scherm\n")
    #     monkeypatch.setattr(testee, 'get_choice_item', mock_get_choice_2)
    #     testobj.print_()
    #     assert capsys.readouterr().out == (
    #             "called get_choice_item with args"
    #             f" ({testobj}, 'Wat wil je afdrukken?', ['huidig scherm', 'huidige actie'])\n"
    #             "called Main.print_actie\n")

    def test_preview(self, monkeypatch, capsys):
        """unittest for MainGui.preview
        """
        monkeypatch.setattr(testee.qtp, 'QPrintPreviewDialog', mockqtw.MockPrintPreviewDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.afdrukken = lambda: 'print'
        testobj.preview()
        assert isinstance(testobj.print_dlg, testee.qtp.QPrintPreviewDialog)
        assert capsys.readouterr().out == (
                f"called PrintPreviewDialog.__init__ with args ({testobj},)\n"
                f"called Signal.connect with args ({testobj.afdrukken},)\n"
                "called PrintPreviewDialog.exec\n")

    def test_afdrukken(self, monkeypatch, capsys):
        """unittest for MainGui.afdrukken
        """
        class MockTemplate:
            "stub"
            def __init__(self, *args, **kwargs):
                print('called Template.__init__ with args', args, kwargs)
            def render(self, *args, **kwargs):
                print('called Template.render with args', args, kwargs)
        def mock_set(name):
            print(f'called Printer.setOutputFileName with arg {name}')
        monkeypatch.setattr(testee.gui, 'QTextDocument', mockqtw.MockTextDocument)
        monkeypatch.setattr(testee, 'Template', MockTemplate)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(hdr='xxx', printdict={})
        testobj.print_dlg = mockqtw.MockPrintPreviewDialog()
        printer = types.SimpleNamespace(setOutputFileName=mock_set)
        testobj.afdrukken(printer)
        # assert testobj.css == ''
        # assert testobj.master.printdict['css'] == ''
        assert testobj.master.printdict['hdr'] == 'xxx'
        assert capsys.readouterr().out == (
                "called PrintPreviewDialog.__init__ with args ()\n"
                f"called TextDocument.__init__ with args ({testobj},)\n"
                f"called Template.__init__ with args () {{'filename': '{testee.HERE}/actie.tpl'}}\n"
                "called Template.render with args () {'hdr': 'xxx'}\n"
                "called TextDocument.setHtml with arg 'None'\n"
                "called Printer.setOutputFileName with arg xxx\n"
                f"called TextDocument.print with arg {printer}\n"
                "called PrintPreviewDialog.done with arg True\n")

    def test_enable_settingsmenu(self, monkeypatch, capsys):
        """unittest for MainGui.enable_settingsmenu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.settingsmenu = mockqtw.MockAction()
        assert capsys.readouterr().out == "called Action.__init__ with args ()\n"
        testobj.master = types.SimpleNamespace(is_admin=True)
        testobj.enable_settingsmenu()
        assert capsys.readouterr().out == "called Action.setEnabled with arg `True`\n"

    def test_set_statusmessage(self, monkeypatch, capsys):
        """unittest for MainGui.set_statusmessage
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.statusmessage = mockqtw.MockLabel()
        assert capsys.readouterr().out == "called Label.__init__\n"
        testobj.set_statusmessage()
        assert capsys.readouterr().out == "called Label.setText with arg ``\n"
        testobj.set_statusmessage('xxx')
        assert capsys.readouterr().out == "called Label.setText with arg `xxx`\n"

    def test_set_window_title(self, monkeypatch, capsys):
        """unittest for MainGui.set_window_title
        """
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setWindowTitle',
                            mockqtw.MockMainWindow.setWindowTitle)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_window_title('text')
        assert capsys.readouterr().out == "called MainWindow.setWindowTitle with arg `text`\n"

    def test_show_username(self, monkeypatch, capsys):
        """unittest for MainGui.show_username
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.showuser = mockqtw.MockLabel()
        assert capsys.readouterr().out == "called Label.__init__\n"
        testobj.show_username('msg')
        assert capsys.readouterr().out == "called Label.setText with arg `msg`\n"


class TestPageGui:
    """unittest for gui_qt.PageGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.PageGui object

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
        testobj.book = MockBook()
        testobj.master = MockPage()
        testobj.appbase = testobj.book.parent
        assert capsys.readouterr().out == ('called PageGui.__init__ with args ()\n'
                                           'called Page.__init__\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for PageGui.__init__
        """
        monkeypatch.setattr(testee.qtw.QFrame, '__init__', mockqtw.MockFrame.__init__)
        parent = MockBook()
        master = MockPage()
        assert capsys.readouterr().out == 'called Page.__init__\n'
        # master.is_text_page = False
        testobj = testee.PageGui(parent, master)
        assert testobj.book == parent
        assert testobj.master == master
        assert testobj.appbase == parent.parent
        assert capsys.readouterr().out == "called Frame.__init__\n"
        # master.is_text_page = True
        # testobj = testee.PageGui(parent, master)
        # assert testobj.book == parent
        # assert testobj.master == master
        # assert testobj.appbase == parent.parent
        # assert capsys.readouterr().out == ("called Frame.__init__\n"

    def test_start_display(self, monkeypatch, capsys):
        """unittest for PageGui.start_display
        """
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw.QFrame, 'setLayout', mockqtw.MockFrame.setLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert isinstance(testobj.start_display(), testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == ("called VBox.__init__\n"
                                           "called Frame.setLayout with arg MockVBoxLayout\n")

    def test_create_text_field(self, monkeypatch, capsys):
        """unittest for PageGui.create_text_field
        """
        def callback():
            "stub for reference"
        monkeypatch.setattr(testee, 'EditorPanel', mockqtw.MockEditorWidget)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.create_text_field(sizer, 'width', 'height', callback)
        assert isinstance(result, testee.EditorPanel)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                f"called Editor.__init__ with args ({testobj},)\n"
                "called Editor.resize with args ('width', 'height')\n"
                f"called Signal.connect with args ({callback},)\n"
                "called HBox.addWidget with arg MockEditorWidget\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_create_toolbar(self, monkeypatch, capsys, expected_output):
        """unittest for PageGui.create_toolbar
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QToolBar', mockqtw.MockToolBar)
        monkeypatch.setattr(testee.core, 'QSize', mockqtw.MockSize)
        monkeypatch.setattr(mockqtw.MockFontComboBox, 'currentTextChanged',
                            {str: mockqtw.MockSignal()})
        assert capsys.readouterr().out == "called Signal.__init__\n"
        monkeypatch.setattr(testee.qtw, 'QFontComboBox', mockqtw.MockFontComboBox)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.gui, 'QFontDatabase',
                            types.SimpleNamespace(standardSizes=lambda: [10, 12, 20]))
        monkeypatch.setattr(testee.gui, 'QAction', mockqtw.MockAction)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.actiondict = {}
        sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        textfield = MockEditorPanel('text')  # mockqtw.MockEditorWidget()
        textfield.actiondict = {}
        result = testobj.create_toolbar(sizer, textfield, [])
        assert isinstance(result, testee.qtw.QToolBar)
        assert isinstance(testobj.combo_font, testee.qtw.QFontComboBox)
        assert isinstance(testobj.combo_size, testee.qtw.QComboBox)
        assert not textfield.actiondict
        assert capsys.readouterr().out == expected_output['pagetoolbar'].format(testobj=testobj,
                                                                                textfield=textfield)

        testobj.callback1 = lambda: 1
        testobj.callback2 = lambda: 2
        testobj.callback3 = lambda: 3
        data = [('xxx', 'y,z', 'x.ico', 'about xxx', testobj.callback1, testobj.callback2),
                ('yyy', '', '', '', testobj.callback3),
                (),
                ('b', 'b', '', 'Toggle B', testobj.callback1),
                ('i', 'i', '', 'Toggle I', testobj.callback1),
                ('u', 'u', '', 'Toggle U', testobj.callback1),
                ('s', 's', '', 'Toggle S', testobj.callback1),
                ('z', 'z', '', 'Toggle Z', testobj.callback1)]
        result = testobj.create_toolbar(sizer, textfield, data)
        assert isinstance(result, testee.qtw.QToolBar)
        assert isinstance(testobj.combo_font, testee.qtw.QFontComboBox)
        assert isinstance(testobj.combo_size, testee.qtw.QComboBox)
        assert len(textfield.actiondict) == 5
        assert list(textfield.actiondict.keys()) == ['b', 'i', 'u', 's', 'z']
        for x in testobj.actiondict.values():
            assert isinstance(x, testee.gui.QAction)
        assert capsys.readouterr().out == expected_output['pagetoolbar2'].format(testobj=testobj,
                                                                                textfield=textfield)

    def test_create_buttons(self, monkeypatch, capsys):
        """unittest for PageGui.create_buttons
        """
        def callback1():
            "just for reference"
        def callback2():
            "just for reference"
        def mock_add(*args):
            print("called PageGui.add_keybind with args", args)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_keybind = mock_add
        result = testobj.create_buttons([('xx (aa)', callback1), ('yy', callback2)])
        assert isinstance(result[0], testee.qtw.QPushButton)
        assert isinstance(result[1], testee.qtw.QPushButton)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called PushButton.__init__ with args ('xx (aa)', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback1},)\n"
                f"called PageGui.add_keybind with args ('aa', {callback1})\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('yy', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback2},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")
        sizer = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        result = testobj.create_buttons([], sizer)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                "called HBox.addStretch\n"
                "called HBox.addLayout with arg MockHBoxLayout\n")

    def test_add_keybind(self, monkeypatch, capsys):
        """unittest for PageGui.add_keybind
        """
        def callback():
            "just for reference"
        monkeypatch.setattr(testee.gui, 'QShortcut', mockqtw.MockShortcut)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_keybind('keydef', callback)
        assert capsys.readouterr().out == (
                f"called Shortcut.__init__ with args ('keydef', {testobj}, {callback})\n")

    def test_reset_font(self, monkeypatch, capsys):
        """unittest for PageGui.reset_font
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_text = mockqtw.MockEditorWidget('progress')
        testobj.text1 = mockqtw.MockEditorWidget('text')
        assert capsys.readouterr().out == ("called Editor.__init__ with args ('progress',)\n"
                                           "called Editor.__init__ with args ('text',)\n")
        testobj.book.current_tab = 2
        testobj.reset_font()
        # hoe toon ik aan welke waarde win heeft?
        assert capsys.readouterr().out == (
                f"called Editor.setFontWeight with arg {testee.gui.QFont.Weight.Normal}\n"
                "called Editor.setFontItalic with arg False\n"
                "called Editor.setFontUnderline with arg False\n"
                "called Editor.setFontFamily with arg 'font family'\n"
                "called Editor.setFontPointSize with arg '12pt'\n")
        testobj.book.current_tab = 6
        testobj.reset_font()
        assert capsys.readouterr().out == (
                f"called Editor.setFontWeight with arg {testee.gui.QFont.Weight.Normal}\n"
                "called Editor.setFontItalic with arg False\n"
                "called Editor.setFontUnderline with arg False\n"
                "called Editor.setFontFamily with arg 'font family'\n"
                "called Editor.setFontPointSize with arg '12pt'\n")

    def test_enable_widget(self, monkeypatch, capsys):
        """unittest for PageGui.enable_widget
        """
        widget = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.enable_widget(widget, 'state')
        assert capsys.readouterr().out == ("called Widget.setEnabled with arg state\n")

    def test_move_cursor_to_end(self, monkeypatch, capsys):
        """unittest for PageGui.move_cursor_to_end
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        text1 = mockqtw.MockEditorWidget()
        testobj.move_cursor_to_end(text1)
        assert capsys.readouterr().out == (
                "called Editor.__init__\n"
                f"called Editor.moveCursor with args ({testee.gui.QTextCursor.MoveOperation.End!r},"
                f" {testee.gui.QTextCursor.MoveMode.MoveAnchor!r})\n")

    def test_set_textarea_contents(self, monkeypatch, capsys):
        """unittest for PageGui.set_textarea_contents
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        text1 = MockEditorPanel('')
        testobj.set_textarea_contents(text1, 'data')
        assert capsys.readouterr().out == "called EditorWidget.set_contents with arg 'data'\n"

    def test_get_textarea_contents(self, monkeypatch, capsys):
        """unittest for PageGui.get_textarea_contents
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        text1 = MockEditorPanel('text')
        assert testobj.get_textarea_contents(text1) == "text"
        assert capsys.readouterr().out == ("called EditorWidget.get_contents\n")

    def test_enable_toolbar(self, monkeypatch, capsys):
        """unittest for PageGui.enable_toolbar
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        toolbar = mockqtw.MockToolBar()
        assert capsys.readouterr().out == "called ToolBar.__init__\n"
        testobj.enable_toolbar(toolbar, True)
        assert capsys.readouterr().out == "called ToolBar.setEnabled with arg True\n"

    def test_set_text_readonly(self, monkeypatch, capsys):
        """unittest for PageGui.set_text_readonly
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        text1 = MockEditorPanel('')
        testobj.set_text_readonly(text1, True)
        assert capsys.readouterr().out == ("called EditorWidget.setReadOnly with arg True\n")

    def test_is_enabled(self, monkeypatch, capsys):
        """unittest for PageGui.is_enabled
        """
        widget = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.is_enabled(widget) == "is enabled"
        assert capsys.readouterr().out == "called Widget.isEnabled\n"

    def test_set_focus_to_field(self, monkeypatch, capsys):
        """unittest for PageGui.set_focus_to_field
        """
        widget = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus_to_field(widget)
        assert capsys.readouterr().out == "called Widget.setFocus\n"


class TestEditorPanel:
    """unittest for gui_qt.EditorPanel
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.EditorPanel object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called EditorPanel.__init__ with args', args)
        monkeypatch.setattr(testee.EditorPanel, '__init__', mock_init)
        parent = MockPage()
        testobj = testee.EditorPanel(parent)
        testobj.parent = parent
        testobj.appbase = parent.book.parent
        assert capsys.readouterr().out == ('called Page.__init__\n'
                                           f'called EditorPanel.__init__ with args ({parent},)\n')
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for EditorPanel.__init__
        """
        def mock_tabsize(arg):
            print(f"called shared.tabsize with arg '{arg}'")
            return 'tabsize'
        monkeypatch.setattr(testee.qtw.QTextEdit, '__init__', mockqtw.MockEditorWidget.__init__)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'setAcceptRichText',
                            mockqtw.MockEditorWidget.setAcceptRichText)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'setAutoFormatting',
                            mockqtw.MockEditorWidget.setAutoFormatting)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'currentCharFormatChanged',
                            mockqtw.MockEditorWidget.currentCharFormatChanged)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'cursorPositionChanged',
                            mockqtw.MockEditorWidget.cursorPositionChanged)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'currentFont',
                            mockqtw.MockEditorWidget.currentFont)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'setTabStopDistance',
                            mockqtw.MockEditorWidget.setTabStopDistance)
        monkeypatch.setattr(testee.shared, 'tabsize', mock_tabsize)
        parent = MockPage()
        assert capsys.readouterr().out == 'called Page.__init__\n'
        testobj = testee.EditorPanel(parent)
        assert testobj.parent == parent
        assert testobj.appbase == parent.book.parent
        assert testobj.defaultfamily == 'fontfamily'
        assert testobj.defaultsize == 'fontsize'
        assert capsys.readouterr().out == expected_output['editor'].format(testobj=testobj)
        testobj.appbase.use_rt = True
        testobj = testee.EditorPanel(parent)
        assert testobj.parent == parent
        assert testobj.appbase == parent.book.parent
        assert testobj.defaultfamily == 'fontfamily'
        assert testobj.defaultsize == 'fontsize'
        assert capsys.readouterr().out == expected_output['editor2'].format(testobj=testobj,
                                                                            testee=testee)

    def test_canInsertFromMimeData(self, monkeypatch, capsys):
        """unittest for EditorPanel.canInsertFromMimeData
        """
        class MimeData:
            "stub"
            def __str__(self):
                return 'mimedata'
            def hasImage(self):
                return False
            def imageData(self):
                return 'imagedata'
        monkeypatch.setattr(testee.qtw.QTextEdit, 'canInsertFromMimeData',
                            mockqtw.MockEditorWidget.canInsertFromMimeData)
        testobj = self.setup_testobj(monkeypatch, capsys)
        source = MimeData()
        assert not testobj.canInsertFromMimeData(source)
        assert capsys.readouterr().out == "called Editor.canInsertFromMimeData with arg 'mimedata'\n"
        source.hasImage = lambda: True
        assert testobj.canInsertFromMimeData(source)
        assert capsys.readouterr().out == ("")

    def test_insertFromMimeData(self, monkeypatch, capsys):
        """unittest for EditorPanel.insertFromMimeData
        """
        class MimeData:
            """stub
            """
            # def __str__(self):
            #     return 'mimedata'
            def hasImage(self):
                return False
            def imageData(self):
                return mockqtw.MockImage()
        def mock_cursor(self):
            print('called TextEdit.textCursor')
            return mockqtw.MockCursor()
        def mock_document(self):
            print('called TextEdit.document')
            doc = mockqtw.MockTextDocument()
            # assert capsys.readouterr().out == 'called TextDocument.__init__ with args ()'
            return doc
        monkeypatch.setattr(testee.qtw.QTextEdit, 'insertFromMimeData',
                            mockqtw.MockEditorWidget.insertFromMimeData)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'textCursor', mock_cursor)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'document', mock_document)
        monkeypatch.setattr(testee.gui, 'QImage', mockqtw.MockImage)
        monkeypatch.setattr(testee.core, 'QUrl', mockqtw.MockUrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.appbase.imagelist = []
        testobj.appbase.imagecount = 0
        testobj.appbase.filename = "test"
        source = MimeData()
        testobj.insertFromMimeData(source)
        assert not testobj.appbase.imagelist
        assert capsys.readouterr().out == (
                f"called Editor.insertFromMimeData with args ({testobj}, {source})\n")
        source.hasImage = lambda: True
        testobj.insertFromMimeData(source)
        assert testobj.appbase.imagelist == ['test_00001.png']
        assert capsys.readouterr().out == (
                "called Image.__init__ with args ()\n"
                "called TextEdit.textCursor\n"
                "called Cursor.__init__\n"
                "called TextEdit.document\n"
                "called TextDocument.__init__ with args ()\n"
                "called image.save with arg test_00001.png\n"
                "called Url.__init__ with args ('test_00001.png',)\n"
                "called TextDocument.addResource with args (2, MockUrl, MockImage)\n"
                "called Cursor.insertImage with arg test_00001.png\n")

    def test_set_contents(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_contents
        """
        def mock_sethtml(text):
            print(f'called Editor.setHtml with arg `{text}`')
        def mock_charformat_changed(arg):
            print('called Editor.charformat_changed')  # with arg {arg}')
        def mock_settext(text):
            print(f'called Editor.setText with arg `{text}`')
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.setHtml = mock_sethtml
        testobj.charformat_changed = mock_charformat_changed
        testobj.setText = mock_settext
        testobj.set_contents("<data>")
        assert capsys.readouterr().out == ("called Editor.setHtml with arg `<data>`\n"
                                           "called TextCharFormat.__init__ with args ()\n"
                                           "called Editor.charformat_changed\n")
        testobj.set_contents("data")
        assert capsys.readouterr().out == "called Editor.setText with arg `data`\n"

    def test_get_contents(self, monkeypatch, capsys):
        """unittest for EditorPanel.get_contents
        """
        def mock_tohtml():
            print('called Editor.toHtml')
            return '<p>editor text</p>'
        def mock_toplaintext():
            print('called Editor.toPlainText')
            return 'editor text'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.toHtml = mock_tohtml
        testobj.toPlainText = mock_toplaintext
        testobj.appbase.use_rt = False
        assert testobj.get_contents() == "editor text"
        assert capsys.readouterr().out == "called Editor.toPlainText\n"
        testobj.appbase.use_rt = True
        assert testobj.get_contents() == "<p>editor text</p>"
        assert capsys.readouterr().out == "called Editor.toHtml\n"

    def test_text_bold(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_bold
        """
        def mock_merge(arg):
            print('called EditorPanel.mergeCurrentCharFormat')
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.hasFocus = lambda: False
        testobj.mergeCurrentCharFormat = mock_merge
        testobj.text_bold()
        assert capsys.readouterr().out == ""
        testobj.hasFocus = lambda: True
        testobj.actiondict = {'&Bold': mockqtw.MockAction()}
        assert capsys.readouterr().out == "called Action.__init__ with args ()\n"
        testobj.text_bold()
        assert capsys.readouterr().out == (
                "called TextCharFormat.__init__ with args ()\n"
                "called Action.isChecked\n"
                f"called TextCharFormat.setFontWeight with arg {testee.gui.QFont.Weight.Normal}\n"
                "called EditorPanel.mergeCurrentCharFormat\n")
        testobj.actiondict['&Bold'].setChecked(True)
        testobj.text_bold()
        assert capsys.readouterr().out == (
                "called Action.setChecked with arg `True`\n"
                "called TextCharFormat.__init__ with args ()\n"
                "called Action.isChecked\n"
                f"called TextCharFormat.setFontWeight with arg {testee.gui.QFont.Weight.Bold}\n"
                "called EditorPanel.mergeCurrentCharFormat\n")

    def test_text_italic(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_italic
        """
        def mock_merge(arg):
            print('called EditorPanel.mergeCurrentCharFormat')
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.hasFocus = lambda: False
        testobj.mergeCurrentCharFormat = mock_merge
        testobj.text_italic()
        assert capsys.readouterr().out == ""
        testobj.hasFocus = lambda: True
        testobj.actiondict = {'&Italic': mockqtw.MockAction()}
        assert capsys.readouterr().out == "called Action.__init__ with args ()\n"
        testobj.text_italic()
        assert capsys.readouterr().out == (
                "called TextCharFormat.__init__ with args ()\n"
                "called Action.isChecked\n"
                "called TextCharFormat.setFontItalic with arg False\n"
                "called EditorPanel.mergeCurrentCharFormat\n")
        testobj.actiondict['&Italic'].setChecked(True)
        testobj.text_italic()
        assert capsys.readouterr().out == (
                "called Action.setChecked with arg `True`\n"
                "called TextCharFormat.__init__ with args ()\n"
                "called Action.isChecked\n"
                "called TextCharFormat.setFontItalic with arg True\n"
                "called EditorPanel.mergeCurrentCharFormat\n")

    def test_text_underline(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_underline
        """
        def mock_merge(arg):
            print('called EditorPanel.mergeCurrentCharFormat')
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.hasFocus = lambda: False
        testobj.mergeCurrentCharFormat = mock_merge
        testobj.text_underline()
        assert capsys.readouterr().out == ""
        testobj.hasFocus = lambda: True
        testobj.actiondict = {'&Underline': mockqtw.MockAction()}
        assert capsys.readouterr().out == "called Action.__init__ with args ()\n"
        testobj.text_underline()
        assert capsys.readouterr().out == (
                "called TextCharFormat.__init__ with args ()\n"
                "called Action.isChecked\n"
                "called TextCharFormat.setFontUnderline with arg False\n"
                "called EditorPanel.mergeCurrentCharFormat\n")
        testobj.actiondict['&Underline'].setChecked(True)
        testobj.text_underline()
        assert capsys.readouterr().out == (
                "called Action.setChecked with arg `True`\n"
                "called TextCharFormat.__init__ with args ()\n"
                "called Action.isChecked\n"
                "called TextCharFormat.setFontUnderline with arg True\n"
                "called EditorPanel.mergeCurrentCharFormat\n")

    def test_text_strikethrough(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_strikethrough
        """
        def mock_merge(arg):
            print('called EditorPanel.mergeCurrentCharFormat')
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.hasFocus = lambda: False
        testobj.mergeCurrentCharFormat = mock_merge
        testobj.text_strikethrough()
        assert capsys.readouterr().out == ""
        testobj.hasFocus = lambda: True
        testobj.actiondict = {'Strike&through': mockqtw.MockAction()}
        assert capsys.readouterr().out == "called Action.__init__ with args ()\n"
        testobj.text_strikethrough()
        assert capsys.readouterr().out == (
                "called TextCharFormat.__init__ with args ()\n"
                "called Action.isChecked\n"
                "called TextCharFormat.setFontStrikeOut with arg False\n"
                "called EditorPanel.mergeCurrentCharFormat\n")
        testobj.actiondict['Strike&through'].setChecked(True)
        testobj.text_strikethrough()
        assert capsys.readouterr().out == (
                "called Action.setChecked with arg `True`\n"
                "called TextCharFormat.__init__ with args ()\n"
                "called Action.isChecked\n"
                "called TextCharFormat.setFontStrikeOut with arg True\n"
                "called EditorPanel.mergeCurrentCharFormat\n")

    def _test_case_lower(self, monkeypatch, capsys):
        """unittest for EditorPanel.case_lower - not implemented
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.case_lower() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_case_upper(self, monkeypatch, capsys):
        """unittest for EditorPanel.case_upper - not implemented
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.case_upper() == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_indent_more(self, monkeypatch, capsys):
        """unittest for EditorPanel.indent_more
        """
        def mock_change(arg):
            print(f"called MainGui.change_indent with arg '{arg}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.change_indent = mock_change
        testobj.indent_more()
        assert capsys.readouterr().out == "called MainGui.change_indent with arg '1'\n"

    def test_indent_less(self, monkeypatch, capsys):
        """unittest for EditorPanel.indent_less
        """
        def mock_change(arg):
            print(f"called MainGui.change_indent with arg '{arg}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.change_indent = mock_change
        testobj.indent_less()
        assert capsys.readouterr().out == "called MainGui.change_indent with arg '-1'\n"

    def test_change_indent(self, monkeypatch, capsys):
        """unittest for EditorPanel.change_indent
        """
        def mock_textcursor():
            print('called EditorPanel.textCursor')
            return mockqtw.MockTextCursor()
        def mock_indent(self):
            print("called TextBlockFormat.indent")
            return 0
        monkeypatch.setattr(testee.EditorPanel, 'hasFocus', mockqtw.MockEditorWidget.hasFocus)
        monkeypatch.setattr(testee.EditorPanel, 'textCursor', mockqtw.MockEditorWidget.textCursor)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.textCursor = mock_textcursor
        testobj.hasFocus = lambda: False
        testobj.change_indent(10)
        assert capsys.readouterr().out == ""
        testobj.hasFocus = lambda: True
        testobj.change_indent(10)
        assert capsys.readouterr().out == ("called EditorPanel.textCursor\n"
                                           "called TextCursor.__init__\n"
                                           "called TextCursor.blockFormat\n"
                                           "called TextBlockFormat.__init__ with args ()\n"
                                           "called TextBlockFormat.indent\n"
                                           "called TextBlockFormat.setIndent with arg 11\n"
                                           "called TextCursor.mergeBlockFormat\n")
        monkeypatch.setattr(mockqtw.MockTextBlockFormat, 'indent', mock_indent)
        testobj.change_indent(10)
        assert capsys.readouterr().out == ("called EditorPanel.textCursor\n"
                                           "called TextCursor.__init__\n"
                                           "called TextCursor.blockFormat\n"
                                           "called TextBlockFormat.__init__ with args ()\n"
                                           "called TextBlockFormat.indent\n"
                                           "called TextCursor.mergeBlockFormat\n")

    def test_text_font(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_font
        """
        def mock_merge(arg):
            print('called EditorPanel.mergeCurrentCharFormat')
        def mock_tabsize(arg):
            print(f'called shared.tabsize with arg {arg}')
            return 10
        def mock_set(arg):
            print(f'called EditorPanel.setTabStopWidth with arg {arg}')
        monkeypatch.setattr(testee.shared, 'tabsize', mock_tabsize)
        monkeypatch.setattr(testee.qtw, 'QFontDialog', mockqtw.MockFontDialog)
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.hasFocus = lambda: False
        testobj.currentFont = lambda: mockqtw.MockFont()
        testobj.mergeCurrentCharFormat = mock_merge
        testobj.setTabStopWidth = mock_set
        testobj.text_font()
        assert capsys.readouterr().out == ("")
        testobj.hasFocus = lambda: True
        # breakpoint()
        testobj.text_font()
        assert capsys.readouterr().out == ("called Font.__init__\n"
                                           f"called FontDialog.getFont with args {testobj}\n")
        monkeypatch.setattr(mockqtw.MockFontDialog, 'getFont', mockqtw.MockFontDialog.getFont2)
        monkeypatch.setattr(testee.qtw, 'QFontDialog', mockqtw.MockFontDialog)
        testobj.text_font()
        assert capsys.readouterr().out == ("called Font.__init__\n"
                                           f"called FontDialog.getFont with args {testobj}\n"
                                           "called Font.__init__\n"
                                           "called TextCharFormat.__init__ with args ()\n"
                                           "called TextCharFormat.setFont\n"
                                           "called Font.pointSize\n"
                                           "called shared.tabsize with arg fontsize\n"
                                           "called EditorPanel.setTabStopWidth with arg 10\n"
                                           "called EditorPanel.mergeCurrentCharFormat\n")

    def test_text_family(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_family
        """
        def mock_merge(arg):
            print('called EditorPanel.mergeCurrentCharFormat')
        def mock_set():
            print('called EditorPanel.setFocus')
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mergeCurrentCharFormat = mock_merge
        testobj.setFocus = mock_set
        testobj.text_family('family')
        assert capsys.readouterr().out == ("called TextCharFormat.__init__ with args ()\n"
                                           "called TextCharFormat.setFontFamily with arg family\n"
                                           "called EditorPanel.mergeCurrentCharFormat\n"
                                           "called EditorPanel.setFocus\n")

    def test_enlarge_text(self, monkeypatch, capsys):
        """unittest for EditorPanel.enlarge_text
        """
        def mock_text_size(arg):
            print(f"called EditorPanel.text_size with arg '{arg}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.text_size = mock_text_size
        testobj.parent.combo_size = mockqtw.MockComboBox()
        assert capsys.readouterr().out == 'called ComboBox.__init__\n'
        testobj.parent.fontsizes = ['current text', 'larger text']
        testobj.enlarge_text()
        assert capsys.readouterr().out == ("called ComboBox.currentText\n"
                                           "called EditorPanel.text_size with arg 'larger text'\n")
        testobj.parent.fontsizes = ['smaller text', 'current text']
        testobj.enlarge_text()
        assert capsys.readouterr().out == "called ComboBox.currentText\n"

    def test_shrink_text(self, monkeypatch, capsys):
        """unittest for EditorPanel.shrink_text
        """
        def mock_text_size(arg):
            print(f"called EditorPanel.text_size with arg '{arg}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.text_size = mock_text_size
        testobj.parent.combo_size = mockqtw.MockComboBox()
        assert capsys.readouterr().out == 'called ComboBox.__init__\n'
        testobj.parent.fontsizes = ['smaller text', 'current text']
        testobj.shrink_text()
        assert capsys.readouterr().out == ("called ComboBox.currentText\n"
                                           "called EditorPanel.text_size with arg 'smaller text'\n")
        testobj.parent.fontsizes = ['current text', 'larger text']
        testobj.shrink_text()
        assert capsys.readouterr().out == "called ComboBox.currentText\n"

    def test_linespacing_1(self, monkeypatch, capsys):
        """unittest for EditorPanel.linespacing_1
        """
        def mock_set_linespacing(arg):
            print(f"called EditorPanel.set_linespacing with arg '{arg}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_linespacing = mock_set_linespacing
        testobj.linespacing_1()
        assert capsys.readouterr().out == ("called EditorPanel.set_linespacing with arg '0'\n")

    def test_linespacing_15(self, monkeypatch, capsys):
        """unittest for EditorPanel.linespacing_15
        """
        def mock_set_linespacing(arg):
            print(f"called EditorPanel.set_linespacing with arg '{arg}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_linespacing = mock_set_linespacing
        testobj.linespacing_15()
        assert capsys.readouterr().out == ("called EditorPanel.set_linespacing with arg '150'\n")

    def test_linespacing_2(self, monkeypatch, capsys):
        """unittest for EditorPanel.linespacing_2
        """
        def mock_set_linespacing(arg):
            print(f"called EditorPanel.set_linespacing with arg '{arg}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_linespacing = mock_set_linespacing
        testobj.linespacing_2()
        assert capsys.readouterr().out == ("called EditorPanel.set_linespacing with arg '200'\n")

    def test_set_linespacing(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_linespacing
        """
        def mock_textcursor():
            print('called EditorPanel.textCursor')
            return mockqtw.MockTextCursor()
        monkeypatch.setattr(testee.EditorPanel, 'hasFocus', mockqtw.MockEditorWidget.hasFocus)
        monkeypatch.setattr(testee.EditorPanel, 'textCursor', mockqtw.MockEditorWidget.textCursor)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.textCursor = mock_textcursor
        testobj.hasFocus = lambda: False
        testobj.set_linespacing(100)
        assert capsys.readouterr().out == ""
        testobj.hasFocus = lambda: True
        testobj.set_linespacing(0)
        assert capsys.readouterr().out == ("called EditorPanel.textCursor\n"
                                           "called TextCursor.__init__\n"
                                           "called TextCursor.blockFormat\n"
                                           "called TextBlockFormat.__init__ with args ()\n"
                                           "called TextBlockFormat.setLineHeight with args"
                                           " (0, <LineHeightTypes.SingleHeight: 0>)\n"
                                           "called TextCursor.mergeBlockFormat\n")
        testobj.set_linespacing(100)
        assert capsys.readouterr().out == ("called EditorPanel.textCursor\n"
                                           "called TextCursor.__init__\n"
                                           "called TextCursor.blockFormat\n"
                                           "called TextBlockFormat.__init__ with args ()\n"
                                           "called TextBlockFormat.setLineHeight with args"
                                           " (100, <LineHeightTypes.ProportionalHeight: 1>)\n"
                                           "called TextCursor.mergeBlockFormat\n")

    def test_increase_paragraph_spacing(self, monkeypatch, capsys):
        """unittest for EditorPanel.increase_paragraph_spacing
        """
        def mock_set(**kwargs):
            print('called testobj.set_paragraph_spacing with args', kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_paragraph_spacing = mock_set
        testobj.increase_paragraph_spacing()
        assert capsys.readouterr().out == (
                "called testobj.set_paragraph_spacing with args {'more': True}\n")

    def test_decrease_paragraph_spacing(self, monkeypatch, capsys):
        """unittest for EditorPanel.decrease_paragraph_spacing
        """
        def mock_set(**kwargs):
            print('called EditorPanel.set_paragraph_spacing with args', kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_paragraph_spacing = mock_set
        testobj.decrease_paragraph_spacing()
        assert capsys.readouterr().out == (
                "called EditorPanel.set_paragraph_spacing with args {'less': True}\n")

    def test_set_paragraph_spacing(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_paragraph_spacing
        """
        def mock_textcursor():
            print('called EditorPanel.textCursor')
            return mockqtw.MockTextCursor()
        def mock_top(self):
            print("called TextBlockFormat.topMargin")
            return 0.5
        def mock_bottom(self):
            print("called TextBlockFormat.bottomMargin")
            return 0.5
        def mock_fontsize(self):
            print('called Font.pointSize')
            return 10
        monkeypatch.setattr(testee.EditorPanel, 'hasFocus', mockqtw.MockEditorWidget.hasFocus)
        monkeypatch.setattr(testee.EditorPanel, 'textCursor', mockqtw.MockEditorWidget.textCursor)
        monkeypatch.setattr(mockqtw.MockFont, 'pointSize', mock_fontsize)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.textCursor = mock_textcursor
        testobj.currentFont = lambda: mockqtw.MockFont()
        testobj.hasFocus = lambda: False
        testobj.set_paragraph_spacing()
        assert capsys.readouterr().out == ""
        testobj.hasFocus = lambda: True
        testobj.set_paragraph_spacing(more=True)
        assert capsys.readouterr().out == ("called EditorPanel.textCursor\n"
                                           "called TextCursor.__init__\n"
                                           "called TextCursor.blockFormat\n"
                                           "called TextBlockFormat.__init__ with args ()\n"
                                           "called TextBlockFormat.topMargin\n"
                                           "called TextBlockFormat.bottomMargin\n"
                                           "called Font.__init__\n"
                                           "called Font.pointSize\n"
                                           "called TextBlockFormat.setTopMargin with arg 6.0\n"
                                           "called Font.__init__\n"
                                           "called Font.pointSize\n"
                                           "called TextBlockFormat.setBottomMargin with arg 6.0\n"
                                           "called TextCursor.mergeBlockFormat\n")
        testobj.set_paragraph_spacing(less=True)
        assert capsys.readouterr().out == ("called EditorPanel.textCursor\n"
                                           "called TextCursor.__init__\n"
                                           "called TextCursor.blockFormat\n"
                                           "called TextBlockFormat.__init__ with args ()\n"
                                           "called TextBlockFormat.topMargin\n"
                                           "called TextBlockFormat.bottomMargin\n"
                                           "called Font.__init__\n"
                                           "called Font.pointSize\n"
                                           "called TextBlockFormat.setTopMargin with arg -4.0\n"
                                           "called Font.__init__\n"
                                           "called Font.pointSize\n"
                                           "called TextBlockFormat.setBottomMargin with arg -4.0\n"
                                           "called TextCursor.mergeBlockFormat\n")
        monkeypatch.setattr(mockqtw.MockTextBlockFormat, 'topMargin', mock_top)
        monkeypatch.setattr(mockqtw.MockTextBlockFormat, 'bottomMargin', mock_bottom)
        testobj.set_paragraph_spacing(less=True)
        assert capsys.readouterr().out == ("called EditorPanel.textCursor\n"
                                           "called TextCursor.__init__\n"
                                           "called TextCursor.blockFormat\n"
                                           "called TextBlockFormat.__init__ with args ()\n"
                                           "called TextBlockFormat.topMargin\n"
                                           "called TextBlockFormat.bottomMargin\n"
                                           "called TextCursor.mergeBlockFormat\n")

    def test_text_size(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_size
        """
        def mock_tabsize(arg):
            print('called shared.mock_tabsize with arg', arg)
            return 18
        def mock_settab(arg):
            print('called EditorPanel.setTabStopDistance with arg', arg)
        def mock_merge(arg):
            print('called EditorPanel.mergeCurrentcharformat')
        def mock_setfocus():
            print('called EditorPanel.set_focus')
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        monkeypatch.setattr(testee.shared, 'tabsize', mock_tabsize)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.setTabStopDistance = mock_settab
        testobj.mergeCurrentCharFormat = mock_merge
        testobj.setFocus = mock_setfocus
        testobj.text_size(0)
        assert capsys.readouterr().out == ""
        testobj.text_size(10)
        assert capsys.readouterr().out == (
                "called TextCharFormat.__init__ with args ()\n"
                "called TextCharFormat.setFontPointSize with arg 10.0\n"
                "called shared.mock_tabsize with arg 10.0\n"
                "called EditorPanel.setTabStopDistance with arg 18\n"
                "called EditorPanel.mergeCurrentcharformat\n"
                "called EditorPanel.set_focus\n")

    def test_charformat_changed(self, monkeypatch, capsys):
        """unittest for EditorPanel.charformat_changed
        """
        def mock_font_changed(arg):
            print(f'called EditorPanel.font_changed with arg {arg}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.font_changed = mock_font_changed
        fmt = mockqtw.MockTextCharFormat()
        testobj.charformat_changed(fmt)
        assert capsys.readouterr().out == ("called TextCharFormat.__init__ with args ()\n"
                                           "called TextCharFormat.font\n"
                                           "called EditorPanel.font_changed with arg a font\n")

    def _test_cursorposition_changed(self, monkeypatch, capsys):
        """unittest for EditorPanel.cursorposition_changed - not implemented
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.cursorposition_changed() == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_font_changed(self, monkeypatch, capsys):
        """unittest for EditorPanel.font_changed
        """
        monkeypatch.setattr(testee.gui, 'QFontInfo', mockqtw.MockFontInfo)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.combo_font = mockqtw.MockComboBox()
        testobj.parent.combo_size = mockqtw.MockComboBox()
        testobj.actiondict = {"&Bold": mockqtw.MockCheckBox(),
                              "&Italic": mockqtw.MockCheckBox(),
                              "&Underline": mockqtw.MockCheckBox(),
                              "Strike&through": mockqtw.MockCheckBox()}
        font = mockqtw.MockFont()
        font.bold = lambda: False
        font.italic = lambda: False
        font.underline = lambda: False
        font.strikeOut = lambda: False
        assert capsys.readouterr().out == ("called ComboBox.__init__\ncalled ComboBox.__init__\n"
                                           "called CheckBox.__init__\ncalled CheckBox.__init__\n"
                                           "called CheckBox.__init__\ncalled CheckBox.__init__\n"
                                           "called Font.__init__\n")

        testobj.font_changed(font)
        assert capsys.readouterr().out == (f"called FontInfo.__init__ with arg {font}\n"
                                           "called Font.family\n"
                                           "called ComboBox.findText with args ('family name',)\n"
                                           "called ComboBox.setCurrentIndex with arg `1`\n"
                                           "called Font.pointSize\n"
                                           "called ComboBox.findText with args ('fontsize',)\n"
                                           "called ComboBox.setCurrentIndex with arg `1`\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n")
        font.bold = lambda: True
        font.italic = lambda: True
        font.underline = lambda: True
        font.strikeOut = lambda: True
        testobj.font_changed(font)
        assert capsys.readouterr().out == (f"called FontInfo.__init__ with arg {font}\n"
                                           "called Font.family\n"
                                           "called ComboBox.findText with args ('family name',)\n"
                                           "called ComboBox.setCurrentIndex with arg `1`\n"
                                           "called Font.pointSize\n"
                                           "called ComboBox.findText with args ('fontsize',)\n"
                                           "called ComboBox.setCurrentIndex with arg `1`\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n")

    def test_mergeCurrentCharFormat(self, monkeypatch, capsys):
        """unittest for EditorPanel.mergeCurrentCharFormat
        """
        def mock_cursor():
            print('called TextEdit.textCursor')
            return mockqtw.MockTextCursor()
        def mock_has_sel(self):
            print('called TextCursor.hasSelection')
            return True
        def mock_merge(self, *args):
            print('called TextCursor.mergeCurrentCharFormat with args', args)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'mergeCurrentCharFormat', mock_merge)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.textCursor = mock_cursor
        testobj.mergeCurrentCharFormat('format')
        assert capsys.readouterr().out == (
                "called TextEdit.textCursor\n"
                "called TextCursor.__init__\n"
                "called TextCursor.hasSelection\n"
                "called TextCursor.select with"
                f" arg {testee.gui.QTextCursor.SelectionType.WordUnderCursor}\n"
                "called TextCursor.mergeCharFormat with arg format\n"
                "called TextCursor.mergeCurrentCharFormat with args ('format',)\n")
        monkeypatch.setattr(mockqtw.MockTextCursor, 'hasSelection', mock_has_sel)
        testobj.mergeCurrentCharFormat('format')
        assert capsys.readouterr().out == (
                "called TextEdit.textCursor\n"
                "called TextCursor.__init__\n"
                "called TextCursor.hasSelection\n"
                "called TextCursor.mergeCharFormat with arg format\n"
                "called TextCursor.mergeCurrentCharFormat with args ('format',)\n")

    def _test_update_bold(self, monkeypatch, capsys):
        """unittest for EditorPanel.update_bold - not implemented
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.update_bold() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_update_italic(self, monkeypatch, capsys):
        """unittest for EditorPanel.update_italic - not implemented
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.update_italic() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_update_underline(self, monkeypatch, capsys):
        """unittest for EditorPanel.update_underline - not implemented
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.update_underline() == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_check_dirty(self, monkeypatch, capsys):
        """unittest for EditorPanel._check_dirty
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.document = lambda: mockqtw.MockTextDocument()
        assert testobj._check_dirty() == "modified"
        assert capsys.readouterr().out == ("called TextDocument.__init__ with args ()\n"
                                           "called textDocument.isModified\n")

    def test_mark_dirty(self, monkeypatch, capsys):
        """unittest for EditorPanel._mark_dirty
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.document = lambda: mockqtw.MockTextDocument()
        testobj._mark_dirty('value')
        assert capsys.readouterr().out == ("called TextDocument.__init__ with args ()\n"
                                           "called TextDocument.setModified with arg value\n")

    def test_openup(self, monkeypatch, capsys):
        """unittest for EditorPanel._openup
        """
        def mock_set(value):
            print(f'called EditorPanel.setReadOnly with arg {value}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.setReadOnly = mock_set
        testobj._openup('value')
        assert capsys.readouterr().out == ("called EditorPanel.setReadOnly with arg False\n")
        testobj._openup('')
        assert capsys.readouterr().out == ("called EditorPanel.setReadOnly with arg True\n")


class TestPage0Gui:
    """unittest for gui_qt.Page0Gui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.Page0Gui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Page0Gui.__init__ with args', args)
            self.book = args[0]
            self.master = args[1]
        parent = MockBook()
        master = MockPage()
        monkeypatch.setattr(testee.Page0Gui, '__init__', mock_init)
        testobj = testee.Page0Gui(parent, master, [])
        assert capsys.readouterr().out == (
                'called Page.__init__\n'
                f'called Page0Gui.__init__ with args ({parent}, {master}, [])\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Page0Gui.__init__
        """
        def mock_init(self, parent, master):
            """stub
            """
            print(f'called PageGui.__init__ with args ({parent}, {master})')
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        parent = MockBook()
        master = MockPage()
        assert capsys.readouterr().out == 'called Page.__init__\n'
        monkeypatch.setattr(testee.PageGui, '__init__', mock_init)
        testobj = testee.Page0Gui(parent, master)
        assert isinstance(testobj.sizer, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == (
                f"called PageGui.__init__ with args ({parent}, {master})\n"
                "called VBox.__init__\n")

    def test_add_list(self, monkeypatch, capsys):
        """unittest for Page0Gui.add_list
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QTreeWidget', mockqtw.MockTreeWidget)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_list(['xx', 'yy'], [10, 20])
        assert isinstance(result, testee.qtw.QTreeWidget)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called Tree.__init__\n"
                "called Tree.setSortingEnabled with arg True\n"
                "called Tree.setHeaderLabels with arg `['xx', 'yy']`\n"
                "called Tree.setAlternatingRowColors with arg True\n"
                "called Tree.header\n"
                "called Header.__init__\n"
                "called Header.setSectionsClickable with arg True\n"
                "called Header.resizeSection with args (0, 10)\n"
                "called Header.resizeSection with args (1, 20)\n"
                "called Header.setStretchLastSection with arg True\n"
                f"called Signal.connect with args ({testobj.on_activate_item},)\n"
                f"called Signal.connect with args ({testobj.on_change_selected},)\n"
                "called HBox.addWidget with arg MockTreeWidget\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    # def test_add_buttons(self, monkeypatch, capsys):
    #     """unittest for Page0Gui.add_buttons
    #     """
    #     def callback1():
    #         "stub for reference"
    #     def callback2():
    #         "stub for reference"
    #     monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    #     monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.sizer = mockqtw.MockVBoxLayout()
    #     assert capsys.readouterr().out == "called VBox.__init__\n"
    #     testobj.add_buttons([('xx', callback1), ('yy', callback2)])
    #     assert capsys.readouterr().out == (
    #             "called HBox.__init__\n"
    #             "called HBox.addStretch\n"
    #             f"called PushButton.__init__ with args ('xx', {testobj}) {{}}\n"
    #             f"called Signal.connect with args ({callback1},)\n"
    #             "called HBox.addWidget with arg MockPushButton\n"
    #             f"called PushButton.__init__ with args ('yy', {testobj}) {{}}\n"
    #             f"called Signal.connect with args ({callback2},)\n"
    #             "called HBox.addWidget with arg MockPushButton\n"
    #             "called HBox.addStretch\n"
    #             "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_enable_button(self, monkeypatch, capsys):
        """unittest for Page0Gui.enable_button
        """
        monkeypatch.setattr(testee.PageGui, 'setLayout', mockqtw.MockFrame.setLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.finish_display()
        assert capsys.readouterr().out == "called Frame.setLayout with arg MockVBoxLayout\n"

    def test_enable_sorting(self, monkeypatch, capsys):
        """unittest for Page0Gui.enable_sorting
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.enable_sorting(p0list, 'value')
        assert capsys.readouterr().out == "called Tree.setSortingEnabled with arg value\n"

    # def test_enable_button(self, monkeypatch, capsys):
    #     """unittest for Page0Gui.enable_button
    #     """
    #     button = mockqtw.MockPushButton()
    #     assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.enable_button(button, 'state')
    #     assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `state`\n")

    def test_on_change_selected(self, monkeypatch, capsys):
        """unittest for Page0Gui.on_change_selected
        """
        def mock_change(*args):
            print('called Page0.change_selected with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(change_selected=mock_change)
        testobj.on_change_selected(None, 'item_o')
        assert capsys.readouterr().out == ("")
        testobj.on_change_selected('item_n', 'item_o')
        assert capsys.readouterr().out == ("called Page0.change_selected with args ('item_n',)\n")

    def test_on_activate_item(self, monkeypatch, capsys):
        """unittest for Page0Gui.on_activate_item
        """
        def mock_activate():
            print('called Page0.activate_item')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(activate_item=mock_activate)
        testobj.on_activate_item('item')
        assert capsys.readouterr().out == "called Page0.activate_item\n"

    def test_clear_list(self, monkeypatch, capsys):
        """unittest for Page0Gui.clear_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.clear_list(p0list)
        assert not p0list.has_selection
        assert capsys.readouterr().out == "called Tree.clear\n"

    def test_add_listitem(self, monkeypatch, capsys):
        """unittest for Page0Gui.add_listitem
        """
        monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        result = testobj.add_listitem(p0list, 'data')
        assert isinstance(result, testee.qtw.QTreeWidgetItem)
        assert capsys.readouterr().out == (
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.setData with args"
                f" (0, {testee.core.Qt.ItemDataRole.UserRole!r}, 'data')\n"
                "called Tree.addTopLevelItem\n")

    # def test_set_listitem_values(self, monkeypatch, capsys):
    #     """unittest for Page0Gui.set_listitem_values
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     p0list = mockqtw.MockTreeWidget()
    #     item = mockqtw.MockTreeItem()
    #     assert capsys.readouterr().out == ("called Tree.__init__\n"
    #                                        "called TreeItem.__init__ with args ()\n")
    #     testobj.set_listitem_values(p0list, item, ('xxx', 'yyy.a', 'zzz.b', 'q'))
    #     assert p0list.has_selection
    #     assert capsys.readouterr().out == ("called TreeItem.setText with args (0, 'xxx (A)')\n"
    #                                        "called TreeItem.setText with args (1, 'A')\n"
    #                                        "called TreeItem.setText with args (2, 'b')\n")
    #     testobj.set_listitem_values(p0list, item, ('xxx', 'y.abc', 'z.defg', 'hij', 'klm', ''))
    #     assert p0list.has_selection
    #     assert capsys.readouterr().out == ("called TreeItem.setText with args (0, 'xxx')\n"
    #                                        "called TreeItem.setText with args (1, 'A')\n"
    #                                        "called TreeItem.setText with args (2, 'defg')\n"
    #                                        "called TreeItem.setText with args (3, 'hij')\n"
    #                                        "called TreeItem.setText with args (4, 'klm')\n")

    def test_get_items(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_items
        """
        def mock_count():
            print('called Tree.topLevelItemCount')
            return 2
        def mock_item(num):
            print(f'called Tree.topLevelItem with arg {num}')
            return f'item{num}'
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTreeWidget()
        p0list.topLevelItemCount = mock_count
        p0list.topLevelItem = mock_item
        assert capsys.readouterr().out == "called Tree.__init__\n"
        assert testobj.get_items(p0list) == ['item0', 'item1']
        assert capsys.readouterr().out == ("called Tree.topLevelItemCount\n"
                                           "called Tree.topLevelItem with arg 0\n"
                                           "called Tree.topLevelItem with arg 1\n")

    def test_get_item_text(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_item_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        # p0list = 'p0list'
        item = mockqtw.MockTreeItem('col0', 'col1')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('col0', 'col1')\n"
        for column in (0, 1):
            assert testobj.get_item_text('p0list', item, column) == f"col{column}"
        assert capsys.readouterr().out == ("called TreeItem.text with arg 0\n"
                                           "called TreeItem.text with arg 1\n")

    def test_set_item_text(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_item_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        # p0list = 'p0list'
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.set_item_text('p0list', item, 0, 'text')
        assert capsys.readouterr().out == ("called TreeItem.setText with args (0, 'text')\n")

    def test_get_first_item(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_first_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        assert testobj.get_first_item(p0list) == "Tree.topLevelItem"
        assert capsys.readouterr().out == ("called Tree.topLevelItem with arg `0`\n")

    # def test_get_item_by_index(self, monkeypatch, capsys):
    #     """unittest for Page0Gui.get_item_by_index
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.p0list = mockqtw.MockTreeWidget()
    #     assert capsys.readouterr().out == "called Tree.__init__\n"
    #     assert testobj.get_item_by_index('item_n') == "Tree.topLevelItem"
    #     assert capsys.readouterr().out == ("called Tree.topLevelItem with arg `item_n`\n")

    def test_get_item_by_id(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_item_by_id
        """
        def mock_find(*args):
            print('called Tree.findItems with args', args)
            return []
        def mock_find_2(*args):
            print('called Tree.findItems with args', args)
            return ['x', 'y']
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        p0list.findItems = mock_find
        assert testobj.get_item_by_id(p0list, 'item_id') is None
        assert capsys.readouterr().out == (
                "called Tree.findItems with args ('item_id', <MatchFlag.MatchExactly: 0>, 0)\n")
        p0list.findItems = mock_find_2
        assert testobj.get_item_by_id(p0list, 'item_id') == 'x'
        assert capsys.readouterr().out == (
                "called Tree.findItems with args ('item_id', <MatchFlag.MatchExactly: 0>, 0)\n")

    # def test_has_selection(self, monkeypatch, capsys):
    #     """unittest for Page0Gui.has_selection
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.p0list = mockqtw.MockTreeWidget()
    #     assert capsys.readouterr().out == "called Tree.__init__\n"
    #     testobj.p0list.has_selection = True
    #     assert testobj.has_selection()
    #     testobj.p0list.has_selection = False
    #     assert not testobj.has_selection()

    def test_set_selection(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_selection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book = types.SimpleNamespace(current_item=None)
        p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.set_selection(p0list)
        assert capsys.readouterr().out == ""
        testobj.book.current_item = 'not None'
        testobj.set_selection(p0list)
        assert capsys.readouterr().out == "called Tree.setCurrentItem with arg `not None`\n"

    def test_get_selection(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_selection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        assert testobj.get_selection(p0list) == "called Tree.currentItem"
        assert capsys.readouterr().out == ("")

    def test_ensure_visible(self, monkeypatch, capsys):
        """unittest for Page0Gui.ensure_visible
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.ensure_visible(p0list, 'item')
        assert capsys.readouterr().out == "called Tree.scrollToItem with arg `item`\n"

    def test_set_button_text(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_archive_button_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
        testobj.set_button_text(button, 'text')
        assert capsys.readouterr().out == "called PushButton.setText with arg `text`\n"

    def test_get_selected_action(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_selected_action
        """
        def mock_item():
            print('called Tree.currentItem')
            return item
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTreeWidget()
        item = mockqtw.MockTreeItem()
        item.setData(0, testee.core.Qt.ItemDataRole.UserRole, 'data')
        p0list.currentItem = mock_item
        assert capsys.readouterr().out == (
                "called Tree.__init__\n"
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.setData with args (0, <ItemDataRole.UserRole: 256>, 'data')\n")
        assert testobj.get_selected_action(p0list) == "data"
        assert capsys.readouterr().out == (
                "called Tree.currentItem\n"
                "called TreeItem.data with args (0, <ItemDataRole.UserRole: 256>)\n")

    def test_get_list_row(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_list_row
        """
        def mock_get(*args):
            print('called Page0Gui.get_selection with args', args)
            return 'selection'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_selection = mock_get
        assert testobj.get_list_row('listbox') == "selection"
        assert capsys.readouterr().out == "called Page0Gui.get_selection with args ('listbox',)\n"

    def test_set_list_row(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_list_row
        """
        def mock_set(*args):
            print('called Page0Gui.set_selection with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_selection = mock_set
        testobj.set_list_row('listbox', 'num')
        assert capsys.readouterr().out == "called Page0Gui.set_selection with args ('listbox',)\n"


class TestPage1Gui:
    """unittest for gui_qt.Page1Gui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.Page1Gui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Page1Gui.__init__ with args', args)
            self.book = parent
            self.master = master
            self.appbase = self.book.parent
        parent = MockBook()
        master = MockPage()
        monkeypatch.setattr(testee.Page1Gui, '__init__', mock_init)
        testobj = testee.Page1Gui(parent, master)
        assert capsys.readouterr().out == (
                'called Page.__init__\n'
                f'called Page1Gui.__init__ with args ({parent}, {master})\n')
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for Page1Gui.__init__
        """
        def mock_init(self, parent, master):
            """stub
            """
            print(f'called PageGui.__init__ with args ({parent}, {master})')
            self.book = parent
            self.master = master
            self.appbase = self.book.parent
            self.appbase = types.SimpleNamespace()
        parent = MockBook()
        master = MockPage()
        assert capsys.readouterr().out == 'called Page.__init__\n'
        monkeypatch.setattr(testee.PageGui, '__init__', mock_init)
        monkeypatch.setattr(testee.PageGui, 'setLayout', mockqtw.MockFrame.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        testobj = testee.Page1Gui(parent, master)
        assert isinstance(testobj.sizer, testee.qtw.QVBoxLayout)
        assert isinstance(testobj.gsizer, testee.qtw.QGridLayout)
        assert testobj.row == 0
        assert capsys.readouterr().out == (
                f"called PageGui.__init__ with args ({parent}, {master})\n"
                "called VBox.__init__\n"
                "called Frame.setLayout with arg MockVBoxLayout\n"
                "called VBox.addSpacing\n"
                "called HBox.__init__\n"
                "called HBox.addSpacing\n"
                "called Grid.__init__\n"
                "called Grid.setRowMinimumHeight with args (0, 10)\n"
                "called Grid.setColumnStretch with args (2, 1)\n"
                "called HBox.addLayout with arg MockGridLayout\n"
                "called VBox.addLayout with arg MockHBoxLayout\n"
                "called VBox.addStretch\n")

    def test_add_textentry_line(self, monkeypatch, capsys):
        """unittest for Page1Gui.add_textentry_line
        """
        def callback():
            "stub, for reference"
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.row = 0
        result = testobj.add_textentry_line('labeltext', 'width', None)
        assert isinstance(result, testee.qtw.QLineEdit)
        assert testobj.row == 2
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('labeltext', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at (1, 0)\n"
                f"called LineEdit.__init__ with args ({testobj},)\n"
                "called LineEdit.setMaximumWidth with arg `width`\n"
                "called LineEdit.setMinimumWidth with arg `width`\n"
                "called Grid.addWidget with arg MockLineEdit at (1, 1)\n"
                "called Grid.setRowMinimumHeight with args (2, 5)\n")
        testobj.row = 0
        result = testobj.add_textentry_line('labeltext', 'width', callback)
        assert isinstance(result, testee.qtw.QLineEdit)
        assert testobj.row == 2
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('labeltext', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at (1, 0)\n"
                f"called LineEdit.__init__ with args ({testobj},)\n"
                "called LineEdit.setMaximumWidth with arg `width`\n"
                "called LineEdit.setMinimumWidth with arg `width`\n"
                f"called Signal.connect with args ({callback},)\n"
                "called Grid.addWidget with arg MockLineEdit at (1, 1)\n"
                "called Grid.setRowMinimumHeight with args (2, 5)\n")

    def test_add_combobox_line(self, monkeypatch, capsys):
        """unittest for Page1Gui.add_combobox_line
        """
        def callback():
            "stub, for reference"
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.row = 0
        result = testobj.add_combobox_line('labe;text', 'width', None)
        assert isinstance(result, testee.qtw.QComboBox)
        assert testobj.row == 2
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('labe;text', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at (1, 0)\n"
                "called ComboBox.__init__\n"
                "called ComboBox.setEditable with arg `False`\n"
                "called ComboBox.setMaximumWidth with arg `width`\n"
                "called Grid.addWidget with arg MockComboBox at (1, 1)\n"
                "called Grid.setRowMinimumHeight with args (2, 5)\n")
        testobj.row = 0
        result = testobj.add_combobox_line('labe;text', 'width', callback)
        assert isinstance(result, testee.qtw.QComboBox)
        assert testobj.row == 2
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('labe;text', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at (1, 0)\n"
                "called ComboBox.__init__\n"
                "called ComboBox.setEditable with arg `False`\n"
                "called ComboBox.setMaximumWidth with arg `width`\n"
                f"called Signal.connect with args ({callback},)\n"
                "called Grid.addWidget with arg MockComboBox at (1, 1)\n"
                "called Grid.setRowMinimumHeight with args (2, 5)\n")

    def test_add_pushbutton_line(self, monkeypatch, capsys):
        """unittest for Page1Gui.add_pushbutton_line
        """
        def callback():
            "stub, for reference"
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.row = 0
        results = testobj.add_pushbutton_line('labeltext', 'buttontext', callback)
        assert isinstance(results[0], testee.qtw.QLabel)
        assert isinstance(results[1], testee.qtw.QPushButton)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                f"called Label.__init__ with args ('labeltext', {testobj})\n"
                "called HBox.addWidget with arg MockLabel\n"
                "called HBox.addStretch\n"
                "called Grid.addLayout with arg MockHBoxLayout at (1, 1)\n"
                "called HBox.__init__\n"
                f"called PushButton.__init__ with args ('buttontext', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called Grid.addLayout with arg MockHBoxLayout at (2, 1)\n")

    def test_add_textbox_line(self, monkeypatch, capsys):
        """unittest for Page1Gui.add_textbox_line
        """
        def callback():
            "stub, for reference"
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QTextEdit', mockqtw.MockEditorWidget)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.row = 0
        result = testobj.add_textbox_line('labeltext', callback)
        assert isinstance(result, testee.qtw.QTextEdit)
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('labeltext', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at (1, 0)\n"
                "called HBox.__init__\n"
                f"called Editor.__init__ with args ({testobj},)\n"
                f"called Signal.connect with args ({callback},)\n"
                "called HBox.addWidget with arg MockEditorWidget\n"
                "called Grid.addLayout with arg MockHBoxLayout at (2, 0, 1, -1)\n")

    def test_show_button(self, monkeypatch, capsys):
        """unittest for Page1Gui.show_button
        """
        button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.show_button(button, '')
        assert capsys.readouterr().out == ("called PushButton.hide\n")
        testobj.show_button(button, 'value')
        assert capsys.readouterr().out == ("called PushButton.show\n")

    def test_set_textfield_value(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_textfield_value
        """
        field = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_textfield_value(field, 'value')
        assert capsys.readouterr().out == "called LineEdit.setText with arg `value`\n"

    def test_set_label_value(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_label_value
        """
        field = mockqtw.MockLabel()
        assert capsys.readouterr().out == "called Label.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_label_value(field, 'value')
        assert capsys.readouterr().out == "called Label.setText with arg `value`\n"

    def test_set_textbox_value(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_textbox_value
        """
        field = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == "called Editor.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_textbox_value(field, 'value')
        assert capsys.readouterr().out == "called Editor.setPlainText with arg `value`\n"

    def test_get_textfield_value(self, monkeypatch, capsys):
        """unittest for Page1Gui.get_textfield_valuetestobj.on_text
        """
        field = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textfield_value(field) == ""
        assert capsys.readouterr().out == "called LineEdit.text\n"

    # def test_get_label_value(self, monkeypatch, capsys):
    #     """unittest for Page1Gui.get_label_value
    #     """
    #     field = mockqtw.MockLabel()
    #     assert capsys.readouterr().out == "called Label.__init__\n"
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.get_label_value(field) == ""
    #     assert capsys.readouterr().out == "called Label.text\n"

    def test_get_textbox_value(self, monkeypatch, capsys):
        """unittest for Page1Gui.get_textbox_value
        """
        field = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == "called Editor.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textbox_value(field) == "editor text"
        assert capsys.readouterr().out == "called Editor.toPlainText\n"

    def test_set_choice(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_choice
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        domain = ['x', 'y', 'z']
        field = mockqtw.MockComboBox()
        field.itemData = lambda x: ['aaa', 'bbb', 'ccc'][x]
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.set_choice(field, domain, 'bbb')
        assert capsys.readouterr().out == "called ComboBox.setCurrentIndex with arg `1`\n"
        testobj.set_choice(field, domain, 'qqq')
        assert capsys.readouterr().out == ""

    def test_get_choice_index(self, monkeypatch, capsys):
        """unittest for Page1Gui.get_choice_index
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        field = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        assert testobj.get_choice_index(field) == 1
        assert capsys.readouterr().out == "called ComboBox.currentIndex\n"

    def test_get_choice_data(self, monkeypatch, capsys):
        """unittest for Page1Gui.get_choice_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        field = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        field.currentIndex = lambda: 2
        field.currentText = lambda: 'two'
        field.itemData = lambda x: ['aaa', 'bbb', 'ccc'][x]
        assert testobj.get_choice_data(field) == ('ccc', 'two')
        assert capsys.readouterr().out == ""

    def test_set_button_text(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_button_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == 'called PushButton.__init__ with args () {}\n'
        testobj.set_button_text(button, 'value')
        assert capsys.readouterr().out == "called PushButton.setText with arg `value`\n"

    def test_enable_widget(self, monkeypatch, capsys):
        """unittest for Page1Gui.enable_widget
        """
        widget = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.enable_widget(widget, 'state')
        assert capsys.readouterr().out == "called Widget.setEnabled with arg state\n"

    def test_clear_combobox(self, monkeypatch, capsys):
        """unittest for Page1Gui.clear_stats
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cmb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.clear_combobox(cmb)
        assert capsys.readouterr().out == "called ComboBox.clear\n"

    # def test_clear_stats(self, monkeypatch, capsys):
    #     """unittest for Page1Gui.clear_stats
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.stat_choice = mockqtw.MockComboBox()
    #     assert capsys.readouterr().out == "called ComboBox.__init__\n"
    #     testobj.clear_stats()
    #     assert capsys.readouterr().out == "called ComboBox.clear\n"

    # def test_clear_cats(self, monkeypatch, capsys):
    #     """unittest for Page1Gui.clear_cats
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.cat_choice = mockqtw.MockComboBox()
    #     assert capsys.readouterr().out == "called ComboBox.__init__\n"
    #     testobj.clear_cats()
    #     assert capsys.readouterr().out == "called ComboBox.clear\n"

    def test_add_combobox_choice(self, monkeypatch, capsys):
        """unittest for Page1Gui.add_cat_choice
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cmb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.add_combobox_choice(cmb, 'text', 'value')
        assert capsys.readouterr().out == (
                "called ComboBox.addItem with arg `text`, userdata = value\n")

    # def test_add_cat_choice(self, monkeypatch, capsys):
    #     """unittest for Page1Gui.add_cat_choice
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.cat_choice = mockqtw.MockComboBox()
    #     assert capsys.readouterr().out == "called ComboBox.__init__\n"
    #     testobj.add_cat_choice('text', 'value')
    #     assert capsys.readouterr().out == (
    #             "called ComboBox.addItem with arg `text`, userdata = value\n")

    # def test_add_stat_choice(self, monkeypatch, capsys):
    #     """unittest for Page1Gui.add_stat_choice
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.stat_choice = mockqtw.MockComboBox()
    #     assert capsys.readouterr().out == "called ComboBox.__init__\n"
    #     testobj.add_stat_choice('text', 'value')
    #     assert capsys.readouterr().out == (
    #             "called ComboBox.addItem with arg `text`, userdata = value\n")

    # def test_set_focus(self, monkeypatch, capsys):
    #     """unittest for Page1Gui.set_focus
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.proc_entry = mockqtw.MockLineEdit()
    #     assert capsys.readouterr().out == "called LineEdit.__init__ with args ()\n"
    #     testobj.set_focus()
    #     assert capsys.readouterr().out == "called LineEdit.setFocus\n"


class TestPage6Gui:
    """unittest for gui_qt.Page6Gui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.Page6Gui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Page6Gui.__init__ with args', args)
            self.book = parent
            self.master = master
            self.appbase = self.book.parent
        parent = MockBook()
        master = MockPage()
        monkeypatch.setattr(testee.Page6Gui, '__init__', mock_init)
        testobj = testee.Page6Gui(parent, master)
        assert capsys.readouterr().out == (
                'called Page.__init__\n'
                f'called Page6Gui.__init__ with args ({parent}, {master})\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Page6Gui.__init__
        """
        def mock_init(self, parent, master):
            """stub
            """
            print(f'called PageGui.__init__ with args ({parent}, {master})')
            self.book = parent
            self.master = master
            # self.appbase = types.SimpleNamespace(use_rt=False, work_with_user=True)
        parent = MockBook()
        master = MockPage()
        assert capsys.readouterr().out == 'called Page.__init__\n'
        monkeypatch.setattr(testee.PageGui, '__init__', mock_init)
        monkeypatch.setattr(testee.qtw, 'QSplitter', mockqtw.MockSplitter)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee, 'LIN', True)
        testobj = testee.Page6Gui(parent, master)
        assert isinstance(testobj.pnl, testee.qtw.QSplitter)
        # assert isinstance(testobj.progress_list, testee.qtw.QListWidget)
        # assert isinstance(testobj.progress_text, mockqtw.MockEditorWidget)
        # assert isinstance(testobj.new_action, mockqtw.MockShortcut)
        # assert isinstance(testobj.save_button, mockqtw.MockPushButton)
        # assert isinstance(testobj.cancel_button, mockqtw.MockPushButton)
        # assert testobj.actiondict == {'xx': 'yyy'}
        assert capsys.readouterr().out == (
                f"called PageGui.__init__ with args ({parent}, {master})\n"
                "called VBox.__init__\n"
                "called HBox.__init__\n"
                "called Splitter.__init__\n"
                "called Splitter.setOrientation with args (<Orientation.Vertical: 2>,)\n"
                "called Splitter.setSizes with args ((200, 250),)\n"
                "called HBox.addWidget with arg MockSplitter\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")
        # expected_output['page6_init'].format(testobj=testobj, topsize=200, bottomsize=250)

        monkeypatch.setattr(testee, 'LIN', False)
        testobj = testee.Page6Gui(parent, master)
        assert isinstance(testobj.pnl, testee.qtw.QSplitter)
        # assert testobj.actiondict == {'xx': 'yyy'}
        assert capsys.readouterr().out == (
                f"called PageGui.__init__ with args ({parent}, {master})\n"
                "called VBox.__init__\n"
                "called HBox.__init__\n"
                "called Splitter.__init__\n"
                "called Splitter.setOrientation with args (<Orientation.Vertical: 2>,)\n"
                "called Splitter.setSizes with args ((280, 110),)\n"
                "called HBox.addWidget with arg MockSplitter\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")
        # expected_output['page6_init2'].format(testobj=testobj, topsize=280, bottomsize=110)

    def test_create_list(self, monkeypatch, capsys):
        """unittest for Page6Gui.create_list
        """
        monkeypatch.setattr(testee.qtw, 'QListWidget', mockqtw.MockListBox)
        monkeypatch.setattr(testee.gui, 'QShortcut', mockqtw.MockShortcut)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockqtw.MockSplitter()
        assert capsys.readouterr().out == "called Splitter.__init__\n"
        testobj.appbase.work_with_user = False
        assert isinstance(testobj.create_list(), testee.qtw.QListWidget)
        assert isinstance(testobj.new_action, mockqtw.MockShortcut)
        assert capsys.readouterr().out == (
                "called List.__init__\n"
                f"called Signal.connect with args ({testobj.on_select_item},)\n"
                f"called Shortcut.__init__ with args ('Shift+Ctrl+N', {testobj})\n"
                f"called Signal.connect with args ({testobj.on_activate_item},)\n"
                f"called Signal.connect with args ({testobj.on_activate_item},)\n"
                "called Splitter.addWidget with arg MockListBox\n"
                "called Shortcut.__init__ with args"
                f" ('Shift+Ctrl+Up', {testobj}, {testobj.master.goto_prev})\n"
                "called Shortcut.__init__ with args"
                f" ('Shift+Ctrl+Down', {testobj}, {testobj.master.goto_next})\n")
        testobj.appbase.work_with_user = True
        assert isinstance(testobj.create_list(), testee.qtw.QListWidget)
        assert isinstance(testobj.new_action, mockqtw.MockShortcut)
        assert capsys.readouterr().out == (
                "called List.__init__\n"
                f"called Signal.connect with args ({testobj.on_select_item},)\n"
                f"called Shortcut.__init__ with args ('Shift+Ctrl+N', {testobj})\n"
                "called Splitter.addWidget with arg MockListBox\n"
                "called Shortcut.__init__ with args"
                f" ('Shift+Ctrl+Up', {testobj}, {testobj.master.goto_prev})\n"
                "called Shortcut.__init__ with args"
                f" ('Shift+Ctrl+Down', {testobj}, {testobj.master.goto_next})\n")

    def test_create_textfield(self, monkeypatch, capsys):
        """unittest for Page6Gui.create_textfield
        """
        def mock_create(*args):
            print('called Page.create_text_field with args', type(args[0]).__name__, args[1:])
            return 'ptext'
        def mock_data(arg):
            print('called Page.get_toolbar_data with arg', arg)
            return 'toolbardata'
        def mock_toolbar(*args):
            print('called Page.create_toolbar with args', type(args[0]).__name__, args[1:])
        def callback():
            "reference to callback"
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.create_text_field = mock_create
        testobj.master.get_toolbar_data = mock_data
        testobj.create_toolbar = mock_toolbar
        testobj.pnl = mockqtw.MockSplitter()
        assert capsys.readouterr().out == "called Splitter.__init__\n"
        testobj.appbase.use_rt = False
        assert testobj.create_textfield('width', 'height', callback) == 'ptext'
        assert capsys.readouterr().out == (
                "called Frame.__init__\n"
                "called VBox.__init__\n"
                "called HBox.__init__\n"
                "called Page.create_text_field with args"
                f" MockHBoxLayout ('width', 'height', {callback})\n"
                "called VBox.addLayout with arg MockHBoxLayout\n"
                "called Frame.setLayout with arg MockVBoxLayout\n"
                "called Frame.show\n"
                "called Splitter.addWidget with arg MockFrame\n")
        testobj.appbase.use_rt = True
        assert testobj.create_textfield('width', 'height', callback) == 'ptext'
        assert capsys.readouterr().out == (
                "called Frame.__init__\n"
                "called VBox.__init__\n"
                "called HBox.__init__\n"
                "called Page.create_text_field with args"
                f" MockHBoxLayout ('width', 'height', {callback})\n"
                "called Page.get_toolbar_data with arg ptext\n"
                "called Page.create_toolbar with args MockHBoxLayout ('ptext', 'toolbardata')\n"
                "called VBox.addLayout with arg MockHBoxLayout\n"
                "called Frame.setLayout with arg MockVBoxLayout\n"
                "called Frame.show\n"
                "called Splitter.addWidget with arg MockFrame\n")

    # def _test_add_buttons(self, monkeypatch, capsys):
    #     """unittest for Page6Gui.add_buttons
    #     """
    #     monkeypatch.setattr(testee.gui, 'QPushButton', mockqtw.MockPushButton)
    #     monkeypatch.setattr(testee.gui, 'QShortcut', mockqtw.MockShortcut)
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.sizer = mockqtw.MockVBoxLayout()
    #     assert capsys.readouterr().out == "called VBox.__init__\n"
    #     assert testobj.add_buttons() == "expected_result"
    #     # assert isinstance(testobj.save_button, mockqtw.MockPushButton)
    #     # assert isinstance(testobj.cancel_button, mockqtw.MockPushButton)
    #     assert capsys.readouterr().out == ("")

    def test_finish_display(self, monkeypatch, capsys):
        """unittest for Page6Gui.finish_display
        """
        monkeypatch.setattr(testee.PageGui, 'setLayout', mockqtw.MockFrame.setLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.finish_display()
        assert capsys.readouterr().out == "called Frame.setLayout with arg MockVBoxLayout\n"

    def test_on_activate_item(self, monkeypatch, capsys):
        """unittest for Page6Gui.on_activate_item
        """
        def mock_init():
            print('called Page6.initialize_new_event')
        # def mock_item(arg):
        #     print(f"called Page6Gui.is_first_item with arg {arg}")
        #     return False
        # def mock_item_2(arg):
        #     print(f"called Page6Gui.is_first_item with arg {arg}")
        #     return True
        def mock_item(num):
            print(f'called ListWidget.item with arg {num}')
            if num == 0:
                return item1
            return item2
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(initializing=True, initialize_new_event=mock_init)
        item1 = mockqtw.MockListItem()
        item2 = mockqtw.MockListItem()
        testobj.progress_list = mockqtw.MockListBox()
        assert capsys.readouterr().out == ("called ListItem.__init__\ncalled ListItem.__init__\n"
                                           "called List.__init__\n")
        testobj.progress_list.item = mock_item
        # testobj.is_first_line = mock_item
        testobj.on_activate_item()
        assert capsys.readouterr().out == ""
        testobj.master.initializing = False
        testobj.on_activate_item()
        assert capsys.readouterr().out == "called Page6.initialize_new_event\n"
        testobj.on_activate_item(item1)
        assert capsys.readouterr().out == ("called ListWidget.item with arg 0\n"
                                           "called Page6.initialize_new_event\n")
        testobj.on_activate_item(item2)
        assert capsys.readouterr().out == "called ListWidget.item with arg 0\n"

    def test_on_select_item(self, monkeypatch, capsys):
        """unittest for Page6Gui.on_select_item
        """
        class MockTextBox:
            def __repr__(self):
                return "'prtext'"
            def setFocus(self):
                print('called TextField.setFocus')
            def setReadOnly(self, *args):
                print('called TextField.setReadOnly with args', args)
        def mock_protect(*args):
            print('called Page6Gui.protect_textfield with args', args)
        def mock_get_row(*args):
            print('called Page6Gui.get_list_row with args', args)
            return 0
        def mock_get_row2(*args):
            print('called Page6Gui.get_list_row with args', args)
            return 1
        def mock_convert(*args, **kwargs):
            print('called Page6Gui.convert_text with args', args, kwargs)
            return args[1]
        def mock_enable(*args):
            print('called Page6Gui.enable_toolbar with args', args)
        def mock_move(*args):
            print('called Page6Gui.move_cursor_to_end with args', args)
        def mock_set_focus():
            print('called Page6Gui.set_focus_to_textfield')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.event_data = ['xxx']
        testobj.master.progress_list = 'prlist'
        testobj.master.progress_text = MockTextBox()
        testobj.book.pagedata = types.SimpleNamespace(arch=False)
        testobj.appbase.is_user = False
        testobj.protect_textfield = mock_protect
        testobj.get_list_row = mock_get_row
        testobj.convert_text = mock_convert
        testobj.enable_toolbar = mock_enable
        testobj.move_cursor_to_end = mock_move
        testobj.set_focus_to_textfield = mock_set_focus
        testobj.on_select_item(None, 'item_o')
        assert capsys.readouterr().out == (
                "called TextField.setReadOnly with args (True,)\n")

        testobj.on_select_item('item_n', 'item_o')
        assert testobj.current_item == 0
        assert testobj.master.oldtext == ''
        assert capsys.readouterr().out == (
                "called TextField.setReadOnly with args (True,)\n"
                "called Page6Gui.get_list_row with args ('prlist',)\n"
                "called Page6Gui.convert_text with args ('prtext', '') {'to': 'rich'}\n"
                "called Page6Gui.move_cursor_to_end with args ('prtext',)\n"
                "called TextField.setFocus\n")

        testobj.get_list_row = mock_get_row2
        testobj.appbase.use_rt = False
        testobj.on_select_item('item_n', 'item_o')
        assert testobj.current_item == 1
        assert testobj.master.oldtext == 'xxx'
        assert capsys.readouterr().out == (
                "called TextField.setReadOnly with args (True,)\n"
                "called Page6Gui.get_list_row with args ('prlist',)\n"
                "called Page6Gui.convert_text with args ('prtext', 'xxx') {'to': 'rich'}\n"
                "called TextField.setReadOnly with args (True,)\n"
                "called Page6Gui.move_cursor_to_end with args ('prtext',)\n"
                "called TextField.setFocus\n")
        testobj.appbase.use_rt = True
        testobj.toolbar = 'toolbar'
        testobj.on_select_item('item_n', 'item_o')
        assert testobj.current_item == 1
        assert testobj.master.oldtext == 'xxx'
        assert capsys.readouterr().out == (
                "called TextField.setReadOnly with args (True,)\n"
                "called Page6Gui.get_list_row with args ('prlist',)\n"
                "called Page6Gui.convert_text with args ('prtext', 'xxx') {'to': 'rich'}\n"
                "called TextField.setReadOnly with args (True,)\n"
                "called Page6Gui.enable_toolbar with args ('toolbar', False)\n"
                "called Page6Gui.move_cursor_to_end with args ('prtext',)\n"
                "called TextField.setFocus\n")

        testobj.book.pagedata.arch = True
        testobj.get_list_row = mock_get_row
        testobj.on_select_item('item_n', 'item_o')
        assert testobj.current_item == 0
        assert testobj.master.oldtext == ''
        assert capsys.readouterr().out == (
                "called TextField.setReadOnly with args (True,)\n"
                "called Page6Gui.get_list_row with args ('prlist',)\n"
                "called Page6Gui.convert_text with args ('prtext', '') {'to': 'rich'}\n"
                "called TextField.setFocus\n")

        testobj.get_list_row = mock_get_row2
        testobj.on_select_item('item_n', 'item_o')
        assert testobj.current_item == 1
        assert testobj.master.oldtext == 'xxx'
        assert capsys.readouterr().out == (
                "called TextField.setReadOnly with args (True,)\n"
                "called Page6Gui.get_list_row with args ('prlist',)\n"
                "called Page6Gui.convert_text with args ('prtext', 'xxx') {'to': 'rich'}\n"
                "called TextField.setFocus\n")

    def test_create_new_listitem(self, monkeypatch, capsys):
        """unittest for Page6Gui.create_new_listitem
        """
        monkeypatch.setattr(testee.qtw, 'QListWidgetItem', mockqtw.MockListItem)
        listbox = mockqtw.MockListBox()
        textfield = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == "called List.__init__\ncalled Editor.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.create_new_listitem(listbox, textfield, 'datum', 'oldtext')
        assert capsys.readouterr().out == (
                "called ListItem.__init__ with args ('datum - oldtext',)\n"
                "called ListItem.setData with args (<ItemDataRole.UserRole: 256>, 0)\n"
                "called List.insertItem with args (1, MockListItem)\n"
                "called List.setCurrentRow with arg 1\n"
                "called Editor.setText with arg `oldtext`\n"
                "called Editor.setReadOnly with arg `False`\ncalled Editor.setFocus\n")

    # def test_is_first_line(self, monkeypatch, capsys):
    #     """unittest for Page6Gui.is_first_line
    #     """
    #     def mock_item(num):
    #         print(f'called ListWidget.item with arg {num}')
    #         if num == 0:
    #             return item1
    #         return item2
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     item1 = mockqtw.MockListItem()
    #     item2 = mockqtw.MockListItem()
    #     testobj.progress_list = mockqtw.MockListBox()
    #     assert capsys.readouterr().out == ("called ListItem.__init__\ncalled ListItem.__init__\n"
    #                                        "called List.__init__\n")
    #     testobj.progress_list.item = mock_item
    #     assert testobj.is_first_line(item1)
    #     assert capsys.readouterr().out == "called ListWidget.item with arg 0\n"
    #     assert not testobj.is_first_line(item2)
    #     assert capsys.readouterr().out == "called ListWidget.item with arg 0\n"

    def test_clear_list(self, monkeypatch, capsys):
        """unittest for Page6Gui.clear_list
        """
        listbox = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.clear_list(listbox)
        assert capsys.readouterr().out == ("called List.clear\n")

    def test_add_first_listitem(self, monkeypatch, capsys):
        """unittest for Page6Gui.add_first_listitem
        """
        monkeypatch.setattr(testee.qtw, 'QListWidgetItem', mockqtw.MockListItem)
        listbox = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_first_listitem(listbox, 'text')
        first_item = listbox.list[0]
        assert capsys.readouterr().out == (
                "called ListItem.__init__ with args ('text',)\n"
                "called ListItem.setData with args (<ItemDataRole.UserRole: 256>, -1)\n"
                f"called List.addItem with arg `{first_item}`\n")

    def test_add_item_to_list(self, monkeypatch, capsys):
        """unittest for Page6Gui.add_item_to_list
        """
        def mock_set(data):
            print(f"called Editor.set_contents with arg '{data}'")
        def mock_text():
            print("called Editor.toPlainText")
            return testobj.master.event_data[0]
        def mock_text_2():
            print("called Editor.toPlainText")
            return testobj.master.event_data[1]
        def mock_add(*args):
            print('called List.addItem')
        monkeypatch.setattr(testee.qtw, 'QListWidgetItem', mockqtw.MockListItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        progress_list = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        progress_list.addItem = mock_add
        testobj.master = types.SimpleNamespace(event_data=['xxxxxx', 10 * '1234567890'])
        testobj.master.progress_text = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == "called Editor.__init__\n"
        testobj.master.progress_text.set_contents = mock_set
        testobj.master.progress_text.toPlainText = mock_text
        testobj.add_item_to_list(progress_list, testobj.master.progress_text, 0, 'datum')
        assert capsys.readouterr().out == (
            f"called Editor.set_contents with arg '{testobj.master.event_data[0]}'\n"
            "called Editor.toPlainText\n"
            f"called ListItem.__init__ with args ('datum - {testobj.master.event_data[0]}',)\n"
            f"called ListItem.setData with args ({testee.core.Qt.ItemDataRole.UserRole!r}, 0)\n"
            "called List.addItem\n")
        testobj.master.progress_text.toPlainText = mock_text_2
        testobj.add_item_to_list(progress_list, testobj.master.progress_text, 1, 'datum')
        text = 8 * '1234567890' + '...'
        assert capsys.readouterr().out == (
            f"called Editor.set_contents with arg '{testobj.master.event_data[1]}'\n"
            "called Editor.toPlainText\n"
            f"called ListItem.__init__ with args ('datum - {text}',)\n"
            f"called ListItem.setData with args ({testee.core.Qt.ItemDataRole.UserRole!r}, 1)\n"
            "called List.addItem\n")

    def test_set_list_callbacks(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_list_callback
        """
        def callback1():
            "stub for reference"
        def callback2():
            "stub for reference"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.appbase = types.SimpleNamespace(is_user=True)
        testobj.on_activate_item = lambda: 'dummy'
        progress_list = mockqtw.MockListBox()
        testobj.new_action = mockqtw.MockShortcut()
        assert capsys.readouterr().out == ("called List.__init__\n"
                                           "called Shortcut.__init__ with args ()\n")
        testobj.set_list_callbacks(progress_list, callback1, callback2)
        assert capsys.readouterr().out == (
                f"called Signal.connect with args ({callback1},)\n"
                f"called Signal.connect with args ({callback2},)\n")
        testobj.appbase.is_user = False
        testobj.set_list_callbacks(progress_list, callback1, callback2)
        assert capsys.readouterr().out == ("called Signal.disconnect\n"
                                           "called Signal.disconnect\n")

    def test_set_listitem_text(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_listitem_text
        """
        def mock_item(indx):
            result = mockqtw.MockListItem()
            assert capsys.readouterr().out == "called ListItem.__init__\n"
            print(f'called List.item with arg {indx}')
            return result
        testobj = self.setup_testobj(monkeypatch, capsys)
        progress_list = mockqtw.MockListBox()
        progress_list.item = mock_item
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj.set_listitem_text(progress_list, 1, 'text')
        assert capsys.readouterr().out == ("called List.item with arg 1\n"
                                           "called ListItem.setText with arg 'text'\n")

    def test_set_listitem_data(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_listitem_data
        """
        def mock_item(indx):
            result = mockqtw.MockListItem()
            assert capsys.readouterr().out == "called ListItem.__init__\n"
            print(f'called List.item with arg {indx}')
            return result
        testobj = self.setup_testobj(monkeypatch, capsys)
        progress_list = mockqtw.MockListBox()
        progress_list.item = mock_item
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj.set_listitem_data(progress_list, 1)
        assert capsys.readouterr().out == ("called List.item with arg 1\n"
                                           "called ListItem.setData with args"
                                           f" (0, {testee.core.Qt.ItemDataRole.UserRole!r})\n")

    def test_get_listitem_text(self, monkeypatch, capsys):
        """unittest for Page6Gui.get_listitem_text
        """
        def mock_item(indx):
            result = mockqtw.MockListItem('xxx')
            assert capsys.readouterr().out == "called ListItem.__init__ with args ('xxx',)\n"
            print(f'called List.item with arg {indx}')
            return result
        testobj = self.setup_testobj(monkeypatch, capsys)
        progress_list = mockqtw.MockListBox()
        progress_list.item = mock_item
        assert capsys.readouterr().out == "called List.__init__\n"
        assert testobj.get_listitem_text(progress_list, 'itemindex') == "xxx"
        assert capsys.readouterr().out == ("called List.item with arg itemindex\n"
                                           "called ListItem.text\n")

    def test_get_list_row(self, monkeypatch, capsys):
        """unittest for Page6Gui.get_list_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        progress_list = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        assert testobj.get_list_row(progress_list) == "current row"
        assert capsys.readouterr().out == ("called List.currentRow\n")

    def test_set_list_row(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_list_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        progress_list = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj.set_list_row(progress_list, 'num')
        assert capsys.readouterr().out == ("called List.setCurrentRow with arg num\n")

    def test_get_list_rowcount(self, monkeypatch, capsys):
        """unittest for Page6Gui.get_list_rowcount
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        progress_list = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        assert testobj.get_list_rowcount(progress_list) == 0
        assert capsys.readouterr().out == "called List.count\n"

    def test_clear_textfield(self, monkeypatch, capsys):
        """unittest for Page6Gui.clear_textfield
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        progress_text = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == "called Editor.__init__\n"
        testobj.clear_textfield(progress_text)
        assert capsys.readouterr().out == ("called Editor.clear\n")

    def test_get_textfield_contents(self, monkeypatch, capsys):
        """unittest for Page6Gui.get_textfield_contents
        """
        def mock_get():
            print('called Editor.get_contents')
            return 'editor text'
        testobj = self.setup_testobj(monkeypatch, capsys)
        progress_text = mockqtw.MockEditorWidget()
        progress_text.get_contents = mock_get
        assert capsys.readouterr().out == "called Editor.__init__\n"
        assert testobj.get_textfield_contents(progress_text) == "editor text"
        assert capsys.readouterr().out == ("called Editor.get_contents\n")

    def test_set_textfield_contents(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_textfield_contents
        """
        def mock_set(value):
            print(f"called Editor.set_contents with arg '{value}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        progress_text = mockqtw.MockEditorWidget()
        progress_text.set_contents = mock_set
        assert capsys.readouterr().out == "called Editor.__init__\n"
        testobj.set_textfield_contents(progress_text, 'text')
        assert capsys.readouterr().out == ("called Editor.set_contents with arg 'text'\n")

    def test_move_cursor_to_end(self, monkeypatch, capsys):
        """unittest for Page6Gui.move_cursor_to_end
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        progress_text = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == "called Editor.__init__\n"
        testobj.move_cursor_to_end(progress_text)
        assert capsys.readouterr().out == ("called Editor.moveCursor with args"
                                           f" ({testee.gui.QTextCursor.MoveOperation.End!r},"
                                           f" {testee.gui.QTextCursor.MoveMode.MoveAnchor!r})\n")

    def test_convert_text(self, monkeypatch, capsys):
        """unittest for Page6Gui.convert_text
        """
        def mock_set(value):
            print(f"called Editor.set_contents with arg '{value}'")
        def mock_get():
            print("called Editor.get_contents")
            return 'editor text'
        testobj = self.setup_testobj(monkeypatch, capsys)
        progress_text = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == "called Editor.__init__\n"
        progress_text.set_contents = mock_set
        progress_text.get_contents = mock_get
        assert testobj.convert_text(progress_text, 'text', 'rich') == "editor text"
        assert capsys.readouterr().out == ("called Editor.set_contents with arg 'text'\n"
                                          "called Editor.get_contents\n")
        assert testobj.convert_text(progress_text, 'text', 'plain') == "editor text"
        assert capsys.readouterr().out == ("called Editor.toPlainText\n")


class TestSortOptionsDialogGui:
    """unittests for qtgui.SortOptionsDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.SortOptionsDialogGui object

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
        parent = types.SimpleNamespace(gui='SortOptionsDialogGui')
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        testobj = testee.SortOptionsDialogGui('master', parent, 'title')
        assert testobj.master == 'master'
        assert isinstance(testobj.sizer, testee.qtw.QVBoxLayout)
        assert isinstance(testobj.grid, testee.qtw.QGridLayout)
        assert testobj.row == 0
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args SortOptionsDialogGui () {}\n"
                "called Dialog.setWindowTitle with args ('title',)\n"
                "called VBox.__init__\n"
                "called Grid.__init__\n"
                "called VBox.addLayout with arg MockGridLayout\n"
                "called Dialog.setLayout with arg MockVBoxLayout\n")

    def test_add_checkbox_line(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.add_checkbox_line
        """
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.row = 0
        testobj.grid = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        result = testobj.add_checkbox_line('tekst', 'checked', 'callback')
        assert isinstance(result, testee.qtw.QCheckBox)
        assert testobj.row == 0
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ('tekst', {testobj})\n"
                "called CheckBox.setChecked with arg checked\n"
                "called Signal.connect with args ('callback',)\n"
                "called Grid.addWidget with arg MockCheckBox at (0, 0, 1, 4)\n")

    def test_add_seqnumtext_to_list(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.add_seqnumtext_to_list
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.row = 0
        result = testobj.add_seqnumtext_to_list('label')
        assert isinstance(result, testee.qtw.QLabel)
        assert testobj.row == 1
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('label', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at (1, 0)\n")

    def test_add_colnameselector_to_list(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.add_colnameselector_to_list
        """
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.row = 0
        result = testobj.add_colnameselector_to_list('name', ['lijst', 'name'])
        assert isinstance(result, testee.qtw.QComboBox)
        assert testobj.row == 0
        assert capsys.readouterr().out == (
                "called ComboBox.__init__\n"
                "called ComboBox.setEditable with arg `False`\n"
                "called ComboBox.addItems with arg ['lijst', 'name']\n"
                "called ComboBox.setCurrentIndex with arg `1`\n"
                "called Grid.addWidget with arg MockComboBox at (0, 1)\n")

    def test_add_radiobuttons_to_line(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.add_radiobuttons_to_line
        """
        monkeypatch.setattr(testee.qtw, 'QButtonGroup', mockqtw.MockButtonGroup)
        monkeypatch.setattr(testee.qtw, 'QRadioButton', mockqtw.MockRadioButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.row = 0
        result = testobj.add_radiobuttons_to_line([('xx', 'A', True), ('yy', 'D', False)])
        assert isinstance(result, testee.qtw.QButtonGroup)
        assert testobj.row == 0
        assert capsys.readouterr().out == (
                f"called ButtonGroup.__init__ with args ({testobj},)\n"
                f"called RadioButton.__init__ with args ('xx', {testobj}) {{}}\n"
                "called RadioButton.setChecked with arg `True`\n"
                "called ButtonGroup.addButton with arg MockRadioButton and id A\n"
                "called Grid.addWidget with arg MockRadioButton at (0, 2)\n"
                f"called RadioButton.__init__ with args ('yy', {testobj}) {{}}\n"
                "called RadioButton.setChecked with arg `False`\n"
                "called ButtonGroup.addButton with arg MockRadioButton and id D\n"
                "called Grid.addWidget with arg MockRadioButton at (0, 3)\n")

    def test_add_okcancel_buttonbox(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.add_okcancel_buttonbox
        """
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_okcancel_buttonbox()
        assert capsys.readouterr().out == (
                "called ButtonBox.__init__ with args (3,)\n"
                f"called Signal.connect with args ({testobj.accept},)\n"
                f"called Signal.connect with args ({testobj.reject},)\n"
                "called VBox.addWidget with arg MockButtonBox\n")

    def test_enable_fields(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.enable_fields
        """
        def mock_buttons1():
            return btn1, btn2
        def mock_buttons2():
            return btn3, btn4
        cmb1 = mockqtw.MockComboBox()
        cmb2 = mockqtw.MockComboBox()
        btn1 = mockqtw.MockPushButton()
        btn2 = mockqtw.MockPushButton()
        btn3 = mockqtw.MockPushButton()
        btn4 = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called ComboBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n")
        rbg1 = types.SimpleNamespace(buttons=mock_buttons1)
        rbg2 = types.SimpleNamespace(buttons=mock_buttons2)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(widgets=[('lbl1', cmb1, rbg1), ('lbl2', cmb2, rbg2)])
        testobj.enable_fields('state')
        assert capsys.readouterr().out == ("called ComboBox.setEnabled with arg state\n"
                                           "called PushButton.setEnabled with arg `state`\n"
                                           "called PushButton.setEnabled with arg `state`\n"
                                           "called ComboBox.setEnabled with arg state\n"
                                           "called PushButton.setEnabled with arg `state`\n"
                                           "called PushButton.setEnabled with arg `state`\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.accept
        """
        def mock_confirm():
            print('called SortOptionsDialog.confirm')
            return False
        def mock_confirm2():
            print('called SortOptionsDialog.confirm')
            return True
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == ("called SortOptionsDialog.confirm\n")
        testobj.master.confirm = mock_confirm2
        testobj.accept()
        assert capsys.readouterr().out == ("called SortOptionsDialog.confirm\n"
                                           "called Dialog.accept\n")

    def test_get_combobox_value(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.get_combobox_value
        """
        cmb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_combobox_value(cmb) == "current text"
        assert capsys.readouterr().out == ("called ComboBox.currentText\n")

    def test_get_rbgroup_value(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.get_rbgroup_value
        """
        rbg = mockqtw.MockButtonGroup()
        assert capsys.readouterr().out == "called ButtonGroup.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_rbgroup_value(rbg) is None
        assert capsys.readouterr().out == ("called ButtonGroup.checkediId\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for SortOptionsDialogGui.get_checkbox_value
        """
        cb = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert not testobj.get_checkbox_value(cb)
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n")


class TestSelectOptionsDialogGui:
    """unittests for qtgui.SelectOptionsDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.SelectOptionsDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SelectOptionsDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.SelectOptionsDialogGui, '__init__', mock_init)
        testobj = testee.SelectOptionsDialogGui()
        assert capsys.readouterr().out == 'called SelectOptionsDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.__init__
        """
        parent = types.SimpleNamespace(gui='SelectOptionsDialogGui')
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QButtonGroup', mockqtw.MockButtonGroup)
        testobj = testee.SelectOptionsDialogGui('master', parent, 'title')
        assert isinstance(testobj.sizer, testee.qtw.QVBoxLayout)
        assert isinstance(testobj.grid, testee.qtw.QGridLayout)
        assert isinstance(testobj._cbg, testee.qtw.QButtonGroup)
        assert testobj.extra_cbgs == []
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args SelectOptionsDialogGui () {}\n"
                "called Dialog.setWindowTitle with args ('title',)\n"
                "called VBox.__init__\ncalled Grid.__init__\n"
                "called VBox.addLayout with arg MockGridLayout\n"
                "called ButtonGroup.__init__ with args ()\n"
                "called ButtonGroup.setExclusive with arg False\n"
                "called Dialog.setLayout with arg MockVBoxLayout\n")

    def test_add_checkbox_to_grid(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.add_checkbox_to_grid
        """
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._cbg = mockqtw.MockButtonGroup()
        testobj.grid = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == ("called ButtonGroup.__init__ with args ()\n"
                                           "called Grid.__init__\n")
        result = testobj.add_checkbox_to_grid('title', 'row', 'col')
        assert isinstance(result, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
                "called VBox.__init__\n"
                f"called CheckBox.__init__ with args ('title', {testobj})\n"
                "called ButtonGroup.addButton with arg MockCheckBox\n"
                "called VBox.addWidget with arg MockCheckBox\n"
                "called VBox.addStretch\n"
                "called Grid.addLayout with arg MockVBoxLayout at ('row', 'col')\n")

    def test_start_optionsblock(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.start_optionsblock
        """
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        assert isinstance(testobj.start_optionsblock(), testee.qtw.QGridLayout)
        assert testobj.blockrow == -1
        assert capsys.readouterr().out == "called Grid.__init__\n"

    def test_add_textentry_line_to_block(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.add_textentry_line_to_block
        """
        def callback():
            "stub; need a callable here"
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        block = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.blockrow = 0
        result = testobj.add_textentry_line_to_block(block, 'text', callback)
        assert isinstance(result, testee.qtw.QLineEdit)
        assert testobj.blockrow == 1
        assert capsys.readouterr().out == (
                f"called LineEdit.__init__ with args ({testobj},)\n"
                f"called Label.__init__ with args ('text', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at (1, 0)\n"
                f"called Signal.connect with args (functools.partial({callback}, {result}),)\n"
                "called Grid.addWidget with arg MockLineEdit at (1, 1)\n")
        testobj.blockrow = 0
        result = testobj.add_textentry_line_to_block(block, 'text', callback, first=True)
        assert isinstance(result, testee.qtw.QLineEdit)
        assert testobj.blockrow == 1
        assert capsys.readouterr().out == (
                f"called LineEdit.__init__ with args ({testobj},)\n"
                f"called Label.__init__ with args ('text', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at (1, 0)\n"
                f"called Signal.connect with args (functools.partial({callback}, {result}),)\n"
                "called Grid.addWidget with arg MockLineEdit at (1, 1)\n")

    def test_add_radiobuttonrow_to_block(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.add_radiobuttonrow_to_block
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QButtonGroup', mockqtw.MockButtonGroup)
        monkeypatch.setattr(testee.qtw, 'QRadioButton', mockqtw.MockRadioButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        block = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.blockrow = 0
        buttondefs = ['xxx', 'yyy']
        result = testobj.add_radiobuttonrow_to_block(block, buttondefs)
        assert len(result) == len(buttondefs)
        for item in result:
            assert isinstance(item, testee.qtw.QRadioButton)
        assert testobj.blockrow == 1
        assert capsys.readouterr().out == (
                f"called ButtonGroup.__init__ with args ({testobj},)\n"
                "called HBox.__init__\n"
                f"called RadioButton.__init__ with args ('xxx', {testobj}) {{}}\n"
                "called ButtonGroup.addButton with arg MockRadioButton\n"
                "called HBox.addWidget with arg MockRadioButton\n"
                f"called RadioButton.__init__ with args ('yyy', {testobj}) {{}}\n"
                "called ButtonGroup.addButton with arg MockRadioButton\n"
                "called HBox.addWidget with arg MockRadioButton\n"
                "called HBox.addStretch\n"
                "called Grid.addLayout with arg MockHBoxLayout at (1, 0)\n"
                "called ButtonGroup.buttons\n")
        testobj.blockrow = 0
        result = testobj.add_radiobuttonrow_to_block(block, buttondefs, 'callback', False)
        assert len(result) == len(buttondefs)
        for item in result:
            assert isinstance(item, testee.qtw.QRadioButton)
        assert testobj.blockrow == 1
        assert capsys.readouterr().out == (
                f"called ButtonGroup.__init__ with args ({testobj},)\n"
                "called HBox.__init__\n"
                f"called RadioButton.__init__ with args ('xxx', {testobj}) {{}}\n"
                "called ButtonGroup.addButton with arg MockRadioButton\n"
                "called Signal.connect with args ('callback',)\n"
                "called HBox.addWidget with arg MockRadioButton\n"
                f"called RadioButton.__init__ with args ('yyy', {testobj}) {{}}\n"
                "called ButtonGroup.addButton with arg MockRadioButton\n"
                "called Signal.connect with args ('callback',)\n"
                "called HBox.addWidget with arg MockRadioButton\n"
                "called Grid.addLayout with arg MockHBoxLayout at (1, 0)\n"
                "called ButtonGroup.buttons\n")

    def test_add_checkboxlist_to_block(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.add_checkboxlist_to_grid
        """
        def callback():
            "stub; need a callable here"
        monkeypatch.setattr(testee.qtw, 'QButtonGroup', mockqtw.MockButtonGroup)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.blockrow = 0
        testobj.extra_cbgs = []
        block = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        namelist = [('xxx', 'x'), ('yyy', 'y')]
        result = testobj.add_checkboxlist_to_block(block, namelist, callback)
        assert testobj.blockrow == 1
        assert len(result) == len(namelist)
        for item in result:
            assert isinstance(item, testee.qtw.QCheckBox)
        assert len(testobj.extra_cbgs) == 1
        assert isinstance(testobj.extra_cbgs[0], testee.qtw.QButtonGroup)
        assert capsys.readouterr().out == (
                f"called ButtonGroup.__init__ with args ({testobj},)\n"
                "called ButtonGroup.setExclusive with arg False\n"
                "called VBox.__init__\n"
                f"called CheckBox.__init__ with args (('xxx', 'x'), {testobj})\n"
                f"called Signal.connect with args (functools.partial({callback}, {result[0]}),)\n"
                "called VBox.addWidget with arg MockCheckBox\n"
                "called ButtonGroup.addButton with arg MockCheckBox\n"
                f"called CheckBox.__init__ with args (('yyy', 'y'), {testobj})\n"
                f"called Signal.connect with args (functools.partial({callback}, {result[1]}),)\n"
                "called VBox.addWidget with arg MockCheckBox\n"
                "called ButtonGroup.addButton with arg MockCheckBox\n"
                "called Grid.addLayout with arg MockVBoxLayout at (1, 0)\n"
                "called ButtonGroup.buttons\n")

    def test_finish_block(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.finish_block
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        block = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.finish_block(block, 'row', 'col')
        assert capsys.readouterr().out == (
                "called Grid.addLayout with arg MockGridLayout at ('row', 'col')\n")

    def test_add_okcancel_buttonbar(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.add_okcancel_buttonbar
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_okcancel_buttonbar()
        assert capsys.readouterr().out == (
                "called ButtonBox.__init__ with args (3,)\n"
                f"called Signal.connect with args ({testobj.accept},)\n"
                f"called Signal.connect with args ({testobj.reject},)\n"
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                "called HBox.addWidget with arg MockButtonBox\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_finalize_display(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.finalize_display
        """
        # testobj = self.setup_testobj(monkeypatch, capsys)
        # assert testobj.finalize_display() == "expected_result"
        # assert capsys.readouterr().out == ("")

    # def _test_doelayout(self, monkeypatch, capsys):
    #     """unittest for SelectOptionsDialogGui.doelayout
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.doelayout() == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def test_set_textentry_value(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.set_textentry_value with args ('Page1Gui',)
        """
        textentry = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_textentry_value(textentry, 'value')
        assert capsys.readouterr().out == ("called LineEdit.setText with arg `value`\n")

    def test_set_radiobutton_value(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.set_radiobutton_value
        """
        radiobutton = mockqtw.MockRadioButton()
        assert capsys.readouterr().out == "called RadioButton.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_radiobutton_value(radiobutton, 'value')
        assert capsys.readouterr().out == ("called RadioButton.setChecked with arg `value`\n")

    def test_set_checkbox_value(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.set_checkbox_value
        """
        checkbox = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_checkbox_value(checkbox, 'value')
        assert capsys.readouterr().out == ("called CheckBox.setChecked with arg value\n")

    def test_on_text(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.on_text
        """
        btn1 = mockqtw.MockRadioButton()
        btn2 = mockqtw.MockRadioButton()
        assert capsys.readouterr().out == ("called RadioButton.__init__ with args () {}\n"
                                           "called RadioButton.__init__ with args () {}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        # testobj.check_options = types.SimpleNamespace(buttons=lambda *x: [btn1, '', '', btn2])
        testobj._cbg = types.SimpleNamespace(buttons=lambda *x: [btn1, '', '', btn2])
        testobj.master = types.SimpleNamespace()

        testobj.master.text_lt = mockqtw.MockLineEdit('text_lt')
        testobj.master.text_gt = mockqtw.MockLineEdit('text_gt')
        assert capsys.readouterr().out == ("called LineEdit.__init__ with args ('text_lt',)\n"
                                           "called LineEdit.__init__ with args ('text_gt',)\n")
        assert testobj.on_text('gt', 'text') == btn1
        assert capsys.readouterr().out == ("called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_text('gt', '') == btn1
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_text('lt', 'text') == btn1
        assert capsys.readouterr().out == ("called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_text('lt', '') == btn1
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called RadioButton.setChecked with arg `True`\n")

        testobj.master.text_lt = mockqtw.MockLineEdit('')
        testobj.master.text_gt = mockqtw.MockLineEdit('')
        assert capsys.readouterr().out == ("called LineEdit.__init__ with args ('',)\n"
                                           "called LineEdit.__init__ with args ('',)\n")
        assert capsys.readouterr().out == ("")
        assert testobj.on_text('gt', 'text') == btn1
        assert capsys.readouterr().out == ("called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_text('gt', '') == btn1
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called RadioButton.setChecked with arg `False`\n")
        assert testobj.on_text('lt', 'text') == btn1
        assert capsys.readouterr().out == ("called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_text('lt', '') == btn1
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called RadioButton.setChecked with arg `False`\n")

        testobj.master.text_lt = mockqtw.MockLineEdit('text_lt')
        testobj.master.text_gt = mockqtw.MockLineEdit('')
        assert capsys.readouterr().out == ("called LineEdit.__init__ with args ('text_lt',)\n"
                                           "called LineEdit.__init__ with args ('',)\n")
        testobj.on_text('gt', 'text')
        assert capsys.readouterr().out == ("called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_text('gt', '') == btn1
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_text('lt', 'text') == btn1
        assert capsys.readouterr().out == ("called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_text('lt', '') == btn1
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called RadioButton.setChecked with arg `False`\n")

        testobj.master.text_lt = mockqtw.MockLineEdit('')
        testobj.master.text_gt = mockqtw.MockLineEdit('text_gt')
        assert capsys.readouterr().out == ("called LineEdit.__init__ with args ('',)\n"
                                           "called LineEdit.__init__ with args ('text_gt',)\n")
        testobj.on_text('gt', 'text')
        assert capsys.readouterr().out == ("called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_text('gt', '') == btn1
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called RadioButton.setChecked with arg `False`\n")
        assert testobj.on_text('lt', 'text') == btn1
        assert capsys.readouterr().out == ("called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_text('lt', '') == btn1
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called RadioButton.setChecked with arg `True`\n")

        testobj.master.text_zoek = mockqtw.MockLineEdit('text_zoek')
        testobj.master.text_zoek2 = mockqtw.MockLineEdit('text_zoek2')
        assert capsys.readouterr().out == ("called LineEdit.__init__ with args ('text_zoek',)\n"
                                           "called LineEdit.__init__ with args ('text_zoek2',)\n")
        assert testobj.on_text('zoek2', 'text') == btn2
        assert capsys.readouterr().out == ("called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_text('zoek2', '') == btn2
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_text('zoek', 'text') == btn2
        assert capsys.readouterr().out == ("called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_text('zoek', '') == btn2
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called RadioButton.setChecked with arg `True`\n")

        testobj.master.text_zoek = mockqtw.MockLineEdit('')
        testobj.master.text_zoek2 = mockqtw.MockLineEdit('')
        assert capsys.readouterr().out == ("called LineEdit.__init__ with args ('',)\n"
                                           "called LineEdit.__init__ with args ('',)\n")
        assert capsys.readouterr().out == ("")
        assert testobj.on_text('zoek2', 'text') == btn2
        assert capsys.readouterr().out == ("called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_text('zoek2', '') == btn2
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called RadioButton.setChecked with arg `False`\n")
        assert testobj.on_text('zoek', 'text') == btn2
        assert capsys.readouterr().out == ("called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_text('zoek', '') == btn2
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called RadioButton.setChecked with arg `False`\n")

        testobj.master.text_zoek = mockqtw.MockLineEdit('text_zoek')
        testobj.master.text_zoek2 = mockqtw.MockLineEdit('')
        assert capsys.readouterr().out == ("called LineEdit.__init__ with args ('text_zoek',)\n"
                                           "called LineEdit.__init__ with args ('',)\n")
        testobj.on_text('zoek2', 'text')
        assert capsys.readouterr().out == ("called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_text('zoek2', '') == btn2
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_text('zoek', 'text') == btn2
        assert capsys.readouterr().out == ("called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_text('zoek', '') == btn2
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called RadioButton.setChecked with arg `False`\n")

        testobj.master.text_zoek = mockqtw.MockLineEdit('')
        testobj.master.text_zoek2 = mockqtw.MockLineEdit('text_zoek2')
        assert capsys.readouterr().out == ("called LineEdit.__init__ with args ('',)\n"
                                           "called LineEdit.__init__ with args ('text_zoek2',)\n")
        testobj.on_text('zoek2', 'text')
        assert capsys.readouterr().out == ("called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_text('zoek2', '') == btn2
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called RadioButton.setChecked with arg `False`\n")
        assert testobj.on_text('zoek', 'text') == btn2
        assert capsys.readouterr().out == ("called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_text('zoek', '') == btn2
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called RadioButton.setChecked with arg `True`\n")

    def test_on_cb_checked(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.on_cb_checked
        """
        def mock_buttons():
            print('called ButtonGroup.buttons for cat buttongroup')
            return cb1, cb2
        def mock_buttons_2():
            print('called ButtonGroup.buttons for stat buttongroup')
            return cb3, cb4
        def mock_buttons_3():
            print('called ButtonGroup.buttons for main buttongroup')
            return '', rb1, rb2
        cb1 = mockqtw.MockCheckBox()
        cb2 = mockqtw.MockCheckBox()
        cb3 = mockqtw.MockCheckBox()
        cb4 = mockqtw.MockCheckBox()
        rb1 = mockqtw.MockRadioButton()
        rb2 = mockqtw.MockRadioButton()
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called RadioButton.__init__ with args () {}\n"
                                           "called RadioButton.__init__ with args () {}\n")
        cbg1 = types.SimpleNamespace(buttons=mock_buttons)
        cbg2 = types.SimpleNamespace(buttons=mock_buttons_2)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._cbg = types.SimpleNamespace(buttons=mock_buttons_3)
        testobj.extra_cbgs = [cbg1, cbg2]
        assert testobj.on_cb_checked(cb1) == (cb2, rb1)
        assert capsys.readouterr().out == ("called ButtonGroup.buttons for cat buttongroup\n"
                                           "called ButtonGroup.buttons for main buttongroup\n"
                                           "called ButtonGroup.buttons for cat buttongroup\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called RadioButton.setChecked with arg `False`\n")
        assert testobj.on_cb_checked(cb4) == (cb4, rb2)
        assert capsys.readouterr().out == ("called ButtonGroup.buttons for cat buttongroup\n"
                                           "called ButtonGroup.buttons for stat buttongroup\n"
                                           "called ButtonGroup.buttons for main buttongroup\n"
                                           "called ButtonGroup.buttons for stat buttongroup\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called RadioButton.setChecked with arg `False`\n")

        cb1.setChecked(True)
        cb4.setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n")
        assert testobj.on_cb_checked(cb1) == (cb1, rb1)
        assert capsys.readouterr().out == ("called ButtonGroup.buttons for cat buttongroup\n"
                                           "called ButtonGroup.buttons for main buttongroup\n"
                                           "called ButtonGroup.buttons for cat buttongroup\n"
                                           "called CheckBox.isChecked\n"
                                           "called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_cb_checked(cb4) == (cb4, rb2)
        assert capsys.readouterr().out == ("called ButtonGroup.buttons for cat buttongroup\n"
                                           "called ButtonGroup.buttons for stat buttongroup\n"
                                           "called ButtonGroup.buttons for main buttongroup\n"
                                           "called ButtonGroup.buttons for stat buttongroup\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called RadioButton.setChecked with arg `True`\n")

        cb2.setChecked(True)
        cb3.setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n")
        assert testobj.on_cb_checked(cb1) == (cb1, rb1)
        assert capsys.readouterr().out == ("called ButtonGroup.buttons for cat buttongroup\n"
                                           "called ButtonGroup.buttons for main buttongroup\n"
                                           "called ButtonGroup.buttons for cat buttongroup\n"
                                           "called CheckBox.isChecked\n"
                                           "called RadioButton.setChecked with arg `True`\n")
        assert testobj.on_cb_checked(cb4) == (cb3, rb2)
        assert capsys.readouterr().out == ("called ButtonGroup.buttons for cat buttongroup\n"
                                           "called ButtonGroup.buttons for stat buttongroup\n"
                                           "called ButtonGroup.buttons for main buttongroup\n"
                                           "called ButtonGroup.buttons for stat buttongroup\n"
                                           "called CheckBox.isChecked\n"
                                           "called RadioButton.setChecked with arg `True`\n")
        testobj.extra_cbgs = []
        assert testobj.on_cb_checked(cb1) is None
        assert capsys.readouterr().out == ""

    def test_on_rb_checked(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.on_rb_checked
        """
        def mock_buttons():
            print('called RadioButtonGroup.buttons')
            return ['', '', '', '', radiobutton]
        radiobutton = mockqtw.MockRadioButton()
        assert capsys.readouterr().out == "called RadioButton.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._cbg = types.SimpleNamespace(buttons=mock_buttons)
        testobj.on_rb_checked('arg')
        assert capsys.readouterr().out == ("called RadioButtonGroup.buttons\n"
                                           "called RadioButton.setChecked with arg `True`\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.accept
        """
        def mock_confirm():
            print('called SelectOptionsDialog.confirm')
            return False
        def mock_confirm_2():
            print('called SelectOptionsDialog.confirm')
            return True
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == "called SelectOptionsDialog.confirm\n"
        testobj.master = types.SimpleNamespace(confirm=mock_confirm_2)
        testobj.accept()
        assert capsys.readouterr().out == ("called SelectOptionsDialog.confirm\n"
                                           "called Dialog.accept\n")

    def test_get_textentry_value(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.get_textentry_value
        """
        textentry = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textentry_value(textentry) == ""
        assert capsys.readouterr().out == "called LineEdit.text\n"

    def test_get_radiobutton_value(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.get_radiobutton_value
        """
        radiobutton = mockqtw.MockRadioButton()
        assert capsys.readouterr().out == "called RadioButton.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert not testobj.get_radiobutton_value(radiobutton)
        assert capsys.readouterr().out == "called RadioButton.isChecked\n"

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.get_checkbox_value
        """
        checkbox = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert not testobj.get_checkbox_value(checkbox)
        assert capsys.readouterr().out == "called CheckBox.isChecked\n"

    def test_set_focus_to(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialogGui.set_focus_to
        """
        widget = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus_to(widget)
        assert capsys.readouterr().out == "called Widget.setFocus\n"


class TestSettOptionsDialogGui:
    """unittests for qtgui.SettOptionsDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.SettOptionsDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SettOptionsDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.SettOptionsDialogGui, '__init__', mock_init)
        testobj = testee.SettOptionsDialogGui()
        assert capsys.readouterr().out == 'called SettOptionsDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.__init__
        """
        parent = types.SimpleNamespace(gui='SettOptionsDialogGui')
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'resize', mockqtw.MockDialog.resize)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = testee.SettOptionsDialogGui('master', parent, 'title')
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args SettOptionsDialogGui () {}\n"
                "called Dialog.resize with args (350, 200)\n"
                "called Dialog.setWindowTitle with args ('title',)\n"
                "called VBox.__init__\n")

    def test_add_listbox_with_buttons(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.add_listbox_with_buttons
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QListWidget', mockqtw.MockListBox)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_listbox_with_buttons('titel', ['da', 'ta'], {'can_add_remove': False,
                                                                          'can_reorder': False})
        assert isinstance(result, testee.qtw.QListWidget)
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('titel', {testobj})\n"
                "called VBox.addWidget with arg MockLabel\n"
                "called List.__init__\n"
                f"called Signal.connect with args ({testobj.end_edit},)\n"
                f"called Signal.connect with args ({testobj.edit_item},)\n"
                "called List.addItem with arg `da`\n"
                "called List.addItem with arg `ta`\n"
                "called VBox.addWidget with arg MockListBox\n"
                "called HBox.__init__\ncalled HBox.addStretch\n"
                f"called PushButton.__init__ with args ('&Edit', {testobj}) {{}}\n"
                f"called Signal.connect with args ({testobj.edit_item},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")
        result = testobj.add_listbox_with_buttons('titel', ['da', 'ta'], {'can_add_remove': True,
                                                                          'can_reorder': True})
        assert isinstance(result, testee.qtw.QListWidget)
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('titel', {testobj})\n"
                "called VBox.addWidget with arg MockLabel\n"
                "called List.__init__\n"
                f"called Signal.connect with args ({testobj.end_edit},)\n"
                f"called Signal.connect with args ({testobj.edit_item},)\n"
                "called List.addItem with arg `da`\n"
                "called List.addItem with arg `ta`\n"
                "called VBox.addWidget with arg MockListBox\n"
                "called HBox.__init__\ncalled HBox.addStretch\n"
                f"called PushButton.__init__ with args ('&Edit', {testobj}) {{}}\n"
                f"called Signal.connect with args ({testobj.edit_item},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('&New', {testobj}) {{}}\n"
                f"called Signal.connect with args ({testobj.add_item},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('&Delete', {testobj}) {{}}\n"
                f"called Signal.connect with args ({testobj.remove_item},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('Move &Up', {testobj}) {{}}\n"
                f"called Signal.connect with args ({testobj.move_item_up},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('Move &Down', {testobj}) {{}}\n"
                f"called Signal.connect with args ({testobj.move_item_down},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_label(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.add_label
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_label(['xxx', 'yyy'])
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('xxx\\nyyy', {testobj})\n"
                "called VBox.addWidget with arg MockLabel\n")

    def test_add_okcancel_buttonbox(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.add_okcancel_buttonbox
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_okcancel_buttonbox()
        assert capsys.readouterr().out == (
                "called ButtonBox.__init__ with args (3,)\n"
                f"called Signal.connect with args ({testobj.accept},)\n"
                f"called Signal.connect with args ({testobj.reject},)\n"
                # "called HBox.__init__\n"
                # "called HBox.addStretch\n"
                # "called HBox.addWidget with arg MockButtonBox\n"
                # "called HBox.addStretch\n"
                # "called VBox.addLayout with arg MockHBoxLayout\n")
                "called VBox.addWidget with arg MockButtonBox\n")

    def test_finish_display(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.finish_display
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.finish_display()
        assert capsys.readouterr().out == "called Dialog.setLayout with arg MockVBoxLayout\n"

    def test_keyReleaseEvent(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.keyReleaseEvent
        """
        def mock_key():
            print('called Event.key')
            return 'xxx'
        def mock_key_2():
            print('called Event.key')
            return testee.core.Qt.Key.Key_F2
        def mock_edit():
            print('called SettOptionsDialogGui.edit.item')
        monkeypatch.setattr(testee.qtw.QDialog, 'keyReleaseEvent',
                            mockqtw.MockDialog.keyReleaseEvent)
        evt = mockqtw.MockEvent(key=mock_key)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.edit_item = mock_edit
        testobj.keyReleaseEvent(evt)
        assert capsys.readouterr().out == f"called Dialog.keyReleaseEvent with args ({evt},)\n"
        evt.key = mock_key_2
        testobj.keyReleaseEvent(evt)
        assert capsys.readouterr().out == ("called Event.key\n"
                                           "called SettOptionsDialogGui.edit.item\n")

    def test_edit_item(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.edit_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.elb = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj.edit_item()
        assert capsys.readouterr().out == (
                "called List.currentItem\n"
                "called List.openPersistentEditor with arg current item\n"
                "called editItem with arg current item\n")

    def test_end_edit(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.end_edit
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.elb = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj.end_edit('item_n', 'item_o')
        assert capsys.readouterr().out == "called List.closePersistentEditor with arg item_o\n"

    def test_add_item(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.add_item
        """
        monkeypatch.setattr(testee.qtw, 'QListWidgetItem', mockqtw.MockListItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.elb = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        result = testobj.add_item()
        assert isinstance(result, testee.qtw.QListWidgetItem)
        assert capsys.readouterr().out == (
                "called ListItem.__init__ with args ('',)\n"
                f"called List.addItem with arg `{result}`\n"
                "called List.setCurrentItem\n"
                f"called List.openPersistentEditor with arg {result}\n"
                f"called editItem with arg {result}\n")

    def test_remove_item(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.remove_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.elb = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj.remove_item()
        assert capsys.readouterr().out == ("called List.currentRow\n"
                                           "called List.takeItem with arg `current row`\n")

    def test_move_item_up(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.move_item_up
        """
        def mock_move(**kwargs):
            print('called SettOptionsDialogGui.move_item with args', kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.move_item = mock_move
        testobj.move_item_up()
        assert capsys.readouterr().out == (
                "called SettOptionsDialogGui.move_item with args {'up': True}\n")

    def test_move_item_down(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.move_item_down
        """
        def mock_move(**kwargs):
            print('called SettOptionsDialogGui.move_item with args', kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.move_item = mock_move
        testobj.move_item_down()
        assert capsys.readouterr().out == (
                "called SettOptionsDialogGui.move_item with args {'up': False}\n")

    def test_move_item(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.move_item
        """
        class MockList:
            def currentItem(self):
                print('called List.currentItem')
                return item1
            def item(self, arg):
                print(f'called List.item with arg {arg}')
                return item2
            def currentRow(self):
                print('called List.currentRow')
                return 0
            def count(self):
                print('called List.count')
                return 2
            def setCurrentItem(self, item):
                print(f'called List.setCurrentItem with arg {item}')
        def mock_row():
            print('called List.currentRow')
            return 1
        item1 = mockqtw.MockListItem('item1')
        item2 = mockqtw.MockListItem('item2')
        assert capsys.readouterr().out == ("called ListItem.__init__ with args ('item1',)\n"
                                           "called ListItem.__init__ with args ('item2',)\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.elb = MockList()
        testobj.move_item()
        assert capsys.readouterr().out == "called List.currentRow\n"
        testobj.move_item(up=False)
        assert capsys.readouterr().out == ("called List.currentRow\n"
                                           "called List.count\n"
                                           "called List.currentItem\n"
                                           "called ListItem.text\n"
                                           "called List.item with arg 1\n"
                                           "called ListItem.text\n"
                                           "called ListItem.setText with arg 'item1'\n"
                                           "called ListItem.setText with arg 'item2'\n"
                                           f"called List.setCurrentItem with arg {item2}\n")
        assert item1.text() == 'item2'
        assert item2.text() == 'item1'
        assert capsys.readouterr().out == ("called ListItem.text\ncalled ListItem.text\n")
        testobj.elb.currentRow = mock_row
        testobj.move_item()
        assert capsys.readouterr().out == ("called List.currentRow\n"
                                           "called List.currentItem\n"
                                           "called ListItem.text\n"
                                           "called List.item with arg 0\n"
                                           "called ListItem.text\n"
                                           "called ListItem.setText with arg 'item2'\n"
                                           "called ListItem.setText with arg 'item1'\n"
                                           f"called List.setCurrentItem with arg {item2}\n")
        testobj.move_item(up=False)
        assert capsys.readouterr().out == ("called List.currentRow\n"
                                           "called List.count\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.accept
        """
        def mock_confirm():
            print('called SettOptionsDialog.confirm')
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.elb = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj.accept()
        assert capsys.readouterr().out == (
                "called List.currentItem\n"
                "called List.closePersistentEditor with arg current item\n"
                "called SettOptionsDialog.confirm\n"
                "called Dialog.accept\n")

    def test_read_listbox_data(self, monkeypatch, capsys):
        """unittest for SettOptionsDialogGui.read_listbox_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        elb = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        assert testobj.read_listbox_data(elb) == []
        assert capsys.readouterr().out == ("called List.count\n")
        item1 = mockqtw.MockListItem('xxx')
        item2 = mockqtw.MockListItem('yyy')
        elb.addItem(item1)
        elb.addItem(item2)
        assert capsys.readouterr().out == ("called ListItem.__init__ with args ('xxx',)\n"
                                           "called ListItem.__init__ with args ('yyy',)\n"
                                           f"called List.addItem with arg `{item1}`\n"
                                           f"called List.addItem with arg `{item2}`\n")
        assert testobj.read_listbox_data(elb) == ['xxx', 'yyy']
        assert capsys.readouterr().out == ("called List.count\n"
                                           "called ListItem.text\n"
                                           "called ListItem.text\n")


class TestLoginBoxGui:
    """unittest for gui_qt.LoginBoxGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.LoginBoxGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called LoginBoxGui.__init__ with args', args)
        monkeypatch.setattr(testee.LoginBoxGui, '__init__', mock_init)
        testobj = testee.LoginBoxGui()
        assert capsys.readouterr().out == 'called LoginBoxGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for LoginBoxGui.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        master = 'master'
        parent = types.SimpleNamespace(gui=MockGui())
        testobj = testee.LoginBoxGui(master, parent)
        assert testobj.master == 'master'
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert isinstance(testobj.grid, testee.qtw.QGridLayout)
        assert testobj.row == -1
        assert capsys.readouterr().out == (
                "called Gui.__init__ with args ()\n"
                f"called Dialog.__init__ with args {parent.gui} () {{}}\n"
                "called VBox.__init__\n"
                "called Grid.__init__\n"
                "called VBox.addLayout with arg MockGridLayout\n")
        # expected_output['loginbox'].format(testobj=testobj)

    def test_add_textinput_line(self, monkeypatch, capsys):
        """unittest for LoginBoxGui.add_textinput_line
        """
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockqtw.MockGridLayout()
        testobj.row = 0
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.add_textinput_line('text')
        assert testobj.row == 1
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('text', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at (1, 0)\n"
                f"called LineEdit.__init__ with args ({testobj},)\n"
                "called Grid.addWidget with arg MockLineEdit at (1, 1)\n")
        testobj.row = 0
        testobj.add_textinput_line('text', hide=True)
        assert testobj.row == 1
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('text', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at (1, 0)\n"
                f"called LineEdit.__init__ with args ({testobj},)\n"
                "called Grid.addWidget with arg MockLineEdit at (1, 1)\n"
                "called LineEdit.setEchoMode with arg 2\n")

    def test_add_okcancel_buttonbox(self, monkeypatch, capsys):
        """unittest for LoginBoxGui.add_okcancel_buttonbox
        """
        # monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_okcancel_buttonbox()
        assert capsys.readouterr().out == (
                "called ButtonBox.__init__ with args (3,)\n"
                f"called Signal.connect with args ({testobj.accept},)\n"
                f"called Signal.connect with args ({testobj.reject},)\n"
                # "called HBox.__init__\n"
                # "called HBox.addStretch\n"
                # "called HBox.addWidget with arg MockButtonBox\n"
                # "called HBox.addStretch\n"
                # "called VBox.addLayout with arg MockHBoxLayout\n")
                "called VBox.addWidget with arg MockButtonBox\n")

    def test_finish_display(self, monkeypatch, capsys):
        """unittest for LoginBoxGui.finish_display
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.finish_display()
        assert capsys.readouterr().out == "called Dialog.setLayout with arg MockVBoxLayout\n"

    def test_accept(self, monkeypatch, capsys):
        """unittest for LoginBoxGui.accept
        """
        def mock_confirm():
            print('called LoginBox.confirm')
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        # testobj.parent = types.SimpleNamespace(master=types.SimpleNamespace(filename='xxx'))
        # testobj.t_username = mockqtw.MockLineEdit()
        # testobj.t_password = mockqtw.MockLineEdit()
        # assert capsys.readouterr().out == "called LineEdit.__init__\ncalled LineEdit.__init__\n"
        testobj.accept()
        assert capsys.readouterr().out == ("called LoginBox.confirm\n"
                                           "called Dialog.accept\n")

    def test_get_textinput_value(self, monkeypatch, capsys):
        """unittest for LoginBoxGui.get_textinput_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        field = mockqtw.MockLineEdit('xxx')
        assert capsys.readouterr().out == "called LineEdit.__init__ with args ('xxx',)\n"
        assert testobj.get_textinput_value(field) == 'xxx'
        assert capsys.readouterr().out == "called LineEdit.text\n"
