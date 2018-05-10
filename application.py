from flask import Flask, flash, redirect, render_template, request, session, abort
from helpers import upcoming_games
from datetime import date, timedelta, datetime
import sqlite3
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
@app.route("/<day>")
def index(day=str(date.today())):
    date_object = datetime.strptime(day, '%Y-%m-%d')
    next_date_object = date_object + timedelta(days=1)
    next_day = datetime.strftime(next_date_object, '%Y-%m-%d')
    previous_date_object = date_object - timedelta(days=1)
    previous_day = datetime.strftime(previous_date_object, '%Y-%m-%d')
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
        "ORDER BY DateTime ASC",([day]))
    games = cur.fetchall()

    return render_template("index.html", day=day, next_day=next_day, previous_day=previous_day,
        games=games, datetime=datetime)


@app.route('/game/<int:game_id>', methods=["GET", "POST"])
def game(game_id):
    con = sqlite3.connect('mlb_stats.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT GameID, DateTime, "
        "HomeTeam.WikipediaLogoUrl as HomeTeamLogo, HomeTeam.Name as HomeTeamName, HomeTeam.TeamID as HomeTeamID, "
        "AwayTeam.WikipediaLogoUrl as AwayTeamLogo, AwayTeam.Name as AwayTeamName, AwayTeam.TeamID as AwayTeamID "
        "FROM games "
        "JOIN Teams as HomeTeam ON HomeTeamID = HomeTeam.TeamID "
        "JOIN Teams as AwayTeam ON AwayTeamID = AwayTeam.TeamID "
        "WHERE GameID=?",([game_id]))
    game = cur.fetchone()

    cur.execute("SELECT DISTINCT PlayerID, Name FROM players "
        "JOIN matchups ON PlayerID=matchups.PitcherID "
        "WHERE Position='SP' AND TeamID=?", ([game["HomeTeamID"]]))
    home_pitchers = cur.fetchall()

    cur.execute("SELECT DISTINCT PlayerID, Name FROM players "
        "JOIN matchups ON PlayerID=matchups.PitcherID "
        "WHERE Position='SP' AND TeamID=?", ([game["AwayTeamID"]]))
    away_pitchers = cur.fetchall()
    matchups = {}

    if request.method == "POST":
        away_pitcher_id = request.form.get("away-pitcher")
        home_pitcher_id = request.form.get("home-pitcher")
        cur.execute("SELECT BatterID, players.Name AS Batter, \"" + away_pitcher_id + "\" AS OPS "
            "FROM matchup_predictions "
            "JOIN players ON players.PlayerID=BatterID "
            "WHERE players.TeamID=? ORDER BY OPS DESC", ([game["HomeTeamID"]]))
        matchups["away_pitcher_matchups"] = cur.fetchall()
        cur.execute("SELECT BatterID, players.Name AS Batter, \"" + home_pitcher_id + "\" AS OPS "
            "FROM matchup_predictions "
            "JOIN players ON players.PlayerID=BatterID "
            "WHERE players.TeamID=? ORDER BY OPS DESC", ([game["AwayTeamID"]]))
        matchups["home_pitcher_matchups"] = cur.fetchall()

    return render_template("game.html", game=game, home_pitchers=home_pitchers, away_pitchers=away_pitchers,
        datetime=datetime, matchups=matchups)

if __name__ == "__main__":
    app.run()
