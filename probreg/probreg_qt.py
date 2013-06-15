#! usr/bin/env python
# -*- coding: UTF-8 -*-
"""Actie (was: problemen) Registratie, GUI versie
"""
from __future__ import print_function

import sys, os
LIN = True if os.name == 'posix' else False
from datetime import datetime
import pprint
import images
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
import logging
import functools
from mako.template import Template
import pr_globals as pr
XML_VERSION = SQL_VERSION = False
sortorder = {"A": core.Qt.AscendingOrder, "D": core.Qt.DescendingOrder}

def get_dts():
    "routine om een geformatteerd date/time stamp te verkrijgen"
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class Page(gui.QFrame):
    "base class for notebook page"
    def __init__(self, parent, standard=True): # Done
        self.parent = parent
        gui.QFrame.__init__(self, parent)
        if not standard:
            return
        high = 330 if LIN else 430
        self.text1 = gui.QTextEdit(self)
        self.text1.resize(490, high)
        self.text1.textChanged.connect(self.on_text)
        self.save_button = gui.QPushButton('Sla wijzigingen op (Ctrl-S)', self)
        self.save_button.clicked.connect(self.savep)
        action = gui.QShortcut('Ctrl+S', self, self.savepfromkey)
        self.saveandgo_button = gui.QPushButton('Sla op en ga verder (Ctrl-G)', self)
        self.saveandgo_button.clicked.connect(self.savepgo)
        action = gui.QShortcut('Ctrl+G', self, self.savepgofromkey)
        self.cancel_button = gui.QPushButton('Zet originele tekst terug (Alt-Ctrl-Z)',
            self)
        self.cancel_button.clicked.connect(self.restorep)
        action = gui.QShortcut('Alt+Ctrl+Z', self, self.restorep) # Ctrl-Z zit al in text control
        action = gui.QShortcut('Alt+N', self, self.nieuwp)

    def doelayout(self): # Done
        "layout page"
        sizer0 = gui.QVBoxLayout()
        sizer1 = gui.QVBoxLayout()
        sizer1.addWidget(self.text1)
        sizer0.addLayout(sizer1)
        sizer2 = gui.QHBoxLayout()
        sizer2.addStretch()
        sizer2.addWidget(self.save_button)
        sizer2.addWidget(self.saveandgo_button)
        sizer2.addWidget(self.cancel_button)
        sizer2.addStretch()
        sizer0.addLayout(sizer2)
        self.setLayout(sizer0)
        return True

    def vulp(self, evt=None): # Done, seems to work
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina"""
        self.initializing = True
        self.enable_buttons(False)
        if self.parent.current_tab == 0:
            text = self.seltitel
        else:
            text = self.parent.tabs[self.parent.current_tab].split(None,1)
            if self.parent.pagedata:
                text = str(self.parent.pagedata.id) + ' ' + self.parent.pagedata.titel
        self.parent.parent.setWindowTitle("{} | {}".format(self.parent.parent.title,
            text))
        self.parent.parent.sbar.showMessage(
            self.parent.pagehelp[self.parent.current_tab])
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
                ## if self.parent.pagedata.arch:
                    ## self.text1.setReadOnly(True)
                ## else:
                    ## self.text1.setReadOnly(False)
                self.text1.setReadOnly(self.parent.pagedata.arch)
            self.text1.setText(self.oldbuf)
        self.initializing = False
        self.parent.checked_for_leaving = True

    def readp(self, pid): # Done, seems to work
        "lezen van een actie"
        self.parent.pagedata = Actie(self.parent.fnaam, pid)
        self.parent.old_id = self.parent.pagedata.id
        self.parent.newitem = False

    def nieuwp(self, evt=None): # Done, seems to work
        """voorbereiden opvoeren nieuwe actie"""
        if self.leavep():
            self.parent.pagedata = Actie(self.parent.fnaam, 0)
            self.parent.newitem = True
            if self.parent.current_tab == 1:
                self.vulp() # om de velden leeg te maken
                self.proc_entry.setFocus()
            else:
                self.goto_page(1, check=False)
        else:
            print("leavep() geeft False: nog niet klaar met huidige pagina")

    def hideEvent(self, event):
        if self.parent.current_tab != -1:
            print('deciding to ignore hideEvent', event.type())
            if not self.parent.parent.mag_weg:
                print('ignoring...')
                event.ignore()
                ## return False
        self.hide_show_event(event)
        return gui.QFrame.hideEvent(self, event)
        return True

    def showEvent(self, event):
        if self.parent.current_tab != -1:
            print('deciding to ignore showEvent', event.type())
            if not self.parent.parent.mag_weg:
                print('ignoring...')
                event.ignore()
                ## return False
        return gui.QFrame.showEvent(self, event)
        return True

    ## def event(self, event):
    def hide_show_event(self, event):
        ## print("in {}.event: {}".format(self.__class__, event.type()))
        ## test = event.type()
        ## if test in (core.QEvent.HideToParent, core.QEvent.ShowToParent,
                ## core.QEvent.Show) and self.parent.current_tab != -1:
            ## print('deciding to ignore event', test)
            ## if not self.parent.parent.mag_weg:
                ## print('ignoring...')
                ## core.QEvent.ignore(event)
                ## return False
        ## elif test != core.QEvent.Hide:
            ## gui.QFrame.event(self, event)
            ## return True
        msg = ""
        print("in hideEvent for tab", self.parent.current_tab)
        if self.parent.current_tab == -1 or self.parent.parent.initializing:
            pass
        elif self.parent.fnaam == "":
            if XML_VERSION:
                wat = 'bestand'
            elif SQL_VERSION:
                wat = 'project'
            msg = "Kies eerst een {} om mee te werken".format(wat)
            self.parent.parent.mag_weg = False
        elif len(self.parent.data) == 0 and not self.parent.book.newitem:
            msg = "Voer eerst één of meer acties op"
            self.parent.parent.mag_weg = False
        elif self.parent.current_item == -1 and not self.parent.book.newitem:
            msg = "Selecteer eerst een actie"
            self.parent.parent.mag_weg = False
        print('going to check for leaving', self.parent.checked_for_leaving)
        if not self.parent.checked_for_leaving:
            self.parent.parent.mag_weg = True
            if self.parent.current_tab == 0:
                self.parent.parent.mag_weg = self.parent.page0.leavep()
            elif self.parent.current_tab == 1:
                self.parent.parent.mag_weg = self.parent.page1.leavep()
            elif self.parent.current_tab == 2:
                self.parent.parent.mag_weg = self.parent.page2.leavep()
            elif self.parent.current_tab == 3:
                self.parent.parent.mag_weg = self.parent.page3.leavep()
            elif self.parent.current_tab == 4:
                self.parent.parent.mag_weg = self.parent.page4.leavep()
            elif self.parent.current_tab == 5:
                self.parent.parent.mag_weg = self.parent.page5.leavep()
            elif self.parent.current_tab == 6:
                self.parent.mag_weg = self.parent.page6.leavep()
        print('determined if we can leave', self.parent.parent.mag_weg)
        if not self.parent.parent.mag_weg:
            if msg != "":
                gui.QMessageBox.information(self, "Navigatie niet toegestaan", msg)
                ## self.book.setCurrent(self.book.current_tab)
            event.ignore()
            ## return False
        ## else:
            ## gui.QFrame.event(self, event)
        return self.parent.parent.mag_weg

    def leavep(self): # Done, untested
        "afsluitende acties uit te voeren alvorens de pagina te verlaten"
        print('leavep for page', self.parent.current_tab)
        if self.parent.current_tab == 1:
            newbuf = (str(self.proc_entry.text()), str(self.desc_entry.text()),
                int(self.stat_choice.currentIndex()),
                int(self.cat_choice.currentIndex()))
            if self.parent.newitem and newbuf[0] == "" and newbuf[1] == "" \
                    and not self.parent.parent.exiting:
                self.parent.newitem = False
                self.parent.pagedata = Actie(self.parent.fnaam, self.parent.old_id)
        elif self.parent.current_tab == 6:
            newbuf = (self.event_list, self.event_data)
        elif self.parent.current_tab > 1:
            newbuf = self.text1.toPlainText()
        ok_to_leave = True
        self.parent.checked_for_leaving = True
        if self.parent.current_tab > 0 and newbuf != self.oldbuf:
            retval = gui.QMessageBox.question(self, self.parent.parent.title,
                "\n".join(("De gegevens op de pagina zijn gewijzigd, ",
                "wilt u de wijzigingen opslaan voordat u verder gaat?")),
                buttons = gui.QMessageBox.Yes | gui.QMessageBox.No |
                gui.QMessageBox.Cancel)
            if retval == gui.QMessageBox.Yes:
                ok_to_leave = self.savep()
            elif retval == gui.QMessageBox.Cancel:
                self.parent.checked_for_leaving = ok_to_leave = False
        return ok_to_leave

    def savep(self, evt=None): # Done
        "gegevens van een actie opslaan afhankelijk van pagina"
        self.enable_buttons(False)
        if self.parent.current_tab <= 1 or self.parent.current_tab == 6:
            return
        wijzig = False
        text = str(self.text1.toPlainText())
        if self.parent.current_tab == 2 and text != self.parent.pagedata.melding:
            self.oldbuf = self.parent.pagedata.melding = text
            self.parent.pagedata.events.append((get_dts(),"Meldingtekst aangepast"))
            wijzig = True
        if self.parent.current_tab == 3 and text != self.parent.pagedata.oorzaak:
            self.oldbuf = self.parent.pagedata.oorzaak = text
            self.parent.pagedata.events.append((get_dts(),"Beschrijving oorzaak aangepast"))
            wijzig = True
        if self.parent.current_tab == 4 and text != self.parent.pagedata.oplossing:
            self.oldbuf = self.parent.pagedata.oplossing = text
            self.parent.pagedata.events.append((get_dts(),"Beschrijving oplossing aangepast"))
            wijzig = True
        if self.parent.current_tab == 5 and text != self.parent.pagedata.vervolg:
            self.oldbuf = self.parent.pagedata.vervolg = text
            self.parent.pagedata.events.append((get_dts(),"Tekst vervolgactie aangepast"))
            wijzig = True
        if wijzig:
            self.update_actie()
            self.parent.page0.p0list.currentItem().setText(3,
                self.parent.pagedata.updated)
        return True

    def savepgo(self, evt=None): # Done, untested
        "opslaan en naar de volgende pagina"
        if self.savep():
            self.goto_next()
        else:
            self.enable_buttons()
    def savepfromkey(self):
        if self.save_button.isEnabled():
            self.savep()

    def savepgofromkey(self):
            if self.saveandgo_button.isEnabled():
                self.savepgo()

    def restorep(self, evt=None): # Done, works
        "oorspronkelijke (laatst opgeslagen) inhoud van de pagina herstellen"
        self.vulp()

    def on_text(self, evt=None): # Done, works
        """callback voor EVT_TEXT

        de initializing flag wordt uitgevraagd omdat deze event ook tijdens vulp()
        en tijdens vul_combos plaatsvindt"""
        if not self.initializing:
            if self.parent.current_tab == 1:
                newbuf = (str(self.proc_entry.text()), str(self.desc_entry.text()),
                    int(self.stat_choice.currentIndex()),
                    int(self.cat_choice.currentIndex()))
            elif 1 < self.parent.current_tab < 6:
                newbuf = self.text1.toPlainText()
            elif self.parent.current_tab == 6:
                newbuf = (self.event_list, self.event_data)
            self.enable_buttons(newbuf != self.oldbuf)

    def on_choice(self, evt): # Done, untested
        "callback voor combobox"
        self.enable_buttons()

    def update_actie(self): # Done, untested
        ## self.parent.pagedata.list() # NB element 0 is leeg
        self.parent.pagedata.write()
        self.parent.checked_for_leaving = True
        self.mag_weg = True
        self.parent.pagedata.read()    # om "updated" attribuut op te halen

    def enable_buttons(self, state=True): # Done, works
        "buttons wel of niet klikbaar maken"
        if state:
            self.parent.checked_for_leaving = False
        self.save_button.setEnabled(state)
        if self.parent.current_tab < 6:
            self.saveandgo_button.setEnabled(state)
        self.cancel_button.setEnabled(state)

    def goto_actie(self, evt=None): # Done
        "naar startpagina actie gaan"
        self.goto_page(1)

    def goto_next(self): # Done, untested
        "naar de volgende pagina gaan"
        if not self.leavep():
            return
        next = self.parent.current_tab + 1
        if next > self.parent.pages:
            next = 0
        self.parent.setCurrentIndex(next)

    def goto_prev(self): # Done, untested
        "naar de vorige pagina gaan"
        next = self.parent.current_tab - 1
        if next < 0:
            next = self.parent.pages
        self.parent.setCurrentIndex(next)

    def goto_page(self, page_num, check=True): # Done, untested
        "naar de aangegeven pagina gaan"
        if check and not self.leavep():
            return
        if 0 <= page_num <= self.parent.pages:
            self.parent.setCurrentIndex(page_num)


class Page0(Page):
    "pagina 0: overzicht acties"
    def __init__(self, parent): # Done
        self.parent = parent
        Page.__init__(self, parent, standard=False)
        self.selection = 'excl. gearchiveerde'
        self.sel_args = {}

        widths = [94, 24, 146, 90, 400] if LIN else [64, 24, 114, 72, 292]
        ## if XML_VERSION:
            ## titels = self.parent.ctitels[:-1]
        if SQL_VERSION:
            ## titels = self.parent.ctitels
            widths[4] = 90 if LIN else 72
            extra = 310 if LIN else 220
            widths.append(extra)
        self.p0list = gui.QTreeWidget(self)
        ## high = 400 if LIN else 444
        ## self.p0list.SetMinSize((440,high))
        self.p0list.setSortingEnabled(True)
        self.p0list.setHeaderLabels(self.parent.ctitels)
        self.p0list.setAlternatingRowColors(True)
        self.p0hdr = self.p0list.header()
        self.p0hdr.setClickable(True)
        for indx, wid in enumerate(widths):
            self.p0hdr.resizeSection(indx, wid)
        self.p0hdr.setStretchLastSection(True)

        self.populate_list()

        self.sorted = (0, "A")

        self.p0list.itemActivated.connect(self.on_activate_item)
        self.p0list.currentItemChanged.connect(self.on_change_selected)

        self.sort_button = gui.QPushButton('S&Orteer', self)
        self.filter_button = gui.QPushButton('F&Ilter', self)
        self.go_button = gui.QPushButton('&Ga naar melding', self)
        self.archive_button = gui.QPushButton('&Archiveer', self)
        self.new_button = gui.QPushButton('Voer &Nieuwe melding op', self)
        self.sort_button.clicked.connect(self.sort_items)
        self.filter_button.clicked.connect(self.select_items)
        self.go_button.clicked.connect(self.goto_actie)
        self.archive_button.clicked.connect(self.archiveer)
        self.new_button.clicked.connect(self.nieuwp)

    def doelayout(self): # Done
        "layout page"
        sizer0 = gui.QVBoxLayout()
        sizer1 = gui.QHBoxLayout()
        sizer2 = gui.QHBoxLayout()
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

    ## def leavep(self):
        ## "afsluitende acties uit te voeren alvorens de pagina te verlaten"
        ## return True # niks doen, doorgaan

    def vulp(self, evt = None): # Done
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina"""
        self.seltitel = 'alle meldingen ' + self.selection
        Page.vulp(self)
        if self.parent.rereadlist:
            self.parent.data = {}
            select = self.sel_args.copy()
            arch = ""
            if "arch" in select:
                arch = select.pop("arch")
            try:
                data = get_acties(self.parent.fnaam, select, arch)
            except DataError as msg:
                print("samenstellen lijst mislukt: " + str(msg))
                raise
            else:
                for idx, item in enumerate(data):
                    ## print(item)
                    if XML_VERSION:
                        # nummer, start, stat, cat, titel, gewijzigd = item
                        self.parent.data[idx] = (item[0],
                                                 item[1],
                                                 ".".join((item[3][1], item[3][0])), \
                                                 ".".join((item[2][1], item[2][0])),
                                                 item[5],
                                                 item[4])
                    elif SQL_VERSION:
                        # nummer, start, stat_title, stat_value, cat_title, cat_value, \
                        # about, titel, gewijzigd = item
                        self.parent.data[idx] = (item[0],
                                                 item[1],
                                                 ".".join((item[5], item[4])), \
                                                 ".".join((str(item[3]), item[2])),
                                                 item[8],
                                                 item[6],
                                                 item[7])
            self.populate_list()
            self.p0list.sortItems(self.sorted[0], sortorder[self.sorted[1]]) #, True)
            self.parent.current_item = self.p0list.topLevelItem(0)
            self.parent.rereadlist = False
        self.parent.parent.setToolTip("{0} - {1} items".format(
            self.parent.pagehelp[self.parent.current_tab], len(self.parent.data)))
        if self.parent.current_item is not None:
            self.p0list.setCurrentItem(self.parent.current_item)
        self.p0list.scrollToItem(self.parent.current_item)

    def hideEvent(self, event):
        return Page.hideEvent(self, event)
    def showEvent(self, event):
        return Page.showEvent(self, event)

    def populate_list(self): # Done
        "list control vullen"
        ## self.p0list.blockSignals(True)
        self.p0list.clear()
        ## self.p0list.blockSignals(False)

        self.parent.rereadlist = False
        items = self.parent.data.items()
        if items is None or len(items) == 0:
            print('list is empty')
            return

        for key, data in items:
            if XML_VERSION:
                actie, _, soort, status, l_wijz, titel = data
            elif SQL_VERSION:
                actie, _, soort, status, l_wijz, over, titel = data
                l_wijz = l_wijz[:19]
            ## idx = self.p0list.InsertStringItem(sys.maxint, actie)
            new_item = gui.QTreeWidgetItem()
            new_item.setText(0, actie)
            new_item.setData(0, core.Qt.UserRole, actie if XML_VERSION else
                key if SQL_VERSION else '')
            pos = soort.index(".") + 1
            new_item.setText(1, soort[pos:pos+1].upper())
            pos = status.index(".") + 1
            new_item.setText(2, status[pos:])
            new_item.setText(3, l_wijz)
            if XML_VERSION:
                new_item.setText(4, titel)
            elif SQL_VERSION:
                new_item.setText(4, over)
                new_item.setText(5, titel)
            self.p0list.addTopLevelItem(new_item)
        self.colorize()

    def colorize(self): # Done,
        """de regels om en om kleuren"""
        return
        kleur = False
        for row in range(self.p0list.topLevelItemCount()):
            item = self.p0list.topLevelItem(row)
            for col in range(len(self.parent.ctitels)):
                if kleur:
                    item.setBackgroundColor(col, gui.QColor('#FCF090')) # core.Qt.yellow)
                else:
                    item.setBackgroundColor(col, core.Qt.white)
            kleur = not kleur

    def on_change_selected(self, item_n, item_o): # Done
        """callback voor wijzigen geselecteerd item, o.a. door verplaatsen van de
        cursor of door klikken"""
        print('selected item')
        print(item_n)
        print(self.p0list.currentItem())
        if item_n is None: # o.a. self.p0list.clear() veroorzaakt dit
            return
        self.parent.current_item = item_n # self.p0list.currentItem()
        ## for row in range(self.p0list.topLevelItemCount()):
            ## if self.p0list.topLevelItem(row) ==
        selindx = self.parent.current_item.data(0, core.Qt.UserRole).toPyObject()
        selindx = str(selindx) if XML_VERSION else int(selindx)
        self.readp(selindx)
        hlp = "&Herleef" if self.parent.pagedata.arch else "&Archiveer"
        self.archive_button.setText(hlp)

    def on_activate_item(self, item): # Done
        """callback voor activeren van item, door doubleclick of enter

        gek genoeg leidt een enter op een regel al tot het naar de volgende
        tab gaan (misschien door de on key afhandeling?)
        """
        print('activated item')
        print(item)
        print(self.p0list.currentItem())
        ## self.parent.current_item = self.p0list.currentItem()
        self.goto_actie()

    def sort_oncolumn(self, colno): # unnecessary, not connected?
        """callback voor klikken op column header

        het werkt ook zonder deze te connecten, maar ik meende dat het nodig was
        de sorteervolgorde te kennen en die is niet af te leiden vandaar een eigen
        instelling. Maar misschien heb ik dat wel helemaal niet nodig.
        """
        print('sort_oncolumn clicked with', colno, 'with current',
            self.p0list.sortColumn())
        column, order = self.sorted
        print('order is', column, order)
        ## if self.p0list.sortColumn == colno:
        if column == colno:
            order = 'A' if order == 'D' else 'D'
        else:
            order = 'A'
        print('reversing order',)
        self.sorted = colno, order
        print('order is now', colno, order)
        ## self.p0list.sortItems(self.sorted[0], sortorder[self.sorted[1]]) #, True)
        print('items resorted')
        ## self.p0hdr.setSortIndicator(colno, sortorder[self.sorted[1]])
        print('indicator reset')
        self.colorize()
        print('ready')

    def select_items(self, evt = None): # Done, untested
        """tonen van de selectie dialoog

        niet alleen selecteren op tekst(deel) maar ook op status, soort etc"""
        while True:
            test = SelectOptionsDialog(self, self.sel_args).exec_()
            if test != gui.QDialog.Accepted:
                break
            self.parent.rereadlist = True
            try:
                self.vulp()
            except DataError as msg:
                self.parent.rereadlist = False
                gui.QMessageBox.information(self, "Oeps", str(msg))
            else:
                break
        ## self.parent.parent.zetfocus(0)

    def sort_items(self, evt = None): # Done
        """tonen van de sorteer-opties dialoog

        sortering mogelijk op datum/tijd, soort, titel, status via schermpje met
        2x4 comboboxjes waarin je de volgorde van de rubrieken en de sorteervolgorde
        per rubriek kunt aangeven"""
        test = SortOptionsDialog(self).exec_()
        if test == gui.QDialog.Accepted:
            gui.QMessageBox.information(self, 'Oeps', "Sorry, werkt nog niet")
            # self.colorize() # formerly known as self.AfterSort()
        ## self.parent.parent.zetfocus(0)

    def archiveer(self, evt = None): # Done, untested
        "archiveren of herleven van het geselecteerde item"
        selindx = self.parent.current_item.data(0, core.Qt.UserRole).toPyObject()
        selindx = str(selindx) if XML_VERSION else int(selindx)
        self.readp(selindx)
        if XML_VERSION:
            self.parent.pagedata.arch = not self.parent.pagedata.arch
            hlp = "gearchiveerd" if self.parent.pagedata.arch else "herleefd"
            self.parent.pagedata.events.append((get_dts(), "Actie {0}".format(hlp)))
        elif SQL_VERSION:
            self.parent.pagedata.set_arch(not self.parent.pagedata.arch)
        self.update_actie() # self.parent.pagedata.write()
        self.parent.rereadlist = True
        self.vulp()
        self.parent.parent.zetfocus(0)
        # het navolgende geldt alleen voor de selectie "gearchiveerd en actief"
        if self.sel_args.get("arch", "") == "alles":
            self.p0list.scrollToItem(self.parent.current_item)
            hlp = "&Herleef" if self.parent.pagedata.arch else "&Archiveer"
            self.archive_button.setText(hlp)

    def enable_buttons(self, state = True): # Done
        "zorgen dat de gelijknamige methode van de base class niet wordt geactiveerd"
        pass

