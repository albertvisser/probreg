#! usr/bin/env python
# -*- coding: UTF-8 -*-
"""Actie (was: problemen) Registratie, PyQT5 versie
"""
import os
# import sys
import pathlib
# import pprint
# import collections
# import functools
# to be removed
# import PyQt5.QtWidgets as qtw
# import PyQt5.QtPrintSupport as qtp
# import PyQt5.QtGui as gui
# import PyQt5.QtCore as core
# maybe the next one as well, maybe not
# from mako.template import Template
## import probreg.pr_globals as pr
import probreg.gui as gui
import probreg.shared as shared   # import DataError, et_projnames
## import probreg.dml_sql as dmls
import probreg.dml_django as dmls
import probreg.dml_xml as dmlx
## checkfile = dmlx.checkfile
LIN = True if os.name == 'posix' else False


class Page():
    "base class for notebook page"
    def __init__(self, parent, pageno, standard=True):
        self.parent = parent
        self.pageno = pageno
        self.is_text_page = standard
        if standard:
            self.gui = gui.PageGui(parent, self)

    def get_toolbar_data(self):
        "return texts, shortcuts and picture names for setting op toolbar"
        return (('&Bold', 'Ctrl+B', 'icons/sc_bold', 'CheckB'),
                ('&Italic', 'Ctrl+I', 'icons/sc_italic', 'CheckI'),
                ('&Underline', 'Ctrl+U', 'icons/sc_underline', 'CheckU'),
                ('Strike&through', 'Ctrl+~', 'icons/sc_strikethrough.png', 'CheckS'),
                # ("Toggle &Monospace", 'Shift+Ctrl+M', 'icons/text',
                #     'Switch using proportional font off/on'),
                (),
                ("&Enlarge text", 'Ctrl+Up', 'icons/sc_grow', 'Use bigger letters'),
                ("&Shrink text", 'Ctrl+Down', 'icons/sc_shrink', 'Use smaller letters'),
                (),
                ('To &Lower Case', 'Shift+Ctrl+L', 'icons/sc_changecasetolower',
                 'Use all lower case letters'),
                ('To &Upper Case', 'Shift+Ctrl+U', 'icons/sc_changecasetoupper',
                 'Use all upper case letters'),
                (),
                ("Indent &More", 'Ctrl+]', 'icons/sc_incrementindent', 'Increase indentation'),
                ("Indent &Less", 'Ctrl+[', 'icons/sc_decrementindent', 'Decrease indentation'),
                (),
                # ("Normal Line Spacing", '', 'icons/sc_spacepara1',
                #     'Set line spacing to 1'),
                # ("1.5 Line Spacing",    '', 'icons/sc_spacepara15',
                #     'Set line spacing to 1.5'),
                # ("Double Line Spacing", '', 'icons/sc_spacepara2',
                #     'Set line spacing to 2'),
                # (),
                ("Increase Paragraph &Spacing", '', 'icons/sc_paraspaceincrease',
                 'Increase spacing between paragraphs'),
                ("Decrease &Paragraph Spacing", '', 'icons/sc_paraspacedecrease',
                 'Decrease spacing between paragraphs'))

    def vulp(self):
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina"""
        self.initializing = True
        self.parent.parent.enable_settingsmenu()
        if self.parent.current_tab == 0:
            text = self.seltitel
        else:
            self.enable_buttons(False)
            text = self.parent.tabs[self.parent.current_tab].split(None, 1)
            if self.parent.pagedata:
                text = str(self.parent.pagedata.id) + ' ' + self.parent.pagedata.titel
        self.parent.parent.set_windowtitle("{} | {}".format(self.parent.parent.title, text))
        self.parent.parent.set_statusmessage()
        if 1 < self.parent.current_tab < 6:
            self.oldbuf = ''
            is_readonly = False
            if self.parent.pagedata is not None:
                if self.parent.current_tab == 2 and self.parent.pagedata.melding:
                    self.oldbuf = self.parent.pagedata.melding
                if self.parent.current_tab == 3 and self.parent.pagedata.oorzaak:
                    self.oldbuf = self.parent.pagedata.oorzaak
                if self.parent.current_tab == 4 and self.parent.pagedata.oplossing:
                    self.oldbuf = self.parent.pagedata.oplossing
                if self.parent.current_tab == 5 and self.parent.pagedata.vervolg:
                    self.oldbuf = self.parent.pagedata.vervolg
                # self.text1.setReadOnly(self.parent.pagedata.arch)
                is_readonly = self.parent.pagedata.arch
            self.gui.set_textarea_contents(self.oldbuf)
            if not is_readonly:
                is_readonly = not self.parent.parent.is_user
            self.gui.set_text_readonly(is_readonly)
            self.gui.enable_toolbar(self.parent.parent.is_user)
            self.oldbuf = self.gui.get_textarea_contents()  # make sure it's rich text
            self.gui.move_cursor_to_end()
        self.initializing = False
        self.parent.checked_for_leaving = True

    def readp(self, pid):
        "lezen van een actie"
        if self.parent.pagedata:  # spul van de vorige actie opruimen
            self.parent.pagedata.clear()
        self.parent.pagedata = shared.Actie[self.parent.parent.datatype](self.parent.fnaam, pid,
                                                                         self.parent.parent.user)
        self.parent.parent.imagelist = self.parent.pagedata.imagelist
        self.parent.old_id = self.parent.pagedata.id
        self.parent.newitem = False

    def nieuwp(self):
        """voorbereiden opvoeren nieuwe actie"""
        shared.log('opvoeren nieuwe actie')
        self.parent.newitem = True
        if self.leavep():
            if self.parent.current_tab == 0:
                self.parent.parent.gui.enable_book_tabs(True, tabfrom=1)
            self.parent.pagedata = shared.Actie[self.parent.parent.datatype](self.parent.fnaam, 0,
                                                                             self.parent.parent.user)
            self.parent.parent.imagelist = self.parent.pagedata.imagelist
            self.parent.newitem = True
            if self.parent.current_tab == 1:
                self.vulp()  # om de velden leeg te maken
                self.gui.set_focus()
            else:
                self.goto_page(1, check=False)
        else:
            self.parent.newitem = False
            shared.log("leavep() geeft False: nog niet klaar met huidige pagina")

    def leavep(self):
        "afsluitende acties uit te voeren alvorens de pagina te verlaten"
        newbuf = self.gui.build_newbuf()
        if self.parent.current_tab == 1 and self.parent.newitem and newbuf[0] == "" \
                and newbuf[1] == "" and not self.parent.parent.exiting:
            self.parent.newitem = False
            self.parent.pagedata = shared.Actie[self.parent.parent.datatype](self.parent.fnaam,
                                                                             self.parent.old_id,
                                                                             self.parent.parent.user)
        ok_to_leave = True
        self.parent.checked_for_leaving = True
        if self.parent.current_tab == 0:
            shared.log('%s %s', self.parent.parent.mag_weg, self.parent.newitem)
            if not self.parent.parent.mag_weg and not self.parent.newitem:
                ok_to_leave = False
        elif newbuf != self.oldbuf:
            print(self.oldbuf)
            print(newbuf)
            message = "\n".join(("De gegevens op de pagina zijn gewijzigd, ",
                                 "wilt u de wijzigingen opslaan voordat u verder gaat?"))
            ok, cancel = gui.ask_cancel_question(self.gui, message)
            if ok:
                ok_to_leave = self.savep()
            elif cancel:
                self.parent.checked_for_leaving = ok_to_leave = False
            if not cancel:
                self.parent.parent.gui.enable_all_other_tabs()
        return ok_to_leave

    def savep(self):
        "gegevens van een actie opslaan afhankelijk van pagina"
        if not self.gui.can_save:
            return False
        self.gui.enable_buttons(False)
        if self.parent.current_tab <= 1 or self.parent.current_tab == 6:
            return False
        wijzig = False
        text = self.gui.get_textarea_contents()
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
            self.parent.page0.gui.set_item_text(self.parent.page0.gui.get_selection(), 3,
                                                self.parent.pagedata.updated)
        return True

    def savepgo(self):
        "opslaan en naar de volgende pagina"
        if not self.gui.can_saveandgo():
            return
        if self.savep():
            self.goto_next()
        else:
            self.enable_buttons()

    def restorep(self):
        "oorspronkelijke (laatst opgeslagen) inhoud van de pagina herstellen"
        # reset font - are these also needed: case? indent? linespacing? paragraphspacing?
        if self.parent.current_tab > 1:
            self.gui.reset_font()
        self.vulp()

    def on_text(self):
        """callback voor EVT_TEXT

        de initializing flag wordt uitgevraagd omdat deze event ook tijdens vulp()
        en tijdens vul_combos plaatsvindt"""
        if not self.initializing:
            newbuf = self.gui.build_newbuf()
            changed = newbuf != self.oldbuf
            self.enable_buttons(changed)

    def on_choice(self):
        "callback voor combobox"
        self.enable_buttons()

    def update_actie(self):
        """pass page data from the GUI to the internal storage
        """
        self.parent.pagedata.imagecount = self.parent.parent.imagecount
        self.parent.pagedata.imagelist = self.parent.parent.imagelist
        if self.parent.parent.datatype == shared.DataType.SQL.name:
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
        self.gui.enable_buttons(state)
        if self.parent.current_tab > 0:
            self.parent.parent.gui.enable_all_other_tabs()

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
        self.parent.parent.gui.set_page(next)

    def goto_prev(self):
        "naar de vorige pagina gaan"
        if not self.leavep():
            return
        next = self.parent.current_tab - 1
        if next < 0:
            next = self.parent.pages
        self.parent.parent.gui.set_page(next)

    def goto_page(self, page_num, check=True):
        "naar de aangegeven pagina gaan"
        if check and not self.leavep():
            return
        if 0 <= page_num <= self.parent.pages:
            self.parent.parent.gui.set_page(page_num)


class Page0(Page):
    "pagina 0: overzicht acties"
    def __init__(self, parent):
        self.parent = parent
        Page.__init__(self, parent, pageno=0, standard=False)
        self.selection = 'excl. gearchiveerde'
        self.sel_args = {}
        self.sorted = (0, "A")

        widths = [94, 24, 146, 90, 400] if LIN else [64, 24, 114, 72, 292]
        if self.parent.parent.datatype == shared.DataType.SQL.name:
            widths[4] = 90 if LIN else 72
            extra = 310 if LIN else 220
            widths.append(extra)

        self.gui = gui.Page0Gui(parent, self, widths)

        self.sort_via_options = False

    def vulp(self):
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina
        """
        self.saved_sortopts = None
        if (self.parent.parent.datatype == shared.DataType.SQL.name
                and self.parent.parent.filename):
            if self.parent.parent.is_user:
                self.saved_sortopts = dmls.SortOptions(self.parent.parent.filename)
                test = self.saved_sortopts.load_options()
                test = bool(test)
                self.sort_via_options = test
                value = not test
            else:
                value = False
            self.gui.enable_sorting(value)

        self.seltitel = 'alle meldingen ' + self.selection
        Page.vulp(self)
        msg = ''
        if self.parent.rereadlist:
            self.parent.data = {}
            select = self.sel_args.copy()
            arch = ""  # "alles"
            if "arch" in select:
                arch = select.pop("arch")

            # try:
            data = shared.get_acties[self.parent.parent.datatype](self.parent.fnaam, select,
                                                                  arch, self.parent.parent.user)
            # except (dmlx.DataError, dmls.dataError) as msg:
            #     print("samenstellen lijst mislukt: " + str(msg))
            #     raise
            for idx, item in enumerate(data):
                if self.parent.parent.datatype == shared.DataType.XML.name:
                    # nummer, start, stat, cat, titel, gewijzigd = item
                    self.parent.data[idx] = (item[0],
                                             item[1],
                                             ".".join((item[3][1], item[3][0])),
                                             ".".join((item[2][1], item[2][0])),
                                             item[5],
                                             item[4])
                elif self.parent.parent.datatype == shared.DataType.SQL.name:
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
            # if self.parent.parent.datatype == shared.DataType.XML.name:
            #     self.p0list.sortItems(self.sorted[0], sortorder[self.sorted[1]])  # , True)
            #
            self.parent.current_item = self.gui.get_first_item()
            # self.parent.rereadlist = False  # (wordt al uitgezet in rereadlist)
        # for i in range(1, self.parent.count()):
        #     self.parent.setTabEnabled(i, False)
        self.parent.parent.gui.enable_all_book_tabs(False)
        self.gui.enable_buttons()
        if self.gui.has_selection():
            self.parent.parent.gui.enable_all_book_tabs(True)
        # self.parent.parent.setToolTip("{0} - {1} items".format(
        #     self.parent.pagehelp[self.parent.current_tab], len(self.parent.data)))
        self.gui.set_selection()
        self.gui.ensure_visible(self.parent.current_item)
        self.parent.parent.set_statusmessage(msg)

    def populate_list(self):
        "list control vullen"
        self.gui.clear_list()

        self.parent.rereadlist = False
        items = self.parent.data.items()
        if items is None:
            self.parent.parent.set_statusmessage('Selection is None?')
        if not items:
            return

        for _, data in items:
            new_item = self.gui.add_listitem(data[0])
            self.gui.set_listitem_values(new_item, [data[0]] + list(data[2:]))

    def change_selected(self, item_n):
        """callback voor wijzigen geselecteerd item, o.a. door verplaatsen van de
        cursor of door klikken
        """
        print('in page0.change_selected')
        self.parent.current_item = item_n
        self.gui.set_selection()
        print('  current_item is', item_n)
        if not self.parent.newitem:
            selindx = self.gui.get_selected_action()
            print('  got selected action:', selindx)
            self.readp(selindx)
        hlp = "&Herleef" if self.parent.pagedata.arch else "&Archiveer"
        self.gui.set_archive_button_text(hlp)

    def activate_item(self):
        """callback voor activeren van item, door doubleclick of enter
        """
        print('in page0.change_selected')
        self.goto_actie()

    def select_items(self):
        """tonen van de selectie dialoog

        niet alleen selecteren op tekst(deel) maar ook op status, soort etc
        """
        args = self.sel_args, None
        if self.parent.parent.datatype == shared.DataType.SQL.name:
            data = dmls.SelectOptions(self.parent.fnaam, self.parent.parent.user)
            args, sel_args = data.load_options(), {}
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
            args = sel_args, data
        while True:
            test = gui.show_dialog(self.gui, gui.SelectOptionsDialog, args)
            if not test:
                break
            self.parent.rereadlist = True
            try:
                self.vulp()
            except (dmlx.DataError, dmls.DataError) as msg:
                self.parent.rereadlist = False
                gui.show_message(self, str(msg))
            else:
                break

    def sort_items(self):
        """tonen van de sorteer-opties dialoog

        sortering mogelijk op datum/tijd, soort, titel, status via schermpje met
        2x4 comboboxjes waarin je de volgorde van de rubrieken en de sorteervolgorde
        per rubriek kunt aangeven"""
        sortopts, sortlist = {}, []
        if self.parent.parent.datatype == shared.DataType.SQL.name:
            sortopts = self.saved_sortopts.load_options()
            try:
                sortlist = [x[0] for x in dmls.SORTFIELDS]
            except AttributeError:
                pass
        if not sortlist:
            sortlist = [x for x in self.parent.ctitels]
            sortlist[1] = "Soort"
        sortlist.insert(0, "(geen)")
        args = sortopts, sortlist
        test = gui.show_dialog(self.gui, gui.SortOptionsDialog, args)
        if not test:
            return
        if self.sort_via_options:
            self.gui.enable_sorting(False)
            self.parent.rereadlist = True
            try:
                self.vulp()
            except (dmlx.DataError, dmls.DataError) as msg:
                self.parent.rereadlist = False
                gui.show_message(self, str(msg))
        else:
            self.gui.enable_sorting(True)

    def archiveer(self):
        "archiveren of herleven van het geselecteerde item"
        selindx = self.gui.get_selected_action()
        if self.parent.parent.datatype == shared.DataType.XML.name:
            selindx = shared.data2str(selindx)
        else:
            selindx = shared.data2int(selindx)
        self.readp(selindx)
        if self.parent.parent.datatype == shared.DataType.XML.name:
            self.parent.pagedata.arch = not self.parent.pagedata.arch
            hlp = "gearchiveerd" if self.parent.pagedata.arch else "herleefd"
            self.parent.pagedata.events.append((shared.get_dts(), "Actie {0}".format(hlp)))
        elif self.parent.parent.datatype == shared.DataType.SQL.name:
            self.parent.pagedata.set_arch(not self.parent.pagedata.arch)
        self.update_actie()  # self.parent.pagedata.write()
        self.parent.rereadlist = True
        self.vulp()
        self.parent.parent.gui.set_tabfocus(0)
        # het navolgende geldt alleen voor de selectie "gearchiveerd en actief"
        if self.sel_args.get("arch", "") == "alles":
            self.gui.ensure_visible(self.parent.current_item)
            hlp = "&Herleef" if self.parent.pagedata.arch else "&Archiveer"
            self.gui.set_archive_button_text(hlp)

    def enable_buttons(self):
        "buttons wel of niet bruikbaar maken"
        self.gui.enable_buttons()

    def get_items(self):
        "retrieve all listitems"
        return self.gui.get_items()

    def get_item_text(self, item_or_index, column):
        "get the item's text for a specified column"
        return self.gui.get_item_text(item_or_index, column)

    def clear_selection(self):
        "initialize selection criteria"
        self.sel_args = {}


