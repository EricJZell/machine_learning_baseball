
# FIRST
# $ pip3 install numpy
# $ pip3 install pandas
# $ pip3 install scipy
import numpy as np
import pandas as pd
import matrix_factorization_utilities

# Load pitcher batter matchups
raw_matchups_df = pd.read_csv('matchups.csv')

# Convert the running list of matchups into a matrix
matchups_df = pd.pivot_table(raw_matchups_df, index='BatterID', columns='PitcherID', aggfunc=np.max)

# Create a csv of the raw mathups data, just for comparison:
matchups_df.to_csv("initial_matchups.csv")

# Apply matrix factorization to find the latent features
U, M = matrix_factorization_utilities.low_rank_matrix_factorization(matchups_df.as_matrix(),
                                                                    num_features=15,
                                                                    regularization_amount=.5)

# Find all predicted ratings by multiplying the U by M
predicted_matchups = np.matmul(U, M)

# Save all the ratings to a csv file
predicted_matchups_df = pd.DataFrame(index=matchups_df.index,
                                    columns=matchups_df.columns,
                                    data=predicted_matchups)
predicted_matchups_df.to_csv("predicted_matchups.csv")