class Page1(Page):
    "pagina 1: startscherm actie"
    def __init__(self, parent): # Done
        Page.__init__(self, parent, standard=False)

        self.id_text = gui.QLineEdit(self)
        self.id_text.setMaximumWidth(120)
        self.date_text = gui.QLineEdit(self)
        self.date_text.setMaximumWidth(150)

        self.proc_entry = gui.QLineEdit(self)
        self.proc_entry.setMaximumWidth(150)
        self.proc_entry.textChanged.connect(self.on_text)
        self.desc_entry = gui.QLineEdit(self)
        self.desc_entry.setMaximumWidth(360)
        self.desc_entry.textChanged.connect(self.on_text)

        self.cat_choice = gui.QComboBox(self)
        self.cat_choice.setEditable(False)
        self.cat_choice.setMaximumWidth(180)
        self.cat_choice.currentIndexChanged.connect(self.on_text)
        self.stat_choice = gui.QComboBox(self)
        self.stat_choice.setEditable(False)
        self.id_text.setMaximumWidth(140)
        self.stat_choice.currentIndexChanged.connect(self.on_text)
        ## self.vul_combos()

        self.archive_text = gui.QLabel(self)
        self.archive_button = gui.QPushButton("Archiveren", self)
        self.archive_button.clicked.connect(self.archiveer)

        self.save_button = gui.QPushButton('Sla wijzigingen op (Ctrl-S)', self)
        self.save_button.clicked.connect(self.savep)
        action = gui.QShortcut('Ctrl+S', self, self.savepfromkey)
        self.saveandgo_button = gui.QPushButton('Sla op en ga verder (Ctrl-G)',
            self)
        self.saveandgo_button.clicked.connect(self.savepgo)
        action = gui.QShortcut('Ctrl+G', self, self.savepgofromkey)
        self.cancel_button = gui.QPushButton('Maak wijzigingen ongedaan (Alt-Ctrl-Z)',
            self)
        self.cancel_button.clicked.connect(self.restorep)
        action = gui.QShortcut('Alt+Ctrl+Z', self, self.restorep) # Ctrl-Z zit al in text control
        action = gui.QShortcut('Alt+N', self, self.nieuwp)

    def doelayout(self): # Done
        "layout page"
        sizer0 = gui.QVBoxLayout()
        sizer0.addSpacing(10)

        sizerx = gui.QHBoxLayout()
        sizerx.addSpacing(10)

        sizer1 = gui.QGridLayout() # rows, cols, hgap, vgap
        row = 0
        sizer1.setRowMinimumHeight(row, 10)
        sizer1.setColumnStretch(2, 1)
        row += 1
        sizer1.addWidget(gui.QLabel("Actie-id:", self), row, 0)
        sizer1.addWidget(self.id_text, row, 1)
        row += 1
        sizer1.setRowMinimumHeight(row, 5)
        row += 1
        sizer1.addWidget(gui.QLabel("Datum/tijd:", self), row, 0)
        sizer1.addWidget(self.date_text, row, 1)
        row += 1
        sizer1.setRowMinimumHeight(row, 5)
        row += 1
        sizer1.addWidget(gui.QLabel("Job/\ntransactie:", self), row, 0)
        sizer1.addWidget(self.proc_entry, row, 1)
        row += 1
        sizer1.setRowMinimumHeight(row, 5)
        row += 1
        sizer1.addWidget(gui.QLabel("Melding/code/\nomschrijving:", self), row, 0)
        sizer1.addWidget(self.desc_entry, row, 1, 1, 2)
        row += 1
        sizer1.setRowMinimumHeight(row, 5)
        row += 1
        sizer1.addWidget(gui.QLabel("Categorie:", self), row, 0)
        sizer1.addWidget(self.cat_choice, row, 1)
        row += 1
        sizer1.setRowMinimumHeight(row, 5)
        row += 1
        sizer1.addWidget(gui.QLabel("Status:", self), row, 0)
        sizer1.addWidget(self.stat_choice, row, 1)
        row += 1
        sizer1.setRowMinimumHeight(row, 5)
        row += 1
        sizery = gui.QHBoxLayout()
        sizery.addWidget(self.archive_text)
        sizery.addStretch()
        sizer1.addLayout(sizery, row, 1)
        row += 1
        sizery = gui.QHBoxLayout()
        sizery.addWidget(self.archive_button)
        sizery.addStretch()
        sizer1.addLayout(sizery, row, 1)

        sizerx.addLayout(sizer1)

        sizer0.addLayout(sizerx)

        sizer0.addStretch()

        sizer2 = gui.QHBoxLayout()
        sizer2.addStretch()
        sizer2.addWidget(self.save_button)
        sizer2.addWidget(self.saveandgo_button)
        sizer2.addWidget(self.cancel_button)
        sizer2.addStretch()
        sizer0.addLayout(sizer2)

        self.setLayout(sizer0)

    ## def event(self, event):
        ## print("in {}.event: {}".format(self.__class__, event.type()))
        ## return Page.event(self, event)
    def hideEvent(self, event):
        return Page.hideEvent(self, event)
    def showEvent(self, event):
        return Page.showEvent(self, event)

    def vulp(self, evt=None): # Done, untested
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina"""
        Page.vulp(self)
        print('vulp tab 1')
        self.initializing = True
        self.id_text.clear()
        self.date_text.clear()
        self.proc_entry.clear()
        self.desc_entry.clear()
        self.archive_text.setText("")
        self.cat_choice.setCurrentIndex(0)
        self.stat_choice.setCurrentIndex(0)
        self.parch = False
        if self.parent.pagedata is not None: # and not self.parent.newitem:
            self.id_text.setText(str(self.parent.pagedata.id))
            self.date_text.setText(self.parent.pagedata.datum)
            self.parch = self.parent.pagedata.arch
            if XML_VERSION:
                if self.parent.pagedata.titel is not None:
                    if " - " in self.parent.pagedata.titel:
                        hlp = self.parent.pagedata.titel.split(" - ", 1)
                    else:
                        hlp = self.parent.pagedata.titel.split(": ", 1)
                    self.proc_entry.setText(hlp[0])
                    if len(hlp) > 1:
                        self.desc_entry.setText(hlp[1])
            elif SQL_VERSION:
                self.proc_entry.setText(self.parent.pagedata.over)
                self.desc_entry.setText(self.parent.pagedata.titel)
            ## print(self.parent.pagedata.status)
            for x in range(len(self.parent.stats)):
                y = str(self.stat_choice.itemData(x).toPyObject())
                ## print(x, y)
                if y == self.parent.pagedata.status:
                    self.stat_choice.setCurrentIndex(x)
                    break
            ## print(self.parent.pagedata.soort)
            for x in range(len(self.parent.cats)):
                y = str(self.cat_choice.itemData(x).toPyObject())
                ## print(x, y)
                if y == self.parent.pagedata.soort:
                    self.cat_choice.setCurrentIndex(x)
                    break
        self.oldbuf = (str(self.proc_entry.text()), str(self.desc_entry.text()),
            int(self.stat_choice.currentIndex()), int(self.cat_choice.currentIndex()))
        ## self.initializing = False # gebeurt al in Page.vulp()?
        if self.parch:
            aanuit = False
            self.archive_text.setText("Deze actie is gearchiveerd")
            self.archive_button.setText("Herleven")
        else:
            aanuit = True
            self.archive_text.setText("")
            self.archive_button.setText("Archiveren")
        self.id_text.setEnabled(False)
        self.date_text.setEnabled(False)
        self.proc_entry.setEnabled(aanuit)
        self.desc_entry.setEnabled(aanuit)
        self.cat_choice.setEnabled(aanuit)
        self.stat_choice.setEnabled(aanuit)
        if self.parent.newitem:
            self.archive_button.setEnabled(False)
        else:
            self.archive_button.setEnabled(True)
        self.initializing = False

    def savep(self, evt=None): # Done, untested
        "opslaan van de paginagegevens"
        Page.savep(self)
        proc = str(self.proc_entry.text())
        ## try:
        proc = proc.capitalize() # [0].upper() + s1[1:]
        self.proc_entry.setText(proc)
        self.enable_buttons(False)
        ## except IndexError:
            ## pass
        desc = str(self.desc_entry.text())
        if proc == "" or desc == "":
            gui.QMessageBox.information(self, "Oeps",
                "Beide tekstrubrieken moeten worden ingevuld")
            return False
        wijzig = False
        if self.parent.newitem:
            self.parent.pagedata.events.append(
                (get_dts(), "Actie opgevoerd"))
        procdesc = " - ".join((proc, desc))
        if procdesc != self.parent.pagedata.titel:
            if XML_VERSION:
                self.parent.pagedata.titel = procdesc
            elif SQL_VERSION:
                self.parent.pagedata.over = proc
                self.parent.pagedata.titel = desc
            self.parent.pagedata.events.append(
                (get_dts(), 'Titel gewijzigd in "{0}"'.format(procdesc)))
            wijzig = True
        idx = self.stat_choice.currentIndex()
        newstat = str(self.stat_choice.itemData(idx).toPyObject())
        if newstat != self.parent.pagedata.status:
            self.parent.pagedata.status = newstat
            sel = str(self.stat_choice.currentText())
            self.parent.pagedata.events.append(
                (get_dts(), 'Status gewijzigd in "{0}"'.format(sel)))
            wijzig = True
        idx = self.cat_choice.currentIndex()
        newcat = str(self.cat_choice.itemData(idx).toPyObject())
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
                self.parent.current_item = len(self.parent.data) # + 1
                self.parent.data[self.parent.current_item] = (
                    str(self.date_text.text()),
                    " - ".join((str(self.proc_entry.text()),
                        str(self.desc_entry.text()))),
                    int(self.stat_choice.currentIndex()),
                    int(self.cat_choice.currentIndex()),
                    str(self.id_text.text()))
                self.parent.newitem = False
                self.parent.rereadlist = True
            self.parent.page0.p0list.currentItem().setText(1,
                self.parent.pagedata.get_soorttext()[0].upper()) # self.parent.pagedata.soort)[0][0].upper())
            self.parent.page0.p0list.currentItem().setText(2,
                self.parent.pagedata.get_statustext()) # self.parent.pagedata.status)[0])
            self.parent.page0.p0list.currentItem().setText(3,
                self.parent.pagedata.updated)
            self.parent.page0.p0list.currentItem().setText(4,
                self.parent.pagedata.titel)
            self.oldbuf = (str(self.proc_entry.text()), str(self.desc_entry.text()),
                int(self.stat_choice.currentIndex()),
                int(self.cat_choice.currentIndex()))
        return True

    def archiveer(self, evt=None): # Done, untested
        "archiveren/herleven"
        self.parch = not self.parch
        self.savep()
        self.parent.rereadlist = True
        self.vulp()
        ## self.goto_prev() # waarom? oorspronkelijk zou ik in dit geval terug naar de lijst

    def vul_combos(self): # Done
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

class Page6(Page):
    "pagina 6: voortgang"
    def __init__(self, parent): # Done (almost)
        Page.__init__(self, parent, standard=False)
        self.current_item = 0
        self.oldtext = ""
        sizes = 200, 100 if LIN else 280, 110
        self.pnl = gui.QSplitter(self)
        self.pnl.setOrientation(core.Qt.Vertical)

        self.progress_list = gui.QListWidget(self)
        ## self.resize=(500, high)
        self.progress_list.currentItemChanged.connect(self.on_select_item)
        self.progress_list.itemActivated.connect(self.on_activate_item)
        action = gui.QShortcut('Shift+Ctrl+N', self, functools.partial(
            self.on_activate_item, self.progress_list.item(0)))
        self.progress_text = gui.QTextEdit(self)
        ## self.resize(500, high)
        self.progress_text.textChanged.connect(self.on_text)
        self.pnl.addWidget(self.progress_list)
        self.pnl.addWidget(self.progress_text)
        ## self.pnl.setSizes(sizes)

        self.save_button = gui.QPushButton('Sla wijzigingen op (Ctrl-S)', self)
        self.save_button.clicked.connect(self.savep)
        action = gui.QShortcut('Ctrl+S', self, self.savepfromkey)
        ## self.saveandgo_button = gui.QPushButton('Sla op en ga verder (Ctrl-G)',
            ## self)
        ## self.saveandgo_button.clicked.connect(self.savepgo)
        ## action = gui.QShortcut('Ctrl+G', self, self.savepgofromkey)
        self.cancel_button = gui.QPushButton('Maak wijzigingen ongedaan (Alt-Ctrl-Z)',
            self)
        self.cancel_button.clicked.connect(self.restorep)
        action = gui.QShortcut('Alt+Ctrl+Z', self, self.restorep) # Ctrl-Z zit al in text control
        action = gui.QShortcut('Alt+N', self, self.nieuwp)
        action = gui.QShortcut('Ctrl+Up', self, self.goto_prev)
        action = gui.QShortcut('Ctrl+Down', self, self.goto_next)

    def doelayout(self):    # Done
        "layout page"
        sizer0 = gui.QVBoxLayout()
        sizer1 = gui.QHBoxLayout()
        sizer1.addWidget(self.pnl)
        sizer0.addLayout(sizer1)
        sizer2 = gui.QHBoxLayout()
        sizer2.addStretch()
        sizer2.addWidget(self.save_button)
        ## sizer2.addWidget(self.saveandgo_button)
        sizer2.addWidget(self.cancel_button)
        sizer2.addStretch()
        sizer0.addLayout(sizer2)
        self.setLayout(sizer0)

    ## def event(self, event):
        ## print("in {}.event: {}".format(self.__class__, event.type()))
        ## return Page.event(self, event)
    def hideEvent(self, event):
        return Page.hideEvent(self, event)
    def showEvent(self, event):
        return Page.showEvent(self, event)

    def vulp(self, evt=None):  # Done, untested
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina"""
        print('\nvulp Page 6', file=self._out)
        Page.vulp(self)
        self.initializing = True
        self.event_list, self.event_data, self.old_list, self.old_data = [], [], [], []
        self.progress_text.clear()
        self.progress_text.setReadOnly(True)
        # om te zien of de volgende if nodig is
        if self.parent.newitem:
            print('bij nieuw item:', self.parent.pagedata)
        if self.parent.pagedata: # and not self.parent.newitem:
            self.event_list = [x[0] for x in self.parent.pagedata.events]
            self.event_list.reverse()
            self.old_list = self.event_list[:]
            self.event_data = [x[1] for x in self.parent.pagedata.events]
            self.event_data.reverse()
            self.old_data = self.event_data[:]
            self.progress_list.clear()
            first_item = gui.QListWidgetItem(
                '-- doubleclick or press Shift-Ctrl-N to add new item --')
            first_item.setData(core.Qt.UserRole, -1)
            self.progress_list.addItem(first_item)
            for idx, datum in enumerate(self.event_list):
                if SQL_VERSION:
                    datum = datum[:19]
                try:
                    text = self.event_data[idx].split("\n")[0].strip()
                except AttributeError:
                    text = self.event_data[idx] or ""
                text = text if len(text) < 80 else text[:80] + "..."
                newitem = gui.QListWidgetItem('{} - {}'.format(datum, text))
                newitem.setData(core.Qt.UserRole, idx)
                self.progress_list.addItem(newitem)
        self.oldbuf = (self.old_list, self.old_data)
        self.oldtext = ''
        self.initializing = False
        print(self.event_data, file=self._out)

    def savep(self, evt=None):  # Done, untested
        "opslaan van de paginagegevens"
        print("\nsaving data", file=self._out)
        Page.savep(self)
        # voor het geval er na het aanpassen van een tekst direkt "sla op" gekozen is
        # nog even kijken of de tekst al in self.event_data is aangepast.
        idx = self.current_item
        hlp = str(self.progress_text.toPlainText())
        if idx > 0:
            idx -= 1
        if self.event_data[idx] != hlp:
            print('first saving local text', idx, hlp, file=self._out)
            self.event_data[idx] = hlp
            self.oldtext = hlp
            short_text = hlp.split("\n")[0]
            if len(short_text) < 80:
                short_text = short_text[:80] + "..."
            if XML_VERSION:
                short_text = short_text.encode('latin-1')
            self.progress_list.item(idx + 1).setText("{} - {}".format(
                self.event_list[idx], short_text))
            self.progress_list.item(idx + 1).setData(idx, core.Qt.UserRole)
        wijzig = False
        print(self.event_data, file=self._out)
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
            self.parent.page0.p0list.currentItem().setText(3,
                self.parent.pagedata.updated)
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

    def on_activate_item(self, item=None):  # Done, untested
        """callback voor dubbelklik of Enter op een item

        wanneer dit gebeurt op het eerste item kan een nieuwe worden aangemaakt
        """
        if item:
            print("\nactivate item:", item, item.text(), file=self._out)
        else:
            print('supposedly Shift-Ctrl-N was pressed')
        if self.initializing:
            return
        if item is None or int(item.data(core.Qt.UserRole).toPyObject()) == -1:
            print("adding new item", file = self._out)
            datum, self.oldtext = get_dts(), ''
            newitem = gui.QListWidgetItem('{} - {}'.format(datum, self.oldtext))
            newitem.setData(core.Qt.UserRole, 0)
            self.progress_list.insertItem(1, newitem)
            self.event_list.insert(0, datum)
            self.event_data.insert(0, self.oldtext)
            self.progress_list.setCurrentRow(1)
            self.progress_text.setText(self.oldtext)
            self.progress_text.setReadOnly(False)
            self.progress_text.setFocus()
        print(self.event_data, file=self._out)

    ## def currentItemChanged(self, item_n, item_o):  # Done, untested
    def on_select_item(self, item_n, item_o):  # Done, untested
        """callback voor het selecteren van een item

        selecteren van (klikken op) een regel in de listbox doet de inhoud van de
        textctrl ook veranderen. eerst controleren of de tekst veranderd is
        dat vragen moet ook in de situatie dat je op een geactiveerde knop klikt,
        het panel wilt verlaten of afsluiten
        de knoppen onderaan doen de hele lijst bijwerken in self.parent.book.p
        """
        if item_n is not None:
            print('\nselect item   ', item_n.text(), file=self._out)
        if item_o is not None:
            print('vorig item was', item_o.text(), file=self._out)
        self.progress_text.setReadOnly(True)
        ## if item_o is not None:
            ## # hoeft dit wel (aangenomen dat dit is om te kijken of de tekst gewijzigd is -
            ## # dat gebeurt volgens mij al in on_text() - nee dat is alleen het aanpassen in
            ## # de event_data tabel, zie opmerking aldaar)
            ## print('bijwerken vorig item in interne tabel')
            ## text = item_o.text()
            ## indx = int(item_o.data(core.Qt.UserRole).toPyObject())
            ## if indx > -1:
                ## datum = text.split(' - ')[0]
                ## tekst = str(self.progress_text.toPlainText()) # self.progress_list.GetItemText(idx)
                ## if tekst != self.oldtext:
                    ## self.event_data[indx] = tekst
                    ## short_text = tekst.split("\n")[0]
                    ## if len(short_text) >= 80:
                        ## short_text = short_text[:80] + "..."
                    ## item_o.setText("{} - {}".format(datum, short_text))
                    ## self.progress_list.SetItemData(indx, indx - 1)
        if item_n is None:
            return
        text, indx = item_n.text(), int(item_n.data(core.Qt.UserRole).toPyObject())
        print('ophalen data huidige item', indx, file=self._out)
        self.current_item = self.progress_list.currentRow() # item_n # self.currentItem()
        if indx == -1:
            self.oldtext = ""
        else:
            self.oldtext = self.event_data[indx] # dan wel item_n.text()
            self.progress_text.setText(self.oldtext)
            if not self.parent.pagedata.arch:
                self.progress_text.setReadOnly(False)
                self.progress_text.moveCursor(gui.QTextCursor.End,
                    gui.QTextCursor.MoveAnchor)
            self.progress_text.setFocus()
        print(self.event_data, file=self._out)
        #~ event.Skip()

    def on_text(self):  # Done, untested
        """callback voor wanneer de tekst gewijzigd is

        de initializing flag wordt uitgevraagd omdat deze event ook tijdens vulp()
        plaatsvindt

        als je hier al de event_data tabel aanpast, waarom dan niet ook gelijk de
        tekst in de list?
        """
        if self.initializing:
            return
        ## idx = self.current_item # self.progress_list.Selection # niet gebruikt
        tekst = str(self.progress_text.toPlainText()) # self.progress_list.GetItemText(ix)
        print("\non text:", tekst, file=self._out)
        if tekst != self.oldtext:
            self.oldtext = tekst
            self.enable_buttons()
            ## print(self.current_item)
            ## current_item = self.progress_list.currentRow() # item_n # self.currentItem()
            if self.current_item > 0:
                indx = self.current_item - 1
                self.event_data[indx] = tekst
                item = self.progress_list.currentItem()
                datum = str(item.text()).split(' - ')[0]
                short_text = ' - '.join((datum, tekst.split("\n")[0]))
                if len(short_text) >= 80:
                    short_text = short_text[:80] + "..."
                item.setText(short_text)
        print(self.event_data, file=self._out)

