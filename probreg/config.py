DBLOC = "/home/albert/www/actiereg/actiereg.db"
USER = 2
APPS = "/home/albert/www/actiereg/apps.dat"
# default settings
kopdict = {
    "0": ("Lijst",'index'),
    "1": ("Titel/Status",'detail'),
    "2": ("Probleem/Wens",'meld'),
    "3": ("Oorzaak/Analyse",'oorz'),
    "4": ("Oplossing",'opl'),
    "5": ("Vervolgactie",'verv'),
    "6": ("Voortgang",'voortg')
}
statdict = {
    "0": ("gemeld", 0),
    "1": ("in behandeling", 1),
    "2": ("oplossing controleren",2),
    "3": ("nog niet opgelost",3),
    "4": ("afgehandeld", 4),
    "5": ("afgehandeld - vervolg",5)
}
catdict = {
    "P": ("probleem",1),
    "W": ("wens",2),
    " ": ("onbekend",0),
    "V": ("vraag",3),
    "I": ("idee",4),
    "F": ("div. informatie",5)
}

