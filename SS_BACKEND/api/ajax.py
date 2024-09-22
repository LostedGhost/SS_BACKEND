from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from api.mini_ia import detect_intrusion_with_face_recognition
from api.models import *
from api.utils import *

# Connexion d'un utilisateur
@require_http_methods(["POST"])
def connexion(request):
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    if email and password:
        user = Utilisateur.objects.filter(email=email).first()
        if not user:
            return JsonResponse({'status': 400, 'message': "Informations incorrectes."})
        if user.password == chiffrement(password):
            return JsonResponse({'status': 200, 'message': "Connexion effectuée.", 'user': user.slug})
        else:
            return JsonResponse({'status': 400, 'message': "Informations incorrectes."})
    return JsonResponse({'status': 400, 'message': "Informations incomplètes."})

# Récupération des infos d'un utilisateur
@require_http_methods(["GET"])
def utilisateur(request):
    slug = request.GET.get("api_key", None)
    user = Utilisateur.objects.filter(slug=slug).first()
    if not user:
        return JsonResponse({'status': 400, "message": "Aucun utilisateur n'est connecté."})
    return JsonResponse({'status': 200, 'message': "Utilisateur récupéré avec succès.", "user": user.to_json()})

# Inscription d'un utilisateur
@require_http_methods(["POST"])
def inscription(request):
    nom = request.POST.get('nom', None)
    prenom = request.POST.get('prenom', None)
    email = request.POST.get('email', None)
    telephone = "+229" + request.POST.get('telephone', None)
    password = request.POST.get('password', None)
    photo = request.FILES.get('photo', None)
    profil_id = 2  # Profil utilisateur standard

    if not is_strong_password(password):
        return JsonResponse({'status': 400, "message": "Le mot de passe n'est pas assez robuste"})
    elif not is_valid_email(email):
        return JsonResponse({'status': 400, "message": "L'adresse email n'est pas valide."})
    elif not is_valid_phone_number(telephone):
        return JsonResponse({'status': 400, "message": "Le numéro de téléphone n'est pas valide."})

    user = Utilisateur(
        nom=nom, prenom=prenom, email=email, 
        password=chiffrement(password), telephone=telephone, 
        profil_id=profil_id, photo=photo
    )
    user.save()
    return JsonResponse({'status': 200, "message": "L'utilisateur a été créé avec succès."})

# Ajout d'une maison
@require_http_methods(["POST"])
def add_home(request):
    slug = request.POST.get("api_key", None)
    user = Utilisateur.objects.filter(slug=slug).first()
    if not user or user.profil.id != 1:
        return JsonResponse({'status': 400, "message": "Opération réservée à l'administrateur."})

    nom = request.POST.get('nom', f"Maison {f'{Maison.objects.count() + 1}'.zfill(2)}")
    description = request.POST.get('description', "")
    prop_slug = request.POST.get('prop', "")
    proprietaire = Utilisateur.objects.filter(slug=prop_slug).first()
    if not proprietaire:
        return JsonResponse({'status': 400, "message": "Le propriétaire spécifié n'existe pas."})

    maison = Maison(nom=nom, description=description, proprietaire_id=proprietaire.id)
    maison.save()
    return JsonResponse({'status': 200, "message": f"La maison a été ajoutée avec succès pour {proprietaire.nom} {proprietaire.prenom}."})

# Modification d'une maison
@require_http_methods(["POST"])
def alter_home(request):
    slug = request.POST.get("api_key", None)
    user = Utilisateur.objects.filter(slug=slug).first()
    if not user or user.profil.id != 1:
        return JsonResponse({'status': 400, "message": "Opération réservée à l'administrateur."})

    maison_slug = request.POST.get('maison', "")
    maison = Maison.objects.filter(code=maison_slug).first()
    if not maison:
        return JsonResponse({'status': 400, "message": "La maison spécifiée n'existe pas."})

    nom = request.POST.get('nom', maison.nom)
    description = request.POST.get('description', maison.description)
    prop = request.POST.get('prop', maison.proprietaire.slug)
    maison.nom = nom
    maison.description = description
    maison.proprietaire = Utilisateur.objects.get(slug=prop)
    maison.save()
    return JsonResponse({'status': 200, "message": f"La maison de {maison.proprietaire.nom} {maison.proprietaire.prenom} a été modifiée avec succès."})

