# Oblyk To-Do Exporter

Cet outil permet de générer un tableau *.ods (OpenDocument Spreadsheet), prêt à être imprimé, avec une liste de voies à travailler pour une salle Climb Up (d'autres salles utilisant Oblyk peuvent être compatibles, mais cela n'a pas été testé), à partir de ton historique de grimpe et des voies actuellement disponibles.

Concrètement, l'outil va croiser les voies actuellement disponibles de ta salle avec celles déjà effectuées, en tête et/ou en moulinette, afin de générer deux listes de voies à travailler - une pour la grimpe en moulinette et une pour la grimpe en tête, en fonction de ton historique de grimpe et des plages de cotation choisies (indépendantes pour chacune des feuilles).

La liste générée va trier tes voies par espace, puis par secteur, cotation et couleur des prises (du plus facile au plus difficile).

Enfin, pour chaque voie, il sera mentionné si c'est une voie que tu as déjà travaillé (projet) ou, pour les voies à faire en tête, si tu l'as déjà validée en moulinette (moul' ok). Et, par défaut, les 15% des voies les plus vieilles de chaque secteur seront en rouge, et les 15% suivants en orange, afin de signaler les voies susceptibles d'être démontées prochainement.

## Prérequis

* Un compte Oblyk
* Python 3.11 ou plus récent
* Les dépendances Python du projet installées

## Installation

1. Télécharge le projet en [cliquant ici](https://github.com/arusabu/Oblyk-To-Do-Exporter/archive/refs/heads/master.zip).
2. Extrait le contenu du *.zip où tu le souhaites.
3. À la racine de l'outil (\Oblyk-To-Do-Exporter-master\), ouvre un terminal (sous Windows, clic droit, "Ouvrir dans le terminal")
![Ouverture du terminal](img/01.png)
4. Saisis la commande suivante :

```bash
pip install -r requirements.txt
```
![Installation des dépendances](img/02.png)

Tu devrais obtenir quelque chose de semblable à :
![Dépendances installées](img/03.png)

## Configuration

### 1. Créer le fichier `.env`

Copie `.env.example` puis renomme la copie en `.env`.

Le fichier `.env` doit contenir tes identifiants Oblyk :

```env
OBLYK_EMAIL=ton_adresse_email
OBLYK_PASSWORD=ton_mot_de_passe
```
Tes identifiants sont uniquement stockés sur ton ordinateur. Ils servent uniquement à t'authentifier auprès d'Oblyk. Aucune autre utilisation n'en est faite.

### 2. Créer  `config.toml`

Copie `config.toml.example` puis renomme la copie en `config.toml`.

Le fichier `config.toml` sert à régler :
- l’identifiant de salle ;
- les plages de cotation.

Exemple :

```toml
[gym]
id = 115

[top_rope]
grade_min = "5c"
grade_max = "6c"

[lead]
grade_min = "5b"
grade_max = "6b"
```

#### Champs à adapter

* `gym.id` : l’identifiant de ta salle sur Oblyk.
En fin de `config.toml`, j'ai indiqué la totalité des id des Climb Up proposant de la voie à date.
Pour trouver cet id, il suffit de se rendre sur sa salle dans Oblyk et regarder dans la barre d'adresse :
![Gym ID](img/04.png)
https://oblyk.org/gyms/115/climb-up-aix-bouc-bel-air

L'ID de Climb Up Bouc-Bel-Air est **115**.

-  `top_rope.grade_min` / `top_rope.grade_max` : plage de cotation pour la feuille Moulinette.
-  `lead.grade_min` / `lead.grade_max` : plage de cotation pour la feuille Tête.

## Utilisation

Lance le script principal :

```bash
python main.py
```
![Run main.py](img/05.png)

Le programme :

1. se connecte à Oblyk ;
2. récupère les espaces et les voies ;
3. détermine les voies à afficher dans les listes ;
4. génère un fichier ODS dans le dossier `output/`.

![output console](img/06.png)

## Résultat

Le fichier généré contient deux feuilles :

* **Moulinette**
* **Tête**

Chaque feuille regroupe les voies à travailler selon la plage de cotation choisie.

![Top Rope](img/07.png) ![Lead](img/08.png)

## Dépannage

### Impossible d'activer l'environnement virtuel

Si PowerShell affiche un message indiquant que l'exécution des scripts est désactivée, exécute la commande suivante :
```bash
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
Confirme en répondant O (Oui), puis active à nouveau l'environnement virtuel :
```bash
.venv\Scripts\Activate.ps1
```
Cette modification n'affecte que ton compte utilisateur.

### Erreur de connexion

Vérifie que :

* ton adresse email est correcte ;
* ton mot de passe est correct ;
* ta connexion Internet fonctionne ;
* les informations du fichier `.env` sont bien enregistrées.

### Aucun fichier ODS généré

Vérifie que :

* `config.toml` existe ;
* `gym.id` est correct ;
* les plages de cotation sont compatibles avec les grades présents dans la salle.

### Les voies attendues n’apparaissent pas

Vérifie que :

* la salle Oblyk est la bonne ;
* les grades saisis dans `config.toml` existent bien dans la salle.

### Besoin d'aide ?

Si tu rencontres un problème, constates un bug ou souhaites proposer une amélioration, n'hésite pas à ouvrir une Issue sur GitHub.

Les suggestions sont les bienvenues !

Si tu souhaites contribuer directement au projet, les Pull Requests sont également les bienvenues.