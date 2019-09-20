#! usr/bin/env python
# -*- coding: UTF-8 -*-
"""Actie (was: problemen) Registratie, PyQT5 versie
"""
from __future__ import print_function
import os
import sys
import pathlib
import enum
from datetime import datetime
## import pprint
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
    qtw.QMessageBox.information(win, win.title, message)


def get_open_filename(parent):  # binnenhalen via gui module
    fname, pattern = qtw.QFileDialog.getOpenFileName(
        parent, parent.title + " - kies een gegevensbestand", parent.dirname, xmlfilter)
    return fname


def get_save_filename(parent):  # binnenhalen via gui module
    fname, pattern = qtw.QFileDialog.getSaveFileName(
        parent, parent.title + " - nieuw gegevensbestand", parent.dirname, xmlfilter)
    return fname


def get_choice_item(self, caption, choices):  # binnenhalen via gui module
    choice, ok = qtw.QInputDialog.getItem(self, 'Probreg SQL versie', caption, choices,
                                          current=current, editable=False)
    if ok:
        return choice
    return ''


class EditorPanelGui(qtw.QTextEdit):
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
        self.setTabStopWidth(tabsize(font.pointSize()))
        self.defaultfamily, self.defaultsize = font.family(), font.pointSize()

    def canInsertFromMimeData(self, source):
        "reimplementation of event handler"
        if source.hasImage:
            return True
        else:
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
            self.setTabStopWidth(tabsize(font.pointSize()))
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
            self.setTabStopWidth(tabsize(pointsize))
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
    def __init__(self, parent, pageno, standard=True):
        self.parent = parent
        super().__init__(parent)
        if not standard:
            return
        self.actiondict = collections.OrderedDict()
        self.create_toolbar()
        self.create_text_field(pageno)
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

    def readp(self, pid):
        "lezen van een actie"
        if self.parent.pagedata:  # spul van de vorige actie opruimen
            self.parent.pagedata.clear()
        self.parent.pagedata = Actie[self.parent.parent.datatype](self.parent.fnaam, pid,
                                                                  self.parent.parent.user)
        self.parent.parent.imagelist = self.parent.pagedata.imagelist
        self.parent.old_id = self.parent.pagedata.id
        self.parent.newitem = False

    def nieuwp(self):
        """voorbereiden opvoeren nieuwe actie"""
        log('opvoeren nieuwe actie')
        self.parent.newitem = True
        if self.leavep():
            if self.parent.current_tab == 0:
                for i in range(1, self.parent.count()):
                    self.parent.setTabEnabled(i, True)
            self.parent.pagedata = Actie[self.parent.parent.datatype](self.parent.fnaam, 0,
                                                                      self.parent.parent.user)
            self.parent.parent.imagelist = self.parent.pagedata.imagelist
            self.parent.newitem = True
            if self.parent.current_tab == 1:
                self.vulp()  # om de velden leeg te maken
                self.proc_entry.setFocus()
            else:
                self.goto_page(1, check=False)
        else:
            self.parent.newitem = False
            log("leavep() geeft False: nog niet klaar met huidige pagina")

    def leavep(self):
        "afsluitende acties uit te voeren alvorens de pagina te verlaten"
        newbuf = self.build_newbuf()
        if self.parent.current_tab == 1 and self.parent.newitem and newbuf[0] == "" \
                and newbuf[1] == "" and not self.parent.parent.exiting:
            self.parent.newitem = False
            self.parent.pagedata = Actie[self.parent.parent.datatype](self.parent.fnaam,
                                                                      self.parent.old_id,
                                                                      self.parent.parent.user)
        ok_to_leave = True
        self.parent.checked_for_leaving = True
        if self.parent.current_tab == 0:
            log('%s %s', self.parent.parent.mag_weg, self.parent.newitem)
            if not self.parent.parent.mag_weg and not self.parent.newitem:
                ok_to_leave = False
        elif newbuf != self.oldbuf:
            retval = qtw.QMessageBox.question(
                self, self.parent.parent.title,
                "\n".join(("De gegevens op de pagina zijn gewijzigd, ",
                           "wilt u de wijzigingen opslaan voordat u verder gaat?")),
                buttons=qtw.QMessageBox.Yes | qtw.QMessageBox.No | qtw.QMessageBox.Cancel)
            if retval == qtw.QMessageBox.Yes:
                ok_to_leave = self.savep()
            elif retval == qtw.QMessageBox.Cancel:
                self.parent.checked_for_leaving = ok_to_leave = False
            if retval != qtw.QMessageBox.Cancel:
                for i in range(self.parent.count()):
                    if i != self.parent.current_tab:
                        self.parent.setTabEnabled(i, True)
        return ok_to_leave

    def savep(self):
        "gegevens van een actie opslaan afhankelijk van pagina"
        if not self.save_button.isEnabled():
            return
        self.enable_buttons(False)
        if self.parent.current_tab <= 1 or self.parent.current_tab == 6:
            return
        wijzig = False
        text = self.text1.get_contents()
        if self.parent.current_tab == 2 and text != self.parent.pagedata.melding:
            self.oldbuf = self.parent.pagedata.melding = text
            self.parent.pagedata.events.append((get_dts(), "Meldingtekst aangepast"))
            wijzig = True
        if self.parent.current_tab == 3 and text != self.parent.pagedata.oorzaak:
            self.oldbuf = self.parent.pagedata.oorzaak = text
            self.parent.pagedata.events.append((get_dts(), "Beschrijving oorzaak aangepast"))
            wijzig = True
        if self.parent.current_tab == 4 and text != self.parent.pagedata.oplossing:
            self.oldbuf = self.parent.pagedata.oplossing = text
            self.parent.pagedata.events.append((get_dts(), "Beschrijving oplossing aangepast"))
            wijzig = True
        if self.parent.current_tab == 5 and text != self.parent.pagedata.vervolg:
            self.oldbuf = self.parent.pagedata.vervolg = text
            self.parent.pagedata.events.append((get_dts(), "Tekst vervolgactie aangepast"))
            wijzig = True
        if wijzig:
            self.update_actie()
            self.parent.page0.p0list.currentItem().setText(3, self.parent.pagedata.updated)
        return True

    def savepgo(self):
        "opslaan en naar de volgende pagina"
        if not self.saveandgo_button.isEnabled():
            return
        if self.savep():
            self.goto_next()
        else:
            self.enable_buttons()

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
        newbuf = None
        if self.parent.current_tab == 1:
            newbuf = (str(self.proc_entry.text()), str(self.desc_entry.text()),
                      int(self.stat_choice.currentIndex()),
                      int(self.cat_choice.currentIndex()))
        elif 1 < self.parent.current_tab < 6:
            newbuf = self.text1.get_contents()
        elif self.parent.current_tab == 6:
            newbuf = (self.event_list, self.event_data)
        return newbuf

    def on_choice(self):
        "callback voor combobox"
        self.enable_buttons()

    def update_actie(self):
        """pass page data from the GUI to the internal storage
        """
        self.parent.pagedata.imagecount = self.parent.parent.imagecount
        self.parent.pagedata.imagelist = self.parent.parent.imagelist
        if self.parent.parent.datatype == DataType.SQL.name:
            self.parent.pagedata.write(self.parent.parent.user)
        else:
            self.parent.pagedata.write()
        self.parent.checked_for_leaving = True
        self.mag_weg = True
        self.parent.pagedata.read()    # om "updated" attribuut op te halen

    def enable_buttons(self, state=True):
        "buttons wel of niet bruikbaar maken"
        if state:
            self.parent.checked_for_leaving = False
        self.save_button.setEnabled(state)
        if self.parent.current_tab < 6:
            self.saveandgo_button.setEnabled(state)
        self.cancel_button.setEnabled(state)
        if self.parent.current_tab > 0:
            for i in range(self.parent.count()):
                if i != self.parent.current_tab:
                    self.parent.setTabEnabled(i, not state)

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

    def get_entry_text(self):  # methode van PageGui
        return self.text1.get_contents()


