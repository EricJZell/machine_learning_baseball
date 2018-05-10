# This script was used to seed teams table in the mlb_stats.db database
# Raw data was retrieved using https://developer.fantasydata.com/ API
import sqlite3
import json

conn = sqlite3.connect('mlb_stats.db')
c = conn.cursor()
print("Opened database successfully")

# Before executing this script, create the table in the sqlite3 console with:
# CREATE TABLE teams (TeamID INTEGER PRIMARY KEY NOT NULL, Key TEXT, City TEXT, Name TEXT, League TEXT, Division TEXT, PrimaryColor TEXT, SecondaryColor TEXT, WikipediaLogoUrl TEXT);

team_data = json.load(open('teams.json'))

#Insert team date into the teams table in the mlb_stats.db database:
for team in team_data:
    c.execute("INSERT INTO teams (TeamID,Key,City,Name,League,Division,PrimaryColor,SecondaryColor,WikipediaLogoUrl) VALUES (?,?,?,?,?,?,?,?,?)",(
        team['TeamID'], team['Key'], team['City'], team['Name'], team['League'], team['Division'], team['PrimaryColor'], team['SecondaryColor'], team['WikipediaLogoUrl']
    ))


conn.commit()
conn.close
print("Closed database successfull")
