#! usr/bin/env python
# -*- coding: UTF-8 -*-
"""Actie (was: problemen) Registratie, PyQT5 versie
"""
from __future__ import print_function
import os
import sys
import pathlib
# import enum
# import pprint
import collections
import functools
import PyQt5.QtWidgets as qtw
import PyQt5.QtPrintSupport as qtp
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
from mako.template import Template
## import probreg.pr_globals as pr
import probreg.shared as shared
LIN = True if os.name == 'posix' else False
# HERE = os.path.dirname(__file__)
sortorder = {shared.Order.A.name: core.Qt.AscendingOrder,
             shared.Order.D.name: core.Qt.DescendingOrder}
xmlfilter = "XML files (*.xml);;all files (*.*)"


def show_message(win, message):
    "present a message and wait for the user to confirm (having read it or whatever)"
    qtw.QMessageBox.information(win, shared.app_title, message)


def get_open_filename(parent, start=pathlib.Path.cwd()):
    "get the name of a file to open"
    fname, pattern = qtw.QFileDialog.getOpenFileName(
        parent, shared.app_title + " - kies een gegevensbestand", str(start), xmlfilter)
    return fname


def get_save_filename(parent, start=pathlib.Path.cwd()):
    "get the name of a file to save"
    fname, pattern = qtw.QFileDialog.getSaveFileName(
        parent, shared.app_title + " - nieuw gegevensbestand", str(start), xmlfilter)
    return fname


def get_choice_item(parent, caption, choices, current=0):
    "allow the user to choose one of a set of options and return it"
    choice, ok = qtw.QInputDialog.getItem(parent, shared.app_title, caption, choices,
                                          current=current, editable=False)
    if ok:
        return choice
    return ''


def ask_cancel_question(win, message):
    "ask the user a question with an option to cancel the process"
    retval = qtw.QMessageBox.question(win, shared.app_title, message,
                                      buttons=qtw.QMessageBox.Yes | qtw.QMessageBox.No |
                                                                    qtw.QMessageBox.Cancel)
    return retval == qtw.QMessageBox.Yes, retval == qtw.QMessageBox.Cancel


def show_dialog(win, dlg, args=None):
    "show a dialog and return if the dialog was confirmed / accepted"
    ok = False
    if args is not None:
        ok = dlg(win, args).exec_()
    else:
        ok = dlg(win).exec_()
    return ok == qtw.QDialog.Accepted


class EditorPanelGui(qtw.QTextEdit):    # TODO: mogelijk alleen hier
    "Rich text editor displaying the selected note"

    def __init__(self, parent):
        self.tbparent = parent
        self.parent = parent.parent.parent
        super().__init__()
        self.setAcceptRichText(True)
        self.setAutoFormatting(qtw.QTextEdit.AutoAll)
        self.currentCharFormatChanged.connect(self.charformat_changed)
        self.cursorPositionChanged.connect(self.cursorposition_changed)
        font = self.currentFont()
        self.setTabStopWidth(shared.tabsize(font.pointSize()))
        self.defaultfamily, self.defaultsize = font.family(), font.pointSize()

    def canInsertFromMimeData(self, source):
        "reimplementation of event handler"
        if source.hasImage:
            return True
        return qtw.QTextEdit.canInsertFromMimeData(source)

    def insertFromMimeData(self, source):
        "reimplementation of event handler"
        if source.hasImage():
            image = source.imageData()
            if sys.version < '3':
                image = gui.QImage(image)
            cursor = self.textCursor()
            document = self.document()
            num = self.parent.imagecount
            num += 1
            self.parent.imagecount = num
            urlname = '{}_{:05}.png'.format(self.parent.filename, num)
            image.save(urlname)
            urlname = os.path.basename(urlname)  # make name "relative"
            document.addResource(gui.QTextDocument.ImageResource,
                                 core.QUrl(urlname), image)
            cursor.insertImage(urlname)
            self.parent.imagelist.append(urlname)
        else:
            qtw.QTextEdit.insertFromMimeData(self, source)

    def set_contents(self, data):
        "load contents into editor"
        if data.startswith('<'):  # only load as html if it looks like html
            self.setHtml(data)
        else:
            self.setText(data)
        fmt = gui.QTextCharFormat()
        self.charformat_changed(fmt)
        self.oldtext = data

    def get_contents(self):
        "return contents from editor"
        return self.toHtml()

    def text_bold(self):
        "selectie vet maken"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        if self.tbparent.actiondict['&Bold'].isChecked():
            fmt.setFontWeight(gui.QFont.Bold)
        else:
            fmt.setFontWeight(gui.QFont.Normal)
        self.mergeCurrentCharFormat(fmt)

    def text_italic(self):
        "selectie schuin schrijven"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        fmt.setFontItalic(self.tbparent.actiondict['&Italic'].isChecked())
        self.mergeCurrentCharFormat(fmt)

    def text_underline(self):
        "selectie onderstrepen"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        fmt.setFontUnderline(self.tbparent.actiondict['&Underline'].isChecked())
        self.mergeCurrentCharFormat(fmt)

    def text_strikethrough(self):
        "selectie doorstrepen"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        fmt.setFontStrikeOut(self.tbparent.actiondict['Strike&through'].isChecked())
        self.mergeCurrentCharFormat(fmt)

    def case_lower(self):
        "change case not implemented"
        pass

    def case_upper(self):
        "change case not implemented"
        pass

    def indent_more(self):
        "alinea verder laten inspringen"
        if not self.hasFocus():
            return
        loc = self.textCursor()
        where = loc.block()
        fmt = where.blockFormat()
        wid = fmt.indent()
        fmt.setIndent(wid + 1)
        loc.mergeBlockFormat(fmt)

    def indent_less(self):
        "alinea minder ver laten inspringen"
        if not self.hasFocus():
            return
        loc = self.textCursor()
        where = loc.block()
        fmt = where.blockFormat()
        wid = fmt.indent()
        if wid >= 1:
            fmt.setIndent(wid - 1)
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
        size = self.tbparent.combo_size.currentText()
        indx = self.tbparent.fontsizes.index(size)
        if indx < len(self.tbparent.fontsizes) - 1:
            self.text_size(self.tbparent.fontsizes[indx + 1])

    def shrink_text(self):
        "change text style"
        size = self.tbparent.combo_size.currentText()
        indx = self.tbparent.fontsizes.index(size)
        if indx > 0:
            self.text_size(self.tbparent.fontsizes[indx - 1])

    def linespacing_1(self):
        "change text style"
        if not self.hasFocus():
            return
        loc = self.textCursor()
        fmt = loc.block().blockFormat()
        fmt.setLineHeight(0, gui.QTextBlockFormat.SingleHeight)
        loc.mergeBlockFormat(fmt)

    def linespacing_15(self):
        "change text style"
        if not self.hasFocus():
            return
        loc = self.textCursor()
        fmt = loc.block().blockFormat()
        fmt.setLineHeight(150, gui.QTextBlockFormat.ProportionalHeight)
        loc.mergeBlockFormat(fmt)

    def linespacing_2(self):
        "change text style"
        if not self.hasFocus():
            return
        loc = self.textCursor()
        fmt = loc.block().blockFormat()
        fmt.setLineHeight(200, gui.QTextBlockFormat.ProportionalHeight)
        loc.mergeBlockFormat(fmt)

    def increase_paragraph_spacing(self):
        "change text style"
        if not self.hasFocus():
            return
        loc = self.textCursor()
        fmt = loc.block().blockFormat()
        top, bottom = fmt.topMargin(), fmt.bottomMargin()
        fmt.setTopMargin(top + 0.5 * self.currentFont().pointSize())
        fmt.setBottomMargin(bottom + 0.5 * self.currentFont().pointSize())
        loc.mergeBlockFormat(fmt)

    def decrease_paragraph_spacing(self):
        "change text style"
        if not self.hasFocus():
            return
        loc = self.textCursor()
        fmt = loc.block().blockFormat()
        top, bottom = fmt.topMargin(), fmt.bottomMargin()
        if top > 0.5:
            fmt.setTopMargin(top - 0.5 * self.currentFont().pointSize())
        if bottom > 0.5:
            fmt.setBottomMargin(bottom - 0.5 * self.currentFont().pointSize())
        loc.mergeBlockFormat(fmt)

    def text_size(self, size):
        "lettergrootte instellen"
        pointsize = float(size)
        if pointsize > 0:
            fmt = gui.QTextCharFormat()
            fmt.setFontPointSize(pointsize)
            self.setTabStopWidth(shared.tabsize(pointsize))
            self.mergeCurrentCharFormat(fmt)
            self.setFocus()

    def charformat_changed(self, format):
        "wordt aangeroepen als het tekstformat gewijzigd is"
        self.font_changed(format.font())

    def cursorposition_changed(self):
        "wordt aangeroepen als de cursorpositie gewijzigd is"
        pass  # self.alignment_changed(self.alignment())

    def font_changed(self, font):
        """fontgegevens aanpassen

        de selectie in de comboboxen wordt aangepast, de van toepassing zijnde
        menuopties worden aangevinkt, en en de betreffende toolbaricons worden
        geaccentueerd"""
        self.tbparent.combo_font.setCurrentIndex(
            self.tbparent.combo_font.findText(gui.QFontInfo(font).family()))
        self.tbparent.combo_size.setCurrentIndex(
            self.tbparent.combo_size.findText(str(font.pointSize())))
        self.tbparent.actiondict["&Bold"].setChecked(font.bold())
        self.tbparent.actiondict["&Italic"].setChecked(font.italic())
        self.tbparent.actiondict["&Underline"].setChecked(font.underline())
        self.tbparent.actiondict["Strike&through"].setChecked(font.strikeOut())

    def mergeCurrentCharFormat(self, format):
        "de geselecteerde tekst op de juiste manier weergeven"
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.select(gui.QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)
        qtw.QTextEdit.mergeCurrentCharFormat(self, format)

    def _check_dirty(self):
        "check for modifications"
        return self.document().isModified()

    def _mark_dirty(self, value):
        "manually turn modified flag on/off (mainly intended for off)"
        self.document().setModified(value)

    def _openup(self, value):
        "make text accessible (or not)"
        self.setReadOnly(not value)


