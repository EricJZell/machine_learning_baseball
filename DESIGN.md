# Machine Learning Baseball Design Document
# Eric Zell CS50 Spring 2018 Final Project

Machine Learning Baseball is a web application built with python and Flask. It uses machine learning techniques to
predict how well Major League Baseball patters will perform against any Major League Baseball pitcher. The basic principle
is this:

If Batter A performs well against Pitcher #1, and if Pitcher #1 is very similar to Pitcher #2, then we can
predict that Batter A will perform well against Pitcher #2.

Similarly, if Batter A is very similar to Batter B, and Batter B performs very well against Pitcher #3, then we
can predict Batter A will perform well against Pitcher #3.

To implement this, the first step was to collect all of the requried data. Major League Baseball data for Teams, Players,
and Games is freely available from the fantasydata.com web API. The fantasydata.com API returns the data in json format.
Data for every major league game, team and player was collected up front, and used to seed an SQL database.
The database was seedup up front so that when a user visits the page, all the info can be queried from the database
instead of relying on API calls for every page view.

The pitcher vs. batter matchup statistics were harder to come by. SwishAnalytics.com displays all the daily pitcher vs.
batter matchup statistics, but do not offer an API for this data. Using some jQuery in the JavaScript console, the
required data was collected and saved in JSON format. From this JSON, a `matchups` table was created in the database
with three columns: `BatterID`, `PitcherID`, and `OPS`. However, the `matchups` table did not contain data for every
possible combination of a batter vs. a pitcher. That is where machine learning techniques come in.

Using the python libraries `numpy`, `scipy`, and `pandas`, the three column `matchups` table can be converted to a matrix
holding predicted OPS values for every batter vs. every pitcher.
First, using `pandas` pivot table function, a matrix was generated with cells to hold OPS data
for every possible batter vs. pitcher combination. However, only cells for combinations existing in the `matchups` table
were populated. This matrix can be viewed in `machine_learning_files/initial_matchups.csv`
It is clear that this is initially a very sparse matrix.

However using a process called Low Rank Matrix Factorization, this sparse matrix can be fully populated
with predicted OPS values for every matchup, based solely on the existing values.  Tools to perform
Low Rank Matrix Factorization are provided by https://www.lynda.com/Data-Science-tutorials/Machine-Learning-Fundamentals-Learning-Make-Recommendations/563030-2.html
and are in the `machine_learning_files/matrix_factorization_utilities.py` file.

Performing Low Rank Matrix Factorization on the sparse initial matchups matrix produced the fully populated
matrix of predicted OPS values seen at `machine_learning_files/matchup_predictions.csv`

This fully populated prediction matrix was converted to a SQL table called `matchup_predictions` for
ease and performance of querying data from within the flask application.

From within the flask application, in `application.py` the sqlite3 library is used to query game,
player, and predicted_matchup data for any user selected combination of pitcher vs. opponent.
