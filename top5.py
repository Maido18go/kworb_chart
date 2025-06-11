import pandas as pd
import glob
import os
from datetime import datetime
from country_data import country_names

def extract_top5(directory="charts"):
    today = datetime.now().strftime("%Y-%m-%d")    
    # Search files
    csv_files = glob.glob(os.path.join(directory, f"*_dailytop50_{today}.csv"))
    if not csv_files:
        print(f"'{directory}' Chart file not found.")
        return

    for csv_file in csv_files:
        # Extract country code from file name (e.g. 'kr_dailytop50_20240523.csv' -> 'kr')
        country_code = os.path.basename(csv_file).split('_')[0]

        # Get the country name for the country code, or use the default file name
        display_name = country_names.get(country_code, os.path.basename(csv_file))

        print(f"\n--- Spotify Today's Top 5 - {display_name} ---")

        try:
            df = pd.read_csv(csv_file, header=None, nrows=5, encoding='utf-8-sig')

            for index, row in df.iterrows():
                output_string = f"{row[1]},{row[2]},{row[3]}"
                print(output_string)

        except Exception as e:
            print(f"An error occurred while loading the file '{csv_file}': {e}")

if __name__ == "__main__":
    extract_top5()

