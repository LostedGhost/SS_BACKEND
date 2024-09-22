from api.models import *

p = Profil(libelle="Admin")
p.save()

p = Profil(libelle="Propriétaire")
p.save()

u = Utilisateur(
    nom="TOPANOU",
    prenom="Ludel",
    email="topanoulucio@gmail.com",
    password=chiffrement("Lucio@05042023"),
    telephone="+22961012344",
    profil_id=1
)
u.save()

u = Utilisateur(
    nom="ASSOGBA",
    prenom="Lucrèce",
    email="topanoululudel@gmail.com",
    password=chiffrement("0000"),
    telephone="+22961012344",
    profil_id=2
)
u.save()