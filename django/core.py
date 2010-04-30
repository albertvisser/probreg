## from django.template import Context, loader
## from django.http import
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import django.contrib.auth.models as aut
import datetime as dt

UIT_DOCTOOL = "Actie opgevoerd vanuit Doctool"

def is_user(root,user):
    """geeft indicatie terug of de betreffende gebruiker acties mag wijzigen"""
    test = root + "_user"
    ## if root == "basic":
        ## test = '_' + test
    for grp in user.groups.all():
        if grp.name == test:
            return True
    return False

def is_admin(root,user):
    """geeft indicatie terug of de betreffende gebruiker acties en settings mag wijzigen"""
    test = root + "_admin"
    ## if root == "basic":
        ## test = '_' + test
    for grp in user.groups.all():
        if grp.name == test:
            return True
    return False

def store_event(my,msg,actie,user):
    my.Event.objects.create(actie=actie,starter=user,text=msg)

def store_gewijzigd(my,msg,txt,mld,actie,user):
    store_event(my,'{0} gewijzigd in "{1}"'.format(msg,txt),actie,user)
    mld.append(msg)
    return mld

def koppel(root,my,request):
    """doorkoppeling vanuit doctool:
    actie opvoeren en terugkeren"""
    data = request.POST
    vervolg = data.get("hFrom","")
    usernaam = data.get("hUser","")
    volgnr = 0
    aant = my.Actie.objects.count()
    nw_date = dt.datetime.now()
    if aant:
        last = my.Actie.objects.all()[aant - 1]
        jaar,volgnr = last.nummer.split("-")
        volgnr = int(volgnr) if int(jaar ) == nw_date.year else 0
    volgnr += 1
    actie = my.Actie()
    actie.nummer = "{0}-{1:04}".format(nw_date.year,volgnr)
    actie.start = nw_date
    actie.starter = aut.User.objects.get(pk=1)
    behandelaar = actie.starter
    if usernaam:
        try:
            behandelaar = aut.User.objects.get(username=usernaam)
        except ObjectDoesNotExist:
            pass
    actie.behandelaar = behandelaar
    actie.about = "testbevinding" if "bevinding" in vervolg else ""
    actie.title = data.get("hMeld","")
    if "userwijz" in vervolg:
        soort = "W"
    elif "userprob" in vervolg:
        soort = "P"
    else:
        soort = " "
    actie.soort = my.Soort.objects.get(value=soort)
    actie.status = my.Status.objects.get(value='0')
    actie.lasteditor = actie.behandelaar
    actie.melding = data.get("hOpm","")
    actie.save()
    store_event(my,"{0} {1}".format(UIT_DOCTOOL,vervolg.split('koppel')[0]),
        actie, actie.starter)
    store_event(my,'titel: "{0}"'.format(actie.title),actie,actie.starter)
    store_event(my,'categorie: "{0}"'.format(str(actie.soort)),actie,actie.starter)
    store_event(my,'status: "{0}"'.format(str(actie.status)),actie,actie.starter)

    if vervolg:
        ## return HttpResponse("""\
        ## vervolg: {0}<br/>
        ## adres: {1}""".format(vervolg,vervolg.format(actie.id,actie.nummer)))
        return HttpResponseRedirect(vervolg.format(actie.id,actie.nummer))
    else:
        meld = "Opgevoerd vanuit DocTool zonder terugkeeradres"
        return HttpResponseRedirect("/{0}/{1}/meld/?msg={2}".format(root,actie.id,msg))

