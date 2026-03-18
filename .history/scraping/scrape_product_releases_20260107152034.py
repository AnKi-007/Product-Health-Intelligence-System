import requests
import pandas as pd

url = "https://api.github.com/repos/spotify/annoy/releases"

response = requests.get(url)
response.raise_for_status()

releases = response.json()

rows = []

for r in releases:
    rows.append({
        "version": r.get("tag_name"),
        "release_date": r.get("published_at"),
        "release_notes": r.get("body"),
        "source": "github"
    })

df = pd.DataFrame(rows)

df["release_date"] = pd.to_datetime(df["release_date"])

df.to_csv("data/product_releases_raw.csv", index=False)

print("Scraped releases:", len(df))
print(df.head())
