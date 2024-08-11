# BACKEND de l'application Sentinelle Security (SS)

## Documentation sur l'utilisation de l'API

| URL                                                                               | Description                                                |                        Résultat                        |
| --------------------------------------------------------------------------------- | ---------------------------------------------------------- | :------------------------------------------------------: |
| /api/get_error/                                                                   | Récupération des erreurs sur la nouvelle page            |                            ~                            |
| /api/get_success/                                                                 | Récupération des succès sur la nouvelle page            |                            ~                            |
| /api/connexion/?email=`<EMAIL>&password=<PASSWORD>`                             | Connexion d'un utilisateur                                 |                                                          |
| /api/deconnexion/                                                                 | Déconnexion de l'utilisateur connecté à la session      |                                                          |
| /api/utilisateur/                                                                 | Récupération des informations de l'utilisateur connecté |                                                          |
| /api/inscription/?`nom=<NOM>&prenom=<PRENOM>&email=<EMAIL>&password=<PASSWORD>` | Inscription d'un propriétaire de maison                   | "success": "L'utilisateur a été créé avec succès." |
