import os
import pandas as pd

def clean_csv_boxscore_tables(folder_path):
    num = 1
    for file_name in os.listdir(folder_path):
        print(f" cleaning and writing box_score number {(num)}:")
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            box_score = pd.read_csv(file_path)
            box_score.to_csv(f'../clean_box_scores/{file_name}', index=False)
        num += 1
    print("Done cleaning all box score tables there no missing values.")

if __name__ == "__main__":
    folder_path = '../box_score_tables_csv'
    clean_csv_boxscore_tables(folder_path)
