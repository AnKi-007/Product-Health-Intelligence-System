from google_play_scraper import app
import pandas as pd

result = app(
    "com.spotify.music",
    lang="en",
    country="us"
)

rows = []

for h in result.get("histogram", []):
    rows.append({
        "version": h.get("version"),
        "release_date": pd.to_datetime(h.get("date")),
        "release_notes": h.get("text"),
        "source": "google_play"
    })

df = pd.DataFrame(rows)

df.to_csv("data/product_releases_raw.csv", index=False)

print("Scraped app releases:", len(df))
print(df.head())
