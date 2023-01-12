from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from flask_login import (
    LoginManager,
    UserMixin,
    login_required,
    current_user,
    login_user,
    logout_user,
)
import numpy as np

setup = False
app = Flask(__name__)
app.secret_key = "dev"
app.config["MYSQL_HOST"] = "mysql_db"
app.config["MYSQL_USER"] = "admin"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "webservice"
mysql = MySQL(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):

    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(user_id):
    # Charge l'utilisateur à partir de votre base de données
    user = User(user_id)
    return user


############################################################
def valeur_db(dbVarStr, dbName="train", condi=None):
    cursor = mysql.connection.cursor()
    sql = "SELECT " + dbVarStr + " FROM " + dbName
    if condi is not None:
        sql = "SELECT " + dbVarStr + " FROM " + dbName + " WHERE " + condi
    cursor.execute(sql)
    data = cursor.fetchall()
    if len(data) == 1:
        liste = [np.squeeze(data).tolist()]
    else:
        liste = list(set(np.squeeze(data)))

    cursor.close()
    return liste


############################################################


@app.route("/")
def Acceuil():
    # --------
    # 1. Charge la liste des reservations
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM reservation")
    datal1 = cursor.fetchall()
    # 2. Charge la liste des trains
    cursor.execute("SELECT * FROM train")
    datal2 = cursor.fetchall()
    cursor.close()
    return render_template("index.html", reservation=datal1, train=datal2)


############################################################
# Login API
############################################################


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        # Récupérez les données de formulaire soumises
        username = request.form["username"]
        password = request.form["password"]

        # Vérifiez les identifiants de connexion
        if username == "Prevel" and password == "123":
            # Connectez l'utilisateur
            user = User(username)
            login_user(user)
            return redirect("/protected")
        # Affichez un message d'erreur
        flash("Nom de compte ou mot de passe incorrect", "error")
        return redirect(url_for("Acceuil"))
    # Affichez le formulaire de connexion
    return redirect(url_for("Acceuil"))


############################################################
# Logout API
############################################################


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous êtes déconnecté")
    return redirect(url_for("Acceuil"))


############################################################
# Notif login API
############################################################


@app.route("/protected")
@login_required
def protected():
    # Cette route n'est accessible que pour les utilisateurs connectés
    if current_user.is_authenticated:
        # L'utilisateur est connecté, vous pouvez accéder à son ID
        user_id = current_user.id
        message = "Welcome," + str(user_id) + " !"
        flash(message)
    else:
        # L'utilisateur n'est pas connecté, vous ne pouvez pas accéder à son ID
        user_id = None
    return redirect(url_for("Acceuil"))


#############################################################
# Insert API
#############################################################


@app.route("/insert", methods=["POST"])
def insert():
    if request.method == "POST":
        flash("Les données ont été ajoutées avec succès")

        user_id = current_user.id
        Nom = request.form["Nom"]
        date = request.form["date"]
        trainid = request.form["trainid"]
        départ = request.form["Depart_reserv"]
        arrivée = request.form["Arrivee_reserv"]
        quantité = request.form["quantité"]
        prix_tot = request.form["prix_tot"]

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM reservation")
        data = cursor.fetchone()
        Idxmax = data[0] + 1
        mysql.connection.commit()

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO reservation (reservation.index, User, Nom , Date , ID ,depart_reserv , arrivee_reserv ,Quantite, Prix ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (Idxmax, user_id, Nom, date, trainid, départ, arrivée, quantité,
             prix_tot),
        )
        mysql.connection.commit()

        return redirect(url_for("Acceuil"))


##############################################################
# Update API
##############################################################


