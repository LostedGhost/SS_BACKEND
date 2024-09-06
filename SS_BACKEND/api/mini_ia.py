import face_recognition
from .models import MembreMaison

def detect_intrusion_with_face_recognition(camera_image, maison):
    # Convertir l'image provenant de la caméra en tableau de pixels
    camera_image = face_recognition.load_image_file(camera_image)
    
    # Extraire les encodings faciaux de l'image capturée par la caméra
    camera_encodings = face_recognition.face_encodings(camera_image)
    
    if len(camera_encodings) == 0:
        return False, camera_image  # Aucun visage détecté dans l'image de la caméra
    
    # Obtenir les images des membres de la maison
    membres_images = MembreMaison.objects.filter(maison=maison).values_list('photo', flat=True)
    
    for membre_image_path in membres_images:
        # Charger l'image du membre et extraire son encodage facial
        membre_image = face_recognition.load_image_file(membre_image_path)
        membre_encodings = face_recognition.face_encodings(membre_image)
        
        if len(membre_encodings) == 0:
            continue  # Aucun visage détecté dans l'image du membre
        
        # Comparer l'encodage du visage de la caméra avec celui du membre
        results = face_recognition.compare_faces(membre_encodings, camera_encodings[0])
        
        if True in results:
            return False, camera_image  # C'est un membre autorisé, donc pas d'intrusion
    
    # Si aucune correspondance n'est trouvée, une intrusion est détectée
    return True, camera_image
