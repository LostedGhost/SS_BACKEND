# API Documentation

## Table of Contents

- [Introduction](#introduction)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [POST /connexion](#post-connexion)
  - [POST /utilisateur](#post-utilisateur)
  - [POST /inscription](#post-inscription)
  - [POST /add_home](#post-add_home)
  - [POST /alter_home](#post-alter_home)
  - [POST /remove_home](#post-remove_home)
  - [GET /read_home](#get-read_home)
  - [POST /add_camera](#post-add_camera)
  - [POST /alter_camera](#post-alter_camera)
  - [POST /remove_camera](#post-remove_camera)
  - [POST /add_home_member](#post-add_home_member)
  - [POST /alter_home_member](#post-alter_home_member)
  - [POST /remove_home_member](#post-remove_home_member)
  - [GET /read_home_member](#get-read_home_member)
  - [GET /handle_video_feed/camera_id](#get-handle_video_feed-camera_id)

## Introduction

Cette API permet de gérer les utilisateurs, les maisons, les caméras et les membres de maison, et inclut des fonctionnalités liées à la gestion de la vidéo en direct. L'API utilise des requêtes POST pour l'ajout et la modification des données et GET pour la récupération des informations.

## Authentication

Certaines routes peuvent nécessiter un token d'authentification. Assurez-vous de gérer les jetons appropriés si l'authentification est nécessaire.

---

## Endpoints

### POST /connexion

Authentification des utilisateurs.

#### Paramètres:

- `username`: (str) Nom d'utilisateur
- `password`: (str) Mot de passe

#### Réponse:

```json
{
  "success": bool,
  "message": "string",
  "token": "string"  // Token JWT si la connexion est réussie
}
```

---

### POST /utilisateur

Récupération des informations de l'utilisateur connecté.

#### Paramètres:

- Token d'authentification (inclus dans l'en-tête)

#### Réponse:

```json
{
  "username": "string",
  "email": "string",
  "homes": []
}
```

---

### POST /inscription

Création d'un nouvel utilisateur.

#### Paramètres:

- `username`: (str) Nom d'utilisateur
- `password`: (str) Mot de passe
- `email`: (str) Adresse e-mail

#### Réponse:

```json
{
  "success": bool,
  "message": "string"
}
```

---

### POST /add_home

Ajout d'une nouvelle maison.

#### Paramètres:

- `name`: (str) Nom de la maison
- `address`: (str) Adresse de la maison
- Token d'authentification (inclus dans l'en-tête)

#### Réponse:

```json
{
  "success": bool,
  "message": "string"
}
```

---

### POST /alter_home

Modification des informations d'une maison existante.

#### Paramètres:

- `home_id`: (int) ID de la maison à modifier
- `name`: (str) Nouveau nom (optionnel)
- `address`: (str) Nouvelle adresse (optionnel)
- Token d'authentification (inclus dans l'en-tête)

#### Réponse:

```json
{
  "success": bool,
  "message": "string"
}
```

---

### POST /remove_home

Suppression d'une maison.

#### Paramètres:

- `home_id`: (int) ID de la maison à supprimer
- Token d'authentification (inclus dans l'en-tête)

#### Réponse:

```json
{
  "success": bool,
  "message": "string"
}
```

---

### GET /read_home

Récupération des informations de toutes les maisons associées à l'utilisateur.

#### Paramètres:

- Token d'authentification (inclus dans l'en-tête)

#### Réponse:

```json
{
  "success": bool,
  "homes": [
    {
      "home_id": int,
      "name": "string",
      "address": "string"
    }
  ]
}
```

---

### POST /add_camera

Ajout d'une nouvelle caméra à une maison.

#### Paramètres:

- `home_id`: (int) ID de la maison
- `camera_name`: (str) Nom de la caméra
- `camera_ip`: (str) Adresse IP de la caméra
- Token d'authentification (inclus dans l'en-tête)

#### Réponse:

```json
{
  "success": bool,
  "message": "string"
}
```

---

### POST /alter_camera

Modification des informations d'une caméra existante.

#### Paramètres:

- `camera_id`: (int) ID de la caméra
- `camera_name`: (str) Nouveau nom de la caméra (optionnel)
- `camera_ip`: (str) Nouvelle adresse IP (optionnel)
- Token d'authentification (inclus dans l'en-tête)

#### Réponse:

```json
{
  "success": bool,
  "message": "string"
}
```

---

### POST /remove_camera

Suppression d'une caméra.

#### Paramètres:

- `camera_id`: (int) ID de la caméra à supprimer
- Token d'authentification (inclus dans l'en-tête)

#### Réponse:

```json
{
  "success": bool,
  "message": "string"
}
```

---

### POST /add_home_member

Ajout d'un nouveau membre à une maison.

#### Paramètres:

- `home_id`: (int) ID de la maison
- `member_name`: (str) Nom du membre
- `photo`: (file) Photo du membre (format image)
- Token d'authentification (inclus dans l'en-tête)

#### Réponse:

```json
{
  "success": bool,
  "message": "string"
}
```

---

### POST /alter_home_member

Modification des informations d'un membre de la maison.

#### Paramètres:

- `member_id`: (int) ID du membre
- `member_name`: (str) Nouveau nom (optionnel)
- `photo`: (file) Nouvelle photo du membre (optionnel)
- Token d'authentification (inclus dans l'en-tête)

#### Réponse:

```json
{
  "success": bool,
  "message": "string"
}
```

---

### POST /remove_home_member

Suppression d'un membre de la maison.

#### Paramètres:

- `member_id`: (int) ID du membre à supprimer
- Token d'authentification (inclus dans l'en-tête)

#### Réponse:

```json
{
  "success": bool,
  "message": "string"
}
```

---

### GET /read_home_member

Récupération des informations de tous les membres d'une maison.

#### Paramètres:

- Token d'authentification (inclus dans l'en-tête)

#### Réponse:

```json
{
  "success": bool,
  "members": [
    {
      "member_id": int,
      "member_name": "string",
      "photo_url": "string"
    }
  ]
}
```

---

### GET /handle_video_feed/<camera_id>

Récupération du flux vidéo d'une caméra.

#### Paramètres:

- `camera_id`: (int) ID de la caméra
- Token d'authentification (inclus dans l'en-tête)

#### Réponse:

Flux vidéo en direct.

---

## Notes

- Toutes les requêtes nécessitent un token d'authentification dans l'en-tête sauf indication contraire.
- Le format des fichiers envoyés pour les images doit être compatible avec le backend (JPEG, PNG, etc.).
- Assurez-vous que les caméras ont une connexion stable pour le bon fonctionnement du flux vidéo.