class Page1(Page):
    "pagina 1: startscherm actie"
    def __init__(self, parent):
        self.parent = parent
        Page.__init__(self, parent, pageno=0, standard=False)
        self.gui = gui.Page1Gui(parent, self)

    def vulp(self):
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina"""
        Page.vulp(self)
        self.initializing = True
        self.gui.init_fields()
        self.parch = False
        if self.parent.pagedata is not None:  # and not self.parent.newitem:
            self.gui.set_text('id', str(self.parent.pagedata.id))
            self.gui.set_text('date', self.parent.pagedata.datum)
            self.parch = self.parent.pagedata.arch
            if self.parent.parent.datatype == shared.DataType.XML.name:
                if self.parent.pagedata.titel is not None:
                    if " - " in self.parent.pagedata.titel:
                        hlp = self.parent.pagedata.titel.split(" - ", 1)
                    else:
                        hlp = self.parent.pagedata.titel.split(": ", 1)
                    self.gui.set_text('proc', hlp[0])
                    if len(hlp) > 1:
                        self.gui.set_text('desc', hlp[1])
            elif self.parent.parent.datatype == shared.DataType.SQL.name:
                self.gui.set_text('proc', self.parent.pagedata.over)
                self.gui.set_text('desc', self.parent.pagedata.titel)
            self.gui.set_choice('stat', self.parent.pagedata.status)
            self.gui.set_choice('cat', self.parent.pagedata.soort)

        self.oldbuf = self.gui.set_oldbuf()
        if self.parch:
            aanuit = False
            if self.parent.parent.datatype == shared.DataType.XML.name:
                if self.parent.pagedata.titel is not None:
                    if " - " in self.parent.pagedata.titel:
                        hlp = self.parent.pagedata.titel.split(" - ", 1)
                    else:
                        hlp = self.parent.pagedata.titel.split(": ", 1)
                    self.gui.set_text('proc', hlp[0])
                    if len(hlp) > 1:
                        self.gui.set_text('desc', hlp[1])
            elif self.parent.parent.datatype == shared.DataType.SQL.name:
                self.gui.set_text('proc', self.parent.pagedata.over)
                self.gui.set_text('desc', self.parent.pagedata.titel)
            self.gui.set_text('arch', "Deze actie is gearchiveerd")
            self.gui.set_archive_button_text("Herleven")
        else:
            aanuit = True
            self.gui.set_text('arch', '')
            self.gui.set_archive_button_text("Archiveren")

        if not self.parent.parent.is_user:
            aanuit = False
        self.gui.enable_fields(aanuit)

        self.initializing = False

    def savep(self):
        "opslaan van de paginagegevens"
        Page.savep(self)
        proc = self.gui.get_text('proc')
        self.gui.set_text('proc', proc.capitalize())
        self.enable_buttons(False)
        desc = self.gui.get_text('desc')
        if proc == "" or desc == "":
            gui.show_message(self.gui, "Beide tekstrubrieken moeten worden ingevuld")
            return False
        wijzig = False
        procdesc = " - ".join((proc, desc))
        if procdesc != self.parent.pagedata.titel:
            if self.parent.parent.datatype == shared.DataType.XML.name:
                self.parent.pagedata.titel = procdesc
            elif self.parent.parent.datatype == shared.DataType.SQL.name:
                self.parent.pagedata.over = proc
                self.parent.pagedata.events.append(
                    (shared.get_dts(), 'Onderwerp gewijzigd in "{0}"'.format(proc)))
                self.parent.pagedata.titel = procdesc = desc
            self.parent.pagedata.events.append(
                (shared.get_dts(), 'Titel gewijzigd in "{0}"'.format(procdesc)))
            wijzig = True
        newstat, sel = self.gui.get_choice_data('stat')
        print(newstat, sel)
        if newstat != self.parent.pagedata.status:
            self.parent.pagedata.status = newstat
            self.parent.pagedata.events.append(
                (shared.get_dts(), 'Status gewijzigd in "{0}"'.format(sel)))
            wijzig = True
        newcat, sel = self.gui.get_choice_data('cat')
        print(newcat, sel)
        if newcat != self.parent.pagedata.soort:
            self.parent.pagedata.soort = newcat
            self.parent.pagedata.events.append(
                (shared.get_dts(), 'Categorie gewijzigd in "{0}"'.format(sel)))
            wijzig = True
        if self.parch != self.parent.pagedata.arch:
            self.parent.pagedata.set_arch(self.parch)
            hlp = "gearchiveerd" if self.parch else "herleefd"
            self.parent.pagedata.events.append(
                (shared.get_dts(), "Actie {0}".format(hlp)))
            wijzig = True
        if wijzig:
            self.update_actie()
            if self.parent.newitem:
                # nieuwe entry maken in de tabel voor panel 0
                newindex = len(self.parent.data)  # + 1
                itemdata = (self.gui.get_text('date'),
                            " - ".join((self.gui.get_text('proc'), self.gui.get_text('desc'))),
                            self.gui.get_choice_data('stat')[0], self.gui.get_choice_data('cat')[0],
                            self.gui.get_text('id'))
                self.parent.data[newindex] = itemdata  # waarom niet append?
                # ook nieuwe entry maken in de visuele tree
                self.parent.current_item = self.parent.page0.gui.add_listitem(itemdata[0])
                self.parent.page0.gui.set_selection()
                self.parent.newitem = False  # is None niet correcter?
                self.parent.rereadlist = True
                self.parent.page0.enable_buttons()  # True)
            # teksten op panel 0 bijwerken
            item = self.parent.page0.gui.get_selection()
            self.parent.page0.gui.set_item_text(item, 1,
                                                self.parent.pagedata.get_soorttext()[0].upper())
            self.parent.page0.gui.set_item_text(item, 2, self.parent.pagedata.get_statustext())
            self.parent.page0.gui.set_item_text(item, 3, self.parent.pagedata.updated)
            if self.parent.parent.datatype == shared.DataType.XML.name:
                self.parent.page0.gui.set_item_text(item, 4, self.parent.pagedata.titel)
            elif self.parent.parent.datatype == shared.DataType.SQL.name:
                self.parent.page0.gui.set_item_text(item, 4, self.parent.pagedata.over)
                self.parent.page0.gui.set_item_text(item, 5, self.parent.pagedata.titel)
            self.oldbuf = self.gui.set_oldbuf()
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
        self.gui.clear_stats()
        self.gui.clear_cats()
        for key in sorted(self.parent.cats.keys()):
            text, value = self.parent.cats[key][:2]
            self.gui.add_cat_choice(text, value)
        for key in sorted(self.parent.stats.keys()):
            text, value = self.parent.stats[key][:2]
            self.gui.add_stat_choice(text, value)
        self.initializing = False

    def get_entry_text(self, entry_type):
        "return an entry field's text"
        return self.gui.get_entry_text(entry_type)


class Page6(Page):
    "pagina 6: voortgang"
    def __init__(self, parent):
        Page.__init__(self, parent, pageno=6, standard=False)
        self.current_item = 0
        self.oldtext = ""
        self.gui = gui.Page6Gui(parent, self)

    def vulp(self):
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina"""
        Page.vulp(self)
        self.initializing = True
        self.event_list, self.event_data, self.old_list, self.old_data = [], [], [], []
        self.gui.init_textfield()
        # self.progress_text.clear()
        # self.progress_text.setReadOnly(True)

        if self.parent.pagedata:
            self.event_list = [x[0] for x in self.parent.pagedata.events]
            self.event_list.reverse()
            self.old_list = self.event_list[:]
            self.event_data = [x[1] for x in self.parent.pagedata.events]
            self.event_data.reverse()
            self.old_data = self.event_data[:]
            if self.parent.parent.is_user:
                text = '-- doubleclick or press Shift-Ctrl-N to add new item --'
            else:
                text = '-- adding new items is disabled --'
            self.gui.init_list(text)
            # self.progress_list.clear()
            # first_item = qtw.QListWidgetItem(text)
            # first_item.setData(core.Qt.UserRole, -1)
            # self.progress_list.addItem(first_item)
            for idx, datum in enumerate(self.event_list):
                self.gui.add_item_to_list(idx, datum)
                # # convert to HTML (if needed) and back
                # self.progress_text.set_contents(self.event_data[idx])
                # tekst_plat = self.progress_text.toPlainText()
                # try:
                #     text = tekst_plat.split("\n")[0].strip()
                # except AttributeError:
                #     text = tekst_plat or ""
                # text = text if len(text) < 80 else text[:80] + "..."
                # newitem = qtw.QListWidgetItem('{} - {}'.format(datum, text))
                # newitem.setData(core.Qt.UserRole, idx)
                # self.progress_list.addItem(newitem)
        if self.parent.parent.datatype == shared.DataType.SQL.name:
            self.gui.set_list_callback()
            # if self.parent.parent.is_user:
            #     self.progress_list.itemActivated.connect(self.on_activate_item)
            #     # action = qtw.QShortcut('Shift+Ctrl+N', self, functools.partial(
            #     #     self.on_activate_item, self.progress_list.item(0)))
            #     self.new_action.activated.connect(functools.partial(self.on_activate_item,
            #                                                         self.progress_list.item(0)))
            # else:
            #     try:
            #         self.progress_list.itemActivated.disconnect()
            #         self.new_action.activated.disconnect()
            #     except TypeError:
            #         # avoid "disconnect() failed between 'itemActivated' and all its connections"
            #         pass
        self.gui.clear_textfield()
        self.oldbuf = (self.old_list, self.old_data)
        self.oldtext = ''
        self.initializing = False

    def savep(self):
        "opslaan van de paginagegevens"
        Page.savep(self)
        # voor het geval er na het aanpassen van een tekst direkt "sla op" gekozen is
        # nog even kijken of de tekst al in self.event_data is aangepast.
        idx = self.current_item
        hlp = self.gui.get_textfield_contents()
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
            self.gui.set_listitem_text(idx + 1, "{} - {}".format(self.event_list[idx], short_text))
            self.gui.set_listitem_data(idx + 1)
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
            # waar is deze voor (self.book.current_item.setText) ?
            # self.parent.current_item = self.parent.page0.p0list.topLevelItem(x)
            # self.parent.current_item.setText(4, self.parent.pagedata.updated)
            self.parent.page0.gui.set_item_text(self.parent.current_item, 3,
                                                self.parent.pagedata.updated)
            # dit was self.parent.page0.p0list.currentItem().setText( -- is dat niet hetzelfde?
            self.old_list = self.event_list[:]
            self.old_data = self.event_data[:]
            self.oldbuf = (self.old_list, self.old_data)
        else:
            print("Leuk hoor, er was niks gewijzigd ! @#%&*Grrr")
        return True

    def goto_prev(self):
        "set the selection to the previous row, if possible"
        test = self.gui.get_list.row() - 1
        if test > 0:
            self.gui.set_list.row(test)

    def goto_next(self):
        "set the selection to the next row, if possible"
        test = self.gui.get_list.row() + 1
        if test < self.gui.get_list_rowcount():
            self.gui.set_list.row(test)

    def activate_item(self, item):
        """callback voor dubbelklik of Enter op een item

        wanneer dit gebeurt op het eerste item kan een nieuwe worden aangemaakt
        """
        if self.initializing:
            return
        if item is None:  # or self.gui.is_first_line(item): -- blijkt niet nodig te zijn
            self.oldtext = self.gui.add_entry()

    def select_item(self):
        """callback voor het selecteren van een item

        selecteren van (klikken op) een regel in de listbox doet de inhoud van de
        textctrl ook veranderen. eerst controleren of de tekst veranderd is
        dat vragen moet ook in de situatie dat je op een geactiveerde knop klikt,
        het panel wilt verlaten of afsluiten
        de knoppen onderaan doen de hele lijst bijwerken in self.parent.book.p
        """
        self.current_item = self.gui.get_list_row()
        indx = self.current_item - 1
        if indx == -1:
            self.oldtext = ""
        else:
            self.oldtext = self.event_data[indx]  # dan wel item_n.text()
        self.initializing = True
        self.oldtext = self.gui.convert_text(self.oldtext, to='rich')
        self.initializing = False
        if not self.parent.pagedata.arch:
            if indx > -1:
                self.gui.protect_textfield(not self.parent.parent.is_user)
                self.gui.enable_toolbar(self.parent.parent.is_user)
            self.gui.move_cursor_to_end()
        self.gui.set_focus_to_textfield()

    def on_text(self):
        """callback voor wanneer de tekst gewijzigd is

        de initializing flag wordt uitgevraagd omdat deze event ook tijdens vulp()
        en wijzigen van list positie plaatsvindt
        """
        if self.initializing:
            return
        # lees de inhoud van het tekstveld en vergelijk deze met de buffer
        tekst = self.gui.get_textfield_contents()
        # str(self.progress_text.get_contents())  # self.progress_list.GetItemText(ix)
        if tekst != self.oldtext:
            # stel de buffer in op de nieuwe tekst
            self.oldtext = tekst
            # maak er platte tekst van om straks in de listbox bij te werken
            tekst_plat = self.gui.convert_text(self.oldtext, to='plain')
            # stel in dat we niet van dit scherm af kunnen zonder te updaten
            if self.parent.parent.is_user:
                self.enable_buttons()
            self.current_item = self.gui.get_list_row()
            if self.current_item > 0:
                indx = self.current_item - 1
                self.event_data[indx] = tekst
                # item = self.progress_list.currentItem()
                # datum = str(item.text()).split(' - ')[0]
                datum = self.gui.get_listitem_text(self.current_item).split(' - ')[0]
                short_text = ' - '.join((datum, tekst_plat.split("\n")[0]))
                if len(short_text) >= 80:
                    short_text = short_text[:80] + "..."
                # item.setText(short_text)
                self.gui.set_listitem_text(self.current_item, short_text)


