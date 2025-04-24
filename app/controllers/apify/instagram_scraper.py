from apify_client import ApifyClient

def scrape_instagram_profile_posts(profile_url):
    try:
        client = ApifyClient("apify_api_Kj06ex13B1I68hYcX3gxpklsjgrsyH44bRGM")

        username = profile_url.rstrip('/').split('/')[-1]
        if not username:
            return {"error": "Invalid Instagram profile URL"}, 400

        run_input = {
            "searchType": "user",
            "directUrls": [profile_url],
            "resultsType": "posts",
            "resultsLimit": 1,
            "onlyPostsNewerThan": "7 days",
            "proxyConfiguration": {"useApifyProxy": True},
            "searchLimit": 10
            
        }

        run = client.actor("apify/instagram-scraper").call(run_input=run_input, wait_secs=30)

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
