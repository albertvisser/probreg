"""Actie (was: problemen) Registratie, PyQt versie
"""
import os
import sys
import pathlib
import contextlib
import functools
import PyQt6.QtWidgets as qtw
import PyQt6.QtPrintSupport as qtp
import PyQt6.QtGui as gui
import PyQt6.QtCore as core
from mako.template import Template
from probreg import shared
LIN = os.name == 'posix'
HERE = os.path.dirname(__file__)
xmlfilter = "XML files (*.xml);;all files (*.*)"


def show_message(win, message, title=''):
    "present a message and wait for the user to confirm (having read it or whatever)"
    if not title:
        title = shared.app_title
    qtw.QMessageBox.information(win, title, message)


def show_error(win, message, title=''):
    "present a message and wait for the user to confirm (having read it or whatever)"
    if not title:
        title = shared.app_title
    qtw.QMessageBox.critical(win, title, message)


def get_open_filename(win, start=None):
    "get the name of a file to open"
    start = start or pathlib.Path.cwd()
    fname = qtw.QFileDialog.getOpenFileName(win, shared.app_title + " - kies een gegevensbestand",
                                            str(start), xmlfilter)[0]
    return fname


def get_save_filename(win, start=None):
    "get the name of a file to save"
    start = start or pathlib.Path.cwd()
    fname = qtw.QFileDialog.getSaveFileName(win, shared.app_title + " - nieuw gegevensbestand",
                                            str(start), xmlfilter)[0]
    return fname


def get_choice_item(win, caption, choices, current=0):
    "allow the user to choose one of a set of options and return it"
    choice, ok = qtw.QInputDialog.getItem(win, shared.app_title, caption, choices,
                                          current=current, editable=False)
    if ok:
        return choice
    return ''


def ask_question(win, message):
    "ask the user a question with an option to cancel the process"
    retval = qtw.QMessageBox.question(win, shared.app_title, message,
                                      qtw.QMessageBox.StandardButton.Yes
                                      | qtw.QMessageBox.StandardButton.No)
    return retval == qtw.QMessageBox.StandardButton.Yes


def ask_cancel_question(win, message):
    "ask the user a question with an option to cancel the process"
    retval = qtw.QMessageBox.question(win, shared.app_title, message,
                                      qtw.QMessageBox.StandardButton.Yes
                                      | qtw.QMessageBox.StandardButton.No
                                      | qtw.QMessageBox.StandardButton.Cancel)
    return (retval == qtw.QMessageBox.StandardButton.Yes,
            retval == qtw.QMessageBox.StandardButton.Cancel)


def show_dialog(dlg):
    "show a dialog and return if the dialog was confirmed / accepted"
    # ok = False
    ok = dlg.exec()
    return ok == qtw.QDialog.DialogCode.Accepted


class MainGui(qtw.QMainWindow):
    """Hoofdscherm met menu, statusbalk, notebook en een "quit" button"""
    def __init__(self, master):
        self.master = master
        self.app = qtw.QApplication(sys.argv)
        super().__init__()
        self.setWindowTitle(self.master.title)
        self.setWindowIcon(gui.QIcon(os.path.join(HERE, 'icons', 'task.png')))
        if LIN:
            wide, high, left, top = 864, 720, 2, 2
        else:
            wide, high, left, top = 588, 594, 20, 32
        self.move(left, top)
        self.resize(wide, high)
        self.sbar = self.statusBar()
        self.statusmessage = qtw.QLabel(self)
        self.sbar.addWidget(self.statusmessage, stretch=2)
        self.showuser = qtw.QLabel(self)
        self.sbar.addPermanentWidget(self.showuser, stretch=1)
        self.pnl = qtw.QFrame(self)
        self.setCentralWidget(self.pnl)
        self.toolbar = None

    def create_menu(self):
        """Create application menu
        """
        def add_to_menu(menu, menuitem):
            "parse line and create menu item"
            action = None
            if len(menuitem) == 1:
                menu.addSeparator()
            elif len(menuitem) == len(['caption', 'callback', 'key', 'tip']):
                caption, callback, key, tip = menuitem
                action = menu.addAction(caption)
                action.triggered.connect(callback)
                if key:
                    action.setShortcut(key)
                if tip:
                    action.setToolTip(tip)
            elif len(menuitem) == len(['title', 'items']):
                title, items = menuitem
                sub = menu.addMenu(title)
                if title == '&Data':
                    self.settingsmenu = sub
                for subitem in items:
                    add_to_menu(sub, subitem)
            return action

        menu_bar = self.menuBar()
        # self.master.tabmenus = []
        for title, items in self.master.get_menu_data():
            menu = menu_bar.addMenu(title)
            for menuitem in items:
                action = add_to_menu(menu, menuitem)
                # if title == '&View':
                #     self.master.tabmenus.append(action)

    def create_actions(self, actiondefs):
        """Create additional application actions
        """
        for text, callback in actiondefs:
            gui.QShortcut(text, self, callback)
        # gui.QShortcut('Ctrl+P', self, self.master.print_something)
        # gui.QShortcut('Alt+Left', self, self.master.goto_prev)
        # gui.QShortcut('Alt+Right', self, self.master.goto_next)

    def get_bookwidget(self):
        "build the tabbed widget"
        bookwidget = qtw.QTabWidget(self.pnl)
        bookwidget.resize(300, 300)
        bookwidget.sorter = None
        # bookwidget.textcallbacks = {}   -- not used
        bookwidget.currentChanged.connect(self.on_page_changing)
        return bookwidget

    def go(self):
        """realize the screen layout and start application
        """
        sizer0 = qtw.QVBoxLayout()
        sizer0.addWidget(self.master.book)
        sizer1 = qtw.QHBoxLayout()
        sizer1.addStretch()
        button = qtw.QPushButton('&Quit', self.pnl)
        button.clicked.connect(self.master.exit_app)
        sizer1.addWidget(button)
        sizer1.addStretch()
        sizer0.addLayout(sizer1)
        self.pnl.setLayout(sizer0)
        self.show()
        sys.exit(self.app.exec())

    def refresh_page(self):
        """reload page while staying on it
        this method is called after a user has signed in
        """
        self.on_page_changing(newtabnum=0)

    def on_page_changing(self, newtabnum=None):
        """deze methode was in de wx versie bedoeld om wanneer er van pagina gewisseld gaat worden
        te controleren of dat wel mogelijk is en zo niet, te melden waarom en de
        paginawissel tegen te houden (ok, terug te gaan naar de vorige pagina).

        PyQt kent geen aparte beforechanging methode zoals wx, daarom is wordt die controle (leavep)
        niet meer in deze methode gedaan maar in nieuwp, goto_next/prev/page en exit_app
        wel wordt hier ervoor gezorgd dat na het wisselen van pagina
        het veld / de velden van de nieuwe pagina een waarde krijgen met behulp van de vulp methode

        een probleem hiermee is wel dat je met klikken op een tab deze controle overslaat
        je komt direct op de nieuwe tab en teruggaan vind ik geen fraaie optie

        newtabnum wordt door de event meegegeven maar niet door refresh_page
        """
        old = self.master.book.current_tab
        new = self.get_page(self.master.book) if newtabnum is None else newtabnum
        self.master.book.current_tab = new
        if LIN and old == -1:  # bij initialisatie en bij afsluiten
            return
        self.master.enable_all_other_tabs(True)
        page = self.master.book.pages[new]
        firsttab = 0
        lasttab = len(self.master.book.pages) - 1
        if firsttab < new < lasttab:
            page.vulp()
        else:  # if new in (firsttab, lasttab): enig andere mogelijkheid
            listbox = page.p0list if new == firsttab else page.progress_list
            if new == old:
                item = page.gui.get_list_row(listbox)        # remember current item
            self.master.book.pages[new].vulp()
            if new == old:
                page.gui.set_list_row(listbox, item)         # reselect item
        self.set_tabfocus(self.master.book.current_tab)

    # def enable_navigation_via_menu(self, tabno, state):
    #     "make specified tabs (in)accessible"
    #     self.master.tabmenus[tabno].setEnabled(state)

    def add_book_tab(self, bookwidget, tab, title):
        "add a new tab to the widget"
        bookwidget.addTab(tab.gui, title)

    def enable_tab(self, bookwidget, tabno, state):
        "make a tab accessible or not"
        bookwidget.setTabEnabled(tabno, state)

    def get_tab_count(self, bookwidget):
        "return the number of pages"
        return bookwidget.count()

    def exit(self):
        "Menukeuze: exit applicatie"
        self.close()    # enough for now

    def close(self):
        "redefined"
        self.master.save_startitem_on_exit()
        super().close()

    def set_page(self, bookwidget, num):
        "set the selected page to this index"
        bookwidget.setCurrentIndex(num)

    def set_page_title(self, bookwidget, num, text):
        "change the tab title"
        bookwidget.setTabText(num, text)

    def get_page(self, bookwidget):
        "return index for the selected page"
        return bookwidget.currentIndex()

    def set_tabfocus(self, tabno):
        "focus geven aan de gekozen tab"
        self.master.get_focus_widget_for_tab(tabno).setFocus()

    # verplaatst naar master
    # def print_(self):
    #     """callback voor ctrl-P(rint)

    #     vraag om printen scherm of actie, bv. met een InputDialog
    #     """
    #     choices = ['huidig scherm', 'huidige actie']
    #     choice = get_choice_item(self, 'Wat wil je afdrukken?', choices)
    #     if choice == choices[0]:
    #         self.master.print_scherm()
    #     else:  # if choice == choices[1]: enige andere mogelijkheid
    #         self.master.print_actie()

    def preview(self):
        "callback voor print preview"
        self.print_dlg = qtp.QPrintPreviewDialog(self)
        self.print_dlg.paintRequested.connect(self.afdrukken)
        self.print_dlg.exec()

    def afdrukken(self, printer):
        "wordt aangeroepen door de menuprint methodes"
        # self.css = ""
        # if self.css:
        #     self.master.printdict['css'] = self.css
        self.master.printdict['hdr'] = self.master.hdr
        doc = gui.QTextDocument(self)
        html = Template(filename=os.path.join(HERE, 'actie.tpl')).render(**self.master.printdict)
        doc.setHtml(html)
        printer.setOutputFileName(self.master.hdr)
        doc.print(printer)
        self.print_dlg.done(True)

    def enable_settingsmenu(self):
        "instellen of gebruik van settingsmenu mogelijk is"
        self.settingsmenu.setEnabled(self.master.is_admin)

    def set_statusmessage(self, msg=''):
        """stel tekst in statusbar in
        """
        self.statusmessage.setText(msg)

    def set_window_title(self, text):
        "build title for window"
        self.setWindowTitle(text)

    def show_username(self, msg):
        "show if/which user is logged in"
        self.showuser.setText(msg)