class TabOptions:
    "hulp klasse bij dialoog voor mogelijke tab headers"
    def initstuff(self, parent):
        "aanvullende initialisatie"
        self.titel = "Tab titels"
        self.data = []
        for key in sorted(parent.master.book.tabs.keys()):
            tab_text = parent.master.book.tabs[key].split(" ", 1)[1]
            self.data.append(tab_text)
        self.tekst = ["De tab titels worden getoond in de volgorde",
                      "zoals ze van links naar rechts staan.",
                      "Er kunnen geen tabs worden verwijderd of toegevoegd."]
        self.editable = False

    def leesuit(self, parent, optionslist):
        "wijzigingen doorvoeren"
        self.newtabs = {}
        for idx, item in enumerate(optionslist):
            self.newtabs[str(idx)] = str(item)
        parent.master.save_settings("tab", self.newtabs)


class StatOptions:
    "hulp klasse bij dialoog voor de mogelijke statussen"
    def initstuff(self, parent):
        "aanvullende initialisatie"
        self.titel = "Status codes en waarden"
        self.data = []
        for key in sorted(parent.master.book.stats.keys()):
            if parent.master.datatype == shared.DataType.XML.name:
                item_text, item_value = parent.master.book.stats[key]
                self.data.append(": ".join((item_value, item_text)))
            elif parent.master.datatype == shared.DataType.SQL.name:
                item_text, item_value, row_id = parent.master.book.stats[key]
                self.data.append(": ".join((item_value, item_text, row_id)))
        self.tekst = ["De waarden voor de status worden getoond in dezelfde volgorde",
                      "als waarin ze in de combobox staan.",
                      "Vóór de dubbele punt staat de code, erachter de waarde.",
                      "Denk erom dat als je codes wijzigt of statussen verwijdert, deze",
                      "ook niet meer getoond en gebruikt kunnen worden in de registratie."]
        self.editable = True

    def leesuit(self, parent, optionslist):
        "wijzigingen doorvoeren"
        self.newstats = {}
        for sortkey, item in enumerate(optionslist):
            try:
                value, text = str(item).split(": ")
            except ValueError:
                return 'Foutieve waarde: bevat geen dubbele punt'
            self.newstats[value] = (text, sortkey)
        parent.master.save_settings("stat", self.newstats)
        return ''


