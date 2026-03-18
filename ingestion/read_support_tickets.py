import pandas as pd

# Load support tickets CSV
df = pd.read_csv("data/support_tickets.csv")

print("Support tickets loaded successfully")
print("Rows:", df.shape[0])
print("Columns:", list(df.columns))

print("\nFirst 5 rows:")
print(df.head())
