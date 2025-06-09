import psycopg2
from psycopg2 import sql
from logger_config import log
from JobOffer import JobOffer
from typing import List


class DatabaseConfig:
    def __init__(self, name='database'):
        self.name = name

    def connect_to_database(self, database):
        log.info(f"Connecting to database '{database}'")
        conn = psycopg2.connect(
            dbname=database,
            password='password',
            port='5432',
            user='postgres',
            host='localhost'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        log.info(f"Connected to database '{database}'")

        return conn, cursor

    def disconnect_from_database(self, conn, cursor, database):
        cursor.close()
        conn.close()
        log.info(f"Disconnected from database '{database}'")

    def create_database(self):
        conn, cursor = self.connect_to_database('postgres')

        log.info(f"Checking if database '{self.name}' exists")
        cursor.execute('SELECT 1 FROM pg_database WHERE datname = %s', (self.name,))
        if_exists = cursor.fetchone()

        if if_exists:
            log.info(f"Database '{self.name}' already exists")
        else:
            log.info(f"Creating database '{self.name}'")
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.name)))
            log.info(f"Database '{self.name}' has been created")

        self.disconnect_from_database(conn, cursor, 'postgres')

    def create_table(self):
        conn, cursor = self.connect_to_database(self.name)

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

        self.disconnect_from_database(conn, cursor, self.name)

    def insert_data(self, data):
        conn, cursor = self.connect_to_database(self.name)
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

        self.disconnect_from_database(conn, cursor, self.name)
        return inserted_offers

    def reset_database(self):
        conn, cursor = self.connect_to_database(self.name)

        log.info(f"Resetting data in '{self.name}'.")
        cursor.execute('TRUNCATE TABLE data RESTART IDENTITY')
        log.info(f"Data from '{self.name}' has been reset.")

        self.disconnect_from_database(conn, cursor, self.name)

    def read_data(self):
        conn, cursor = self.connect_to_database(self.name)

        log.info(f"reading data from database: '{self.name}'.")
        cursor.execute('SELECT * FROM data')
        db_offers = cursor.fetchall()
        log.info(f"Data from '{self.name}' has been read.")
        self.disconnect_from_database(conn, cursor, self.name)

        offers_to_return: List[JobOffer] = []
        for offer in db_offers:
            offers_to_return.append(JobOffer(offer[1], offer[2], offer[3], offer[4], offer[0], offer[5], offer[6]))

        return offers_to_return

    def delete_database(self):
        conn, cursor = self.connect_to_database('postgres')

        log.info(f"Deleting database '{self.name}'.")
        cursor.execute(f"DROP DATABASE IF EXISTS {self.name}")
        log.info(f"Database '{self.name}' has been deleted.")

        self.disconnect_from_database(conn, cursor, 'postgres')


if __name__ == '__main__':
    dc = DatabaseConfig()

    jobOffer = JobOffer('test', 'test', 'test', 'test', 'test', 'test')

    dc.create_database()
    dc.create_table()
    #dc.insert_data([jobOffer])
    dc.reset_database()
