Projet Web Service - Hichem & Dimitri
# Système simple de réservation de billets de train avec Flask

## Dépendences/Exigences (les dernières versions fonctionnent également)

1. Python 3.10.7        --> Allez sur python.org/downloads/ 
2. Flask 2.2.2          --> pip install Flask
3. Flask-Cors 3.0.10    --> devrait s'installer avec Flask mais sinon : pip install -U flask-cors
4. Flask-MySQLdb 1.0.1  --> pip install flask-mysqldb
5. PyMySQL 1.0.2        --> pip install PyMySQL
6. SQLAlchemy 1.4.46    --> pip install SQLAlchemy
7. Pandas 1.5.2         --> pip install pandas

## Installation Docker

1. Clonez le repo

2. Se positionné sur le répertoire racine et lancé : docker-compose up

## Installation Classique

## Installation

1. Clonez le repo

2. Installer les dépendences

## Utilisation
1. Créez votre base de données dans MySQL :
```sql
   CREATE DATABASE web_service;  // avec le nom de la base de données définis dans les paramètres du code
```
2. Créer les table par défaut:
   N'oubliez pas de corrigé le nom d'utilisateur et le mot de passe de la DB dans le fichier.
```
   python database_init.py
```
3. Exécuter l'app:
```
   python App.py
```

## Auto-Evaluation
1. Create REST Train Filtering service B : 5/6

2. Create SOAP Train Booking service A : 0/4

3. Interaction between two services (REST - REST): 2/4

4. Test with Web service Client (instead of using Eclipse's Web service Explorer) (pas en java) : 2/2

5. Work with complex data type (class, table, etc.) : 2/2

6. Work with database (in text file, xml, in mysql, etc.) : 2/2

7. Postman : 2/2

8. OpenAPI : 3/3
