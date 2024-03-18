import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime as dt


def time_string_to_timedelta(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return dt.timedelta(minutes=minutes, seconds=seconds)


def timedelta_to_seconds(td):
    return td.total_seconds()


time_strings = ["2:30", "3:45", "4:20", "5:10"]
durations = [time_string_to_timedelta(ts) for ts in time_strings]
print(durations)
x = np.array([timedelta_to_seconds(td) for td in durations]).reshape(-1, 1)
y = np.array([10, 20, 30, 40])  # Example dependent variable (response)

[print(f"THis is X: {item}") for item in x]
[print(f"THis is Y: {item}") for item in y]

# Perform linear regression
regressor = LinearRegression()
regressor.fit(x, y)

# Print the coefficients
print("Coefficient:", regressor.coef_[0])
print("Intercept:", regressor.intercept_)
