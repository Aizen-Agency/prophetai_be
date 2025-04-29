from app.extensions import get_db_connection
from datetime import datetime

class Analytics:
    def __init__(self, analytics_id=None, userid=None, posts=None, instagram_url=None, created_at=None):
        self.analytics_id = analytics_id
        self.userid = userid
        self.posts = posts
        self.instagram_url = instagram_url
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        return {
            'analytics_id': self.analytics_id,
            'userid': self.userid,
            'posts': self.posts,
            'instagram_url': self.instagram_url
        }
        
    @staticmethod
    def recreate_table():
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            # Drop the existing table
            cur.execute("DROP TABLE IF EXISTS analytics CASCADE")
            conn.commit()
            
            # Create the new table with updated schema
            create_table_sql = """
                CREATE TABLE analytics (
                    analytics_id SERIAL PRIMARY KEY,
                    userid VARCHAR(255) NOT NULL,
                    posts JSONB NOT NULL,
                    instagram_url VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            
            cur.execute(create_table_sql)
            conn.commit()
            print("Analytics table recreated successfully with new schema")
            
        except Exception as e:
            print(f"Error recreating analytics table: {str(e)}")
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()
            
    def save(self):
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            # First check if a record with this Instagram URL already exists
            check_sql = """
                SELECT analytics_id FROM analytics 
                WHERE instagram_url = %s AND userid = %s
            """
            cur.execute(check_sql, (self.instagram_url, self.userid))
            existing_record = cur.fetchone()
            
            if existing_record:
                # Update existing record
                update_sql = """
                    UPDATE analytics 
                    SET posts = %s, created_at = %s
                    WHERE analytics_id = %s
                    RETURNING analytics_id
                """
                cur.execute(update_sql, (self.posts, self.created_at, existing_record['analytics_id']))
                result = cur.fetchone()
                self.analytics_id = result['analytics_id']
            else:
                # Insert new record
                insert_sql = """
                    INSERT INTO analytics (userid, posts, instagram_url)
                    VALUES (%s, %s, %s)
                    RETURNING analytics_id
                """
                cur.execute(insert_sql, (self.userid, self.posts, self.instagram_url))
                result = cur.fetchone()
                self.analytics_id = result['analytics_id']
            
            conn.commit()
            
        except Exception as e:
            print(f"Error saving analytics: {str(e)}")
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()
            
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT * FROM analytics")
            analytics_data = cur.fetchall()
            analytics_list = []
            
            for data in analytics_data:
                analytics_list.append(Analytics(**data))
                
            return analytics_list
            
        except Exception as e:
            print(f"Error retrieving analytics: {str(e)}")
            raise
        finally:
            cur.close()
            conn.close()
