#! usr/bin/env python
"""Actie (was: problemen) Registratie, GUI toolkit onafhankelijke code
"""
import os
# import sys
import pathlib
import datetime
import functools
# import probreg.gui as gui
from probreg import gui
# import probreg.shared as shared   # import DataError, et_projnames
from probreg import shared   # import DataError, et_projnames
import probreg.dml_django as dmls
import probreg.dml_xml as dmlx
# import probreg.dml_mongo as dmlm
LIN = os.name == 'posix'


def db_stat_to_book_stat(item_value, item):
    """zet een in Settings ingelezen status instelling om naar zoals de applicatie deze gebruikt

    subroutine van gemaakt omdat dit op meerdere plekken gebruikt wordt"""
    retval = [item[0], item_value]
    return retval


def db_cat_to_book_cat(item_value, item):
    """zet een in Settings ingelezen categorie instelling om naar zoals de applicatie deze gebruikt

    subroutine van gemaakt omdat dit op meerdere plekken gebruikt wordt"""
    retval = [item[0], item_value]
    return retval


def db_head_to_book_head(tab_num, tab_item):
    """zet een in Settings ingelezen tabheading instelling om naar zoals de applicatie deze gebruikt

    subroutine van gemaakt omdat dit op meerdere plekken gebruikt wordt"""
    return " ".join((tab_num, tab_item[0].title()))


def dbdate2listdate(datestring):
    "opslagdatum EEJJMMDD etc laten zien als dd-mm-EEJJ etc"
    try:
        date = datetime.datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S')
        return date.strftime('%d-%m-%Y %H:%M:%S')
    except ValueError:
        return datestring  # assume other format


def listdate2dbdate(datestring):
    "weergavedatum dd-mm-EEJJ etc omzetten naar opslagdatum EEJJMMDD etc"
    try:  # try old format
        date = datetime.datetime.strptime(datestring, '%d-%m-%Y %H:%M:%S')
        return date.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return datestring  # assume already converted


