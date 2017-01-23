import pandas as pd

results = pd.read_sql_table('listings', 'sqlite:///listings.db')