class SortOptionsDialog(gui.QDialog):   # Done
    "dialoog om de sorteer opties in te stellen"
    def __init__(self, parent):
        self.parent = parent
        lijst = ["(geen)"]
        for idx, text in enumerate(parent.parent.ctitels):
            if idx == 1:
                lijst.append("Soort")
            else:
                lijst.append(text)
        wid = 600 # if LIN else 450
        hig = 600 # if LIN else 450
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle("Sorteren op meer dan 1 kolom")
        ## self.resize(wid, hig)

        sizer = gui.QVBoxLayout()
        grid = gui.QGridLayout()
        for num in range(1, 5):
            row = num - 1
            grid.addWidget(gui.QLabel("  {}.".format(num), self), row, 0)
            ## size=(20, -1))
            cmb = gui.QComboBox(self)
            cmb.setEditable(False)
            cmb.addItems(lijst)
            cmb.setCurrentIndex(0)
             ## size=(80, -1),
            grid.addWidget(cmb, row, 1)
            rbg = gui.QButtonGroup(self)
            rba = gui.QRadioButton(" Asc ", self)
            rbg.addButton(rba)
            grid.addWidget(rba, row, 2)
            rbd = gui.QRadioButton(" Desc ", self)
            rbg.addButton(rbd)
            grid.addWidget(rbd, row, 3)

        sizer.addLayout(grid)

        buttonbox = gui.QDialogButtonBox(gui.QDialogButtonBox.Ok |
            gui.QDialogButtonBox.Cancel)
        sizer.addWidget(buttonbox)
        self.setLayout(sizer)

        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)

    def accept(self):
        """sorteerkolommen en -volgordes teruggeven aan hoofdscherm

        moet nog bedenken hoe dit te implementeren dus doet voorlopig niks extra
        """
        gui.QDialog.accept(self)