class CatOptions:
    "hulp klasse bij dialoog voor de mogelijke categorieen"
    def initstuff(self, parent):
        "aanvullende initialisatie"
        self.titel = "Soort codes en waarden"
        self.data = []
        for key in sorted(parent.master.book.cats.keys()):
            if parent.master.datatype == shared.DataType.XML.name:
                item_value, item_text = parent.master.book.cats[key]
                self.data.append(": ".join((item_text, item_value)))
            elif parent.master.datatype == shared.DataType.SQL.name:
                item_value, item_text, row_id = parent.master.book.cats[key]
                self.data.append(": ".join((item_text, item_value, str(row_id))))
        self.tekst = ["De waarden voor de soorten worden getoond in dezelfde volgorde",
                      "als waarin ze in de combobox staan.",
                      "Vóór de dubbele punt staat de code, erachter de waarde.",
                      "Denk erom dat als je codes wijzigt of soorten verwijdert, deze",
                      "ook niet meer getoond en gebruikt kunnen worden in de registratie."]
        self.editable = True

    def leesuit(self, parent, optionslist):
        "wijzigingen doorvoeren"
        self.newcats = {}
        for sortkey, item in enumerate(optionslist):
            try:
                value, text = str(item).split(": ")
            except ValueError:
                return 'Foutieve waarde: bevat geen dubbele punt'
            self.newcats[value] = (text, sortkey)
        parent.master.save_settings("cat", self.newcats)
        return ''


