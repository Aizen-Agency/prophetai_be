from app import create_app
from app.models import db
from app.models.userData import User
from app.models.scriptsModel import Script
from app.models.videoModel import Video
from app.models.insights import Insights
import traceback

def print_table_structure_and_data():
    app = create_app()
    try:
        with app.app_context():
            print("\n=== Database Connection Test ===")
            # Test database connection
            try:
                db.engine.connect()
                print("✓ Database connection successful")
            except Exception as e:
                print(f"✗ Database connection failed: {str(e)}")
                return

            print("\n=== Database Tables Structure and Data ===\n")
            
            # User Table
            print("1. User Table (userData):")
            print("-" * 50)
            for column in User.__table__.columns:
                print(f"  {column.name}: {column.type}")
            print("\nData:")
            try:
                users = User.query.all()
                if not users:
                    print("  No data found in User table")
                else:
                    for user in users:
                        print(f"  ID: {user.id}, Email: {user.email}, Username: {user.username}")
            except Exception as e:
                print(f"  Error querying User table: {str(e)}")
            print()
            
            # Script Table
            print("2. Script Table (scripts):")
            print("-" * 50)
            for column in Script.__table__.columns:
                print(f"  {column.name}: {column.type}")
            print("\nData:")
            try:
                scripts = Script.query.all()
                if not scripts:
                    print("  No data found in Script table")
                else:
                    for script in scripts:
                        print(f"  ID: {script.id}, Title: {script.title}, User ID: {script.user_id}")
            except Exception as e:
                print(f"  Error querying Script table: {str(e)}")
            print()
            
            # Video Table
            print("3. Video Table (videos):")
            print("-" * 50)
            for column in Video.__table__.columns:
                print(f"  {column.name}: {column.type}")
            print("\nData:")
            try:
                videos = Video.query.all()
                if not videos:
                    print("  No data found in Video table")
                else:
                    for video in videos:
                        print(f"  ID: {video.id}, Title: {video.title}, User ID: {video.user_id}")
            except Exception as e:
                print(f"  Error querying Video table: {str(e)}")
            print()
            
            # Insights Table
            print("4. Insights Table (insights):")
            print("-" * 50)
            print("  id: Integer (Primary Key)")
            print("  user_id: Integer (Foreign Key to userData.id)")
            print("\n  Monthly Metrics (for each month January-December):")
            print("  - {month}_articles: Integer")
            print("  - {month}_scripts: Integer")
            print("  - {month}_videos_generated: Integer")
            print("  - {month}_videos_posted: Integer")
            print("\nData:")
            try:
                insights = Insights.query.all()
                if not insights:
                    print("  No data found in Insights table")
                else:
                    for insight in insights:
                        print(f"  ID: {insight.id}, User ID: {insight.user_id}")
                        print(f"  January Articles: {insight.january_articles}")
                        print(f"  January Scripts: {insight.january_scripts}")
                        print(f"  January Videos Generated: {insight.january_videos_generated}")
                        print(f"  January Videos Posted: {insight.january_videos_posted}")
                        print()
            except Exception as e:
                print(f"  Error querying Insights table: {str(e)}")
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nStack trace:")
        traceback.print_exc()

if __name__ == "__main__":
    print_table_structure_and_data() 