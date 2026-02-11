import pandas as pd

listings = pd.read_json('listings.json')
print(listings.head(5))