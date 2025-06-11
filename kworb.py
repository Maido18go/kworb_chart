import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime
from country_data import country_codes

def kworb_chart(countrycode): 

  # Download HTML file
  url = f"https://kworb.net/spotify/country/{countrycode}_daily.html"
  response = requests.get(url)
  response.encoding = 'utf-8'

  # Get HTML contents in text format
  html_content = response.text

  # Parse HTML with BeautifulSoup and find the table
  soup = BeautifulSoup(html_content, 'html.parser')
  table = soup.find('table', id='spotifydaily')

  if not table:
      print("Table is not found.")
      exit()

  # File name
  charts_dir = "charts"
  today = datetime.now().strftime("%Y-%m-%d")
  csv_filename = f'{charts_dir}/{countrycode}_dailytop50_{today}.csv'

  # Extract data from tables
  rows = []

  for i, tr in enumerate(table.find('tbody').find_all('tr')):
      if i >= 50:
          break

      row = []
      row.append(today)

      for td in tr.find_all('td'):
          # Strip HTML tags and get text content only
          row.append(td.text.strip())
      rows.append(row)

  df = pd.DataFrame(rows)
  df.to_csv(csv_filename, index=False, header=False, encoding='utf-8-sig')

if __name__ == "__main__":
    for country in country_codes:
        kworb_chart(country)
