"""unittests for ./probreg/gui_qt.py
"""
import pytest
from mockgui import mockqtwidgets as mockqtw
from probreg import gui_qt as testee

editor_start = """\
called Editor.__init__
"""
editor_middle = """\
called Editor.setAcceptRichText with arg `True`
called Editor.setAutoFormatting with arg `{testee.qtw.QTextEdit.AutoAll}`
called Signal.connect with args ({testobj.charformat_changed},)
"""
editor_end = """\
called Signal.connect with args ({testobj.cursorposition_changed},)
called Editor.currentFont
called Font.__init__
called Font.pointSize
called shared.tabsize with arg 'fontsize'
called Editor.setTabStopWidth with arg tabsize
called Font.family
called Font.pointSize
"""
page_start = """\
called Frame.__init__
called Page.create_text_field
"""
page_middle = """\
called Page.create_toolbar with args {{'textfield': 'text_field'}}
"""
page_end = """\
called PushButton.__init__ with args ('Sla wijzigingen op (Ctrl-S)', {testobj}) {{}}
called Signal.connect with args ({testobj.master.savep},)
called Shortcut.__init__ with args ('Ctrl+S', {testobj}, {testobj.master.savep})
called PushButton.__init__ with args ('Sla op en ga verder (Ctrl-G)', {testobj}) {{}}
called Signal.connect with args ({testobj.master.savepgo},)
called Shortcut.__init__ with args ('Ctrl+G', {testobj}, {testobj.master.savepgo})
called PushButton.__init__ with args ('Zet originele tekst terug (Alt-Ctrl-Z)', {testobj}) {{}}
called Signal.connect with args ({testobj.master.restorep},)
called Shortcut.__init__ with args ('Alt+Ctrl+Z', {testobj}, {testobj.master.restorep})
called Shortcut.__init__ with args ('Alt+N', {testobj}, {testobj.master.nieuwp})
"""
pagelayout_start = """\
called VBox.__init__
"""
pagelayout_middle = """\
called VBox.__init__
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockToolBar'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
"""
pagelayout_end = """\
called VBox.__init__
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockEditorWidget'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
called HBox.__init__
called HBox.addStretch
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Frame.setLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
"""


