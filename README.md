# Machine Learning Baseball
# Eric Zell CS50 Final Project Spring 2018

Machine Learing Baseball is a web application that a user can visit to get predicted pitcher vs. batter
mathup statistics for any Major League Baseball game on any given day. It is built with python and flask,
so it can be ran directly from the CS50 IDE by executing `$ flask run`

The application is now also deployed at https://machine-learning-baseball.herokuapp.com/2018-06-13

The landing page, or the index page, displays a list of major league baseball games to be played for
the current day. The day can be changed either by clicking the `Next Day` or `Previous Day` links, or by
entering a date as a paramter in the URL bar.

To analyze the batter vs. pitcher matchups for a specific game, click the `Analyze Matchups` link under the
desired game. This will take you to the `game/` route with more details about that specfic game, including a form
to select which pitchers from each team to analyze.

Select a pitcher from the select dropdowns for both teams, and click the `Analyze Matchups` button.

This will display a table of predicted matchups for every batter on the opposing team for each selected pitcher.
The form can be re-submitted with a different combination of pitchers to analyze their predicted matchup statistics.
To return to the home page, click the `Machine Learning Baseball` link in the navigation bar

For a video walkthrough, visit https://youtu.be/Rsf4NXdoUV0
