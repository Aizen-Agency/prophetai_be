from apify_client import ApifyClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def scrape_instagram_profile_posts(profile_url):
    try:
        # Get API key from environment variable
        client = ApifyClient(os.environ.get("APIFY_API_KEY"))

        username = profile_url.rstrip('/').split('/')[-1]
        if not username:
            return {"error": "Invalid Instagram profile URL"}, 400

        # run_input = {
        #     "searchType": "user",
        #     "directUrls": [profile_url],
        #     "resultsType": "posts",
        #     "resultsLimit": 10,
        #     "onlyPostsNewerThan": "7 days",
        #     "proxyConfiguration": {"useApifyProxy": True},
        #     "searchLimit": 10
            
        # }

        run_input = {
            "resultsLimit": 10,
            "username": [
                profile_url
            ]
            }

        # run = client.actor("apify/instagram-scraper").call(run_input=run_input)
        run = client.actor("xMc5Ga1oCONPmWJIa").call(run_input=run_input)

        posts = [
            item for item in client.dataset(run["defaultDatasetId"]).iterate_items()
        ]

        return {
            "username": username,
            "dataset_url": f"https://console.apify.com/storage/datasets/{run['defaultDatasetId']}",
            "posts": posts
        }, 200

    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        return {"error": str(e)}, 500
