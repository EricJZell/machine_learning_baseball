class UpcomingGame:

    def __init__(self, time, home_team, away_team, home_starter, away_starter):
        self.time = time    # instance variable unique to each instance
        self.home_team = home_team
        self.away_team = away_team
        self.home_starter = home_starter
        self.away_starter = away_starter

def upcoming_games(date):
    # can I use this data? https://swishanalytics.com/optimus/mlb/batter-vs-pitcher-stats?date=2018-04-30
    # use the MLB API available through https://www.mysportsfeeds.com to gather data
    return [
        UpcomingGame("May 16 4:00", "Boston Red Sox", "New York Yankees", "Rick Porcello", "Tanaka"),
        UpcomingGame("May 16 5:00", "Baltimore Orioles", "Toronto Blue Jays", "I dunno", "Someone else"),
        UpcomingGame("May 16 6:00", "New York Mets", "Phillies", "Jake DeGrom", "Pedro")
    ]
