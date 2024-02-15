import re
from datetime import datetime
# Sample strings
# Extracting information from each string
from datetime import datetime
import re

def get_game_info_list(game_string):
    # Regular expression pattern to extract game details, team names, and date
    pattern = r'(?:In-SeasonTournamentFinal:)?([A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)*)at([A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)*)BoxScore_(\w+\d+_\d+)'
    # Extracting information from each string
    match = re.match(pattern, game_string)
    if match:
        team1 = match.group(1)
        team2 = match.group(2)
        date = match.group(3)
        # Insert spaces between camel case team names
        team1 = re.sub(r"(?<=\w)([A-Z])", r" \1", team1)
        team2 = re.sub(r"(?<=\w)([A-Z])", r" \1", team2)
        date_obj = datetime.strptime(date, '%B%d_%Y')
        formatted_date = date_obj.strftime('%Y-%m-%d')
        print("Game:", team1, "at", team2)
        print("Date:", formatted_date)
        return [team1, team2, formatted_date]
    else:
        print("No match found for:", game_string)

# Test the function





info = get_game_info_list("In-SeasonTournamentFinal:IndianaPacersatLosAngelesLakersBoxScore_December9_2023")
print(info)