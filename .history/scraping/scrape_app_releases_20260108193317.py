from google_play_scraper import app
import pandas as pd

result = app(
    "com.spotify.music",
    lang="en",
    country="us"
)

rows = [{
    "version": result.get("version"),
    "release_date": pd.to_datetime(result.get("updated")),
    "release_notes": result.get("recentChanges"),
    "source": "google_play"
}]

df = pd.DataFrame(rows)

df.to_csv("data/product_releases_raw.csv", index=False)

print("Scraped app releases:", len(df))
print(df)