def index(root,name,my,request):
    """
    samenstellen van de lijst met acties:
    - selecteer en sorteer de acties volgens de voor de user vastgelegde regels
      (het selecteren op actienummer en beschrijving is nog even niet actief)
    - de soort user wordt meegegeven aan het scherm om indien nodig diverse knoppen
        te verbergen
    """
    msg = request.GET.get("msg","")
    if not msg:
        if request.user.is_authenticated():
            msg = 'U bent ingelogd als <i>{0}</i>. '.format(request.user.username)
            msg += 'Klik <a href="/logout/'
            inuit = 'uit'
        else:
            msg = 'U bent niet ingelogd. Klik <a href="/accounts/login/'
            inuit = 'in'
        msg += '?next=/{0}/">hier</a> om {1} te loggen. '.format(root,inuit)
        if inuit == "uit":
            msg += "Klik op een actienummer om de details te bekijken."
    page_data = {
        "title" : "Actielijst",
        "name": name,
        "root": root,
        "pages": my.Page.objects.all().order_by('order'),
        "admin": is_admin(root,request.user),
        "msg": msg,
        }
    if is_user(root,request.user) or is_admin(root,request.user):
        page_data["readonly"] = False
    else:
        page_data["readonly"] = True
    page_data["readonly"] = True if not is_user(root,request.user) and not is_admin(root,request.user) else False
    data = my.Actie.objects.all()
    if data:
        seltest = my.Selection.objects.filter(user=request.user.id)

        filtered = seltest.filter(veldnm="nummer")
        if filtered:
            filter = ""
            for f in filtered:
                if f.extra == "EN":
                    filter += " & "
                elif f.extra == "OF":
                    filter += " | "
                filter += 'Q(nummer__{0}="{1}")'.format(f.operator.lower(),f.value)
            ## return HttpResponse(filter)
            exec('data = data.filter({0})'.format(filter))

        filtered = seltest.filter(veldnm="soort")
        sel = [my.Soort.objects.get(value=x.value).id for x in filtered]
        if sel:
            data = data.filter(soort__in=sel)
        filtered = seltest.filter(veldnm="status")
        sel = [my.Status.objects.get(value=int(x.value)).id for x in filtered]
        if sel:
            data = data.filter(status__in=sel)
        filtered = seltest.filter(veldnm="user")
        ## sel = [aut.User.objects.get(pk=int(x.value)).id for x in filtered]
        sel = [int(x.value) for x in filtered]
        if sel:
            data = data.filter(behandelaar__in=sel)

        filtered = seltest.filter(veldnm="about")
        filter = ''
        if filtered:
            filter = 'Q(about__icontains="{0}")'.format(filtered[0].value)
        filtered = seltest.filter(veldnm="title")
        if filtered:
            if filter:
                if filtered[0].extra == "EN":
                    filter += " & "
                elif filtered[0].extra == "OF":
                    filter += " | "
            filter += 'Q(title__icontains="{0}")'.format(filtered[0].value)
        if filter:
            ## return HttpResponse(filter)
            exec('data = data.filter({0})'.format(filter))

        filtered = seltest.filter(veldnm="arch")
        if not filtered:
            data = data.exclude(arch=True)
        elif len(filtered) == 1:
            data = data.filter(arch=True)

        sorters = my.SortOrder.objects.filter(user=request.user.id).order_by("volgnr")
        order = []
        for sorter in sorters:
            if sorter.veldnm == "title":
                if sorter.richting == "asc":
                    order.extend(("about","title"))
                else:
                    order.extend(("-about","-title"))
            elif sorter.veldnm == "behandelaar":
                ordr = sorter.veldnm + "__username"
                ordr = ordr if sorter.richting == "asc" else "-" + ordr
                order.append(ordr)
            else:
                ordr = sorter.veldnm if sorter.richting == "asc" else "-" + sorter.veldnm
                order.append(ordr)
        ## return HttpResponse(" ".join([x for x in order]))
        data = data.order_by(*order)
        page_data["order"] = order
        page_data["acties"] = data
        page_data["geen_items"] = "Geen acties die aan deze criteria voldoen"
    else:
        page_data["geen_items"] = "Nog geen acties opgevoerd voor dit project"
        if not [x.assigned for x in my.Worker.objects.all()]:
            page_data["readonly"] = True
            page_data["geen_items"] += "<br/><br/>" + " ".join(("\nLet op:",
                "aan dit project moeten eerst nog medewerkers",
                "en bevoegdheden voor die medewerkers worden toegevoegd"))
    page_data["geen_items"] = page_data["geen_items"].join(("<p>","</p>"))
    return render_to_response(root + '/index.html',page_data)