class Page0Gui(PageGui):
    "pagina 0: overzicht acties"
    def __init__(self, parent):
        self.parent = parent
        Page.__init__(self, parent, pageno=0, standard=False)
        self.selection = 'excl. gearchiveerde'
        self.sel_args = {}
        self.sorted = (0, "A")

        widths = [94, 24, 146, 90, 400] if LIN else [64, 24, 114, 72, 292]
        if self.parent.parent.datatype == DataType.SQL.name:
            widths[4] = 90 if LIN else 72
            extra = 310 if LIN else 220
            widths.append(extra)
        self.p0list = qtw.QTreeWidget(self)
        self.sort_button = qtw.QPushButton('S&Orteer', self)
        self.filter_button = qtw.QPushButton('F&Ilter', self)
        self.go_button = qtw.QPushButton('&Ga naar melding', self)
        self.archive_button = qtw.QPushButton('&Archiveer', self)
        self.new_button = qtw.QPushButton('Voer &Nieuwe melding op', self)

        self.sort_via_options = False
        self.p0list.setSortingEnabled(True)
        self.p0list.setHeaderLabels(self.parent.ctitels)
        self.p0list.setAlternatingRowColors(True)
        self.p0hdr = self.p0list.header()
        self.p0hdr.setSectionsClickable(True)
        for indx, wid in enumerate(widths):
            self.p0hdr.resizeSection(indx, wid)
        self.p0hdr.setStretchLastSection(True)
        self.p0list.itemActivated.connect(self.on_activate_item)
        self.p0list.currentItemChanged.connect(self.on_change_selected)

        self.sort_button.clicked.connect(self.sort_items)
        self.filter_button.clicked.connect(self.select_items)
        self.go_button.clicked.connect(self.goto_actie)
        self.archive_button.clicked.connect(self.archiveer)
        self.new_button.clicked.connect(self.nieuwp)

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

    def vulp(self):
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina
        """
        if (self.parent.parent.datatype == DataType.SQL.name
                and self.parent.parent.filename):
            if self.parent.parent.is_user:
                self._data = dmls.SortOptions(self.parent.parent.filename)
                test = self._data.load_options()
                test = bool(test)
                self.sort_via_options = test
                self.p0list.setSortingEnabled(not test)
            else:
                self.p0list.setSortingEnabled(False)

        self.seltitel = 'alle meldingen ' + self.selection
        Page.vulp(self)
        msg = ''
        if self.parent.rereadlist:
            self.parent.data = {}
            select = self.sel_args.copy()
            arch = ""  # "alles"
            if "arch" in select:
                arch = select.pop("arch")

            try:
                data = get_acties[self.parent.parent.datatype](self.parent.fnaam, select,
                                                               arch, self.parent.parent.user)
            except DataError as msg:
                print("samenstellen lijst mislukt: " + str(msg))
                raise
            for idx, item in enumerate(data):
                if self.parent.parent.datatype == DataType.XML.name:
                    # nummer, start, stat, cat, titel, gewijzigd = item
                    self.parent.data[idx] = (item[0],
                                             item[1],
                                             ".".join((item[3][1], item[3][0])),
                                             ".".join((item[2][1], item[2][0])),
                                             item[5],
                                             item[4])
                elif self.parent.parent.datatype == DataType.SQL.name:
                    # nummer, start, stat_title, stat_value, cat_title, cat_value, \
                    # about, titel, gewijzigd = item
                    self.parent.data[idx] = (item[0],
                                             item[1],
                                             ".".join((item[5], item[4])),
                                             ".".join((str(item[3]), item[2])),
                                             item[8],
                                             item[6],
                                             item[7])
            msg = self.populate_list()
            # nodig voor sorteren?
            # if self.parent.parent.datatype == DataType.XML.name:
            #     self.p0list.sortItems(self.sorted[0], sortorder[self.sorted[1]])  # , True)
            #
            self.parent.current_item = self.p0list.topLevelItem(0)
            # self.parent.rereadlist = False  # (wordt al uitgezet in rereadlist)
        for i in range(1, self.parent.count()):
            self.parent.setTabEnabled(i, False)
        self.enable_buttons()
        if self.p0list.has_selection:
            for i in range(1, self.parent.count()):
                self.parent.setTabEnabled(i, True)
        self.parent.parent.setToolTip("{0} - {1} items".format(
            self.parent.pagehelp[self.parent.current_tab], len(self.parent.data)))
        if self.parent.current_item is not None:
            self.p0list.setCurrentItem(self.parent.current_item)
        self.p0list.scrollToItem(self.parent.current_item)
        self.parent.parent.set_statusmessage(msg)

    def populate_list(self):
        "list control vullen"
        self.p0list.clear()
        self.p0list.has_selection = False

        self.parent.rereadlist = False
        items = self.parent.data.items()
        if items is None:
            self.parent.parent.sbar.showMessage('Selection is None?', 1000)
        if not items:
            return

        self.p0list.has_selection = True
        for key, data in items:
            if self.parent.parent.datatype == DataType.XML.name:
                actie, _, soort, status, l_wijz, titel = data
            elif self.parent.parent.datatype == DataType.SQL.name:
                actie, _, soort, status, l_wijz, over, titel = data
            new_item = qtw.QTreeWidgetItem()
            new_item.setText(0, actie)
            new_item.setData(0, core.Qt.UserRole, actie)
            pos = soort.index(".") + 1
            new_item.setText(1, soort[pos:pos + 1].upper())
            pos = status.index(".") + 1
            new_item.setText(2, status[pos:])
            new_item.setText(3, l_wijz)
            if self.parent.parent.datatype == DataType.XML.name:
                new_item.setText(4, titel)
            elif self.parent.parent.datatype == DataType.SQL.name:
                new_item.setText(4, over)
                new_item.setText(5, titel)
            self.p0list.addTopLevelItem(new_item)

    def on_change_selected(self, item_n, item_o):
        """callback voor wijzigen geselecteerd item, o.a. door verplaatsen van de
        cursor of door klikken"""
        if item_n is None:  # o.a. self.p0list.clear() veroorzaakt dit
            return
        self.parent.current_item = item_n
        if not self.parent.newitem:
            selindx = data2str(self.parent.current_item.data(0, core.Qt.UserRole))
            self.readp(selindx)
        hlp = "&Herleef" if self.parent.pagedata.arch else "&Archiveer"
        self.archive_button.setText(hlp)

    def on_activate_item(self, item):
        """callback voor activeren van item, door doubleclick of enter

        gek genoeg leidt een enter op een regel al tot het naar de volgende
        tab gaan (misschien door de on key afhandeling?)
        """
        self.goto_actie()

    def select_items(self):
        """tonen van de selectie dialoog

        niet alleen selecteren op tekst(deel) maar ook op status, soort etc"""
        while True:
            test = SelectOptionsDialog(self, self.sel_args).exec_()
            if test != qtw.QDialog.Accepted:
                break
            self.parent.rereadlist = True
            try:
                self.vulp()
            except DataError as msg:
                self.parent.rereadlist = False
                qtw.QMessageBox.information(self, "Oeps", str(msg))
            else:
                break

    def sort_items(self):
        """tonen van de sorteer-opties dialoog

        sortering mogelijk op datum/tijd, soort, titel, status via schermpje met
        2x4 comboboxjes waarin je de volgorde van de rubrieken en de sorteervolgorde
        per rubriek kunt aangeven"""
        test = SortOptionsDialog(self).exec_()
        if test != qtw.QDialog.Accepted:
            return
        if self.sort_via_options:
            self.p0list.setSortingEnabled(False)
            self.parent.rereadlist = True
            try:
                self.vulp()
            except DataError as msg:
                self.parent.rereadlist = False
                qtw.QMessageBox.information(self, "Oeps", str(msg))
        else:
            self.p0list.setSortingEnabled(True)

    def archiveer(self):
        "archiveren of herleven van het geselecteerde item"
        selindx = self.parent.current_item.data(0, core.Qt.UserRole)
        selindx = data2str(selindx) if self.parent.parent.datatype == DataType.XML else data2int(selindx)
        self.readp(selindx)
        if self.parent.parent.datatype == DataType.XML.name:
            self.parent.pagedata.arch = not self.parent.pagedata.arch
            hlp = "gearchiveerd" if self.parent.pagedata.arch else "herleefd"
            self.parent.pagedata.events.append((get_dts(), "Actie {0}".format(hlp)))
        elif self.parent.parent.datatype == DataType.SQL.name:
            self.parent.pagedata.set_arch(not self.parent.pagedata.arch)
        self.update_actie()  # self.parent.pagedata.write()
        self.parent.rereadlist = True
        self.vulp()
        self.parent.parent.zetfocus(0)
        # het navolgende geldt alleen voor de selectie "gearchiveerd en actief"
        if self.sel_args.get("arch", "") == "alles":
            self.p0list.scrollToItem(self.parent.current_item)
            hlp = "&Herleef" if self.parent.pagedata.arch else "&Archiveer"
            self.archive_button.setText(hlp)

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

    def get_items(self):  # methode van Page0Gui
        return [self.p0list.topLevelItem(indx) for i in range(self.p0list.topLevelItemCount())]

    def get_item_text(self, item_or_index, column):  # methode van Page0Gui
        return item_or_index.text(column)


class Page1Gui(PageGui):
    "pagina 1: startscherm actie"
    def __init__(self, parent):
        Page.__init__(self, parent, pageno=1, standard=False)

        self.id_text = qtw.QLineEdit(self)
        self.id_text.setMaximumWidth(120)
        self.date_text = qtw.QLineEdit(self)
        self.date_text.setMaximumWidth(150)

        self.proc_entry = qtw.QLineEdit(self)
        self.proc_entry.setMaximumWidth(150)
        self.proc_entry.textChanged.connect(self.on_text)
        self.desc_entry = qtw.QLineEdit(self)
        self.desc_entry.setMaximumWidth(360)
        self.desc_entry.textChanged.connect(self.on_text)

        self.cat_choice = qtw.QComboBox(self)
        self.cat_choice.setEditable(False)
        self.cat_choice.setMaximumWidth(180)
        self.cat_choice.currentIndexChanged.connect(self.on_text)
        self.stat_choice = qtw.QComboBox(self)
        self.stat_choice.setEditable(False)
        self.id_text.setMaximumWidth(140)
        self.stat_choice.currentIndexChanged.connect(self.on_text)

        self.archive_text = qtw.QLabel(self)
        self.archive_button = qtw.QPushButton("Archiveren", self)
        self.archive_button.clicked.connect(self.archiveer)

        self.save_button = qtw.QPushButton('Sla wijzigingen op (Ctrl-S)', self)
        self.save_button.clicked.connect(self.savep)
        action = qtw.QShortcut('Ctrl+S', self, self.savep)
        self.saveandgo_button = qtw.QPushButton('Sla op en ga verder (Ctrl-G)', self)
        self.saveandgo_button.clicked.connect(self.savepgo)
        action = qtw.QShortcut('Ctrl+G', self, self.savepgo)
        self.cancel_button = qtw.QPushButton('Maak wijzigingen ongedaan (Alt-Ctrl-Z)',
                                             self)
        self.cancel_button.clicked.connect(self.restorep)
        action = qtw.QShortcut('Alt+Ctrl+Z', self, self.restorep)  # Ctrl-Z zit al in text control
        action = qtw.QShortcut('Alt+N', self, self.nieuwp)

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

    def vulp(self):
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina"""
        Page.vulp(self)
        self.initializing = True
        self.id_text.clear()
        self.date_text.clear()
        self.proc_entry.clear()
        self.desc_entry.clear()
        self.archive_text.setText("")
        self.cat_choice.setCurrentIndex(0)
        self.stat_choice.setCurrentIndex(0)
        self.parch = False
        if self.parent.pagedata is not None:  # and not self.parent.newitem:
            self.id_text.setText(str(self.parent.pagedata.id))
            self.date_text.setText(self.parent.pagedata.datum)
            self.parch = self.parent.pagedata.arch
            if self.parent.parent.datatype == DataType.XML.name:
                if self.parent.pagedata.titel is not None:
                    if " - " in self.parent.pagedata.titel:
                        hlp = self.parent.pagedata.titel.split(" - ", 1)
                    else:
                        hlp = self.parent.pagedata.titel.split(": ", 1)
                    self.proc_entry.setText(hlp[0])
                    if len(hlp) > 1:
                        self.desc_entry.setText(hlp[1])
            elif self.parent.parent.datatype == DataType.SQL.name:
                self.proc_entry.setText(self.parent.pagedata.over)
                self.desc_entry.setText(self.parent.pagedata.titel)
            for x in range(len(self.parent.stats)):
                y = data2str(self.stat_choice.itemData(x))
                if y == self.parent.pagedata.status:
                    self.stat_choice.setCurrentIndex(x)
                    break
            for x in range(len(self.parent.cats)):
                y = data2str(self.cat_choice.itemData(x))
                if y == self.parent.pagedata.soort:
                    self.cat_choice.setCurrentIndex(x)
                    break
        self.oldbuf = (str(self.proc_entry.text()), str(self.desc_entry.text()),
                       int(self.stat_choice.currentIndex()),
                       int(self.cat_choice.currentIndex()))
        if self.parch:
            aanuit = False
            self.archive_text.setText("Deze actie is gearchiveerd")
            self.archive_button.setText("Herleven")
        else:
            aanuit = True
            self.archive_text.setText("")
            self.archive_button.setText("Archiveren")
        if not self.parent.parent.is_user:
            aanuit = False
        self.id_text.setEnabled(False)
        self.date_text.setEnabled(False)
        self.proc_entry.setEnabled(aanuit)
        self.desc_entry.setEnabled(aanuit)
        self.cat_choice.setEnabled(aanuit)
        self.stat_choice.setEnabled(aanuit)
        if self.parent.newitem or not self.parent.parent.is_user:
            self.archive_button.setEnabled(False)
        else:
            self.archive_button.setEnabled(True)
        self.initializing = False

    def savep(self):
        "opslaan van de paginagegevens"
        Page.savep(self)
        proc = str(self.proc_entry.text())
        proc = proc.capitalize()
        self.proc_entry.setText(proc)
        self.enable_buttons(False)
        desc = str(self.desc_entry.text())
        if proc == "" or desc == "":
            qtw.QMessageBox.information(self, "Oeps",
                                        "Beide tekstrubrieken moeten worden ingevuld")
            return False
        wijzig = False
        procdesc = " - ".join((proc, desc))
        if procdesc != self.parent.pagedata.titel:
            if self.parent.parent.datatype == DataType.XML.name:
                self.parent.pagedata.titel = procdesc
            elif self.parent.parent.datatype == DataType.SQL.name:
                self.parent.pagedata.over = proc
                self.parent.pagedata.events.append(
                    (get_dts(), 'Onderwerp gewijzigd in "{0}"'.format(proc)))
                self.parent.pagedata.titel = procdesc = desc
            self.parent.pagedata.events.append(
                (get_dts(), 'Titel gewijzigd in "{0}"'.format(procdesc)))
            wijzig = True
        idx = self.stat_choice.currentIndex()
        # newstat = data2str(self.stat_choice.itemData(idx))  # xml versie?
        newstat = data2int(self.stat_choice.itemData(idx))
        if newstat != self.parent.pagedata.status:
            self.parent.pagedata.status = newstat
            sel = self.stat_choice.currentText()
            self.parent.pagedata.events.append(
                (get_dts(), 'Status gewijzigd in "{0}"'.format(sel)))
            wijzig = True
        idx = self.cat_choice.currentIndex()
        newcat = data2str(self.cat_choice.itemData(idx))
        if newcat != self.parent.pagedata.soort:
            self.parent.pagedata.soort = newcat
            sel = str(self.cat_choice.currentText())
            self.parent.pagedata.events.append(
                (get_dts(), 'Categorie gewijzigd in "{0}"'.format(sel)))
            wijzig = True
        if self.parch != self.parent.pagedata.arch:
            self.parent.pagedata.set_arch(self.parch)
            hlp = "gearchiveerd" if self.parch else "herleefd"
            self.parent.pagedata.events.append(
                (get_dts(), "Actie {0}".format(hlp)))
            wijzig = True
        if wijzig:
            self.update_actie()
            if self.parent.newitem:
                # nieuwe entry maken in de tabel voor panel 0
                self.parent.current_item = len(self.parent.data)  # + 1
                self.parent.data[self.parent.current_item] = (
                    str(self.date_text.text()),
                    " - ".join((str(self.proc_entry.text()),
                                str(self.desc_entry.text()))),
                    int(self.stat_choice.currentIndex()),
                    int(self.cat_choice.currentIndex()),
                    str(self.id_text.text()))
                # ook nieuwe entry maken in de visuele tree
                new_item = qtw.QTreeWidgetItem()
                new_item.setData(0, self.parent.current_item, core.Qt.UserRole)
                self.parent.page0.p0list.addTopLevelItem(new_item)
                self.parent.page0.p0list.setCurrentItem(new_item)
                self.parent.newitem = False
                self.parent.rereadlist = True
                self.parent.page0.enable_buttons(True)
            # teksten op panel 0 bijwerken
            self.parent.page0.p0list.currentItem().setText(
                1, self.parent.pagedata.get_soorttext()[0].upper())
            self.parent.page0.p0list.currentItem().setText(
                2, self.parent.pagedata.get_statustext())
            self.parent.page0.p0list.currentItem().setText(
                3, self.parent.pagedata.updated)
            if self.parent.parent.datatype == DataType.XML.name:
                self.parent.page0.p0list.currentItem().setText(
                    4, self.parent.pagedata.titel)
            elif self.parent.parent.datatype == DataType.SQL.name:
                self.parent.page0.p0list.currentItem().setText(
                    4, self.parent.pagedata.over)
                self.parent.page0.p0list.currentItem().setText(
                    5, self.parent.pagedata.titel)
            self.oldbuf = (str(self.proc_entry.text()), str(self.desc_entry.text()),
                           int(self.stat_choice.currentIndex()),
                           int(self.cat_choice.currentIndex()))
        return True

    def archiveer(self):
        "archiveren/herleven"
        self.parch = not self.parch
        self.savep()
        self.parent.rereadlist = True
        self.vulp()

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

    def get_entry_text(self, entry_type):  # methode van Page1Gui
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


