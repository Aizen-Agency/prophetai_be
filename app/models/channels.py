from ..extensions import get_db_connection
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Channel:
    def __init__(self, id=None, user_id=None, product_id=None, product_name=None, link=None, description=None, created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.product_name = product_name
        self.link = link
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create_table():
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            create_table_sql = """
                CREATE TABLE IF NOT EXISTS channels (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    product_name VARCHAR(255) NOT NULL,
                    link VARCHAR(255),
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            
            cur.execute(create_table_sql)
            conn.commit()
            logger.info("Channels table created successfully")
            
        except Exception as e:
            logger.error(f"Error creating channels table: {str(e)}")
            raise
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()

    def save(self):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            if self.id is None:
                # Insert new channel
                cur.execute("""
                    INSERT INTO channels (user_id, product_id, product_name, link, description)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id, created_at, updated_at
                """, (self.user_id, self.product_id, self.product_name, self.link, self.description))
                
                result = cur.fetchone()
                self.id = result['id']
                self.created_at = result['created_at']
                self.updated_at = result['updated_at']
            else:
                # Update existing channel
                cur.execute("""
                    UPDATE channels
                    SET user_id = %s, product_id = %s, product_name = %s, link = %s, description = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    RETURNING updated_at
                """, (self.user_id, self.product_id, self.product_name, self.link, self.description, self.id))
                
                result = cur.fetchone()
                self.updated_at = result['updated_at']
            
            conn.commit()
            
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error saving channel: {str(e)}")
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def get_by_user(user_id):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            cur.execute("SELECT * FROM channels WHERE user_id = %s", (user_id,))
            channels = cur.fetchall()
            
            return [Channel(**channel) for channel in channels]
            
        except Exception as e:
            logger.error(f"Error getting channels for user {user_id}: {str(e)}")
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def get_by_id(channel_id):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            cur.execute("SELECT * FROM channels WHERE id = %s", (channel_id,))
            channel = cur.fetchone()
            
            if channel:
                return Channel(**channel)
            return None
            
        except Exception as e:
            logger.error(f"Error getting channel {channel_id}: {str(e)}")
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def delete(channel_id):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            cur.execute("DELETE FROM channels WHERE id = %s", (channel_id,))
            conn.commit()
            
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error deleting channel {channel_id}: {str(e)}")
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'link': self.link,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f"<Channel {self.id} | User {self.user_id} | Product {self.product_name}>"