def settings(root,name,my,request):
    """settings scherm opbouwen"""
    if not is_admin(root,request.user):
        return HttpResponse("U bent niet geautoriseerd om instellingen te wijzigen"
        '<br>Klik <a href="/{0}/">hier</a> om door te gaan'.format(root))
    proj_users = my.Worker.objects.all().order_by('assigned__username')
    hlp = [x.assigned for x in proj_users]
    all_users = [x for x in aut.User.objects.all().order_by('username') if x not in hlp]
    page_data = {
        ## "title" : "Instellingen",
        "name": name,
        "root": root,
        "pages": my.Page.objects.all().order_by('order'),
        "soorten" : my.Soort.objects.all().order_by('order'),
        "stats": my.Status.objects.all().order_by('order'),
        "all_users": all_users,
        "proj_users": proj_users, # .order_by('username')
        }
    return render_to_response(root + '/settings.html',page_data)

def setusers(root,my,request):
    """users aan project koppelen"""
    if not is_admin(root,request.user):
        return HttpResponse("U bent niet geautoriseerd om instellingen te wijzigen"
        '<br>Klik <a href="/{0}/">hier</a> om door te gaan'.format(root))
    data = request.POST
    users = data.getlist("ProjUsers")
    users = [aut.User.objects.get(pk=x) for x in data.get("result").split("$#$")]
    ## return HttpResponse("hallo" + " ".join([str(x) for x in data]))
    current = my.Worker.objects.all()
    old_users = [x.assigned.id for x in current]
    for user in users:
        if user not in old_users:
            ok = my.Worker.objects.create(assigned=user)
    for user in old_users:
        if user not in users:
            ok = my.Worker.objects.get(assigned=user).delete()
    return HttpResponseRedirect("/{0}/settings/".format(root))

def settabs(root,my,request):
    """tab titels aanpassen en terug naar settings scherm"""
    if not is_admin(root,request.user):
        return HttpResponse("U bent niet geautoriseerd om instellingen te wijzigen"
        '<br>Klik <a href="/{0}/">hier</a> om door te gaan'.format(root))
    data = request.POST
    pages = my.Page.objects.all().order_by('order')
    for ix,item in enumerate(pages):
        field = "page" + str(ix + 1)
        if data[field] != item.title:
            item.title = data[field]
            item.save()
    return HttpResponseRedirect("/{0}/settings/".format(root))

def settypes(root,my,request):
    """soort-gegevens aanpassen en terug naar settings scherm"""
    if not is_admin(root,request.user):
        return HttpResponse("U bent niet geautoriseerd om instellingen te wijzigen"
        '<br>Klik <a href="/{0}/">hier</a> om door te gaan'.format(root))
    data = request.POST
    soorten = my.Soort.objects.all().order_by('order')
    for ix,item in enumerate(soorten):
        field_o = "order" + str(ix+1)
        field_t = "title" + str(ix+1)
        field_v = "value" + str(ix+1)
        if "del" + str(ix+1) in data:
            item.delete()
        else:
            changed = False
            if data[field_o] != item.order:
                item.order = data[field_o]
                changed = True
            if data[field_t] != item.title:
                item.title = data[field_t]
                changed = True
            if data[field_v] != item.value:
                item.value = data[field_v]
                changed = True
            if changed:
                item.save()
    if data["order0"]:
        new = my.Soort.objects.create(
            order = data["order0"],
            title = data["title0"],
            value = data["value0"],
            )
    return HttpResponseRedirect("/{0}/settings/".format(root))

def setstats(root,my,request):
    """status-gegevens aanpassen en terug naar settings scherm"""
    if not is_admin(root,request.user):
        return HttpResponse("U bent niet geautoriseerd om instellingen te wijzigen"
        '<br>Klik <a href="/{0}/">hier</a> om door te gaan'.format(root))
    data = request.POST
    stats = my.Status.objects.all().order_by('order')
    for ix,item in enumerate(stats):
        field_o = "order" + str(ix+1)
        field_t = "title" + str(ix+1)
        field_v = "value" + str(ix+1)
        if "del" + str(ix+1) in data:
            item.delete()
        else:
            changed = False
            if data[field_o] != item.order:
                item.order = data[field_o]
                changed = True
            if data[field_t] != item.title:
                item.title = data[field_t]
                changed = True
            if data[field_v] != item.value:
                item.value = data[field_v]
                changed = True
            if changed:
                item.save()
    if data["order0"]:
        new = my.Status.objects.create(
            order = data["order0"],
            title = data["title0"],
            value = data["value0"],
            )
    return HttpResponseRedirect("/{0}/settings/".format(root))