class SelectOptionsDialog(gui.QDialog): # Nog testen en verder aanpassen
    """dialoog om de selectie op te geven

    sel_args is de dictionary waarin de filterwaarden zitten, bv:
    {'status': ['probleem'], 'idlt': '2006-0009', 'titel': 'x', 'soort': ['gemeld'],
    'id': 'and', 'idgt': '2005-0019'}"""
    def __init__(self, parent, sel_args): # Done
        self.parent = parent
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle("Selecteren")
            ## size=(250,  250)

        self.check_options = gui.QButtonGroup()
        self.check_options.setExclusive(False)

        self.check_options.addButton(gui.QCheckBox(parent.parent.ctitels[0] +
            '   -', self))
        self.text_gt = gui.QLineEdit(self)
        self.text_gt.textChanged.connect(functools.partial(self.on_text, 'gt'))
        self.radio_id = gui.QButtonGroup(self)
        for text in ('en', 'of'):
            radio = gui.QRadioButton(text, self)
            self.radio_id.addButton(radio)
        self.text_lt = gui.QLineEdit(self)
        self.text_lt.textChanged.connect(functools.partial(self.on_text, 'lt'))

        self.check_options.addButton(gui.QCheckBox("soort   -", self))
        self.check_cats = gui.QButtonGroup(self)
        self.check_cats.setExclusive(False)
        for x in [self.parent.parent.cats[y] for y in sorted(
                self.parent.parent.cats.keys())]:
            check = gui.QCheckBox(x[0], self)
            check.toggled.connect(functools.partial(self.on_checked, 'cat'))
            self.check_cats.addButton(check)

        self.check_options.addButton(gui.QCheckBox(parent.parent.ctitels[2] +
            '   -', self))
        self.check_stats = gui.QButtonGroup(self)
        self.check_stats.setExclusive(False)
        for x in [self.parent.parent.stats[y] for y in sorted(
                self.parent.parent.stats.keys())]:
            check = gui.QCheckBox(x[0], self)
            check.toggled.connect(functools.partial(self.on_checked, 'stat'))
            self.check_stats.addButton(check)

        self.check_options.addButton(gui.QCheckBox(parent.parent.ctitels[4] +
            '   -', self))
        self.text_zoek = gui.QLineEdit(self)
        self.text_zoek.textChanged.connect(functools.partial(self.on_text,
            'zoek'))

        self.check_options.addButton(gui.QCheckBox("Archief    -", self))
        self.radio_arch = gui.QButtonGroup(self)
        for text in ("Alleen gearchiveerd", "gearchiveerd en lopend"):
            radio = gui.QRadioButton(text, self)
            self.radio_arch.addButton(radio)
            radio.toggled.connect(functools.partial(self.on_checked, 'arch'))

        self.buttonbox = gui.QDialogButtonBox(gui.QDialogButtonBox.Ok |
            gui.QDialogButtonBox.Cancel)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)

        self.set_defaults(sel_args)
        self.doelayout()

    def doelayout(self):
        sizer = gui.QVBoxLayout()
        grid = gui.QGridLayout()

        vbox = gui.QVBoxLayout()
        vbox.addWidget(self.check_options.buttons()[0])
        vbox.addStretch()
        grid.addLayout(vbox, 0, 0)

        vbox = gui.QVBoxLayout()
        hgrid = gui.QGridLayout()
        hgrid.addWidget(gui.QLabel('groter dan:', self), 0, 0)
        hgrid.addWidget(self.text_gt, 0, 1)
        hbox = gui.QHBoxLayout()
        for rb in self.radio_id.buttons():
            hbox.addWidget(rb)
        hgrid.addLayout(hbox, 1, 0)
        hgrid.addWidget(gui.QLabel('kleiner dan:', self), 2, 0)
        hgrid.addWidget(self.text_lt, 2, 1)
        vbox.addLayout(hgrid)
        vbox.addStretch()
        grid.addLayout(vbox, 0, 2)

        vbox = gui.QVBoxLayout()
        vbox.addWidget(self.check_options.buttons()[1])
        vbox.addStretch()
        grid.addLayout(vbox, 1, 0)

        hbox = gui.QHBoxLayout()
        vbox = gui.QVBoxLayout()
        vbox.addWidget(gui.QLabel("selecteer een of meer:", self))
        vbox.addStretch()
        hbox.addLayout(vbox)
        vbox = gui.QVBoxLayout()
        for check in self.check_cats.buttons():
            vbox.addWidget(check)
        hbox.addLayout(vbox)
        grid.addLayout(hbox, 1, 2)

        vbox = gui.QVBoxLayout()
        vbox.addWidget(self.check_options.buttons()[2])
        vbox.addStretch()
        grid.addLayout(vbox, 2, 0)

        hbox = gui.QHBoxLayout()
        vbox = gui.QVBoxLayout()
        vbox.addWidget(gui.QLabel("selecteer een of meer:", self))
        vbox.addStretch()
        hbox.addLayout(vbox)
        vbox = gui.QVBoxLayout()
        for check in self.check_stats.buttons():
            vbox.addWidget(check)
        hbox.addLayout(vbox)
        grid.addLayout(hbox, 2, 2)

        vbox = gui.QVBoxLayout()
        vbox.addWidget(self.check_options.buttons()[3])
        vbox.addStretch()
        grid.addLayout(vbox, 3, 0)

        hbox = gui.QHBoxLayout()
        hbox.addWidget(gui.QLabel('zoek naar:', self))
        hbox.addWidget(self.text_zoek)
        grid.addLayout(hbox, 3, 2)

        vbox = gui.QVBoxLayout()
        vbox.addWidget(self.check_options.buttons()[4])
        vbox.addStretch()
        grid.addLayout(vbox, 4, 0)
        ## grid.addWidget(gui.QLabel('-', self), 4, 1)
        hbox = gui.QHBoxLayout()
        for radio in self.radio_arch.buttons():
            hbox.addWidget(radio)
        grid.addLayout(hbox, 4, 2)
        sizer.addLayout(grid)

        sizer.addWidget(self.buttonbox)
        self.setLayout(sizer)

    def set_defaults(self, sel_args):
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

        if XML_VERSION:
            itemindex = 1
        elif SQL_VERSION:
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
            self.text_zoek.setText(sel_args["titel"])
            self.check_options.buttons()[3].setChecked(True)

        if "arch" in sel_args:
            if sel_args["arch"] == "arch":
                self.radio_arch.buttons()[0].setChecked(True)
            if sel_args["arch"] == "alles":
                self.radio_arch.buttons()[1].setChecked(True)
            self.check_options.buttons()[4].setChecked(True)

    def on_text(self, arg, text): # Done, untested
        "callback voor EVT_TEXT"
        ## it = evt.GetEventObject() # unused
        ## print('on_text:', arg, text)
        if arg in ('gt', 'lt'):
            obj = self.check_options.buttons()[0]
        elif arg == 'zoek':
            obj = self.check_options.buttons()[3]
        if text == "":
            obj.setChecked(False)
        else:
            obj.setChecked(True)

    def on_checked(self, arg, val): # Done, untested
        "callback voor EVT_CHECK"
        ## print('on_check:', val, arg)
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

    def accept(self): # TODO
        "aangegeven opties verwerken in sel_args dictionary"
        selection = 'excl.gearchiveerde'
        sel_args = {}
        if self.check_options.buttons()[0].isChecked(): #  checkbox voor "id"
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
        if XML_VERSION:
            itemindex = 1
        elif SQL_VERSION:
            itemindex = 2
        if self.check_options.buttons()[1].isChecked(): #  checkbox voor "soort"
            selection = '(gefilterd)'
            if XML_VERSION:
                lst = [self.parent.parent.cats[x][itemindex]
                    for x in range(len(self.parent.parent.cats.keys()))
                    if self.check_cats.buttons()[x].isChecked()]
            elif SQL_VERSION:
                lst = [self.parent.parent.cats[x][itemindex]
                    for x in range(len(self.parent.parent.cats.keys()))
                    if self.check_cats.buttons()[x].isChecked()]
            if lst:
                sel_args["soort"] = lst
        if self.check_options.buttons()[2].isChecked(): #  checkbox voor "status"
            selection = '(gefilterd)'
            if XML_VERSION:
                lst = [self.parent.parent.stats[x][itemindex]
                    for x in range(len(self.parent.parent.stats.keys()))
                    if self.check_stats.buttons()[x].isChecked()]
            elif SQL_VERSION:
                lst = [self.parent.parent.stats[x][itemindex]
                    for x in range(len(self.parent.parent.stats.keys()))
                    if self.check_stats.buttons()[x].isChecked()]
            if lst:
                sel_args["status"] = lst
        if self.check_options.buttons()[3].isChecked(): # checkbox voor "titel bevat"
            selection = '(gefilterd)'
            sel_args["titel"] = str(self.text_zoek.text())
        if self.check_options.buttons()[4].isChecked(): # checkbox voor "archiefstatus"
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
        gui.QDialog.accept(self)

