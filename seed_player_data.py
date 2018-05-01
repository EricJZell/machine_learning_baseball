import sqlite3
import json

conn = sqlite3.connect('mlb_stats.db')
c = conn.cursor()
print("Opened database successfully")

# CREATE TABLE players (PlayerID INTEGER PRIMARY KEY NOT NULL, TeamID INTEGER, PositionCategory TEXT, Position TEXT, FirstName TEXT, LastName TEXT, BatHand TEXT, ThrowHand TEXT);

player_data = json.load(open('players.json'))

for player in player_data:
    if player['Status'] == 'Active':
        c.execute("INSERT INTO players (PlayerID,TeamID,PositionCategory,Position,FirstName,LastName,BatHand,ThrowHand) VALUES (?,?,?,?,?,?,?,?)",(
            player['PlayerID'], player['TeamID'], player['PositionCategory'], player['Position'], player['FirstName'], player['LastName'], player['BatHand'], player['ThrowHand']
        ))


conn.commit()
conn.close
print("Closed database successfull")