def select(root,name,my,request):
    """
    bouw het scherm op aan de hand van de huidige selectiegegevens bij de gebruiker
    """
    if request.user.is_authenticated():
        msg = 'U bent ingelogd als <i>{0}</i>. '.format(request.user.username)
        msg += 'Klik <a href="/logout/?next=/{0}/select/">hier</a> om uit te loggen.'.format(root)
    else:
        return HttpResponse('U moet ingelogd zijn om de selectie voor dit scherm ' +
            'te mogen wijzigen. <br/><br/>' +
            'Klik <a href="/accounts/login/?next=/{0}/select/">'.format(root) +
            'hier</a> om in te loggen, <a href="/{0}/">hier</a>'.format(root) +
            ' om terug te gaan.')
    page_data = {
        "name": name,
        "root": root,
        "msg": msg,
        "pages": my.Page.objects.all().order_by('order'),
        "soorten" : my.Soort.objects.all(),
        "stats": my.Status.objects.all(),
        "users": [x.assigned for x in my.Worker.objects.all()],
        "selected": {"nummer": [],
            "gewijzigd": [],
            "soort": [],
            "status": [],
            "user": [],
            "arch": 0,
            }
        }
    ## return HttpResponse("<br>".join([str(x) for x in my.Selection.objects.filter(user=1)]))
    ## testdata = ""
    for sel in my.Selection.objects.filter(user=request.user.id):
        ## testdata += str(sel) + ' '
        if sel.veldnm == "soort":
            page_data["selected"][sel.veldnm].append(sel.value)
        elif sel.veldnm in ("status", "user"):
            page_data["selected"][sel.veldnm].append(int(sel.value))
        elif sel.veldnm == "arch":
            page_data["selected"][sel.veldnm] += 1
        elif sel.veldnm == "nummer":
            page_data["selected"]["nummer"] = True
            if sel.extra.strip():
                page_data["selected"]["enof1"] = sel.extra.lower()
            page_data["selected"][sel.operator] = sel.value
        elif sel.veldnm in ("about", "title"):
            page_data["selected"]["zoek"] = True
            if sel.extra.strip():
                page_data["selected"]["enof2"] = sel.extra.lower()
            page_data["selected"][sel.veldnm] = sel.value
        else:
            return HttpResponse("Unknown search argument: " + self.veldnm)
        ## testdata += str(page_data["selected"][sel.veldnm]) + "<br/>"
    ## return HttpResponse(testdata) # "<br>".join([str(x) for x in page_data["selected"].items()]))
    return render_to_response(root + '/select.html',page_data)

