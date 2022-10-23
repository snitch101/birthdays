import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

#day variable
DAYS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"
]

MONTHS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        #validate submition
        name = request.form.get("name")
        day = request.form.get("day")
        month = request.form.get("month")
        id = request.form.get("id")
        if id:
            db.execute("DELETE FROM birthdays WHERE id = ?", id)
            birthdays = db.execute("SELECT * FROM birthdays")
            return render_template("index.html", message="Deleted", birthdays=birthdays, days=DAYS, months=MONTHS)
        elif not name or day not in DAYS or month not in MONTHS:
            birthdays = db.execute("SELECT * FROM birthdays")
            return render_template("index.html", message="Missing Info", birthdays=birthdays, days=DAYS, months=MONTHS)
        elif name and day in DAYS and month in MONTHS and not id:
            db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)
            birthdays = db.execute("SELECT * FROM birthdays")
            return render_template("index.html", message="Success", birthdays=birthdays, days=DAYS, months=MONTHS)



    else:

        # TODO: Display the entries in the database on index.html
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", message="", birthdays=birthdays, days=DAYS, months=MONTHS)