class MainWindow():
    """Hoofdscherm met menu, statusbalk, notebook en een "quit" button"""
    def __init__(self, parent, fnaam="", version=None):
        if not version:
            raise ValueError('No data method specified')
        self.parent = parent
        self.datatype = version
        self.title = 'Actieregistratie'
        self.initializing = True
        self.exiting = False
        self.mag_weg = True
        self.helptext = ''
        self.pagedata = self.oldbuf = None
        self.is_newfile = self.newitem = False
        self.oldsort = -1
        self.idlist = self.actlist = self.alist = []
        shared.log('fnaam is %s', fnaam)
        if fnaam and not os.path.exists(fnaam):
            shared.log('switched to SQL')
            self.datatype = shared.DataType.SQL.name
            if fnaam == 'sql':
                fnaam = ''
        if self.datatype == shared.DataType.XML.name:
            test = pathlib.Path(fnaam)
            self.dirname, self.filename = test.parent, test.name
            shared.log('XML: %s %s', self.dirname, self.filename)
        elif self.datatype == shared.DataType.SQL.name:
            self.filename = ""
            self.projnames = dmls.get_projnames()
            if fnaam:
                test = fnaam.lower()
                for x in self.projnames:
                    if x[0].lower() == test:
                        if test == 'basic':
                            self.filename = '_basic'
                        else:
                            self.filename = x[0]
                        break
            shared.log('SQL: %s', self.filename)
        self.gui = gui.MainGui(self)
        self.create_book_pages()

        self.user = None    # start without user
        self.is_user = self.is_admin = False
        if self.datatype == shared.DataType.XML.name:
            self.user = 1  # pretend user
            self.is_user = self.is_admin = True  # force editability for XML mode

        if self.datatype == shared.DataType.XML.name:
            if self.filename == "":
                self.open_xml()
            else:
                self.startfile()
        elif self.datatype == shared.DataType.SQL.name:
            if self.filename:
                self.open_sql(do_sel=False)
            else:
                self.open_sql()
        self.initializing = False

    def get_menu_data(self):
        """Define application menu
        """
        data = [("&File", [("&Open", self.open_xml, 'Ctrl+O', " Open a new file"),
                           ("&New", self.new_file, 'Ctrl+N', " Create a new file"),
                           ('',),
                           ("&Print", (("Dit &Scherm", self.print_scherm, 'Shift+Ctrl+P',
                                        "Print the contents of the current screen"),
                                       ("Deze &Actie", self.print_actie, 'Alt+Ctrl+P',
                                        "Print the contents of the current issue"))),
                           ('',),
                           ("&Quit", self.exit_app, 'Ctrl+Q', " Terminate the program")]),
                ("&Login", [("&Go", self.sign_in, 'Ctrl+L', " Sign in to the database")]),
                ("&Settings", (("&Applicatie", (("&Lettertype", self.font_settings, '',
                                                 " Change the size and font of the text"),
                                                ("&Kleuren", self.colour_settings, '',
                                                 " Change the colours of various items"))),
                               ("&Data", (("&Tabs", self.tab_settings, '',
                                           " Change the titles of the tabs"),
                                          ("&Soorten", self.cat_settings, '',
                                           " Add/change type categories"),
                                          ("St&atussen", self.stat_settings, '',
                                           " Add/change status categories"))),
                               ("&Het leven", self.silly_menu, '',
                                " Change the way you look at life"))),
                ("&Help", (("&About", self.about_help, 'F1', " Information about this program"),
                           ("&Keys", self.hotkey_help, 'Ctrl+H', " List of shortcut keys")))]
        if self.datatype == shared.DataType.XML.name:
            data.pop(1)
        elif self.datatype == shared.DataType.SQL.name:
            data[0][1][0] = ("&Other project", self.open_sql, 'Ctrl+O', " Select a project")
            data[0][1][1] = ("&New", self.new_file, 'Ctrl+N', " Create a new project")
        return data

    def create_book(self, book):
        """define the tabbed interface and its subclasses
        """
        self.book = book
        self.book.parent = self
        self.book.fnaam = ""
        if self.filename and self.datatype == shared.DataType.SQL.name:
            self.book.fnaam = self.filename
        self.book.current_item = None
        self.book.data = {}
        self.book.rereadlist = True
        self.lees_settings()
        self.book.ctitels = ["actie", " ", "status", "L.wijz."]
        if self.datatype == shared.DataType.XML.name:
            self.book.ctitels.append("titel")
        elif self.datatype == shared.DataType.SQL.name:
            self.book.ctitels.extend(("betreft", "omschrijving"))
        self.book.current_tab = -1
        self.book.newitem = False
        self.book.pagedata = None

    def create_book_pages(self):
        "add the pages to the tabbed widget"
        self.book.page0 = Page0(self.book)
        self.book.page1 = Page1(self.book)
        self.book.page2 = Page(self.book, 2)
        self.book.page3 = Page(self.book, 3)
        self.book.page4 = Page(self.book, 4)
        self.book.page5 = Page(self.book, 5)
        self.book.page6 = Page6(self.book)
        self.book.pages = 7
        self.book.checked_for_leaving = True

        self.gui.add_book_tab(self.book.page0, "&" + self.book.tabs[0])
        self.gui.add_book_tab(self.book.page1, "&" + self.book.tabs[1])
        self.gui.add_book_tab(self.book.page2, "&" + self.book.tabs[2])
        self.gui.add_book_tab(self.book.page3, "&" + self.book.tabs[3])
        self.gui.add_book_tab(self.book.page4, "&" + self.book.tabs[4])
        self.gui.add_book_tab(self.book.page5, "&" + self.book.tabs[5])
        self.gui.add_book_tab(self.book.page6, "&" + self.book.tabs[6])
        self.gui.enable_all_book_tabs(False)

    def not_implemented_message(self):
        "information"
        gui.show_message(self.gui, "Sorry, werkt nog niet")

    def new_file(self, event=None):
        "Menukeuze: nieuw file"
        if self.datatype == shared.DataType.SQL.name:
            self.not_implemented_message()
            return
        self.is_newfile = False
        # self.dirname = str(self.dirname)  # defaults to '.' so no need for `or os.getcwd()`
        fname = gui.get_save_filename(self.gui, start=self.dirname)
        if fname:
            test = pathlib.Path(fname)
            self.dirname, self.filename = test.parent, test.name
            self.is_newfile = True
            self.startfile()
            self.is_newfile = False
            self.gui.enable_all_booktabs(False)

    def open_xml(self, event=None):
        "Menukeuze: open file"
        shared.log('in open_xml: %s', self.filename)
        self.dirname = self.dirname or os.getcwd()
        fname = gui.get_open_filename(self.gui, start=self.dirname)
        if fname:
            test = pathlib.Path(fname)
            self.dirname, self.filename = test.parent, test.name
            self.startfile()

    def open_sql(self, event=None, do_sel=True):
        "Menukeuze: open project"
        shared.log('in open_sql: %s', self.filename)
        current = choice = 0
        data = self.projnames
        if self.filename in data:
            current = data.index(self.filename)
        if do_sel:
            choice = gui.get_choice_item(self.gui, 'Kies een project om te openen',
                                         [": ".join((h[0], h[2])) for h in data], current)
        else:
            for h in data:
                shared.log(h)
                if h[0] == self.filename or (h[0] == 'basic' and self.filename == "_basic"):
                    choice = h[0]
                    break
        if choice:
            self.filename = choice.split(': ')[0]
            if self.filename in ("Demo", 'basic'):
                self.filename = "_basic"
            self.startfile()

    def print_scherm(self, event=None):
        "Menukeuze: print dit scherm"
        self.printdict = {'lijst': [], 'actie': [], 'sections': [], 'events': []}
        self.hdr = "Actie: {} {}".format(self.book.pagedata.id,
                                         self.book.pagedata.titel)
        if self.book.current_tab == 0:
            self.hdr = "Overzicht acties uit " + self.filename
            lijst = []
            for item in self.book.page0.get_items():
                actie = self.book.page0.get_item_text(item, 0)
                started = ''
                soort = str(item.text(1))
                for x in self.book.cats.values():
                    oms, code = x[0], x[1]
                    if code == soort:
                        soort = oms
                        break
                status = self.book.page0.get_item_text(item, 2)
                l_wijz = self.book.page0.get_item_text(item, 3)
                titel = self.book.page0.get_item_text(item, 4)
                if self.datatype == shared.DataType.SQL.name:
                    over = titel
                    titel = self.book.page0.get_item_text(item, 5)
                    l_wijz = l_wijz[:19]
                    actie = actie + " - " + over
                    started = started[:19]
                if status != self.book.stats[0][0]:
                    if l_wijz:
                        l_wijz = ", laatst behandeld op " + l_wijz
                    l_wijz = "status: {}{}".format(status, l_wijz)
                else:
                    hlp = "status: {}".format(status)
                    if l_wijz and not started:
                        hlp += ' op {}'.format(l_wijz)
                    l_wijz = hlp
                lijst.append((actie, titel, soort, started, l_wijz))
            self.printdict['lijst'] = lijst
        elif self.book.current_tab == 1:
            data = {x: self.book.page1.get_entry_text(x) for x in ('actie', 'datum', 'oms',
                                                                   'tekst', 'soort', 'status')}
            self.hdr = "Informatie over actie {}: samenvatting".format(data["actie"])
            self.printdict.update(data)
        elif 2 <= self.book.current_tab <= 5:
            title = self.book.tabs[self.book.current_tab].split(None, 1)[1]
            if self.book.current_tab == 2:
                text = self.book.page2.get_textarea_contents()
            elif self.book.current_tab == 3:
                text = self.book.page3.get_textarea_contents()
            elif self.book.current_tab == 4:
                text = self.book.page4.get_textarea_contents()
            elif self.book.current_tab == 5:
                text = self.book.page5.get_textarea_contents()
            self.printdict['sections'] = [(title, text.replace('\n', '<br>'))]
        elif self.book.current_tab == 6:
            events = []
            for idx, data in enumerate(self.book.page6.event_list):
                if self.datatype == shared.DataType.SQL.name:
                    data = data[:19]
                events.append((data, self.book.page6.event_data[idx].replace('\n',
                                                                             '<br>')))
            self.printdict['events'] = events
        self.gui.preview()

    def print_actie(self, event=None):
        "Menukeuze: print deze actie"
        if self.book.pagedata is None or self.book.newitem:
            gui.show_message(self.gui, "Wel eerst een actie kiezen om te printen")
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
        self.gui.preview()

    def exit_app(self, event=None):
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
            self.gui.exit()

    def tab_settings(self, event=None):
        "Menukeuze: settings - data - tab titels"
        gui.show_dialog(self.gui, gui.SettOptionsDialog, args=(TabOptions, "Wijzigen tab titels"))

    def stat_settings(self, event=None):
        "Menukeuze: settings - data - statussen"
        gui.show_dialog(self.gui, gui.SettOptionsDialog, args=(StatOptions, "Wijzigen statussen"))

    def cat_settings(self, event=None):
        "Menukeuze: settings - data - soorten"
        gui.show_dialog(self.gui, gui.SettOptionsDialog, args=(CatOptions, "Wijzigen categorieën"))

    def font_settings(self, event=None):
        "Menukeuze: settings - applicatie - lettertype"
        self.not_implemented_message()

    def colour_settings(self, event=None):
        "Menukeuze: settings - applicatie - kleuren"
        self.not_implemented_message()

    def hotkey_settings(self, event=None):
        "Menukeuze: settings - applicatie- hotkeys (niet geactiveerd)"
        self.not_implemented_message()

    def about_help(self, event=None):
        "Menukeuze: help - about"
        gui.show_message(self.gui, "PyQt versie van mijn actiebox")

    def hotkey_help(self, event=None):
        "menukeuze: help - keys"
        if not self.helptext:
            lines = ["=== Albert's actiebox ===\n",
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
            if self.datatype == shared.DataType.XML.name:
                lines.insert(8, "    Ctrl-O: _o_pen een (ander) actiebestand")
                lines.insert(8, "    Ctrl-N: maak een _n_ieuw actiebestand")
            elif self.datatype == shared.DataType.SQL.name:
                lines.insert(8, "    Ctrl-O: selecteer een (ander) pr_o_ject")
            self.helptext = "\n".join(lines)
        gui.show_message(self.gui, self.helptext)

    def silly_menu(self, event=None):
        "Menukeuze: settings - het leven"
        gui.show_message(self.gui, "Yeah you wish...\nHet leven is niet in te stellen helaas")

    def startfile(self):
        "initialisatie t.b.v. nieuw bestand"
        if self.datatype == shared.DataType.XML.name:
            fullname = self.dirname / self.filename
            retval = dmlx.checkfile(fullname, self.is_newfile)
            if retval != '':
                gui.show_message(self.gui, retval)
                return retval
            self.book.fnaam = fullname
            self.title = self.filename
        elif self.datatype == shared.DataType.SQL.name:
            self.book.fnaam = self.title = self.filename
        self.book.rereadlist = True
        self.book.sorter = None
        self.lees_settings()
        self.gui.set_tab_titles(self.book.tabs)
        self.book.page0.clear_selection()
        self.book.page1.vul_combos()
        if self.book.current_tab == 0:
            self.book.page0.vulp()
        else:
            self.gui.select_first_tab()
        self.book.checked_for_leaving = True
        return ''

    def lees_settings(self):
        """instellingen (tabnamen, actiesoorten en actiestatussen) inlezen"""
        self.book.stats = {0: ('dummy,', 0, 0)}
        self.book.cats = {0: ('dummy,', ' ', 0)}
        self.book.tabs = {0: '0 start'}
        data = shared.Settings[self.datatype](self.book.fnaam)
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
            if self.datatype == shared.DataType.XML.name:
                item_text, sortkey = item
                self.book.stats[int(sortkey)] = (item_text, item_value)
            elif self.datatype == shared.DataType.SQL.name:
                item_text, sortkey, row_id = item
                self.book.stats[int(sortkey)] = (item_text, item_value, row_id)
        for item_value, item in data.cat.items():
            if self.datatype == shared.DataType.XML.name:
                item_text, sortkey = item
                self.book.cats[int(sortkey)] = (item_text, item_value)
            elif self.datatype == shared.DataType.SQL.name:
                item_text, sortkey, row_id = item
                self.book.cats[int(sortkey)] = (item_text, item_value, row_id)
        for tab_num, tab_text in data.kop.items():
            if self.datatype == shared.DataType.XML.name:
                self.book.tabs[int(tab_num)] = " ".join((tab_num, tab_text))
            elif self.datatype == shared.DataType.SQL.name:
                tab_text = tab_text[0]  # , tab_adr = tab_text
                self.book.tabs[int(tab_num)] = " ".join((tab_num, tab_text.title()))

    def save_settings(self, srt, data):
        """instellingen (tabnamen, actiesoorten of actiestatussen) terugschrijven

        argumenten: soort, data
        data is een dictionary die in een van de dialogen TabOptions, CatOptions
        of StatOptions wordt opgebouwd"""
        settings = shared.Settings[self.datatype](self.book.fnaam)
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
                if self.datatype == shared.DataType.XML.name:
                    item_text, sortkey = item
                    self.book.stats[sortkey] = (item_text, item_value)
                elif self.datatype == shared.DataType.SQL.name:
                    item_text, sortkey, row_id = item
                    self.book.stats[sortkey] = (item_text, item_value, row_id)
        elif srt == "cat":
            settings.cat = data
            settings.write()
            self.book.cats = {}
            for item_value, item in data.items():
                if self.datatype == shared.DataType.XML.name:
                    item_text, sortkey = item
                    self.book.cats[sortkey] = (item_text, item_value)
                elif self.datatype == shared.DataType.SQL.name:
                    item_text, sortkey, row_id = item
                    self.book.cats[sortkey] = (item_text, item_value, row_id)
        self.book.page1.vul_combos()

    def print_(self):
        """callback voor ctrl-P(rint)

        vraag om printen scherm of actie, bv. met een InputDialog
        """
        choice, ok = gui.get_choice_item(self.gui, 'Wat wil je afdrukken?',
                                         ['huidig scherm', 'huidige actie'])
        if ok:
            print('printing', choice)
            if choice == 0:
                self.print_scherm()
            else:
                self.print_actie()

    def goto_next(self):
        """redirect to the method of the current page
        """
        Page.goto_next(self.book.widget(self.book.current_tab).master)

    def goto_prev(self):
        """redirect to the method of the current page
        """
        Page.goto_prev(self.book.widget(self.book.current_tab).master)

    def goto_page(self, page):
        """redirect to the method of the current page
        """
        Page.goto_page(self.book.widget(self.book.current_tab).master, page)

    def page_changing(self):
        """deze methode is bedoeld om wanneer er van pagina gewisseld gaat worden
        te controleren of dat wel mogelijk is en zo niet, te melden waarom en de
        paginawissel tegen te houden (ok, terug te gaan naar de vorige pagina).

        PyQT4 kent geen aparte beforechanging methode, daarom is deze methode
        tevens bedoeld om ervoor te zorgen dat na het wisselen
        van pagina het veld / de velden van de nieuwe pagina een waarde krijgen
        met behulp van de vulp methode
        dus mogelijk bij combinatie met wxPython deze methode nog eens opsplitsen
        """
        old = self.book.current_tab
        new = self.book.current_tab = self.gui.get_page()
        if LIN and old == -1:  # bij initialisatie en bij afsluiten - op Windows is deze altijd -1?
            return
        self.gui.enable_all_other_tabs()
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
                item = self.book.page6.get_list_row()  # remember current item
            self.book.page6.vulp()
            if old == new:
                self.book.page6.set_list_row(item)  # reselect item
        self.gui.set_tabfocus(self.book.current_tab)

    # def preview(self):
    #     "callback voor print preview"
    #     self.not_implemented_message()
    #     # self.print_dlg = qtp.QPrintPreviewDialog(self)
    #     # self.print_dlg.paintRequested.connect(self.afdrukken)
    #     # self.print_dlg.exec_()

    # def afdrukken(self, printer):
    #     "wordt aangeroepen door de menuprint methodes"
    #     self.css = ""
    #     if self.css:
    #         self.printdict['css'] = self.css
    #     self.printdict['hdr'] = self.hdr
    #     doc = gui.QTextDocument(self)
    #     html = Template(filename='probreg/actie.tpl').render(**self.printdict)
    #     doc.setHtml(html)
    #     printer.setOutputFileName(self.hdr)
    #     doc.print_(printer)
    #     self.print_dlg.done(True)

    def sign_in(self):
        """aanloggen in SQL/Django mode
        """
        logged_in = False
        while not logged_in:
            ok = gui.show_dialog(self.gui, gui.LoginBox)
            if not ok:
                break
            test = dmls.validate_user(*self.gui.dialog_data)
            if test:
                text = 'Login accepted'
                logged_in = True
            else:
                text = 'Login failed'
            gui.show_message(self.gui, text)
        if logged_in:
            self.user, self.is_user, self.is_admin = test
            self.book.rereadlist = True
            # self.on_page_changing(0) werkt in de bestaande versie ook niet zo

    def enable_settingsmenu(self):
        "instellen of gebruik van settingsmenu mogelijk is"
        self.gui.enable_settingsmenu()

    def set_windowtitle(self, text):
        "build title for window"
        self.gui.set_window_title(text)

    def set_statusmessage(self, msg=''):
        """stel tekst in statusbar in
        """
        if not msg:
            msg = self.book.pagehelp[self.book.current_tab]
            if self.book.current_tab == 0:
                msg += ' - {} items'.format(len(self.book.data))
        self.gui.set_statusmessage(msg)
        if self.datatype == shared.DataType.SQL.name:
            if self.user:
                msg = 'Aangemeld als {}'.format(self.user.username)
            else:
                msg = 'Niet aangemeld'
        self.gui.show_username(msg)


def main(arg=None):
    "opstart routine"
    if arg is None:
        version = shared.DataType.SQL.name
    else:
        version = shared.DataType.XML.name
    try:
        frame = MainWindow(None, arg, version)
    except ValueError as err:
        print(err)
    else:
        frame.gui.go()