def setsel(root,my,request):
    """
    verwerk de aanpassingen en koppel door naar tonen van de lijst met acties
    de huidige selectiegegevens voor de user worden verwijderd
    daarna worden nieuwe selectiegegevens bepaald en opgeslagen
    """
    data = request.POST
    selact = data.getlist("select") # aangekruiste selecties: "act" "srt" "stat" "txt" of "arch"
    txtgt = data.get("txtgt","")
    gt_lt = data.get("enof","")    # "en" of "of"
    txtlt = data.get("txtlt","")
    srtval = data.getlist("srtval") # aangekruiste soorten
    statval = data.getlist("statval") # aangekruiste statussen
    userval = data.getlist("userval") # geselcteerde medewerkers
    txtabout = data.get("txtabout","")
    gt_lt2 = data.get("enof2","")    # "en" of "of"
    txttitle = data.get("txttitle","")
    archall = data.get("archall","") # "arch" of "all"
    page_data = {}
    my.Selection.objects.filter(user=request.user.id).delete()
    extra = "  "
    if "act" in selact:
        if txtgt:
            ok = my.Selection.objects.create(user=request.user.id,
                veldnm="nummer", operator="GT", extra=extra, value=txtgt)
            extra = gt_lt.upper()
        if txtlt:
            ok = my.Selection.objects.create(user=request.user.id,
                veldnm="nummer", operator="LT", extra=extra, value=txtlt)
            extra = "  "
    if "srt" in selact:
        for srt in srtval:
            ok = my.Selection.objects.create(user=request.user.id,
                veldnm="soort", operator="EQ", extra=extra,value=srt)
            extra = "OR"
        extra = "  "
    if "stat" in selact:
        for stat in statval:
            ok = my.Selection.objects.create(user=request.user.id,
                veldnm="status", operator="EQ", extra=extra,value=stat)
            extra = "OR"
        extra = "  "
    if "user" in selact:
        for user in userval:
            ok = my.Selection.objects.create(user=request.user.id,
                veldnm="user", operator="EQ", extra=extra,value=user)
            extra = "OR"
        extra = "  "
    if "txt" in selact:
        if txtabout:
            ok = my.Selection.objects.create(user=request.user.id,
                veldnm="about", operator="INCL", extra=extra, value=txtabout)
            extra = gt_lt2.upper()
        if txttitle:
            ok = my.Selection.objects.create(user=request.user.id,
                veldnm="title", operator="INCL", extra=extra, value=txttitle)
    if "arch" in selact:
        ok = my.Selection.objects.create(user=request.user.id,
            veldnm="arch", operator="EQ", extra=extra, value=False)
        if "all" in archall:
            ok = my.Selection.objects.create(user=request.user.id,
                veldnm="arch", operator="EQ", extra=extra, value=True)
    return HttpResponseRedirect("/{0}/?msg=De selectie is gewijzigd.".format(root))
def order(root,name,my,request):
    """
    bouw het scherm op aan de hand van de huidige sorteringsgegevens bij de gebruiker
    """
    if request.user.is_authenticated():
        msg = 'U bent ingelogd als <i>{0}</i>. '.format(request.user.username)
        msg += 'Klik <a href="/logout/?next=/{0}/order/">hier</a> om uit te loggen'.format(root)
    else:
        return HttpResponse('U moet ingelogd zijn om de sortering voor dit scherm ' +
            'te mogen wijzigen. <br/><br/>' +
            'Klik <a href="/accounts/login/?next=/{0}/select/">'.format(root) +
            'hier</a> om in te loggen, <a href="/{0}/">hier</a>'.format(root) +
            ' om terug te gaan.')
    page_data = {
        "name": name,
        "root": root,
        "pages": my.Page.objects.all().order_by('order'),
        "fields": [
            ("nummer","nummer"),
            ("gewijzigd","laatst gewijzigd"),
            ("soort", "soort"),
            ("status", "status"),
            ("behandelaar","behandelaar"),
            ("title","omschrijving"),
            ],
        "sorters": [],
        "msg": msg,
        }
    for sorter in my.SortOrder.objects.filter(user=request.user.id):
        page_data["sorters"].append(sorter)
    while len(page_data["sorters"]) < len(page_data["fields"]):
        page_data["sorters"].append(None)
    ## return HttpResponse("<br>".join([str(page_data[x]) for x in page_data]))
    return render_to_response(root + '/order.html',page_data)

def setorder(root,my,request):
    """
    verwerk de aanpassingen en koppel door naar tonen van de lijst met acties
    de huidige sorteringsgegevens voor de user worden verwijderd
    daarna worden nieuwe sorteringsgegevens bepaald en opgeslagen
    """
    data = request.POST
    fields = {
        "nummer": "nummer",
        "laatst gewijzigd": "gewijzigd",
        "soort": "soort",
        "status": "status",
        "behandelaar": "behandelaar",
        "omschrijving":"title",
        }
    page_data = {}
    my.SortOrder.objects.filter(user=request.user.id).delete()
    ix = 1
    while True:
        if "field" + str(ix) in data:
          if data["field" + str(ix)]:
            my.SortOrder.objects.create(user=request.user.id,volgnr=ix,
                veldnm=fields[data["field" + str(ix)]],richting=data["order" + str(ix)])
        else:
            break
        ix += 1
    return HttpResponseRedirect("/{0}/?msg=De sortering is gewijzigd.".format(root))

