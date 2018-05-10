# Eric Zell CS50 final project: machine_learning_baseball
from flask import Flask, flash, redirect, render_template, request, session, abort
from helpers import get_games, game_details, team_pitchers, pitcher_name, matchup_predictions
from datetime import date, timedelta, datetime
import sqlite3
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
@app.route("/<day>")
def index(day=str(date.today())):
    """ List all of the games for a given day on the page """
    # Convert the day to a datetime object so we can add and subtract 1 day
    # In order to create links to the next and previous day's games:
    date_object = datetime.strptime(day, '%Y-%m-%d')
    next_date_object = date_object + timedelta(days=1)
    next_day = datetime.strftime(next_date_object, '%Y-%m-%d')
    previous_date_object = date_object - timedelta(days=1)
    previous_day = datetime.strftime(previous_date_object, '%Y-%m-%d')
    # Get all the games for the selected day from the database:
    games = get_games(day)
    return render_template("index.html", day=day, next_day=next_day, previous_day=previous_day,
        games=games, datetime=datetime)


@app.route('/game/<int:game_id>', methods=["GET", "POST"])
def game(game_id):
    """
        List single game details, with a form to select pitchers to analyze matchups
        If pitchers have been selected, display the predicted matchups
    """
    con = sqlite3.connect('mlb_stats.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    # Query the database for game details:
    game = game_details(cur, game_id)

    # Get a list of home team and away team pitchers
    home_pitchers = team_pitchers(cur, game["HomeTeamID"])
    away_pitchers = team_pitchers(cur, game["AwayTeamID"])

    # Only populate the matchups and selected_pitchers dictionaries if the user
    # has selected pitchers to analyze
    matchups = {}
    selected_pitchers = {}

    if request.method == "POST":
        # get selected pitcher_ids from the form
        away_pitcher_id = request.form.get("away-pitcher")
        home_pitcher_id = request.form.get("home-pitcher")

        # query database for the pitcher's names
        selected_pitchers["away"] = pitcher_name(cur, away_pitcher_id)
        selected_pitchers["home"] = pitcher_name(cur, home_pitcher_id)

        # query database for the pitchers' matchup predictions against the opponent
        matchups["away_pitcher_matchups"] = matchup_predictions(cur, away_pitcher_id, game["HomeTeamID"])
        matchups["home_pitcher_matchups"] = matchup_predictions(cur, home_pitcher_id, game["AwayTeamID"])

    con.close()
    return render_template("game.html", game=game, home_pitchers=home_pitchers, away_pitchers=away_pitchers,
        datetime=datetime, matchups=matchups, selected_pitchers=selected_pitchers)

if __name__ == "__main__":
    app.run()
