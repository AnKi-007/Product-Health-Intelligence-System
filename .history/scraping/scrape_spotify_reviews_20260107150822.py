from google_play_scraper import Sort, reviews
import pandas as pd

APP_ID = "com.spotify.music"

all_reviews = []
continuation_token = None

for _ in range(5):  # ~5 x 1000 = 5000 reviews
    result, continuation_token = reviews(
        APP_ID,
        lang="en",
        country="us",
        sort=Sort.NEWEST,
        count=1000,
        continuation_token=continuation_token,
    )
    all_reviews.extend(result)

df = pd.DataFrame(all_reviews)

df = df[
    [
        "reviewId",
        "content",
        "score",
        "at",
        "thumbsUpCount"
    ]
]

df.rename(
    columns={
        "reviewId": "review_id",
        "content": "review_text",
        "score": "rating",
        "at": "review_date",
        "thumbsUpCount": "likes",
    },
    inplace=True,
)

df.to_csv("data/app_reviews_raw.csv", index=False)

print("Scraped reviews:", len(df))
print(df.head())