def detail(root,name,my,request,actie=""):
    """
    bouw het scherm met actiegegevens op.
    de soort user wordt meegegeven aan het scherm om indien nodig wijzigen onmogelijk te
        maken en diverse knoppen te verbergen.
    """
    msg = request.GET.get("msg","")
    if not msg:
        if request.user.is_authenticated():
            msg = 'U bent ingelogd als <i>{0}</i>. '.format(request.user.username)
            msg += 'Klik <a href="/logout/'
            inuit = 'uit'
        else:
            msg = 'U bent niet ingelogd. Klik <a href="/accounts/login/'
            inuit = 'in'
        msg += '?next=/{0}/{1}/">hier</a> om {2} te loggen. '.format(root,actie,inuit)
        if inuit == "uit":
            msg += "Klik op een van onderstaande termen om meer te zien."
    page_data = {
        "name": name,
        "root": root,
        "pages": my.Page.objects.all().order_by('order'),
        "soorten": my.Soort.objects.all().order_by('order'),
        "stats": my.Status.objects.all().order_by('order'),
        "users": [x.assigned for x in my.Worker.objects.all()],
        "msg": msg,
        }
    page_data["readonly"] = False if is_user(root,request.user) or is_admin(root,request.user) else True
    if actie == "nieuw":
        titel = "Nieuwe actie"
        volgnr = 0
        aant = my.Actie.objects.count()
        nw_date = dt.datetime.now()
        if aant:
            last = my.Actie.objects.all()[aant - 1]
            jaar,volgnr = last.nummer.split("-")
            volgnr = int(volgnr) if int(jaar ) == nw_date.year else 0
        volgnr += 1
        page_data["nummer"] = "{0}-{1:04}".format(nw_date.year,volgnr)
        ## page_data["start"] = nw_date
        page_data["nieuw"] = request.user
    else:
        actie = my.Actie.objects.get(pk=actie)
        page_data["actie"] = actie
        titel = "Actie {0} - titel/status".format(actie.nummer)
    page_data["title"] = titel
    return render_to_response(root + '/actie.html',page_data)

def wijzig(root,my,request,actie="",doe=""):
    """verwerk de aanpassingen en koppel door naar tonen van het scherm"""
    if not is_user(root,request.user) and not is_admin(root,request.user):
        if actie == "nieuw":
            text = "op te voeren"
        else:
            text = "te wijzigen"
        return HttpResponse("U bent niet geautoriseerd om acties {0}"
        '<br>Klik <a href="/{1}/">hier</a> om door te gaan'.format(text,root))
    data = request.POST
    nummer = data.get("nummer","")
    about = data.get("about","")
    title = data.get("title","")
    actor = int(data.get("user","0"))
    soort = data.get("soort"," ")
    status = int(data.get("status","1"))
    vervolg = data.get("vervolg","")
    if actie == "nieuw":
        actie = my.Actie()
        actie.nummer = nummer
        actie.starter = request.user
        actie.behandelaar = request.user
        ## actie.start = start
        doe = "nieuw"
        srt,stat = my.Soort.objects.get(value=" "), my.Status.objects.get(value="0")
    else:
        actie = get_object_or_404(my.Actie,pk=actie)
        over, wat, wie = actie.about, actie.title, actie.behandelaar
        srt, stat = actie.soort, actie.status
        arch = actie.arch
    if doe in ("arch","herl"):
        actie.arch = not arch
    else:
        actie.about = about
        actie.title = title
        actie.behandelaar = aut.User.objects.get(pk=actor)
        actie.soort = my.Soort.objects.get(value=soort)
        actie.status = my.Status.objects.get(value=status)
    actie.lasteditor = request.user
    actie.save()
    msg = ''
    mld = []
    if doe == "nieuw":
        msg = "Actie opgevoerd"
        store_event(my,msg, actie, request.user)
    elif doe == "arch":
        msg = "Actie gearchiveerd"
        store_event(my,msg, actie, request.user)
    elif doe == "herl":
        msg = "Actie herleefd"
        store_event(my,msg, actie, request.user)
    else:
        if actie.about != over:
            mld = store_gewijzigd(my,'onderwerp', str(actie.about),
                mld, actie, request.user)
        if actie.title != wat:
            mld = store_gewijzigd(my,'titel', str(actie.title),
                mld, actie, request.user)
        if actie.behandelaar != wie:
            mld = store_gewijzigd(my,'behandelaar', str(actie.behandelaar),
                mld, actie, request.user)
    if actie.soort != srt:
        mld = store_gewijzigd(my,'categorie', str(actie.soort),
            mld, actie, request.user)
    if actie.status != stat:
        mld = store_gewijzigd(my,'status',str(actie.status),
            mld, actie, request.user)
    if mld and not msg:
        if len(mld) == 1:
            msg = mld[0] + " gewijzigd"
        else:
            msg = ", ".join(mld[:-1]) + " en {0} gewijzigd".format(mld[-1])
        msg = msg.capitalize()
    ## return HttpResponse("*{0}* *{1}*".format(mld,msg))
    if vervolg:
        doc = "/{0}/{1}/meld/?msg={2}".format(root,actie.id,msg)
    else:
        doc = "/{0}/{1}/?msg={2}".format(root,actie.id,msg)
    if doe in ("arch","herl"):
        # indien nodig eerst naar doctool om de actie af te melden of te herleven
        follow = my.Event.objects.filter(actie=actie.id).order_by('id')[0].text
        if follow.startswith(UIT_DOCTOOL):
            doc = "{0}meld/?status={1}&from={2}".format(follow.split()[-1].strip(),doe,doc)
    return HttpResponseRedirect(doc)