class OptionsDialog(gui.QDialog):
    """base class voor de opties dialogen

    nu nog F2 en dubbelklikken mogelijk maken om editen te starten"""
    def __init__(self, parent, title, size=(300,300)): # Done
        self.parent = parent
        gui.QDialog.__init__(self, parent)
        self.resize(size[0], size[1])
        self.setWindowTitle(title)
        self.initstuff()
        sizer = gui.QVBoxLayout()

        sizer.addWidget(gui.QLabel(self.titel, self))

        self.elb = gui.QListWidget(self)
        self.elb.currentItemChanged.connect(self.end_edit)
        self.elb.itemDoubleClicked.connect(self.edit_item)
        for text in self.data:
            self.elb.addItem(text)
        sizer.addWidget(self.elb)

        box = gui.QHBoxLayout()
        box.addStretch()
        self.b_edit = gui.QPushButton('&Edit', self)
        self.b_edit.clicked.connect(self.edit_item)
        box.addWidget(self.b_edit)
        if self.editable:
            self.b_new = gui.QPushButton('&New', self)
            self.b_new.clicked.connect(self.add_item)
            box.addWidget(self.b_new)
            self.b_delete = gui.QPushButton('&Delete', self)
            self.b_delete.clicked.connect(self.remove_item)
            box.addWidget(self.b_delete)
            self.b_up = gui.QPushButton('Move &Up', self)
            self.b_up.clicked.connect(self.move_item_up)
            box.addWidget(self.b_up)
            self.b_down = gui.QPushButton('Move &Down', self)
            self.b_down.clicked.connect(self.move_item_down)
            box.addWidget(self.b_down)
        box.addStretch()
        sizer.addLayout(box)

        sizer.addWidget(gui.QLabel("\n".join(self.tekst), self))

        buttonbox = gui.QDialogButtonBox(gui.QDialogButtonBox.Ok |
            gui.QDialogButtonBox.Cancel)
        sizer.addWidget(buttonbox)
        self.setLayout(sizer)

        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)

    def initstuff(self): # Done
        """placeholder voor aanvullende initialisatie methode

        tevens om te tonen welke dingen er hier ingesteld moeten worden
        """
        self.titel = ""
        self.data = []
        self.tekst = ["", ""]
        self.editable = True


    def keyReleaseEvent(self, evt):
        keycode = evt.key()
        if keycode == core.Qt.Key_F2:
            self.edit_item()
            return
        gui.QDialog.keyReleaseEvent(self, evt)

    def edit_item(self): # Done, seems ok
        "open de betreffende regel voor editing"
        item = self.elb.currentItem()
        self.elb.openPersistentEditor(item)
        self.elb.editItem(item)

    def end_edit(self, item_n, item_o): # ok
        self.elb.closePersistentEditor(item_o)

    def add_item(self): # seems ok
        "open een nieuwe lege regel"
        item = gui.QListWidgetItem('')
        self.elb.addItem(item)
        self.elb.setCurrentItem(item)
        self.elb.openPersistentEditor(item)
        self.elb.editItem(item)

    def remove_item(self): # seems ok
        "verwijder de betreffende regel"
        item = self.elb.currentItem()
        row = self.elb.currentRow()
        self.elb.takeItem(row)

    def move_item_up(self): # ok
        "inhoud omwisselen met de regel erboven"
        self.move_item(up=True)

    def move_item_down(self): # ok
        "inhoud omwisselen met de regel eronder"
        self.move_item(up=False)

    def move_item(self, up=True):
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

    def accept(self): # Done, untested
        message = self.leesuit()
        if message:
            gui.QMessageBox.information(self, 'Probreg', message)
            return
        gui.QDialog.accept(self)

