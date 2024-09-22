from django.test import TestCase, Client
from django.urls import reverse
from api.models import Utilisateur, Maison, CameraMaison, MembreMaison
from django.core.files.uploadedfile import SimpleUploadedFile

class APITestCase(TestCase):

    def setUp(self):
        # Set up client
        self.client = Client()

        # Create a test user
        self.user = Utilisateur.objects.create(
            nom="Doe", 
            prenom="John", 
            email="john@example.com", 
            password="password123", 
            telephone="+22912345678", 
            profil_id=2
        )

        # Create a test maison
        self.maison = Maison.objects.create(
            nom="Maison Test",
            description="Une maison de test",
            proprietaire=self.user
        )

        # Create a test camera
        self.camera = CameraMaison.objects.create(
            nom="Caméra Test",
            description="Caméra de test",
            lien="http://example.com/video_feed",
            maison=self.maison
        )

        # Create a test member
        self.membre = MembreMaison.objects.create(
            nom="Membre Test",
            maison=self.maison,
            photo=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )

    def test_connexion(self):
        response = self.client.post(reverse('connexion'), {'email': self.user.email, 'password': self.user.password})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "Connexion effectuée.")
    
    def test_inscription(self):
        response = self.client.post(reverse('inscription'), {
            'nom': "Jane",
            'prenom': "Doe",
            'email': "jane@example.com",
            'telephone': "123456789",
            'password': "password123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "L'utilisateur a été créé avec succès.")

    def test_add_home(self):
        response = self.client.post(reverse('add_home'), {
            'api_key': self.user.slug,
            'nom': "Maison 2",
            'description': "Deuxième maison",
            'prop': self.user.slug
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "La maison a été ajoutée avec succès pour Doe John.")

    def test_add_camera(self):
        response = self.client.post(reverse('add_camera'), {
            'api_key': self.user.slug,
            'maison': self.maison.code,
            'nom': "Caméra 2",
            'description': "Deuxième caméra",
            'lien': "http://example.com/video_feed_2"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "La caméra a été ajoutée avec succès pour la maison 'Maison Test'.")

    def test_api_handle_video_feed(self):
        with open('path_to_test_image.jpg', 'rb') as img:
            response = self.client.post(reverse('handle_video_feed', kwargs={'camera_id': self.camera.id}),
                                        {'image': img})
            self.assertEqual(response.status_code, 200)

    def test_read_home(self):
        response = self.client.post(reverse('read_home'), {
            'api_key': self.user.slug,
            'maison': self.maison.code
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "Maison récupérée avec succès.")

    def test_remove_home(self):
        response = self.client.post(reverse('remove_home'), {
            'api_key': self.user.slug,
            'maison': self.maison.code
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], f"La maison de {self.user.nom} {self.user.prenom} a été supprimée avec succès.")
