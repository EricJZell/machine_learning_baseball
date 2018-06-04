# This script is used to seed the 'games' table in the mlb_stats.db database
import sqlite3
import json

conn = sqlite3.connect('mlb_stats.db')
c = conn.cursor()
print("Opened database successfully")

# Before executing this script, create the table in the sqlite3 console with:
# CREATE TABLE games (GameID INTEGER PRIMARY KEY NOT NULL, Day DATETIME, DateTime DATETIME, AwayTeamID INTEGER, HomeTeamID INTEGER, AwayTeamPitcherID INTEGER, HomeTeamPitcherID INTEGER)

# load raw game data from the file 'games.json'
game_data = json.load(open('seed_data_json_files/games.json'))

# Insert records into the games table
for game in game_data:
    if game['DateTime'] is None:
        game['DateTime'] = game['Day']

    c.execute("INSERT INTO games (GameID,Day,DateTime,AwayTeamID,HomeTeamID) VALUES (?,?,?,?,?)",(
        game['GameID'], game['Day'], game['DateTime'], game['AwayTeamID'], game['HomeTeamID']
    ))


conn.commit()
conn.close
print("Closed database successfull")