class PageGui(qtw.QFrame):
    "base class for notebook page"
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        super().__init__(parent)
        if not self.master.is_text_page:
            return
        self.actiondict = collections.OrderedDict()
        self.create_toolbar()
        self.create_text_field(self.master.pageno)
        self.save_button = qtw.QPushButton('Sla wijzigingen op (Ctrl-S)', self)
        self.save_button.clicked.connect(self.savep)
        action = qtw.QShortcut('Ctrl+S', self, self.savep)
        self.saveandgo_button = qtw.QPushButton('Sla op en ga verder (Ctrl-G)', self)
        self.saveandgo_button.clicked.connect(self.savepgo)
        action = qtw.QShortcut('Ctrl+G', self, self.savepgo)
        self.cancel_button = qtw.QPushButton('Zet originele tekst terug (Alt-Ctrl-Z)',
                                             self)
        self.cancel_button.clicked.connect(self.restorep)
        action = qtw.QShortcut('Alt+Ctrl+Z', self, self.restorep)  # Ctrl-Z zit al in text control
        action = qtw.QShortcut('Alt+N', self, self.nieuwp)

    def create_toolbar(self):
        """build toolbar wih buttons for changing text style
        """
        toolbar = qtw.QToolBar('styles')
        toolbar.setIconSize(core.QSize(16, 16))
        self.combo_font = qtw.QFontComboBox(toolbar)
        toolbar.addWidget(self.combo_font)
        self.combo_size = qtw.QComboBox(toolbar)
        toolbar.addWidget(self.combo_size)
        self.combo_size.setEditable(True)
        db = gui.QFontDatabase()
        self.fontsizes = []
        for size in db.standardSizes():
            self.combo_size.addItem(str(size))
            self.fontsizes.append(str(size))
        toolbar.addSeparator()

        data = (
            ('&Bold', 'Ctrl+B', 'icons/sc_bold', 'CheckB'),
            ('&Italic', 'Ctrl+I', 'icons/sc_italic', 'CheckI'),
            ('&Underline', 'Ctrl+U', 'icons/sc_underline', 'CheckU'),
            ('Strike&through', 'Ctrl+~', 'icons/sc_strikethrough.png', 'CheckS'),
            ## ("Toggle &Monospace", 'Shift+Ctrl+M', 'icons/text',
            ##     'Switch using proportional font off/on'),
            (),
            ("&Enlarge text", 'Ctrl+Up', 'icons/sc_grow', 'Use bigger letters'),
            ("&Shrink text", 'Ctrl+Down', 'icons/sc_shrink', 'Use smaller letters'),
            (),
            ('To &Lower Case', 'Shift+Ctrl+L', 'icons/sc_changecasetolower',
             'Use all lower case letters'),
            ('To &Upper Case', 'Shift+Ctrl+U', 'icons/sc_changecasetoupper',
             'Use all upper case letters'),
            (),
            ("Indent &More", 'Ctrl+]', 'icons/sc_incrementindent',
             'Increase indentation'),
            ("Indent &Less", 'Ctrl+[', 'icons/sc_decrementindent',
             'Decrease indentation'),
            (),
            ## ("Normal Line Spacing", '', 'icons/sc_spacepara1',
            ##     'Set line spacing to 1'),
            ## ("1.5 Line Spacing",    '', 'icons/sc_spacepara15',
            ##     'Set line spacing to 1.5'),
            ## ("Double Line Spacing", '', 'icons/sc_spacepara2',
            ##     'Set line spacing to 2'),
            ## (),
            ("Increase Paragraph &Spacing", '', 'icons/sc_paraspaceincrease',
             'Increase spacing between paragraphs'),
            ("Decrease &Paragraph Spacing", '', 'icons/sc_paraspacedecrease',
             'Decrease spacing between paragraphs'))
        for menudef in data:
            if not menudef:
                toolbar.addSeparator()
                continue
            label, shortcut, icon, info = menudef
            if icon:
                action = qtw.QAction(gui.QIcon(os.path.join(HERE, icon)), label, self)
                toolbar.addAction(action)
            else:
                action = qtw.QAction(label, self)
            if shortcut:
                action.setShortcuts([x for x in shortcut.split(",")])
            if info.startswith("Check"):
                action.setCheckable(True)
                info = info[5:]
                if info in ('B', 'I', 'U', 'S'):
                    font = gui.QFont()
                    if info == 'B':
                        font.setBold(True)
                    elif info == 'I':
                        font.setItalic(True)
                    elif info == 'U':
                        font.setUnderline(True)
                    elif info == 'S':
                        font.setStrikeOut(True)
                    action.setFont(font)
            self.actiondict[label] = action
        self.toolbar = toolbar

    def create_text_field(self, pageno):
        """build rich text area with style changing properties
        """
        high = 330 if LIN else 430
        self.text1 = EditorPanel(self)
        self.text1.resize(490, high)
        self.text1.textChanged.connect(self.on_text)
        for action, callback in zip(self.actiondict.values(), [
                self.text1.text_bold,
                self.text1.text_italic,
                self.text1.text_underline,
                self.text1.text_strikethrough,
                ## self.text1.toggle_monospace,
                self.text1.enlarge_text,
                self.text1.shrink_text,
                self.text1.case_lower,
                self.text1.case_upper,
                self.text1.indent_more,
                self.text1.indent_less,
                self.text1.linespacing_1,
                self.text1.linespacing_15,
                self.text1.linespacing_2,
                self.text1.increase_paragraph_spacing,
                self.text1.decrease_paragraph_spacing]):
            action.triggered.connect(callback)
        self.combo_font.activated[str].connect(self.text1.text_family)
        self.combo_size.activated[str].connect(self.text1.text_size)
        self.text1.font_changed(self.text1.font())

    def doelayout(self):
        "layout page"
        sizer0 = qtw.QVBoxLayout()
        sizer1 = qtw.QVBoxLayout()
        sizer1.addWidget(self.toolbar)
        sizer0.addLayout(sizer1)
        sizer1 = qtw.QVBoxLayout()
        sizer1.addWidget(self.text1)
        sizer0.addLayout(sizer1)
        sizer2 = qtw.QHBoxLayout()
        sizer2.addStretch()
        sizer2.addWidget(self.save_button)
        sizer2.addWidget(self.saveandgo_button)
        sizer2.addWidget(self.cancel_button)
        sizer2.addStretch()
        sizer0.addLayout(sizer2)
        self.setLayout(sizer0)
        return True

    def vulp(self):
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina"""
        self.initializing = True
        self.parent.parent.settingsmenu.setEnabled(self.parent.parent.is_admin)
        if self.parent.current_tab == 0:
            text = self.seltitel
        else:
            self.enable_buttons(False)
            text = self.parent.tabs[self.parent.current_tab].split(None, 1)
            if self.parent.pagedata:
                text = str(self.parent.pagedata.id) + ' ' + self.parent.pagedata.titel
        self.parent.parent.setWindowTitle("{} | {}".format(self.parent.parent.title, text))
        self.parent.parent.set_statusmessage()
        if 1 < self.parent.current_tab < 6:
            self.oldbuf = ''
            if self.parent.pagedata is not None:
                if self.parent.current_tab == 2 and self.parent.pagedata.melding:
                    self.oldbuf = self.parent.pagedata.melding
                if self.parent.current_tab == 3 and self.parent.pagedata.oorzaak:
                    self.oldbuf = self.parent.pagedata.oorzaak
                if self.parent.current_tab == 4 and self.parent.pagedata.oplossing:
                    self.oldbuf = self.parent.pagedata.oplossing
                if self.parent.current_tab == 5 and self.parent.pagedata.vervolg:
                    self.oldbuf = self.parent.pagedata.vervolg
                self.text1.setReadOnly(self.parent.pagedata.arch)
            self.text1.set_contents(self.oldbuf)
            self.text1.setReadOnly(not self.parent.parent.is_user)
            self.toolbar.setEnabled(self.parent.parent.is_user)
            self.oldbuf = self.text1.get_contents()  # make sure it's rich text
        self.initializing = False
        self.parent.checked_for_leaving = True

    def savep(self):
        "gegevens van een actie opslaan afhankelijk van pagina"
        if not self.save_button.isEnabled():
            return False
        self.enable_buttons(False)
        if self.parent.current_tab <= 1 or self.parent.current_tab == 6:
            return False
        wijzig = False
        text = self.text1.get_contents()
        if self.parent.current_tab == 2 and text != self.parent.pagedata.melding:
            self.oldbuf = self.parent.pagedata.melding = text
            self.parent.pagedata.events.append((shared.get_dts(), "Meldingtekst aangepast"))
            wijzig = True
        if self.parent.current_tab == 3 and text != self.parent.pagedata.oorzaak:
            self.oldbuf = self.parent.pagedata.oorzaak = text
            self.parent.pagedata.events.append((shared.get_dts(), "Beschrijving oorzaak aangepast"))
            wijzig = True
        if self.parent.current_tab == 4 and text != self.parent.pagedata.oplossing:
            self.oldbuf = self.parent.pagedata.oplossing = text
            self.parent.pagedata.events.append((shared.get_dts(), "Beschrijving oplossing aangepast"))
            wijzig = True
        if self.parent.current_tab == 5 and text != self.parent.pagedata.vervolg:
            self.oldbuf = self.parent.pagedata.vervolg = text
            self.parent.pagedata.events.append((shared.get_dts(), "Tekst vervolgactie aangepast"))
            wijzig = True
        if wijzig:
            self.update_actie()
            self.parent.page0.p0list.currentItem().setText(3, self.parent.pagedata.updated)
        return True

    def restorep(self):
        "oorspronkelijke (laatst opgeslagen) inhoud van de pagina herstellen"
        # reset font - are these also needed: case? indent? linespacing? paragraphspacing?
        if self.parent.current_tab > 1:
            if self.parent.current_tab == 6:
                win = self.progress_text
            else:
                win = self.text1
        win.setFontWeight(gui.QFont.Normal)
        win.setFontItalic(False)
        win.setFontUnderline(False)
        win.setFontFamily(win.defaultfamily)
        win.setFontPointSize(win.defaultsize)
        self.vulp()

    def on_text(self):
        """callback voor EVT_TEXT

        de initializing flag wordt uitgevraagd omdat deze event ook tijdens vulp()
        en tijdens vul_combos plaatsvindt"""
        if not self.initializing:
            newbuf = self.build_newbuf()
            changed = newbuf != self.oldbuf
            self.enable_buttons(changed)

    def build_newbuf(self):
        """read widget contents into the compare buffer
        """
        return self.text1.get_contents()

    def on_choice(self):
        "callback voor combobox"
        self.enable_buttons()

    def enable_buttons(self, state=True):
        "buttons wel of niet bruikbaar maken"
        self.save_button.setEnabled(state)
        if self.parent.current_tab < 6:
            self.saveandgo_button.setEnabled(state)
        self.cancel_button.setEnabled(state)

    def goto_actie(self):
        "naar startpagina actie gaan"
        self.goto_page(1)

    def goto_next(self):
        "naar de volgende pagina gaan"
        if not self.leavep():
            return
        next = self.parent.current_tab + 1
        if next > self.parent.pages:
            next = 0
        self.parent.setCurrentIndex(next)

    def goto_prev(self):
        "naar de vorige pagina gaan"
        if not self.leavep():
            return
        next = self.parent.current_tab - 1
        if next < 0:
            next = self.parent.pages
        self.parent.setCurrentIndex(next)

    def goto_page(self, page_num, check=True):
        "naar de aangegeven pagina gaan"
        if check and not self.leavep():
            return
        if 0 <= page_num <= self.parent.pages:
            self.parent.setCurrentIndex(page_num)

    def get_entry_text(self):
        "get the page text"
        return self.text1.get_contents()

    def set_text_contents(self, data):
        "set the page text"
        self.text1.set_contents(data)

    def get_text_contents(self):
        "get the page text"
        return self.text1.get_contents()

    def enable_toolbar(self, value):
        "make the toolbar accessible (or not)"
        self.toolbar.setEnabled(value)

    def set_text_readonly(self, value):
        "protect page text from updating (or not)"
        self.text1.setReadOnly(value)

    def can_saveandgo(self):
        "check if we are allowed/able to do this"
        return self.saveandgo_button.isEnabled()

    def can_save(self):
        "check if we are allowed/able to do this"
        return self.save_button.isEnabled()


class Page0Gui(PageGui):
    "pagina 0: overzicht acties"
    def __init__(self, parent, master, widths):
        self.parent = parent
        self.master = master
        super().__init__(parent, master)

        self.p0list = qtw.QTreeWidget(self)
        self.sort_button = qtw.QPushButton('S&Orteer', self)
        self.filter_button = qtw.QPushButton('F&Ilter', self)
        self.go_button = qtw.QPushButton('&Ga naar melding', self)
        self.archive_button = qtw.QPushButton('&Archiveer', self)
        self.new_button = qtw.QPushButton('Voer &Nieuwe melding op', self)

        # self.sort_via_options = False
        self.p0list.setSortingEnabled(True)
        self.p0list.setHeaderLabels(self.parent.ctitels)
        self.p0list.setAlternatingRowColors(True)
        self.p0hdr = self.p0list.header()
        self.p0hdr.setSectionsClickable(True)
        for indx, wid in enumerate(widths):
            self.p0hdr.resizeSection(indx, wid)
        self.p0hdr.setStretchLastSection(True)
        self.p0list.itemActivated.connect(self.master.on_activate_item)
        self.p0list.currentItemChanged.connect(self.master.on_change_selected)

        self.sort_button.clicked.connect(self.master.sort_items)
        self.filter_button.clicked.connect(self.master.select_items)
        self.go_button.clicked.connect(self.master.goto_actie)
        self.archive_button.clicked.connect(self.master.archiveer)
        self.new_button.clicked.connect(self.master.nieuwp)

    def doelayout(self):
        "layout page"
        sizer0 = qtw.QVBoxLayout()
        sizer1 = qtw.QHBoxLayout()
        sizer2 = qtw.QHBoxLayout()
        sizer1.addWidget(self.p0list)
        sizer0.addLayout(sizer1)
        sizer2.addStretch()
        sizer2.addWidget(self.sort_button)
        sizer2.addWidget(self.filter_button)
        sizer2.addWidget(self.go_button)
        sizer2.addWidget(self.archive_button)
        sizer2.addWidget(self.new_button)
        sizer2.addStretch()
        sizer0.addLayout(sizer2)
        self.setLayout(sizer0)

    def enable_sorting(self, value):
        "stel in of sorteren mogelijk is"
        self.p0list.setSortingEnabled(value)

    def enable_buttons(self):
        "buttons wel of niet bruikbaar maken"
        self.filter_button.setEnabled(bool(self.parent.parent.user))
        self.go_button.setEnabled(self.p0list.has_selection)
        self.new_button.setEnabled(self.parent.parent.is_user)
        if self.p0list.has_selection:
            self.sort_button.setEnabled(bool(self.parent.parent.user))
            self.archive_button.setEnabled(self.parent.parent.is_user)
        else:
            self.sort_button.setEnabled(False)
            self.archive_button.setEnabled(False)

    def clear_list(self):
        "initialize the list"
        self.p0list.clear()
        self.p0list.has_selection = False

    def set_listitem_values(self, data):
        "set column values for list entry"
        new_item = qtw.QTreeWidgetItem()
        for col, value in enumerate(data):
            if col == 1:
                pos = value.index(".") + 1
                value = value[pos:pos + 1].upper()
            elif col == 2:
                pos = value.index(".") + 1
                value = value[pos:]
            new_item.setText(col, value)
        new_item.setData(0, core.Qt.UserRole, data[0])
        self.p0list.addTopLevelItem(new_item)
        self.p0list.has_selection = True

    def get_items(self):
        "retrieve all listitems"
        return [self.p0list.topLevelItem(i) for i in range(self.p0list.topLevelItemCount())]

    def get_item_text(self, item_or_index, column):
        "get the item's text for a specified column"
        return item_or_index.text(column)

    def set_item_text(self, item_or_index, column, text):
        "set the item's text for a specified column"
        item_or_index.setText(column, text)

    def get_first_item(self):
        "select the first item in the list"
        return self.p0list.topLevelItem(0)

    def has_selection(self):
        "return if list contains selection of data"
        return self.p0list.has_selection

    def set_selection(self):
        "set selected item if any"
        if self.parent.current_item is not None:
            self.p0list.setCurrentItem(self.parent.current_item)

    def get_selection(self):
        "get selected item"
        return self.p0list.currentItem()

    def ensure_visible(self, item):
        "make sure listitem is visible"
        self.p0list.scrollToItem(item)

    def build_newbuf(self):
        """read widget contents into the compare buffer
        """
        return None

    def set_archive_button_text(self, txt):
        "set button text according to archive status"
        self.archive_button.setText(txt)


class Page1Gui(PageGui):
    "pagina 1: startscherm actie"
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        super().__init__(parent, master)

        self.id_text = qtw.QLineEdit(self)
        self.id_text.setMaximumWidth(120)
        self.date_text = qtw.QLineEdit(self)
        self.date_text.setMaximumWidth(150)

        self.proc_entry = qtw.QLineEdit(self)
        self.proc_entry.setMaximumWidth(150)
        self.proc_entry.textChanged.connect(self.master.on_text)
        self.desc_entry = qtw.QLineEdit(self)
        self.desc_entry.setMaximumWidth(360)
        self.desc_entry.textChanged.connect(self.master.on_text)

        self.cat_choice = qtw.QComboBox(self)
        self.cat_choice.setEditable(False)
        self.cat_choice.setMaximumWidth(180)
        self.cat_choice.currentIndexChanged.connect(self.master.on_text)
        self.stat_choice = qtw.QComboBox(self)
        self.stat_choice.setEditable(False)
        self.id_text.setMaximumWidth(140)
        self.stat_choice.currentIndexChanged.connect(self.master.on_text)

        self.archive_text = qtw.QLabel(self)
        self.archive_button = qtw.QPushButton("Archiveren", self)
        self.archive_button.clicked.connect(self.master.archiveer)

        self.save_button = qtw.QPushButton('Sla wijzigingen op (Ctrl-S)', self)
        self.save_button.clicked.connect(self.master.savep)
        action = qtw.QShortcut('Ctrl+S', self, self.master.savep)
        self.saveandgo_button = qtw.QPushButton('Sla op en ga verder (Ctrl-G)', self)
        self.saveandgo_button.clicked.connect(self.master.savepgo)
        action = qtw.QShortcut('Ctrl+G', self, self.master.savepgo)
        self.cancel_button = qtw.QPushButton('Maak wijzigingen ongedaan (Alt-Ctrl-Z)', self)
        self.cancel_button.clicked.connect(self.master.restorep)
        action = qtw.QShortcut('Alt+Ctrl+Z', self, self.master.restorep)  # Ctrl-Z is al op
        action = qtw.QShortcut('Alt+N', self, self.master.nieuwp)

    def doelayout(self):
        "layout page"
        sizer0 = qtw.QVBoxLayout()
        sizer0.addSpacing(10)

        sizerx = qtw.QHBoxLayout()
        sizerx.addSpacing(10)

        sizer1 = qtw.QGridLayout()
        row = 0
        sizer1.setRowMinimumHeight(row, 10)
        sizer1.setColumnStretch(2, 1)
        row += 1
        sizer1.addWidget(qtw.QLabel("Actie-id:", self), row, 0)
        sizer1.addWidget(self.id_text, row, 1)
        row += 1
        sizer1.setRowMinimumHeight(row, 5)
        row += 1
        sizer1.addWidget(qtw.QLabel("Datum/tijd:", self), row, 0)
        sizer1.addWidget(self.date_text, row, 1)
        row += 1
        sizer1.setRowMinimumHeight(row, 5)
        row += 1
        sizer1.addWidget(qtw.QLabel("Job/\ntransactie:", self), row, 0)
        sizer1.addWidget(self.proc_entry, row, 1)
        row += 1
        sizer1.setRowMinimumHeight(row, 5)
        row += 1
        sizer1.addWidget(qtw.QLabel("Melding/code/\nomschrijving:", self), row, 0)
        sizer1.addWidget(self.desc_entry, row, 1, 1, 2)
        row += 1
        sizer1.setRowMinimumHeight(row, 5)
        row += 1
        sizer1.addWidget(qtw.QLabel("Categorie:", self), row, 0)
        sizer1.addWidget(self.cat_choice, row, 1)
        row += 1
        sizer1.setRowMinimumHeight(row, 5)
        row += 1
        sizer1.addWidget(qtw.QLabel("Status:", self), row, 0)
        sizer1.addWidget(self.stat_choice, row, 1)
        row += 1
        sizer1.setRowMinimumHeight(row, 5)
        row += 1
        sizery = qtw.QHBoxLayout()
        sizery.addWidget(self.archive_text)
        sizery.addStretch()
        sizer1.addLayout(sizery, row, 1)
        row += 1
        sizery = qtw.QHBoxLayout()
        sizery.addWidget(self.archive_button)
        sizery.addStretch()
        sizer1.addLayout(sizery, row, 1)

        sizerx.addLayout(sizer1)

        sizer0.addLayout(sizerx)

        sizer0.addStretch()

        sizer2 = qtw.QHBoxLayout()
        sizer2.addStretch()
        sizer2.addWidget(self.save_button)
        sizer2.addWidget(self.saveandgo_button)
        sizer2.addWidget(self.cancel_button)
        sizer2.addStretch()
        sizer0.addLayout(sizer2)

        self.setLayout(sizer0)

    def init_fields(self):
        "initialize the fields on this screen"
        self.id_text.clear()
        self.date_text.clear()
        self.proc_entry.clear()
        self.desc_entry.clear()
        self.archive_text.setText("")
        self.cat_choice.setCurrentIndex(0)
        self.stat_choice.setCurrentIndex(0)

    def set_text(self, fieldtype, value):
        "set textfield value"
        if fieldtype == 'id':
            self.id_text.setText(value)
        elif fieldtype == 'date':
            self.date_text.setText(value)
        elif fieldtype == 'proc':
            self.proc_entry.setText(value)
        elif fieldtype == 'desc':
            self.desc_entry.setText(value)
        elif fieldtype == 'arch':
            self.archive_text.setText(value)

    def get_text(self, fieldtype):
        "get textfield value"
        if fieldtype == 'id':
            value = str(self.id_text.text())
        elif fieldtype == 'date':
            value = str(self.date_text.text())
        elif fieldtype == 'proc':
            value = str(self.proc_entry.text())
        elif fieldtype == 'desc':
            value = str(self.desc_entry.text())
        return value

    # TODO: een van deze beiden kiezen
    def get_entry_text(self, entry_type):
        if entry_type == 'actie':
            return self.id_text.text()
        elif entry_type == 'datum':
            return self.date_text.text()
        elif entry_type == 'oms':
            return self.proc_entry.text()
        elif entry_type == 'tekst':
            return self.desc_entry.text()
        elif entry_type == 'soort':
            return self.cat_choice.currentText()
        elif entry_type == 'status':
            return self.stat_choice.currentText()
        return None

    def vul_combos(self):
        "vullen comboboxen"
        self.initializing = True
        self.stat_choice.clear()
        self.cat_choice.clear()
        for key in sorted(self.parent.cats.keys()):
            text, value = self.parent.cats[key][:2]
            self.cat_choice.addItem(text, value)
        for key in sorted(self.parent.stats.keys()):
            text, value = self.parent.stats[key][:2]
            self.stat_choice.addItem(text, value)
        self.initializing = False

    # TODO een van deze beiden kiezen oid
    def set_choice(self, fieldtype, value):
        "set selected entry in a combobox"
        if fieldtype == 'stat':
            domain = self.parent.stats
            field = self.stat_choice
        elif fieldtype == 'cat':
            domain = self.parent.cats
            field = self.cat_choice
        for x in range(len(domain)):
            y = shared.data2str(field.itemData(x))
            if y == value:
                field.setCurrentIndex(x)
                break

    def get_choice_data(self, fieldtype):
        "get selected entry in a combobox"
        if fieldtype == 'stat':
            idx = self.stat_choice.currentIndex()
            # newstat = shared.data2str(self.stat_choice.itemData(idx))  # xml versie?
            indx = shared.data2int(self.stat_choice.itemData(idx))
            sel = self.stat_choice.currentText()
        elif fieldcat == 'cat':
            idx = self.cat_choice.currentIndex()
            indx = shared.data2str(self.cat_choice.itemData(idx))
            sel = str(self.cat_choice.currentText())
        return indx, text

    def set_oldbuf(self):
        "get fieldvalues for comparison of entry was changed"
        return (str(self.proc_entry.text()), str(self.desc_entry.text()),
                int(self.stat_choice.currentIndex()), int(self.cat_choice.currentIndex()))

    def set_archive_button_text(self, value):
        "set the text for the archive button"
        self.archive_button.setText(value)

    def enable_fields(self, state):
        "make fields accessible, depending on user permissions"
        self.id_text.setEnabled(False)
        self.date_text.setEnabled(False)
        self.proc_entry.setEnabled(state)
        self.desc_entry.setEnabled(state)
        self.cat_choice.setEnabled(state)
        self.stat_choice.setEnabled(state)
        if self.master.parent.newitem or not self.master.parent.parent.is_user:
            self.archive_button.setEnabled(False)
        else:
            self.archive_button.setEnabled(True)

    def clear_stats(self):
        "initialize status choices"
        self.stat_choice.clear()

    def clear_cats(self):
        "initialize category choices"
        self.cat_choice.clear()

    def add_cat_choice(self, text, value):
        "add category choice"
        self.cat_choice.addItem(text, value)

    def add_stat_choice(self, text, value):
        "add status choice"
        self.stat_choice.addItem(text, value)

    def set_focus(self):
        "set the focus for this page to the proc field"
        self.proc_entry.setFocus()

    def build_newbuf(self):
        """read widget contents into the compare buffer
        """
        return (str(self.proc_entry.text()), str(self.desc_entry.text()),
                int(self.stat_choice.currentIndex()), int(self.cat_choice.currentIndex()))


class Page6Gui(PageGui):
    "pagina 6: voortgang"
    def __init__(self, parent):
        PageGui.__init__(self, parent, pageno=6, standard=False)
        self.current_item = 0
        self.oldtext = ""
        ## sizes = 200, 100 if LIN else 280, 110
        sizes = 350, 100 if LIN else 280, 110
        self.pnl = qtw.QSplitter(self)
        self.pnl.setOrientation(core.Qt.Vertical)

        self.progress_list = qtw.QListWidget(self)
        self.progress_list.currentItemChanged.connect(self.on_select_item)
        self.new_action = qtw.QShortcut('Shift+Ctrl+N', self)
        if self.parent.parent.datatype == shared.DataType.XML.name:
            self.progress_list.itemActivated.connect(self.on_activate_item)
            # action = qtw.QShortcut('Shift+Ctrl+N', self, functools.partial(
            #     self.on_activate_item, self.progress_list.item(0)))
            self.new_action.activated.connect(functools.partial(self.on_activate_item,
                                                                self.progress_list.item(0)))
        textpanel = qtw.QFrame(self)
        self.actiondict = collections.OrderedDict()
        Page.create_toolbar(self)
        Page.create_text_field(self, 6)
        self.progress_text = self.text1  # to save modifying all references (TODO: fix - why?)
        sizer0 = qtw.QHBoxLayout()
        sizer1 = qtw.QVBoxLayout()
        sizer1.addWidget(self.toolbar)
        sizer1.addWidget(self.progress_text)
        sizer0.addLayout(sizer1)
        textpanel.setLayout(sizer0)
        textpanel.show()
        self.pnl.addWidget(self.progress_list)
        self.pnl.addWidget(textpanel)
        self.pnl.setSizes(sizes)
        self.save_button = qtw.QPushButton('Sla wijzigingen op (Ctrl-S)', self)
        self.save_button.clicked.connect(self.savep)
        action = qtw.QShortcut('Ctrl+S', self, self.savep)
        self.cancel_button = qtw.QPushButton('Maak wijzigingen ongedaan (Alt-Ctrl-Z)',
                                             self)
        self.cancel_button.clicked.connect(self.restorep)
        action = qtw.QShortcut('Alt+Ctrl+Z', self, self.restorep)  # Ctrl-Z zit al in text control
        action = qtw.QShortcut('Shift+Ctrl+Up', self, self.goto_prev)
        action = qtw.QShortcut('Shift+Ctrl+Down', self, self.goto_next)

    def doelayout(self):
        "layout page"
        sizer0 = qtw.QVBoxLayout()
        sizer1 = qtw.QHBoxLayout()
        sizer1.addWidget(self.pnl)
        sizer0.addLayout(sizer1)
        sizer2 = qtw.QHBoxLayout()
        sizer2.addStretch()
        sizer2.addWidget(self.save_button)
        sizer2.addWidget(self.cancel_button)
        sizer2.addStretch()
        sizer0.addLayout(sizer2)
        self.setLayout(sizer0)

    def vulp(self):
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina"""
        Page.vulp(self)
        self.initializing = True
        self.event_list, self.event_data, self.old_list, self.old_data = [], [], [], []
        self.progress_text.clear()
        self.progress_text.setReadOnly(True)
        if self.parent.pagedata:
            self.event_list = [x[0] for x in self.parent.pagedata.events]
            self.event_list.reverse()
            self.old_list = self.event_list[:]
            self.event_data = [x[1] for x in self.parent.pagedata.events]
            self.event_data.reverse()
            self.old_data = self.event_data[:]
            self.progress_list.clear()
            if self.parent.parent.is_user:
                text = '-- doubleclick or press Shift-Ctrl-N to add new item --'
            else:
                text = '-- adding new items is disabled --'
            first_item = qtw.QListWidgetItem(text)
            first_item.setData(core.Qt.UserRole, -1)
            self.progress_list.addItem(first_item)
            for idx, datum in enumerate(self.event_list):
                # convert to HTML (if needed) and back
                self.progress_text.set_contents(self.event_data[idx])
                tekst_plat = self.progress_text.toPlainText()
                try:
                    text = tekst_plat.split("\n")[0].strip()
                except AttributeError:
                    text = tekst_plat or ""
                text = text if len(text) < 80 else text[:80] + "..."
                newitem = qtw.QListWidgetItem('{} - {}'.format(datum, text))
                newitem.setData(core.Qt.UserRole, idx)
                self.progress_list.addItem(newitem)
        if self.parent.parent.datatype == shared.DataType.SQL.name:
            if self.parent.parent.is_user:
                self.progress_list.itemActivated.connect(self.on_activate_item)
                # action = qtw.QShortcut('Shift+Ctrl+N', self, functools.partial(
                #     self.on_activate_item, self.progress_list.item(0)))
                self.new_action.activated.connect(functools.partial(self.on_activate_item,
                                                                    self.progress_list.item(0)))
            else:
                try:
                    self.progress_list.itemActivated.disconnect()
                    self.new_action.activated.disconnect()
                except TypeError:
                    # avoid "disconnect() failed between 'itemActivated' and all its connections"
                    pass
        self.progress_text.clear()
        self.oldbuf = (self.old_list, self.old_data)
        self.oldtext = ''
        self.initializing = False

    def savep(self):
        "opslaan van de paginagegevens"
        Page.savep(self)
        # voor het geval er na het aanpassen van een tekst direkt "sla op" gekozen is
        # nog even kijken of de tekst al in self.event_data is aangepast.
        idx = self.current_item
        hlp = str(self.progress_text.get_contents())
        if idx > 0:
            idx -= 1
        if self.event_data[idx] != hlp:
            self.event_data[idx] = hlp
            self.oldtext = hlp
            short_text = hlp.split("\n")[0]
            if len(short_text) < 80:
                short_text = short_text[:80] + "..."
            if self.parent.parent.datatype == shared.DataType.XML.name:
                short_text = short_text.encode('latin-1')
            self.progress_list.item(idx + 1).setText("{} - {}".format(
                self.event_list[idx], short_text))
            self.progress_list.item(idx + 1).setData(idx, core.Qt.UserRole)
        wijzig = False
        if self.event_list != self.old_list or self.event_data != self.old_data:
            wijzig = True
            hlp = len(self.event_list) - 1
            for idx, data in enumerate(self.parent.pagedata.events):
                if data != (self.event_list[hlp - idx], self.event_data[hlp - idx]):
                    self.parent.pagedata.events[idx] = (self.event_list[hlp - idx],
                                                        self.event_data[hlp - idx])
            for idx in range(len(self.parent.pagedata.events), hlp + 1):
                if self.event_data[hlp - idx]:
                    self.parent.pagedata.events.append((self.event_list[hlp - idx],
                                                        self.event_data[hlp - idx]))
        if wijzig:
            self.update_actie()
            self.parent.current_item.setText(4, self.parent.pagedata.updated)
            self.parent.page0.p0list.currentItem().setText(
                3, self.parent.pagedata.updated)
            self.old_list = self.event_list[:]
            self.old_data = self.event_data[:]
            self.oldbuf = (self.old_list, self.old_data)
        else:
            print("Leuk hoor, er was niks gewijzigd ! @#%&*Grrr")
        return True

    def goto_prev(self):
        test = self.progress_list.currentRow() - 1
        if test > 0:
            self.progress_list.setCurrentRow(test)

    def goto_next(self):
        test = self.progress_list.currentRow() + 1
        if test < self.progress_list.count():
            self.progress_list.setCurrentRow(test)

    def on_activate_item(self, item=None):
        """callback voor dubbelklik of Enter op een item

        wanneer dit gebeurt op het eerste item kan een nieuwe worden aangemaakt
        """
        if self.initializing:
            return
        if item is None or shared.data2int(item.data(core.Qt.UserRole)) == -1:
            datum, self.oldtext = shared.get_dts(), ''
            newitem = qtw.QListWidgetItem('{} - {}'.format(datum, self.oldtext))
            newitem.setData(core.Qt.UserRole, 0)
            self.progress_list.insertItem(1, newitem)
            self.event_list.insert(0, datum)
            self.event_data.insert(0, self.oldtext)
            self.progress_list.setCurrentRow(1)
            self.progress_text.setText(self.oldtext)
            self.progress_text.setReadOnly(False)
            self.progress_text.setFocus()

    def on_select_item(self, item_n, item_o):
        """callback voor het selecteren van een item

        selecteren van (klikken op) een regel in de listbox doet de inhoud van de
        textctrl ook veranderen. eerst controleren of de tekst veranderd is
        dat vragen moet ook in de situatie dat je op een geactiveerde knop klikt,
        het panel wilt verlaten of afsluiten
        de knoppen onderaan doen de hele lijst bijwerken in self.parent.book.p
        """
        self.progress_text.setReadOnly(True)
        if item_n is None:
            # als ik al eens eerder op page 6 geweest ben en er terugkom of bij reset
            return
        self.current_item = self.progress_list.currentRow()
        indx = self.current_item - 1
        if indx == -1:
            self.oldtext = ""
        else:
            self.oldtext = self.event_data[indx]  # dan wel item_n.text()
        self.initializing = True
        self.progress_text.set_contents(self.oldtext)
        self.oldtext = self.progress_text.get_contents()
        self.initializing = False
        if not self.parent.pagedata.arch:
            if indx > -1:
                self.progress_text.setReadOnly(not self.parent.parent.is_user)
                self.toolbar.setEnabled(self.parent.parent.is_user)
            self.progress_text.moveCursor(gui.QTextCursor.End,
                                          gui.QTextCursor.MoveAnchor)
        self.progress_text.setFocus()

    def on_text(self):
        """callback voor wanneer de tekst gewijzigd is

        de initializing flag wordt uitgevraagd omdat deze event ook tijdens vulp()
        en wijzigen van list positie plaatsvindt
        """
        if self.initializing:
            return
        # lees de inhoud van het tekstveld en vergelijk deze met de buffer
        tekst = str(self.progress_text.get_contents())  # self.progress_list.GetItemText(ix)
        if tekst != self.oldtext:
            # stel de buffer in op de nieuwe tekst
            self.oldtext = tekst
            # maak er platte tekst van om straks in de listbox bij te werken
            tekst_plat = self.progress_text.toPlainText()
            # stel in dat we niet van dit scherm af kunnen zonder te updaten
            if self.parent.parent.is_user:
                self.enable_buttons()
            self.current_item = self.progress_list.currentRow()
            if self.current_item > 0:
                indx = self.current_item - 1
                self.event_data[indx] = tekst
                item = self.progress_list.currentItem()
                datum = str(item.text()).split(' - ')[0]
                short_text = ' - '.join((datum, tekst_plat.split("\n")[0]))
                if len(short_text) >= 80:
                    short_text = short_text[:80] + "..."
                item.setText(short_text)

    def build_newbuf(self):
        """read widget contents into the compare buffer
        """
        return (self.event_list, self.event_data)