class PageGui(qtw.QFrame):
    "base class for notebook page"
    def __init__(self, parent, master):
        self.book = parent
        self.master = master
        self.appbase = self.book.parent
        super().__init__(parent)

    def start_display(self):
        "begin building the screen"
        sizer = qtw.QVBoxLayout()
        self.setLayout(sizer)
        return sizer

    def create_text_field(self, sizer, width, height, callback):
        """build rich text area with style changing properties
        """
        hbox = qtw.QHBoxLayout()
        textfield = EditorPanel(self)
        textfield.resize(width, height)
        textfield.textChanged.connect(callback)
        hbox.addWidget(textfield)
        sizer.addLayout(hbox)
        return textfield

    def create_toolbar(self, sizer, textfield, toolbardata):
        """build toolbar wih buttons for changing text style
        """
        hbox = qtw.QHBoxLayout()
        toolbar = qtw.QToolBar('styles')
        toolbar.setIconSize(core.QSize(16, 16))
        self.combo_font = qtw.QFontComboBox(toolbar)
        toolbar.addWidget(self.combo_font)
        self.combo_size = qtw.QComboBox(toolbar)
        toolbar.addWidget(self.combo_size)
        self.combo_size.setEditable(True)
        # db = gui.QFontDatabase()
        self.fontsizes = []
        # for size in db.standardSizes():
        for size in gui.QFontDatabase.standardSizes():
            self.combo_size.addItem(str(size))
            self.fontsizes.append(str(size))
        toolbar.addSeparator()

        for menudef in toolbardata:
            if not menudef:
                toolbar.addSeparator()
                continue
            # callback is vanwege compatibiliteit met wx versie soms twee routines,
            # waarvan hier alleen de eerste gebruikt wordt
            label, shortcut, icon, info, *callback = menudef
            if icon:
                action = gui.QAction(gui.QIcon(os.path.join(HERE, icon)), label, self)
                toolbar.addAction(action)
            else:
                action = gui.QAction(label, self)
            if shortcut:
                action.setShortcuts(list(shortcut.split(",")))
            if info.startswith("Toggle"):
                action.setCheckable(True)
                info = info[7]
                if info in ('B', 'I', 'U', 'S'):
                    font = gui.QFont()
                    if info == 'B':
                        font.setBold(True)
                    elif info == 'I':
                        font.setItalic(True)
                    elif info == 'U':
                        font.setUnderline(True)
                    else:  # if info == 'S':
                        font.setStrikeOut(True)
                    action.setFont(font)
                textfield.actiondict[label] = action
            action.triggered.connect(callback[0])
        # self.combo_font.activated[str].connect(textfield.text_family)
        self.combo_font.currentTextChanged[str].connect(textfield.text_family)
        # self.combo_size.activated[str].connect(textfield.text_size)
        self.combo_size.activated.connect(textfield.text_size)
        textfield.font_changed(textfield.font())
        hbox.addWidget(textfield)
        sizer.insertLayout(0, hbox)
        return toolbar

    def create_buttons(self, buttondefs, sizer=None):
        """add buttonbar
        """
        hbox = qtw.QHBoxLayout()
        buttons = []
        hbox.addStretch()
        for text, callback in buttondefs:
            btn = qtw.QPushButton(text, self)
            btn.clicked.connect(callback)
            if '(' in text:
                keydef = text.split('(')[1].split(')')[0]
                self.add_keybind(keydef, callback)
            hbox.addWidget(btn)
            buttons.append(btn)
        hbox.addStretch()
        if sizer:
            sizer.addLayout(hbox)
        else:
            self.sizer.addLayout(hbox)
        return buttons

    def add_keybind(self, keydef, callback, last=False):
        """add a keyborad shortcut definition
        """
        gui.QShortcut(keydef, self, callback)
        # extra actie in geval last == True hier niet nodig

    def reset_font(self):
        "initialize to standard values"
        progress_tab = 6
        # win = self.progress_text if self.master.parent.current_tab == progress_tab else self.text1
        win = self.progress_text if self.book.current_tab == progress_tab else self.text1
        win.setFontWeight(gui.QFont.Weight.Normal)
        win.setFontItalic(False)
        win.setFontUnderline(False)
        win.setFontFamily(win.defaultfamily)
        win.setFontPointSize(win.defaultsize)

    def enable_widget(self, widget, state):
        "make a field accessible or not"
        widget.setEnabled(state)

    def move_cursor_to_end(self, textfield):
        "position the cursor at the end of the text"
        textfield.moveCursor(gui.QTextCursor.MoveOperation.End, gui.QTextCursor.MoveMode.MoveAnchor)

    def set_textarea_contents(self, textfield, data):
        "set the page text"
        textfield.set_contents(data)

    def get_textarea_contents(self, textfield):
        "get the page text"
        return textfield.get_contents()

    def enable_toolbar(self, toolbar, value):
        "make the toolbar accessible (or not)"
        toolbar.setEnabled(value)

    def set_text_readonly(self, textfield, value):
        "protect page text from updating (or not)"
        textfield.setReadOnly(value)

    def is_enabled(self, widget):
        "return if the widget is accessible"
        return widget.isEnabled()

    def set_focus_to_field(self, field):
        "set the focus for this page to a specific field"
        field.setFocus()


