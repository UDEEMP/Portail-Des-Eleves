# Portail-Des-Eleves
Code source du Portail des élèves de l'ensmp

## Instructions

Pas mal de choses sont faites pour simplifier la vie sur Linux/OSX, pour Windows faudra se démerdouiller tout seul.

* Cloner le portail en local
`git clone https://github.com/UDEEMP/Portail-Des-Eleves/`
* Installer un environnement de serveur local (MAMP sous OSX, LAMP sous Linux par exemple)
* Démarrer le serveur MySQL et créer une base de donnée à partir du fichier `portail-database.sql
* Lancer le fichier `configure.py` avec Python 3.5
À partir de là, un environnement virtuel avec toutes les dépendances nécessaires va s'installer, et vous pourrez lancer le portail en local avec la commande
`python manage.py runserver`