class Page:
    "base class for notebook page"
    def __init__(self, parent, pageno, standard=True):
        self.parent = parent
        self.appbase = parent.parent
        self.pageno = pageno
        self.is_text_page = standard
        if standard:
            self.gui = gui.PageGui(parent, self)

    def get_toolbar_data(self, textfield):
        "return texts, shortcuts and picture names for setting op toolbar"
        return (('&Bold', 'Ctrl+B', 'icons/sc_bold', 'Toggle Bold', textfield.text_bold,
                 textfield.update_bold),
                ('&Italic', 'Ctrl+I', 'icons/sc_italic', 'Toggle Italic', textfield.text_italic,
                 textfield.update_italic),
                ('&Underline', 'Ctrl+U', 'icons/sc_underline', 'Toggle Underline',
                 textfield.text_underline, textfield.update_underline),
                ('Strike&through', 'Ctrl+~', 'icons/sc_strikethrough', 'Toggle Strikethrough',
                 textfield.text_strikethrough),
                # ("Toggle &Monospace", 'Shift+Ctrl+M', 'icons/text',
                #     'Switch using proportional font off/on', textfield.toggle_monospace),
                (),
                ("&Enlarge text", 'Ctrl+Up', 'icons/sc_grow', 'Use bigger letters',
                 textfield.enlarge_text),
                ("&Shrink text", 'Ctrl+Down', 'icons/sc_shrink', 'Use smaller letters',
                 textfield.shrink_text),
                (),
                ('To &Lower Case', 'Shift+Ctrl+L', 'icons/sc_changecasetolower',
                 'Use lower case letters', textfield.case_lower),
                ('To &Upper Case', 'Shift+Ctrl+U', 'icons/sc_changecasetoupper',
                 'Use upper case letters', textfield.case_upper),
                (),
                ("Indent &More", 'Ctrl+]', 'icons/sc_incrementindent', 'Increase indentation',
                 textfield.indent_more),
                ("Indent &Less", 'Ctrl+[', 'icons/sc_decrementindent', 'Decrease indentation',
                 textfield.indent_less),
                (),
                # ("Normal Line Spacing", '', 'icons/sc_spacepara1',
                #     'Set line spacing to 1', textfield.linespacing_1),
                # ("1.5 Line Spacing",    '', 'icons/sc_spacepara15',
                #     'Set line spacing to 1.5', textfield.linespacing_15),
                # ("Double Line Spacing", '', 'icons/sc_spacepara2',
                #     'Set line spacing to 2', textfield.linespacing_2),
                # (),
                ("Increase Paragraph &Spacing", '', 'icons/sc_paraspaceincrease',
                 'Increase spacing between paragraphs', textfield.increase_paragraph_spacing),
                ("Decrease &Paragraph Spacing", '', 'icons/sc_paraspacedecrease',
                 'Decrease spacing between paragraphs', textfield.decrease_paragraph_spacing))

    def vulp(self):
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina"""
        self.initializing = True
        # if self.appbase.datatype != shared.DataType.MNG:
        if self.parent.current_tab == 0:
            text = self.seltitel
        else:
            state = self.parent.current_tab == 1 and self.parent.newitem
            self.enable_buttons(state)
            text = self.parent.tabs[self.parent.current_tab].split(None, 1)[1]
            if self.parent.pagedata:
                text = self.parent.pagedata.titel
                if self.appbase.use_separate_subject:
                    text = f'{self.parent.pagedata.over} - {text}'
                text = f'{self.parent.pagedata.id} {text}'
        test = self.appbase.title
        if test:
            self.appbase.set_windowtitle(f"{test} | {text}")
        else:
            self.appbase.set_windowtitle(text)
        self.appbase.set_statusmessage()
        if 1 < self.parent.current_tab < len(self.parent.pages) - 1:
            self.oldbuf = ''
            is_readonly = False
            if self.parent.pagedata is not None:
                self.oldbuf = self.get_pagetext()
                is_readonly = self.parent.pagedata.arch
            self.gui.set_textarea_contents(self.oldbuf)
            if not is_readonly:
                is_readonly = not self.appbase.is_user
            self.gui.set_text_readonly(is_readonly)
            self.gui.enable_toolbar(self.appbase.is_user)
            self.oldbuf = self.gui.get_textarea_contents()  # make sure it's rich text
            self.gui.move_cursor_to_end()
        self.initializing = False

    def get_pagetext(self):
        "read the textfield on the given page"
        text = ''
        if self.parent.current_tab == 2:
            text = self.parent.pagedata.melding
        elif self.parent.current_tab == 3:
            text = self.parent.pagedata.oorzaak
        elif self.parent.current_tab == 4:
            text = self.parent.pagedata.oplossing
        else:  # if self.parent.current_tab == 5: -- momenteel enig andere mogelijkhedi
            text = self.parent.pagedata.vervolg
        return text

    def readp(self, pid):
        "lezen van een actie"
        if self.parent.pagedata:  # spul van de vorige actie opruimen
            self.parent.pagedata.cleanup()
        self.parent.pagedata = shared.Actie[self.appbase.datatype](self.parent.fnaam, pid,
                                                                   self.appbase.user)
        self.appbase.imagelist = self.parent.pagedata.imagelist
        self.parent.old_id = self.parent.pagedata.id
        self.parent.newitem = False

    def nieuwp(self, *args):
        """voorbereiden opvoeren nieuwe actie"""
        shared.log('opvoeren nieuwe actie')
        self.parent.newitem = True
        if self.leavep():
            if self.parent.current_tab == 0:
                self.appbase.gui.enable_book_tabs(True, tabfrom=1)
            self.parent.pagedata = shared.Actie[self.appbase.datatype](self.parent.fnaam, 0,
                                                                       self.appbase.user)
            self.parent.pagedata.add_event('Actie opgevoerd')
            self.appbase.imagelist = self.parent.pagedata.imagelist
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
        # newbuf = []                     # wordt nu via on_text methode bijgouden in changed_item?
        # if self.parent.current_tab > 0:
        #     newbuf = self.oldbuf
        #     newbuf = self.gui.build_newbuf()
        ok_to_leave = True
        if self.parent.current_tab == 0:
            if self.appbase.exiting:
                pass
            # overgenomen uit wx versie on_page_changing
            elif self.parent.fnaam == "":
                wat = ''
                if self.appbase.multiple_files:  # datatype == shared.DataType.XML.name:
                    wat = 'bestand'
                elif self.appbase.multiple_projects:  # datatype == shared.DataType.SQL.name:
                    wat = 'project'
                else:
                    raise ValueError('ProgrammingError: fnaam should only be empty'
                                     ' with multiple files or projects')
                msg = f"Kies eerst een {wat} om mee te werken"
                ok_to_leave = False
            elif not self.parent.data and not self.parent.newitem:
                # bestand bevat nog geen gegevens en we zijn nog niet bezig met de eerste opvoeren
                msg = "Voer eerst één of meer acties op"
                ok_to_leave = False
            elif self.parent.current_item == -1 and not self.parent.newitem:
                # geen actie geselecteerd en we zijn niet bezig met een nieuwe
                msg = "Selecteer eerst een actie"
                ok_to_leave = False
            # mag_weg = self.parent.book.pages[self.parent.book.current_tab].leavep()
            if not ok_to_leave:
                gui.show_message(self.parent, msg, "Navigatie niet toegestaan")
        elif self.parent.changed_item:
            message = ("De gegevens op de pagina zijn gewijzigd,\n"
                       "wilt u de wijzigingen opslaan voordat u verder gaat?")
            ok, cancel = gui.ask_cancel_question(self.gui, message)
            if ok:
                ok_to_leave = self.savep()
            elif cancel:
                # self.parent.checked_for_leaving = ok_to_leave = False
                ok_to_leave = False
            if not cancel:
                self.appbase.gui.enable_all_other_tabs(True)
        return ok_to_leave

    def savep(self, *args):
        "gegevens van een actie opslaan afhankelijk van pagina"
        if not self.gui.can_save:
            return False
        self.enable_buttons(False)
        if self.parent.current_tab <= 1 or self.parent.current_tab == 6:
            return False
        if self.parent.current_tab == 2 and not self.appbase.use_text_panels:
            return False
        text = self.gui.get_textarea_contents()
        event_text = ''
        if self.parent.current_tab == 2 and text != self.parent.pagedata.melding:
            self.oldbuf = self.parent.pagedata.melding = text
            event_text = "Meldingtekst aangepast"
        if self.parent.current_tab == 3 and text != self.parent.pagedata.oorzaak:
            self.oldbuf = self.parent.pagedata.oorzaak = text
            event_text = "Beschrijving oorzaak aangepast"
        if self.parent.current_tab == 4 and text != self.parent.pagedata.oplossing:
            self.oldbuf = self.parent.pagedata.oplossing = text
            event_text = "Beschrijving oplossing aangepast"
        if self.parent.current_tab == 5 and text != self.parent.pagedata.vervolg:
            self.oldbuf = self.parent.pagedata.vervolg = text
            event_text = "Tekst vervolgactie aangepast"
        if event_text:
            self.parent.pagedata.add_event(event_text)
            self.update_actie()
            # onderstaande verplaatst naar update_actie
            # self.parent.pages[0].gui.set_item_text(self.parent.pages[0].gui.get_selection(), 3,
            #                                        self.parent.pagedata.updated)
        return True

    def savepgo(self, *args):
        "opslaan en naar de volgende pagina"
        if not self.gui.can_saveandgo():
            return
        if self.savep():
            self.goto_next()
        else:
            self.enable_buttons()

    def restorep(self, *args):
        "oorspronkelijke (laatst opgeslagen) inhoud van de pagina herstellen"
        # reset font - are these also needed: case? indent? linespacing? paragraphspacing?
        if self.parent.current_tab > 1 and self.appbase.use_rt:
            self.gui.reset_font()
        if self.parent.current_tab == len(self.parent.pages) - 1 and self.status_auto_changed:
            self.parent.pagedata.status = '0'
        self.vulp()

    def on_text(self, *args):
        """callback voor EVT_TEXT e.d.

        de initializing flag wordt uitgevraagd omdat deze event ook tijdens vulp()
        en tijdens vul_combos plaatsvindt"""
        if not self.initializing:
            newbuf = self.gui.build_newbuf()
            changed = newbuf != self.oldbuf
            self.enable_buttons(changed)

    # def on_choice(self):
    #     "callback voor combobox (? wordt on_text hier niet gewoon voor gebruikt?)"
    #     self.enable_buttons()

    def update_actie(self):
        """pass page data from the GUI to the internal storage
        """
        self.parent.pagedata.imagecount = self.appbase.imagecount
        self.parent.pagedata.imagelist = self.appbase.imagelist
        # aangenomen dat "gemeld" altijd "0" zal blijven en de eerstvolgende status "1"
        # if self.parent.current_tab >= 3 and self.parent.pagedata.status == '0':
        if (self.parent.pagedata.status == '0' and self.appbase.use_text_panels
                and self.parent.current_tab >= 3):
            self.parent.pagedata.status = '1'
            sel = [y for x, y in self.parent.stats.items() if y[1] == '1'][0]
            self.parent.pagedata.add_event(f'Status gewijzigd in "{sel[0]}"')

        if self.appbase.work_with_user:
            self.parent.pagedata.write(self.appbase.user)
        else:
            self.parent.pagedata.write()

        self.parent.pagedata.read()
        if self.parent.newitem:
            # nieuwe entry maken in de tabel voor panel 0
            # jamaar hier zit toch ook een verschil voor de verschillende datatypes?
            newindex = len(self.parent.data)  # + 1
            pagegui = self.parent.pages[1].gui
            itemdata = (pagegui.get_text('date'),
                        " - ".join((pagegui.get_text('proc'),
                                    pagegui.get_text('desc'))),
                        pagegui.get_choice_data(self.gui.stat_choice)[0],
                        pagegui.get_choice_data(self.gui.cat_choice)[0],
                        pagegui.get_text('id'))
            self.parent.data[newindex] = itemdata
            # ook nieuwe entry maken in de visuele tree
            page = self.parent.pages[0]
            self.parent.current_item = page.gui.add_listitem(itemdata[0].split(' ')[0])
            page.gui.set_selection()
            self.parent.newitem = False
            self.parent.rereadlist = True
        else:
            # actiegegevens bijwerken op panel 0
            pagegui = self.parent.pages[0].gui
            item = pagegui.get_selection()
            pagegui.set_item_text(item, 1, self.parent.pagedata.get_soorttext()[0].upper())
            pagegui.set_item_text(item, 2, self.parent.pagedata.get_statustext())
            pagegui.set_item_text(item, 3, self.parent.pagedata.updated)
            if self.appbase.use_separate_subject:
                pagegui.set_item_text(item, 4, self.parent.pagedata.over)
                pagegui.set_item_text(item, 5, self.parent.pagedata.titel)
            else:
                pagegui.set_item_text(item, 4, self.parent.pagedata.titel)

    def enable_buttons(self, state=True):
        "buttons wel of niet bruikbaar maken"
        self.gui.enable_buttons(state)
        self.parent.changed_item = state
        if self.parent.current_tab > 0:
            self.appbase.gui.enable_all_other_tabs(not state)

    def goto_actie(self, *args):
        "naar startpagina actie gaan"
        self.goto_page(1)

    def goto_next(self, *args):
        "naar de volgende pagina gaan"
        if self.leavep():
            next = self.parent.current_tab + 1
            if next >= len(self.parent.pages):
                next = 0
            self.appbase.gui.set_page(next)

    def goto_prev(self, *args):
        "naar de vorige pagina gaan"
        if self.leavep():
            next = self.parent.current_tab - 1
            if next < 0:
                next = len(self.parent.pages) - 1
            self.appbase.gui.set_page(next)

    def goto_page(self, page_num, check=True):
        "naar de aangegeven pagina gaan"
        if (not check or self.leavep()) and 0 <= page_num < len(self.parent.pages):
            self.appbase.gui.set_page(page_num)

    def get_textarea_contents(self):
        "get the page text"
        return self.gui.get_textarea_contents()


class Page0(Page):
    "pagina 0: overzicht acties"
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, pageno=0, standard=False)
        self.selection = 'excl. gearchiveerde'
        self.sel_args = {}
        self.sorted = (0, "A")

        # widths = [94, 24, 146, 90, 400] if LIN else [64, 24, 114, 72, 292]
        widths = [122, 24, 146, 100, 300] if LIN else [64, 24, 114, 72, 292]
        if self.appbase.use_separate_subject:
            # widths[4] = 90 if LIN else 72
            # extra = 310 if LIN else 220
            # widths.append(extra)
            # widths[4:] = [90, 310] if LIN else [72, 220]
            widths.append(90 if LIN else 72)

        self.gui = gui.Page0Gui(parent, self, widths)
        self.gui.enable_buttons()

        self.sort_via_options = False
        self.saved_sortopts = None
        # dit werkt hier alleen als ik met een user heb kunnen aanloggen vóór start van de GUI
        # if self.appbase.work_with_user and self.appbase.is_user:
        #     self.saved_sortopts = dmls.SortOptions(self.appbase.filename)

    def vulp(self):
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina
        """
        self.selection = ''
        if self.appbase.work_with_user:
            if self.saved_sortopts:
                # laden hier doen garandeert wijzigen van opties bij wijzigen project
                self.saved_sortopts.load_options()
                self.sort_via_options = True
        self.gui.enable_sorting(not self.sort_via_options)
        if self.sort_via_options:
            self.selection = 'volgens user gedefinieerde selectie'

        self.seltitel = 'alle meldingen ' + self.selection
        super().vulp()
        msg = ''
        if self.parent.rereadlist:
            msg = self.populate_list()
            self.parent.rereadlist = False
            # nodig voor sorteren?  Geen idee maar als het ergens goed voor is dan moet dit
            # naar de gui module want sortItems is een qt methode
            # if self.appbase.datatype == shared.DataType.XML:
            #     self.gui.p0list.sortItems(self.sorted[0], sortorder[self.sorted[1]])  # , True)
            #
            if self.appbase.startitem:
                self.parent.current_item = self.gui.get_item_by_id(self.appbase.startitem)
            else:
                self.parent.current_item = self.gui.get_first_item()
        self.appbase.enable_all_book_tabs(False)
        self.gui.enable_buttons()
        if self.gui.has_selection():
            self.appbase.enable_all_book_tabs(True)
            self.gui.set_selection()
            self.gui.ensure_visible(self.parent.current_item)
        self.appbase.set_statusmessage(msg)

    def populate_list(self):
        "list control vullen"
        self.parent.data = {}
        self.gui.clear_list()

        select = self.sel_args.copy()
        arch = select.pop("arch") if ("arch" in select) else ""  # "alles"
        data = shared.get_acties[self.appbase.datatype](self.parent.fnaam, select,
                                                        arch, self.appbase.user)
        for idx, item in enumerate(data):
            if len(item) == 7:  # type == self.appbase.shared.DataType.XML:
                self.parent.data[idx] = (item[0],
                                         item[1],
                                         ".".join((item[3][1], item[3][0])),
                                         ".".join((item[2][1], item[2][0])),
                                         item[5],
                                         item[4],
                                         item[6] == 'arch')
            elif len(item) == 8:  # type == self.appbase.shared.DataType.MNG:
                cats = {y: x for x, y in self.parent.cats.values()}
                stats = {y: x for x, y in self.parent.stats.values()}
                self.parent.data[idx] = (item[0],
                                         item[1],
                                         '.'.join((item[2], cats[item[2]])),
                                         '.'.join((item[3], stats[item[3]])),
                                         item[4],
                                         item[5],
                                         item[6],
                                         item[7])
            elif len(item) == 10:  # type == self.appbase.shared.DataType.SQL:
                self.parent.data[idx] = (item[0],
                                         item[1],
                                         ".".join((item[5], item[4])),
                                         ".".join((str(item[3]), item[2])),
                                         item[8],
                                         item[6],
                                         item[7],
                                         item[9])
            else:
                raise ValueError('ProgrammingError: Unexpected length of pagedata item')
        # items = self.parent.data.items()
        # if items is None:
        #     self.appbase.set_statusmessage('Selection is None?')
        # for _, data in items:
        for data in self.parent.data.values():
            new_item = self.gui.add_listitem(data[0])
            self.gui.set_listitem_values(new_item, [data[0]] + list(data[2:]))
        return f'{len(data)} items found'

    def change_selected(self, item_n):
        """callback voor wijzigen geselecteerd item, o.a. door verplaatsen van de
        cursor of door klikken
        """
        self.parent.current_item = item_n
        self.gui.set_selection()
        if not self.parent.newitem:
            selindx = self.gui.get_selected_action()
            self.readp(selindx)
        hlp = "&Herleef" if self.parent.pagedata.arch else "&Archiveer"
        self.gui.set_archive_button_text(hlp)

    def activate_item(self):
        """callback voor activeren van item, door doubleclick of enter
        """
        self.goto_actie()

    def select_items(self, event=None):
        """tonen van de selectie dialoog

        niet alleen selecteren op tekst(deel) maar ook op status, soort etc
        """
        args = self.sel_args, None
        if self.appbase.work_with_user:
            data = dmls.SelectOptions(self.parent.fnaam, self.appbase.user)
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
                        else:
                            raise('ProgrammingError: illegal value in select arguments')
                elif value:
                    sel_args[key] = value
                else:
                    raise('ProgrammingError: illegal value in select arguments')
            args = sel_args, data
        while True:
            test = gui.show_dialog(self.gui, gui.SelectOptionsDialog, args)
            if not test:
                break
            self.parent.rereadlist = True
            try:
                self.vulp()
            except shared.DataError[self.appbase.datatype] as msg:
                self.parent.rereadlist = False
                gui.show_message(self, str(msg))
            else:
                break

    def sort_items(self, *args):
        """tonen van de sorteer-opties dialoog

        sortering mogelijk op datum/tijd, soort, titel, status via schermpje met
        2x4 comboboxjes waarin je de volgorde van de rubrieken en de sorteervolgorde
        per rubriek kunt aangeven"""
        sortopts, sortlist = {}, []
        if self.saved_sortopts:
            sortopts = self.saved_sortopts.load_options()
            # try:
            sortlist = [x[0] for x in dmls.my.SORTFIELDS]
            # except AttributeError:
            #     pass
        else:
            gui.show_message(self.gui, 'Sorry, multi-column sorteren werkt nog niet')
            return
        if not sortlist:  # kan dit? Nu dat deze in dmls geïmporteerd wordt niet meer denk ik
                          # als de niet-django variant mogelijk wordt kan het wel
            sortlist = list(self.parent.ctitels)  # [x for x in self.parent.ctitels]
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
            # moet hier soms nog het daadwerkelijke sorteren tussen (bij XML)?
            except shared.DataError[self.appbase.datatype] as msg:
                self.parent.rereadlist = False
                gui.show_message(self, str(msg))
        else:
            self.gui.enable_sorting(True)

    def archiveer(self, *args):
        "archiveren of herleven van het geselecteerde item"
        self.readp(self.gui.get_selected_action())
        self.parent.pagedata.arch = not self.parent.pagedata.arch
        hlp = "gearchiveerd" if self.parent.pagedata.arch else "herleefd"
        self.parent.pagedata.add_event(f"Actie {hlp}")
        self.update_actie()  # self.parent.pagedata.write()
        self.parent.rereadlist = True  # wordt uitgezet in vulp
        self.vulp()
        self.appbase.gui.set_tabfocus(0)
        if self.sel_args.get("arch", "") == "alles":
            self.gui.ensure_visible(self.parent.current_item)
            hlp = "&Herleef" if self.parent.pagedata.arch else "&Archiveer"
            self.gui.set_archive_button_text(hlp)

    def enable_buttons(self, value=None):
        "buttons wel of niet bruikbaar maken"
        if value is not None:
            self.gui.enable_buttons(value)
        else:
            self.gui.enable_buttons()

    def get_items(self):
        "retrieve all listitems"
        return self.gui.get_items()

    # onduidelijk waarom deze in Page0 wel en in Page, Page1 en Page6 niet geredirect is
    # terwijl het alleen maar een doorgeefluik is (alleen gebruikt in MainWindow.print_scherm op p0?)
    def get_item_text(self, itemindicator, column):
        "get the item's text for a specified column"
        return self.gui.get_item_text(itemindicator, column)

    def clear_selection(self):
        "initialize selection criteria"
        self.sel_args = {}


