from apify_client import ApifyClient
from flask import jsonify
from datetime import datetime

def scrape_instagram_posts_controller(profile_url):
    try:
        client = ApifyClient("apify_api_25IZgfGFO1Ahv3ch5cukSTiD90nouL2SRw5K")

        # Extract username from profile URL
        username = profile_url.split('/')[-1].strip()
        if not username:
            return {"error": "Invalid Instagram profile URL"}, 400

        run_input = {
            "searchType": "user",
            "searchLimit": 1,
            "resultsLimit": 50,
            "usernames": [username],
            "resultsType": "posts",
            "proxyConfiguration": {"useApifyProxy": True}
        }


        run = client.actor("apify/instagram-scraper").call(run_input=run_input)

        posts_data = []
        total_views, total_likes, total_comments, total_shares = 0, 0, 0, 0
        daily_views = {}

        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            print(item)
            try:
                # Safely get the timestamp, defaulting to current time if not available
                taken_at = datetime.fromtimestamp(item.get("takenAtTimestamp", datetime.now().timestamp()))
                date_str = taken_at.strftime("%m/%d/%Y")

                # Extract relevant metrics with safe defaults
                views = item.get("videoViewCount", 0) or item.get("viewCount", 0) or 0
                likes = item.get("likesCount", 0) or item.get("likeCount", 0) or 0
                comments = item.get("commentsCount", 0) or item.get("commentCount", 0) or 0

                # Update totals
                total_views += views
                total_likes += likes
                total_comments += comments

                # Aggregate views per day for trend
                daily_views[date_str] = daily_views.get(date_str, 0) + views

                # Calculate performance (arbitrary thresholds)
                if views >= 10000:
                    performance = "High"
                elif views >= 3000:
                    performance = "Medium"
                else:
                    performance = "Low"

                posts_data.append({
                    "title": item.get("title") or f"Instagram Post {item.get('shortCode', '')}",
                    "date": date_str,
                    "views": views,
                    "likes": likes,
                    "comments": comments,
                    "shares": 0,  # Placeholder since shares aren't available
                    "avg_views_per_day": round(views / max((datetime.now() - taken_at).days, 1)),
                    "performance": performance,
                    "url": f"https://www.instagram.com/p/{item.get('shortCode', '')}/"
                })
            except Exception as e:
                print(f"Error processing post: {str(e)}")
                continue

        # Format trend
        trend_data = [{"date": date, "views": views} for date, views in sorted(daily_views.items())]

        # Summary
        summary = {
            "total_views": total_views,
            "total_likes": total_likes,
            "total_comments": total_comments,
            "total_shares": total_shares,  # Always 0 unless you track it externally
            "trend": trend_data,
            "posts": posts_data,
            "username": username
        }

        return summary, 200
    except Exception as e:
        print(f"Scraper error: {str(e)}")
        return {"error": f"Failed to scrape Instagram data: {str(e)}"}, 500
