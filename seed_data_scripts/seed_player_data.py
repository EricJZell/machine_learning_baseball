# This script was used to seed players table in the mlb_stats.db database
# Raw data was retrieved using https://developer.fantasydata.com/ API
import sqlite3
import json

conn = sqlite3.connect('mlb_stats.db')
c = conn.cursor()
print("Opened database successfully")

# Before executing this script, create the table in the sqlite3 console with:
# CREATE TABLE players (PlayerID INTEGER PRIMARY KEY NOT NULL, TeamID INTEGER, PositionCategory TEXT, Position TEXT, Name TEXT, BatHand TEXT, ThrowHand TEXT);

# Load raw player data from players.json
player_data = json.load(open('players.json'))

# insert records into players table
for player in player_data:
    if player['Status'] == 'Active':
        c.execute("INSERT INTO players (PlayerID,TeamID,PositionCategory,Position,Name,BatHand,ThrowHand) VALUES (?,?,?,?,?,?,?)",(
            player['PlayerID'], player['TeamID'], player['PositionCategory'], player['Position'], player['FirstName'] + " " + player['LastName'], player['BatHand'], player['ThrowHand']
        ))


conn.commit()
conn.close
print("Closed database successfull")
