from django.db import models
from api.config import AUTH_EXPIRATION
from api.utils import *

# Create your models here.
class Profil(models.Model):
    libelle = models.CharField(max_length=MAX_LENGHT_LIBELLE)
    def to_json(self):
        return {
            "id": self.id,
            "libelle": self.libelle
        }

class Utilisateur(models.Model):
    slug = models.CharField(max_length=LENGTH_CODE, unique=True)
    nom = models.CharField(max_length=MAX_LENGHT_LIBELLE)
    prenom = models.CharField(max_length=MAX_LENGHT_LIBELLE)
    email = models.EmailField(max_length=MAX_LENGHT_LIBELLE, unique=True)
    telephone = models.CharField(max_length=MAX_LENGHT_LIBELLE)
    password = models.CharField(max_length=MAX_LENGHT_LIBELLE)
    photo = models.ImageField(upload_to='photos/Utilisateur/', null=True, blank=True)
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(default=datetime.now())
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slugs = Utilisateur.objects.all().values_list('slug', flat=True).distinct()
            while True:
                slug = generate_string(LENGTH_CODE)
                if slug not in slugs:
                    break
            self.slug = slug
        super().save(*args, **kwargs)
    
    def to_json(self):
        return {
            "slug": self.slug,
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "telephone": self.telephone,
            "photo": self.photo,
            "profil": self.profil.to_json(),
            "date_ajout": full_date_to_text(self.date_ajout),
        }
    
    def maisons(self):
        return Maison.objects.filter(proprietaire=self)

class AuthUser(models.Model):
    code = models.CharField(max_length=LENGTH_CODE, unique=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name="auth_utilisateur")
    date_expiration = models.DateTimeField(default=datetime.now()+timedelta(minutes=AUTH_EXPIRATION))
    
    def save(self, *args, **kwargs):
        if not self.code:
            codes = AuthUser.objects.all().values_list('code', flat=True).distinct()
            while True:
                code = generate_string(30)
                if code not in codes:
                    break
            self.code = code
        super().save(*args, **kwargs)
    
    def to_json(self):
        return {
            "code": self.code,
            "utilisateur": self.utilisateur.to_json(),
            "date_expiration": full_date_to_text(self.date_expiration),
        }

class Maison(models.Model):
    code = models.CharField(max_length=LENGTH_CODE, unique=True)
    nom = models.CharField(max_length=MAX_LENGHT_LIBELLE)
    description = models.CharField(max_length=MAX_LENGHT_LIBELLE)
    date_ajout = models.DateTimeField(auto_created=True)
    proprietaire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.code:
            codes = Maison.objects.all().values_list('code', flat=True).distinct()
            while True:
                code = generate_string(LENGTH_CODE)
                if code not in codes:
                    break
            self.code = code
        super().save(*args, **kwargs)
    
    def to_json(self):
        return {
            "code": self.code,
            "nom": self.nom,
            "description": self.description,
            "date_ajout": full_date_to_text(self.date_ajout),
            "propietaire": self.proprietaire.to_json(),
            
        }
        h = {"cameras": [cam.to_json() for cam in self.cameras()],
        "periodes_surveillance": [period.to_json() for period in self.periods()],
        "membres": [membre.to_json() for membre in self.membres()],
        "intrusions": [intrusion.to_json() for intrusion in self.intrusions()]}
    
    def cameras(self):
        return CameraMaison.objects.filter(maison=self)
    
    def camIds(self):
        return self.cameras().values_list('id', flat=True)
    
    def periods(self):
        return PeriodeSurveillanceMaison.objects.filter(maison=self)
    
    def membres(self):
        return MembreMaison.objects.filter(maison=self)
    
    def intrusions(self):
        return IntrusionMaison.objects.filter(camera_maison__in=self.camIds())

class PeriodeSurveillanceMaison(models.Model):
    code = models.CharField(max_length=LENGTH_CODE, unique=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    maison = models.ForeignKey(Maison, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.code:
            codes = Maison.objects.all().values_list('code', flat=True).distinct()
            while True:
                code = generate_string(LENGTH_CODE)
                if code not in codes:
                    break
            self.code = code
        super().save(*args, **kwargs)
    
    def to_json(self):
        return {
            "code": self.code,
            "date_debut": full_date_to_text(self.date_debut),
            "date_fin": full_date_to_text(self.date_fin),
            "maison": self.maison.to_json(),
        }

class MembreMaison(models.Model):
    code = models.CharField(max_length=LENGTH_CODE, unique=True)
    nom = models.CharField(max_length=MAX_LENGHT_LIBELLE)
    photo = models.ImageField(upload_to='photos/MembreMaison/')
    maison = models.ForeignKey(Maison, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(default=datetime.now())
    
    def save(self, *args, **kwargs):
        if not self.code:
            codes = Maison.objects.all().values_list('code', flat=True).distinct()
            while True:
                code = generate_string(LENGTH_CODE)
                if code not in codes:
                    break
            self.code = code
        super().save(*args, **kwargs)
    
    def to_json(self):
        return {
            "code": self.code,
            "nom": self.nom,
            "photo": self.photo,
            "maison": self.maison.to_json(),
            "date_ajout": full_date_to_text(self.date_ajout),
        }

class CameraMaison(models.Model):
    code = models.CharField(max_length=LENGTH_CODE, unique=True)
    nom = models.CharField(max_length=MAX_LENGHT_LIBELLE)
    description = models.CharField(max_length=MAX_LENGHT_LIBELLE)
    lien = models.CharField(max_length=MAX_LENGHT_LIBELLE)
    date_ajout = models.DateTimeField(auto_created=True)
    maison = models.ForeignKey(Maison, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.code:
            codes = Maison.objects.all().values_list('code', flat=True).distinct()
            while True:
                code = generate_string(LENGTH_CODE)
                if code not in codes:
                    break
            self.code = code
        super().save(*args, **kwargs)
    
    def to_json(self):
        return {
            "code": self.code,
            "nom": self.nom,
            "description": self.description,
            "lien": self.lien,
            "date_ajout": full_date_to_text(self.date_ajout),
            "maison": self.maison.to_json(),
        }

class IntrusionMaison(models.Model):
    code = models.CharField(max_length=LENGTH_CODE, unique=True)
    date_ajout = models.DateTimeField(auto_created=True)
    camera_maison = models.ForeignKey(CameraMaison, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/IntrusionMaison/')

    def save(self, *args, **kwargs):
        if not self.code:
            codes = Maison.objects.all().values_list('code', flat=True).distinct()
            while True:
                code = generate_string(LENGTH_CODE)
                if code not in codes:
                    break
            self.code = code
        super().save(*args, **kwargs)
    
    def to_json(self):
        return {
            "code": self.code,
            "date_ajout": full_date_to_text(self.date_ajout),
            "camera_maison": self.camera_maison.to_json(),
            "photo": self.photo,
        }