def tekst(root,name,my,request,actie="",page=""):
    """
    toon een van de uitgebreide tekstrubrieken.
    de soort user wordt meegegeven aan het scherm om indien nodig wijzigen onmogelijk te
        maken en diverse knoppen te verbergen.
    """
    msg = request.GET.get("msg","")
    if not msg:
        if request.user.is_authenticated():
            msg = 'U bent ingelogd als <i>{0}</i>. '.format(request.user.username)
            msg += 'Klik <a href="/logout/'
            inuit = 'uit'
        else:
            msg = 'U bent niet ingelogd. Klik <a href="/accounts/login/'
            inuit = 'in'
        msg += '?next=/{0}/{1}/{2}/">hier</a> om {3} te loggen'.format(root,actie,page,inuit)
    page_data = {
        "root": root,
        "name": name,
        "pages": my.Page.objects.all().order_by('order'),
        "msg": msg,
        }
    page_data["readonly"] = False if is_user(root,request.user) or is_admin(root,request.user) else True
    actie = get_object_or_404(my.Actie,pk=actie)
    tab = my.Page.objects.get(link=page)
    page_titel = tab.title
    if page == "meld":
        page_text = actie.melding
        next = "oorz"
    elif page == "oorz":
        page_text = actie.oorzaak
        next = "opl"
    elif page == "opl":
        page_text = actie.oplossing
        next = "verv"
    elif page == "verv":
        page_text = actie.vervolg
        next = "voortg"
    else:
        return HttpResponse('<p>Geen <i>page</i> opgegeven</p>')
    page_data["page"] = page
    page_data["next"] = next
    page_data["page_titel"] = page_titel
    page_data["page_text"] = page_text
    page_data["actie"] = actie
    return render_to_response(root + '/tekst.html',page_data)