class Page6Gui(PageGui):
    "pagina 6: voortgang"
    def __init__(self, parent):
        Page.__init__(self, parent, pageno=6, standard=False)
        self.current_item = 0
        self.oldtext = ""
        ## sizes = 200, 100 if LIN else 280, 110
        sizes = 350, 100 if LIN else 280, 110
        self.pnl = qtw.QSplitter(self)
        self.pnl.setOrientation(core.Qt.Vertical)

        self.progress_list = qtw.QListWidget(self)
        self.progress_list.currentItemChanged.connect(self.on_select_item)
        self.new_action = qtw.QShortcut('Shift+Ctrl+N', self)
        if self.parent.parent.datatype == DataType.XML.name:
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
        if self.parent.parent.datatype == DataType.SQL.name:
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
            if self.parent.parent.datatype == DataType.XML.name:
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
        if item is None or data2int(item.data(core.Qt.UserRole)) == -1:
            datum, self.oldtext = get_dts(), ''
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


class SortOptionsGui(qtw.QDialog):
    """dialoog om de sorteer opties in te stellen
    """
    _asc_id = 1
    _desc_id = 2

    def __init__(self, parent):
        self.parent = parent
        self.sortopts = {}
        self._data = None

        lijst = []
        if self.parent.parent.parent.datatype == DataType.SQL.name:
            try:
                lijst = [x[0] for x in dmls.SORTFIELDS]
            except AttributeError:
                pass
        if not lijst:
            lijst = [x for x in parent.parent.ctitels]
            lijst[1] = "Soort"
        lijst.insert(0, "(geen)")
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
        self.on_off.setChecked(self.parent.sort_via_options)
        if self.parent.parent.parent.datatype == DataType.SQL.name:
            self.sortopts = self.parent._data.load_options()
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
        if self.parent.parent.parent.datatype == DataType.XML.name:
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
        if via_options == self.parent.sort_via_options and new_sortopts == self.sortopts:
            qtw.QMessageBox.information(self, 'Probreg', 'U heeft niets gewijzigd')
            return
        self.parent.sort_via_options = via_options
        if via_options:
            if self.parent._data:      # alleen SQL versie
                self.parent._data.save_options(new_sortopts)
        super().accept()