class SortOptionsDialog(qtw.QDialog):
    """dialoog om de sorteer opties in te stellen
    """
    _asc_id = 1
    _desc_id = 2

    def __init__(self, parent, args):
        self.parent = parent

        self.sortopts, lijst = args
        super().__init__(parent)
        self.setWindowTitle("Sorteren op meer dan 1 kolom")

        sizer = qtw.QVBoxLayout()
        grid = qtw.QGridLayout()
        row = 0
        tekst = 'Multi-sorteren mogelijk maken'
        ## tekst = 'Sorteren via instellingen ipv. via control'
        self.on_off = qtw.QCheckBox(tekst, self)
        self.on_off.stateChanged.connect(self.enable_fields)
        grid.addWidget(self.on_off, row, 0, 1, 4)
        self._widgets = []
        row += 1
        while row < len(lijst):
            lbl = qtw.QLabel("  {}.".format(row), self)
            grid.addWidget(lbl, row, 0)
            cmb = qtw.QComboBox(self)
            cmb.setEditable(False)
            cmb.addItems(lijst)
            cmb.setCurrentIndex(0)
            grid.addWidget(cmb, row, self._asc_id)
            rbg = qtw.QButtonGroup(self)
            rba = qtw.QRadioButton(" Asc ", self)
            rbg.addButton(rba, 1)
            grid.addWidget(rba, row, self._desc_id)
            rbd = qtw.QRadioButton(" Desc ", self)
            rbg.addButton(rbd, 2)
            rbg.button(self._asc_id).setChecked(True)
            grid.addWidget(rbd, row, 3)
            self._widgets.append((lbl, cmb, rbg))
            row += 1

        sizer.addLayout(grid)

        buttonbox = qtw.QDialogButtonBox(qtw.QDialogButtonBox.Ok |
                                         qtw.QDialogButtonBox.Cancel)
        sizer.addWidget(buttonbox)
        self.setLayout(sizer)

        self.set_defaults()

        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)

    def set_defaults(self):
        """set atart values for dialog
        """
        self.enable_fields(False)
        self.on_off.setChecked(self.parent.master.sort_via_options)
        for ix, line in enumerate(self._widgets):
            _, combobox, rbgroup = line
            if ix in sorted(self.sortopts):
                fieldname, orient = self.sortopts[ix]
                combobox.setCurrentText(fieldname)
                if orient == 'desc':
                    rbgroup.button(self._desc_id).setChecked(True)
                else:
                    rbgroup.button(self._asc_id).setChecked(True)

    def enable_fields(self, state):
        "enable/disable widgets"
        for lbl, cmb, rbg in self._widgets:
            lbl.setEnabled(state)
            cmb.setEnabled(state)
            for btn in rbg.buttons():
                btn.setEnabled(state)

    def accept(self):
        """sorteerkolommen en -volgordes teruggeven aan hoofdscherm
        """
        if self.parent.parent.parent.datatype == shared.DataType.XML.name:
            qtw.QMessageBox.information(self, 'Probreg', 'Sorry, werkt nog niet')
            return
        new_sortopts = {}
        for ix, line in enumerate(self._widgets):
            _, combobox, rbgroup = line
            fieldname = combobox.currentText()
            checked_id = rbgroup.checkedId()
            if fieldname and fieldname != '(geen)':
                if checked_id == self._asc_id:
                    orient = 'asc'
                elif checked_id == self._desc_id:
                    orient = 'desc'
                new_sortopts[ix] = (fieldname, orient)
        via_options = self.on_off.isChecked()
        if via_options == self.parent.master.sort_via_options and new_sortopts == self.sortopts:
            qtw.QMessageBox.information(self, 'Probreg', 'U heeft niets gewijzigd')
            return
        self.parent.master.sort_via_options = via_options
        if via_options:
            if self.parent._data:      # alleen SQL versie
                self.parent._data.save_options(new_sortopts)
        super().accept()


