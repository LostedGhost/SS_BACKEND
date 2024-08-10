from django.http import JsonResponse
from api.models import *

# Create your views here.

def get_error(request):
    error = request.session.pop('error', None)
    response_data = {
        'error': error
    }
    return JsonResponse(response_data)

def get_success(request):
    success = request.session.pop('success', None)
    response_data = {
       'success': success
    }
    return JsonResponse(response_data)

def connexion(request):
    email = request.GET.get('email', None)
    password = request.GET.get('password', None)
    if email and password:
        user = Utilisateur.objects.filter(email=email)
        if not user.exists():
            return JsonResponse({
                'error': "Informations incorrectes."
            })
        else:
            user = user.first()
            if user.password == chiffrement(password):
                request.session["user_slug"] = user.slug
                return JsonResponse({
                    'success': "Connexion effectuée.",
                    'user': user.to_json(),
                    "user_slug": request.session.get("user_slug", None)
                })
            else:
                return JsonResponse({
                    'error': "Informations incorrectes."
                })
    else:
        return JsonResponse({
            'error': "Informations incomplètes."
        })

def utilisateur(request):
    slug = request.session.get("user_slug", None)
    user = Utilisateur.objects.filter(slug=slug)
    if not user.exists():
        error = "Aucun utilisateur n'est connecté."
        request.session["error"] = error
        return JsonResponse({
            "error": error
        })
    else:
        user = user.first()
        return JsonResponse({
            "user": user.to_json(),
        })

def deconnexion(request):
    request.session.clear()
    success = "Déconnexion effectuée avec succès."
    request.session["success"] = success
    return JsonResponse({
        'success': success,
    })

def inscription(request):
    nom = request.GET.get('nom', None)
    prenom = request.GET.get('prenom', None)
    email = request.GET.get('email', None)
    telephone = "+229" + request.GET.get('telephone', None)
    password = request.GET.get('password', None)
    photo = request.FILES.get('photo', None)
    profil_id = 2
    
    if not is_strong_password(password):
        error = "Le mot de passe n'est pas assez robuste"
        request.session["error"] = error
        return JsonResponse({
            "error": error,
        })
    elif not is_valid_email(email):
        error = "L'adresse email n'est pas valide."
        request.session["error"] = error
        return JsonResponse({
            "error": error
        })
    elif not is_valid_phone_number(telephone):
        error = "Le numéro de téléphone n'est pas valide."
        request.session["error"] = error
        return JsonResponse({
            "error": error
        })
    elif not photo:
        error = "La photo n'est pas optionnelle."
        request.session["error"] = error
        return JsonResponse({
            "error": error
        })
    else:
        user = Utilisateur(
            nom=nom,
            prenom=prenom,
            email=email,
            password=chiffrement(password),
            telephone=telephone,
            profil_id=profil_id,
            photo = photo,
        )
        user.save()
        success = "L'utilisateur a été créé avec succès."
        request.session["success"] = success
        return JsonResponse({
            "success": success
        })