class EditorPanel(qtw.QTextEdit):
    "Rich text editor displaying the selected comment"
    def __init__(self, parent):
        self.parent = parent
        # self.appbase = parent.book.parent
        # assert self.appbase == parent.appbase
        self.appbase = parent.appbase
        super().__init__()
        if self.appbase.use_rt:
            self.setAcceptRichText(True)
            self.setAutoFormatting(qtw.QTextEdit.AutoFormattingFlag.AutoAll)
            self.currentCharFormatChanged.connect(self.charformat_changed)
            self.actiondict = {}
        self.cursorPositionChanged.connect(self.cursorposition_changed)
        font = self.currentFont()
        self.setTabStopDistance(shared.tabsize(font.pointSize()))
        self.defaultfamily, self.defaultsize = font.family(), font.pointSize()

    def canInsertFromMimeData(self, source):
        "reimplementation of event handler"
        if source.hasImage():
            return True
        return super().canInsertFromMimeData(source)

    def insertFromMimeData(self, source):
        "reimplementation of event handler"
        if source.hasImage():
            image = source.imageData()
            # if sys.version < '3':
            #     image = gui.QImage(image)
            cursor = self.textCursor()
            document = self.document()
            num = self.appbase.imagecount
            num += 1
            self.appbase.imagecount = num
            urlname = f'{self.appbase.filename}_{num:05}.png'
            image.save(urlname)
            urlname = os.path.basename(urlname)  # make name "relative"
            document.addResource(gui.QTextDocument.ResourceType.ImageResource, core.QUrl(urlname),
                                 image)
            cursor.insertImage(urlname)
            self.appbase.imagelist.append(urlname)
        else:
            super().insertFromMimeData(self, source)

    def set_contents(self, data):
        "load contents into editor"
        if data.startswith('<'):  # only load as html if it looks like html
            self.setHtml(data)
            fmt = gui.QTextCharFormat()
            self.charformat_changed(fmt)
        else:
            self.setText(data)
        # self.oldtext = data

    def get_contents(self):
        "return contents from editor"
        if self.appbase.use_rt:
            return self.toHtml()
        return self.toPlainText()

    def text_bold(self):
        "selectie vet maken"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        if self.actiondict['&Bold'].isChecked():
            fmt.setFontWeight(gui.QFont.Weight.Bold)
        else:
            fmt.setFontWeight(gui.QFont.Weight.Normal)
        self.mergeCurrentCharFormat(fmt)

    def text_italic(self):
        "selectie schuin schrijven"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        fmt.setFontItalic(self.actiondict['&Italic'].isChecked())
        self.mergeCurrentCharFormat(fmt)

    def text_underline(self):
        "selectie onderstrepen"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        fmt.setFontUnderline(self.actiondict['&Underline'].isChecked())
        self.mergeCurrentCharFormat(fmt)

    def text_strikethrough(self):
        "selectie doorstrepen"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        fmt.setFontStrikeOut(self.actiondict['Strike&through'].isChecked())
        self.mergeCurrentCharFormat(fmt)

    def case_lower(self):
        "change case not implemented"

    def case_upper(self):
        "change case not implemented"

    def indent_more(self):
        "alinea verder laten inspringen"
        self.change_indent(1)

    def indent_less(self):
        "alinea minder ver laten inspringen"
        self.change_indent(-1)

    def change_indent(self, amount):
        "alinea verder/minder ver laten inspringen"
        if not self.hasFocus():
            return
        loc = self.textCursor()
        fmt = loc.blockFormat()
        wid = fmt.indent()
        if wid >= 1:
            fmt.setIndent(wid + amount)
        loc.mergeBlockFormat(fmt)

    def text_font(self):
        "lettertype en/of -grootte instellen"
        if not self.hasFocus():
            return
        font, ok = qtw.QFontDialog.getFont(self.currentFont(), self)
        if ok:
            fmt = gui.QTextCharFormat()
            fmt.setFont(font)
            self.setTabStopWidth(shared.tabsize(font.pointSize()))
            self.mergeCurrentCharFormat(fmt)

    def text_family(self, family):
        "lettertype instellen"
        fmt = gui.QTextCharFormat()
        fmt.setFontFamily(family)
        self.mergeCurrentCharFormat(fmt)
        self.setFocus()

    def enlarge_text(self):
        "change text style"
        size = self.parent.combo_size.currentText()
        indx = self.parent.fontsizes.index(size)
        if indx < len(self.parent.fontsizes) - 1:
            self.text_size(self.parent.fontsizes[indx + 1])

    def shrink_text(self):
        "change text style"
        size = self.parent.combo_size.currentText()
        indx = self.parent.fontsizes.index(size)
        if indx > 0:
            self.text_size(self.parent.fontsizes[indx - 1])

    def linespacing_1(self):
        "change text style"
        self.set_linespacing(0)

    def linespacing_15(self):
        "change text style"
        self.set_linespacing(150)

    def linespacing_2(self):
        "change text style"
        self.set_linespacing(200)

    def set_linespacing(self, amount):
        "change text style"
        if not self.hasFocus():
            return
        loc = self.textCursor()
        fmt = loc.blockFormat()
        if amount:
            format_type = gui.QTextBlockFormat.LineHeightTypes.ProportionalHeight
        else:
            format_type = gui.QTextBlockFormat.LineHeightTypes.SingleHeight
        fmt.setLineHeight(amount, format_type)
        loc.mergeBlockFormat(fmt)

    def increase_paragraph_spacing(self):
        "ruimte tussen alinea's vergroten"
        self.set_paragraph_spacing(more=True)

    def decrease_paragraph_spacing(self):
        "ruimte tussen alinea's verkleinen"
        self.set_paragraph_spacing(less=True)

    def set_paragraph_spacing(self, more=False, less=False):
        "ruimte tussen alinea's instellen"
        if not self.hasFocus():
            return
        unit = 0.5
        loc = self.textCursor()
        fmt = loc.blockFormat()
        top, bottom = fmt.topMargin(), fmt.bottomMargin()
        if more:
            factor = unit
        if less:
            factor = - 1 * unit
        if more or (less and top > unit):
            fmt.setTopMargin(top + factor * self.currentFont().pointSize())
        if more or (less and bottom > unit):
            fmt.setBottomMargin(bottom + factor * self.currentFont().pointSize())
        loc.mergeBlockFormat(fmt)

    def text_size(self, size):
        "lettergrootte instellen"
        pointsize = float(size)
        if pointsize > 0:
            fmt = gui.QTextCharFormat()
            fmt.setFontPointSize(pointsize)
            self.setTabStopDistance(shared.tabsize(pointsize))
            self.mergeCurrentCharFormat(fmt)
            self.setFocus()

    def charformat_changed(self, format):
        "wordt aangeroepen als het tekstformat gewijzigd is"
        self.font_changed(format.font())

    def cursorposition_changed(self):
        "wordt aangeroepen als de cursorpositie gewijzigd is"
        # self.alignment_changed(self.alignment())

    def font_changed(self, font):
        """fontgegevens aanpassen

        de selectie in de comboboxen wordt aangepast, de van toepassing zijnde
        menuopties worden aangevinkt, en en de betreffende toolbaricons worden
        geaccentueerd"""
        self.parent.combo_font.setCurrentIndex(
            self.parent.combo_font.findText(gui.QFontInfo(font).family()))
        self.parent.combo_size.setCurrentIndex(
            self.parent.combo_size.findText(str(font.pointSize())))
        self.actiondict["&Bold"].setChecked(font.bold())
        self.actiondict["&Italic"].setChecked(font.italic())
        self.actiondict["&Underline"].setChecked(font.underline())
        self.actiondict["Strike&through"].setChecked(font.strikeOut())

    def mergeCurrentCharFormat(self, format):
        "de geselecteerde tekst op de juiste manier weergeven"
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.select(gui.QTextCursor.SelectionType.WordUnderCursor)
        cursor.mergeCharFormat(format)
        super().mergeCurrentCharFormat(format)

    def update_bold(self):
        "compatibility"

    def update_italic(self):
        "compatibility"

    def update_underline(self):
        "compatibility"

    def _check_dirty(self):
        "check for modifications"
        return self.document().isModified()

    def _mark_dirty(self, value):
        "manually turn modified flag on/off (mainly intended for off)"
        self.document().setModified(value)

    def _openup(self, value):
        "make text accessible (or not)"
        self.setReadOnly(not value)