class SelectOptionsDialog(qtw.QDialog):
    """dialoog om de selectie op te geven

    sel_args is de dictionary waarin de filterwaarden zitten, bv:
    {'status': ['probleem'], 'idlt': '2006-0009', 'titel': 'x', 'soort': ['gemeld'],
     'id': 'and', 'idgt': '2005-0019'}
    voor de Django versie is deze overbodig want de selectie ligt vast in de database
    """
    def __init__(self, parent, args):
        self.parent = parent
        self.datatype = self.parent.parent.parent.datatype
        sel_args, self._data = args
        super().__init__(parent)
        self.setWindowTitle("Selecteren")

        self.check_options = qtw.QButtonGroup()
        self.check_options.setExclusive(False)

        self.check_options.addButton(qtw.QCheckBox(parent.parent.ctitels[0] +
                                                   '   -', self))
        self.text_gt = qtw.QLineEdit(self)
        self.text_gt.textChanged.connect(functools.partial(self.on_text, 'gt'))
        self.radio_id = qtw.QButtonGroup(self)
        for text in ('en', 'of'):
            radio = qtw.QRadioButton(text, self)
            self.radio_id.addButton(radio)
        self.text_lt = qtw.QLineEdit(self)
        self.text_lt.textChanged.connect(functools.partial(self.on_text, 'lt'))

        self.check_options.addButton(qtw.QCheckBox("soort   -", self))
        self.check_cats = qtw.QButtonGroup(self)
        self.check_cats.setExclusive(False)
        for x in [self.parent.parent.cats[y] for y in sorted(
                self.parent.parent.cats.keys())]:
            check = qtw.QCheckBox(x[0], self)
            check.toggled.connect(functools.partial(self.on_checked, 'cat'))
            self.check_cats.addButton(check)

        self.check_options.addButton(qtw.QCheckBox(parent.parent.ctitels[2] + '   -',
                                                   self))
        self.check_stats = qtw.QButtonGroup(self)
        self.check_stats.setExclusive(False)
        for x in [self.parent.parent.stats[y] for y in sorted(
                self.parent.parent.stats.keys())]:
            check = qtw.QCheckBox(x[0], self)
            check.toggled.connect(functools.partial(self.on_checked, 'stat'))
            self.check_stats.addButton(check)

        if self.datatype == shared.DataType.XML.name:
            self.check_options.addButton(qtw.QCheckBox(parent.parent.ctitels[4] +
                                                       '   -', self))
            self.text_zoek = qtw.QLineEdit(self)
            self.text_zoek.textChanged.connect(functools.partial(self.on_text, 'zoek'))
        elif self.datatype == shared.DataType.SQL.name:
            self.check_options.addButton(qtw.QCheckBox('zoek in   -', self))
            self.text_zoek = qtw.QLineEdit(self)
            self.text_zoek.textChanged.connect(functools.partial(self.on_text, 'zoek'))
            self.radio_id2 = qtw.QButtonGroup(self)
            for text in ('en', 'of'):
                radio = qtw.QRadioButton(text, self)
                self.radio_id2.addButton(radio)
            self.text_zoek2 = qtw.QLineEdit(self)
            self.text_zoek2.textChanged.connect(functools.partial(self.on_text, 'zoek'))

        self.check_options.addButton(qtw.QCheckBox("Archief    -", self))
        self.radio_arch = qtw.QButtonGroup(self)
        for text in ("Alleen gearchiveerd", "gearchiveerd en lopend"):
            radio = qtw.QRadioButton(text, self)
            self.radio_arch.addButton(radio)
            radio.toggled.connect(functools.partial(self.on_checked, 'arch'))

        self.buttonbox = qtw.QDialogButtonBox(qtw.QDialogButtonBox.Ok |
                                              qtw.QDialogButtonBox.Cancel)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)

        self.set_default_values(sel_args)
        self.doelayout()

    def doelayout(self):
        """realize the dialog layout
        """
        sizer = qtw.QVBoxLayout()
        grid = qtw.QGridLayout()

        vbox = qtw.QVBoxLayout()
        vbox.addWidget(self.check_options.buttons()[0])
        vbox.addStretch()
        grid.addLayout(vbox, 0, 0)

        vbox = qtw.QVBoxLayout()
        hgrid = qtw.QGridLayout()
        hgrid.addWidget(qtw.QLabel('groter dan:', self), 0, 0)
        hgrid.addWidget(self.text_gt, 0, 1)
        hbox = qtw.QHBoxLayout()
        for rb in self.radio_id.buttons():
            hbox.addWidget(rb)
        hgrid.addLayout(hbox, 1, 0)
        hgrid.addWidget(qtw.QLabel('kleiner dan:', self), 2, 0)
        hgrid.addWidget(self.text_lt, 2, 1)
        vbox.addLayout(hgrid)
        grid.addLayout(vbox, 0, 2)

        vbox = qtw.QVBoxLayout()
        vbox.addWidget(self.check_options.buttons()[1])
        vbox.addStretch()
        grid.addLayout(vbox, 1, 0)

        hbox = qtw.QHBoxLayout()
        vbox = qtw.QVBoxLayout()
        vbox.addWidget(qtw.QLabel("selecteer een of meer:", self))
        vbox.addStretch()
        hbox.addLayout(vbox)
        vbox = qtw.QVBoxLayout()
        for check in self.check_cats.buttons():
            vbox.addWidget(check)
        hbox.addLayout(vbox)
        grid.addLayout(hbox, 1, 2)

        vbox = qtw.QVBoxLayout()
        vbox.addWidget(self.check_options.buttons()[2])
        vbox.addStretch()
        grid.addLayout(vbox, 2, 0)

        hbox = qtw.QHBoxLayout()
        vbox = qtw.QVBoxLayout()
        vbox.addWidget(qtw.QLabel("selecteer een of meer:", self))
        vbox.addStretch()
        hbox.addLayout(vbox)
        vbox = qtw.QVBoxLayout()
        for check in self.check_stats.buttons():
            vbox.addWidget(check)
        hbox.addLayout(vbox)
        grid.addLayout(hbox, 2, 2)

        vbox = qtw.QVBoxLayout()
        vbox.addWidget(self.check_options.buttons()[3])
        vbox.addStretch()
        grid.addLayout(vbox, 3, 0)

        hbox = qtw.QHBoxLayout()
        if self.datatype == shared.DataType.XML.name:
            hbox.addWidget(qtw.QLabel('zoek naar:', self))
            hbox.addWidget(self.text_zoek)
        elif self.datatype == shared.DataType.SQL.name:
            grid2 = qtw.QGridLayout()
            grid2.addWidget(qtw.QLabel(self.parent.parent.ctitels[4] + ":", self),
                            0, 0)
            grid2.addWidget(self.text_zoek, 0, 1)
            hbox2 = qtw.QHBoxLayout()
            for rb in self.radio_id2.buttons():
                hbox2.addWidget(rb)
            grid2.addLayout(hbox2, 1, 0)
            grid2.addWidget(qtw.QLabel(self.parent.parent.ctitels[5] + ":", self),
                            2, 0)
            grid2.addWidget(self.text_zoek2, 2, 1)
            hbox.addLayout(grid2)
        grid.addLayout(hbox, 3, 2)

        vbox = qtw.QVBoxLayout()
        vbox.addWidget(self.check_options.buttons()[4])
        vbox.addStretch()
        grid.addLayout(vbox, 4, 0)
        hbox = qtw.QHBoxLayout()
        for radio in self.radio_arch.buttons():
            hbox.addWidget(radio)
        grid.addLayout(hbox, 4, 2)
        sizer.addLayout(grid)

        sizer.addWidget(self.buttonbox)
        self.setLayout(sizer)

    def set_default_values(self, sel_args):
        """get search settings and present them in the dialog
        """
        test = self.parent.parent.fnaam
        if "idgt" in sel_args:
            self.text_gt.setText(sel_args["idgt"])
        if "id" in sel_args:
            if sel_args["id"] == "and":
                self.radio_id.buttons()[0].setChecked(True)
            else:
                self.radio_id.buttons()[1].setChecked(True)
            self.check_options.buttons()[0].setChecked(True)
        if "idlt" in sel_args:
            self.text_lt.setText(sel_args["idlt"])

        if self.datatype == shared.DataType.XML.name:
            itemindex = 1
        elif self.datatype == shared.DataType.SQL.name:
            itemindex = 2
        if "soort" in sel_args:
            for x in self.parent.parent.cats.keys():
                if self.parent.parent.cats[x][itemindex] in sel_args["soort"]:
                    self.check_cats.buttons()[int(x)].setChecked(True)
            self.check_options.buttons()[1].setChecked(True)

        if "status" in sel_args:
            for x in self.parent.parent.stats.keys():
                if self.parent.parent.stats[x][itemindex] in sel_args["status"]:
                    self.check_stats.buttons()[int(x)].setChecked(True)
            self.check_options.buttons()[2].setChecked(True)

        if "titel" in sel_args:
            try:
                self.text_zoek.setText(sel_args["titel"])
            except TypeError:
                for item in sel_args["titel"]:
                    if item[0] == 'about':
                        self.text_zoek.setText(item[1])
                    elif item[0] == 'title':
                        self.text_zoek2.setText(item[1])
                    elif item[0] == 'of':
                        self.radio_id2.buttons()[0].setChecked(True)
                    else:
                        self.radio_id2.buttons()[1].setChecked(True)
            self.check_options.buttons()[3].setChecked(True)

        if "arch" in sel_args:
            if sel_args["arch"] == "arch":
                self.radio_arch.buttons()[0].setChecked(True)
            if sel_args["arch"] == "alles":
                self.radio_arch.buttons()[1].setChecked(True)
            self.check_options.buttons()[4].setChecked(True)

    def on_text(self, arg, text):
        "callback voor activiteitnummer checkboxes"
        if arg in ('gt', 'lt'):
            obj = self.check_options.buttons()[0]
        elif arg == 'zoek':
            obj = self.check_options.buttons()[3]
        if text == "":
            obj.setChecked(False)
        else:
            obj.setChecked(True)

    def on_checked(self, arg, val):
        "callback voor status en soort checkboxes"
        if arg == 'cat':
            obj = self.check_options.buttons()[1]
            grp = self.check_cats
        elif arg == 'stat':
            obj = self.check_options.buttons()[2]
            grp = self.check_stats
        elif arg == 'arch':
            obj = self.check_options.buttons()[4]
            grp = self.radio_arch
        oneormore = False
        for btn in grp.buttons():
            if btn.isChecked():
                oneormore = True
                break
        if oneormore:
            obj.setChecked(True)
        else:
            obj.setChecked(False)

    def accept(self):
        "aangegeven opties verwerken in sel_args dictionary"
        selection = 'excl.gearchiveerde'
        sel_args = {}
        if self.check_options.buttons()[0].isChecked():
            selection = '(gefilterd)'
            id_gt, id_lt = str(self.text_gt.text()), str(self.text_lt.text())
            if id_gt:
                sel_args["idgt"] = id_gt
            if id_lt:
                sel_args["idlt"] = id_lt
            if self.radio_id.buttons()[0].isChecked():
                sel_args["id"] = "and"
            elif self.radio_id.buttons()[1].isChecked():
                sel_args["id"] = "or"
        if self.datatype == shared.DataType.XML.name:
            itemindex = 1
        elif self.datatype == shared.DataType.SQL.name:
            itemindex = 2
        if self.check_options.buttons()[1].isChecked():
            selection = '(gefilterd)'
            if self.datatype == shared.DataType.XML.name:
                lst = [self.parent.parent.cats[x][itemindex]
                       for x in range(len(self.parent.parent.cats.keys()))
                       if self.check_cats.buttons()[x].isChecked()]
            elif self.datatype == shared.DataType.SQL.name:
                lst = [self.parent.parent.cats[x][itemindex]
                       for x in range(len(self.parent.parent.cats.keys()))
                       if self.check_cats.buttons()[x].isChecked()]
            if lst:
                sel_args["soort"] = lst
        if self.check_options.buttons()[2].isChecked():
            selection = '(gefilterd)'
            if self.datatype == shared.DataType.XML.name:
                lst = [self.parent.parent.stats[x][itemindex]
                       for x in range(len(self.parent.parent.stats.keys()))
                       if self.check_stats.buttons()[x].isChecked()]
            elif self.datatype == shared.DataType.SQL.name:
                lst = [self.parent.parent.stats[x][itemindex]
                       for x in range(len(self.parent.parent.stats.keys()))
                       if self.check_stats.buttons()[x].isChecked()]
            if lst:
                sel_args["status"] = lst
        if self.check_options.buttons()[3].isChecked():
            selection = '(gefilterd)'
            if self.datatype == shared.DataType.XML.name:
                sel_args["titel"] = str(self.text_zoek.text())
            elif self.datatype == shared.DataType.SQL.name:
                sel_args["titel"] = [('about', str(self.text_zoek.text()))]
                if self.radio_id2.buttons()[0].isChecked():
                    sel_args["titel"].append(("and",))
                elif self.radio_id2.buttons()[1].isChecked():
                    sel_args["titel"].append(("or",))
                else:
                    sel_args["titel"].append((""))
                sel_args["titel"].append(('title', str(self.text_zoek2.text())))

        if self.check_options.buttons()[4].isChecked():
            if self.radio_arch.buttons()[0].isChecked():
                sel_args["arch"] = "arch"
                if selection != '(gefilterd)':
                    selection = '(gearchiveerd)'
            elif self.radio_arch.buttons()[1].isChecked():
                sel_args["arch"] = "alles"
                if selection != '(gefilterd)':
                    selection = ''
        self.parent.master.selection = selection
        self.parent.master.sel_args = sel_args

        if self._data:
            self._data.save_options(sel_args)
        super().accept()