@app.route("/update", methods=["POST", "GET"])
def update():
    if request.method == "POST":
        data = request.form.to_dict()
        orderID = data["id"]
        Nom = data["Nom"]
        date = data["date"]
        trainid = data["trainid"]
        départ = data["Depart_reserv"]
        arrivée = data["Arrivee_reserv"]
        quantité = data["quantité"]

        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE reservation SET Nom=%s, Date=%s, ID=%s, depart_reserv=%s, arrivee_reserv=%s, Quantite=%s WHERE reservation.index=%s ",
            (Nom, date, trainid, départ, arrivée, quantité, orderID),
        )
        flash("Donné modifié avec succès")
        mysql.connection.commit()
        return redirect(url_for("Acceuil"))


##############################################################
# Delete API
##############################################################


@app.route("/delete/<string:id>", methods=["POST", "GET"])
def delete(id):
    flash("Donnée supprimée avec succès")
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM reservation WHERE reservation.index =%s",
                   (id, ))
    mysql.connection.commit()
    return redirect(url_for("Acceuil"))


##############################################################
# Options de requête
##############################################################


@app.route("/updateDrop/dateSelect")
def update_selectDate():
    # 1. information utilisateur
    select_date = request.args.get("date", type=str)

    #################################
    # 2. requête base de données
    sqlCondition = "Date = '" + select_date + "'"
    dep = valeur_db("Depart", "train", sqlCondition)
    # -----------------------------------
    # 3. Options HTML
    depart_html = '<option value=" "></option>'
    for entry in dep:
        depart_html += '<option value="{}">{}</option>'.format(entry, entry)
    #################################
    return jsonify(depart_option=depart_html)


@app.route("/updateDrop/departSelect")
def update_selectDepart():
    # 1. information utilisateur
    select_date = request.args.get("date", type=str)
    select_depart = request.args.get("select_depart", type=str)
    ##################################
    # 2. requête base de données
    sqlCondition = "Date = '" + select_date + "' AND Depart = '" + select_depart + "'"
    arri = valeur_db("Destination", "train", sqlCondition)
    # -----------------------------------
    # 3. Options HTML
    arrivé_html = '<option value=" "></option>'
    for entry in arri:
        arrivé_html += '<option value="{}">{}</option>'.format(entry, entry)
    ##################################
    return jsonify(
        arrivé_option=arrivé_html
    )  # , train_selected = trainId_html, amountAllow = amount_html) #


@app.route("/updateDrop/arrivéSelect")
def update_selectArrive():
    # 1. information utilisateur
    select_date = request.args.get("date", type=str)
    select_depart = request.args.get("select_depart", type=str)
    select_arrivée = request.args.get("select_arrivée", type=str)
    ##################################
    # 2. requête base de données
    sqlCondition = ("Date = '" + select_date + "' AND Depart = '" +
                    select_depart + "' AND Destination = '" + select_arrivée +
                    "'")
    TrainIDs = valeur_db("ID", "train", sqlCondition)
    ClasseIDs = valeur_db("classe", "train", sqlCondition)
    # -----------------------------------
    # 3. Options HTML
    train_html = '<option value=" "></option>'
    classe_html = '<option value=" "></option>'
    for entry in TrainIDs:
        train_html += '<option value="{}">{}</option>'.format(entry, entry)
    for entry in ClasseIDs:
        classe_html += '<option value="{}">{}</option>'.format(entry, entry)
    ##################################
    return jsonify(train_opt=train_html, classe_opt=classe_html)


