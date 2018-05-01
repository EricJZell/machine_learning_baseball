from flask import Flask, flash, redirect, render_template, request, session, abort
from helpers import upcoming_games
import sqlite3
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

conn = sqlite3.connect('mlb_stats.db')
print("Opened database successfully")

@app.route("/")
def index():
    return render_template("index.html", name="Eric", upcoming_games=upcoming_games())

if __name__ == "__main__":
    app.run()