class OptionsGui(qtw.QDialog):
    """base class voor de opties dialogen

    nu nog F2 en dubbelklikken mogelijk maken om editen te starten"""
    def __init__(self, parent, title, size=(300, 300)):
        self.parent = parent
        super().__init__(parent)
        self.resize(size[0], size[1])
        self.setWindowTitle(title)
        self.initstuff()
        sizer = qtw.QVBoxLayout()

        sizer.addWidget(qtw.QLabel(self.titel, self))

        self.elb = qtw.QListWidget(self)
        self.elb.currentItemChanged.connect(self.end_edit)
        self.elb.itemDoubleClicked.connect(self.edit_item)
        for text in self.data:
            self.elb.addItem(text)
        sizer.addWidget(self.elb)

        box = qtw.QHBoxLayout()
        box.addStretch()
        self.b_edit = qtw.QPushButton('&Edit', self)
        self.b_edit.clicked.connect(self.edit_item)
        box.addWidget(self.b_edit)
        if self.editable:
            self.b_new = qtw.QPushButton('&New', self)
            self.b_new.clicked.connect(self.add_item)
            box.addWidget(self.b_new)
            self.b_delete = qtw.QPushButton('&Delete', self)
            self.b_delete.clicked.connect(self.remove_item)
            box.addWidget(self.b_delete)
            self.b_up = qtw.QPushButton('Move &Up', self)
            self.b_up.clicked.connect(self.move_item_up)
            box.addWidget(self.b_up)
            self.b_down = qtw.QPushButton('Move &Down', self)
            self.b_down.clicked.connect(self.move_item_down)
            box.addWidget(self.b_down)
        box.addStretch()
        sizer.addLayout(box)

        sizer.addWidget(qtw.QLabel("\n".join(self.tekst), self))

        buttonbox = qtw.QDialogButtonBox(qtw.QDialogButtonBox.Ok |
                                         qtw.QDialogButtonBox.Cancel)
        sizer.addWidget(buttonbox)
        self.setLayout(sizer)

        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)

    def initstuff(self):
        """placeholder voor aanvullende initialisatie methode

        tevens om te tonen welke dingen er hier ingesteld moeten worden
        """
        self.titel = ""
        self.data = []
        self.tekst = ["", ""]
        self.editable = True

    def keyReleaseEvent(self, evt):
        """reimplementation of keyboard event handler
        """
        keycode = evt.key()
        if keycode == core.Qt.Key_F2:
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

        FIXME: (how) is this used?
        """
        self.elb.closePersistentEditor(item_o)

    def add_item(self):
        "open een nieuwe lege regel"
        item = qtw.QListWidgetItem('')
        self.elb.addItem(item)
        self.elb.setCurrentItem(item)
        self.elb.openPersistentEditor(item)
        self.elb.editItem(item)

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
        item = self.elb.currentItem()
        text = item.text()
        oldrow = self.elb.currentRow()
        if up:
            if oldrow == 0:
                return
            newrow = oldrow - 1
        else:
            newrow = self.elb.currentRow() + 1
            if newrow == self.elb.count():
                return
        item_to_replace = self.elb.item(newrow)
        text_to_replace = item_to_replace.text()
        item_to_replace.setText(text)
        item.setText(text_to_replace)
        self.elb.setCurrentItem(item_to_replace)

    def leesuit(self):
        "pass changed options to parent"
        return "This method is implemented in the subclasses"

    def accept(self):
        """Confirm changes to parent window
        """
        message = self.leesuit()
        if message:
            qtw.QMessageBox.information(self, 'Probreg', message)
            return
        super().accept()


class TabOptionsGui(OptionsGui):
    "dialoog voor mogelijke tab headers"
    def initstuff(self):
        "aanvullende initialisatie"
        self.titel = "Tab titels"
        self.data = []
        for key in sorted(self.parent.book.tabs.keys()):
            tab_id, tab_text = self.parent.book.tabs[key].split(" ", 1)
            self.data.append(tab_text)
        self.tekst = ["De tab titels worden getoond in de volgorde",
                      "zoals ze van links naar rechts staan.",
                      "Er kunnen geen tabs worden verwijderd of toegevoegd."]
        self.editable = False

    def leesuit(self):
        "wijzigingen doorvoeren"
        self.newtabs = {}
        ## for idx, item in enumerate(self.elb.items()):
        for idx in range(self.elb.count()):
            item = self.elb.item(idx).text()
            self.newtabs[str(idx)] = str(item)
        self.parent.save_settings("tab", self.newtabs)


class StatOptionsGui(OptionsGui):
    "dialoog voor de mogelijke statussen"
    def initstuff(self):
        "aanvullende initialisatie"
        self.titel = "Status codes en waarden"
        self.data = []
        for key in sorted(self.parent.book.stats.keys()):
            if self.parent.datatype == shared.DataType.XML.name:
                item_text, item_value = self.parent.book.stats[key]
                self.data.append(": ".join((item_value, item_text)))
            elif self.parent.datatype == shared.DataType.SQL.name:
                item_text, item_value, row_id = self.parent.book.stats[key]
                self.data.append(": ".join((item_value, item_text, row_id)))
        self.tekst = ["De waarden voor de status worden getoond in dezelfde volgorde",
                      "als waarin ze in de combobox staan.",
                      "Vóór de dubbele punt staat de code, erachter de waarde.",
                      "Denk erom dat als je codes wijzigt of statussen verwijdert, deze",
                      "ook niet meer getoond en gebruikt kunnen worden in de registratie."]
        self.editable = True

    def leesuit(self):
        "wijzigingen doorvoeren"
        self.newstats = {}
        for sortkey in range(self.elb.count()):
            item = self.elb.item(sortkey).text()
            try:
                value, text = str(item).split(": ")
            except ValueError:
                return 'Foutieve waarde: bevat geen dubbele punt'
            self.newstats[value] = (text, sortkey)
        self.parent.save_settings("stat", self.newstats)


class CatOptionsGui(OptionsGui):
    "dialoog voor de mogelijke categorieen"
    def initstuff(self):
        "aanvullende initialisatie"
        self.titel = "Soort codes en waarden"
        self.data = []
        for key in sorted(self.parent.book.cats.keys()):
            if self.parent.datatype == shared.DataType.XML.name:
                item_value, item_text = self.parent.book.cats[key]
                self.data.append(": ".join((item_text, item_value)))
            elif self.parent.datatype == shared.DataType.SQL.name:
                item_value, item_text, row_id = self.parent.book.cats[key]
                self.data.append(": ".join((item_text, item_value, str(row_id))))
        self.tekst = ["De waarden voor de soorten worden getoond in dezelfde volgorde",
                      "als waarin ze in de combobox staan.",
                      "Vóór de dubbele punt staat de code, erachter de waarde.",
                      "Denk erom dat als je codes wijzigt of soorten verwijdert, deze",
                      "ook niet meer getoond en gebruikt kunnen worden in de registratie."]
        self.editable = True

    def leesuit(self):
        "wijzigingen doorvoeren"
        self.newcats = {}
        for sortkey in range(self.elb.count()):
            item = self.elb.item(sortkey).text()
            try:
                value, text = str(item).split(": ")
            except ValueError:
                return 'Foutieve waarde: bevat geen dubbele punt'
            self.newcats[value] = (text, sortkey)
        self.parent.save_settings("cat", self.newcats)


class LoginBox(qtw.QDialog):
    """Sign in with userid & password
    """
    def __init__(self, parent):
        self.parent = parent
        self.parent.dialog_data = ()
        super().__init__(parent)
        vbox = qtw.QVBoxLayout()
        grid = qtw.QGridLayout()
        grid.addWidget(qtw.QLabel('Userid', self), 0, 0)
        self.t_username = qtw.QLineEdit(self)
        grid.addWidget(self.t_username, 0, 1)
        grid.addWidget(qtw.QLabel('Password', self), 1, 0)
        self.t_password = qtw.QLineEdit(self)
        self.t_password.setEchoMode(qtw.QLineEdit.Password)
        grid.addWidget(self.t_password, 1, 1)
        vbox.addLayout(grid)
        bbox = qtw.QDialogButtonBox(qtw.QDialogButtonBox.Ok |
                                    qtw.QDialogButtonBox.Cancel)
        ## bbox.button(qtw.QDialogButtonBox.Ok).setDefault(True)  # -- werkt ook al niet
        vbox.addWidget(bbox)
        self.setLayout(vbox)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)

    def accept(self):
        """check login credentials
        """
        self.parent.dialog_data = (self.t_username.text(), self.t_password.text(),
                                   self.parent.master.filename)
        super().accept()


class MainGui(qtw.QMainWindow):
    """Hoofdscherm met menu, statusbalk, notebook en een "quit" button"""
    def __init__(self, master):
        self.master = master
        self.app = qtw.QApplication(sys.argv)
        super().__init__()
        self.setWindowTitle(self.master.title)
        self.setWindowIcon(gui.QIcon("task.ico"))
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
        self.create_menu()
        self.create_actions()
        self.pnl = qtw.QFrame(self)
        self.setCentralWidget(self.pnl)
        self.toolbar = None
        self.create_book()

    def create_menu(self):
        """Create application menu
        """
        def add_to_menu(menu, menuitem):
            "parse line and create menu item"
            if len(menuitem) == 1:
                menu.addSeparator()
            elif len(menuitem) == 4:
                caption, callback, keys, tip = menuitem
                action = menu.addAction(caption)
                action.triggered.connect(callback)
                if keys:
                    action.setShortcut(keys)
                if tip:
                    action.setToolTip(tip)
            elif len(menuitem) == 2:
                title, items = menuitem
                sub = menu.addMenu(title)
                if title == '&Data':
                    self.settingsmenu = sub
                for subitem in items:
                    add_to_menu(sub, subitem)

        menu_bar = self.menuBar()
        for title, items in self.master.get_menu_data():
            menu = menu_bar.addMenu(title)
            for menuitem in items:
                add_to_menu(menu, menuitem)

    def create_actions(self):
        """Create additional application actions
        """
        return  # skip for now
        action = qtw.QShortcut('Ctrl+P', self, self.print_)
        action = qtw.QShortcut('Alt+Left', self, self.go_prev)
        action = qtw.QShortcut('Alt+Right', self, self.go_next)
        for char in '0123456':
            action = qtw.QShortcut('Alt+{}'.format(char), self,
                                   functools.partial(self.go_to, int(char)))

    def create_book(self):
        "build the tabbed widget"
        self.bookwidget = qtw.QTabWidget(self.pnl)
        self.bookwidget.resize(300, 300)
        self.bookwidget.sorter = None
        self.bookwidget.textcallbacks = {}
        self.bookwidget.currentChanged.connect(self.master.on_page_changing)
        # return self.bookwidget
        self.master.create_book(self.bookwidget)

    def go(self):
        """realize the screen layout and start application
        """
        sizer0 = qtw.QVBoxLayout()
        sizer0.addWidget(self.bookwidget)
        sizer1 = qtw.QHBoxLayout()
        sizer1.addStretch()
        self.exit_button = qtw.QPushButton('&Quit', self.pnl)
        self.exit_button.clicked.connect(self.master.exit_app)
        sizer1.addWidget(self.exit_button)
        sizer1.addStretch()
        sizer0.addLayout(sizer1)
        self.pnl.setLayout(sizer0)
        self.show()
        # self.set_tabfocus(0)
        sys.exit(self.app.exec_())

    def not_implemented_message(self):
        "information"
        qtw.QMessageBox.information(self, "Oeps", "Sorry, werkt nog niet")

    def enable_all_book_tabs(self, state):
        "make all tabs (in)accessible"
        for i in range(1, self.master.book.count()):
            self.bookwidget.setTabEnabled(i, state)

    def enable_book_tabs(self, state, tabfrom=0, tabto=-1):
        "make specified tabs (in)accessible"
        if tabto == -1:
            tabto = self.master.book.count()
        for i in range(tabfrom, tabto):
            self.bookwidget.setTabEnabled(i, state)

    def enable_all_other_tabs(self):
        "make all tabs accessible except the current one"
        for i in range(self.master.book.count()):
            if i != self.master.book.current_tab:
                self.bookwidget.setTabEnabled(i, True)

    def add_book_tab(self, tab, title):
        "add a new tab to the widget"
        self.bookwidget.addTab(tab.gui, title)
        tab.gui.doelayout()

    def exit(self):
        "Menukeuze: exit applicatie"
        self.close()    # enough for now

    def set_page(self, num):
        "set the selected page to this index"
        self.bookwidget.setCurrentIndex(num)

    def get_page(self):
        "return index g=for the selected page"
        return self.bookwidget.currentIndex()

    def set_tabfocus(self, tabno):
        "focus geven aan de gekozen tab"
        if tabno == 0:
            self.master.book.page0.gui.p0list.setFocus()
        elif tabno == 1:
            self.master.book.page1.gui.set_focus()  # proc_entry.setFocus()
        elif tabno == 2:
            self.master.book.page2.gui.text1.setFocus()
        elif tabno == 3:
            self.master.book.page3.gui.text1.setFocus()
        elif tabno == 4:
            self.master.book.page4.gui.text1.setFocus()
        elif tabno == 5:
            self.master.book.page5.gui.text1.setFocus()
        elif tabno == 6:
            self.master.book.page6.gui.progress_list.setFocus()

    def print_(self):
        """callback voor ctrl-P(rint)

        vraag om printen scherm of actie, bv. met een InputDialog
        """
        choice, ok = qtw.QInputDialog.getItem(self, 'Afdrukken', 'Wat wil je afdrukken?',
                                              ['huidig scherm', 'huidige actie'])
        if ok:
            print('printing', choice)
            if choice == 0:
                self.print_scherm()
            else:
                self.print_actie()

    def go_next(self):
        """redirect to the method of the current page
        """
        Page.goto_next(self.book.widget(self.book.current_tab))

    def go_prev(self):
        """redirect to the method of the current page
        """
        Page.goto_prev(self.book.widget(self.book.current_tab))

    def go_to(self, page):
        """redirect to the method of the current page
        """
        Page.goto_page(self.book.widget(self.book.current_tab), page)

    def preview(self):
        "callback voor print preview"
        self.print_dlg = qtp.QPrintPreviewDialog(self)
        self.print_dlg.paintRequested.connect(self.afdrukken)
        self.print_dlg.exec_()

    def afdrukken(self, printer):
        "wordt aangeroepen door de menuprint methodes"
        self.css = ""
        if self.css:
            self.printdict['css'] = self.css
        self.printdict['hdr'] = self.hdr
        doc = gui.QTextDocument(self)
        html = Template(filename='probreg/actie.tpl').render(**self.printdict)
        doc.setHtml(html)
        printer.setOutputFileName(self.hdr)
        doc.print_(printer)
        self.print_dlg.done(True)

    def enable_settingsmenu(self):
        "instellen of gebruik van settingsmenu mogelijk is"
        self.settingsmenu.setEnabled(self.master.is_admin)

    def set_statusmessage(self, msg):
        """stel tekst in statusbar in
        """
        self.statusmessage.setText(msg)

    def set_window_title(self, text):
        "build title for window"
        self.setWindowTitle(text)

    def show_username(self, msg):
        "show if/which user is logged in"
        self.showuser.setText(msg)

    def set_tab_titles(self, tabs):
        "(re)build the titles on the tabs"
        for x in self.master.book.tabs.keys():
            self.bookwidget.setTabText(x, self.master.book.tabs[x])

    def select_first_tab(self):
        "set selection to first page"
        self.bookwidget.setCurrentIndex(0)
