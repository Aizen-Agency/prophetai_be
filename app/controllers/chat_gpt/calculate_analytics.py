from datetime import datetime
from datetime import timezone

def calculate_instagram_analytics(posts_data):
    total_views = 0
    total_likes = 0
    total_comments = 0
    total_shares = 0  # Instagram doesn't provide this, stays 0

    processed_posts = []

    for idx, post in enumerate(posts_data):
        try:
            views = post.get("videoPlayCount", 0) or post.get("videoViewCount", 0) or 0
            likes = post.get("likesCount", 0) or post.get("likeCount", 0) or 0
            comments = post.get("commentsCount", 0) or post.get("commentCount", 0) or 0
            timestamp = post.get("timestamp")
            display_url = post.get("displayUrl")

            if timestamp:
                # Parse ISO format timestamp string and ensure it's timezone-aware
                post_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            else:
                # Use UTC timezone for current time
                post_date = datetime.now(timezone.utc)

            # Get current time in UTC for consistent comparison
            current_time = datetime.now(timezone.utc)
            days_diff = (current_time - post_date).days
            avg_views_per_day = round(views / max(days_diff, 1))

            total_views += views
            total_likes += likes
            total_comments += comments

            processed_posts.append({
                "video": f"Instagram Post {idx + 1}",
                "views": views,
                "likes": likes,
                "comments": comments,
                "display_url": display_url,
                "shares": 0,  # Instagram doesn't provide
                "date": post_date.strftime("%m/%d/%Y"),
                "avg_views_per_day": avg_views_per_day
            })

        except Exception as e:
            print(f"Error processing post {idx + 1}: {str(e)}")
            continue

    summary = {
        "total_views": total_views,
        "total_likes": total_likes,
        "total_comments": total_comments,
        "total_shares": total_shares,
        "posts": processed_posts
    }

    return summary
