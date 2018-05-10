# This file contains helper functions for querying the mlb_stats.db database
import sqlite3

def get_games(day):
    """ Query the mlb_stats.db database for games on a given day """
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
    con.close()
    return games

def game_details(cur, game_id):
    """ Query the mlb_stats.db database for game details of a specific game """
    cur.execute("SELECT GameID, DateTime, "
        "HomeTeam.WikipediaLogoUrl as HomeTeamLogo, HomeTeam.Name as HomeTeamName, HomeTeam.TeamID as HomeTeamID, "
        "AwayTeam.WikipediaLogoUrl as AwayTeamLogo, AwayTeam.Name as AwayTeamName, AwayTeam.TeamID as AwayTeamID "
        "FROM games "
        "JOIN Teams as HomeTeam ON HomeTeamID = HomeTeam.TeamID "
        "JOIN Teams as AwayTeam ON AwayTeamID = AwayTeam.TeamID "
        "WHERE GameID=?",([game_id]))
    return cur.fetchone()

def team_pitchers(cur, team_id):
    """ Query the mlb_stats.db database for all the starting pitchers from a given team """
    cur.execute("SELECT DISTINCT PlayerID, Name FROM players "
        "JOIN matchups ON PlayerID=matchups.PitcherID "
        "WHERE Position='SP' AND TeamID=?", ([team_id]))
    return cur.fetchall()

def pitcher_name(cur, pitcher_id):
    """ Given a pitcher's PlayerID, return the pitcher's name """
    cur.execute("SELECT Name FROM players WHERE PlayerID=?", ([pitcher_id]))
    pitcher = cur.fetchone()
    return pitcher["Name"]

def matchup_predictions(cur, pitcher_id, opponent_id):
    """ Query mlb_stats.db database for matchup predictions of a given pitcher vs a given opponent """
    cur.execute("SELECT BatterID, players.Name AS Batter, \"" + pitcher_id + "\" AS OPS "
        "FROM matchup_predictions "
        "JOIN players ON players.PlayerID=BatterID "
        "WHERE players.TeamID=? ORDER BY OPS DESC", ([opponent_id]))
    return cur.fetchall()
