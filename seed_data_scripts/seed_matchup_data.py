import sqlite3
import json
import os

con = sqlite3.connect('mlb_stats.db')
con.row_factory = sqlite3.Row
cur = con.cursor()
print("Opened database successfully")


# AT https://swishanalytics.com/optimus/mlb/batter-vs-pitcher-stats
# rows = $("#stat-table tbody tr")
# data = $.map(rows, function(e) { return {batter: $(e).find('td span.batter-name').text(), pitcher: $(e).find('td span.pitcher-name').text(), plate_appearances: $(e).find('td:nth-child(3)').text(), avg: $(e).find('td:nth-child(12)').text(), obp: $(e).find('td:nth-child(13)').text(), slg: $(e).find('td:nth-child(14)').text()}})


# CREATE TABLE matchups (MatchupID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, BatterID INTEGER, PitcherID INTEGER, OPS NUMERIC)

for file in os.listdir("./matchup_data"):
    matchup_data = json.load(open(os.path.join("./matchup_data", file)))
    for matchup in matchup_data:
        if int(matchup['plate_appearances']) > 4:
            batter = matchup['batter'].strip()
            cur.execute("SELECT PlayerID FROM players WHERE Name=?", ([batter]))
            batter_record = cur.fetchone()
            pitcher = matchup['pitcher'].strip()
            cur.execute("SELECT PlayerID FROM players WHERE Name=?", ([pitcher]))
            pitcher_record = cur.fetchone()
            if batter_record and pitcher_record:
                cur.execute("DELETE FROM matchups WHERE BatterID=? AND PitcherID=?", ([batter_record['PlayerID'], pitcher_record['PlayerID']]))
                ops = float(matchup['obp']) + float(matchup['slg'])
                cur.execute("INSERT INTO matchups (BatterID,PitcherID,OPS) VALUES (?,?,?)",(
                    batter_record['PlayerID'], pitcher_record['PlayerID'], ops
                ))

con.commit()
con.close
print("Closed database successfull")