class Page0Gui(PageGui):
    "pagina 0: overzicht acties"
    def __init__(self, parent, master):
        # self.parent = parent
        # self.master = master
        super().__init__(parent, master)
        self.sizer = qtw.QVBoxLayout()

    def add_list(self, titles, widths):
        "add the selection list to the display"
        sizer = qtw.QHBoxLayout()
        p0list = qtw.QTreeWidget(self)
        p0list.setSortingEnabled(True)
        p0list.setHeaderLabels(titles)
        p0list.setAlternatingRowColors(True)
        p0hdr = p0list.header()
        p0hdr.setSectionsClickable(True)
        for indx, wid in enumerate(widths):
            p0hdr.resizeSection(indx, wid)
        p0hdr.setStretchLastSection(True)
        p0list.itemActivated.connect(self.on_activate_item)
        p0list.currentItemChanged.connect(self.on_change_selected)
        sizer.addWidget(p0list)
        self.sizer.addLayout(sizer)
        return p0list

    # def add_buttons(self, buttondefs):
    #     "add a button strip to the display"
    #     sizer = qtw.QHBoxLayout()
    #     sizer.addStretch()
    #     buttons = []
    #     for text, callback in buttondefs:
    #         button = qtw.QPushButton(text, self)
    #         button.clicked.connect(callback)
    #         sizer.addWidget(button)
    #         buttons.append(button)
    #     sizer.addStretch()
    #     self.sizer.addLayout(sizer)
    #     return buttons

    def finish_display(self):
        "final actions to show the screen"
        self.setLayout(self.sizer)

    def enable_sorting(self, p0list, value):
        "stel in of sorteren mogelijk is"
        p0list.setSortingEnabled(value)

    def on_change_selected(self, item_n, item_o):
        """callback voor wijzigen geselecteerd item, o.a. door verplaatsen van de
        cursor of door klikken

        item_n en item_o zijn de parameters vanuit de event
        """
        if item_n is None:  # o.a. self.p0list.clear() veroorzaakt dit
            return
        self.master.change_selected(item_n)

    def on_activate_item(self, item):
        """callback voor activeren van item, door doubleclick of enter

        item is de parameter vanuit de event
        """
        self.master.activate_item()

    def clear_list(self, p0list):
        "initialize the list"
        p0list.clear()
        p0list.has_selection = False

    def add_listitem(self, p0list, data):
        "add an item to the list"
        new_item = qtw.QTreeWidgetItem()
        new_item.setData(0, core.Qt.ItemDataRole.UserRole, data)
        p0list.addTopLevelItem(new_item)
        return new_item

    # def set_listitem_values(self, p0list, item, data):
    #     "set column values for list entry"
    #     for col, value in enumerate(data):
    #         if col == 0 and data[-1]:
    #             value = value + ' (A)'
    #         elif col == 1:
    #             pos = value.index(".") + 1
    #             value = value[pos:pos + 1].upper()
    #         elif col == 2:
    #             pos = value.index(".") + 1
    #             value = value[pos:]
    #         if col < len(data) - 1:
    #             item.setText(col, value)
    #     p0list.has_selection = True

    def get_items(self, p0list):
        "retrieve all listitems"
        return [p0list.topLevelItem(i) for i in range(p0list.topLevelItemCount())]

    # itemindicator is bij Qt een item, bij Wx een itemindex
    def get_item_text(self, p0list, itemindicator, column):
        "get the item's text for a specified column"
        return itemindicator.text(column)

    def set_item_text(self, p0list, itemindicator, column, text):
        "set the item's text for a specified column"
        itemindicator.setText(column, text)

    def get_first_item(self, p0list):
        "select the first item in the list"
        return p0list.topLevelItem(0)

    # def get_item_by_index(self, p0list, item_n):
    #     "select the indicated item in the list"
    #     return p0list.topLevelItem(item_n)

    def get_item_by_id(self, p0list, item_id):
        "select the item with the id requested"
        items = p0list.findItems(item_id, core.Qt.MatchFlag.MatchExactly, 0)
        if items:
            return items[0]
        return None

    # def has_selection(self, p0list):
    #     "return if list contains selection of data"
    #     return p0list.has_selection

    def set_selection(self, p0list):
        "set selected item if any"
        if self.book.current_item:  # is not None
            p0list.setCurrentItem(self.book.current_item)

    def get_selection(self, p0list):
        "get selected item"
        return p0list.currentItem()

    def ensure_visible(self, p0list, item):
        "make sure listitem is visible"
        p0list.scrollToItem(item)

    def set_button_text(self, button, txt):
        "set button text according to archive status"
        button.setText(txt)

    def get_selected_action(self, listbox):
        "return the key of the selected action"
        return listbox.currentItem().data(0, core.Qt.ItemDataRole.UserRole)

    def get_list_row(self, listbox):
        "return the event list's selected row index"
        return self.get_selection(listbox)

    def set_list_row(self, listbox, num):
        "set the event list's row selection"
        self.set_selection(listbox)