@app.route("/updateDrop/trainSelect")
def update_seleTrainId():
    ###### update de la quantité et du prix
    # 1. information utilisateur
    select_date = request.args.get("date", type=str)
    select_depart = request.args.get("select_depart", type=str)
    select_arrivée = request.args.get("select_arrivée", type=str)
    select_trainid = request.args.get("trainid", type=str)
    select_quantite = request.args.get("quantité", type=str)
    select_quantite = int(
        select_quantite) if select_quantite is not None else 1
    # ########## 2. Requête pour les places ##########
    sqlCondi1 = ("Date = '" + select_date + "' AND Depart = '" +
                 select_depart + "' AND Destination = '" + select_arrivée +
                 "' AND ID='" + select_trainid + "'")
    place_restante = valeur_db("Places", "train", sqlCondi1)[0]
    sqlCondi2 = ("Date = '" + select_date + "' AND ID ='" + select_trainid +
                 "' AND Depart_reserv = '" + select_depart +
                 "' AND arrivee_reserv ='" + select_arrivée + "'")
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT SUM(Quantite) FROM reservation WHERE " + sqlCondi2)

    reservation_data = cursor.fetchone()[0]
    reservation_data = reservation_data if reservation_data is not None else 0
    mysql.connection.commit()

    quantite_max = 0
    quantite_dispo = 0
    if place_restante is not None:
        quantite_max = max(place_restante - reservation_data, 0)
        quantite_dispo = min(int(select_quantite), quantite_max)
    print(place_restante, quantite_dispo, reservation_data, select_quantite)
    # ########## 3. Calcul du prix ##########
    ville = ["paris", "marseille", "lyon", "nante"]

    prixParVille = 100
    distance = abs(ville.index(select_depart) - ville.index(select_arrivée))
    prix = max(distance * quantite_dispo * prixParVille, 0)
    #########################################
    return jsonify(quantite_limit="{}".format(quantite_max),
                   affiche_prix="{}".format(prix))


@app.route("/updateDrop/quantiteSelect")
def update_seleAmount():
    # select
    select_date = request.args.get("date", type=str)
    select_trainid = request.args.get("trainid", type=str)
    select_depart = request.args.get("select_depart", type=str)
    select_arrivée = request.args.get("select_arrivée", type=str)
    select_quantite = request.args.get("quantité", type=str)
    select_quantite = int(
        select_quantite) if select_quantite is not None else 1
    ###################################################
    sqlCondi1 = ("Date = '" + select_date + "' AND Depart = '" +
                 select_depart + "' AND Destination = '" + select_arrivée +
                 "' AND ID='" + select_trainid + "'")
    place_restante = valeur_db("Places", "train", sqlCondi1)[0]
    sqlCondi2 = ("Date = '" + select_date + "' AND ID ='" + select_trainid +
                 "' AND Depart_reserv = '" + select_depart +
                 "' AND arrivee_reserv ='" + select_arrivée + "'")
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT SUM(Quantite) FROM reservation WHERE " + sqlCondi2)

    reservation_data = cursor.fetchone()[0]
    reservation_data = reservation_data if reservation_data is not None else 0
    mysql.connection.commit()

    quantite_max = 0
    quantite_dispo = 0
    if place_restante is not None:
        quantite_max = max(place_restante - reservation_data, 0)
        quantite_dispo = min(int(select_quantite), quantite_max)

    #############################################################
    ville = ["paris", "marseille", "lyon", "nante"]
    prixParVille = 100
    distance = abs(ville.index(select_depart) - ville.index(select_arrivée))
    prix = max(distance * quantite_dispo * prixParVille, 0)

    return jsonify(affiche_prix="{}".format(prix))


@app.route("/updateDrop/classeSelect")
def update_seleClasse():
    # select
    select_date = request.args.get("date", type=str)
    select_trainid = request.args.get("trainid", type=str)
    select_depart = request.args.get("select_depart", type=str)
    select_arrivée = request.args.get("select_arrivée", type=str)
    select_quantite = request.args.get("quantité", type=str)
    select_quantite = int(
        select_quantite) if select_quantite is not None else 1
    ###################################################
    sqlCondi1 = ("Date = '" + select_date + "' AND Depart = '" +
                 select_depart + "' AND Destination = '" + select_arrivée +
                 "' AND ID='" + select_trainid + "'")
    classe_prix = valeur_db("classe", "train", sqlCondi1)[0]
    prix_classe = 1
    #############################################################
    if classe_prix == "Standard":
        prix_classe = 1
    elif classe_prix == "affaire":
        prix_classe = 2
    elif classe_prix == "premiere":
        prix_classe = 3
    prixParVille = 100
    prix = prix_classe * prixParVille * select_quantite

    return jsonify(affiche_prix="{}".format(prix))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
