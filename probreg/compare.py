"""vergelijk de twee in de invoer genoemde Probreg XML files em zet de output in een derde

1. lees alles in
2. sorteer eventueel op kenmerkend attribuut per node
nee we gaan niet sorteren maar langslopen en zoeken in de andere
-- settings file met sorteerkenmerk per herhaald element
opbouw bv.
[rootnaam]
elementnaam=keynaam
...
[elementnaam]
subelementnaam=keynaam
"""
import sys
import xml.etree.ElementTree as et


def doactie(x, y):
    "vergelijk acties met een overeenkomstig nummer "
    verschillen = {}
    for a in ('arch', 'datum', 'soort', 'status', 'updated'):
        xa = x.get(a)
        if xa is not None and xa != '' and xa[-1] == '\n':
            xa = xa[:-1]
        ya = y.get(a)
        if ya is not None and ya != '' and ya[-1] == '\n':
            ya = xa[:-1]
        if xa != ya:
            verschillen[a] = (xa, ya)
    for e in ('titel', 'melding', 'oorzaak', 'oplossing', 'vervolg'):
        if x.find(e) is not None:
            xt = x.find(e).text
            if xt is not None and xt[-1] == '\n':
                xt = xt[:-1]
        else:
            xt = ''
        if y.find(e) is not None:
            yt = y.find(e).text
            if yt is not None and yt[-1] == '\n':
                yt = yt[:-1]
        else:
            yt = ''
        if xt != yt:
            verschillen[e] = (xt, yt)
    return verschillen


def dosett(x, y):
    "vergelijk de settings"
    verschillen = {}
    ex = {}
    for e in ('stats', 'cats', 'koppen'):
        dx = []
        for s in x.find(e):
            dx.append((s.get('order'), s.get('value'), s.text))
        dx.sort()
        ex[e] = dx
    ey = {}
    for e in ('stats', 'cats', 'koppen'):
        dy = []
        for s in y.find(e):
            dy.append((s.get('order'), s.get('value'), s.text))
        dy.sort()
        ey[e] = dy
    for e in ('stats', 'cats', 'koppen'):
        if ex[e] != ey[e]:
            verschillen[e] = (ex[e], ey[e])
    return verschillen


def vergelijk(file1, file2, uit=sys.stdout):
    "het daadwerlkelijke vergelijken"
    x1 = et.ElementTree(file=file1)
    r1 = x1.getroot()
    ## l1 = [(e, e.tag) for e in list(r1)]  # deze variabele wordt niet gebruikt

    x2 = et.ElementTree(file=file2)
    r2 = x2.getroot()
    l2 = [(e, e.tag) for e in list(r2)]

    verschillen = []
    for x in list(r1):
        xtg = x.tag
        xid = x.get('id')      # sleutelwaarde voor acties
        for y in l2:
            found = False
            if y[1] == xtg:
                if xtg == 'settings':
                    found = True
                    h = dosett(x, y[0])
                    if len(h) > 0:
                        verschillen.append(('settings', h))
                else:
                    yid = y[0].get('id')
                    if xid is not None and yid is not None and yid == xid:
                        found = True
                        h = doactie(x, y[0])
                        if len(h) > 0:
                            verschillen.append(('actie ' + xid, h))
            if found:
                l2.remove(y)
                break
            # meld dit element als "unmatched"
            verschillen.append(('actie ' + xid, "alleen in " + file1))
    for y in l2:
        # meld deze elementen als "unmatched"
        verschillen.append(('actie ' + y[0].get('id'), "alleen in " + file2))

    if len(verschillen) > 0:
        uit.write(f"verschillen tussen {file1} en {file2}\n")
    for x in verschillen:
        if isinstance(x[1], dict):
            uit.write(f'-------------------------\n{x[0]}\n')
            for y in list(x[1].keys()):
                uit.write(f'-\n{y}\n')
                h = x[1][y][0]
                if h is None:
                    h = 'n/a'
                uit.write(f"*** links: ***\n{h}\n")      #  h.encode('latin-1'))
                h = x[1][y][1]
                if h is None:
                    h = 'n/a'
                uit.write(f"*** rechts: ***\n{h}\n\n")   #  h.encode('latin-1'))
        else:
            uit.write(f"{x[0]} {x[1]}\n")


def main(argv):
    "functie uitvoeren"
    f1 = argv[1]
    f2 = argv[2]
    with open('vergelijk_jvs.txt', 'w') as f3:
        vergelijk(f1, f2, f3)


if __name__ == '__main__':
    main(sys.argv)