class Page1Gui(PageGui):
    "pagina 1: startscherm actie"
    def __init__(self, parent, master):
        # self.parent = parent
        # self.master = master
        super().__init__(parent, master)
        self.sizer = qtw.QVBoxLayout()
        self.setLayout(self.sizer)
        self.sizer.addSpacing(10)
        sizerx = qtw.QHBoxLayout()
        sizerx.addSpacing(10)
        self.gsizer = qtw.QGridLayout()
        self.row = 0
        self.gsizer.setRowMinimumHeight(self.row, 10)
        self.gsizer.setColumnStretch(2, 1)
        sizerx.addLayout(self.gsizer)
        self.sizer.addLayout(sizerx)
        self.sizer.addStretch()

    def add_textentry_line(self, labeltext, width, callback=None):
        "add a line with a text entry field to the display"
        self.row += 1
        self.gsizer.addWidget(qtw.QLabel(labeltext, self), self.row, 0)
        fld = qtw.QLineEdit(self)
        fld.setMaximumWidth(width)
        fld.setMinimumWidth(width)  # als ik deze weglaat worden alle velden even lang
        if callback:
            fld.textChanged.connect(callback)
        self.gsizer.addWidget(fld, self.row, 1)
        self.row += 1
        self.gsizer.setRowMinimumHeight(self.row, 5)
        return fld

    def add_combobox_line(self, labeltext, width, callback):
        "add a line with a combobox to the display"
        self.row += 1
        self.gsizer.addWidget(qtw.QLabel(labeltext, self), self.row, 0)
        fld = qtw.QComboBox(self)
        fld.setEditable(False)
        fld.setMaximumWidth(width)
        if callback:
            fld.currentIndexChanged.connect(callback)
        self.gsizer.addWidget(fld, self.row, 1)
        # extra blanco regel
        self.row += 1
        self.gsizer.setRowMinimumHeight(self.row, 5)
        return fld

    def add_pushbutton_line(self, labeltext, buttontext, callback):
        "add a line with a pushbutton to the display"
        self.row += 1
        sizer = qtw.QHBoxLayout()
        lbl = qtw.QLabel(labeltext, self)
        sizer.addWidget(lbl)
        sizer.addStretch()
        self.gsizer.addLayout(sizer, self.row, 1)
        self.row += 1
        sizer = qtw.QHBoxLayout()
        btn = qtw.QPushButton(buttontext, self)
        btn.clicked.connect(callback)
        sizer.addWidget(btn)
        sizer.addStretch()
        self.gsizer.addLayout(sizer, self.row, 1)
        return lbl, btn

    def add_textbox_line(self, labeltext, callback):
        "add a line with a large text entry field to the display"
        self.row += 1
        self.gsizer.addWidget(qtw.QLabel(labeltext, self), self.row, 0)
        self.row += 1
        sizer = qtw.QHBoxLayout()
        fld = qtw.QTextEdit(self)
        fld.textChanged.connect(callback)
        sizer.addWidget(fld)
        self.gsizer.addLayout(sizer, self.row, 0, 1, -1)
        return fld

    def show_button(self, button, value):
        "hide or shown button"
        if value:
            button.show()
        else:
            button.hide()

    def set_textfield_value(self, field, value):
        "set textfield value"
        field.setText(value)

    def set_label_value(self, field, value):
        "set textfield value"
        field.setText(value)

    def set_textbox_value(self, field, value):
        "set textfield value"
        field.setPlainText(value)

    def get_textfield_value(self, field):
        "get textfield value"
        return field.text()

    # def get_label_value(self, field):
    #     "get textfield value"
    #     return field.text()

    def get_textbox_value(self, field):
        "get textfield value"
        return field.toPlainText()

    def set_choice(self, field, domain, value):
        "set selected entry in a combobox"
        for x in range(len(domain)):
            code = field.itemData(x)
            if code == value:
                field.setCurrentIndex(x)
                break

    def get_choice_index(self, field):
        "get index of selected entry in a combobox"
        return field.currentIndex()

    def get_choice_data(self, field):
        "get selected entry in a combobox"
        idx = field.currentIndex()
        code = field.itemData(idx)
        text = field.currentText()
        return code, text

    def set_button_text(self, button, value):
        "set the text for the archive button"
        button.setText(value)

    def clear_combobox(self, cmb):
        "initialize combobox choices"
        cmb.clear()

    # def clear_stats(self):
    #     "initialize status choices"
    #     self.stat_choice.clear()

    # def clear_cats(self):
    #     "initialize category choices"
    #     self.cat_choice.clear()

    def add_combobox_choice(self, cmb, text, value):
        "add combobox choice"
        cmb.addItem(text, value)

    # def add_cat_choice(self, text, value):
    #     "add category choice"
    #     self.cat_choice.addItem(text, value)

    # def add_stat_choice(self, text, value):
    #     "add status choice"
    #     self.stat_choice.addItem(text, value)


