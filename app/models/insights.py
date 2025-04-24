from ..extensions import get_db_connection
from datetime import datetime

class Insights:
    def __init__(self, id=None, user_id=None, created_at=None, **kwargs):
        self.id = id
        self.user_id = user_id
        self.created_at = created_at or datetime.now()
        # Initialize monthly fields with default values
        for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']:
            setattr(self, f'{month}_total_articles_scraped', kwargs.get(f'{month}_total_articles_scraped', 0))
            setattr(self, f'{month}_total_scripts_generated', kwargs.get(f'{month}_total_scripts_generated', 0))
            setattr(self, f'{month}_total_videos_generated', kwargs.get(f'{month}_total_videos_generated', 0))

    @staticmethod
    def recreate_table():
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            # Drop the existing table
            cur.execute("DROP TABLE IF EXISTS insights CASCADE")
            conn.commit()
            
            # Create the new table with updated schema
            create_table_sql = """
                CREATE TABLE insights (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    jan_total_articles_scraped INTEGER DEFAULT 0,
                    jan_total_scripts_generated INTEGER DEFAULT 0,
                    jan_total_videos_generated INTEGER DEFAULT 0,
                    feb_total_articles_scraped INTEGER DEFAULT 0,
                    feb_total_scripts_generated INTEGER DEFAULT 0,
                    feb_total_videos_generated INTEGER DEFAULT 0,
                    mar_total_articles_scraped INTEGER DEFAULT 0,
                    mar_total_scripts_generated INTEGER DEFAULT 0,
                    mar_total_videos_generated INTEGER DEFAULT 0,
                    apr_total_articles_scraped INTEGER DEFAULT 0,
                    apr_total_scripts_generated INTEGER DEFAULT 0,
                    apr_total_videos_generated INTEGER DEFAULT 0,
                    may_total_articles_scraped INTEGER DEFAULT 0,
                    may_total_scripts_generated INTEGER DEFAULT 0,
                    may_total_videos_generated INTEGER DEFAULT 0,
                    jun_total_articles_scraped INTEGER DEFAULT 0,
                    jun_total_scripts_generated INTEGER DEFAULT 0,
                    jun_total_videos_generated INTEGER DEFAULT 0,
                    jul_total_articles_scraped INTEGER DEFAULT 0,
                    jul_total_scripts_generated INTEGER DEFAULT 0,
                    jul_total_videos_generated INTEGER DEFAULT 0,
                    aug_total_articles_scraped INTEGER DEFAULT 0,
                    aug_total_scripts_generated INTEGER DEFAULT 0,
                    aug_total_videos_generated INTEGER DEFAULT 0,
                    sep_total_articles_scraped INTEGER DEFAULT 0,
                    sep_total_scripts_generated INTEGER DEFAULT 0,
                    sep_total_videos_generated INTEGER DEFAULT 0,
                    oct_total_articles_scraped INTEGER DEFAULT 0,
                    oct_total_scripts_generated INTEGER DEFAULT 0,
                    oct_total_videos_generated INTEGER DEFAULT 0,
                    nov_total_articles_scraped INTEGER DEFAULT 0,
                    nov_total_scripts_generated INTEGER DEFAULT 0,
                    nov_total_videos_generated INTEGER DEFAULT 0,
                    dec_total_articles_scraped INTEGER DEFAULT 0,
                    dec_total_scripts_generated INTEGER DEFAULT 0,
                    dec_total_videos_generated INTEGER DEFAULT 0
                )
            """
            
            cur.execute(create_table_sql)
            conn.commit()
            print("Insights table recreated successfully with new schema")
            
        except Exception as e:
            print(f"Error recreating insights table: {str(e)}")
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def create_table():
        conn = get_db_connection()
        cur = conn.cursor()
        
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS insights (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                jan_total_articles_scraped INTEGER DEFAULT 0,
                jan_total_scripts_generated INTEGER DEFAULT 0,
                jan_total_videos_generated INTEGER DEFAULT 0,
                feb_total_articles_scraped INTEGER DEFAULT 0,
                feb_total_scripts_generated INTEGER DEFAULT 0,
                feb_total_videos_generated INTEGER DEFAULT 0,
                mar_total_articles_scraped INTEGER DEFAULT 0,
                mar_total_scripts_generated INTEGER DEFAULT 0,
                mar_total_videos_generated INTEGER DEFAULT 0,
                apr_total_articles_scraped INTEGER DEFAULT 0,
                apr_total_scripts_generated INTEGER DEFAULT 0,
                apr_total_videos_generated INTEGER DEFAULT 0,
                may_total_articles_scraped INTEGER DEFAULT 0,
                may_total_scripts_generated INTEGER DEFAULT 0,
                may_total_videos_generated INTEGER DEFAULT 0,
                jun_total_articles_scraped INTEGER DEFAULT 0,
                jun_total_scripts_generated INTEGER DEFAULT 0,
                jun_total_videos_generated INTEGER DEFAULT 0,
                jul_total_articles_scraped INTEGER DEFAULT 0,
                jul_total_scripts_generated INTEGER DEFAULT 0,
                jul_total_videos_generated INTEGER DEFAULT 0,
                aug_total_articles_scraped INTEGER DEFAULT 0,
                aug_total_scripts_generated INTEGER DEFAULT 0,
                aug_total_videos_generated INTEGER DEFAULT 0,
                sep_total_articles_scraped INTEGER DEFAULT 0,
                sep_total_scripts_generated INTEGER DEFAULT 0,
                sep_total_videos_generated INTEGER DEFAULT 0,
                oct_total_articles_scraped INTEGER DEFAULT 0,
                oct_total_scripts_generated INTEGER DEFAULT 0,
                oct_total_videos_generated INTEGER DEFAULT 0,
                nov_total_articles_scraped INTEGER DEFAULT 0,
                nov_total_scripts_generated INTEGER DEFAULT 0,
                nov_total_videos_generated INTEGER DEFAULT 0,
                dec_total_articles_scraped INTEGER DEFAULT 0,
                dec_total_scripts_generated INTEGER DEFAULT 0,
                dec_total_videos_generated INTEGER DEFAULT 0
            )
        """
        
        cur.execute(create_table_sql)
        conn.commit()
        cur.close()
        conn.close()

    def save(self):
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            sql = """
                INSERT INTO insights (user_id, created_at, jan_total_articles_scraped, jan_total_scripts_generated, jan_total_videos_generated, feb_total_articles_scraped, feb_total_scripts_generated, feb_total_videos_generated, mar_total_articles_scraped, mar_total_scripts_generated, mar_total_videos_generated, apr_total_articles_scraped, apr_total_scripts_generated, apr_total_videos_generated, may_total_articles_scraped, may_total_scripts_generated, may_total_videos_generated, jun_total_articles_scraped, jun_total_scripts_generated, jun_total_videos_generated, jul_total_articles_scraped, jul_total_scripts_generated, jul_total_videos_generated, aug_total_articles_scraped, aug_total_scripts_generated, aug_total_videos_generated, sep_total_articles_scraped, sep_total_scripts_generated, sep_total_videos_generated, oct_total_articles_scraped, oct_total_scripts_generated, oct_total_videos_generated, nov_total_articles_scraped, nov_total_scripts_generated, nov_total_videos_generated, dec_total_articles_scraped, dec_total_scripts_generated, dec_total_videos_generated)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """
            values = (self.user_id, self.created_at, self.jan_total_articles_scraped, self.jan_total_scripts_generated, self.jan_total_videos_generated, self.feb_total_articles_scraped, self.feb_total_scripts_generated, self.feb_total_videos_generated, self.mar_total_articles_scraped, self.mar_total_scripts_generated, self.mar_total_videos_generated, self.apr_total_articles_scraped, self.apr_total_scripts_generated, self.apr_total_videos_generated, self.may_total_articles_scraped, self.may_total_scripts_generated, self.may_total_videos_generated, self.jun_total_articles_scraped, self.jun_total_scripts_generated, self.jun_total_videos_generated, self.jul_total_articles_scraped, self.jul_total_scripts_generated, self.jul_total_videos_generated, self.aug_total_articles_scraped, self.aug_total_scripts_generated, self.aug_total_videos_generated, self.sep_total_articles_scraped, self.sep_total_scripts_generated, self.sep_total_videos_generated, self.oct_total_articles_scraped, self.oct_total_scripts_generated, self.oct_total_videos_generated, self.nov_total_articles_scraped, self.nov_total_scripts_generated, self.nov_total_videos_generated, self.dec_total_articles_scraped, self.dec_total_scripts_generated, self.dec_total_videos_generated)

            print(f"[DEBUG] Executing SQL: {sql}")
            print(f"[DEBUG] With values: {values}")

            cur.execute(sql, values)
            print(f"Excution complete moving ahead")
            result = cur.fetchone()
            if result:
                self.id = result["id"]
            else:
                print("[ERROR] No ID returned after insert")
                raise Exception("Failed to insert insights record")

            conn.commit()
        except Exception as e:
            print(f"[ERROR] Failed to save insights: {str(e)}")
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()

    def update(self):
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            print(f"[DEBUG] Updating insights record {self.id} with articles_scraped={self.articles_scraped}")
            cur.execute("""
                UPDATE insights
                SET articles_scraped = %s,
                    videos_posted = %s,
                    scripts_generated = %s
                WHERE id = %s
            """, (self.articles_scraped, self.videos_posted, self.scripts_generated, self.id))
            
            conn.commit()
            print(f"[DEBUG] Successfully updated insights record {self.id}")
        except Exception as e:
            print(f"[ERROR] Failed to update insights: {str(e)}")
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_by_user(user_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM insights WHERE user_id = %s", (user_id,))
        insights_data = cur.fetchone()
        cur.close()
        conn.close()
        if insights_data:
            return Insights(**insights_data)
        return None

    def __repr__(self):
        return f"<Insights {self.id} | User {self.user_id}>"

    def update_monthly_data(self, month, articles=0, scripts=0, videos=0):
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            sql = f"""
                UPDATE insights
                SET {month}_total_articles_scraped = {month}_total_articles_scraped + %s,
                    {month}_total_scripts_generated = {month}_total_scripts_generated + %s,
                    {month}_total_videos_generated = {month}_total_videos_generated + %s
                WHERE id = %s
            """
            values = (articles, scripts, videos, self.id)

            print(f"[DEBUG] Executing SQL: {sql}")
            print(f"[DEBUG] With values: {values}")

            cur.execute(sql, values)
            
            conn.commit()
            print(f"[DEBUG] Successfully updated {month} data for insights record {self.id}")
        except Exception as e:
            print(f"[ERROR] Failed to update {month} data: {str(e)}")
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()

# If going for montly insights

# class MonthlyInsights(db.Model):
#     __tablename__ = 'monthly_insights'

#     id = db.Column(Integer, primary_key=True)
#     user_id = db.Column(Integer, ForeignKey('userData.id'), nullable=False)

#     month = db.Column(String(10), nullable=False)  # e.g. 'Jan'
#     year = db.Column(Integer, nullable=False)

#     articles = db.Column(Integer, default=0)
#     scripts = db.Column(Integer, default=0)
#     short_videos = db.Column(Integer, default=0)
#     long_videos = db.Column(Integer, default=0)
#     total_videos = db.Column(Integer, default=0)

#     created_at = db.Column(DateTime, server_default=func.now())
