import sqlite3
import json

conn = sqlite3.connect('mlb_stats.db')
c = conn.cursor()
print("Opened database successfully")


# CREATE TABLE teams (TeamID INTEGER PRIMARY KEY NOT NULL, Key TEXT, City TEXT, Name TEXT, League TEXT, Division TEXT, PrimaryColor TEXT, SecondaryColor TEXT, WikipediaLogoUrl TEXT);

team_data = json.load(open('teams.json'))

for team in team_data:
    c.execute("INSERT INTO teams (TeamID,Key,City,Name,League,Division,PrimaryColor,SecondaryColor,WikipediaLogoUrl) VALUES (?,?,?,?,?,?,?,?,?)",(
        team['TeamID'], team['Key'], team['City'], team['Name'], team['League'], team['Division'], team['PrimaryColor'], team['SecondaryColor'], team['WikipediaLogoUrl']
    ))


conn.commit()
conn.close
print("Closed database successfull")
