import psycopg2
from logger_config import log
from JobOffer import JobOffer
from typing import List
import os
from dotenv import load_dotenv
load_dotenv()

class DatabaseConfig:
    def __init__(self, name='postgres'):
        self.name = name
        # Supabase connection parameters
        self.supabase_host = os.getenv('SUPABASE_DB_HOST')
        self.supabase_database = os.getenv('SUPABASE_DB_NAME')
        self.supabase_user = os.getenv('SUPABASE_DB_USER')
        self.supabase_password = os.getenv('SUPABASE_DB_PASSWORD')
        self.supabase_port = os.getenv('SUPABASE_DB_PORT')
        
    def connect_to_database(self):
        # For Supabase, we don't need to specify a different database name
        log.info(f"Connecting to Supabase database")
        conn = psycopg2.connect(
            host=self.supabase_host,
            database=self.supabase_database,
            user=self.supabase_user,
            password=self.supabase_password,
            port=self.supabase_port
        )
        conn.autocommit = True
        cursor = conn.cursor()
        log.info(f"Connected to Supabase database")

        return conn, cursor

    def disconnect_from_database(self, conn, cursor):
        cursor.close()
        conn.close()
        log.info(f"Disconnected from Supabase database")


    def create_table(self):
        conn, cursor = self.connect_to_database()

        log.info("Creating 'data' table.")
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS data (
                    url TEXT,
                    title TEXT,
                    company TEXT,
                    location TEXT,
                    salary TEXT,
                    site_id TEXT,
                    add_info TEXT,
                    PRIMARY KEY (url, title)
                )
            """)
        log.info("Table 'data' has been created.")

        self.disconnect_from_database(conn, cursor)

    def insert_data(self, data):
        conn, cursor = self.connect_to_database()
        inserted_offers: List[JobOffer] = []

        log.info(f"Saving data to '{self.name}'.")
        for record in data:
            cursor.execute("""
                        INSERT INTO data (title, company, location, salary, url, site_id, add_info)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (url, title) DO NOTHING
                        """,
                           (record.title,
                            record.company,
                            record.location,
                            record.salary,
                            record.url,
                            record.site_id,
                            record.add_info)
                           )
            if cursor.rowcount == 1:
                inserted_offers.append(record)
        log.info("Data has been saved.")

        self.disconnect_from_database(conn, cursor)
        log.info(f"Inserted {len(inserted_offers)} offers into the database.")
        return inserted_offers

    def reset_database(self):
        conn, cursor = self.connect_to_database()

        log.info(f"Resetting data in Supabase.")
        cursor.execute('TRUNCATE TABLE data RESTART IDENTITY')
        log.info(f"Data has been reset.")

        self.disconnect_from_database(conn, cursor)

    def read_data(self):
        conn, cursor = self.connect_to_database()

        log.info(f"Reading data from Supabase.")
        cursor.execute('SELECT * FROM data')
        db_offers = cursor.fetchall()
        log.info(f"Data has been read.")
        self.disconnect_from_database(conn, cursor)

        offers_to_return: List[JobOffer] = []
        for offer in db_offers:
            offers_to_return.append(JobOffer(offer[1], offer[2], offer[3], offer[4], offer[0], offer[5], offer[6]))

        return offers_to_return

if __name__ == '__main__':
    dc = DatabaseConfig()

    jobOffer = JobOffer('test', 'test', 'test', 'test', 'test', 'test')

    dc.create_table()
    dc.insert_data([jobOffer])
    dc.reset_database()