def wijzigtekst(root,my,request,actie="",page=""):
    """verwerk de aanpassingen en koppel door naar tonen van het scherm"""
    if not is_user(root,request.user) and not is_admin(root,request.user):
        return HttpResponse("U bent niet geautoriseerd om acties  te wijzigen"
        '<br>Klik <a href="/{0}/">hier</a> om door te gaan'.format(root))
    data = request.POST
    tekst = data.get("data","")
    vervolg = data.get("vervolg","")
    actie = get_object_or_404(my.Actie,pk=actie)
    if page == "meld":
        orig = actie.melding
        actie.melding = tekst
        ## next = "oorz"
    elif page == "oorz":
        orig = actie.oorzaak
        actie.oorzaak = tekst
        ## next = "opl"
    elif page == "opl":
        orig = actie.oplossing
        actie.oplossing = tekst
        ## next = "verv"
    elif page == "verv":
        orig = actie.vervolg
        actie.vervolg = tekst
        ## next = "voortg"
    else:
        return HttpResponse('<p>Geen <i>page</i> opgegeven</p>')
    ## return HttpResponse('<p>{{tekst}}</p>')
    actie.lasteditor = request.user
    actie.save()
    if page == "meld":
        if actie.melding != orig:
            msg = "Meldingtekst aangepast"
            store_event(my,msg, actie, request.user)
    elif page == "oorz":
        if actie.oorzaak != orig:
            msg = "Beschrijving oorzaak aangepast"
            store_event(my,msg, actie, request.user)
    elif page == "opl":
        if actie.oplossing != orig:
            msg = "Beschrijving oplossing aangepast"
            store_event(my,msg, actie, request.user)
    elif page == "verv":
        if actie.vervolg != orig:
            msg = "Beschrijving vervolgactie aangepast"
            store_event(my,msg, actie, request.user)
    page = vervolg if vervolg else page
    return HttpResponseRedirect(
        "/{0}/{1}/{2}/?msg={3}".format(root,actie.id,page,msg))

def events(root,name,my,request,actie="",event=""):
    """
    bouw de lijst op met actiehistorie (momenten).
    indien er een moment geselecteerd is, deze apart doorgeven voor in het onderste
        gedeelte van het scherm.
    de soort user wordt meegegeven aan het scherm om indien nodig wijzigen onmogelijk te
        maken en diverse knoppen te verbergen.
    """
    msg = request.GET.get("msg","")
    if not msg:
        if request.user.is_authenticated():
            msg = 'U bent ingelogd als <i>{0}</i>. '.format(request.user.username)
            msg += 'Klik <a href="/logout/'
            inuit = 'uit'
        else:
            msg = 'U bent niet ingelogd. Klik <a href="/accounts/login/'
            inuit = 'in'
        msg += '?next=/{0}/{1}/voortg/">hier</a> om {2} te loggen.'.format(root,actie,inuit)
    msg += " Klik op een voortgangsregel om de tekst nader te bekijken."
    actie = my.Actie.objects.select_related().get(id=actie)
    page_data = {
        "name": name,
        "root": root,
        "msg": msg,
        "pages": my.Page.objects.all().order_by('order'),
        "actie": actie,
        "events": actie.events.order_by("-start").order_by("-id"),
        "user": request.user,
        }
    page_data["readonly"] = False if is_user(root,request.user) or is_admin(root,request.user) else True
    if event == "nieuw":
        nw_date = dt.datetime.now()
        page_data["nieuw"] = True
        page_data["curr_ev"] = {"id": "nieuw","start": nw_date}
    elif event:
        page_data["curr_ev"] = my.Event.objects.get(pk=event)
    return render_to_response(root + '/voortgang.html',page_data)

def wijzigevents(root,my,request,actie="",event=""):
    """verwerk de aanpassingen en koppel door naar tonen van het scherm"""
    if not is_user(root,request.user) and not is_admin(root,request.user):
        return HttpResponse("U bent niet geautoriseerd om acties  te wijzigen"
        '<br>Klik <a href="/{0}/">hier</a> om door te gaan'.format(root))
    data = request.POST
    tekst = data.get("data","")
    actie = get_object_or_404(my.Actie,pk=actie)
    if event == "nieuw":
        event = my.Event()
        event.actie = actie
        event.starter = request.user
        ## actie.nummer = nummer
        ## event.start = dt.datetime.now()
    elif event:
        event = get_object_or_404(my.Event,pk=event)
    else:
        return HttpResponse("{0} {1}".format(actie,event))
    event.text = tekst
    event.save()
    return HttpResponseRedirect(
        "/{0}/{1}/voortg/?msg=De gebeurtenis is bijgewerkt.".format(root,actie.id))
