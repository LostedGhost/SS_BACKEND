from django.shortcuts import render, redirect
from api.models import *

# Create your views here.
def home(request):
    user_code = request.session.get('user_code', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if user_code == None:
        return redirect('/login')
    user = Utilisateur.objects.filter(slug=user_code).first()
    return render(request, 'home.html',{
        'user': user,
        'error': error,
        'success': success,
    })

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        if email and password:
            user = Utilisateur.objects.filter(email=email).first()
            if not user:
                request.session['error'] = "Informations incorrectes."
                return redirect('/')
            if user.password == chiffrement(password):
                request.session['user_code'] = user.slug
                return redirect('/')
            else:
                request.session['error'] = "Informations incorrectes."
                return redirect('/')
        request.session['error'] = "Informations incomplètes."
        return redirect('/')
    else:
        return render(request, 'login.html', {
            'error': request.session.pop('error', None),
            'success': request.session.pop('success', None),
        })

def logout(request):
    request.session.pop('user_code', None)
    return redirect('/login')
        
def users(request):
    user_code = request.session.get('user_code', None)
    if user_code == None:
        return redirect('/login')
    user = Utilisateur.objects.filter(slug=user_code).first()
    if user.profil.id != 1:
        return redirect('/')
    users = Utilisateur.objects.all()
    users = [user.to_json() for user in users]
    return render(request, 'users.html', {
        'user': user,
        'users': users,
        'nb_donnees': len(users),
        'error': request.session.pop('error', None),
        'success': request.session.pop('success', None),
    })

def add_user(request):
    user_code = request.session.get('user_code', None)
    if user_code == None:
        return redirect('/login')
    user = Utilisateur.objects.filter(slug=user_code).first()
    if user.profil.id != 1:
        return redirect('/')
    if request.method == 'POST':
        nom = request.POST.get('nom', None)
        prenom = request.POST.get('prenom', None)
        email = request.POST.get('email', None)
        telephone = "+229" + request.POST.get('telephone', None)
        password = request.POST.get('password', None)
        photo = request.FILES.get('photo', None)
        profil_id = 2  # Profil utilisateur standard
        """ if not is_strong_password(password):
            request.session['error'] = "Le mot de passe n'est pas assez robuste"
            return redirect('/users')
        elif not is_valid_email(email):
            request.session['error'] = "L'adresse email n'est pas valide."
            return redirect('/users') """
        """ elif not is_valid_phone_number(telephone):
            request.session['error'] = "Le numéro de téléphone n'est pas valide."
            return redirect('/users') """
        user = Utilisateur(
            nom=nom, prenom=prenom, email=email,
            password=chiffrement(password), telephone=telephone,
            profil_id=profil_id, photo=photo
        )
        user.save()
        request.session['success'] = "Utilisateur ajouté avec succès."
        return redirect('/users')
    return render(request, 'add_user.html', {
        'user': user,
        'error': request.session.pop('error', None),
        'success': request.session.pop('success', None),
    })

def edit_user(request, slug):
    user_code = request.session.get('user_code', None)
    if user_code == None:
        return redirect('/login')
    user = Utilisateur.objects.filter(slug=user_code).first()
    if user.profil.id != 1:
        return redirect('/')
    prop = Utilisateur.objects.filter(slug=slug).first()
    if request.method == 'POST':
        nom = request.POST.get('nom', None)
        prenom = request.POST.get('prenom', None)
        email = request.POST.get('email', None)
        telephone = "+229" + request.POST.get('telephone', None)
        password = request.POST.get('password', None)
        photo = request.FILES.get('photo', None)
        """ if not is_strong_password(password):
            request.session['error'] = "Le mot de passe n'est pas assez robuste"
            return redirect('/users')
        elif not is_valid_email(email):
            request.session['error'] = "L'adresse email n'est pas valide."
            return redirect('/users') """
        """ elif not is_valid_phone_number(telephone):
            request.session['error'] = "Le numéro de téléphone n'est pas valide."
            return redirect('/users') """
        prop.nom = nom
        prop.prenom = prenom
        prop.email = email
        prop.telephone = telephone
        prop.password = chiffrement(password)
        if photo:
            prop.photo = photo
        prop.save()
        request.session['success'] = "Utilisateur modifié avec succès."
        return redirect('/users')
    return render(request, 'alter_user.html', {
        'user': user,
        'prop': prop,
        'error': request.session.pop('error', None),
        'success': request.session.pop('success', None),
    })

def remove_user(request, slug):
    user_code = request.session.get('user_code', None)
    if user_code == None:
        return redirect('/login')
    user = Utilisateur.objects.filter(slug=user_code).first()
    if user.profil.id != 1:
        return redirect('/')
    prop = Utilisateur.objects.filter(slug=slug).first()
    prop.delete()
    request.session['success'] = "Utilisateur supprimé avec succès."
    return redirect('/users')