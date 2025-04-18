from apify_client import ApifyClient
from flask import jsonify

def scrape_twitter_posts_controller(profile_url):
    try:
        client = ApifyClient("apify_api_25IZgfGFO1Ahv3ch5cukSTiD90nouL2SRw5K")

        run_input = {
            "runMode": "DEVELOPMENT",
            "startUrls": [{"url": profile_url}],
            "linkSelector": "a[href]",
            "globs": [{"glob": profile_url + "/*"}],
            "excludes": [{"glob": "/**/*.{png,jpg,jpeg,pdf}"}],
            "pageFunction": """
                async function pageFunction(context) {
                    const $ = context.jQuery;
                    const pageTitle = $('title').first().text();
                    const tweets = [];
                    $('article').each((i, el) => {
                        const tweet = $(el).text();
                        if (tweet) tweets.push(tweet);
                    });
                    return {
                        url: context.request.url,
                        pageTitle,
                        tweets
                    };
                }
            """,
            "proxyConfiguration": {"useApifyProxy": True},
            "initialCookies": [],
            "waitUntil": ["networkidle2"],
            "preNavigationHooks": "[]",
            "postNavigationHooks": "[]",
            "breakpointLocation": "NONE",
            "customData": {}
        }

        run = client.actor("apify/web-scraper").call(run_input=run_input)

        tweets_data = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            tweets_data.append(item)

        return tweets_data, 200
    except Exception as e:
        return {"error": str(e)}, 500
