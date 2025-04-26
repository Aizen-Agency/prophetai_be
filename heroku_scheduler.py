import os
import sys
import psycopg2
import json
from datetime import datetime

# Add the app directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from app.controllers.apify.instagram_scraper import scrape_instagram_profile_posts
from app.controllers.chat_gpt.calculate_analytics import calculate_instagram_analytics
from app.extensions import get_db_connection
from app.models.analytics import Analytics

def fetch_and_store_instagram_analytics():
    """
    Fetch Instagram analytics using Apify and store in database
    """
    print("Starting Instagram analytics fetch...")
    
    # Dummy Instagram profile URL to scrape
    instagram_profile_url = "https://www.instagram.com/instagram/"
    
    try:
        # Scrape the Instagram profile
        print(f"Scraping Instagram profile: {instagram_profile_url}")
        scraped_data, status_code = scrape_instagram_profile_posts(instagram_profile_url)
        
        if status_code != 200:
            print(f"Error scraping Instagram profile: {scraped_data}")
            return
        
        # Calculate analytics from the scraped data
        print("Calculating analytics from scraped data...")
        analytics = calculate_instagram_analytics(scraped_data.get('posts', []))
        
        # Create a new Analytics object
        analytics_obj = Analytics(
            userid="0",  # Using userid=0 for dummy/system data
            posts=json.dumps(analytics),
            instagram_url=instagram_profile_url
        )
        
        # Save to database
        print("Saving analytics to database...")
        analytics_obj.save()
        
        print("Instagram analytics successfully fetched and stored!")
        
    except Exception as e:
        print(f"Error during Instagram analytics fetch: {str(e)}")

if __name__ == "__main__":
    fetch_and_store_instagram_analytics()
