from apify_client import ApifyClient
from flask import jsonify
import dotenv
from datetime import datetime, timedelta

def scrape_twitter_posts_controller(profile_url):
    try:
        print(f"[DEBUG] Starting Twitter scraper for URL: {profile_url}")
        
        client = ApifyClient("apify_api_ybMbddryhwVdnfhoWT7bYZWxd4s1A64quJvO")
        print("[DEBUG] Apify client initialized successfully")

        # Calculate dates for the last 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        # Format dates as YYYY-MM-DD
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        # Extract username from URL
        username = profile_url.split('/')[-1]
        search_query = f"from:{username} since:{start_date_str} until:{end_date_str}"
        
        print(f"[DEBUG] Search query: {search_query}")

        run_input = {
            "startUrls": [profile_url],
            "searchQueries": [search_query],
            "maxItems": 1,
            "proxyConfig": {
                "useApifyProxy": True
            },
            "sort": "Latest",
            "tweetLanguage": "en"
        }
        print("[DEBUG] Run input configuration prepared")

        print("[DEBUG] Starting Apify actor execution...")
        run = client.actor("builditn0w/x-twitter-scrapper").call(run_input=run_input)
        print(f"[DEBUG] Apify actor execution completed. Run ID: {run.get('id')}")
        print(f"💾 Check your data here: https://console.apify.com/storage/datasets/{run['defaultDatasetId']}")

        tweets_data = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            print(f"[DEBUG] Processing tweet: {item}")
            tweets_data.append(item)

        print(f"[DEBUG] Scraping completed. Found {len(tweets_data)} tweets")
        if not tweets_data:
            print("[DEBUG] No tweet content was extracted. This might be due to Twitter's anti-scraping measures.")
            return {"error": "No tweet content could be extracted"}, 500
            
        return {"tweets": tweets_data}, 200
    except Exception as e:
        print(f"[ERROR] Twitter scraper failed: {str(e)}")
        return {"error": str(e)}, 500
