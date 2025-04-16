
# Web Service - myapp

## 🌍 Présentation

Ce projet est une application web construite avec **Flask** et **MySQL**, **dockerisée** pour une utilisation facile. Il offre diverses fonctionnalités, telles que :

- Calculatrice via API
- Authentification et enregistrement TOTP (Time-based One-Time Password)
- Commerce en ligne avec gestion des stocks et du panier

---

## 🚀 Installation & Déploiement

### Prérequis

Avant de commencer, assurez-vous d'avoir **Docker** et **Docker Compose** installés sur votre machine.

### Étapes de déploiement

1. **Clonez le repository** :

    ```bash
    git clone https://github.com/Warziz/SimpleWebService.git
    cd SimpleWebService
    ```

2. **Construisez et lancez les services** :

    ```bash
    docker-compose up --build -d
    ```

    Vous devriez voir quelque chose comme ça dans votre terminal :

    ```bash
    Creating mysql1 ... done
    Creating flask-app ... done
    ```

3. **Vérifiez l’état des containers** :

    ```bash
    docker ps
    ```

    Vous devriez voir deux containers en cours d'exécution :

    ```bash
    CONTAINER ID   IMAGE                COMMAND                  CREATED          STATUS                    PORTS                                       NAMES
    6f6dcbfd032a   web_service_web      "gunicorn -b 0.0.0.0…"   5 seconds ago    Up 4 seconds              0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   flask-app
    5f6df19ab149   mysql/mysql-server   "/entrypoint.sh mysq…"   25 seconds ago   Up 25 seconds (healthy)   3306/tcp, 33060-33061/tcp                   mysql1
    ```

4. **Accédez à l'application**  
    Vous pouvez maintenant accéder à l’application via l’URL suivante (par défaut) :

    [http://localhost:8000/](http://localhost:8000/)

---

## 🔐 Sécurité

/!\ **ATTENTION** /!\  
Les mots de passe par défaut sont faibles. Il est **fortement recommandé** de les changer avant de déployer en production.

### 📜 Pour modifier les mots de passe :

1. Ouvrez le fichier `docker-compose.yml`.
2. Allez dans la section `web-environment`.
3. Modifiez les variables d'environnement pour renforcer la sécurité.
4. N'oubliez pas de modifier les variables correspondantes dans la section `db-environment`.

---

## 🛠️ Fonctionnalités du Service Web

Voici les différentes API que vous pouvez tester avec cette application :

### 1. Calculatrice

Effectuez des calculs simples via l'API :

- **Exemple 1 : Addition**
  
    ```bash
    curl http://localhost:8000/calculatrice?expr=5+%2B+8
    ```

- **Exemple 2 : Multiplication**
  
    ```bash
    curl http://localhost:8000/calculatrice?expr=5*8
    ```

### 2. Enregistrement et Authentification (TOTP)

#### Enregistrement d'un utilisateur

```bash
curl -X PUT http://localhost:8000/totp/register -d '{"secret":"AAAAAAAA", "user":"robert"}'
```

#### Authentification d'un utilisateur

```bash
curl -X POST http://localhost:8000/totp/auth -H "X-User: robert" -d '{"password":"599e79061e8cc3b4"}'
```

---

### 3. Commerce en ligne

#### Ajouter des stocks

```bash
curl -X PUT http://localhost:8000/shop/stock -d '[{"id": 123, "amount": 4}, {"id": 64, "amount": 1}]'
```

#### Modifier le panier

```bash
curl -X POST http://localhost:8000/shop/basket -d '{"id": 214124, "basket": [{"id": 123, "amount": 5}, {"id": 64, "amount": 2}]}'
```

#### Visualiser les stocks

```bash
curl -X GET http://localhost:8000/shop/stock
```

#### Confirmer la commande

```bash
curl -X POST http://localhost:8000/shop/checkout -d '{"id": 214124}'
```

---

## ⚙️ Configuration

Les principales variables d'environnement sont définies dans le fichier `docker-compose.yml`. Voici les principales options à personnaliser :


**Attention**, si vous êtes en mode **testing**, aucun Docker n'est déployé (et donc pas de BDD). Il vous faudra un fichier .env avec les variables ci-dessous !

### Variables pour l'application web :

- `GPG_PASSPHRASE`: La phrase secrète pour l'encryption/décryption.
- `DB_HOST`: L'adresse de la base de données (habituellement `db` si vous utilisez Docker Compose).
- `DB_USER`: L'utilisateur de la base de données.
- `DB_PASSWORD`: Le mot de passe de l'utilisateur de la base de données.
- `DB_NAME`: Le nom de la base de données.
- `CONFIG_TYPE`: Lance l'application en mode testing ou production

### Variables pour la base de données (MySQL) :

- `MYSQL_ROOT_PASSWORD`: Le mot de passe pour l'utilisateur `root` de MySQL.
- `MYSQL_USER`: L'utilisateur de la base de données.
- `MYSQL_PASSWORD`: Le mot de passe de cet utilisateur.
- `MYSQL_DATABASE`: Le nom de la base de données à créer à l'initialisation.



### 🚀 Bonne utilisation !