class TabOptions(OptionsDialog): # Done
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
            "Er kunnen geen tabs worden verwijderd",
            "of toegevoegd."]
        self.editable = False

    def leesuit(self):
        "wijzigingen doorvoeren"
        self.newtabs = {}
        ## for idx, item in enumerate(self.elb.items()):
        for idx in range(self.elb.count()):
            item = self.elb.item(idx).text()
            self.newtabs[str(idx)] = str(item)
        self.parent.save_settings("tab", self.newtabs)

class StatOptions(OptionsDialog): # Done
    "dialoog voor de mogelijke statussen"
    def initstuff(self):
        "aanvullende initialisatie"
        self.titel = "Status codes en waarden"
        self.data = []
        for key in sorted(self.parent.book.stats.keys()):
            if XML_VERSION:
                item_text, item_value = self.parent.book.stats[key]
                self.data.append(": ".join((item_value, item_text)))
            elif SQL_VERSION:
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
        ## for sortkey, item in enumerate(self.elb.items()):
        for sortkey in range(self.elb.count()):
            item = self.elb.item(sortkey).text()
            try:
                value, text = str(item).split(": ")
            except ValueError:
                return 'Foutieve waarde: bevat geen dubbele punt'
            self.newstats[value] = (text, sortkey)
        self.parent.save_settings("stat", self.newstats)

class CatOptions(OptionsDialog): # Done
    "dialoog voor de mogelijke categorieen"
    def initstuff(self):
        "aanvullende initialisatie"
        self.titel = "Soort codes en waarden"
        self.data = []
        for key in sorted(self.parent.book.cats.keys()):
            if XML_VERSION:
                item_value, item_text = self.parent.book.cats[key]
                self.data.append(": ".join((item_text, item_value)))
            elif SQL_VERSION:
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
        ## for sortkey, item in enumerate(self.elb.items()):
        for sortkey in range(self.elb.count()):
            item = self.elb.item(sortkey).text()
            try:
                value, text = str(item).split(": ")
            except ValueError:
                return 'Foutieve waarde: bevat geen dubbele punt'
            self.newcats[value] = (text, sortkey)
        self.parent.save_settings("cat", self.newcats)