# Suppression d'une maison
@require_http_methods(["POST"])
def remove_home(request):
    slug = request.POST.get("api_key", None)
    user = Utilisateur.objects.filter(slug=slug).first()
    if not user or user.profil.id != 1:
        return JsonResponse({'status': 400, "message": "Opération réservée à l'administrateur."})

    maison_slug = request.POST.get('maison', "")
    maison = Maison.objects.filter(code=maison_slug).first()
    if not maison:
        return JsonResponse({'status': 400, "message": "La maison spécifiée n'existe pas."})

    maison.delete()
    return JsonResponse({'status': 200, "message": f"La maison de {maison.proprietaire.nom} {maison.proprietaire.prenom} a été supprimée avec succès."})

# Lecture d'une maison
@require_http_methods(["POST"])
def read_home(request):
    slug = request.POST.get("api_key", None)
    user = Utilisateur.objects.filter(slug=slug).first()
    if not user:
        return JsonResponse({'status': 400, "message": "Aucun utilisateur n'est connecté."})
    
    home_code = request.POST.get('maison', "")
    maison = Maison.objects.filter(code=home_code).first()
    if not maison:
        return JsonResponse({'status': 400, "message": "La maison spécifiée n'existe pas."})
    
    return JsonResponse({'status': 200, "message": "Maison récupérée avec succès.", "data": maison.to_json()})

# Gestion des caméras
@require_http_methods(["POST"])
def add_camera(request):
    slug = request.POST.get("api_key", None)
    user = Utilisateur.objects.filter(slug=slug).first()
    if not user:
        return JsonResponse({'status': 400, "message": "Aucun utilisateur n'est connecté."})

    maison_slug = request.POST.get('maison', "")
    maison = Maison.objects.filter(code=maison_slug).first()
    if not maison:
        return JsonResponse({'status': 400, "message": "La maison spécifiée n'existe pas."})

    nom = request.POST.get('nom', f"Caméra {f'{CameraMaison.objects.count() + 1}'.zfill(2)}")
    description = request.POST.get('description', "")
    lien = request.POST.get('lien', "#")
    camera = CameraMaison(nom=nom, description=description, lien=lien, maison_id=maison.id)
    camera.save()
    return JsonResponse({'status': 200, "message": f"La caméra a été ajoutée avec succès pour la maison '{maison.nom}'."})

@require_http_methods(["POST"])
def alter_camera(request):
    slug = request.POST.get("api_key", None)
    user = Utilisateur.objects.filter(slug=slug).first()
    if not user:
        return JsonResponse({'status': 400, "message": "Aucun utilisateur n'est connecté."})

    maison_slug = request.POST.get('maison', "")
    maison = Maison.objects.filter(code=maison_slug).first()
    if not maison:
        return JsonResponse({'status': 400, "message": "La maison spécifiée n'existe pas."})
    
    camera_slug = request.POST.get('camera', "")
    camera = CameraMaison.objects.filter(code=camera_slug).first()
    if not camera:
        return JsonResponse({'status': 400, "message": "La caméra spécifiée n'existe pas."})
    
    nom = request.POST.get('nom', camera.nom)
    description = request.POST.get('description', camera.description)
    lien = request.POST.get('lien', camera.lien)
    camera.nom = nom
    camera.description = description
    camera.lien = lien
    camera.save()
    return JsonResponse({'status': 200, "message": f"La caméra a été modifiée avec succès pour la maison '{maison.nom}'."})

@require_http_methods(["POST"])
def remove_camera(request):
    slug = request.POST.get("api_key", None)
    user = Utilisateur.objects.filter(slug=slug).first()
    if not user:
        return JsonResponse({'status': 400, "message": "Aucun utilisateur n'est connecté."})

    maison_slug = request.POST.get('maison', "")
    maison = Maison.objects.filter(code=maison_slug).first()
    if not maison:
        return JsonResponse({'status': 400, "message": "La maison spécifiée n'existe pas."})

    camera_slug = request.POST.get('camera', "")
    camera = CameraMaison.objects.filter(code=camera_slug).first()
    if not camera:
        return JsonResponse({'status': 400, "message": "La caméra spécifiée n'existe pas."})

    camera.delete()
    return JsonResponse({'status': 200, "message": "La caméra a été supprimée avec succès."})

