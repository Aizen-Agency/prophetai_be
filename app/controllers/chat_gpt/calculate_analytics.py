from datetime import datetime

def calculate_instagram_analytics(posts_data):
    total_views = 0
    total_likes = 0
    total_comments = 0
    total_shares = 0  # Instagram doesn't provide this, stays 0

    processed_posts = []

    for idx, post in enumerate(posts_data):
        try:
            views = post.get("videoViewCount", 0) or post.get("viewCount", 0) or 0
            likes = post.get("likesCount", 0) or post.get("likeCount", 0) or 0
            comments = post.get("commentsCount", 0) or post.get("commentCount", 0) or 0
            timestamp = post.get("takenAtTimestamp")

            if timestamp:
                post_date = datetime.fromtimestamp(timestamp)
            else:
                post_date = datetime.utcnow()

            avg_views_per_day = round(views / max((datetime.utcnow() - post_date).days, 1))

            total_views += views
            total_likes += likes
            total_comments += comments

            processed_posts.append({
                "video": f"Instagram Post {idx + 1}",
                "views": views,
                "likes": likes,
                "comments": comments,
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
