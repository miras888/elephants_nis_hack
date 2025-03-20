import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///elephants.db")
 
@app.route("/login", methods = ["GET", "POST"])
def login():
     
    session.clear()

    
    if request.method == "POST":

        
        if not request.form.get("mail"):
            return apology("must provide mail", 403)

        
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        

        
        rows = db.execute("SELECT * FROM user WHERE email = ?", request.form.get("mail"))

        
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid mail and/or password", 403)

        
        session["user_id"] = rows[0]["id"]

        
        return redirect("/")

    
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    
    session.clear()

    
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":
        mail = request.form.get("mail")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not mail:
            return apology("Type mail")

        elif not password:
            return apology("Type Password")

        elif not confirmation:
            return apology("Type Confirmation")
     
        elif password != confirmation:
            return apology("password don't Match")

        rows = db.execute("SELECT * FROM user WHERE email = ?", mail)

        if len(rows) > 0:
            return apology("mail already exists")
        db.execute("INSERT INTO user (email, hash) VALUES (?, ?)", mail, generate_password_hash(password))

        rows1 = db.execute("SELECT * FROM user WHERE email = ?", request.form.get("mail"))

        session["user_id"] = rows1[0]["id"]

        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template("index.html")

@app.route("/get_locations", methods=["GET"])
def get_locations():
    """Fetch locations from the database"""
    locations = db.execute("SELECT name, lon, lat, reserve, productionperday, yearinreserve, img FROM locations")
    return jsonify(locations)

@app.route("/globe", methods=["GET", "POST"])
@login_required
def globe():
    oilfield = db.execute("SELECT * FROM oilfield")
    return render_template("globe.html", oilfield=oilfield)

@app.route("/drone", methods=["GET", "POST"])
@login_required
def hard():
    return render_template("hardware.html")