# Ajout d'un membre à la maison
@require_http_methods(["POST"])
def add_home_member(request):
    slug = request.POST.get("api_key", None)
    user = Utilisateur.objects.filter(slug=slug).first()
    if not user:
        return JsonResponse({'status': 400, "message": "Aucun utilisateur n'est connecté."})

    maison_slug = request.POST.get('maison', "")
    maison = Maison.objects.filter(code=maison_slug).first()
    if not maison:
        return JsonResponse({'status': 400, "message": "La maison spécifiée n'existe pas."})

    nom = request.POST.get('nom', None)
    photo = request.FILES.get('photo', None)
    membre = MembreMaison(nom=nom, maison=maison, photo=photo)
    membre.save()
    return JsonResponse({'status': 200, "message": f"{nom} a été ajouté comme membre de la maison."})

# Lecture d'un membre de maison
@require_http_methods(["GET"])
def read_home_member(request):
    slug = request.GET.get("api_key", None)
    user = Utilisateur.objects.filter(slug=slug).first()
    if not user:
        return JsonResponse({'status': 400, "message": "Aucun utilisateur n'est connecté."})

    maison_slug = request.GET.get('maison', "")
    maison = Maison.objects.filter(code=maison_slug).first()
    if not maison:
        return JsonResponse({'status': 400, "message": "La maison spécifiée n'existe pas."})

    membres = MembreMaison.objects.filter(maison=maison)
    return JsonResponse({'status': 200, "message": "Membres récupérés avec succès.", "membres": [membre.to_json() for membre in membres]})

# Modification d'un membre de maison
@require_http_methods(["POST"])
def alter_home_member(request):
    slug = request.POST.get("api_key", None)
    user = Utilisateur.objects.filter(slug=slug).first()
    if not user:
        return JsonResponse({'status': 400, "message": "Aucun utilisateur n'est connecté."})
    membre_slug = request.POST.get('membre', "")
    membre = MembreMaison.objects.filter(slug=membre_slug).first()
    if not membre:
        return JsonResponse({'status': 400, "message": "Le membre spécifié n'existe pas."})
    nom = request.POST.get('nom', membre.nom)
    photo = request.FILES.get('photo', membre.photo)
    membre.nom = nom
    membre.photo = photo
    membre.save()
    return JsonResponse({'status': 200, "message": "Le membre a été modifié avec succès."})


# Suppression d'un membre de maison
@require_http_methods(["POST"])
def remove_home_member(request):
    slug = request.POST.get("api_key", None)
    user = Utilisateur.objects.filter(slug=slug).first()
    if not user:
        return JsonResponse({'status': 400, "message": "Aucun utilisateur n'est connecté."})

    membre_slug = request.POST.get('membre', "")
    membre = MembreMaison.objects.filter(slug=membre_slug).first()
    if not membre:
        return JsonResponse({'status': 400, "message": "Le membre spécifié n'existe pas."})

    membre.delete()
    return JsonResponse({'status': 200, "message": "Le membre a été supprimé avec succès."})

# Gestion du flux vidéo de la caméra
@require_http_methods(["POST"])
def api_handle_video_feed(request, camera_id):
    camera = CameraMaison.objects.get(id=camera_id)
    if request.method == 'POST':
        image_file = request.FILES.get('image', None)
        if image_file:
            intrusion_detected, camera_image = detect_intrusion_with_face_recognition(image_file, camera.maison)
            if intrusion_detected:
                # Envoyer un email
                subject = "Intrusion détectée!"
                message = "Une intrusion a été détectée dans votre maison."
                recipient_list = [camera.maison.proprietaire.email]
                send_personalized_email(subject, message, recipient_list)

                # Appeler l'utilisateur
                call_user(camera.maison.proprietaire.telephone)

                return JsonResponse({'status': 200, "message": "Intrusion détectée!", "image": camera_image})
            return JsonResponse({'status': 200, "message": "Aucune intrusion détectée.", "image": camera_image})
    return JsonResponse({'status': 400, "message": "Aucune image reçue."})