@pytest.fixture
def expected_output():
    return {'editor': editor_start + editor_end, 'editor2': editor_start + editor_middle + editor_end,
            'page_init': page_start + page_end, 'page_init_2': page_start + page_middle + page_end,
            'pagelayout': pagelayout_start + pagelayout_end,
            'pagelayout2': pagelayout_start + pagelayout_middle + pagelayout_end,
            }

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
        self.parent = MockBook()


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
            f"called FileDialog.getOpenFilename with args {win} ('xxx - kies een gegevensbestand',"
            f" '{testee.pathlib.Path.home()}', 'XML files (*.xml);;all files (*.*)') {{}}\n")
    assert testee.get_open_filename(win, start='qqq') == ""
    assert capsys.readouterr().out == (
            f"called FileDialog.getOpenFilename with args {win} ('xxx - kies een gegevensbestand',"
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
            f"called FileDialog.getSaveFilename with args {win} ('xxx - nieuw gegevensbestand',"
            f" '{testee.pathlib.Path.home()}', 'XML files (*.xml);;all files (*.*)') {{}}\n")
    assert testee.get_save_filename(win, start='qqq') == ""
    assert capsys.readouterr().out == (
            f"called FileDialog.getSaveFilename with args {win} ('xxx - nieuw gegevensbestand',"
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


def test_ask_cancel_question(monkeypatch, capsys):
    """unittest for gui_qt.ask_cancel_question
    """
    def mock_ask(parent, caption, message, buttons):
        print(f'called MessageBox.question with args `{parent}` `{caption}` `{message}` `{buttons}`')
        return mockqtw.MockMessageBox.Yes
    def mock_ask_2(parent, caption, message, buttons):
        print(f'called MessageBox.question with args `{parent}` `{caption}` `{message}` `{buttons}`')
        return mockqtw.MockMessageBox.Cancel
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    win = MockGui()
    assert capsys.readouterr().out == "called Gui.__init__ with args ()\n"
    testee.shared.app_title = 'xxx'
    assert testee.ask_cancel_question(win, 'question') == (False, False)
    assert capsys.readouterr().out == ("called MessageBox.question with args"
                                       f" `{win}` `xxx` `question` `14`\n")
    monkeypatch.setattr(testee.qtw.QMessageBox, 'question',mock_ask)
    assert testee.ask_cancel_question(win, 'question') == (True, False)
    assert capsys.readouterr().out == ("called MessageBox.question with args"
                                       f" `{win}` `xxx` `question` `14`\n")
    monkeypatch.setattr(testee.qtw.QMessageBox, 'question',mock_ask_2)
    assert testee.ask_cancel_question(win, 'question') == (False, True)
    assert capsys.readouterr().out == ("called MessageBox.question with args"
                                       f" `{win}` `xxx` `question` `14`\n")


def test_show_dialog(monkeypatch, capsys):
    """unittest for gui_qt.show_dialog
    """
    def mock_exec(self):
        print('called Dialog.exec_')
        return testee.qtw.QDialog.Accepted
    cls = mockqtw.MockDialog
    win = mockqtw.MockWidget()
    assert capsys.readouterr().out == 'called Widget.__init__\n'
    assert not testee.show_dialog(win, cls)
    assert capsys.readouterr().out == (f"called Dialog.__init__ with args {win} () {{}}\n"
                                       "called Dialog.exec_\n")
    monkeypatch.setattr(mockqtw.MockDialog, 'exec_', mock_exec)
    assert testee.show_dialog(win, cls, 'args')
    assert capsys.readouterr().out == (f"called Dialog.__init__ with args {win} ('args',) {{}}\n"
                                       "called Dialog.exec_\n")


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
        testobj.appbase = parent.parent.parent
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
        monkeypatch.setattr(testee.qtw.QTextEdit, 'setTabStopWidth',
                            mockqtw.MockEditorWidget.setTabStopWidth)
        monkeypatch.setattr(testee.shared, 'tabsize', mock_tabsize)
        parent = MockPage()
        assert capsys.readouterr().out == 'called Page.__init__\n'
        testobj = testee.EditorPanel(parent)
        assert testobj.parent == parent
        assert testobj.appbase == parent.parent.parent
        assert testobj.defaultfamily == 'fontfamily'
        assert testobj.defaultsize == 'fontsize'
        assert capsys.readouterr().out == expected_output['editor'].format(testobj=testobj)
        parent.parent.parent.use_rt = True
        testobj = testee.EditorPanel(parent)
        assert testobj.parent == parent
        assert testobj.appbase == parent.parent.parent
        assert testobj.defaultfamily == 'fontfamily'
        assert testobj.defaultsize == 'fontsize'
        assert capsys.readouterr().out == expected_output['editor2'].format(testobj=testobj,
                                                                            testee=testee)

    def test_canInsertFromMimeData(self, monkeypatch, capsys):
        """unittest for EditorPanel.canInsertFromMimeData
        """
        class MimeData:
            def __init__(self):
                self.hasImage = False
            def __str__(self):
                return 'mimedata'
            def imageData(self):
                return 'imagedata'
        monkeypatch.setattr(testee.qtw.QTextEdit, 'canInsertFromMimeData',
                            mockqtw.MockEditorWidget.canInsertFromMimeData)
        testobj = self.setup_testobj(monkeypatch, capsys)
        source = MimeData()
        assert not testobj.canInsertFromMimeData(source)
        assert capsys.readouterr().out == "called Editor.canInsertFromMimeData with arg 'mimedata'\n"
        source.hasImage = True
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
        class MockDocument:
            """stub for Qtgui.QTextDocument
            """
            def addResource(self, *args):
                print('called textdocument.addResource with args', args)
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
                "called TextDocument.addResource with args"
                " (2, <class 'mockgui.mockqtwidgets.MockUrl'>,"
                " <class 'mockgui.mockqtwidgets.MockImage'>)\n"
                "called Cursor.insertImage with arg test_00001.png\n")

    def test_set_contents(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_contents
        """
        def mock_sethtml(text):
            print(f'called Editor.setHtml with arg `{text}`')
        def mock_charformat_changed(arg):
            print('called Editor.charformat_changed')  #  with arg {arg}')
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
        testobj.parent.actiondict = {'&Bold': mockqtw.MockAction()}
        assert capsys.readouterr().out == "called Action.__init__ with args ()\n"
        testobj.text_bold()
        assert capsys.readouterr().out == (
                "called TextCharFormat.__init__ with args ()\n"
                "called Action.isChecked\n"
                f"called TextCharFormat.setFontWeight with arg {testee.gui.QFont.Normal}\n"
                "called EditorPanel.mergeCurrentCharFormat\n")
        testobj.parent.actiondict['&Bold'].setChecked(True)
        testobj.text_bold()
        assert capsys.readouterr().out == (
                "called TextCharFormat.__init__ with args ()\n"
                "called Action.isChecked\n"
                f"called TextCharFormat.setFontWeight with arg {testee.gui.QFont.Bold}\n"
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
        testobj.parent.actiondict = {'&Italic': mockqtw.MockAction()}
        assert capsys.readouterr().out == "called Action.__init__ with args ()\n"
        testobj.text_italic()
        assert capsys.readouterr().out == (
                "called TextCharFormat.__init__ with args ()\n"
                "called Action.isChecked\n"
                "called TextCharFormat.setFontItalic with arg False\n"
                "called EditorPanel.mergeCurrentCharFormat\n")
        testobj.parent.actiondict['&Italic'].setChecked(True)
        testobj.text_italic()
        assert capsys.readouterr().out == (
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
        testobj.parent.actiondict = {'&Underline': mockqtw.MockAction()}
        assert capsys.readouterr().out == "called Action.__init__ with args ()\n"
        testobj.text_underline()
        assert capsys.readouterr().out == (
                "called TextCharFormat.__init__ with args ()\n"
                "called Action.isChecked\n"
                "called TextCharFormat.setFontUnderline with arg False\n"
                "called EditorPanel.mergeCurrentCharFormat\n")
        testobj.parent.actiondict['&Underline'].setChecked(True)
        testobj.text_underline()
        assert capsys.readouterr().out == (
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
        testobj.parent.actiondict = {'Strike&through': mockqtw.MockAction()}
        assert capsys.readouterr().out == "called Action.__init__ with args ()\n"
        testobj.text_strikethrough()
        assert capsys.readouterr().out == (
                "called TextCharFormat.__init__ with args ()\n"
                "called Action.isChecked\n"
                "called TextCharFormat.setFontStrikeOut with arg False\n"
                "called EditorPanel.mergeCurrentCharFormat\n")
        testobj.parent.actiondict['Strike&through'].setChecked(True)
        testobj.text_strikethrough()
        assert capsys.readouterr().out == (
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

    def _test_change_indent(self, monkeypatch, capsys):
        """unittest for EditorPanel.change_indent
        """
        def mock_textcursor():
            print('called EditorPanel.textCursor')
            return mockqtw.MockTextCursor()
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.textCursor = mock_textcursor
        testobj.hasFocus = lambda: False
        testobj.change_indent(10)
        assert capsys.readouterr().out == ""
        testobj.hasFocus = lambda: True
        testobj.change_indent(10)
        assert capsys.readouterr().out == ("")

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

    def _test_set_linespacing(self, monkeypatch, capsys):
        def mock_textcursor():
            print('called EditorPanel.textCursor')
            return mockqtw.MockTextCursor()
        """unittest for EditorPanel.set_linespacing
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.textCursor = mock_textcursor
        testobj.hasFocus = lambda: False
        testobj.set_linespacing(100)
        assert capsys.readouterr().out == ""
        testobj.hasFocus = lambda: True
        testobj.set_linespacing(0)
        assert capsys.readouterr().out == ("")
        testobj.set_linespacing(100)
        assert capsys.readouterr().out == ("")

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

    def _test_set_paragraph_spacing(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_paragraph_spacing
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_paragraph_spacing(more=False, less=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_text_size(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_size
        """
        def mock_tabsize(arg):
            print('called shared.mock_tabsize with arg', arg)
            return 18
        def mock_settab(arg):
            print('called EditorPanel.setTabStopWidth with arg', arg)
        def mock_merge(arg):
            print('called EditorPanel.mergeCurrentcharformat')
        def mock_setfocus():
            print('called EditorPanel.set_focus')
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        monkeypatch.setattr(testee.shared, 'tabsize', mock_tabsize)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.setTabStopWidth = mock_settab
        testobj.mergeCurrentCharFormat = mock_merge
        testobj.setFocus = mock_setfocus
        testobj.text_size(0)
        assert capsys.readouterr().out == ""
        testobj.text_size(10)
        assert capsys.readouterr().out == (
                "called TextCharFormat.__init__ with args ()\n"
                "called TextCharFormat.setFontPointSize with arg 10.0\n"
                "called shared.mock_tabsize with arg 10.0\n"
                "called EditorPanel.setTabStopWidth with arg 18\n"
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
        testobj.parent.actiondict = {"&Bold": mockqtw.MockCheckBox(),
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
                f"called TextCursor.select with arg {testee.gui.QTextCursor.WordUnderCursor}\n"
                "called TextCursor.mergeCharFormat with arg format\n"
                f"called TextCursor.mergeCurrentCharFormat with args ({testobj}, 'format')\n")
        monkeypatch.setattr(mockqtw.MockTextCursor, 'hasSelection', mock_has_sel)
        testobj.mergeCurrentCharFormat('format')
        assert capsys.readouterr().out == (
                "called TextEdit.textCursor\n"
                "called TextCursor.__init__\n"
                "called TextCursor.hasSelection\n"
                "called TextCursor.mergeCharFormat with arg format\n"
                f"called TextCursor.mergeCurrentCharFormat with args ({testobj}, 'format')\n")

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
                                           "called textDocument.setModified with arg value\n")

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
        testobj.parent = MockGui()
        testobj.master = MockPage()
        testobj.appbase = testobj.master.parent.parent
        assert capsys.readouterr().out == ('called PageGui.__init__ with args ()\n'
                                           'called Gui.__init__ with args ()\n'
                                           'called Page.__init__\n')
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for PageGui.__init__
        """
        def mock_create(self):
            print('called Page.create_text_field')
            return 'text_field'
        def mock_create_tb(self, **kwargs):
            print('called Page.create_toolbar with args', kwargs)
        monkeypatch.setattr(testee.qtw.QFrame, '__init__', mockqtw.MockFrame.__init__)
        monkeypatch.setattr(testee.PageGui, 'create_text_field', mock_create)
        monkeypatch.setattr(testee.PageGui, 'create_toolbar', mock_create_tb)
        monkeypatch.setattr(testee.qtw, 'QShortcut', mockqtw.MockShortcut)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        parent = MockGui()
        master = MockPage()
        assert capsys.readouterr().out == ("called Gui.__init__ with args ()\n"
                                           'called Page.__init__\n')
        master.is_text_page = False
        master.savep = lambda: 'save'
        master.savepgo = lambda: 'save&go'
        master.restorep = lambda: 'restore'
        master.nieuwp = lambda: 'nieuw'
        testobj = testee.PageGui(parent, master)
        assert capsys.readouterr().out == "called Frame.__init__\n"
        master.is_text_page = True
        master.parent.parent.use_rt = False
        testobj = testee.PageGui(parent, master)
        assert capsys.readouterr().out == expected_output['page_init'].format(testobj=testobj)

        master.parent.parent.use_rt = True
        testobj = testee.PageGui(parent, master)
        assert capsys.readouterr().out == expected_output['page_init_2'].format(testobj=testobj)

    def test_create_text_field(self, monkeypatch, capsys):
        """unittest for PageGui.create_text_field
        """
        monkeypatch.setattr(testee, 'EditorPanel', mockqtw.MockEditorWidget)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.on_text = lambda x: x
        monkeypatch.setattr(testee, 'LIN', False)
        result = testobj.create_text_field()
        assert isinstance(result, testee.EditorPanel)
        assert capsys.readouterr().out == (
                f"called Editor.__init__ with args ({testobj},)\n"
                "called Editor.resize with args (490, 430)\n"
                f"called Signal.connect with args ({testobj.master.on_text},)\n")
        monkeypatch.setattr(testee, 'LIN', True)
        result = testobj.create_text_field()
        assert isinstance(result, testee.EditorPanel)
        assert capsys.readouterr().out == (
                f"called Editor.__init__ with args ({testobj},)\n"
                "called Editor.resize with args (490, 330)\n"
                f"called Signal.connect with args ({testobj.master.on_text},)\n")

    def _test_create_toolbar(self, monkeypatch, capsys):
        """unittest for PageGui.create_toolbar
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.create_toolbar(textfield=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_doelayout(self, monkeypatch, capsys, expected_output):
        """unittest for PageGui.doelayout
        """
        def mock_setLayout(arg):
            print(f'called Frame.setLayout with arg of type {type(arg)}')
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.toolbar = mockqtw.MockToolBar()
        testobj.text1 = mockqtw.MockEditorWidget()
        testobj.save_button = mockqtw.MockPushButton()
        testobj.saveandgo_button = mockqtw.MockPushButton()
        testobj.cancel_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called ToolBar.__init__ \n"
                                           "called Editor.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.appbase.use_rt = False
        testobj.setLayout = mock_setLayout
        assert testobj.doelayout()
        assert capsys.readouterr().out == expected_output['pagelayout'].format(testobj=testobj)
        testobj.appbase.use_rt = True
        assert testobj.doelayout()
        assert capsys.readouterr().out == expected_output['pagelayout2'].format(testobj=testobj)

    def test_reset_font(self, monkeypatch, capsys):
        """unittest for PageGui.reset_font
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_text = mockqtw.MockEditorWidget('progress')
        testobj.text1 = mockqtw.MockEditorWidget('text')
        assert capsys.readouterr().out == ("called Editor.__init__ with args ('progress',)\n"
                                           "called Editor.__init__ with args ('text',)\n")
        testobj.master.parent.current_tab = 2
        testobj.reset_font()
        # hoe toon ik aan welke waarde win heeft?
        assert capsys.readouterr().out == (
                f"called Editor.setFontWeight with arg {testee.gui.QFont.Normal}\n"
                "called Editor.setFontItalic with arg False\n"
                "called Editor.setFontUnderline with arg False\n"
                "called Editor.setFontFamily with arg 'font family'\n"
                "called Editor.setFontPointSize with arg '12pt'\n")
        testobj.master.parent.current_tab = 6
        testobj.reset_font()
        assert capsys.readouterr().out == (
                f"called Editor.setFontWeight with arg {testee.gui.QFont.Normal}\n"
                "called Editor.setFontItalic with arg False\n"
                "called Editor.setFontUnderline with arg False\n"
                "called Editor.setFontFamily with arg 'font family'\n"
                "called Editor.setFontPointSize with arg '12pt'\n")

    def test_enable_buttons(self, monkeypatch, capsys):
        """unittest for PageGui.enable_buttons
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.save_button = mockqtw.MockPushButton()
        testobj.saveandgo_button = mockqtw.MockPushButton()
        testobj.cancel_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n")
        assert not testobj.save_button.isEnabled()
        assert not testobj.saveandgo_button.isEnabled()
        assert not testobj.cancel_button.isEnabled()
        testobj.parent.count = lambda: 3
        testobj.parent.current_tab = 1
        testobj.enable_buttons()
        assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `True`\n")
        assert testobj.save_button.isEnabled()
        assert testobj.saveandgo_button.isEnabled()
        assert testobj.cancel_button.isEnabled()
        testobj.parent.current_tab = 2
        testobj.enable_buttons(False)
        assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `False`\n"
                                           "called PushButton.setEnabled with arg `False`\n")
        assert not testobj.save_button.isEnabled()
        assert testobj.saveandgo_button.isEnabled()
        assert not testobj.cancel_button.isEnabled()

    def test_move_cursor_to_end(self, monkeypatch, capsys):
        """unittest for PageGui.move_cursor_to_end
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.text1 = mockqtw.MockEditorWidget()
        testobj.move_cursor_to_end()
        assert capsys.readouterr().out == (
                "called Editor.__init__\n"
                f"called Editor.moveCursor with args ({testee.gui.QTextCursor.End},"
                f" {testee.gui.QTextCursor.MoveAnchor})\n")

    def test_set_textarea_contents(self, monkeypatch, capsys):
        """unittest for PageGui.set_textarea_contents
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.text1 = MockEditorPanel('')
        testobj.set_textarea_contents('data')
        assert capsys.readouterr().out == "called EditorWidget.set_contents with arg 'data'\n"

    def test_get_textarea_contents(self, monkeypatch, capsys):
        """unittest for PageGui.get_textarea_contents
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.text1 = MockEditorPanel('text')
        assert testobj.get_textarea_contents() == "text"
        assert capsys.readouterr().out == ("called EditorWidget.get_contents\n")

    def test_enable_toolbar(self, monkeypatch, capsys):
        """unittest for PageGui.enable_toolbar
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.toolbar = mockqtw.MockToolBar()
        assert capsys.readouterr().out == "called ToolBar.__init__ \n"
        testobj.appbase.use_rt = False
        testobj.enable_toolbar(True)
        assert capsys.readouterr().out == ""
        testobj.appbase.use_rt = True
        testobj.enable_toolbar(True)
        assert capsys.readouterr().out == "called ToolBar.setEnabled with arg True\n"

    def test_set_text_readonly(self, monkeypatch, capsys):
        """unittest for PageGui.set_text_readonly
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.text1 = MockEditorPanel('')
        testobj.set_text_readonly(True)
        assert capsys.readouterr().out == ("called EditorWidget.setReadOnly with arg True\n")

    def test_can_saveandgo(self, monkeypatch, capsys):
        """unittest for PageGui.can_saveandgo
        """
        def mock_isEnabled(self):
            print('called PushButton.isEnabled')
            return self._enabled
        monkeypatch.setattr(mockqtw.MockPushButton, 'isEnabled', mock_isEnabled)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.saveandgo_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
        assert not testobj.can_saveandgo()
        assert capsys.readouterr().out == "called PushButton.isEnabled\n"

    def test_can_save(self, monkeypatch, capsys):
        """unittest for PageGui.can_save
        """
        def mock_isEnabled(self):
            print('called PushButton.isEnabled')
            return self._enabled
        monkeypatch.setattr(mockqtw.MockPushButton, 'isEnabled', mock_isEnabled)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.save_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
        assert not testobj.can_save()
        assert capsys.readouterr().out == "called PushButton.isEnabled\n"

    def test_build_newbuf(self, monkeypatch, capsys):
        """unittest for PageGui.build_newbuf
        """
        def mock_get():
            print('called PageGui.get_textarea_contents')
            return 'text'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_textarea_contents = mock_get
        assert testobj.build_newbuf() == "text"
        assert capsys.readouterr().out == "called PageGui.get_textarea_contents\n"


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
        testobj = testee.Page0Gui()
        assert capsys.readouterr().out == 'called Page0Gui.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for Page0Gui.__init__
        """
        testobj = testee.Page0Gui(parent, master, widths)
        assert capsys.readouterr().out == ("")

    def _test_doelayout(self, monkeypatch, capsys):
        """unittest for Page0Gui.doelayout
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.doelayout() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_sorting(self, monkeypatch, capsys):
        """unittest for Page0Gui.enable_sorting
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_sorting(value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_buttons(self, monkeypatch, capsys):
        """unittest for Page0Gui.enable_buttons
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_buttons() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_change_selected(self, monkeypatch, capsys):
        """unittest for Page0Gui.on_change_selected
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_change_selected(item_n, item_o) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_activate_item(self, monkeypatch, capsys):
        """unittest for Page0Gui.on_activate_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_activate_item(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_clear_list(self, monkeypatch, capsys):
        """unittest for Page0Gui.clear_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.clear_list() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_listitem(self, monkeypatch, capsys):
        """unittest for Page0Gui.add_listitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_listitem(data) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_listitem_values(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_listitem_values
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_listitem_values(item, data) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_items(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_items
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_items() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_item_text(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_item_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_item_text(item_or_index, column) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_item_text(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_item_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_item_text(item_or_index, column, text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_first_item(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_first_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_first_item() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_item_by_index(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_item_by_index
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_item_by_index(item_n) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_item_by_id(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_item_by_id
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_item_by_id(item_id) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_has_selection(self, monkeypatch, capsys):
        """unittest for Page0Gui.has_selection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.has_selection() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_selection(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_selection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_selection() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_selection(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_selection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_selection() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_ensure_visible(self, monkeypatch, capsys):
        """unittest for Page0Gui.ensure_visible
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ensure_visible(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_archive_button_text(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_archive_button_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_archive_button_text(txt) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_selected_action(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_selected_action
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_selected_action() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_list_row(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_list_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_list_row() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_list_row(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_list_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_list_row(num) == "expected_result"
        assert capsys.readouterr().out == ("")


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
        testobj = testee.Page1Gui()
        assert capsys.readouterr().out == 'called Page1Gui.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for Page1Gui.__init__
        """
        testobj = testee.Page1Gui(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_doelayout(self, monkeypatch, capsys):
        """unittest for Page1Gui.doelayout
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.doelayout() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_init_fields(self, monkeypatch, capsys):
        """unittest for Page1Gui.init_fields
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.init_fields() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_text(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_text(fieldtype, value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_text(self, monkeypatch, capsys):
        """unittest for Page1Gui.get_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_text(fieldtype) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_choice(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_choice
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_choice(domain, field, value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_choice_data(self, monkeypatch, capsys):
        """unittest for Page1Gui.get_choice_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_choice_data(field) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_oldbuf(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_oldbuf
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_oldbuf() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_field_text(self, monkeypatch, capsys):
        """unittest for Page1Gui.get_field_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_field_text(entry_type) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_archive_button_text(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_archive_button_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_archive_button_text(value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_fields(self, monkeypatch, capsys):
        """unittest for Page1Gui.enable_fields
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_fields(state) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_clear_stats(self, monkeypatch, capsys):
        """unittest for Page1Gui.clear_stats
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.clear_stats() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_clear_cats(self, monkeypatch, capsys):
        """unittest for Page1Gui.clear_cats
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.clear_cats() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_cat_choice(self, monkeypatch, capsys):
        """unittest for Page1Gui.add_cat_choice
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_cat_choice(text, value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_stat_choice(self, monkeypatch, capsys):
        """unittest for Page1Gui.add_stat_choice
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_stat_choice(text, value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_focus(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_focus
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_focus() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_build_newbuf(self, monkeypatch, capsys):
        """unittest for Page1Gui.build_newbuf
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.build_newbuf() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_fieldvalues(self, monkeypatch, capsys):
        """unittest for Page1Gui.get_fieldvalues
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_fieldvalues() == "expected_result"
        assert capsys.readouterr().out == ("")


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
        testobj = testee.Page6Gui()
        assert capsys.readouterr().out == 'called Page6Gui.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for Page6Gui.__init__
        """
        testobj = testee.Page6Gui(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_doelayout(self, monkeypatch, capsys):
        """unittest for Page6Gui.doelayout
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.doelayout() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_activate_item(self, monkeypatch, capsys):
        """unittest for Page6Gui.on_activate_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_activate_item(item=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_new_item_to_list(self, monkeypatch, capsys):
        """unittest for Page6Gui.add_new_item_to_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_new_item_to_list(datum, oldtext) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_is_first_line(self, monkeypatch, capsys):
        """unittest for Page6Gui.is_first_line
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.is_first_line(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_select_item(self, monkeypatch, capsys):
        """unittest for Page6Gui.on_select_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_select_item(item_n, item_o) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_init_textfield(self, monkeypatch, capsys):
        """unittest for Page6Gui.init_textfield
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.init_textfield() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_init_list(self, monkeypatch, capsys):
        """unittest for Page6Gui.init_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.init_list(text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_item_to_list(self, monkeypatch, capsys):
        """unittest for Page6Gui.add_item_to_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_item_to_list(idx, datum) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_list_callback(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_list_callback
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_list_callback() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_clear_textfield(self, monkeypatch, capsys):
        """unittest for Page6Gui.clear_textfield
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.clear_textfield() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_protect_textfield(self, monkeypatch, capsys):
        """unittest for Page6Gui.protect_textfield
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.protect_textfield(value=True) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_textfield_contents(self, monkeypatch, capsys):
        """unittest for Page6Gui.get_textfield_contents
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textfield_contents() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_textfield_contents(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_textfield_contents
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_textfield_contents(text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_listitem_text(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_listitem_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_listitem_text(itemindex, text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_listitem_data(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_listitem_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_listitem_data(itemindex) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_list_row(self, monkeypatch, capsys):
        """unittest for Page6Gui.get_list_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_list_row() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_list_row(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_list_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_list_row(num) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_list_rowcount(self, monkeypatch, capsys):
        """unittest for Page6Gui.get_list_rowcount
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_list_rowcount() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_move_cursor_to_end(self, monkeypatch, capsys):
        """unittest for Page6Gui.move_cursor_to_end
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.move_cursor_to_end() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_focus_to_textfield(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_focus_to_textfield
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_focus_to_textfield() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_convert_text(self, monkeypatch, capsys):
        """unittest for Page6Gui.convert_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.convert_text(text, to) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_listitem_text(self, monkeypatch, capsys):
        """unittest for Page6Gui.get_listitem_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_listitem_text(itemindex) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_build_newbuf(self, monkeypatch, capsys):
        """unittest for Page6Gui.build_newbuf
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.build_newbuf() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestSortOptionsDialog:
    """unittest for gui_qt.SortOptionsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.SortOptionsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SortOptionsDialog.__init__ with args', args)
        testobj = testee.SortOptionsDialog()
        assert capsys.readouterr().out == 'called SortOptionsDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for SortOptionsDialog.__init__
        """
        testobj = testee.SortOptionsDialog(parent, args)
        assert capsys.readouterr().out == ("")

    def _test_set_defaults(self, monkeypatch, capsys):
        """unittest for SortOptionsDialog.set_defaults
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_defaults() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_fields(self, monkeypatch, capsys):
        """unittest for SortOptionsDialog.enable_fields
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_fields(state) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for SortOptionsDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestSelectOptionsDialog:
    """unittest for gui_qt.SelectOptionsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.SelectOptionsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SelectOptionsDialog.__init__ with args', args)
        testobj = testee.SelectOptionsDialog()
        assert capsys.readouterr().out == 'called SelectOptionsDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.__init__
        """
        testobj = testee.SelectOptionsDialog(parent, args)
        assert capsys.readouterr().out == ("")

    def _test_doelayout(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.doelayout
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.doelayout() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_default_values(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.set_default_values
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_default_values(sel_args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_text(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.on_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_text(arg, text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_checked(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.on_checked
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_checked(arg) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestSettOptionsDialog:
    """unittest for gui_qt.SettOptionsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.SettOptionsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SettOptionsDialog.__init__ with args', args)
        testobj = testee.SettOptionsDialog()
        assert capsys.readouterr().out == 'called SettOptionsDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.__init__
        """
        testobj = testee.SettOptionsDialog(parent, args)
        assert capsys.readouterr().out == ("")

    def _test_initstuff(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.initstuff
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.initstuff(parent) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_keyReleaseEvent(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.keyReleaseEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.keyReleaseEvent(evt) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_edit_item(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.edit_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.edit_item() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_end_edit(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.end_edit
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.end_edit(item_n, item_o) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_item(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.add_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_item() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_remove_item(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.remove_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.remove_item() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_move_item_up(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.move_item_up
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.move_item_up() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_move_item_down(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.move_item_down
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.move_item_down() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_move_item(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.move_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.move_item(up=True) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestLoginBox:
    """unittest for gui_qt.LoginBox
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.LoginBox object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called LoginBox.__init__ with args', args)
        testobj = testee.LoginBox()
        assert capsys.readouterr().out == 'called LoginBox.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for LoginBox.__init__
        """
        testobj = testee.LoginBox(parent)
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for LoginBox.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


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
        testobj = testee.MainGui()
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for MainGui.__init__
        """
        testobj = testee.MainGui(master)
        assert capsys.readouterr().out == ("")

    def _test_create_menu(self, monkeypatch, capsys):
        """unittest for MainGui.create_menu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.create_menu() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_create_actions(self, monkeypatch, capsys):
        """unittest for MainGui.create_actions
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.create_actions() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_bookwidget(self, monkeypatch, capsys):
        """unittest for MainGui.get_bookwidget
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_bookwidget() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_go(self, monkeypatch, capsys):
        """unittest for MainGui.go
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.go() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_refresh_page(self, monkeypatch, capsys):
        """unittest for MainGui.refresh_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.refresh_page() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_page_changing(self, monkeypatch, capsys):
        """unittest for MainGui.on_page_changing
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_page_changing(newtabnum) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_book_tabs(self, monkeypatch, capsys):
        """unittest for MainGui.enable_book_tabs
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_book_tabs(state, tabfrom=0, tabto=-1) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_all_other_tabs(self, monkeypatch, capsys):
        """unittest for MainGui.enable_all_other_tabs
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_all_other_tabs(state) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_book_tab(self, monkeypatch, capsys):
        """unittest for MainGui.add_book_tab
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_book_tab(tab, title) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_exit(self, monkeypatch, capsys):
        """unittest for MainGui.exit
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.exit() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_close(self, monkeypatch, capsys):
        """unittest for MainGui.close
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.close() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_page(self, monkeypatch, capsys):
        """unittest for MainGui.set_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_page(num) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_page_title(self, monkeypatch, capsys):
        """unittest for MainGui.set_page_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_page_title(num, text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_page(self, monkeypatch, capsys):
        """unittest for MainGui.get_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_page() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_tabfocus(self, monkeypatch, capsys):
        """unittest for MainGui.set_tabfocus
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_tabfocus(tabno) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_go_next(self, monkeypatch, capsys):
        """unittest for MainGui.go_next
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.go_next() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_go_prev(self, monkeypatch, capsys):
        """unittest for MainGui.go_prev
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.go_prev() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_go_to(self, monkeypatch, capsys):
        """unittest for MainGui.go_to
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.go_to(page) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_print_(self, monkeypatch, capsys):
        """unittest for MainGui.print_
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.print_() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_preview(self, monkeypatch, capsys):
        """unittest for MainGui.preview
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.preview() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_afdrukken(self, monkeypatch, capsys):
        """unittest for MainGui.afdrukken
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.afdrukken(printer) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_settingsmenu(self, monkeypatch, capsys):
        """unittest for MainGui.enable_settingsmenu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_settingsmenu() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_statusmessage(self, monkeypatch, capsys):
        """unittest for MainGui.set_statusmessage
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_statusmessage(msg='') == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_window_title(self, monkeypatch, capsys):
        """unittest for MainGui.set_window_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_window_title(text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_show_username(self, monkeypatch, capsys):
        """unittest for MainGui.show_username
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.show_username(msg) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_tab_titles(self, monkeypatch, capsys):
        """unittest for MainGui.set_tab_titles
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_tab_titles(tabs) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_select_first_tab(self, monkeypatch, capsys):
        """unittest for MainGui.select_first_tab
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.select_first_tab() == "expected_result"
        assert capsys.readouterr().out == ("")
