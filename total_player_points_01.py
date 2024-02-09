from sklearn.linear_model import LinearRegression
import numpy as np

# Input data
player_minutes = [30, 25, 28, 32, 29, 27, 26, 31, 33, 25, 28, 30, 29, 27, 26, 31, 33, 25, 28, 30, 29, 27, 26, 31, 33, 25, 28, 30, 29, 27]
usage_rate = [0.25, 0.28, 0.3, 0.27, 0.29, 0.26, 0.29, 0.32, 0.28, 0.26, 0.3, 0.29, 0.28, 0.3, 0.27, 0.29, 0.26, 0.29, 0.32, 0.28, 0.26, 0.3, 0.29, 0.28, 0.3, 0.27, 0.29, 0.26, 0.29, 0.32]
avg_shots_attempted = [12, 10, 11, 13, 12, 14, 15, 12, 13, 12, 10, 11, 13, 12, 14, 15, 12, 13, 12, 10, 11, 13, 12, 14, 15, 12, 13, 12, 10, 11]
fg_percentage = [0.45, 0.48, 0.42, 0.47, 0.46, 0.43, 0.44, 0.41, 0.45, 0.43, 0.42, 0.47, 0.46, 0.43, 0.44, 0.41, 0.45, 0.43, 0.42, 0.47, 0.46, 0.43, 0.44, 0.41, 0.45, 0.43, 0.42, 0.47, 0.46, 0.43]
opp_defensive_rating = [105, 100, 110, 98, 105, 105, 98, 110, 100, 105, 105, 98, 110, 100, 105, 105, 98, 110, 100, 105, 105, 98, 110, 100, 105, 105, 98, 110, 100, 105]
total_points = [24, 20, 22, 26, 25, 15, 14, 20, 22, 26, 25, 24, 20, 22, 26, 15, 14, 20, 22, 26, 25, 24, 20, 22, 26, 25, 15, 14, 20, 22]
opponent_length = [2.05, 2.03, 2.08, 2.01, 2.07, 2.03, 2.01, 2.09, 2.05, 2.03, 2.08, 2.01, 2.07, 2.03, 2.01, 2.09, 2.05, 2.03, 2.08, 2.01, 2.07, 2.03, 2.01, 2.09, 2.05, 2.03, 2.08, 2.01, 2.07, 2.03]
opponent_steal_rate = [1.2, 1.5, 1.3, 1.4, 1.6, 1.3, 1.4, 1.2, 1.5, 1.3, 1.4, 1.6, 1.3, 1.4, 1.2, 1.5, 1.3, 1.4, 1.6, 1.3, 1.4, 1.2, 1.5, 1.3, 1.4, 1.6, 1.3, 1.4, 1.2, 1.5, 1.3]
opponent_block_rate = [2.3, 2.1, 2.5, 2.4, 2.2, 2.1, 2.4, 2.3, 2.1, 2.5, 2.4, 2.2, 2.1, 2.4, 2.3, 2.1, 2.5, 2.4, 2.2, 2.1, 2.4, 2.3, 2.1, 2.5, 2.4, 2.2, 2.1, 2.4, 2.3, 2.1]
avg_shots_attempted_against = [15, 14, 16, 13, 15, 14, 13, 15, 16, 15, 14, 16, 13, 15, 14, 13, 15, 16, 15, 14, 16, 13, 15, 14, 13, 15, 16, 15, 14, 16]

# Reshape data for regression
X = np.array([
    [mins, rate, shots_attempted, fg_percent, def_rating, length, steal_rate, block_rate, avg_shots_against]
    for mins, rate, shots_attempted, fg_percent, def_rating, length, steal_rate, block_rate, avg_shots_against
    in zip(player_minutes, usage_rate, avg_shots_attempted, fg_percentage, opp_defensive_rating,
           opponent_length, opponent_steal_rate, opponent_block_rate, avg_shots_attempted_against)
])
y = np.array(total_points)

# Create and fit the model
model = LinearRegression()
model.fit(X, y)

# Predict total points for the next game
next_game_minutes = 27  # Player minutes in the next game
next_game_usage_rate = 0.28  # Usage rate in the next game
next_game_avg_shots_attempted = 14  # Average shots attempted in the next game
next_game_fg_percentage = 0.46  # FG percentage in the next game
next_game_opp_defensive_rating = 110  # Opponent's defensive rating in the next game
next_game_opponent_length = 2.06  # Opponent's average player length in the next game
next_game_opponent_steal_rate = 1.4  # Opponent's steal rate in the next game
next_game_opponent_block_rate = 2.2  # Opponent's block rate in the next game
next_game_avg_shots_attempted_against = 14  # Average shots attempted against the player in the next game

predicted_total_points = model.predict([[next_game_minutes, next_game_usage_rate, next_game_avg_shots_attempted,
                                         next_game_fg_percentage, next_game_opp_defensive_rating,
                                         next_game_opponent_length, next_game_opponent_steal_rate,
                                         next_game_opponent_block_rate, next_game_avg_shots_attempted_against]])

print("Predicted total points in the next game:", predicted_total_points[0])