class Page6Gui(PageGui):
    "pagina 6: voortgang"
    def __init__(self, parent, master):
        # self.parent = parent
        self.master = master
        super().__init__(parent, master)
        # sizes = 200, 100 if LIN else 280, 110
        # sizes = 350, 100 if LIN else 280, 110
        sizes = (200, 250) if LIN else (280, 110)
        self.sizer = qtw.QVBoxLayout()
        hsizer = qtw.QHBoxLayout()
        self.pnl = qtw.QSplitter(self)
        self.pnl.setOrientation(core.Qt.Orientation.Vertical)
        self.pnl.setSizes(sizes)
        hsizer.addWidget(self.pnl)
        self.sizer.addLayout(hsizer)

    def create_list(self):
        "maak het lijstgedeelte van de display"
        plist = qtw.QListWidget(self)
        plist.currentItemChanged.connect(self.on_select_item)
        self.new_action = gui.QShortcut('Shift+Ctrl+N', self)
        if not self.appbase.work_with_user:
            plist.itemActivated.connect(self.on_activate_item)
            # plist.itemDoubleClicked.connect(self.on_activate_item)
            # action = qtw.QShortcut('Shift+Ctrl+N', self, functools.partial(
            #     self.on_activate_item, plist.item(0)))
            self.new_action.activated.connect(self.on_activate_item)
            # self.new_action.activated.connect(functools.partial(self.on_activate_item, plist.item(0)))
        self.pnl.addWidget(plist)
        gui.QShortcut('Shift+Ctrl+Up', self, self.master.goto_prev)
        gui.QShortcut('Shift+Ctrl+Down', self, self.master.goto_next)
        return plist

    def create_textfield(self, width, height, callback):
        "maak het textarea gedeelte van de display"
        textpanel = qtw.QFrame(self)
        vsizer = qtw.QVBoxLayout()
        sizer = qtw.QHBoxLayout()
        ptext = self.create_text_field(sizer, width, height, callback)
        if self.appbase.use_rt:
            data = self.master.get_toolbar_data(ptext)
            self.toolbar = self.create_toolbar(sizer, ptext, data)
        vsizer.addLayout(sizer)
        textpanel.setLayout(vsizer)
        textpanel.show()
        self.pnl.addWidget(textpanel)
        return ptext

    # def add_buttons(self):
    #     self.save_button = qtw.QPushButton('Sla wijzigingen op (Ctrl-S)', self)
    #     self.save_button.clicked.connect(self.master.savep)
    #     gui.QShortcut('Ctrl+S', self, self.master.savep)
    #     self.cancel_button = qtw.QPushButton('Maak wijzigingen ongedaan (Alt-Ctrl-Z)', self)
    #     self.cancel_button.clicked.connect(self.master.restorep)
    #     gui.QShortcut('Alt+Ctrl+Z', self, self.master.restorep)
    #     sizer2 = qtw.QHBoxLayout()
    #     sizer2.addStretch()
    #     sizer2.addWidget(self.save_button)
    #     sizer2.addWidget(self.cancel_button)
    #     sizer2.addStretch()
    #     self.vsizer.addLayout(sizer2)

    def finish_display(self):
        "final actions to show the screen"
        self.setLayout(self.sizer)

    def on_activate_item(self, item=None):
        """callback voor dubbelklik of Enter op een item

        wanneer dit gebeurt op het eerste item kan een nieuwe worden aangemaakt
        """
        if self.master.initializing:
            return
        if item is None or item == self.progress_list.item(0):
            self.master.initialize_new_event()

    def on_select_item(self, item_n, item_o):
        """callback voor het selecteren van een item

        selecteren van (klikken op) een regel in de listbox doet de inhoud van de
        textctrl ook veranderen. eerst controleren of de tekst veranderd is
        dat vragen moet ook in de situatie dat je op een geactiveerde knop klikt,
        het panel wilt verlaten of afsluiten
        de knoppen onderaan doen de hele lijst bijwerken in self.parent.book.p
        item_n en item_o worden door de event meegegeven
        """
        self.set_text_readonly(self.master.progress_text, True)
        if item_n is None:
            # als ik al eens eerder op page 6 geweest ben en er terugkom of bij reset
            return
        self.current_item = self.get_list_row(self.master.progress_list)
        indx = self.current_item - 1
        if indx == -1:
            self.master.oldtext = ""
        else:
            self.master.oldtext = self.master.event_data[indx]  # dan wel item_n.text()
        self.master.initializing = True
        self.master.oldtext = self.convert_text(self.master.progress_text, self.master.oldtext,
                                                to='rich')
        self.master.initializing = False
        if not self.book.pagedata.arch:
            if indx > -1:
                self.master.progress_text.setReadOnly(not self.appbase.is_user)
                if self.appbase.use_rt:
                    self.enable_toolbar(self.toolbar, self.appbase.is_user)
            self.move_cursor_to_end(self.master.progress_text)
        # self.set_focus_to_field(self.master.progress_text)
        self.master.progress_text.setFocus()

    # def init_textfield(self):
    #     "set up text field"
    #     self.clear_textfield()
    #     self.protect_textfield()

    def create_new_listitem(self, listbox, textfield, datum, oldtext):
        """update widgets with new event
        """
        newitem = qtw.QListWidgetItem(f'{datum} - {oldtext}')
        newitem.setData(core.Qt.ItemDataRole.UserRole, 0)
        listbox.insertItem(1, newitem)
        listbox.setCurrentRow(1)
        textfield.setText(oldtext)
        textfield.setReadOnly(False)
        textfield.setFocus()

    def clear_list(self, listbox):
        "clear out events list widget"
        listbox.clear()

    def add_first_listitem(self, listbox, text):
        "set up top item to add new event when doubleclickes"
        first_item = qtw.QListWidgetItem(text)
        first_item.setData(core.Qt.ItemDataRole.UserRole, -1)
        listbox.addItem(first_item)

    def add_item_to_list(self, listbox, textfield, idx, datum):
        """add an entry to the events list widget (when initializing)
        first convert to HTML (if needed, see set_contents method) and back
        """
        maxlen = 80
        textfield.set_contents(self.master.event_data[idx])
        tekst_plat = textfield.toPlainText()
        text = tekst_plat.split("\n")[0].strip()
        text = text if len(text) < maxlen else text[:maxlen] + "..."
        newitem = qtw.QListWidgetItem(f'{datum} - {text}')
        newitem.setData(core.Qt.ItemDataRole.UserRole, idx)
        listbox.addItem(newitem)

    def set_list_callbacks(self, listbox, callback0, callback1):
        "connect or disconnect depending on user's permissions"
        if self.appbase.is_user:
            listbox.itemActivated.connect(callback0)
            self.new_action.activated.connect(callback1)
        else:
            # try:
            with contextlib.suppress(TypeError):
                listbox.itemActivated.disconnect()
                self.new_action.activated.disconnect()
            # except TypeError:
            #     # avoid "disconnect() failed between 'itemActivated' and all its connections"
            #     pass

    def set_listitem_text(self, listbox, itemindex, text):
        "set text for the given listitem"
        listbox.item(itemindex).setText(text)

    def set_listitem_data(self, listbox, itemindex):
        "return the given listitem's text"
        listbox.item(itemindex).setData(itemindex - 1, core.Qt.ItemDataRole.UserRole)

    def get_listitem_text(self, listbox, itemindex):
        "return the indicated listitem's text"
        return listbox.item(itemindex).text()

    def get_list_row(self, listbox):
        "return the event list's selected row index"
        return listbox.currentRow()

    def set_list_row(self, listbox, num):
        "set the event list's row selection"
        listbox.setCurrentRow(num)

    def get_list_rowcount(self, listbox):
        "return the number of rows in the event list (minus the top one)"
        return listbox.count()

    def clear_textfield(self, textbox):
        "empty textfield context"
        textbox.clear()

    def get_textfield_contents(self, textbox):
        "return contents of text area"
        return textbox.get_contents()

    def set_textfield_contents(self, textbox, text):
        "set contents of textarea"
        textbox.set_contents(text)

    def move_cursor_to_end(self, textbox):
        "position cursor at the end of the text"
        textbox.moveCursor(gui.QTextCursor.MoveOperation.End, gui.QTextCursor.MoveMode.MoveAnchor)

    def convert_text(self, textbox, text, to):
        """convert plain text to html or back using the textfield's methods and return the result

        `to` should be "rich" or "plain"
        """
        retval = ''
        if to == 'rich':
            textbox.set_contents(text)
            retval = textbox.get_contents()
        else:  # if to == 'plain':
            retval = textbox.toPlainText()
        return retval


