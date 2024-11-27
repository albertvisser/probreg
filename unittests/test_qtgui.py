"""unittests for ./probreg/gui_qt.py
"""
import pytest
import types
from mockgui import mockqtwidgets as mockqtw
from probreg import gui_qt as testee
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
        self.parent = MockBook()
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
    monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_ask)
    assert testee.ask_cancel_question(win, 'question') == (True, False)
    assert capsys.readouterr().out == ("called MessageBox.question with args"
                                       f" `{win}` `xxx` `question` `14`\n")
    monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_ask_2)
    assert testee.ask_cancel_question(win, 'question') == (False, True)
    assert capsys.readouterr().out == ("called MessageBox.question with args"
                                       f" `{win}` `xxx` `question` `14`\n")


def test_show_dialog(monkeypatch, capsys):
    """unittest for gui_qt.show_dialog
    """
    def mock_exec(self):
        print('called Dialog.exec')
        return testee.qtw.QDialog.DialogCode.Accepted
    cls = mockqtw.MockDialog
    win = mockqtw.MockWidget()
    assert capsys.readouterr().out == 'called Widget.__init__\n'
    assert not testee.show_dialog(win, cls)
    assert capsys.readouterr().out == (f"called Dialog.__init__ with args {win} () {{}}\n"
                                       "called Dialog.exec\n")
    monkeypatch.setattr(mockqtw.MockDialog, 'exec', mock_exec)
    assert testee.show_dialog(win, cls, 'args')
    assert capsys.readouterr().out == (f"called Dialog.__init__ with args {win} ('args',) {{}}\n"
                                       "called Dialog.exec\n")


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
        monkeypatch.setattr(testee.qtw.QTextEdit, 'setTabStopDistance',
                            mockqtw.MockEditorWidget.setTabStopDistance)
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
        testobj.parent.actiondict = {'&Bold': mockqtw.MockAction()}
        assert capsys.readouterr().out == "called Action.__init__ with args ()\n"
        testobj.text_bold()
        assert capsys.readouterr().out == (
                "called TextCharFormat.__init__ with args ()\n"
                "called Action.isChecked\n"
                f"called TextCharFormat.setFontWeight with arg {testee.gui.QFont.Weight.Normal}\n"
                "called EditorPanel.mergeCurrentCharFormat\n")
        testobj.parent.actiondict['&Bold'].setChecked(True)
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
                "called TextCursor.select with"
                f" arg {testee.gui.QTextCursor.SelectionType.WordUnderCursor}\n"
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
        monkeypatch.setattr(testee.gui, 'QShortcut', mockqtw.MockShortcut)
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
        assert capsys.readouterr().out == ("called ToolBar.__init__\n"
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
                f"called Editor.setFontWeight with arg {testee.gui.QFont.Weight.Normal}\n"
                "called Editor.setFontItalic with arg False\n"
                "called Editor.setFontUnderline with arg False\n"
                "called Editor.setFontFamily with arg 'font family'\n"
                "called Editor.setFontPointSize with arg '12pt'\n")
        testobj.master.parent.current_tab = 6
        testobj.reset_font()
        assert capsys.readouterr().out == (
                f"called Editor.setFontWeight with arg {testee.gui.QFont.Weight.Normal}\n"
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
                f"called Editor.moveCursor with args ({testee.gui.QTextCursor.MoveOperation.End!r},"
                f" {testee.gui.QTextCursor.MoveMode.MoveAnchor!r})\n")

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
        assert capsys.readouterr().out == "called ToolBar.__init__\n"
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
        parent = MockGui()
        master = MockPage()
        monkeypatch.setattr(testee.Page0Gui, '__init__', mock_init)
        testobj = testee.Page0Gui(parent, master, [])
        assert capsys.readouterr().out == (
                "called Gui.__init__ with args ()\n"
                'called Page.__init__\n'
                f'called Page0Gui.__init__ with args ({parent}, {master}, [])\n')
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for Page0Gui.__init__
        """
        def mock_init(self, parent, master):
            """stub
            """
            print(f'called PageGui.__init__ with args ({parent}, {master})')
            self.parent = parent
            self.master = master
        parent = MockGui()
        master = MockPage()
        monkeypatch.setattr(testee.PageGui, '__init__', mock_init)
        monkeypatch.setattr(testee.Page0Gui, 'on_activate_item', lambda: 'dummy')
        monkeypatch.setattr(testee.Page0Gui, 'on_change_selected', lambda: 'dummy')
        monkeypatch.setattr(testee.qtw, 'QTreeWidget', mockqtw.MockTreeWidget)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        assert capsys.readouterr().out == ("called Gui.__init__ with args ()\n"
                                           'called Page.__init__\n')
        parent.ctitels = ['xxx', 'yyy']
        testobj = testee.Page0Gui(parent, master, [10, 20])
        assert capsys.readouterr().out == expected_output['page0_init'].format(testobj=testobj)

    def test_doelayout(self, monkeypatch, capsys, expected_output):
        """unittest for Page0Gui.doelayout
        """
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.Page0Gui, 'setLayout', mockqtw.MockWidget.setLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = mockqtw.MockTreeWidget()
        testobj.sort_button = mockqtw.MockPushButton()
        testobj.filter_button = mockqtw.MockPushButton()
        testobj.go_button = mockqtw.MockPushButton()
        testobj.archive_button = mockqtw.MockPushButton()
        testobj.new_button = mockqtw.MockPushButton()
        testobj.doelayout()
        assert capsys.readouterr().out == expected_output['page0_layout']

    def test_enable_sorting(self, monkeypatch, capsys):
        """unittest for Page0Gui.enable_sorting
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.enable_sorting('value')
        assert capsys.readouterr().out == "called Tree.setSortingEnabled with arg value\n"

    def test_enable_buttons(self, monkeypatch, capsys):
        """unittest for Page0Gui.enable_buttons
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.appbase = types.SimpleNamespace(user='', is_user=False, filename='xx')
        testobj.p0list = mockqtw.MockTreeWidget()
        testobj.p0list.has_selection = True
        testobj.sort_button = mockqtw.MockPushButton()
        testobj.filter_button = mockqtw.MockPushButton()
        testobj.go_button = mockqtw.MockPushButton()
        testobj.archive_button = mockqtw.MockPushButton()
        testobj.new_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.enable_buttons()
        assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `False`\n"
                                           "called PushButton.setEnabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `False`\n"
                                           "called PushButton.setEnabled with arg `False`\n"
                                           "called PushButton.setEnabled with arg `False`\n")
        testobj.appbase = types.SimpleNamespace(user='xx', is_user=True, filename='')
        testobj.enable_buttons()
        assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `False`\n"
                                           "called PushButton.setEnabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `True`\n")
        testobj.appbase.filename = 'xx'
        testobj.enable_buttons()
        assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `True`\n")
        testobj.p0list.has_selection = False
        testobj.enable_buttons()
        assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `False`\n"
                                           "called PushButton.setEnabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `False`\n"
                                           "called PushButton.setEnabled with arg `False`\n")

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
        testobj.p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.clear_list()
        assert not testobj.p0list.has_selection
        assert capsys.readouterr().out == "called Tree.clear\n"

    def test_add_listitem(self, monkeypatch, capsys):
        """unittest for Page0Gui.add_listitem
        """
        monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        result = testobj.add_listitem('data')
        assert isinstance(result, testee.qtw.QTreeWidgetItem)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.setData to `data` with role"
                                           f" {testee.core.Qt.ItemDataRole.UserRole} for col 0\n"
                                           "called Tree.addTopLevelItem\n")

    def test_set_listitem_values(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_listitem_values
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = mockqtw.MockTreeWidget()
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called TreeItem.__init__ with args ()\n")
        testobj.set_listitem_values(item, ('xxx', 'yyy.a', 'zzz.b', 'q'))
        assert testobj.p0list.has_selection
        assert capsys.readouterr().out == ("called TreeItem.setText with arg `xxx (A)` for col 0\n"
                                           "called TreeItem.setText with arg `A` for col 1\n"
                                           "called TreeItem.setText with arg `b` for col 2\n")
        testobj.set_listitem_values(item, ('xxx', 'y.abc', 'z.defg', 'hij', 'klm', ''))
        assert testobj.p0list.has_selection
        assert capsys.readouterr().out == ("called TreeItem.setText with arg `xxx` for col 0\n"
                                           "called TreeItem.setText with arg `A` for col 1\n"
                                           "called TreeItem.setText with arg `defg` for col 2\n"
                                           "called TreeItem.setText with arg `hij` for col 3\n"
                                           "called TreeItem.setText with arg `klm` for col 4\n")

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
        testobj.p0list = mockqtw.MockTreeWidget()
        testobj.p0list.topLevelItemCount = mock_count
        testobj.p0list.topLevelItem = mock_item
        assert capsys.readouterr().out == "called Tree.__init__\n"
        assert testobj.get_items() == ['item0', 'item1']
        assert capsys.readouterr().out == ("called Tree.topLevelItemCount\n"
                                           "called Tree.topLevelItem with arg 0\n"
                                           "called Tree.topLevelItem with arg 1\n")

    def test_get_item_text(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_item_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        item = mockqtw.MockTreeItem('col0', 'col1')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('col0', 'col1')\n"
        for column in (0, 1):
            assert testobj.get_item_text(item, column) == f"col{column}"
        assert capsys.readouterr().out == ("called TreeItem.text for col 0\n"
                                           "called TreeItem.text for col 1\n")

    def test_set_item_text(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_item_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.set_item_text(item, 0, 'text')
        assert capsys.readouterr().out == ("called TreeItem.setText with arg `text` for col 0\n")

    def test_get_first_item(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_first_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        assert testobj.get_first_item() == "Tree.topLevelItem"
        assert capsys.readouterr().out == ("called Tree.topLevelItem with arg `0`\n")

    def test_get_item_by_index(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_item_by_index
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        assert testobj.get_item_by_index('item_n') == "Tree.topLevelItem"
        assert capsys.readouterr().out == ("called Tree.topLevelItem with arg `item_n`\n")

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
        testobj.p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.p0list.findItems = mock_find
        assert testobj.get_item_by_id('item_id') is None
        assert capsys.readouterr().out == (
                "called Tree.findItems with args ('item_id', <MatchFlag.MatchExactly: 0>, 0)\n")
        testobj.p0list.findItems = mock_find_2
        assert testobj.get_item_by_id('item_id') == 'x'
        assert capsys.readouterr().out == (
                "called Tree.findItems with args ('item_id', <MatchFlag.MatchExactly: 0>, 0)\n")

    def test_has_selection(self, monkeypatch, capsys):
        """unittest for Page0Gui.has_selection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.p0list.has_selection = True
        assert testobj.has_selection()
        testobj.p0list.has_selection = False
        assert not testobj.has_selection()

    def test_set_selection(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_selection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(current_item=None)
        testobj.p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.set_selection()
        assert capsys.readouterr().out == ""
        testobj.parent.current_item = 'not None'
        testobj.set_selection()
        assert capsys.readouterr().out == "called Tree.setCurrentItem with arg `not None`\n"

    def test_get_selection(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_selection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        assert testobj.get_selection() == "called Tree.currentItem"
        assert capsys.readouterr().out == ("")

    def test_ensure_visible(self, monkeypatch, capsys):
        """unittest for Page0Gui.ensure_visible
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.ensure_visible('item')
        assert capsys.readouterr().out == "called Tree.scrollToItem with arg `item`\n"

    def test_set_archive_button_text(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_archive_button_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.archive_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
        testobj.set_archive_button_text('text')
        assert capsys.readouterr().out == "called PushButton.setText with arg `text`\n"

    def test_get_selected_action(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_selected_action
        """
        def mock_item():
            print('called Tree.currentItem')
            return item
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = mockqtw.MockTreeWidget()
        item = mockqtw.MockTreeItem()
        item.setData(0, testee.core.Qt.ItemDataRole.UserRole, 'data')
        testobj.p0list.currentItem = mock_item
        assert capsys.readouterr().out == (
                "called Tree.__init__\n"
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.setData to `data` with role 256 for col 0\n")
        assert testobj.get_selected_action() == "data"
        assert capsys.readouterr().out == ("called Tree.currentItem\n"
                                           "called TreeItem.data for col 0 role 256\n")

    def test_get_list_row(self, monkeypatch, capsys):
        """unittest for Page0Gui.get_list_row
        """
        def mock_get():
            print('called Page0Gui.get_selection')
            return 'selection'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_selection = mock_get
        assert testobj.get_list_row() == "selection"
        assert capsys.readouterr().out == "called Page0Gui.get_selection\n"

    def test_set_list_row(self, monkeypatch, capsys):
        """unittest for Page0Gui.set_list_row
        """
        def mock_set():
            print('called Page0Gui.set_selection')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_selection = mock_set
        testobj.set_list_row('num')
        assert capsys.readouterr().out == "called Page0Gui.set_selection\n"


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
        parent = MockGui()
        master = MockPage()
        monkeypatch.setattr(testee.Page1Gui, '__init__', mock_init)
        testobj = testee.Page1Gui(parent, master)
        assert capsys.readouterr().out == (
                "called Gui.__init__ with args ()\n"
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
            self.parent = parent
            self.master = master
            self.appbase = types.SimpleNamespace(use_text_panels=False)
        def mock_init_2(self, parent, master):
            """stub
            """
            print(f'called PageGui.__init__ with args ({parent}, {master})')
            self.parent = parent
            self.master = master
            self.appbase = types.SimpleNamespace(use_text_panels=True)
        parent = MockGui()
        master = MockPage()
        assert capsys.readouterr().out == ("called Gui.__init__ with args ()\n"
                                           'called Page.__init__\n')
        monkeypatch.setattr(testee.PageGui, '__init__', mock_init)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw, 'QTextEdit', mockqtw.MockEditorWidget)
        monkeypatch.setattr(testee.gui, 'QShortcut', mockqtw.MockShortcut)
        testobj = testee.Page1Gui(parent, master)
        assert isinstance(testobj.id_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.date_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.proc_entry, testee.qtw.QLineEdit)
        assert isinstance(testobj.desc_entry, testee.qtw.QLineEdit)
        assert isinstance(testobj.cat_choice, testee.qtw.QComboBox)
        assert isinstance(testobj.stat_choice, testee.qtw.QComboBox)
        assert isinstance(testobj.archive_text, testee.qtw.QLabel)
        assert isinstance(testobj.archive_button, testee.qtw.QPushButton)
        assert isinstance(testobj.summary_entry, testee.qtw.QTextEdit)
        assert isinstance(testobj.save_button, testee.qtw.QPushButton)
        assert isinstance(testobj.saveandgo_button, testee.qtw.QPushButton)
        assert isinstance(testobj.cancel_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['page1_init'].format(testobj=testobj)
        monkeypatch.setattr(testee.PageGui, '__init__', mock_init_2)
        testobj = testee.Page1Gui(parent, master)
        assert isinstance(testobj.id_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.date_text, testee.qtw.QLineEdit)
        assert isinstance(testobj.proc_entry, testee.qtw.QLineEdit)
        assert isinstance(testobj.desc_entry, testee.qtw.QLineEdit)
        assert isinstance(testobj.cat_choice, testee.qtw.QComboBox)
        assert isinstance(testobj.stat_choice, testee.qtw.QComboBox)
        assert isinstance(testobj.archive_text, testee.qtw.QLabel)
        assert isinstance(testobj.archive_button, testee.qtw.QPushButton)
        assert isinstance(testobj.save_button, testee.qtw.QPushButton)
        assert isinstance(testobj.saveandgo_button, testee.qtw.QPushButton)
        assert isinstance(testobj.cancel_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['page1_init2'].format(testobj=testobj)

    def test_doelayout(self, monkeypatch, capsys, expected_output):
        """unittest for Page1Gui.doelayout
        """
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.Page1Gui, 'setLayout', mockqtw.MockWidget.setLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.id_text = mockqtw.MockLineEdit()
        testobj.date_text = mockqtw.MockLineEdit()
        testobj.proc_entry = mockqtw.MockLineEdit()
        testobj.desc_entry = mockqtw.MockLineEdit()
        testobj.cat_choice = mockqtw.MockComboBox()
        testobj.stat_choice = mockqtw.MockComboBox()
        testobj.archive_text = mockqtw.MockLabel()
        testobj.archive_button = mockqtw.MockPushButton()
        testobj.summary_entry = mockqtw.MockEditorWidget()
        testobj.save_button = mockqtw.MockPushButton()
        testobj.saveandgo_button = mockqtw.MockPushButton()
        testobj.cancel_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called ComboBox.__init__\ncalled ComboBox.__init__\n"
                                           "called Label.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called Editor.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.appbase = types.SimpleNamespace(use_text_panels=True)
        testobj.doelayout()
        assert capsys.readouterr().out == expected_output['page1_layout'].format(testobj=testobj)
        testobj.appbase = types.SimpleNamespace(use_text_panels=False)
        testobj.doelayout()
        assert capsys.readouterr().out == expected_output['page1_layout2'].format(testobj=testobj)

    def test_init_fields(self, monkeypatch, capsys):
        """unittest for Page1Gui.init_fields
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.id_text = mockqtw.MockLineEdit()
        testobj.date_text = mockqtw.MockLineEdit()
        testobj.proc_entry = mockqtw.MockLineEdit()
        testobj.desc_entry = mockqtw.MockLineEdit()
        testobj.cat_choice = mockqtw.MockComboBox()
        testobj.stat_choice = mockqtw.MockComboBox()
        testobj.archive_text = mockqtw.MockLabel()
        testobj.summary_entry = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == ("called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called ComboBox.__init__\ncalled ComboBox.__init__\n"
                                           "called Label.__init__\ncalled Editor.__init__\n")
        testobj.appbase = types.SimpleNamespace(use_text_panels=False)
        testobj.init_fields()
        assert capsys.readouterr().out == ("called LineEdit.clear\ncalled LineEdit.clear\n"
                                           "called LineEdit.clear\ncalled LineEdit.clear\n"
                                           "called Label.setText with arg ``\ncalled Editor.clear\n"
                                           "called ComboBox.setCurrentIndex with arg `0`\n"
                                           "called ComboBox.setCurrentIndex with arg `0`\n")
        testobj.appbase.use_text_panels = True
        testobj.init_fields()
        assert capsys.readouterr().out == ("called LineEdit.clear\ncalled LineEdit.clear\n"
                                           "called LineEdit.clear\ncalled LineEdit.clear\n"
                                           "called Label.setText with arg ``\n"
                                           "called ComboBox.setCurrentIndex with arg `0`\n"
                                           "called ComboBox.setCurrentIndex with arg `0`\n")

    def test_set_text(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.id_text = mockqtw.MockLineEdit()
        testobj.date_text = mockqtw.MockLineEdit()
        testobj.proc_entry = mockqtw.MockLineEdit()
        testobj.desc_entry = mockqtw.MockLineEdit()
        testobj.archive_text = mockqtw.MockLabel()
        testobj.summary_entry = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == ("called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called Label.__init__\ncalled Editor.__init__\n")
        testobj.set_text('id', 'value')
        assert capsys.readouterr().out == ("called LineEdit.setText with arg `value`\n")
        testobj.set_text('date', 'value')
        assert capsys.readouterr().out == ("called LineEdit.setText with arg `value`\n")
        testobj.set_text('proc', 'value')
        assert capsys.readouterr().out == ("called LineEdit.setText with arg `value`\n")
        testobj.set_text('desc', 'value')
        assert capsys.readouterr().out == ("called LineEdit.setText with arg `value`\n")
        testobj.set_text('arch', 'value')
        assert capsys.readouterr().out == ("called Label.setText with arg `value`\n")
        testobj.set_text('summary', 'value')
        assert capsys.readouterr().out == ("called Editor.setPlainText with arg `value`\n")
        testobj.set_text('xx', 'value')
        assert capsys.readouterr().out == ""

    def test_get_text(self, monkeypatch, capsys):
        """unittest for Page1Gui.get_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.id_text = mockqtw.MockLineEdit('xx')
        testobj.date_text = mockqtw.MockLineEdit('yy')
        testobj.proc_entry = mockqtw.MockLineEdit('zz')
        testobj.desc_entry = mockqtw.MockLineEdit('qq')
        testobj.summary_entry = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == ("called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called Editor.__init__\n")
        assert testobj.get_text('id') == "xx"
        assert capsys.readouterr().out == ("called LineEdit.text\n")
        assert testobj.get_text('date') == "yy"
        assert capsys.readouterr().out == ("called LineEdit.text\n")
        assert testobj.get_text('proc') == "zz"
        assert capsys.readouterr().out == ("called LineEdit.text\n")
        assert testobj.get_text('desc') == "qq"
        assert capsys.readouterr().out == ("called LineEdit.text\n")
        assert testobj.get_text('summary') == "editor text"
        assert capsys.readouterr().out == ("called Editor.toPlainText\n")
        with pytest.raises(UnboundLocalError):
            assert testobj.get_text('xx') == ""

    def test_set_choice(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_choice
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        domain = ['x', 'y', 'z']
        field = mockqtw.MockComboBox()
        field.itemData = lambda x: ['aaa', 'bbb', 'ccc'][x]
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.set_choice(domain, field, 'bbb')
        assert capsys.readouterr().out == "called ComboBox.setCurrentIndex with arg `1`\n"
        testobj.set_choice(domain, field, 'qqq')
        assert capsys.readouterr().out == ""

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

    def test_set_oldbuf(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_oldbuf
        """
        def mock_get():
            print('called Page1Gui.get_fieldvalues')
            return ['field', 'value', 's']
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_fieldvalues = mock_get
        assert testobj.set_oldbuf() == ['field', 'value', 's']
        assert capsys.readouterr().out == ("called Page1Gui.get_fieldvalues\n")

    def test_get_field_text(self, monkeypatch, capsys):
        """unittest for Page1Gui.get_field_text
        """
        def mock_choice(arg):
            print(f'called Page1Gui.get_choice_data with arg {arg}')
            return arg
        def mock_text(arg):
            print(f'called Page1Gui.get_text with arg {arg}')
            return arg
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_choice_data = mock_choice
        testobj.get_text = mock_text
        assert testobj.get_field_text('actie') == "id"
        assert capsys.readouterr().out == ("called Page1Gui.get_text with arg id\n")
        assert testobj.get_field_text('datum') == "date"
        assert capsys.readouterr().out == ("called Page1Gui.get_text with arg date\n")
        assert testobj.get_field_text('oms') == "proc"
        assert capsys.readouterr().out == ("called Page1Gui.get_text with arg proc\n")
        assert testobj.get_field_text('tekst') == "desc"
        assert capsys.readouterr().out == ("called Page1Gui.get_text with arg desc\n")
        assert testobj.get_field_text('summary') == "smry"
        assert capsys.readouterr().out == ("called Page1Gui.get_text with arg smry\n")
        assert testobj.get_field_text('status') == "t"
        assert capsys.readouterr().out == ("called Page1Gui.get_choice_data with arg stat\n")
        assert testobj.get_field_text('soort') == "a"
        assert capsys.readouterr().out == ("called Page1Gui.get_choice_data with arg cat\n")

    def test_set_archive_button_text(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_archive_button_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.archive_button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == 'called PushButton.__init__ with args () {}\n'
        testobj.set_archive_button_text('value')
        assert capsys.readouterr().out == ("called PushButton.setText with arg `value`\n")

    def test_enable_fields(self, monkeypatch, capsys):
        """unittest for Page1Gui.enable_fields
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.id_text = mockqtw.MockLineEdit()
        testobj.date_text = mockqtw.MockLineEdit()
        testobj.proc_entry = mockqtw.MockLineEdit()
        testobj.desc_entry = mockqtw.MockLineEdit()
        testobj.cat_choice = mockqtw.MockComboBox()
        testobj.stat_choice = mockqtw.MockComboBox()
        testobj.archive_button = mockqtw.MockPushButton()
        testobj.summary_entry = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == ("called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called ComboBox.__init__\ncalled ComboBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called Editor.__init__\n")
        testobj.master = types.SimpleNamespace(parent=types.SimpleNamespace(newitem=False))
        testobj.appbase = types.SimpleNamespace(is_user=True, use_text_panels=False)
        testobj.enable_fields('state')
        assert capsys.readouterr().out == ("called LineEdit.setEnabled with arg False\n"
                                           "called LineEdit.setEnabled with arg False\n"
                                           "called LineEdit.setEnabled with arg state\n"
                                           "called LineEdit.setEnabled with arg state\n"
                                           "called ComboBox.setEnabled with arg state\n"
                                           "called ComboBox.setEnabled with arg state\n"
                                           "called PushButton.setEnabled with arg `True`\n"
                                           "called Editor.setEnabled with arg state\n")
        testobj.master.parent.newitem = True
        testobj.appbase.use_text_panels = True
        testobj.enable_fields('state')
        assert capsys.readouterr().out == ("called LineEdit.setEnabled with arg False\n"
                                           "called LineEdit.setEnabled with arg False\n"
                                           "called LineEdit.setEnabled with arg state\n"
                                           "called LineEdit.setEnabled with arg state\n"
                                           "called ComboBox.setEnabled with arg state\n"
                                           "called ComboBox.setEnabled with arg state\n"
                                           "called PushButton.setEnabled with arg `False`\n")
        testobj.appbase.is_user = False
        testobj.enable_fields('state')
        assert capsys.readouterr().out == ("called LineEdit.setEnabled with arg False\n"
                                           "called LineEdit.setEnabled with arg False\n"
                                           "called LineEdit.setEnabled with arg state\n"
                                           "called LineEdit.setEnabled with arg state\n"
                                           "called ComboBox.setEnabled with arg state\n"
                                           "called ComboBox.setEnabled with arg state\n"
                                           "called PushButton.setEnabled with arg `False`\n")

    def test_clear_stats(self, monkeypatch, capsys):
        """unittest for Page1Gui.clear_stats
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.stat_choice = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.clear_stats()
        assert capsys.readouterr().out == "called ComboBox.clear\n"

    def test_clear_cats(self, monkeypatch, capsys):
        """unittest for Page1Gui.clear_cats
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.cat_choice = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.clear_cats()
        assert capsys.readouterr().out == "called ComboBox.clear\n"

    def test_add_cat_choice(self, monkeypatch, capsys):
        """unittest for Page1Gui.add_cat_choice
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.cat_choice = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.add_cat_choice('text', 'value')
        assert capsys.readouterr().out == (
                "called ComboBox.addItem with arg `text`, userdata = value\n")

    def test_add_stat_choice(self, monkeypatch, capsys):
        """unittest for Page1Gui.add_stat_choice
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.stat_choice = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.add_stat_choice('text', 'value')
        assert capsys.readouterr().out == (
                "called ComboBox.addItem with arg `text`, userdata = value\n")

    def test_set_focus(self, monkeypatch, capsys):
        """unittest for Page1Gui.set_focus
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.proc_entry = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.set_focus()
        assert capsys.readouterr().out == "called LineEdit.setFocus\n"

    def test_build_newbuf(self, monkeypatch, capsys):
        """unittest for Page1Gui.build_newbuf
        """
        def mock_get():
            print('called Page1Gui.get_fieldvalues')
            return ['field', 'value', 's']
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_fieldvalues = mock_get
        assert testobj.build_newbuf() == ['field', 'value', 's']
        assert capsys.readouterr().out == "called Page1Gui.get_fieldvalues\n"

    def test_get_fieldvalues(self, monkeypatch, capsys):
        """unittest for Page1Gui.get_fieldvalues
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.proc_entry = mockqtw.MockLineEdit()
        testobj.desc_entry = mockqtw.MockLineEdit()
        testobj.stat_choice = mockqtw.MockComboBox()
        testobj.cat_choice = mockqtw.MockComboBox()
        testobj.summary_entry = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == ("called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called ComboBox.__init__\ncalled ComboBox.__init__\n"
                                           "called Editor.__init__\n")
        testobj.appbase = types.SimpleNamespace(use_text_panels=True)
        assert testobj.get_fieldvalues() == ['', '', 1, 1]
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called ComboBox.currentIndex\n"
                                           "called ComboBox.currentIndex\n")
        testobj.appbase = types.SimpleNamespace(use_text_panels=False)
        assert testobj.get_fieldvalues() == ['', '', 1, 1, 'editor text']
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called ComboBox.currentIndex\n"
                                           "called ComboBox.currentIndex\n"
                                           "called Editor.toPlainText\n")


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
        parent = MockGui()
        master = MockPage()
        monkeypatch.setattr(testee.Page6Gui, '__init__', mock_init)
        testobj = testee.Page6Gui(parent, master)
        assert capsys.readouterr().out == (
                "called Gui.__init__ with args ()\n"
                'called Page.__init__\n'
                f'called Page6Gui.__init__ with args ({parent}, {master})\n')
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for Page6Gui.__init__
        """
        def mock_init(self, parent, master):
            """stub
            """
            print(f'called PageGui.__init__ with args ({parent}, {master})')
            self.parent = parent
            self.master = master
            self.appbase = types.SimpleNamespace(use_rt=False, work_with_user=True)
        def mock_init_2(self, parent, master):
            """stub
            """
            print(f'called PageGui.__init__ with args ({parent}, {master})')
            self.parent = parent
            self.master = master
            self.appbase = types.SimpleNamespace(use_rt=True, work_with_user=False)
        def mock_text(self, *args, **kwargs):
            print('called PageGui.create_text_field with args', args, kwargs)
            result = mockqtw.MockEditorWidget()
            self.actiondict['xx'] = 'yyy'
            return result
        def mock_toolbar(self, *args, **kwargs):
            print('called PageGui.create_toolbar with args', args, kwargs)
            self.toolbar = mockqtw.MockToolBar()
        parent = MockGui()
        master = MockPage()
        monkeypatch.setattr(testee.PageGui, '__init__', mock_init)
        monkeypatch.setattr(testee.PageGui, 'create_text_field', mock_text)
        monkeypatch.setattr(testee.PageGui, 'create_toolbar', mock_toolbar)
        monkeypatch.setattr(testee.qtw, 'QSplitter', mockqtw.MockSplitter)
        monkeypatch.setattr(testee.qtw, 'QListWidget', mockqtw.MockListBox)
        monkeypatch.setattr(testee.gui, 'QShortcut', mockqtw.MockShortcut)
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        assert capsys.readouterr().out == ("called Gui.__init__ with args ()\n"
                                           'called Page.__init__\n')
        monkeypatch.setattr(testee, 'LIN', True)
        testobj = testee.Page6Gui(parent, master)
        assert isinstance(testobj.pnl, testee.qtw.QSplitter)
        assert isinstance(testobj.progress_list, testee.qtw.QListWidget)
        assert isinstance(testobj.progress_text, mockqtw.MockEditorWidget)
        assert isinstance(testobj.new_action, mockqtw.MockShortcut)
        assert isinstance(testobj.save_button, mockqtw.MockPushButton)
        assert isinstance(testobj.cancel_button, mockqtw.MockPushButton)
        assert testobj.actiondict == {'xx': 'yyy'}
        assert capsys.readouterr().out == expected_output['page6_init'].format(testobj=testobj,
                                                                               topsize=200,
                                                                               bottomsize=250)

        monkeypatch.setattr(testee, 'LIN', False)
        monkeypatch.setattr(testee.PageGui, '__init__', mock_init_2)
        testobj = testee.Page6Gui(parent, master)
        assert isinstance(testobj.pnl, testee.qtw.QSplitter)
        assert isinstance(testobj.progress_list, testee.qtw.QListWidget)
        assert isinstance(testobj.progress_text, mockqtw.MockEditorWidget)
        assert isinstance(testobj.new_action, mockqtw.MockShortcut)
        assert isinstance(testobj.toolbar, mockqtw.MockToolBar)
        assert isinstance(testobj.save_button, mockqtw.MockPushButton)
        assert isinstance(testobj.cancel_button, mockqtw.MockPushButton)
        assert testobj.actiondict == {'xx': 'yyy'}
        assert capsys.readouterr().out == expected_output['page6_init2'].format(testobj=testobj,
                                                                               topsize=280,
                                                                               bottomsize=110)

    def test_doelayout(self, monkeypatch, capsys, expected_output):
        """unittest for Page6Gui.doelayout
        """
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.Page6Gui, 'setLayout', mockqtw.MockWidget.setLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockqtw.MockSplitter()
        testobj.save_button = mockqtw.MockPushButton()
        testobj.cancel_button = mockqtw.MockPushButton()
        testobj.doelayout()
        assert capsys.readouterr().out == expected_output['page6_layout']

    def test_on_activate_item(self, monkeypatch, capsys):
        """unittest for Page6Gui.on_activate_item
        """
        def mock_init():
            print('called Page6.initialize_new_event')
        def mock_item(arg):
            print(f"called Page6Gui.is_first_item with arg {arg}")
            return False
        def mock_item_2(arg):
            print(f"called Page6Gui.is_first_item with arg {arg}")
            return True
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(initializing=True, initialize_new_event=mock_init)
        testobj.is_first_line = mock_item
        testobj.on_activate_item()
        assert capsys.readouterr().out == ""
        testobj.master.initializing = False
        testobj.on_activate_item()
        assert capsys.readouterr().out == "called Page6.initialize_new_event\n"
        testobj.on_activate_item('xxx')
        assert capsys.readouterr().out == "called Page6Gui.is_first_item with arg xxx\n"
        testobj.is_first_line = mock_item_2
        testobj.on_activate_item('xxx')
        assert capsys.readouterr().out == ("called Page6Gui.is_first_item with arg xxx\n"
                                           "called Page6.initialize_new_event\n")
        testobj.on_activate_item()
        assert capsys.readouterr().out == "called Page6.initialize_new_event\n"

    def test_add_new_item_to_list(self, monkeypatch, capsys):
        """unittest for Page6Gui.add_new_item_to_list
        """
        monkeypatch.setattr(testee.qtw, 'QListWidgetItem', mockqtw.MockListItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_list = mockqtw.MockListBox()
        testobj.progress_text = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == "called List.__init__\ncalled Editor.__init__\n"
        testobj.add_new_item_to_list('someday', 'some text')
        assert capsys.readouterr().out == (
                "called ListItem.__init__ with args ('someday - some text',)\n"
                f"called ListItem.setData with args ({testee.core.Qt.ItemDataRole.UserRole!r}, 0)\n"
                "called List.insertItem with args (1, item of type"
                " <class 'mockgui.mockqtwidgets.MockListItem'>)\n"
                "called List.setCurrentRow with rownumber 1\n"
                "called Editor.setText with arg `some text`\n"
                "called Editor.setReadOnly with arg `False`\n"
                "called Editor.setFocus\n")

    def test_is_first_line(self, monkeypatch, capsys):
        """unittest for Page6Gui.is_first_line
        """
        def mock_item(num):
            print(f'called ListWidget.item with arg {num}')
            if num == 0:
                return item1
            return item2
        testobj = self.setup_testobj(monkeypatch, capsys)
        item1 = mockqtw.MockListItem()
        item2 = mockqtw.MockListItem()
        testobj.progress_list = mockqtw.MockListBox()
        assert capsys.readouterr().out == ("called ListItem.__init__\ncalled ListItem.__init__\n"
                                           "called List.__init__\n")
        testobj.progress_list.item = mock_item
        assert testobj.is_first_line(item1)
        assert capsys.readouterr().out == "called ListWidget.item with arg 0\n"
        assert not testobj.is_first_line(item2)
        assert capsys.readouterr().out == "called ListWidget.item with arg 0\n"

    def _test_on_select_item(self, monkeypatch, capsys):
        """unittest for Page6Gui.on_select_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_select_item(item_n, item_o) == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_init_textfield(self, monkeypatch, capsys):
        """unittest for Page6Gui.init_textfield
        """
        def mock_clear():
            print('called Page6Gui.clear_textfield')
        def mock_protect():
            print('called Page6Gui.protect_textfield')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.clear_textfield = mock_clear
        testobj.protect_textfield = mock_protect
        testobj.init_textfield()
        assert capsys.readouterr().out == ("called Page6Gui.clear_textfield\n"
                                           "called Page6Gui.protect_textfield\n")

    def test_init_list(self, monkeypatch, capsys):
        """unittest for Page6Gui.init_list
        """
        def mock_add(*args):
            print('called List.addItem')
        monkeypatch.setattr(testee.qtw, 'QListWidgetItem', mockqtw.MockListItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_list = mockqtw.MockListBox()
        testobj.progress_list.addItem = mock_add
        testobj.progress_text = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == "called List.__init__\ncalled Editor.__init__\n"
        testobj.init_list('text')
        assert capsys.readouterr().out == ("called List.clear\n"
                                           "called ListItem.__init__ with args ('text',)\n"
                                           "called ListItem.setData with args"
                                           f" ({testee.core.Qt.ItemDataRole.UserRole!r}, -1)\n"
                                           "called List.addItem\n")

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
        testobj.progress_list = mockqtw.MockListBox()
        testobj.progress_list.addItem = mock_add
        testobj.progress_text = mockqtw.MockEditorWidget()
        testobj.progress_text.set_contents = mock_set
        assert capsys.readouterr().out == "called List.__init__\ncalled Editor.__init__\n"
        testobj.master = types.SimpleNamespace(event_data=['xxxxxx', 10 * '1234567890'])
        testobj.progress_text.toPlainText = mock_text
        testobj.add_item_to_list(0, 'datum')
        assert capsys.readouterr().out == (
            f"called Editor.set_contents with arg '{testobj.master.event_data[0]}'\n"
            "called Editor.toPlainText\n"
            f"called ListItem.__init__ with args ('datum - {testobj.master.event_data[0]}',)\n"
            f"called ListItem.setData with args ({testee.core.Qt.ItemDataRole.UserRole!r}, 0)\n"
            "called List.addItem\n")
        testobj.progress_text.toPlainText = mock_text_2
        testobj.add_item_to_list(1, 'datum')
        text = 8 * '1234567890' + '...'
        assert capsys.readouterr().out == (
            f"called Editor.set_contents with arg '{testobj.master.event_data[1]}'\n"
            "called Editor.toPlainText\n"
            f"called ListItem.__init__ with args ('datum - {text}',)\n"
            f"called ListItem.setData with args ({testee.core.Qt.ItemDataRole.UserRole!r}, 1)\n"
            "called List.addItem\n")

    def test_set_list_callback(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_list_callback
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.appbase = types.SimpleNamespace(is_user=True)
        testobj.on_activate_item = lambda: 'dummy'
        testobj.progress_list = mockqtw.MockListBox()
        testobj.new_action = mockqtw.MockShortcut()
        assert capsys.readouterr().out == ("called List.__init__\n"
                                           "called Shortcut.__init__ with args ()\n")
        testobj.set_list_callback()
        assert capsys.readouterr().out == (
                f"called Signal.connect with args ({testobj.on_activate_item},)\n"
                "called List.item with arg 0'\n"
                "called Signal.connect with args"
                f" (functools.partial({testobj.on_activate_item}, None),)\n")
        testobj.appbase.is_user = False
        testobj.set_list_callback()
        assert capsys.readouterr().out == ("called Signal.disconnect\n"
                                           "called Signal.disconnect\n")

    def test_clear_textfield(self, monkeypatch, capsys):
        """unittest for Page6Gui.clear_textfield
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_text = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == "called Editor.__init__\n"
        testobj.clear_textfield()
        assert capsys.readouterr().out == ("called Editor.clear\n")

    def test_protect_textfield(self, monkeypatch, capsys):
        """unittest for Page6Gui.protect_textfield
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_text = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == "called Editor.__init__\n"
        testobj.protect_textfield()
        assert capsys.readouterr().out == ("called Editor.setReadOnly with arg `True`\n")
        testobj.protect_textfield(False)
        assert capsys.readouterr().out == ("called Editor.setReadOnly with arg `False`\n")

    def test_get_textfield_contents(self, monkeypatch, capsys):
        """unittest for Page6Gui.get_textfield_contents
        """
        def mock_get():
            print('called Editor.get_contents')
            return 'editor text'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_text = mockqtw.MockEditorWidget()
        testobj.progress_text.get_contents = mock_get
        assert capsys.readouterr().out == "called Editor.__init__\n"
        assert testobj.get_textfield_contents() == "editor text"
        assert capsys.readouterr().out == ("called Editor.get_contents\n")

    def test_set_textfield_contents(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_textfield_contents
        """
        def mock_set(value):
            print(f"called Editor.set_contents with arg '{value}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_text = mockqtw.MockEditorWidget()
        testobj.progress_text.set_contents = mock_set
        assert capsys.readouterr().out == "called Editor.__init__\n"
        testobj.set_textfield_contents('text')
        assert capsys.readouterr().out == ("called Editor.set_contents with arg 'text'\n")

    def test_set_listitem_text(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_listitem_text
        """
        def mock_item(indx):
            result = mockqtw.MockListItem()
            assert capsys.readouterr().out == "called ListItem.__init__\n"
            print(f'called List.item with arg {indx}')
            return result
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_list = mockqtw.MockListBox()
        testobj.progress_list.item = mock_item
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj.set_listitem_text(1, 'text')
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
        testobj.progress_list = mockqtw.MockListBox()
        testobj.progress_list.item = mock_item
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj.set_listitem_data(1)
        assert capsys.readouterr().out == ("called List.item with arg 1\n"
                                           "called ListItem.setData with args"
                                           f" (0, {testee.core.Qt.ItemDataRole.UserRole!r})\n")

    def test_get_list_row(self, monkeypatch, capsys):
        """unittest for Page6Gui.get_list_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_list = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        assert testobj.get_list_row() == "current row"
        assert capsys.readouterr().out == ("called List.currentRow\n")

    def test_set_list_row(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_list_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_list = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj.set_list_row('num')
        assert capsys.readouterr().out == ("called List.setCurrentRow with rownumber num\n")

    def test_get_list_rowcount(self, monkeypatch, capsys):
        """unittest for Page6Gui.get_list_rowcount
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_list = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        assert testobj.get_list_rowcount() == 0
        assert capsys.readouterr().out == ("")

    def test_move_cursor_to_end(self, monkeypatch, capsys):
        """unittest for Page6Gui.move_cursor_to_end
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_text = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == "called Editor.__init__\n"
        testobj.move_cursor_to_end()
        assert capsys.readouterr().out == ("called Editor.moveCursor with args"
                                           f" ({testee.gui.QTextCursor.MoveOperation.End!r},"
                                           f" {testee.gui.QTextCursor.MoveMode.MoveAnchor!r})\n")

    def test_set_focus_to_textfield(self, monkeypatch, capsys):
        """unittest for Page6Gui.set_focus_to_textfield
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_text = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == "called Editor.__init__\n"
        testobj.set_focus_to_textfield()
        assert capsys.readouterr().out == ("called Editor.setFocus\n")

    def test_convert_text(self, monkeypatch, capsys):
        """unittest for Page6Gui.convert_text
        """
        def mock_set(value):
            print(f"called Editor.set_contents with arg '{value}'")
        def mock_get():
            print("called Editor.get_contents")
            return 'editor text'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_text = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == "called Editor.__init__\n"
        testobj.progress_text.set_contents = mock_set
        testobj.progress_text.get_contents = mock_get
        assert testobj.convert_text('text', 'rich') == "editor text"
        assert capsys.readouterr().out == ("called Editor.set_contents with arg 'text'\n"
                                          "called Editor.get_contents\n")
        assert testobj.convert_text('text', 'plain') == "editor text"
        assert capsys.readouterr().out == ("called Editor.toPlainText\n")

    def test_get_listitem_text(self, monkeypatch, capsys):
        """unittest for Page6Gui.get_listitem_text
        """
        def mock_item(indx):
            result = mockqtw.MockListItem('xxx')
            assert capsys.readouterr().out == "called ListItem.__init__ with args ('xxx',)\n"
            print(f'called List.item with arg {indx}')
            return result
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.progress_list = mockqtw.MockListBox()
        testobj.progress_list.item = mock_item
        assert capsys.readouterr().out == "called List.__init__\n"
        assert testobj.get_listitem_text('itemindex') == "xxx"
        assert capsys.readouterr().out == ("called List.item with arg itemindex\n")

    def test_build_newbuf(self, monkeypatch, capsys):
        """unittest for Page6Gui.build_newbuf
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(event_list=['111', '222'], event_data=['aaa', 'bbb'])
        assert testobj.build_newbuf() == (['111', '222'], ['aaa', 'bbb'])
        assert capsys.readouterr().out == ""


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
        monkeypatch.setattr(testee.SortOptionsDialog, '__init__', mock_init)
        testobj = testee.SortOptionsDialog()
        assert capsys.readouterr().out == 'called SortOptionsDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for SortOptionsDialog.__init__
        """
        def mock_set(self):
            print('called SortOptionsDialog.set_defaults')
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.SortOptionsDialog, 'set_defaults', mock_set)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QButtonGroup', mockqtw.MockButtonGroup)
        monkeypatch.setattr(testee.qtw, 'QRadioButton', mockqtw.MockRadioButton)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        parent = types.SimpleNamespace()  # PageGui
        args = [{}, []]
        testobj = testee.SortOptionsDialog(parent, args)
        assert testobj.parent == parent
        assert testobj._widgets == []
        assert isinstance(testobj.on_off, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == expected_output['sortoptions'].format(testobj=testobj)
        args = [{'x': 'y'}, ['aa', 'bb']]
        testobj = testee.SortOptionsDialog(parent, args)
        assert testobj.parent == parent
        assert len(testobj._widgets) == 2
        for item in testobj._widgets:
            assert len(item) == 3
            assert isinstance(item[0], testee.qtw.QLabel)
            assert isinstance(item[1], testee.qtw.QComboBox)
            assert isinstance(item[2], testee.qtw.QButtonGroup)
        assert isinstance(testobj.on_off, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == expected_output['sortoptions2'].format(testobj=testobj)

    def test_set_defaults(self, monkeypatch, capsys):
        """unittest for SortOptionsDialog.set_defaults
        """
        def mock_enable(value):
            print(f'called SortOptionsDialog.enable_fields with arg {value}')
        def mock_button(self, arg):
            print(f'called ButtonGroup.button with arg {arg}')
            return mockqtw.MockRadioButton()
        monkeypatch.setattr(mockqtw.MockButtonGroup, 'button', mock_button)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.enable_fields = mock_enable
        testobj.on_off = mockqtw.MockCheckBox()
        testobj.parent = types.SimpleNamespace(master=MockPage())
        assert capsys.readouterr().out == "called CheckBox.__init__\ncalled Page.__init__\n"
        testobj.parent.master.sort_via_options = False
        testobj.parent.master.saved_sortopts = ''
        testobj._widgets = []
        testobj.set_defaults()
        assert capsys.readouterr().out == (
                "called SortOptionsDialog.enable_fields with arg False\n"
                "called CheckBox.setChecked with arg False\n")
        testobj.parent.master.sort_via_options = True
        testobj.parent.master.saved_sortopts = 'anything'
        testobj._widgets = [('', mockqtw.MockComboBox(), mockqtw.MockButtonGroup()),
                            ('', mockqtw.MockComboBox(), mockqtw.MockButtonGroup()),]
        testobj.sortopts = []  # niet waarschijnlijk
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called ButtonGroup.__init__ with args ()\n"
                                           "called ComboBox.__init__\n"
                                           "called ButtonGroup.__init__ with args ()\n")
        testobj.set_defaults()
        assert capsys.readouterr().out == (
                "called SortOptionsDialog.enable_fields with arg False\n"
                "called CheckBox.setChecked with arg True\n"
                "called CheckBox.setEnabled with arg False\n")
        testobj.sortopts = {1: ('rr', 'asc'), 0: ('qq', 'desc')}
        testobj.set_defaults()
        assert capsys.readouterr().out == (
                "called SortOptionsDialog.enable_fields with arg False\n"
                "called CheckBox.setChecked with arg True\n"
                "called CheckBox.setEnabled with arg False\n"
                "called ComboBox.setCurrentText with arg `qq`\n"
                "called ButtonGroup.button with arg 2\n"
                "called RadioButton.__init__ with args () {}\n"
                "called RadioButton.setChecked with arg `True`\n"
                "called ComboBox.setCurrentText with arg `rr`\n"
                "called ButtonGroup.button with arg 1\n"
                "called RadioButton.__init__ with args () {}\n"
                "called RadioButton.setChecked with arg `True`\n")

    def test_enable_fields(self, monkeypatch, capsys):
        """unittest for SortOptionsDialog.enable_fields
        """
        def mock_buttons(self):
            print('called ButtonGroup.buttons')
            return button1, button2
        monkeypatch.setattr(mockqtw.MockButtonGroup, 'buttons', mock_buttons)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._widgets = [(mockqtw.MockLabel(), mockqtw.MockComboBox(), mockqtw.MockButtonGroup())]
        button1 = mockqtw.MockRadioButton()
        button2 = mockqtw.MockRadioButton()
        assert capsys.readouterr().out == ("called Label.__init__\ncalled ComboBox.__init__\n"
                                           "called ButtonGroup.__init__ with args ()\n"
                                           "called RadioButton.__init__ with args () {}\n"
                                           "called RadioButton.__init__ with args () {}\n")
        testobj.enable_fields(False)
        assert capsys.readouterr().out == ("called ComboBox.setEnabled with arg False\n"
                                           "called ButtonGroup.buttons\n"
                                           "called RadioButton.setEnabled with arg `False`\n"
                                           "called RadioButton.setEnabled with arg `False`\n")
        testobj.enable_fields(True)
        assert capsys.readouterr().out == ("called ComboBox.setEnabled with arg True\n"
                                           "called ButtonGroup.buttons\n"
                                           "called RadioButton.setEnabled with arg `True`\n"
                                           "called RadioButton.setEnabled with arg `True`\n")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for SortOptionsDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(master=MockPage())
        assert capsys.readouterr().out == "called Page.__init__\n"
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
        monkeypatch.setattr(testee.SelectOptionsDialog, '__init__', mock_init)
        testobj = testee.SelectOptionsDialog()
        assert capsys.readouterr().out == 'called SelectOptionsDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for SelectOptionsDialog.__init__
        """
        def mock_set(self, arg):
            print(f'called SelectOptionsDialog.set_default_values with arg {arg}')
        def mock_doe(self):
            print('called SelectOptionsDialog.doelayout')
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        # monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.SelectOptionsDialog, 'set_default_values', mock_set)
        monkeypatch.setattr(testee.SelectOptionsDialog, 'doelayout', mock_doe)
        monkeypatch.setattr(testee.qtw, 'QButtonGroup', mockqtw.MockButtonGroup)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QRadioButton', mockqtw.MockRadioButton)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        parent = types.SimpleNamespace(parent=types.SimpleNamespace(parent=types.SimpleNamespace()))
        args = [{}, []]
        parent.parent.ctitels = ['x1', 'x2', 'x3', 'x4', 'x5']
        parent.parent.cats = {}
        parent.parent.stats = {}
        parent.parent.parent.use_separate_subject = False
        testobj = testee.SelectOptionsDialog(parent, args)

        assert isinstance(testobj.check_options, testee.qtw.QButtonGroup)
        assert isinstance(testobj.text_gt, testee.qtw.QLineEdit)
        assert isinstance(testobj.radio_id, testee.qtw.QButtonGroup)
        assert isinstance(testobj.text_lt, testee.qtw.QLineEdit)
        assert isinstance(testobj.check_cats, testee.qtw.QButtonGroup)
        assert isinstance(testobj.check_stats, testee.qtw.QButtonGroup)
        assert isinstance(testobj.text_zoek, testee.qtw.QLineEdit)
        assert isinstance(testobj.radio_arch, testee.qtw.QButtonGroup)
        assert isinstance(testobj.buttonbox, testee.qtw.QDialogButtonBox)

        assert testobj._data == []
        assert capsys.readouterr().out == expected_output['selectoptions'].format(testobj=testobj,
                                                                                  zoek='x5')

        parent.parent.parent.use_separate_subject = True
        parent.parent.cats = {2: ('yy', 1), 1: ('xx', 0)}
        parent.parent.stats = {2: ('bb', 'b'), 1: ('aa', 'a')}
        testobj = testee.SelectOptionsDialog(parent, args)

        assert isinstance(testobj.check_options, testee.qtw.QButtonGroup)
        assert isinstance(testobj.text_gt, testee.qtw.QLineEdit)
        assert isinstance(testobj.radio_id, testee.qtw.QButtonGroup)
        assert isinstance(testobj.text_lt, testee.qtw.QLineEdit)
        assert isinstance(testobj.check_cats, testee.qtw.QButtonGroup)
        assert isinstance(testobj.check_stats, testee.qtw.QButtonGroup)
        assert isinstance(testobj.text_zoek, testee.qtw.QLineEdit)
        assert isinstance(testobj.radio_id2, testee.qtw.QButtonGroup)
        assert isinstance(testobj.text_zoek2, testee.qtw.QLineEdit)
        assert isinstance(testobj.radio_arch, testee.qtw.QButtonGroup)
        assert isinstance(testobj.buttonbox, testee.qtw.QDialogButtonBox)

        assert testobj._data == []
        assert capsys.readouterr().out == expected_output['selectoptions2'].format(testobj=testobj,
                                                                                   zoek='zoek in')

    def test_doelayout(self, monkeypatch, capsys, expected_output):
        """unittest for SelectOptionsDialog.doelayout
        """
        def mock_buttons(self, *args):
            nonlocal counter
            counter += 1
            print('called ButtonGroup.buttons')
            if counter in (2, 9):
                return button2, button2
            if counter in (4, 6):
                return []
            return button2, button2, button2, button2, button2, button2, button2
        def mock_buttons_2(self, *args):
            nonlocal counter
            counter += 1
            print('called ButtonGroup.buttons')
            if counter in (2, 8, 10):
                return button2, button2
            if counter in (4, 6):
                return button1, button1
            return button2, button2, button2, button2, button2, button2, button2
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(parent=types.SimpleNamespace(
            parent=types.SimpleNamespace()))
        testobj.check_options = mockqtw.MockButtonGroup()
        testobj.text_gt = mockqtw.MockLineEdit()
        testobj.radio_id = mockqtw.MockButtonGroup()
        testobj.text_lt = mockqtw.MockLineEdit()
        testobj.check_cats = mockqtw.MockButtonGroup()
        testobj.radio_id2 = mockqtw.MockButtonGroup()
        testobj.check_stats = mockqtw.MockButtonGroup()
        testobj.text_zoek = mockqtw.MockLineEdit()
        testobj.text_zoek2 = mockqtw.MockLineEdit()
        testobj.radio_arch = mockqtw.MockButtonGroup()
        testobj.buttonbox = mockqtw.MockButtonBox()
        button1 = mockqtw.MockCheckBox()
        button2 = mockqtw.MockRadioButton()
        assert capsys.readouterr().out == (
                "called ButtonGroup.__init__ with args ()\n"
                "called LineEdit.__init__\ncalled ButtonGroup.__init__ with args ()\n"
                "called LineEdit.__init__\ncalled ButtonGroup.__init__ with args ()\n"
                "called ButtonGroup.__init__ with args ()\n"
                "called ButtonGroup.__init__ with args ()\ncalled LineEdit.__init__\n"
                "called LineEdit.__init__\ncalled ButtonGroup.__init__ with args ()\n"
                "called ButtonBox.__init__ with args ()\ncalled CheckBox.__init__\n"
                "called RadioButton.__init__ with args () {}\n")
        monkeypatch.setattr(mockqtw.MockButtonGroup, 'buttons', mock_buttons)
        testobj.parent.parent.ctitels = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6']
        testobj.parent.parent.parent.use_separate_subject = False
        counter = 0
        testobj.doelayout()
        assert capsys.readouterr().out == expected_output['selectlayout'].format(testobj=testobj)
        monkeypatch.setattr(mockqtw.MockButtonGroup, 'buttons', mock_buttons_2)
        testobj.parent.parent.parent.use_separate_subject = True
        counter = 0
        testobj.doelayout()
        assert capsys.readouterr().out == expected_output['selectlayout2'].format(testobj=testobj)

    def test_set_default_values(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.set_default_values
        """
        def mock_buttons(self):
            print('called ButtonGroup.buttons')
            return checkbutton0, checkbutton1, checkbutton2, checkbutton3, checkbutton4
        def mock_set(self, text):
            nonlocal counter
            counter += 1
            print(f'called LineEdit.setText with arg `{text}`')
            if counter == 1:
                raise TypeError
        monkeypatch.setattr(mockqtw.MockButtonGroup, 'buttons', mock_buttons)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(parent=types.SimpleNamespace(
            parent=types.SimpleNamespace()))
        testobj.check_options = mockqtw.MockButtonGroup()
        testobj.text_gt = mockqtw.MockLineEdit()
        testobj.radio_id = mockqtw.MockButtonGroup()
        testobj.text_lt = mockqtw.MockLineEdit()
        testobj.check_cats = mockqtw.MockButtonGroup()
        testobj.radio_id2 = mockqtw.MockButtonGroup()
        testobj.check_stats = mockqtw.MockButtonGroup()
        testobj.text_zoek = mockqtw.MockLineEdit()
        testobj.text_zoek2 = mockqtw.MockLineEdit()
        testobj.radio_arch = mockqtw.MockButtonGroup()
        checkbutton0 = mockqtw.MockCheckBox()
        checkbutton1 = mockqtw.MockCheckBox()
        checkbutton2 = mockqtw.MockCheckBox()
        checkbutton3 = mockqtw.MockCheckBox()
        checkbutton4 = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == (
                "called ButtonGroup.__init__ with args ()\n"
                "called LineEdit.__init__\ncalled ButtonGroup.__init__ with args ()\n"
                "called LineEdit.__init__\ncalled ButtonGroup.__init__ with args ()\n"
                "called ButtonGroup.__init__ with args ()\n"
                "called ButtonGroup.__init__ with args ()\ncalled LineEdit.__init__\n"
                "called LineEdit.__init__\ncalled ButtonGroup.__init__ with args ()\n"
                "called CheckBox.__init__\ncalled CheckBox.__init__\ncalled CheckBox.__init__\n"
                "called CheckBox.__init__\ncalled CheckBox.__init__\n")

        testobj.parent.parent.cats = {}
        testobj.parent.parent.stats = {}
        testobj.set_default_values({})
        assert capsys.readouterr().out == ""

        # TODO: ik moet nog een maniet vinden om aan te geven welke button van een buttongroupi
        # op checked gezet wordt
        testobj.set_default_values({'idgt': 'xx', 'id': '', 'idlt': 'yy', 'soort': '1',
                                    'status': '2', 'titel': '', 'arch': ''})
        assert capsys.readouterr().out == ("called LineEdit.setText with arg `xx`\n"
                                           "called ButtonGroup.buttons\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called ButtonGroup.buttons\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called LineEdit.setText with arg `yy`\n"
                                           "called ButtonGroup.buttons\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called ButtonGroup.buttons\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called LineEdit.setText with arg ``\n"
                                           "called ButtonGroup.buttons\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called ButtonGroup.buttons\n"
                                           "called CheckBox.setChecked with arg True\n")

        testobj.parent.parent.cats = {'0': ('x', '0')}
        testobj.parent.parent.stats = {'0': ('y', '0')}
        testobj.set_default_values({'idgt': 'xx', 'id': 'and', 'idlt': 'yy', 'soort': '1',
                                    'status': '2', 'titel': 'zz', 'arch': 'arch'})
        assert capsys.readouterr().out == ("called LineEdit.setText with arg `xx`\n"
                                           "called ButtonGroup.buttons\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called ButtonGroup.buttons\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called LineEdit.setText with arg `yy`\n"
                                           "called ButtonGroup.buttons\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called ButtonGroup.buttons\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called LineEdit.setText with arg `zz`\n"
                                           "called ButtonGroup.buttons\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called ButtonGroup.buttons\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called ButtonGroup.buttons\n"
                                           "called CheckBox.setChecked with arg True\n")

        counter = 0
        monkeypatch.setattr(mockqtw.MockLineEdit, 'setText', mock_set)
        testobj.parent.parent.cats = {'0': ('x', '0'), '2': ('a', '1')}
        testobj.parent.parent.stats = {'0': ('y', '0'), '1': ('b', '2')}
        testobj.set_default_values({'soort': '1', 'status': '2',
                                    'titel': (('about', 'aa'), ('title', 'bb'), ('of',)),
                                    'arch': 'alles'})
        assert capsys.readouterr().out == (
                "called ButtonGroup.buttons\n"
                "called CheckBox.setChecked with arg True\n"
                "called ButtonGroup.buttons\n"
                "called CheckBox.setChecked with arg True\n"
                "called ButtonGroup.buttons\n"
                "called CheckBox.setChecked with arg True\n"
                "called ButtonGroup.buttons\n"
                "called CheckBox.setChecked with arg True\n"
                "called LineEdit.setText with arg `(('about', 'aa'), ('title', 'bb'), ('of',))`\n"
                "called LineEdit.setText with arg `aa`\n"
                "called LineEdit.setText with arg `bb`\n"
                "called ButtonGroup.buttons\n"
                "called CheckBox.setChecked with arg True\n"
                "called ButtonGroup.buttons\n"
                "called CheckBox.setChecked with arg True\n"
                "called ButtonGroup.buttons\n"
                "called CheckBox.setChecked with arg True\n"
                "called ButtonGroup.buttons\n"
                "called CheckBox.setChecked with arg True\n")

        counter = 0
        testobj.set_default_values({'titel': (('about', 'aa'), ('title', 'bb'), ('',))})
        assert capsys.readouterr().out == (
                "called LineEdit.setText with arg `(('about', 'aa'), ('title', 'bb'), ('',))`\n"
                "called LineEdit.setText with arg `aa`\n"
                "called LineEdit.setText with arg `bb`\n"
                "called ButtonGroup.buttons\n"
                "called CheckBox.setChecked with arg True\n"
                "called ButtonGroup.buttons\n"
                "called CheckBox.setChecked with arg True\n")

    def test_on_text(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.on_text
        """
        def mock_buttons():
            print('called ButtonGroup.buttons')
            return button0, button1, button2, button3, button4
        def mock_set(self, value):
            print(f'called CheckBox.setChecked for {self} with arg {value}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.check_options = mockqtw.MockButtonGroup()
        testobj.check_options.buttons = mock_buttons
        button0 = mockqtw.MockCheckBox()
        button1 = mockqtw.MockCheckBox()
        button2 = mockqtw.MockCheckBox()
        button3 = mockqtw.MockCheckBox()
        button4 = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == ("called ButtonGroup.__init__ with args ()\n"
                                           "called CheckBox.__init__\ncalled CheckBox.__init__\n"
                                           "called CheckBox.__init__\ncalled CheckBox.__init__\n"
                                           "called CheckBox.__init__\n")
        monkeypatch.setattr(mockqtw.MockCheckBox, 'setChecked', mock_set)
        testobj.on_text('gt', '')
        assert capsys.readouterr().out == (
                "called ButtonGroup.buttons\n"
                f"called CheckBox.setChecked for {button0} with arg False\n")
        testobj.on_text('gt', 'xxx')
        assert capsys.readouterr().out == (
                "called ButtonGroup.buttons\n"
                f"called CheckBox.setChecked for {button0} with arg True\n")
        testobj.on_text('lt', '')
        assert capsys.readouterr().out == (
                "called ButtonGroup.buttons\n"
                f"called CheckBox.setChecked for {button0} with arg False\n")
        testobj.on_text('lt', 'xxx')
        assert capsys.readouterr().out == (
                "called ButtonGroup.buttons\n"
                f"called CheckBox.setChecked for {button0} with arg True\n")
        testobj.on_text('zoek', '')
        assert capsys.readouterr().out == (
                "called ButtonGroup.buttons\n"
                f"called CheckBox.setChecked for {button3} with arg False\n")
        testobj.on_text('zoek', 'xxx')
        assert capsys.readouterr().out == (
                "called ButtonGroup.buttons\n"
                f"called CheckBox.setChecked for {button3} with arg True\n")

    def test_on_checked(self, monkeypatch, capsys):
        """unittest for SelectOptionsDialog.on_checked
        """
        def mock_buttons():
            print('called ButtonGroup.buttons')
            return button0, button1, button2, button3, button4
        def mock_buttons_2():
            print('called ButtonGroup.buttons')
            return []
        def mock_buttons_3():
            print('called ButtonGroup.buttons')
            return check0, check1
        def mock_set(self, value):
            print(f'called CheckBox.setChecked for {self} with arg {value}')
            self.checked = value
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.check_options = mockqtw.MockButtonGroup()
        testobj.check_options.buttons = mock_buttons
        testobj.check_cats = mockqtw.MockButtonGroup()
        testobj.check_cats.buttons = mock_buttons_2
        testobj.check_stats = mockqtw.MockButtonGroup()
        testobj.check_stats.buttons = mock_buttons_2
        testobj.radio_arch = mockqtw.MockButtonGroup()
        testobj.radio_arch.buttons = mock_buttons_2
        button0 = mockqtw.MockCheckBox()
        button1 = mockqtw.MockCheckBox()
        button2 = mockqtw.MockCheckBox()
        button3 = mockqtw.MockCheckBox()
        button4 = mockqtw.MockCheckBox()
        check0 = mockqtw.MockCheckBox()
        check1 = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == ("called ButtonGroup.__init__ with args ()\n"
                                           "called ButtonGroup.__init__ with args ()\n"
                                           "called ButtonGroup.__init__ with args ()\n"
                                           "called ButtonGroup.__init__ with args ()\n"
                                           "called CheckBox.__init__\ncalled CheckBox.__init__\n"
                                           "called CheckBox.__init__\ncalled CheckBox.__init__\n"
                                           "called CheckBox.__init__\ncalled CheckBox.__init__\n"
                                           "called CheckBox.__init__\n")
        monkeypatch.setattr(mockqtw.MockCheckBox, 'setChecked', mock_set)
        testobj.on_checked('cat')
        assert capsys.readouterr().out == (
                "called ButtonGroup.buttons\n"
                "called ButtonGroup.buttons\n"
                f"called CheckBox.setChecked for {button1} with arg False\n")
        testobj.on_checked('stat')
        assert capsys.readouterr().out == (
                "called ButtonGroup.buttons\n"
                "called ButtonGroup.buttons\n"
                f"called CheckBox.setChecked for {button2} with arg False\n")
        testobj.on_checked('arch')
        assert capsys.readouterr().out == (
                "called ButtonGroup.buttons\n"
                "called ButtonGroup.buttons\n"
                f"called CheckBox.setChecked for {button4} with arg False\n")

        testobj.check_cats.buttons = mock_buttons_2
        testobj.check_stats.buttons = mock_buttons_2
        testobj.radio_arch.buttons = mock_buttons_2
        testobj.on_checked('cat')
        assert capsys.readouterr().out == (
                "called ButtonGroup.buttons\n"
                "called ButtonGroup.buttons\n"
                f"called CheckBox.setChecked for {button1} with arg False\n")
        testobj.on_checked('stat')
        assert capsys.readouterr().out == (
                "called ButtonGroup.buttons\n"
                "called ButtonGroup.buttons\n"
                f"called CheckBox.setChecked for {button2} with arg False\n")
        testobj.on_checked('arch')
        assert capsys.readouterr().out == (
                "called ButtonGroup.buttons\n"
                "called ButtonGroup.buttons\n"
                f"called CheckBox.setChecked for {button4} with arg False\n")

        testobj.check_cats.buttons = mock_buttons_3
        testobj.check_stats.buttons = mock_buttons_3
        testobj.radio_arch.buttons = mock_buttons_3
        testobj.on_checked('cat')
        assert capsys.readouterr().out == (
                "called ButtonGroup.buttons\n"
                "called ButtonGroup.buttons\n"
                "called CheckBox.isChecked\n"
                "called CheckBox.isChecked\n"
                f"called CheckBox.setChecked for {button1} with arg False\n")
        testobj.on_checked('stat')
        assert capsys.readouterr().out == (
                "called ButtonGroup.buttons\n"
                "called ButtonGroup.buttons\n"
                "called CheckBox.isChecked\n"
                "called CheckBox.isChecked\n"
                f"called CheckBox.setChecked for {button2} with arg False\n")
        testobj.on_checked('arch')
        assert capsys.readouterr().out == (
                "called ButtonGroup.buttons\n"
                "called ButtonGroup.buttons\n"
                "called CheckBox.isChecked\n"
                "called CheckBox.isChecked\n"
                f"called CheckBox.setChecked for {button4} with arg False\n")

        check1.setChecked(True)
        assert capsys.readouterr().out == (
                f"called CheckBox.setChecked for {check1} with arg True\n")
        testobj.on_checked('cat')
        assert capsys.readouterr().out == (
                "called ButtonGroup.buttons\n"
                "called ButtonGroup.buttons\n"
                "called CheckBox.isChecked\n"
                "called CheckBox.isChecked\n"
                f"called CheckBox.setChecked for {button1} with arg True\n")
        testobj.on_checked('stat')
        assert capsys.readouterr().out == (
                "called ButtonGroup.buttons\n"
                "called ButtonGroup.buttons\n"
                "called CheckBox.isChecked\n"
                "called CheckBox.isChecked\n"
                f"called CheckBox.setChecked for {button2} with arg True\n")
        testobj.on_checked('arch')
        assert capsys.readouterr().out == (
                "called ButtonGroup.buttons\n"
                "called ButtonGroup.buttons\n"
                "called CheckBox.isChecked\n"
                "called CheckBox.isChecked\n"
                f"called CheckBox.setChecked for {button4} with arg True\n")

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
        monkeypatch.setattr(testee.SettOptionsDialog, '__init__', mock_init)
        testobj = testee.SettOptionsDialog()
        assert capsys.readouterr().out == 'called SettOptionsDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for SettOptionsDialog.__init__
        """
        def mock_initstuff(self, parent):
            print(f'called Options.initstuff with args {self} {parent}')
            self.data = ['xxx', 'yyy']
            self.editable = False
        def mock_initstuff2(self, parent):
            print(f'called Options.initstuff with args {self} {parent}')
            self.data = ['xxx', 'yyy']
            self.editable = True
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'resize', mockqtw.MockDialog.resize)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QListWidget', mockqtw.MockListBox)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        monkeypatch.setattr(testee.shared, 'app_title', 'xxxx')
        parent = types.SimpleNamespace()
        args = []
        with pytest.raises(ValueError) as exc:
            testobj = testee.SettOptionsDialog(parent, args)
        assert str(exc.value) == "Option type not provided"
        args = ['title']
        with pytest.raises(ValueError) as exc:
            testobj = testee.SettOptionsDialog(parent, args)
        assert str(exc.value) == "Option type not provided"
        clsobj = types.SimpleNamespace(initstuff=mock_initstuff)
        args = [clsobj, 'a title']
        testobj = testee.SettOptionsDialog(parent, args)
        assert testobj.cls == clsobj
        assert isinstance(testobj.elb, testee.qtw.QListWidget)
        assert isinstance(testobj.b_edit, testee.qtw.QPushButton)
        assert not testobj.editable
        assert testobj.titel == ''
        assert testobj.data == ['xxx', 'yyy']
        assert testobj.tekst == ['', '']
        assert capsys.readouterr().out == expected_output['settoptions'].format(testobj=testobj,
                                                                                title='a title',
                                                                                x=350, y=200)
        clsobj = types.SimpleNamespace(initstuff=mock_initstuff2)
        args = [clsobj, 'title', (10, 20)]
        testobj = testee.SettOptionsDialog(parent, args)
        assert testobj.cls == clsobj
        assert isinstance(testobj.elb, testee.qtw.QListWidget)
        assert isinstance(testobj.b_edit, testee.qtw.QPushButton)
        assert testobj.editable
        assert testobj.titel == ''
        assert testobj.data == ['xxx', 'yyy']
        assert testobj.tekst == ['', '']
        assert capsys.readouterr().out == expected_output['settoptions2'].format(testobj=testobj,
                                                                                 title='title',
                                                                                 x=10, y=20)

    def test_keyReleaseEvent(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.keyReleaseEvent
        """
        def mock_edit():
            print('called SettOptionsDialog.edit_item')
        def mock_release(*args):
            print('called Dialog.keyReleaseEvent with args', args)
        monkeypatch.setattr(testee.qtw.QDialog, 'keyReleaseEvent', mock_release)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.edit_item = mock_edit
        evt = types.SimpleNamespace(key=lambda: testee.core.Qt.Key.Key_F2)
        testobj.keyReleaseEvent(evt)
        assert capsys.readouterr().out == "called SettOptionsDialog.edit_item\n"
        evt = types.SimpleNamespace(key=lambda: 'anything else')
        testobj.keyReleaseEvent(evt)
        assert capsys.readouterr().out == (
                f"called Dialog.keyReleaseEvent with args ({testobj}, {evt})\n")

    def test_edit_item(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.edit_item
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
        """unittest for SettOptionsDialog.end_edit
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.elb = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj.end_edit('item_n', 'item_o')
        assert capsys.readouterr().out == "called List.closePersistentEditor with arg item_o\n"

    def test_add_item(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.add_item
        """
        # def mock_init(self, *args):
        #     print('called ListItem.__init__')
        #     return item
        # monkeypatch.setattr(testee.qtw.QListWidgetItem, '__init__', mock_init)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.elb = mockqtw.MockListBox()
        assert testobj.elb.list == []
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj.add_item()
        assert len(testobj.elb.list) == 1
        added_item = testobj.elb.list[0]
        assert capsys.readouterr().out == (
                f"called List.addItem with arg `{added_item}`\n"
                "called List.setCurrentItem\n"
                f"called List.openPersistentEditor with arg {added_item}\n"
                f"called editItem with arg {added_item}\n")

    def test_remove_item(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.remove_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.elb = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj.remove_item()
        assert capsys.readouterr().out == ("called List.currentRow\n"
                                           "called List.takeItem with arg `current row`\n")

    def test_move_item_up(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.move_item_up
        """
        def mock_move(up):
            print(f'called SettOptionsDialog.move_item with arg {up}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.move_item = mock_move
        testobj.move_item_up()
        assert capsys.readouterr().out == ("called SettOptionsDialog.move_item with arg True\n")

    def test_move_item_down(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.move_item_down
        """
        def mock_move(up):
            print(f'called SettOptionsDialog.move_item with arg {up}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.move_item = mock_move
        testobj.move_item_down()
        assert capsys.readouterr().out == ("called SettOptionsDialog.move_item with arg False\n")

    def test_move_item(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.move_item
        """
        def mock_current():
            print('called List.currentItem')
            return current
        def mock_row():
            print('called List.currentRow')
            return 0
        def mock_row2():
            print('called List.currentRow')
            return 1
        def mock_count():
            print('called List.count')
            return 2
        def mock_item(arg):
            print(f'called List.item with arg {arg}')
            return other
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.elb = mockqtw.MockListBox()
        current = mockqtw.MockListItem('from')
        other = mockqtw.MockListItem('to')
        testobj.elb.currentItem = mock_current
        testobj.elb.currentRow = mock_row
        testobj.elb.count = mock_count
        testobj.elb.item = mock_item
        assert capsys.readouterr().out == ("called List.__init__\n"
                                           "called ListItem.__init__ with args ('from',)\n"
                                           "called ListItem.__init__ with args ('to',)\n")
        testobj.move_item()
        assert capsys.readouterr().out == ("called List.currentItem\n"
                                           "called List.currentRow\n")
        testobj.move_item(up=False)
        assert capsys.readouterr().out == ("called List.currentItem\n"
                                           "called List.currentRow\n"
                                           "called List.currentRow\n"
                                           "called List.count\n"
                                           "called List.item with arg 1\n"
                                           "called ListItem.setText with arg 'from'\n"
                                           "called ListItem.setText with arg 'to'\n"
                                           "called List.setCurrentItem\n")
        testobj.elb.currentRow = mock_row2
        testobj.move_item()
        assert capsys.readouterr().out == ("called List.currentItem\n"
                                           "called List.currentRow\n"
                                           "called List.item with arg 0\n"
                                           "called ListItem.setText with arg 'to'\n"
                                           "called ListItem.setText with arg 'from'\n"
                                           "called List.setCurrentItem\n")
        testobj.move_item(up=False)
        assert capsys.readouterr().out == ("called List.currentItem\n"
                                           "called List.currentRow\n"
                                           "called List.currentRow\n"
                                           "called List.count\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for SettOptionsDialog.accept
        """
        def mock_leesuit(*args):
            print('called Obj.leesuit with args', args)
        def mock_count():
            print('called List.count')
            return 2
        def mock_item(arg):
            print(f'called List.item with arg {arg}')
            return anyitem
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.elb = mockqtw.MockListBox()
        testobj.elb.count = mock_count
        testobj.elb.item = mock_item
        anyitem = mockqtw.MockListItem('text')
        assert capsys.readouterr().out == ("called List.__init__\n"
                                           "called ListItem.__init__ with args ('text',)\n")
        testobj.cls = types.SimpleNamespace(leesuit=mock_leesuit)
        testobj.accept()
        assert capsys.readouterr().out == (
                "called List.currentItem\n"
                "called List.closePersistentEditor with arg current item\n"
                "called List.count\n"
                "called List.item with arg 0\n"
                "called List.item with arg 1\n"
                f"called Obj.leesuit with args ({testobj}, {testobj.parent}, ['text', 'text'])\n"
                "called Dialog.accept\n")


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
        monkeypatch.setattr(testee.LoginBox, '__init__', mock_init)
        testobj = testee.LoginBox()
        assert capsys.readouterr().out == 'called LoginBox.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for LoginBox.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        parent = MockGui()
        testobj = testee.LoginBox(parent)
        assert testobj.parent == parent
        assert testobj.parent.dialog_data == ()
        assert isinstance(testobj.t_username, testee.qtw.QLineEdit)
        assert isinstance(testobj.t_password, testee.qtw.QLineEdit)
        assert capsys.readouterr().out == expected_output['loginbox'].format(testobj=testobj)

    def test_accept(self, monkeypatch, capsys):
        """unittest for LoginBox.accept
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(master=types.SimpleNamespace(filename='xxx'))
        testobj.t_username = mockqtw.MockLineEdit()
        testobj.t_password = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\ncalled LineEdit.__init__\n"
        testobj.accept()
        assert testobj.parent.dialog_data == ('', '', 'xxx')
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called Dialog.accept\n")


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
            return [('top menu', [('xx', callback1, [], ''),
                                  ('yy', callback2, ['Ctrl+O'], 'yadayada'),
                                  ('',),
                                  ('sub menu', [('zz', callback3, ['x', 'y'], 'bladibla'),
                                                (),
                                                ('&Data', [])])])]
        def callback1():
            return 1
        def callback2():
            return 2
        def callback3():
            return 3
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.menuBar = mock_menubar
        testobj.master = types.SimpleNamespace(get_menu_data=mock_menudata)
        testobj.create_menu()
        assert capsys.readouterr().out == expected_output['mainmenu']
        testobj.master = types.SimpleNamespace(get_menu_data=mock_menudata_2)
        testobj.create_menu()
        assert capsys.readouterr().out == expected_output['mainmenu2'].format(
                callbacks=[callback1, callback2, callback3])

    def test_create_actions(self, monkeypatch, capsys):
        """unittest for MainGui.create_actions
        """
        monkeypatch.setattr(testee.gui, 'QShortcut', mockqtw.MockShortcut)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(print_something=lambda: 'x',
                                               goto_prev=lambda: 'y',
                                               goto_next=lambda: 'z')
        testobj.create_actions()
        assert capsys.readouterr().out == (
                "called Shortcut.__init__ with args"
                f" ('Ctrl+P', {testobj}, {testobj.master.print_something})\n"
                "called Shortcut.__init__ with args"
                f" ('Alt+Left', {testobj}, {testobj.master.goto_prev})\n"
                "called Shortcut.__init__ with args"
                f" ('Alt+Right', {testobj}, {testobj.master.goto_next})\n")

    def test_get_bookwidget(self, monkeypatch, capsys):
        """unittest for MainGui.get_bookwidget
        """
        monkeypatch.setattr(testee.qtw, 'QTabWidget', mockqtw.MockTabWidget)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = 'panel'
        result = testobj.get_bookwidget()
        assert isinstance(result, testee.qtw.QTabWidget)
        assert result.sorter is None
        assert result.textcallbacks == {}
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
        testobj.master = types.SimpleNamespace(exit_app=lambda: 'exit')
        testobj.pnl = mockqtw.MockFrame()
        testobj.bookwidget = mockqtw.MockTabWidget()
        testobj.app = mockqtw.MockApplication()
        assert capsys.readouterr().out == ("called Frame.__init__\ncalled TabWidget.__init__\n"
                                           "called Application.__init__\n")
        testobj.show = mock_show
        with pytest.raises(SystemExit):
            testobj.go()
        assert capsys.readouterr().out == expected_output['maingo'].format(testobj=testobj)

    def test_refresh_page(self, monkeypatch, capsys):
        """unittest for MainGui.refresh_page
        """
        def mock_change(arg):
            print(f'called mainGui.on_page_changing with arg {arg}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.on_page_changing = mock_change
        testobj.refresh_page()
        assert capsys.readouterr().out == "called mainGui.on_page_changing with arg 0\n"

    def test_on_page_changing(self, monkeypatch, capsys):
        """unittest for MainGui.on_page_changing
        """
        def mock_get():
            print('called Page.get_list_row')
            return 'item'
        def mock_set(item):
            print(f'called Page.set_list_row with arg {item}')
        def mock_get_page():
            print('called MainGui.get_page')
            return 0
        def mock_get_page_2():
            print('called MainGui.get_page')
            return 2
        def mock_get_page_3():
            print('called MainGui.get_page')
            return 6
        def mock_enable(value):
            print(f'called MainGui.enable_all_other_tabs with arg {value}')
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
        testobj.get_page = mock_get_page
        testobj.enable_all_other_tabs = mock_enable
        testobj.set_tabfocus = mock_set_tabfocus
        testobj.LIN = True
        testobj.master.book.current_tab = -1
        testobj.on_page_changing('newtabnum')
        assert capsys.readouterr().out == ("called MainGui.get_page\n")

        testobj.master.book.current_tab = 1
        testobj.on_page_changing('newtabnum')
        assert capsys.readouterr().out == ("called MainGui.get_page\n"
                                           "called MainGui.enable_all_other_tabs with arg True\n"
                                           "called Page.vulp\n"
                                           "called MainGui.set_tabfocus with arg 0\n")

        testobj.master.book.current_tab = 0
        testobj.on_page_changing('newtabnum')
        assert capsys.readouterr().out == ("called MainGui.get_page\n"
                                           "called MainGui.enable_all_other_tabs with arg True\n"
                                           "called Page.get_list_row\n"
                                           "called Page.vulp\n"
                                           "called Page.set_list_row with arg item\n"
                                           "called MainGui.set_tabfocus with arg 0\n")

        testobj.get_page = mock_get_page_2
        testobj.master.book.current_tab = 1
        testobj.on_page_changing('newtabnum')
        assert capsys.readouterr().out == ("called MainGui.get_page\n"
                                           "called MainGui.enable_all_other_tabs with arg True\n"
                                           "called Page.vulp\n"
                                           "called MainGui.set_tabfocus with arg 2\n")

        testobj.get_page = mock_get_page_3
        testobj.master.book.current_tab = 0
        testobj.on_page_changing('newtabnum')
        assert capsys.readouterr().out == ("called MainGui.get_page\n"
                                           "called MainGui.enable_all_other_tabs with arg True\n"
                                           "called Page.vulp\n"
                                           "called MainGui.set_tabfocus with arg 6\n")

        testobj.master.book.current_tab = 6
        testobj.on_page_changing('newtabnum')
        assert capsys.readouterr().out == ("called MainGui.get_page\n"
                                           "called MainGui.enable_all_other_tabs with arg True\n"
                                           "called Page.get_list_row\n"
                                           "called Page.vulp\n"
                                           "called Page.set_list_row with arg item\n"
                                           "called MainGui.set_tabfocus with arg 6\n")

    def test_enable_book_tabs(self, monkeypatch, capsys):
        """unittest for MainGui.enable_book_tabs
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(book=types.SimpleNamespace(count=lambda: 6))
        testobj.bookwidget = mockqtw.MockTabWidget()
        assert capsys.readouterr().out == "called TabWidget.__init__\n"
        testobj.enable_book_tabs('state')
        assert capsys.readouterr().out == (
                "called TabWidget.setTabEnabled with args (0, 'state')\n"
                "called TabWidget.setTabEnabled with args (1, 'state')\n"
                "called TabWidget.setTabEnabled with args (2, 'state')\n"
                "called TabWidget.setTabEnabled with args (3, 'state')\n"
                "called TabWidget.setTabEnabled with args (4, 'state')\n"
                "called TabWidget.setTabEnabled with args (5, 'state')\n")
        testobj.enable_book_tabs('state', tabfrom=1, tabto=4)
        assert capsys.readouterr().out == (
                "called TabWidget.setTabEnabled with args (1, 'state')\n"
                "called TabWidget.setTabEnabled with args (2, 'state')\n"
                "called TabWidget.setTabEnabled with args (3, 'state')\n")

    def test_enable_all_other_tabs(self, monkeypatch, capsys):
        """unittest for MainGui.enable_all_other_tabs
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.bookwidget = mockqtw.MockTabWidget()
        assert capsys.readouterr().out == "called TabWidget.__init__\n"
        testobj.master = types.SimpleNamespace(book=types.SimpleNamespace(count=lambda: 6,
                                                                          current_tab=4))
        testobj.enable_all_other_tabs('state')
        assert capsys.readouterr().out == (
                "called TabWidget.setTabEnabled with args (0, 'state')\n"
                "called TabWidget.setTabEnabled with args (1, 'state')\n"
                "called TabWidget.setTabEnabled with args (2, 'state')\n"
                "called TabWidget.setTabEnabled with args (3, 'state')\n"
                "called TabWidget.setTabEnabled with args (5, 'state')\n")

    def test_add_book_tab(self, monkeypatch, capsys):
        """unittest for MainGui.add_book_tab
        """
        def mock_doe():
            print('called PageGui.doelayout')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.bookwidget = mockqtw.MockTabWidget()
        tab = types.SimpleNamespace(gui=types.SimpleNamespace(doelayout=mock_doe))
        assert capsys.readouterr().out == "called TabWidget.__init__\n"
        testobj.add_book_tab(tab, 'title')
        assert capsys.readouterr().out == (
                f"called TabWidget.addTab with args `{tab.gui}` `title`\n"
                "called PageGui.doelayout\n")

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
        testobj.bookwidget = mockqtw.MockTabWidget()
        assert capsys.readouterr().out == "called TabWidget.__init__\n"
        testobj.set_page('num')
        assert capsys.readouterr().out == "called TabWidget.setCurrentIndex with arg `num`\n"

    def test_set_page_title(self, monkeypatch, capsys):
        """unittest for MainGui.set_page_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.bookwidget = mockqtw.MockTabWidget()
        assert capsys.readouterr().out == "called TabWidget.__init__\n"
        testobj.set_page_title('num', 'text')
        assert capsys.readouterr().out == "called TabWidget.setTabText with args ('num', 'text')\n"

    def test_get_page(self, monkeypatch, capsys):
        """unittest for MainGui.get_page
        """
        def mock_index():
            print('called Book.currentIndex')
            return 1
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.bookwidget = mockqtw.MockTabWidget()
        testobj.bookwidget.currentIndex = mock_index
        assert capsys.readouterr().out == "called TabWidget.__init__\n"
        assert testobj.get_page() == 1
        assert capsys.readouterr().out == "called Book.currentIndex\n"

    def test_set_tabfocus(self, monkeypatch, capsys):
        """unittest for MainGui.set_tabfocus
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        Page0 = types.SimpleNamespace(gui=types.SimpleNamespace(p0list=mockqtw.MockListBox()))
        Page1 = types.SimpleNamespace(gui=types.SimpleNamespace(proc_entry=mockqtw.MockLineEdit()))
        Page2 = types.SimpleNamespace(gui=types.SimpleNamespace(text1=mockqtw.MockEditorWidget()))
        Page3 = types.SimpleNamespace(gui=types.SimpleNamespace(text1=mockqtw.MockEditorWidget()))
        Page4 = types.SimpleNamespace(gui=types.SimpleNamespace(text1=mockqtw.MockEditorWidget()))
        Page5 = types.SimpleNamespace(gui=types.SimpleNamespace(text1=mockqtw.MockEditorWidget()))
        Page6 = types.SimpleNamespace(gui=types.SimpleNamespace(progress_list=mockqtw.MockListBox()))
        assert capsys.readouterr().out == ("called List.__init__\ncalled LineEdit.__init__\n"
                                           "called Editor.__init__\ncalled Editor.__init__\n"
                                           "called Editor.__init__\ncalled Editor.__init__\n"
                                           "called List.__init__\n")
        testobj.master = types.SimpleNamespace(book=types.SimpleNamespace())
        testobj.master.use_text_panels = True
        testobj.master.book.pages = [Page0, Page1, Page2, Page3, Page4, Page5, Page6]
        testobj.set_tabfocus(5)
        assert capsys.readouterr().out == ("called Editor.setFocus\n")
        testobj.master.use_text_panels = False
        testobj.master.book.pages = [Page0, Page1, Page6]
        testobj.set_tabfocus(1)
        assert capsys.readouterr().out == ("called LineEdit.setFocus\n")

    def test_go_next(self, monkeypatch, capsys):
        """unittest for MainGui.go_next
        """
        def mock_goto():
            print('called Main.goto_next')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(goto_next=mock_goto)
        testobj.go_next()
        assert capsys.readouterr().out == ("called Main.goto_next\n")

    def test_go_prev(self, monkeypatch, capsys):
        """unittest for MainGui.go_prev
        """
        def mock_goto():
            print('called Main.goto_prev')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(goto_prev=mock_goto)
        testobj.go_prev()
        assert capsys.readouterr().out == ("called Main.goto_prev\n")

    def test_go_to(self, monkeypatch, capsys):
        """unittest for MainGui.go_to
        """
        def mock_goto(page):
            print(f'called Main.goto_page with arg {page}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(goto_page=mock_goto)
        testobj.go_to('page')
        assert capsys.readouterr().out == ("called Main.goto_page with arg page\n")

    def test_print_(self, monkeypatch, capsys):
        """unittest for MainGui.print_
        """
        def mock_get_choice(*args):
            print('called get_choice_item with args', args)
            return args[2][0]
        def mock_get_choice_2(*args):
            print('called get_choice_item with args', args)
            return args[2][1]
        def mock_scherm():
            print('called Main.print_scherm')
        def mock_actie():
            print('called Main.print_actie')
        monkeypatch.setattr(testee, 'get_choice_item', mock_get_choice)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(print_scherm=mock_scherm, print_actie=mock_actie)
        testobj.print_()
        assert capsys.readouterr().out == (
                "called get_choice_item with args"
                f" ({testobj}, 'Wat wil je afdrukken?', ['huidig scherm', 'huidige actie'])\n"
                "called Main.print_scherm\n")
        monkeypatch.setattr(testee, 'get_choice_item', mock_get_choice_2)
        testobj.print_()
        assert capsys.readouterr().out == (
                "called get_choice_item with args"
                f" ({testobj}, 'Wat wil je afdrukken?', ['huidig scherm', 'huidige actie'])\n"
                "called Main.print_actie\n")

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

    def test_set_tab_titles(self, monkeypatch, capsys):
        """unittest for MainGui.set_tab_titles
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.bookwidget = mockqtw.MockTabWidget()
        assert capsys.readouterr().out == "called TabWidget.__init__\n"
        testobj.set_tab_titles({'tab1': 'text1', 'tab2': 'text2'})
        assert capsys.readouterr().out == (
                "called TabWidget.setTabText with args ('tab1', 'text1')\n"
                "called TabWidget.setTabText with args ('tab2', 'text2')\n")

    def test_select_first_tab(self, monkeypatch, capsys):
        """unittest for MainGui.select_first_tab
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.bookwidget = mockqtw.MockTabWidget()
        assert capsys.readouterr().out == "called TabWidget.__init__\n"
        testobj.select_first_tab()
        assert capsys.readouterr().out == "called TabWidget.setCurrentIndex with arg `0`\n"
