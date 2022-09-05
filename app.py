import os
import calendar

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

MONTHS = [calendar.month_name[i] for i in range(1, 13)]
DAYS = [i for i in range(1, 32)]


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
        # Validate name
        name = request.form.get("name")
        if not name:
            return render_template("status.html", message="Pease fill out a name")

        # Validate month
        month = request.form.get("month")
        if not month:
            return render_template("status.html", message="Pease fill out the date")

        # Validate day
        day = request.form.get("day")
        if not day:
            return render_template("status.html", message="Pease fill out the date")

        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)

        return redirect("/")

    else:
        # TODO: Display the entries in the database on index.html

        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays = birthdays, months=MONTHS, days=DAYS)


@app.route("/remove", methods=["POST"])
def remove():

    id = request.form.get("id")
    db.execute("DELETE FROM birthdays WHERE id = ?", id)
    return redirect("/")