class MainWindow(gui.QMainWindow):
    """Hoofdscherm met menu, statusbalk, notebook en een "quit" button"""
    def __init__(self, parent, fnaam=""):   # Done
        self.parent = parent
        self.title = 'Actieregistratie'
        self.initializing = True
        self.exiting = False
        self.mag_weg = True
        self.helptext = ''
        self.pagedata = self.oldbuf = None
        self.newfile = self.newitem = False
        self.oldsort = -1
        self.idlist = self.actlist = self.alist = []
        if XML_VERSION:
            self.filepad = fnaam
            if fnaam:
                ext = os.path.splitext(self.filepad)[1]
                if ext == "" and not os.path.isdir(self.filepad):
                    self.filepad += ".xml"
                elif ext != ".xml":
                    self.filepad = ""
            self.dirname, self.filename = os.path.split(self.filepad)
        elif SQL_VERSION:
            self.filename = ""

        if LIN:
            wide, high, left, top = 864, 720, 2, 2
        else:
            wide, high, left, top = 588, 594, 20, 32
        gui.QMainWindow.__init__(self, parent)
        self.setWindowTitle(self.title)
        self.setWindowIcon(gui.QIcon("task.ico"))
        self.move(left, top)
        self.resize(wide, high)
        self.sbar = self.statusBar()
        self.create_menu()
        self.create_actions()

        pnl = gui.QFrame(self)
        self.setCentralWidget(pnl)
        ## self.close = self.exit_app
        self.create_book(pnl)
        self.exit_button = gui.QPushButton('&Quit', pnl)
        self.exit_button.clicked.connect(self.exit_app)
        self.doelayout(pnl)
        self.book.page6._out = open("probreg_page6.log", "w")
        if self.filename == "":
            if XML_VERSION:
                self.open_xml()
            elif SQL_VERSION:
                self.open_sql()
        else:
            self.startfile()
        self.initializing = False
        self.zetfocus(0) # book.page0.SetFocus()

    def create_menu(self):
        menu_bar = self.menuBar()
        menudata = (
            ("&File", [
                ("&Open", self.open_xml, 'Ctrl+O', " Open a new file"),
                ("&New", self.new_file, 'Ctrl+N', " Create a new file"),
                ("&Open project", self.open_sql, 'Ctrl+O', " Select a project"),
                ('',),
                ("&Print", (
                    ("Dit &Scherm", self.print_scherm, 'Shift+Ctrl+P',
                        "Print the contents of the current screen"),
                    ("Deze &Actie", self.print_actie, 'Alt+Ctrl+P',
                        "Print the contents of the current issue"), )),
                ('',),
                ("&Quit", self.exit_app, 'Ctrl+Q', " Terminate the program"),
                ]),
            ("&Settings", (
                ("&Applicatie", (
                    ("&Lettertype", self.font_settings, '',
                        " Change the size and font of the text"),
                    ("&Kleuren", self.colour_settings, '',
                        " Change the colours of various items"), )),
                ("&Data", (
                    ("  &Tabs", self.tab_settings, '',
                        " Change the titles of the tabs"),
                    ("  &Soorten", self.cat_settings, '',
                        " Add/change type categories"),
                    ( "  St&atussen", self.stat_settings, '',
                        " Add/change status categories"), )),
                ("&Het leven", self.silly_menu, '',
                    " Change the way you look at life"),
                )),
            ("&Help", (
                ("&About", self.about_help, 'F1', " Information about this program"),
                ("&Keys", self.hotkey_help, 'Ctrl+H', " List of shortcut keys"),
                )))
        if XML_VERSION:
            del menudata[0][1][2]
        elif SQL_VERSION:
            del menudata[0][1][0:1]

        def add_to_menu(menu, menuitem):
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
                for subitem in items:
                    add_to_menu(sub, subitem)

        for title, items in menudata:
            menu = menu_bar.addMenu(title)
            for menuitem in items:
                add_to_menu(menu, menuitem)

    def create_actions(self):
        action = gui.QShortcut('Ctrl+P', self, self.print_)
        action = gui.QShortcut('Alt+Left', self, self.go_prev)
        action = gui.QShortcut('Alt+Right', self, self.go_next)
        for char in '0123456':
            action = gui.QShortcut('Alt+{}'.format(char), self, functools.partial(
                self.go_to, int(char)))

    def print_(self, evt=None):
        """callback voor ctrl-P(rint)

        vraag om printen scherm of actie, bv. met een InputDialog
        """
        choice, ok = gui.QInputDialog.getItem(self, 'Afdrukken',
            'Wat wil je afdrukken?', ['huidig scherm', 'huidige actie'])
        if ok:
            print('printing', choice)
            if choice == 0:
                self.print_scherm(evt)
            else:
                self.print_actie(evt)

    def go_next(self):
        Page.goto_next(self.book.widget(self.book.current_tab))

    def go_prev(self):
        Page.goto_prev(self.book.widget(self.book.current_tab))

    def go_to(self, page):
        Page.goto_page(self.book.widget(self.book.current_tab), page)

    def create_book(self, pnl):
        self.book = gui.QTabWidget(pnl)
        self.book.resize(300,300)
        self.book.parent = self
        self.book.fnaam = ""
        self.book.sorter = None
        self.book.current_item = None
        self.book.data = {}
        self.book.rereadlist = True
        self.lees_settings()
        self.book.ctitels = ["actie", " ", "status", "L.wijz."]
        if XML_VERSION:
            self.book.ctitels.append("titel")
        elif SQL_VERSION:
            self.book.ctitels.extend(("betreft", "omschrijving"))
        self.book.current_tab = -1
        self.book.newitem = False
        self.book.pagedata = None
        #~ self.book.SetMinSize((486,496))
        self.book.page0 = Page0(self.book)
        self.book.page1 = Page1(self.book)
        self.book.page2 = Page(self.book)
        self.book.page3 = Page(self.book)
        self.book.page4 = Page(self.book)
        self.book.page5 = Page(self.book)
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


    def doelayout(self, pnl):
        sizer0 = gui.QVBoxLayout()
        sizer1 = gui.QHBoxLayout()
        sizer1.addWidget(self.book)
        sizer0.addLayout(sizer1)
        sizer2 = gui.QHBoxLayout()
        sizer2.addStretch()
        sizer2.addWidget(self.exit_button)
        sizer2.addStretch()
        sizer0.addLayout(sizer2)
        pnl.setLayout(sizer0)

    def new_file(self, evt):        # Done, untested
        "Menukeuze: nieuw file"
        self.newfile = False
        self.dirname = os.getcwd()
        name = gui.QFileDialog.getSaveFileName(self,
            self.title + " - nieuw gegevensbestand",
            self.dirname, "", "XML files (*.xml);;all files (*.*)")
        if name:
            self.filename, self.dirname = os.path.split(fname)
            self.newfile = True
            self.startfile()
            self.newfile = False

    def open_xml(self, evt=None):   # Done
        "Menukeuze: open file"
        self.dirname = os.getcwd()
        fname = gui.QFileDialog.getOpenFileName(self,
            self.title + " - kies een gegevensbestand",
            self.dirname, "", "XML files (*.xml);;all files (*.*)")
        if fname:
            self.filename, self.dirname = os.path.split(fname)
            self.startfile()

    def open_sql(self, evt=None):   # Done, untested
        "Menukeuze: open project"
        data = []
        with open(APPS) as f_in:
            for line in f_in:
                sel, naam, titel, oms = line.strip().split(";")
                if sel == "X":
                    data.append((naam.capitalize(),titel.capitalize(),oms))
        data = data # [1:]
        data.sort()
        print(self.filename)
        for idx, h in enumerate(data):
            print(h)
            if h[0] == self.filename or \
                    (self.filename == "_basic" and h[0] == "Basic"):
                choice = h[0] # idx
                break
        # combobox versie
        choice, ok = gui.QInputDialog.getItem(self, 'Probreg SQL versie',
            'Kies een project om te openen', [": ".join((h[1],h[2])) for h in data],
            current = idx, editable=False)
        ## # listbox versie
        ## dlg = gui.QInputDialog(self)
        ## dlg.setInputMode(gui.QInputDialog.TextInput)
        ## dlg.setComboBoxItems([": ".join((h[1],h[2])) for h in data])
        ## dlg.setOption(gui.QInputDialog.UseListViewForComboBoxItems, True)
        ## dlg.setLabelText('Kies een project om te openen')
        ## dlg.setTextValue(choice)
        ## dlg.setComboBoxEditable(False)
        ## ok = dlg.exec_() # need a way to transfer the actual choice
        ## if ok == gui.QDialog.Accepted():
        if ok:
            self.filename = choice
            if self.filename == "Basic":
                self.filename = "_basic"
            self.startfile()

    def print_scherm(self, evt = None): # Done
        "Menukeuze: print dit scherm"
        print('printing current screen')
        self.printdict = {'lijst': [], 'actie': [], 'sections': [],
            'events': []}
        self.hdr = "Actie: {} {}".format(self.book.pagedata.id,
            self.book.pagedata.titel)
        if self.book.current_tab == 0:
            self.hdr = "Overzicht acties uit " + self.filename
            lijst = []
            for indx in range(self.book.page0.p0list.topLevelItemCount()):
                item = self.book.page0.p0list.topLevelItem(indx)
                actie = str(item.text(0))
                started = ''
                soort =  str(item.text(1))
                status = str(item.text(2))
                l_wijz = str(item.text(3))
                titel =  str(item.text(4))
                if SQL_VERSION:
                    over = titel
                    titel = str(item.text(5))
                    l_wijz = l_wijz[:19]
                    actie = actie + " - " + over
                    started = started[:19]
                if l_wijz:
                    l_wijz = ", laatst behandeld op " + l_wijz
                if status != self.book.stats[0][0]:
                    l_wijz = "status: {}, {}".format(status, l_wijz)
                else:
                    l_wijz = "status: {}".format(status)
                lijst.append((actie, titel, soort, started, l_wijz))
            self.printdict['lijst'] = lijst
        elif self.book.current_tab == 1:
            actie = str(self.book.page1.id_text.text())
            self.hdr = "Informatie over actie {}: samenvatting".format(actie)
            self.printdict.update({
                'actie': actie,
                'datum': str(self.book.page1.date_text.text()),
                'oms': str(self.book.page1.proc_entry.text()),
                'tekst': str(self.book.page1.desc_entry.text()),
                'soort': str(self.book.page1.cat_choice.currentText()),
                'status': str(self.book.page1.stat_choice.currentText()),
                })
        elif 2 <= self.book.current_tab <= 5:
            title = self.book.tabs[self.book.current_tab].split(None, 1)[1]
            if self.book.current_tab == 2:
                text = self.book.page2.text1.toPlainText()
            elif self.book.current_tab == 3:
                text = self.book.page3.text1.toPlainText()
            elif self.book.current_tab == 4:
                text = self.book.page4.text1.toPlainText()
            elif self.book.current_tab == 5:
                text = self.book.page5.text1.toPlainText()
            self.printdict['sections'] = [(title, str(text).replace('\n', '<br>'))]
        elif self.book.current_tab == 6:
            events = []
            for idx, data in enumerate(self.book.page6.event_list):
                if SQL_VERSION:
                    data = data[:19]
                events.append((data, self.book.page6.event_data[idx].replace('\n',
                    '<br>')))
            self.printdict['events'] = events
        print('alles voorbereid voor printen scherm')
        self.preview()

    def print_actie(self, evt = None):  # Done
        "Menukeuze: print deze actie"
        print('printing current issue')
        if self.book.pagedata is None or self.book.newitem:
            # afbreken met melding geen actie geselecteerd
            dlg = gui.QMessageBox.information(self,
                self.parent.parent.title,
                "Wel eerst een actie kiezen om te printen",
            )
            return
        self.hdr = ("Actie: {} {}".format(self.book.pagedata.id, self.book.pagedata.titel))
        tekst = self.book.pagedata.titel #.split(" - ", 1)
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
        self.printdict = {
            'lijst': [],
            'actie':  self.book.pagedata.id,
            'datum': self.book.pagedata.datum,
            'oms': oms,
            'tekst': tekst,
            'soort': srt,
            'status': stat,
            }
        empty = "(nog niet beschreven)"
        print(self.book.tabs)
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
        print('alles voorbereid voor printen actie')
        self.preview()

    def exit_app(self, evt = None): # Done
        "Menukeuze: exit applicatie"
        self.exiting = True
        if self.book.current_tab == 0:
            ok_to_leave = self.book.page0.leavep()
        elif self.book.current_tab == 1:
            ok_to_leave = self.book.page1.leavep()
        elif self.book.current_tab == 2:
            ok_to_leave = self.book.page2.leavep()
        elif self.book.current_tab == 3:
            ok_to_leave = self.book.page3.leavep()
        elif self.book.current_tab == 4:
            ok_to_leave = self.book.page4.leavep()
        elif self.book.current_tab == 5:
            ok_to_leave = self.book.page5.leavep()
        elif self.book.current_tab == 6:
            ok_to_leave = self.book.page6.leavep()
        if ok_to_leave:
            self.book.page6._out.close()
            self.close()

    def tab_settings(self, evt):    # Done
        "Menukeuze: settings - data - tab titels"
        TabOptions(self, "Wijzigen tab titels", size=(350, 200)).exec_()

    def stat_settings(self, evt):   # Done
        "Menukeuze: settings - data - statussen"
        StatOptions(self, "Wijzigen statussen", size=(350, 200)).exec_()

    def cat_settings(self, evt):    # Done
        "Menukeuze: settings - data - soorten"
        CatOptions(self, "Wijzigen categorieen", size=(350, 200)).exec_()

    def font_settings(self, evt):   # Done
        "Menukeuze: settings - applicatie - lettertype"
        gui.QMessageBox.information(self, "Oeps", "Sorry, werkt nog niet")

    def colour_settings(self, evt): # Done
        "Menukeuze: settings - applicatie - kleuren"
        gui.QMessageBox.information(self, "Oeps", "Sorry, werkt nog niet")

    def hotkey_settings(self, evt): # Done
        "Menukeuze: settings - applicatie- hotkeys (niet geactiveerd)"
        gui.QMessageBox.information(self, "Oeps", "Sorry, werkt nog niet")

    def about_help(self, evt):      # Done
        "Menukeuze: help - about"
        gui.QMessageBox.information(self, 'Help',
            "PyQt4 versie van mijn actiebox")

    def hotkey_help(self, evt):     # Done
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
                "    Ctrl-up/down op tab 6: move in list",
                ]
            if XML_VERSION:
                help.insert(8, "    Ctrl-O: _o_pen een (ander) actiebestand")
                help.insert(8, "    Ctrl-N: maak een _n_ieuw actiebestand")
            elif SQL_VERSION:
                help.insert(8, "    Ctrl-O: selecteer een (ander) pr_o_ject")
            self.helptext = "\n".join(help)
        gui.QMessageBox.information(self, 'Help', self.helptext)

    def silly_menu(self, evt):      # Done
        "Menukeuze: settings - het leven"
        gui.QMessageBox.information(self, 'Haha',
            "Yeah you wish...\nHet leven is niet in te stellen helaas")

    def startfile(self):            # Done
        "initialisatie t.b.v. nieuw bestand"
        if XML_VERSION:
            fullname = os.path.join(self.dirname, self.filename)
            retval = checkfile(fullname, self.newfile)
            if retval != '':
                gui.QMessageBox.info(self, "Oeps", retval)
                return
            self.book.fnaam = fullname
            self.title = self.filename
        elif SQL_VERSION:
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
            self.book.setcurrentIndex(0)
        self.book.checked_for_leaving = True

    def lees_settings(self):        # Done
        """instellingen (tabnamen, actiesoorten en actiestatussen) inlezen"""
        try:
            data = Settings(self.book.fnaam)
        except DataError as err:
            gui.QMessageBox.information(self, "Oh-oh!", str(err))
            return
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
        for item_value, item in data.stat.iteritems():
            if XML_VERSION:
                item_text, sortkey = item
                self.book.stats[int(sortkey)] = (item_text, item_value)
            elif SQL_VERSION:
                item_text, sortkey, row_id = item
                self.book.stats[int(sortkey)] = (item_text, item_value, row_id)
        for item_value, item in data.cat.iteritems():
            if XML_VERSION:
                item_text, sortkey = item
                self.book.cats[int(sortkey)] = (item_text, item_value)
            elif SQL_VERSION:
                item_text, sortkey, row_id = item
                self.book.cats[int(sortkey)] = (item_text, item_value, row_id)
        for tab_num, tab_text in data.kop.iteritems():
            if XML_VERSION:
                self.book.tabs[int(tab_num)] = " ".join((tab_num, tab_text))
            elif SQL_VERSION:
                tab_text, tab_adr = tab_text
                self.book.tabs[int(tab_num)] = " ".join((tab_num, tab_text.title()))

    def save_settings(self, srt, data): # Done
        """instellingen (tabnamen, actiesoorten of actiestatussen) terugschrijven

        argumenten: soort, data
        data is een dictionary die in een van de dialogen TabOptions, CatOptions
        of StatOptions wordt opgebouwd"""
        settings = Settings(self.book.fnaam)
        if srt == "tab":
            settings.kop = data
            settings.write()
            self.book.tabs = {}
            for item_value, item_text in data.iteritems():
                ## if XML_VERSION:
                    ## tabtext = " ".join((item_value, item_text))
                    ## self.book.tabs[item_value] = tabtext
                    ## self.book.setTabText(int(item_value), tabtext)
                ## elif SQL_VERSION:
                    item = " ".join((item_value, item_text))
                    self.book.tabs[int(item_value)] = item
                    self.book.setTabText(int(item_value), item)
        elif srt == "stat":
            settings.stat = data
            settings.write()
            self.book.stats = {}
            for item_value, item in data.iteritems():
                if XML_VERSION:
                    item_text, sortkey = item
                    self.book.stats[sortkey] = (item_text, item_value)
                elif SQL_VERSION:
                    item_text, sortkey, row_id = item
                    self.book.stats[sortkey] = (item_text, item_value, row_id)
        elif srt == "cat":
            settings.cat = data
            settings.write()
            self.book.cats = {}
            for item_value, item in data.iteritems():
                if XML_VERSION:
                    item_text, sortkey = item
                    self.book.cats[sortkey] = (item_text, item_value)
                elif SQL_VERSION:
                    item_text, sortkey, row_id = item
                    self.book.cats[sortkey] = (item_text, item_value, row_id)
        self.book.page1.vul_combos()

    def on_page_changing(self, newtabnum):  # Mostly Done, maar werkt nog niet lekker
        """
        deze methode is bedoeld om wanneer er van pagina gewisseld gaat worden
        te controleren of dat wel mogelijk is en zo niet, te melden waarom en de
        paginawissel tegen te houden (ok, terug te gaan naar de vorige pagina).
        PyQT4 kent geen aparte beforechanging methode, daarom is deze methode
        tevens bedoeld om ervoor te zorgen dat na het wisselen
        van pagina het veld / de velden van de nieuwe pagina een waarde krijgen
        met behulp van de vulp methode
        """
        old = self.book.current_tab
        new = self.book.current_tab = self.book.currentIndex()
        print('going to new page', new)
        ## sel = self.book.GetSelection() # unused
        if LIN and old == -1: # bij initialisatie en bij afsluiten - op Windows is deze altijd -1?
            return
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
            self.book.page6.vulp()
        self.zetfocus(self.book.current_tab)

    def zetfocus(self, tabno):      # Done
        "focus geven aan de gekozen tab"
        #~ self.setFocus()
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
        self.print_dlg = gui.QPrintPreviewDialog(self)
        self.print_dlg.paintRequested.connect(self.afdrukken)
        self.print_dlg.exec_()

    def afdrukken(self, printer):            # Done, maar werkt nog niet naar behoren
        "wordt aangeroepen door de menuprint methodes"
        self.css = ""
        if self.css:
            self.printdict['css'] = self.css
        self.printdict['hdr'] = self.hdr
        ## prt = dlg.printer()
        ## print(self.printdict)
        doc = gui.QTextDocument(self)
        html = Template(filename='actie.tpl').render(**self.printdict)
        ## print(html)
        doc.setHtml(html)
        printer.setOutputFileName(self.hdr)
        ## print(doc.toHtml())
        doc.print_(printer)
        ## self.printer.print_("".join(self.text), self.hdr)
        self.print_dlg.done(True)

def main(arg=None, log=False):
    "opstart routine"
    if log:
        logging.basicConfig(filename='apropos_qt.log', level=logging.DEBUG,
            format='%(asctime)s %(message)s')
    else:
        logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(message)s')
    if arg is None:
        globals()["SQL_VERSION"] = True
        from dml_sql import DataError, get_acties, Actie, Settings
        from config_sql import APPS
        globals()["APPS"] = APPS
    else:
        globals()["XML_VERSION"] = True
        from dml_xml import DataError, checkfile, get_acties, Actie, Settings
        globals()["checkfile"] = checkfile
    globals()["DataError"] = DataError
    globals()["get_acties"] = get_acties
    globals()["Actie"] = Actie
    globals()["Settings"] = Settings
    app = gui.QApplication(sys.argv)
    print('\n** {} **\n'.format(get_dts()))
    frame = MainWindow(None, arg)
    frame.show()
    sys.exit(app.exec_())
