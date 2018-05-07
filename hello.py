from flask import Flask, flash, redirect, render_template, request, session, abort
from helpers import upcoming_games
from datetime import date, timedelta, datetime
import sqlite3
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    con = sqlite3.connect('mlb_stats.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT GameID, DateTime, "
        "HomeTeam.WikipediaLogoUrl as HomeTeamLogo, HomeTeam.Name as HomeTeamName, "
        "AwayTeam.WikipediaLogoUrl as AwayTeamLogo, AwayTeam.Name as AwayTeamName "
        "FROM games "
        "JOIN Teams as HomeTeam ON HomeTeamID = HomeTeam.TeamID "
        "JOIN Teams as AwayTeam ON AwayTeamID = AwayTeam.TeamID "
        "WHERE strftime('%Y-%m-%d', Day)=? "
        "ORDER BY DateTime ASC",([str(date.today())]))
    games = cur.fetchall()
    # for game in games:
    #     game["Time"] = datetime.strptime(game["DateTime"], '%Y-%m-%dT%H:%M:%S').strftime('%-I:%M')
    return render_template("index.html", name="Eric", games=games, datetime=datetime)

@app.route('/game/<int:game_id>')
def game(game_id):
    GameID = game_id
    return render_template("game.html", GameID=GameID)

if __name__ == "__main__":
    app.run()
