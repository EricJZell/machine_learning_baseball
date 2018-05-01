import sqlite3
import json

conn = sqlite3.connect('mlb_stats.db')
c = conn.cursor()
print("Opened database successfully")


# CREATE TABLE games (GameID INTEGER PRIMARY KEY NOT NULL, Day DATETIME, DateTime DATETIME, AwayTeamID INTEGER, HomeTeamID INTEGER, AwayTeamPitcherID INTEGER, HomeTeamPitcherID INTEGER)

game_data = json.load(open('games.json'))

for game in game_data:
    c.execute("INSERT INTO games (GameID,Day,DateTime,AwayTeamID,HomeTeamID) VALUES (?,?,?,?,?)",(
        game['GameID'], game['Day'], game['DateTime'], game['AwayTeamID'], game['HomeTeamID']
    ))


conn.commit()
conn.close
print("Closed database successfull")