class SelectOptionsGui(qtw.QDialog):
    """dialoog om de selectie op te geven

    sel_args is de dictionary waarin de filterwaarden zitten, bv:
    {'status': ['probleem'], 'idlt': '2006-0009', 'titel': 'x', 'soort': ['gemeld'],
     'id': 'and', 'idgt': '2005-0019'}
    voor de Django versie is deze overbodig want de selectie ligt vast in de database
    """
    def __init__(self, parent, sel_args):
        self.parent = parent
        self.datatype = self.parent.parent.parent.datatype
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

        if self.datatype == DataType.XML.name:
            self.check_options.addButton(qtw.QCheckBox(parent.parent.ctitels[4] +
                                                       '   -', self))
            self.text_zoek = qtw.QLineEdit(self)
            self.text_zoek.textChanged.connect(functools.partial(self.on_text, 'zoek'))
        elif self.datatype == DataType.SQL.name:
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

        self.set_defaults(sel_args)
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
        if self.datatype == DataType.XML.name:
            hbox.addWidget(qtw.QLabel('zoek naar:', self))
            hbox.addWidget(self.text_zoek)
        elif self.datatype == DataType.SQL.name:
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

    def set_defaults(self, sel_args):
        """get search settings and present them in the dialog
        """
        test = self.parent.parent.fnaam
        self._data = None
        if self.parent.parent.parent.datatype == DataType.SQL.name:
            self._data = dmls.SelectOptions(test, self.parent.parent.parent.user)
            args, sel_args = self._data.load_options(), {}
            for key, value in args.items():
                if key == 'nummer':
                    for item in value:  # splitsen in idgt, id en idlt
                        if len(item) == 1:
                            sel_args['id'] = 'and' if item[0] == 'en' else 'or'
                        elif item[1] == 'GT':
                            sel_args['idgt'] = item[0]
                        elif item[1] == 'LT':
                            sel_args['idlt'] = item[0]
                # elif key == 'arch':
                #     sel_args[key] = {0: 'narch', 1: 'arch', 2: 'alles'}[value]
                elif value:
                    sel_args[key] = value
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

        if self.datatype == DataType.XML.name:
            itemindex = 1
        elif self.datatype == DataType.SQL.name:
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
        if self.datatype == DataType.XML.name:
            itemindex = 1
        elif self.datatype == DataType.SQL.name:
            itemindex = 2
        if self.check_options.buttons()[1].isChecked():
            selection = '(gefilterd)'
            if self.datatype == DataType.XML.name:
                lst = [self.parent.parent.cats[x][itemindex]
                       for x in range(len(self.parent.parent.cats.keys()))
                       if self.check_cats.buttons()[x].isChecked()]
            elif self.datatype == DataType.SQL.name:
                lst = [self.parent.parent.cats[x][itemindex]
                       for x in range(len(self.parent.parent.cats.keys()))
                       if self.check_cats.buttons()[x].isChecked()]
            if lst:
                sel_args["soort"] = lst
        if self.check_options.buttons()[2].isChecked():
            selection = '(gefilterd)'
            if self.datatype == DataType.XML.name:
                lst = [self.parent.parent.stats[x][itemindex]
                       for x in range(len(self.parent.parent.stats.keys()))
                       if self.check_stats.buttons()[x].isChecked()]
            elif self.datatype == DataType.SQL.name:
                lst = [self.parent.parent.stats[x][itemindex]
                       for x in range(len(self.parent.parent.stats.keys()))
                       if self.check_stats.buttons()[x].isChecked()]
            if lst:
                sel_args["status"] = lst
        if self.check_options.buttons()[3].isChecked():
            selection = '(gefilterd)'
            if self.datatype == DataType.XML.name:
                sel_args["titel"] = str(self.text_zoek.text())
            elif self.datatype == DataType.SQL.name:
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
        self.parent.selection = selection
        self.parent.sel_args = sel_args
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
            if self.parent.datatype == DataType.XML.name:
                item_text, item_value = self.parent.book.stats[key]
                self.data.append(": ".join((item_value, item_text)))
            elif self.parent.datatype == DataType.SQL.name:
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
            if self.parent.datatype == DataType.XML.name:
                item_value, item_text = self.parent.book.cats[key]
                self.data.append(": ".join((item_text, item_value)))
            elif self.parent.datatype == DataType.SQL.name:
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