class Page1(Page):
    "pagina 1: startscherm actie"
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, pageno=1, standard=False)
        self.gui = gui.Page1Gui(parent, self)

    def vulp(self):
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina"""
        super().vulp()
        self.initializing = True
        self.gui.init_fields()
        self.parch = False
        # if self.parent.pagedata is not None:  # is altijd een Actie object
        self.gui.set_text('id', str(self.parent.pagedata.id))
        self.gui.set_text('date', self.parent.pagedata.datum)
        if not self.parent.newitem:
            self.parch = self.parent.pagedata.arch
            if self.appbase.use_separate_subject:
                self.gui.set_text('proc', self.parent.pagedata.over)
                self.gui.set_text('desc', self.parent.pagedata.titel)
            elif self.parent.pagedata.titel:
                if " - " in self.parent.pagedata.titel:
                    hlp = self.parent.pagedata.titel.split(" - ", 1)
                else:
                    hlp = self.parent.pagedata.titel.split(": ", 1)
                self.gui.set_text('proc', hlp[0])
                if len(hlp) > 1:
                    self.gui.set_text('desc', hlp[1])
                else:
                    raise ValueError('ProgrammmingError: subject should be splittable')
            else:
                raise ValueError('ProgrammmingError: subject should not be empty')
            self.gui.set_choice(self.parent.stats, self.gui.stat_choice, self.parent.pagedata.status)
            self.gui.set_choice(self.parent.cats, self.gui.cat_choice, self.parent.pagedata.soort)
            if not self.appbase.use_text_panels:
                self.gui.set_text('summary', self.parent.pagedata.melding)

        self.oldbuf = self.gui.set_oldbuf()
        if self.parch:
            aanuit = False
            # staat hierboven ook al - is dat hier dan nog een keer nodig?
            # if self.appbase.datatype == shared.DataType.XML:
            #     if self.parent.pagedata.titel is not None:
            #         if " - " in self.parent.pagedata.titel:
            #             hlp = self.parent.pagedata.titel.split(" - ", 1)
            #         else:
            #             hlp = self.parent.pagedata.titel.split(": ", 1)
            #         self.gui.set_text('proc', hlp[0])
            #         if len(hlp) > 1:
            #             self.gui.set_text('desc', hlp[1])
            # elif self.appbase.datatype == shared.DataType.SQL:
            #     self.gui.set_text('proc', self.parent.pagedata.over)
            #     self.gui.set_text('desc', self.parent.pagedata.titel)
            self.gui.set_text('arch', "Deze actie is gearchiveerd")
            self.gui.set_archive_button_text("Herleven")
        else:
            aanuit = True
            self.gui.set_text('arch', '')
            self.gui.set_archive_button_text("Archiveren")

        if not self.appbase.is_user:
            aanuit = False
        self.gui.enable_fields(aanuit)

        self.initializing = False

    def savep(self, *args):
        "opslaan van de paginagegevens"
        super().savep()
        proc = self.gui.get_text('proc')
        self.gui.set_text('proc', proc.capitalize())
        self.enable_buttons(False)
        desc = self.gui.get_text('desc')
        if proc == "" or desc == "":
            gui.show_message(self.gui, "Beide tekstrubrieken moeten worden ingevuld")
            return False
        wijzig = False
        procdesc = f"{proc} - {desc}"
        # if procdesc != self.parent.pagedata.titel:
        #     if self.appbase.use_separate_subject:
        #         self.parent.pagedata.over = proc
        #         self.parent.pagedata.add_event(f'Onderwerp gewijzigd in "{proc}"')
        #         self.parent.pagedata.titel = procdesc = desc
        #     else:
        #         self.parent.pagedata.titel = procdesc
        #     self.parent.pagedata.add_event(f'Titel gewijzigd in "{procdesc}"')
        #     wijzig = True
        if procdesc != self.parent.pagedata.titel and not self.appbase.use_separate_subject:
            self.parent.pagedata.titel = procdesc
            self.parent.pagedata.add_event(f'Titel gewijzigd in "{procdesc}"')
            wijzig = True
        elif self.appbase.use_separate_subject:
            if proc != self.parent.pagedata.over:
                self.parent.pagedata.over = proc
                self.parent.pagedata.add_event(f'Onderwerp gewijzigd in "{proc}"')
                wijzig = True
            if desc != self.parent.pagedata.titel:
                self.parent.pagedata.titel = desc
                self.parent.pagedata.add_event(f'Titel gewijzigd in "{desc}"')
                wijzig = True
        newstat, sel = self.gui.get_choice_data(self.gui.stat_choice)
        verb = ''
        if self.parent.newitem:
            verb = 'is'
        elif newstat != self.parent.pagedata.status:
            verb = 'gewijzigd in'
        if verb:
            self.parent.pagedata.status = newstat
            self.parent.pagedata.add_event(f'Status {verb} "{sel}"')
            wijzig = True
        newcat, sel = self.gui.get_choice_data(self.gui.cat_choice)
        verb = ''
        if self.parent.newitem:
            verb = 'is'
        elif newcat != self.parent.pagedata.soort:
            verb = 'gewijzigd in'
        if verb:
            self.parent.pagedata.soort = newcat
            self.parent.pagedata.add_event(f'Categorie {verb} "{sel}"')
            wijzig = True
        if self.parch != self.parent.pagedata.arch:
            self.parent.pagedata.arch = self.parch
            hlp = "gearchiveerd" if self.parch else "herleefd"
            self.parent.pagedata.add_event(f"Actie {hlp}")
            wijzig = True
        if not self.appbase.use_text_panels:
            new_summary = self.gui.get_text('summary')
            # of text = self.gui.get_textarea_contents()
            if new_summary != self.parent.pagedata.melding:
                self.parent.pagedata.melding = new_summary
                self.parent.pagedata.add_event("Meldingtekst aangepast")
                wijzig = True
        if wijzig:
            self.update_actie()
            self.oldbuf = self.gui.set_oldbuf()
        return True

    def archiveer(self, *args):
        "archiveren/herleven"
        self.parch = not self.parch
        self.savep()
        self.parent.rereadlist = True  # wordt in vulp uitgezet
        self.vulp()

    def vul_combos(self):
        "vullen comboboxen"
        self.initializing = True
        self.gui.clear_stats()
        self.gui.clear_cats()
        for key in sorted(self.parent.stats.keys()):
            text, value = self.parent.stats[key][:2]
            self.gui.add_stat_choice(text, value)
        for key in sorted(self.parent.cats.keys()):
            text, value = self.parent.cats[key][:2]
            self.gui.add_cat_choice(text, value)
        self.initializing = False

    def get_field_text(self, entry_type):
        "return a screen field's text"
        return self.gui.get_field_text(entry_type)


class Page6(Page):
    "pagina 6: voortgang"
    def __init__(self, parent):
        super().__init__(parent, pageno=6, standard=False)
        self.current_item = 0
        self.oldtext = ""
        self.event_list, self.event_data, self.old_list, self.old_data = [], [], [], []
        self.gui = gui.Page6Gui(parent, self)
        self.status_auto_changed = False   # t.b.v. ongedaan maken automatische statuswijziging 0->1

    def vulp(self):
        """te tonen gegevens invullen in velden e.a. initialisaties

        methode aan te roepen voorafgaand aan het tonen van de pagina"""
        super().vulp()
        self.initializing = True
        self.gui.init_textfield()

        if not self.parent.pagedata:
            raise ValueError('ProgrammingError: page data should not be empty')
        else:
            self.event_list = [dbdate2listdate(x[0]) for x in self.parent.pagedata.events]
            self.event_list.reverse()
            self.old_list = self.event_list[:]
            self.event_data = [x[1] for x in self.parent.pagedata.events]
            self.event_data.reverse()
            self.old_data = self.event_data[:]
            if self.appbase.is_user:
                text = '-- doubleclick or press Shift-Ctrl-N to add new item --'
            else:
                text = '-- adding new items is disabled --'
            self.gui.init_list(text)
            for idx, datum in enumerate(self.event_list):
                self.gui.add_item_to_list(idx, datum)
        if self.appbase.work_with_user:
            self.gui.set_list_callback()
        self.gui.clear_textfield()
        self.oldbuf = (self.old_list, self.old_data)
        self.oldtext = ''
        self.initializing = False

    def savep(self, *args):
        "opslaan van de paginagegevens"
        super().savep()
        # voor het geval er na het aanpassen van een tekst direkt "sla op" gekozen is
        # nog even kijken of de tekst al in self.event_data is aangepast.
        idx = self.current_item
        hlp = self.gui.get_textfield_contents()
        if idx > 0:
            idx -= 1
        if self.event_data[idx] != hlp:
            self.event_data[idx] = hlp
            self.oldtext = hlp
            short_text = hlp.split("\n", 1)[0]
            maxlen = 80
            if len(short_text) > maxlen:
                short_text = short_text[:maxlen] + "..."
            self.gui.set_listitem_text(idx + 1, f"{self.event_list[idx]} - {short_text}")
            self.gui.set_listitem_data(idx + 1)
        wijzig = False
        if self.event_list != self.old_list or self.event_data != self.old_data:
            wijzig = True
            hlp = len(self.event_list) - 1
            for idx, data in enumerate(self.parent.pagedata.events):
                datestring = listdate2dbdate(self.event_list[hlp - idx])
                if data != (datestring, self.event_data[hlp - idx]):
                    self.parent.pagedata.events[idx] = (datestring, self.event_data[hlp - idx])
            for idx in range(len(self.parent.pagedata.events), hlp + 1):
                if self.event_data[hlp - idx]:
                    self.parent.pagedata.events.append((listdate2dbdate(self.event_list[hlp - idx]),
                                                        self.event_data[hlp - idx]))
        if wijzig:
            self.update_actie()
            # waar is deze voor (self.book.current_item.setText) ?
            # self.parent.current_item = self.parent.page0.p0list.topLevelItem(x)
            # self.parent.current_item.setText(4, self.parent.pagedata.updated)
            self.parent.pages[0].gui.set_item_text(self.parent.current_item, 3,
                                                   self.parent.pagedata.updated)
            # dit was self.parent.page0.p0list.currentItem().setText( -- is dat niet hetzelfde?
            self.old_list = self.event_list[:]
            self.old_data = self.event_data[:]
            self.oldbuf = (self.old_list, self.old_data)
        return True

    def goto_prev(self, *args):
        "set the selection to the previous row, if possible"
        test = self.gui.get_list_row() - 1
        if test > 0:
            self.gui.set_list_row(test)

    def goto_next(self, *args):
        "set the selection to the next row, if possible"
        test = self.gui.get_list_row() + 1
        if test < self.gui.get_list_rowcount():
            self.gui.set_list_row(test)

    def on_text(self, *args):
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
            if self.appbase.is_user:
                self.enable_buttons()
            self.current_item = self.gui.get_list_row()
            if self.current_item > 0:
                indx = self.current_item - 1
                self.event_data[indx] = tekst
                # item = self.progress_list.currentItem()
                # datum = str(item.text()).split(' - ')[0]
                datum = self.gui.get_listitem_text(self.current_item).split(' - ')[0]
                short_text = ' - '.join((datum, tekst_plat.split("\n")[0]))
                maxlen = 80
                if len(short_text) >= maxlen:
                    short_text = short_text[:maxlen] + "..."
                # item.setText(short_text)
                self.gui.set_listitem_text(self.current_item, short_text)

    def initialize_new_event(self):
        "set up entering new event in GUI"
        if not self.appbase.is_user:
            return
        if (self.parent.pagedata.status == '0' and (
                (self.appbase.use_text_panels and self.parent.current_tab >= 3)
                or (not self.appbase.use_text_panels and self.parent.current_tab == 2))):
            self.parent.pagedata.status = '1'
            self.status_auto_changed = True
            sel = [y for x, y in self.parent.stats.items() if y[1] == '1'][0]
            datum, oldtext = shared.get_dts(), f'Status gewijzigd in "{sel[0]}"'
            self.gui.add_new_item_to_list(datum, oldtext)
            self.event_list.insert(0, datum)
            self.event_data.insert(0, oldtext)
        datum, oldtext = shared.get_dts(), ''
        self.event_list.insert(0, datum)
        self.event_data.insert(0, oldtext)
        self.gui.add_new_item_to_list(datum, oldtext)
        self.oldtext = oldtext
        self.gui.enable_buttons()


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
        statitems = []
        for row_id in parent.master.book.stats:
            item_text, item_value = parent.master.book.stats[row_id]
            statitems.append((row_id, item_value, item_text))
        self.data = [': '.join((str(y), z)) for x, y, z in sorted(statitems)]
        self.tekst = ["De waarden voor de status worden getoond in dezelfde volgorde",
                      "als waarin ze in de combobox staan.",
                      "Vóór de dubbele punt staat de code, erachter de waarde.",
                      "Denk erom dat als je codes wijzigt of statussen verwijdert, deze",
                      "ook niet meer getoond en gebruikt kunnen worden in de registratie.",
                      "Omschrijvingen kun je rustig aanpassen"]
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
        catitems = []
        for row_id in parent.master.book.cats:
            item_text, item_value = parent.master.book.cats[row_id]
            catitems.append((row_id, item_value, item_text))
        self.data = [': '.join((str(y), z)) for x, y, z in sorted(catitems)]
        self.tekst = ["De waarden voor de soorten worden getoond in dezelfde volgorde",
                      "als waarin ze in de combobox staan.",
                      "Vóór de dubbele punt staat de code, erachter de waarde.",
                      "Denk erom dat als je codes wijzigt of soorten verwijdert, deze",
                      "ook niet meer getoond en gebruikt kunnen worden in de registratie.",
                      "Omschrijvingen kun je rustig aanpassen"]
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


class MainWindow:
    """Hoofdscherm met menu, statusbalk, notebook en een "quit" button"""
    def __init__(self, parent, fnaam=""):
        self.parent = parent
        self.dirname, self.filename = '', ''
        self.datatype = None
        self.title = 'Actieregistratie'
        self.initializing = True
        self.exiting = False
        self.helptext = ''
        self.is_newfile = False
        self.oldsort = -1
        self.idlist = self.actlist = self.alist = []
        self.projnames = {x[0].lower(): (x[0], x[1]) for x in dmls.get_projnames()}
        if fnaam:
            self.determine_datatype_from_filename(fnaam)
        self.gui = gui.MainGui(self)
        if not self.datatype:
            self.select_datatype()
        self.work_with_user = self.datatype == shared.DataType.SQL
        if self.work_with_user:
            if not self.projnames:
                raise SystemExit('No projects found; add one ior more in the webapp first')
            self.user = None                        # start without user
            self.is_user = self.is_admin = False
        else:
            self.user = 1                           # pretend user
            self.is_user = self.is_admin = True     # force editability
        self.multiple_files = self.datatype == shared.DataType.XML
        self.multiple_projects = self.datatype == shared.DataType.SQL
        self.use_text_panels = self.datatype != shared.DataType.MNG
        self.use_rt = self.datatype == shared.DataType.XML
        self.use_separate_subject = self.datatype in (shared.DataType.SQL, shared.DataType.MNG)
        self.create_book()
        self.gui.create_menu()
        self.enable_settingsmenu()
        self.gui.create_actions()
        self.create_book_pages()

        if self.datatype == shared.DataType.XML:
            if self.filename == "":
                self.open_xml()
            else:
                self.startfile()
        elif self.datatype == shared.DataType.SQL:
            self.open_sql(do_sel=not bool(self.filename))
        else:  # if self.datatype == shared.DataType.MNG:
            self.open_mongo()
        self.initializing = False

    def determine_datatype_from_filename(self, fnaam):
        "get datatype from input parameters"
        if fnaam == 'xml':
            self.datatype = shared.DataType.XML
        elif fnaam in ('sql', 'django'):
            self.datatype = shared.DataType.SQL
        elif fnaam in ('mongo', 'mongodb'):
            self.datatype = shared.DataType.MNG
        elif fnaam.lower() in self.projnames:
            self.datatype = shared.DataType.SQL
            self.filename = fnaam  # .lower()
        elif os.path.exists(fnaam) and os.path.isfile(fnaam):
            self.datatype = shared.DataType.XML
            test = pathlib.Path(fnaam)
            self.dirname, self.filename = test.parent, test.name

    def select_datatype(self):
        "get datatype from user if not determinable from filename"
        self.filename = ''
        choice = gui.get_choice_item(None, 'Select Mode', ['XML', 'SQL', 'MNG'])
        if choice == 'XML':
            self.datatype = shared.DataType.XML
        elif choice == 'SQL':
            self.datatype = shared.DataType.SQL
        elif choice == 'MNG':
            self.datatype = shared.DataType.MNG
        else:
            raise SystemExit('No datatype selected')

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
                ("&User", [("&Login", self.sign_in, 'Ctrl+L', " Sign in to the database")]),
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
                ("&View", []),
                ("&Help", (("&About", self.about_help, 'F1', " Information about this program"),
                           ("&Keys", self.hotkey_help, 'Ctrl+H', " List of shortcut keys")))]
        for tabnum, tabtitle in self.book.tabs.items():
            data[3][1].append((f'&{tabtitle}', functools.partial(self.gui.go_to, int(tabnum)),
                               f'Alt+{tabnum}', "switch to tab"))
        if not self.work_with_user:
            data.pop(1)     # remove login menu
        if self.multiple_projects:
            data[0][1][0] = ("&Other project", self.open_sql, 'Ctrl+O', " Select a project")
            data[0][1][1] = ("&New", self.new_project, 'Ctrl+N', " Create a new project")
        elif not self.multiple_files:
            data[0][1][:3] = []
            # data[0][1].pop(2)  # remove separator
            # data[0][1].pop(1)  # remove file - new
            # data[0][1].pop(0)  # remove file - open
        return data

    def create_book(self):
        """define the tabbed interface and its subclasses
        """
        self.book = self.gui.get_bookwidget()
        self.book.parent = self
        self.book.fnaam = ""
        if self.filename and self.multiple_projects:  # datatype == shared.DataType.SQL:
            self.book.fnaam = self.filename
        self.book.current_item = None
        self.book.data = {}
        self.book.rereadlist = True
        self.lees_settings()
        self.book.ctitels = ["actie", " ", "status", "L.wijz."]
        if self.use_separate_subject:
            self.book.ctitels.extend(("betreft", "omschrijving"))
        else:
            self.book.ctitels.append("titel")
        self.book.current_tab = -1
        self.book.pages = []
        self.book.newitem = False
        self.book.changed_item = True
        self.book.pagedata = None

    def create_book_pages(self):
        "add the pages to the tabbed widget"
        self.book.pages.append(Page0(self.book))
        self.book.pages.append(Page1(self.book))
        if self.use_text_panels:
            self.book.pages.append(Page(self.book, 2))
            self.book.pages.append(Page(self.book, 3))
            self.book.pages.append(Page(self.book, 4))
            self.book.pages.append(Page(self.book, 5))
        self.book.pages.append(Page6(self.book))

        for i, page in enumerate(self.book.pages):
            self.gui.add_book_tab(page, "&" + self.book.tabs[i])
        self.enable_all_book_tabs(False)

    def not_implemented_message(self):
        "information"
        gui.show_message(self.gui, "Sorry, werkt nog niet")

    def new_file(self, event=None):
        "Menukeuze: nieuw file"
        self.is_newfile = False
        # self.dirname = str(self.dirname)  # defaults to '.' so no need for `or os.getcwd()`
        fname = gui.get_save_filename(self.gui, start=self.dirname)
        if fname:
            test = pathlib.Path(fname)
            if test.suffix != '.xml':
                gui.show_message(self.gui, 'Naam voor nieuw file moet wel extensie .xml hebben')
                return
            self.dirname, self.filename = test.parent, test.name
            self.is_newfile = True
            self.startfile()
            self.is_newfile = False
            self.enable_all_book_tabs(False)

    def open_xml(self, event=None):
        "Menukeuze: open file"
        self.dirname = self.dirname or os.getcwd()
        fname = gui.get_open_filename(self.gui, start=self.dirname)
        if fname:
            test = pathlib.Path(fname)
            self.dirname, self.filename = test.parent, test.name
            self.startfile()

    def new_project(self, event=None):
        "Menukeuze: nieuw project"
        gui.show_message(self.gui, "Voor deze functie moet u de ActieReg webapplicatie gebruiken")

    def open_sql(self, event=None, do_sel=True):
        "Menukeuze: open project"
        # shared.log('in open_sql: %s', self.filename)
        current = choice = 0
        data = [f'{x}: {y}' for x, y in self.projnames.values()]
        for i, x in enumerate(data):
            if x.lower().startswith(self.filename.lower()):
                current = i
                choice = self.filename
        if do_sel or not choice:
            choice = gui.get_choice_item(self.gui, 'Kies een project om te openen', data, current)
        if choice:
            self.filename = choice.split(': ')[0]
            self.startfile()

    def open_mongo(self, event=None):
        "open database for the MongoDB version"
        self.filename = 'default'
        self.startfile()

    def print_something(self, event=None):
        """callback voor ctrl-P(rint)

        vraag om printen scherm of actie, bv. met een InputDialog
        """
        choices = ['huidig scherm', 'huidige actie']
        choice = gui.get_choice_item(self.gui, 'Wat wil je afdrukken?', choices)
        if choice == choices[0]:
            self.print_scherm()
        else:  # if choice == choices[1]:  geen andere mogelijkheid
            self.print_actie()

    def print_scherm(self, event=None):
        "Menukeuze: print dit scherm"
        self.printdict = {'lijst': [], 'actie': [], 'sections': [], 'events': []}
        self.hdr = f"Actie: {self.book.pagedata.id} {self.book.pagedata.titel}"

        if self.book.current_tab == 0:
            self.hdr = "Overzicht acties uit " + self.filename
            lijst = []
            page = self.book.pages[0]
            for item in page.get_items():
                actie = page.get_item_text(item, 0)
                started = self.book.pagedata.datum
                soort = page.get_item_text(item, 1)
                for x in self.book.cats.values():
                    oms, code = x[0], x[1]
                    if code == soort:
                        soort = oms
                        break
                status = page.get_item_text(item, 2)
                l_wijz = page.get_item_text(item, 3)
                titel = page.get_item_text(item, 4)
                if self.use_separate_subject:
                    over = titel
                    titel = page.get_item_text(item, 5)
                    l_wijz = l_wijz[:19]
                    actie = actie + " - " + over
                    started = started[:19]
                if status != self.book.stats[0][0]:
                    if l_wijz:
                        l_wijz = f", laatst behandeld op {l_wijz}"
                    l_wijz = f"status: {status}{l_wijz}"
                else:
                    l_wijz = f"status: {status} op {started}"
                lijst.append((actie, titel, soort, started, l_wijz))
            self.printdict['lijst'] = lijst
        elif self.book.current_tab == 1:
            data = {x: self.book.pages[1].get_field_text(x) for x in ('actie', 'datum', 'oms',
                                                                      'tekst', 'soort', 'status')}
            self.hdr = f"Informatie over actie {data['actie']}: samenvatting"
            self.printdict.update(data)
        elif 2 <= self.book.current_tab <= 5:  # and self.parent.use_textpages
            title = self.book.tabs[self.book.current_tab].split(None, 1)[1]
            text = self.book.pages[self.book.current_tab].get_textarea_contents()
            self.printdict['sections'] = [(title, text)]
        else:  # if self.book.current_tab == 6: - geen andere mogelijkheid
            events = []
            for idx, data in enumerate(self.book.pages[6].event_list):
                # if self.datatype == shared.DataType.SQL:
                # if len(data) >= len('eejj-mm-dd hh:mm:ss'):
                #     data = data[:19]
                events.append((data, self.book.pages[6].event_data[idx]))
            self.printdict['events'] = events
        self.gui.preview()

    def print_actie(self, event=None):
        "Menukeuze: print deze actie"
        if self.book.pagedata is None:  # or self.book.newitem:
            gui.show_message(self.gui, "Wel eerst een actie kiezen om te printen")
            return
        self.hdr = f"Actie: {self.book.pagedata.id} {self.book.pagedata.titel}"
        tekst = self.book.pagedata.titel
        try:
            oms, tekst = tekst.split(" - ", 1)
        except ValueError:
            try:
                oms, tekst = tekst.split(": ", 1)
            except ValueError:
                oms = ''
        srt = "(onbekende soort)"
        # for srtoms, srtcode in self.book.cats.values()[:2]:
        for soort in self.book.cats.values():
            # if srtcode == self.book.pagedata.soort:
            if soort[1] == self.book.pagedata.soort:
                # srt = srtoms
                srt = soort[0]
                break
        stat = "(onbekende status)"
        # for statoms, statcode in self.book.stats.values():
        for stat in self.book.stats.values():
            # if statcode == self.book.pagedata.status:
            if stat[1] == self.book.pagedata.status:
                # stat = statoms
                stat = stat[0]
                break
        self.printdict = {'lijst': [],
                          'actie': self.book.pagedata.id,
                          'datum': self.book.pagedata.datum,
                          'oms': oms,
                          'tekst': tekst,
                          'soort': srt,
                          'status': stat}
        empty = "(nog niet beschreven)"
        if self.use_text_panels:
            sections = [[title.split(None, 1)[1], ''] for key, title in
                        sorted(self.book.tabs.items()) if 2 <= key < 6]
            sections[0][1] = self.book.pagedata.melding or empty
            sections[1][1] = self.book.pagedata.oorzaak or empty
            sections[2][1] = self.book.pagedata.oplossing or empty
            sections[3][1] = self.book.pagedata.vervolg or ''
            if not sections[3][1]:
                sections.pop()
            self.printdict['sections'] = sections
        else:
            self.printdict['sections'] = [['Probleem/wens', self.book.pagedata.melding]]
        self.printdict['events'] = list(self.book.pagedata.events)  # [(x, y) for x, y in self.book.pagedata.events] or []
        self.gui.preview()

    def exit_app(self, event=None):
        "Menukeuze: exit applicatie"
        self.exiting = True
        ok_to_leave = True
        if self.book.current_tab >= 0:
            ok_to_leave = self.book.pages[self.book.current_tab].leavep()
        if ok_to_leave:
            self.gui.exit()

    def sign_in(self, *args):
        """aanloggen in SQL/Django mode
        """
        logged_in = False
        while not logged_in:
            ok = gui.show_dialog(self.gui, gui.LoginBox)
            if not ok:
                break
            test = dmls.validate_user(*self.gui.dialog_data)
            if test[0]:
                text = 'Login accepted'
                logged_in = True
            else:
                text = 'Login failed'
            gui.show_message(self.gui, text)
        if logged_in:
            self.user, self.is_user, self.is_admin = test
            self.book.rereadlist = True
            self.enable_settingsmenu()
            if self.is_user or self.is_admin:
                self.book.pages[0].saved_sortopts = dmls.SortOptions(self.filename)
            else:
                self.book.pages[0].saved_sortopts = None
            self.gui.refresh_page()

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
        gui.show_message(self.gui, "GUI versie van mijn actiebox")

    def hotkey_help(self, event=None):
        "menukeuze: help - keys"
        if not self.helptext:
            lines = ["=== Albert's actiebox ===\n",
                     "Keyboard shortcuts:",
                     "    Alt left/right:                verder - terug",
                     "    Alt-0 t/m Alt-6:               naar betreffende pagina",
                     "    Alt-O op tab 1:                S_o_rteren",
                     "    Alt-I op tab 1:                F_i_lteren",
                     "    Alt-G of Enter op tab 1:       _G_a naar aangegeven actie",
                     "    Alt-N op elke tab:             _N_ieuwe actie opvoeren",
                     "    Ctrl-P:                        _p_rinten (scherm of actie)",
                     "    Shift-Ctrl-P:                  print scherm",
                     "    Alt-Ctrl-P:                    print actie",
                     "    Ctrl-Q:                        _q_uit actiebox",
                     "    Ctrl-H:                        _h_elp (dit scherm)",
                     "    Ctrl-S:                        gegevens in het scherm op_s_laan",
                     "    Ctrl-G:                        oplaan en _g_a door naar volgende tab",
                     "    Ctrl-Z in een tekstveld:       undo",
                     "    Shift-Ctrl-Z in een tekstveld: redo",
                     "    Alt-Ctrl-Z overal:             wijzigingen ongedaan maken",
                     "    Shift-Ctrl-N op laatste tab:   nieuwe regel opvoeren",
                     "    Ctrl-up/down op laatste tab:   omhoog/omlaag in list"]
            if self.multiple_files:
                lines.insert(8, "    Ctrl-O:                       _o_pen een (ander) actiebestand")
                lines.insert(8, "    Ctrl-N:                       maak een _n_ieuw actiebestand")
            elif self.multiple_projects:
                lines.insert(8, "    Ctrl-O:                       selecteer een (ander) pr_o_ject")
                lines.insert(8, "    Ctrl-N:                       start een _n_ieuw project")
            self.helptext = "\n".join(lines)
        gui.show_message(self.gui, self.helptext)

    def silly_menu(self, event=None):
        "Menukeuze: settings - het leven"
        gui.show_message(self.gui, "Yeah you wish...\nHet leven is niet in te stellen helaas")

    def startfile(self):
        "initialisatie t.b.v. openen bestand / project"
        if self.multiple_files:
            fullname = self.dirname / self.filename
            retval = dmlx.checkfile(fullname, self.is_newfile)
            if retval != '':
                gui.show_message(self.gui, retval)
                return retval
            self.book.fnaam = fullname
            self.title = str(fullname)  # self.filename
        elif self.multiple_projects:
            self.book.fnaam = self.filename
            if not self.projnames:
                raise ValueError('ProgrammingError: self.projnames should never be empty')
            self.title = self.filename
        else:
            self.book.fnaam = self.filename
            self.title = ''
        self.book.rereadlist = True
        self.book.sorter = None
        self.lees_settings()
        self.gui.set_tab_titles(self.book.tabs)
        self.book.pages[0].clear_selection()
        self.book.pages[1].vul_combos()
        if self.book.current_tab == -1:
            self.book.current_tab = 0
        if self.book.current_tab == 0:
            self.book.pages[0].vulp()
        else:
            self.gui.select_first_tab()
        self.book.changed_item = True
        return ''

    def lees_settings(self):
        """instellingen (tabnamen, actiesoorten en actiestatussen) inlezen"""
        # self.book.stats = {0: ('dummy,', 0, 0)}
        # self.book.cats = {0: ('dummy,', ' ', 0)}
        # self.book.tabs = {0: '0 start'}
        data = shared.Settings[self.datatype](self.book.fnaam)
        self.imagecount = data.imagecount
        self.startitem = data.startitem
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
            self.book.stats[int(item[1])] = db_stat_to_book_stat(item_value, item)
        for item_value, item in data.cat.items():
            self.book.cats[int(item[1])] = db_cat_to_book_cat(item_value, item)
        for tab_num, tab_item in data.kop.items():
            self.book.tabs[int(tab_num)] = db_head_to_book_head(tab_num, tab_item)

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
            for item_value, item in data.items():
                self.book.tabs[int(item_value)] = db_head_to_book_head(item_value, item)
                self.gui.set_page_title(int(item_value), item[0])
        elif srt == "stat":
            settings.stat = data
            result = settings.write()
            if result:
                gui.show_message(self.gui, f'Kan status {result[1]} niet verwijderen,'
                                 ' wordt nog gebruikt in één of meer acties')
                return
            self.book.stats = {}
            for item_value, item in data.items():
                self.book.stats[int(item[1])] = db_stat_to_book_stat(item_value, item)
        else:  # if srt == "cat":  iets anders niet mogelijk
            settings.cat = data
            result = settings.write()
            if result:
                gui.show_message(self.gui, f'Kan soort {result[1]} niet verwijderen,'
                                 ' wordt nog gebruikt in één of meer acties')
                return
            self.book.cats = {}
            for item_value, item in data.items():
                self.book.cats[int(item[1])] = db_cat_to_book_cat(item_value, item)
        self.book.pages[1].vul_combos()

    def save_startitem_on_exit(self):
        "bijwerken geselecteerde actie om te onthouden voor de volgende keer"
        data = shared.Settings[self.datatype](self.book.fnaam)
        if data.startitem and self.book.pagedata:
            data.startitem = self.book.pagedata.id
            data.write()

    def goto_next(self, *args):
        """redirect to the method of the current page
        """
        # Page.goto_next(self.book.pages[self.book.current_tab])
        self.book.pages[self.book.current_tab].goto_next()

    def goto_prev(self, *args):
        """redirect to the method of the current page
        """
        # Page.goto_prev(self.book.pages[self.book.current_tab])
        self.book.pages[self.book.current_tab].goto_prev()

    def goto_page(self, page):
        """redirect to the method of the current page
        """
        # Page.goto_page(self.book.pages[self.book.current_tab], page)
        self.book.pages[self.book.current_tab].goto_page(page)

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
                msg += f' - {len(self.book.data)} items'
        self.gui.set_statusmessage(msg)
        if self.work_with_user:
            msg = f'Aangemeld als {self.user.username}' if self.user else 'Niet aangemeld'
            self.gui.show_username(msg)

    def get_focus_widget_for_tab(self, tabno):
        "determine field to set focus on"
        return (self.book.pages[0].gui.p0list,
                self.book.pages[1].gui.proc_entry,
                self.book.pages[2].gui.text1,
                self.book.pages[3].gui.text1,
                self.book.pages[4].gui.text1,
                self.book.pages[5].gui.text1,
                self.book.pages[6].gui.progress_list)[tabno]

    def enable_all_book_tabs(self, state):
        "make all tabs (in)accessible"
        self.gui.enable_book_tabs(state, tabfrom=1)


def main(arg=None):
    "opstart routine"
    frame = MainWindow(None, arg)
    frame.gui.go()