class SortOptionsDialogGui(qtw.QDialog):
    """dialoog om de sorteer opties in te stellen
    """
    def __init__(self, master, parent, title):
        # self.parent = parent
        self.master = master
        super().__init__(parent.gui)
        self.setWindowTitle(title)
        self.sizer = qtw.QVBoxLayout()
        self.grid = qtw.QGridLayout()
        self.sizer.addLayout(self.grid)
        self.row = 0
        self.setLayout(self.sizer)

    def add_checkbox_line(self, tekst, checked, callback):
        "add a line with a checkbox to the grid (full width)"
        # self.row += 1
        cb = qtw.QCheckBox(tekst, self)
        cb.setChecked(checked)
        cb.stateChanged.connect(callback)
        self.grid.addWidget(cb, self.row, 0, 1, 4)
        return cb

    def add_seqnumtext_to_list(self, label):
        "put a sequwnce number on the current line"
        self.row += 1
        lbl = qtw.QLabel(label, self)
        self.grid.addWidget(lbl, self.row, 0)
        return lbl

    def add_colnameselector_to_list(self, name, lijst):
        "add a combobox to the current line"
        cmb = qtw.QComboBox(self)
        cmb.setEditable(False)
        cmb.addItems(lijst)
        cmb.setCurrentIndex(lijst.index(name))  # 0))
        self.grid.addWidget(cmb, self.row, 1)
        return cmb

    def add_radiobuttons_to_line(self, buttondefs):
        """add a radiobutton to the current line

        also add it to the buttongroup that is created with the first button
        """
        rbg = qtw.QButtonGroup(self)
        col = 1
        for text, direction_id, checked in buttondefs:
            rb = qtw.QRadioButton(text, self)
            rb.setChecked(checked)
            rbg.addButton(rb, direction_id)
            col += 1
            self.grid.addWidget(rb, self.row, col)
            # rbg.button(self._asc_id).setChecked(True)
        return rbg

    def add_okcancel_buttonbox(self):
        "add the action buttons to the bottom of the dialog"
        buttonbox = qtw.QDialogButtonBox(qtw.QDialogButtonBox.StandardButton.Ok
                                         | qtw.QDialogButtonBox.StandardButton.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        self.sizer.addWidget(buttonbox)

    def enable_fields(self, state):
        "enable/disable widgets"
        for lbl, cmb, rbg in self.master.widgets:
            # lbl.setEnabled(state)
            cmb.setEnabled(state)
            for btn in rbg.buttons():
                btn.setEnabled(state)

    def accept(self):
        """dialoog bevestigen
        """
        ok = self.master.confirm()
        if ok:
            super().accept()

    def get_combobox_value(self, cmb):
        "return the selected value of a combobox"
        return cmb.currentText()

    def get_rbgroup_value(self, rbg):
        "return the id of the checked button in a radiobutton group"
        return rbg.checkedId()

    def get_checkbox_value(self, cb):
        "return the state of a checkbox"
        return cb.isChecked()


class SelectOptionsDialogGui(qtw.QDialog):
    """dialoog om de selectie op te geven
    """
    def __init__(self, master, parent, title):
        self.master = master
        # self.parent = parent
        super().__init__(parent.gui)
        self.setWindowTitle(title)
        self.sizer = qtw.QVBoxLayout()
        self.grid = qtw.QGridLayout()
        self.sizer.addLayout(self.grid)
        self._cbg = qtw.QButtonGroup()
        self._cbg.setExclusive(False)
        self.extra_cbgs = []
        self.setLayout(self.sizer)

    def add_checkbox_to_grid(self, title, row, col):
        "set up a checkbox on the left hand side, for a search option"
        vbox = qtw.QVBoxLayout()
        cb = qtw.QCheckBox(title, self)
        self._cbg.addButton(cb)
        vbox.addWidget(cb)
        vbox.addStretch()
        self.grid.addLayout(vbox, row, col)
        return cb

    def start_optionsblock(self):
        "set up space on the right hand size to specify search criteria"
        hgrid = qtw.QGridLayout()
        self.blockrow = -1
        return hgrid

    def add_textentry_line_to_block(self, block, labeltext, callback, first=False):
        "add a caption and a text entry field to the block"
        self.blockrow += 1
        text = qtw.QLineEdit(self)
        block.addWidget(qtw.QLabel(labeltext, self), self.blockrow, 0)
        text.textChanged.connect(functools.partial(callback, text))
        block.addWidget(text, self.blockrow, 1)
        return text

    def add_radiobuttonrow_to_block(self, block, buttondefs, callback=None, alignleft=True):
        "add a row of radiobuttons to the block"
        self.blockrow += 1
        rbg = qtw.QButtonGroup(self)
        hbox = qtw.QHBoxLayout()
        for text in buttondefs:
            rb = qtw.QRadioButton(text, self)
            rbg.addButton(rb)
            if callback:
                # rb.toggled.connect(functools.partial(callback, rb))
                rb.toggled.connect(callback)
            hbox.addWidget(rb)
        if alignleft:
            hbox.addStretch()
        block.addLayout(hbox, self.blockrow, 0)
        return rbg.buttons()

    def add_checkboxlist_to_block(self, block, namelist, callback):
        "add a caption and a list of checkboxes to the block"
        self.blockrow += 1
        cbg = qtw.QButtonGroup(self)
        cbg.setExclusive(False)
        self.extra_cbgs.append(cbg)
        hbox = qtw.QVBoxLayout()
        for x in namelist:
            check = qtw.QCheckBox(x, self)
            check.toggled.connect(functools.partial(callback, check))
            hbox.addWidget(check)
            cbg.addButton(check)
        block.addLayout(hbox, self.blockrow, 0)
        return cbg.buttons()

    def finish_block(self, block, row, col):
        "finish the block layout"
        self.grid.addLayout(block, row, col)  # 0, 2)

    def add_okcancel_buttonbar(self):
        "add action buttons to the dialog"
        buttonbox = qtw.QDialogButtonBox(qtw.QDialogButtonBox.StandardButton.Ok
                                         | qtw.QDialogButtonBox.StandardButton.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

    def finalize_display(self):
        "final actions to realize the screen"

    # def doelayout(self):
    #     """realize the dialog layout
    #     """
    #     vbox = qtw.QVBoxLayout()
    #     vbox.addWidget(self.check_options.buttons()[1])
    #     vbox.addStretch()
    #     grid.addLayout(vbox, 1, 0)

    #     hbox = qtw.QHBoxLayout()
    #     vbox = qtw.QVBoxLayout()
    #     vbox.addSpacing(3)
    #     vbox.addWidget(qtw.QLabel("selecteer een of meer:", self))
    #     vbox.addStretch()
    #     hbox.addLayout(vbox)
    #     vbox = qtw.QVBoxLayout()
    #     for check in self.check_cats.buttons():
    #         vbox.addWidget(check)
    #     hbox.addLayout(vbox)
    #     grid.addLayout(hbox, 1, 2)

    #     vbox = qtw.QVBoxLayout()
    #     vbox.addWidget(self.check_options.buttons()[2])
    #     vbox.addStretch()
    #     grid.addLayout(vbox, 2, 0)

    #     hbox = qtw.QHBoxLayout()
    #     vbox = qtw.QVBoxLayout()
    #     vbox.addSpacing(3)
    #     vbox.addWidget(qtw.QLabel("selecteer een of meer:", self))
    #     vbox.addStretch()
    #     hbox.addLayout(vbox)
    #     vbox = qtw.QVBoxLayout()
    #     for check in self.check_stats.buttons():
    #         vbox.addWidget(check)
    #     hbox.addLayout(vbox)
    #     grid.addLayout(hbox, 2, 2)

    #     vbox = qtw.QVBoxLayout()
    #     vbox.addWidget(self.check_options.buttons()[3])
    #     vbox.addStretch()
    #     grid.addLayout(vbox, 3, 0)

    #     hbox = qtw.QHBoxLayout()
    #     if self.parent.parent.parent.use_separate_subject:
    #         grid2 = qtw.QGridLayout()
    #         grid2.addWidget(qtw.QLabel(self.parent.parent.ctitels[4] + ":", self),
    #                         0, 0)
    #         grid2.addWidget(self.text_zoek, 0, 1)
    #         hbox2 = qtw.QHBoxLayout()
    #         for rb in self.radio_id2.buttons():
    #             hbox2.addWidget(rb)
    #         grid2.addLayout(hbox2, 1, 0)
    #         grid2.addWidget(qtw.QLabel(self.parent.parent.ctitels[5] + ":", self),
    #                         2, 0)
    #         grid2.addWidget(self.text_zoek2, 2, 1)
    #         hbox.addLayout(grid2)
    #     else:
    #         hbox.addWidget(qtw.QLabel('zoek naar:', self))
    #         hbox.addWidget(self.text_zoek)
    #     grid.addLayout(hbox, 3, 2)

    #     vbox = qtw.QVBoxLayout()
    #     vbox.addWidget(self.check_options.buttons()[4])
    #     vbox.addStretch()
    #     grid.addLayout(vbox, 4, 0)
    #     hbox = qtw.QHBoxLayout()
    #     for radio in self.radio_arch.buttons():
    #         hbox.addWidget(radio)
    #     grid.addLayout(hbox, 4, 2)
    #     sizer.addLayout(grid)

    #     sizer.addWidget(self.buttonbox)
    #     self.setLayout(sizer)

    def set_textentry_value(self, textentry, value):
        "set the value of a text entry box"
        textentry.setText(value)

    def set_radiobutton_value(self, radiobutton, value):
        "check or uncheck a radiobutton"
        radiobutton.setChecked(value)

    def set_checkbox_value(self, checkbox, value):
        "check or ncheck a checkbox"
        checkbox.setChecked(value)

    def on_text(self, arg, text):
        "callback voor activiteitnummer checkboxes"
        if arg in ('gt', 'lt'):
            obj = self._cbg.buttons()[0]  # check_options.buttons()[0]
            other = self.master.text_lt if arg == 'gt' else self.master.text_gt
        else:  # if arg.startswith('zoek'):  iets anders niet mogelijk
            obj = self._cbg.buttons()[3]  # check_options.buttons()[3]
            other = self.master.text_zoek2 if arg == 'zoek' else self.master.text_zoek
        if text == "" and other.text() == "":
            obj.setChecked(False)
        else:
            obj.setChecked(True)
        return obj                      # return value is puur voor de testroutine

    def on_cb_checked(self, arg):  # , val):
        "callback voor status en soort checkboxes"
        for ix, grp in enumerate(self.extra_cbgs):
            if arg in grp.buttons():
                obj = self._cbg.buttons()[ix + 1]
                break
        else:  # checkbutton niet in één van de checkbuttongroups - kan eigenlijk niet
            return
        # # if arg == 'cat':
        # if arg in self.extra_cbgs[0].buttons():
        #     obj = self._cbg.buttons()[1]  # parent.cb_soort waarden
        #     grp = self.extra_cbgs[0]
        # # else:  # if arg == 'stat':  iets anders niet mogelijk
        # elif arg in self.extra_cbgs[1].buttons():
        #     obj = self._cbg.buttons()[2]  # parent.cb_status waarden
        #     grp = self.extra_cbgs[1]
        # else:   # zou niet voor moeten kunnen komen - niks doen
        #     return
        oneormore = False
        for btn in grp.buttons():
            if btn.isChecked():
                oneormore = True
                break
        if oneormore:
            obj.setChecked(True)
        else:
            obj.setChecked(False)
        return btn, obj    # t.b.v. testmethode

    def on_rb_checked(self, arg):  # , val):
        "callback voor archief radiobuttons"
        # deze wordt niet (meer) gepartiald, wordt dat arg dan nog wel meegegeven?
        # self.parent.cb_arch.setChecked(True)
        self._cbg.buttons()[4].setChecked(True)

    def accept(self):
        "aangegeven opties verwerken in sel_args dictionary"
        ok = self.master.confirm()
        if ok:
            super().accept()

    def get_textentry_value(self, textentry):
        "return the value of a text entry box"
        return textentry.text()

    def get_radiobutton_value(self, radiobutton):
        "return the state of a radiobutton"
        return radiobutton.isChecked()

    def get_checkbox_value(self, checkbox):
        "return the state of a checkbox"
        return checkbox.isChecked()

    def set_focus_to(self, widget):
        "set the input focus to the specified widget"
        widget.setFocus()


class SettOptionsDialogGui(qtw.QDialog):
    """generic dialog to maintain options

    the specific type of option(s) is passed in via the cls argument
    """
    def __init__(self, master, parent, title):
        self.master = master
        size = (350, 200)
        super().__init__(parent.gui)
        self.resize(*size)
        self.setWindowTitle(title)
        self.sizer = qtw.QVBoxLayout()

    def add_listbox_with_buttons(self, titel, data, actions):
        """maak een listbox waarvan de items aangepast kunnen worden
        met een rij buttons eronder
        wx heeft hiervoor een dedicated widget
        """
        self.sizer.addWidget(qtw.QLabel(titel, self))
        self.elb = qtw.QListWidget(self)
        self.elb.currentItemChanged.connect(self.end_edit)
        self.elb.itemDoubleClicked.connect(self.edit_item)
        for text in data:
            self.elb.addItem(text)
        self.sizer.addWidget(self.elb)

        box = qtw.QHBoxLayout()
        box.addStretch()
        self.b_edit = qtw.QPushButton('&Edit', self)
        self.b_edit.clicked.connect(self.edit_item)
        box.addWidget(self.b_edit)
        if actions['can_add_remove']:
            self.b_new = qtw.QPushButton('&New', self)
            self.b_new.clicked.connect(self.add_item)
            box.addWidget(self.b_new)
            self.b_delete = qtw.QPushButton('&Delete', self)
            self.b_delete.clicked.connect(self.remove_item)
            box.addWidget(self.b_delete)
        if actions['can_reorder']:
            self.b_up = qtw.QPushButton('Move &Up', self)
            self.b_up.clicked.connect(self.move_item_up)
            box.addWidget(self.b_up)
            self.b_down = qtw.QPushButton('Move &Down', self)
            self.b_down.clicked.connect(self.move_item_down)
            box.addWidget(self.b_down)
        box.addStretch()
        self.sizer.addLayout(box)
        return self.elb

    def add_label(self, infotext):
        "add some explanatory text to the display"
        self.sizer.addWidget(qtw.QLabel("\n".join(infotext), self))

    def add_okcancel_buttonbox(self):
        "add action buttons to confirm or discard the dialog"
        buttonbox = qtw.QDialogButtonBox(qtw.QDialogButtonBox.StandardButton.Ok
                                         | qtw.QDialogButtonBox.StandardButton.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        self.sizer.addWidget(buttonbox)

    def finish_display(self):
        "final actions before displaying the screen"
        self.setLayout(self.sizer)

    def keyReleaseEvent(self, evt):
        """reimplementation of keyboard event handler
        """
        # misschien beter met een acceleratorkey?
        keycode = evt.key()
        if keycode == core.Qt.Key.Key_F2:
            self.edit_item()
            return
        super().keyReleaseEvent(evt)

    def edit_item(self):
        "open de betreffende regel voor editing"
        item = self.elb.currentItem()
        self.elb.openPersistentEditor(item)
        self.elb.editItem(item)

    def end_edit(self, item_n, item_o):
        """callback for end of editing

        dit lijkt aangeroepen te worden voorafgaand aan een openPersistentEditor call
        pas op dat moment wordt de gewijzigde waarde doorgegeven aan de dialoog (vanwege
        de closePersistenteditor call)
        item_n en item_o zijn parameters van de event neem ik aan
        """
        self.elb.closePersistentEditor(item_o)

    def add_item(self):
        "open een nieuwe lege regel"
        item = qtw.QListWidgetItem('')
        self.elb.addItem(item)
        self.elb.setCurrentItem(item)
        self.elb.openPersistentEditor(item)
        self.elb.editItem(item)
        return item   # return value is t.b.v. unittest

    def remove_item(self):
        "verwijder de betreffende regel"
        ## item = self.elb.currentItem()
        row = self.elb.currentRow()
        self.elb.takeItem(row)

    def move_item_up(self):
        "inhoud omwisselen met de regel erboven"
        self.move_item(up=True)

    def move_item_down(self):
        "inhoud omwisselen met de regel eronder"
        self.move_item(up=False)

    def move_item(self, up=True):
        "realize moving of item"
        oldrow = self.elb.currentRow()
        if up:
            if oldrow == 0:
                return
            newrow = oldrow - 1
        else:
            newrow = oldrow + 1
            if newrow == self.elb.count():
                return
        item = self.elb.currentItem()
        text = item.text()
        item_to_replace = self.elb.item(newrow)
        text_to_replace = item_to_replace.text()
        item_to_replace.setText(text)
        item.setText(text_to_replace)
        self.elb.setCurrentItem(item_to_replace)

    def accept(self):
        """Confirm changes to parent window

        call method on the helper class if provided
        """
        # force checking in the latest change
        # (this is a workaround as it's not needed in the original version)
        self.elb.closePersistentEditor(self.elb.currentItem())
        self.master.confirm()
        super().accept()

    def read_listbox_data(self, elb):
        "return the updated listbox items"
        return [elb.item(x).text() for x in range(elb.count())]


class LoginBoxGui(qtw.QDialog):
    """Sign in with userid & password
    """
    def __init__(self, master, parent):
        self.master = master
        super().__init__(parent.gui)
        self.vbox = qtw.QVBoxLayout()
        self.grid = qtw.QGridLayout()
        self.row = -1
        self.vbox.addLayout(self.grid)

    def add_textinput_line(self, text, hide=False):
        "add a line with some text and an input field to the display"
        self.row += 1
        self.grid.addWidget(qtw.QLabel(text, self), self.row, 0)
        textfield = qtw.QLineEdit(self)
        self.grid.addWidget(textfield, self.row, 1)
        if hide:
            textfield.setEchoMode(qtw.QLineEdit.EchoMode.Password)
        return textfield

    def add_okcancel_buttonbox(self):
        "add action buttons to confirm or dismiss the dialog"
        bbox = qtw.QDialogButtonBox(qtw.QDialogButtonBox.StandardButton.Ok
                                    | qtw.QDialogButtonBox.StandardButton.Cancel)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        self.vbox.addWidget(bbox)

    def finish_display(self):
        "final actions before showing"
        self.setLayout(self.vbox)

    def accept(self):
        "callback for OK button"
        self.master.confirm()
        super().accept()

    def get_textinput_value(self, field):
        "return the value of a text input field"
        return field.text()
