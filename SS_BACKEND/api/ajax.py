from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from api.mini_ia import *
from api.models import *

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
    maison.nom = nom
    maison.description = description
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

# Gestion des membres d'une maison
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
    
    nom = request.POST.get("nom", f"Membre {f'{MembreMaison.objects.count()+1}'.zfill(2)}")
    photo = request.FILES.get("photo", None)
    if not photo:
        return JsonResponse({'status': 400, "message": "Veuillez sélectionner une photo pour le membre."})

    membre = MembreMaison(nom=nom, maison=maison, photo=photo)
    membre.save()
    return JsonResponse({'status': 200, "message": f"Le membre '{membre.nom}' a été ajouté avec succès pour la maison '{maison.nom}'."})

# Gestion du flux vidéo pour la détection d'intrusions
@require_http_methods(["POST"])
def api_handle_video_feed(request, camera_id):
    camera = CameraMaison.objects.get(id=camera_id)
    maison = camera.maison

    if 'image' not in request.FILES:
        return JsonResponse({'status': 400, 'message': 'Aucune image n\'a été envoyée.'})
    
    image = request.FILES['image']
    
    # Appel de la fonction de reconnaissance faciale
    is_intrusion, _ = detect_intrusion_with_face_recognition(image, maison)
    
    if is_intrusion:
        intrusion = IntrusionMaison.objects.create(camera_maison=camera, photo=image)
        return JsonResponse({'status': 200, 'is_intrusion': True, 'intrusion': intrusion.to_json()})
    
    return JsonResponse({'status': 200, 'is_intrusion': False})