class LoginBoxGui(qtw.QDialog):
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
        test = dmls.validate_user(self.t_username.text(),
                                  self.t_password.text(),
                                  self.parent.filename)
        if not test:
            qtw.QMessageBox.information(self, self.parent.title, 'Login failed')
            return
        qtw.QMessageBox.information(self, self.parent.title, 'Login accepted')
        self.parent.dialog_data = test
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

    def create_menu(self):
        """Create application menu
        """
        return  # skip for now
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

    def create_book(self, pnl):
        """define the tabbed interface and its subclasses
        """
        self.book = qtw.QTabWidget(pnl)
        self.book.resize(300, 300)
        self.book.parent = self
        return  # skip rest for now
        self.book.fnaam = ""
        if self.filename and self.datatype == DataType.SQL.name:
            self.book.fnaam = self.filename
        self.book.sorter = None
        self.book.current_item = None
        self.book.data = {}
        self.book.rereadlist = True
        self.lees_settings()
        self.book.ctitels = ["actie", " ", "status", "L.wijz."]
        if self.datatype == DataType.XML.name:
            self.book.ctitels.append("titel")
        elif self.datatype == DataType.SQL.name:
            self.book.ctitels.extend(("betreft", "omschrijving"))
        self.book.current_tab = -1
        self.book.newitem = False
        self.book.pagedata = None
        self.book.textcallbacks = {}

        self.book.page0 = Page0(self.book)
        self.book.page1 = Page1(self.book)
        self.book.page2 = Page(self.book, 2)
        self.book.page3 = Page(self.book, 3)
        self.book.page4 = Page(self.book, 4)
        self.book.page5 = Page(self.book, 5)
        self.book.page6 = Page6(self.book)
        self.book.pages = 7
        self.book.checked_for_leaving = True
        self.book.currentChanged.connect(self.on_page_changing)

        self.book.addTab(self.book.page0, "&" + self.book.tabs[0])
        self.book.page0.doelayout()
        self.book.addTab(self.book.page1, "&" + self.book.tabs[1])
        self.book.page1.doelayout()
        self.book.addTab(self.book.page2, "&" + self.book.tabs[2])
        self.book.page2.doelayout()
        self.book.addTab(self.book.page3, "&" + self.book.tabs[3])
        self.book.page3.doelayout()
        self.book.addTab(self.book.page4, "&" + self.book.tabs[4])
        self.book.page4.doelayout()
        self.book.addTab(self.book.page5, "&" + self.book.tabs[5])
        self.book.page5.doelayout()
        self.book.addTab(self.book.page6, "&" + self.book.tabs[6])
        self.book.page6.doelayout()
        for i in range(1, self.book.count()):
            self.book.setTabEnabled(i, False)

    def go(self):
        """realize the screen layout and start application
        """
        pnl = qtw.QFrame(self)
        self.setCentralWidget(pnl)
        self.toolbar = None
        self.create_book(pnl)
        sizer0 = qtw.QVBoxLayout()
        sizer0.addWidget(self.book)
        sizer1 = qtw.QHBoxLayout()
        sizer1.addStretch()
        self.exit_button = qtw.QPushButton('&Quit', pnl)
        self.exit_button.clicked.connect(self.master.exit_app)
        sizer1.addWidget(self.exit_button)
        sizer1.addStretch()
        sizer0.addLayout(sizer1)
        pnl.setLayout(sizer0)
        self.show()
        # self.zetfocus(0)
        sys.exit(self.app.exec_())

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

    def not_implemented_message(self):
        "information"
        qtw.QMessageBox.information(self, "Oeps", "Sorry, werkt nog niet")

    def disable_all_book_tabs(self):
        for i in range(1, self.master.book.count()):
            self.book.setTabEnabled(i, False)

    def print_actie(self):
        "Menukeuze: print deze actie"
        if self.book.pagedata is None or self.book.newitem:
            qtw.QMessageBox.information(self, self.parent.parent.title,
                                        "Wel eerst een actie kiezen om te printen")
            return
        self.hdr = ("Actie: {} {}".format(self.book.pagedata.id, self.book.pagedata.titel))
        tekst = self.book.pagedata.titel
        try:
            oms, tekst = tekst.split(" - ", 1)
        except ValueError:
            try:
                oms, tekst = tekst.split(": ", 1)
            except ValueError:
                oms = ''
        srt = "(onbekende soort)"
        for oms, code in self.book.cats.values():
            if code == self.book.pagedata.soort:
                srt = oms
                break
        stat = "(onbekende status)"
        for oms, code in self.book.stats.values():
            if code == self.book.pagedata.status:
                stat = oms
                break
        self.printdict = {'lijst': [],
                          'actie': self.book.pagedata.id,
                          'datum': self.book.pagedata.datum,
                          'oms': oms,
                          'tekst': tekst,
                          'soort': srt,
                          'status': stat}
        empty = "(nog niet beschreven)"
        sections = [[title.split(None, 1)[1], ''] for key, title in
                    self.book.tabs.items() if key > 2]
        sections[0][1] = self.book.pagedata.melding.replace('\n', '<br>') or empty
        sections[1][1] = self.book.pagedata.oorzaak.replace('\n', '<br>') or empty
        sections[2][1] = self.book.pagedata.oplossing.replace('\n', '<br>') or empty
        sections[3][1] = self.book.pagedata.vervolg.replace('\n', '<br>') or ''
        if not sections[3][1]:
            sections.pop()
        self.printdict['sections'] = sections
        self.printdict['events'] = [(x, y.replace('\n', '<br>')) for x, y in
                                    self.book.pagedata.events] or []
        self.preview()

    def exit(self):
        "Menukeuze: exit applicatie"
        self.close()    # enough for now

    def tab_settings(self):
        "Menukeuze: settings - data - tab titels"
        TabOptions(self, "Wijzigen tab titels", size=(350, 200)).exec_()

    def stat_settings(self):
        "Menukeuze: settings - data - statussen"
        StatOptions(self, "Wijzigen statussen", size=(350, 200)).exec_()

    def cat_settings(self):
        "Menukeuze: settings - data - soorten"
        CatOptions(self, "Wijzigen categorieen", size=(350, 200)).exec_()

    def font_settings(self):
        "Menukeuze: settings - applicatie - lettertype"
        self.not_implemented_message()

    def colour_settings(self):
        "Menukeuze: settings - applicatie - kleuren"
        self.not_implemented_message()

    def hotkey_settings(self):
        "Menukeuze: settings - applicatie- hotkeys (niet geactiveerd)"
        self.not_implemented_message()

    def about_help(self):
        "Menukeuze: help - about"
        qtw.QMessageBox.information(self, 'Help',
                                    "PyQt4 versie van mijn actiebox")

    def hotkey_help(self):
        "menukeuze: help - keys"
        if not self.helptext:
            help = ["=== Albert's actiebox ===\n",
                    "Keyboard shortcuts:",
                    "    Alt left/right: verder - terug",
                    "    Alt-0 t/m Alt-6: naar betreffende pagina",
                    "    Alt-O op tab 1: S_o_rteren",
                    "    Alt-I op tab 1: F_i_lteren",
                    "    Alt-G of Enter op tab 1: _G_a naar aangegeven actie",
                    "    Alt-N op elke tab: _N_ieuwe actie opvoeren",
                    "    Ctrl-P: _p_rinten (scherm of actie)",
                    "    Shift-Ctrl-P: print scherm:",
                    "    Alt-Ctrl-P: print actie",
                    "    Ctrl-Q: _q_uit actiebox",
                    "    Ctrl-H: _h_elp (dit scherm)",
                    "    Ctrl-S: gegevens in het scherm op_s_laan",
                    "    Ctrl-G: oplaan en _g_a door naar volgende tab",
                    "    Ctrl-Z in een tekstveld: undo",
                    "    Shift-Ctrl-Z in een tekstveld: redo",
                    "    Alt-Ctrl-Z overal: wijzigingen ongedaan maken",
                    "    Shift-Ctrl-N op tab 6: nieuwe regel opvoeren",
                    "    Ctrl-up/down op tab 6: move in list"]
            if self.datatype == DataType.XML.name:
                help.insert(8, "    Ctrl-O: _o_pen een (ander) actiebestand")
                help.insert(8, "    Ctrl-N: maak een _n_ieuw actiebestand")
            elif self.datatype == DataType.SQL.name:
                help.insert(8, "    Ctrl-O: selecteer een (ander) pr_o_ject")
            self.helptext = "\n".join(help)
        qtw.QMessageBox.information(self, 'Help', self.helptext)

    def silly_menu(self):
        "Menukeuze: settings - het leven"
        qtw.QMessageBox.information(self, 'Haha', "Yeah you wish...\n"
                                    "Het leven is niet in te stellen helaas")

    def startfile(self):
        "initialisatie t.b.v. nieuw bestand"
        if self.datatype == DataType.XML.name:
            fullname = self.dirname / self.filename
            retval = dmlx.checkfile(fullname, self.is_newfile)
            if retval != '':
                qtw.QMessageBox.information(self, "Oeps", retval)
                return retval
            self.book.fnaam = fullname
            self.title = self.filename
        elif self.datatype == DataType.SQL.name:
            self.book.fnaam = self.title = self.filename
        self.book.rereadlist = True
        self.book.sorter = None
        self.lees_settings()
        for x in self.book.tabs.keys():
            self.book.setTabText(x, self.book.tabs[x])
        self.book.page0.sel_args = {}
        self.book.page1.vul_combos()
        if self.book.current_tab == 0:
            self.book.page0.vulp()
        else:
            self.book.setCurrentIndex(0)
        self.book.checked_for_leaving = True

    def lees_settings(self):
        """instellingen (tabnamen, actiesoorten en actiestatussen) inlezen"""
        try:
            data = Settings[self.datatype](self.book.fnaam)
        except (DataError, KeyError):
            raise
        ## print(data.meld)     # "Standaard waarden opgehaald"
        self.imagecount = data.imagecount
        self.book.stats = {}
        self.book.cats = {}
        self.book.tabs = {}
        self.book.pagehelp = ["Overzicht van alle acties",
                              "Identificerende gegevens van de actie",
                              "Beschrijving van het probleem of wens",
                              "Analyse van het probleem of wens",
                              "Voorgestelde oplossing",
                              "Eventuele vervolgactie(s)",
                              "Overzicht stand van zaken"]
        for item_value, item in data.stat.items():
            if self.datatype == DataType.XML.name:
                item_text, sortkey = item
                self.book.stats[int(sortkey)] = (item_text, item_value)
            elif self.datatype == DataType.SQL.name:
                item_text, sortkey, row_id = item
                self.book.stats[int(sortkey)] = (item_text, item_value, row_id)
        for item_value, item in data.cat.items():
            if self.datatype == DataType.XML.name:
                item_text, sortkey = item
                self.book.cats[int(sortkey)] = (item_text, item_value)
            elif self.datatype == DataType.SQL.name:
                item_text, sortkey, row_id = item
                self.book.cats[int(sortkey)] = (item_text, item_value, row_id)
        for tab_num, tab_text in data.kop.items():
            if self.datatype == DataType.XML.name:
                self.book.tabs[int(tab_num)] = " ".join((tab_num, tab_text))
            elif self.datatype == DataType.SQL.name:
                tab_text, tab_adr = tab_text
                self.book.tabs[int(tab_num)] = " ".join((tab_num, tab_text.title()))

    def save_settings(self, srt, data):
        """instellingen (tabnamen, actiesoorten of actiestatussen) terugschrijven

        argumenten: soort, data
        data is een dictionary die in een van de dialogen TabOptions, CatOptions
        of StatOptions wordt opgebouwd"""
        settings = Settings[self.datatype](self.book.fnaam)
        if srt == "tab":
            settings.kop = data
            settings.write()
            self.book.tabs = {}
            for item_value, item_text in data.items():
                item = " ".join((item_value, item_text))
                self.book.tabs[int(item_value)] = item
                self.book.setTabText(int(item_value), item)
        elif srt == "stat":
            settings.stat = data
            settings.write()
            self.book.stats = {}
            for item_value, item in data.items():
                if self.datatype == DataType.XML.name:
                    item_text, sortkey = item
                    self.book.stats[sortkey] = (item_text, item_value)
                elif self.datatype == DataType.SQL.name:
                    item_text, sortkey, row_id = item
                    self.book.stats[sortkey] = (item_text, item_value, row_id)
        elif srt == "cat":
            settings.cat = data
            settings.write()
            self.book.cats = {}
            for item_value, item in data.items():
                if self.datatype == DataType.XML.name:
                    item_text, sortkey = item
                    self.book.cats[sortkey] = (item_text, item_value)
                elif self.datatype == DataType.SQL.name:
                    item_text, sortkey, row_id = item
                    self.book.cats[sortkey] = (item_text, item_value, row_id)
        self.book.page1.vul_combos()

    def on_page_changing(self, newtabnum):
        """deze methode is bedoeld om wanneer er van pagina gewisseld gaat worden
        te controleren of dat wel mogelijk is en zo niet, te melden waarom en de
        paginawissel tegen te houden (ok, terug te gaan naar de vorige pagina).
        PyQT4 kent geen aparte beforechanging methode, daarom is deze methode
        tevens bedoeld om ervoor te zorgen dat na het wisselen
        van pagina het veld / de velden van de nieuwe pagina een waarde krijgen
        met behulp van de vulp methode
        """
        old = self.book.current_tab
        new = self.book.current_tab = self.book.currentIndex()
        if LIN and old == -1:  # bij initialisatie en bij afsluiten - op Windows is deze altijd -1?
            return
        for i in range(self.book.count()):
            if i != self.book.current_tab:
                self.book.setTabEnabled(i, True)
        if new == 0:
            self.book.page0.vulp()
        elif new == 1:
            self.book.page1.vulp()
        elif new == 2:
            self.book.page2.vulp()
        elif new == 3:
            self.book.page3.vulp()
        elif new == 4:
            self.book.page4.vulp()
        elif new == 5:
            self.book.page5.vulp()
        elif new == 6:
            if old == new:
                item = self.book.page6.progress_list.currentRow()  # remember current item
            self.book.page6.vulp()
            if old == new:
                self.book.page6.progress_list.setCurrentRow(item)  # reselect item
        self.zetfocus(self.book.current_tab)

    def zetfocus(self, tabno):
        "focus geven aan de gekozen tab"
        if tabno == 0:
            self.book.page0.p0list.setFocus()
        elif tabno == 1:
            self.book.page1.proc_entry.setFocus()
        elif tabno == 2:
            self.book.page2.text1.setFocus()
        elif tabno == 3:
            self.book.page3.text1.setFocus()
        elif tabno == 4:
            self.book.page4.text1.setFocus()
        elif tabno == 5:
            self.book.page5.text1.setFocus()
        elif tabno == 6:
            self.book.page6.progress_list.setFocus()

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

    def set_statusmessage(self, msg=''):
        """stel tekst in statusbar in
        """
        if not msg:
            msg = self.book.pagehelp[self.book.current_tab]
            if self.book.current_tab == 0:
                msg += ' - {} items'.format(len(self.book.data))
        self.statusmessage.setText(msg)
        if self.datatype == DataType.SQL.name:
            if self.user:
                msg = 'Aangemeld als {}'.format(self.user.username)
            else:
                msg = 'Niet aangemeld'
        self.showuser.setText(msg)

    def sign_in(self):
        """aanloggen in SQL/Django mode
        """
        dlg = LoginBox(self)
        dlg.exec_()
        if self.dialog_data:
            self.user, self.is_user, self.is_admin = self.dialog_data
            self.book.rereadlist = True
            self.on_page_changing(0)