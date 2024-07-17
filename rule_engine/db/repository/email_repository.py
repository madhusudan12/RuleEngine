
from rule_engine.db.models.email import Email

from datetime import datetime

import psycopg2
import psycopg2.extras



class EmailRepository:
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = self.create_connection()
        self.create_table()

    def create_connection(self):
        return psycopg2.connect(**self.db_config)

    def create_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS emails (
            id VARCHAR PRIMARY KEY,
            from_email VARCHAR,
            to_email VARCHAR,
            subject VARCHAR,
            message TEXT,
            received_date TIMESTAMP
        );
        """
        with self.conn.cursor() as cursor:
            cursor.execute(create_table_sql)
        self.conn.commit()

    def insert_email(self, email):
        insert_sql = """
        INSERT INTO emails (id, from_email, subject, message, received_date)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """
        with self.conn.cursor() as cursor:
            cursor.execute(insert_sql, (email.id, email.from_email, email.subject, email.message, email.received_date))
        self.conn.commit()

    def bulk_insert_emails(self, emails):
        insert_sql = """
        INSERT INTO emails (id, from_email, to_email, subject, message, received_date)
        VALUES %s
        ON CONFLICT (id) DO NOTHING;
        """
        data = [
            (
                email.id,
                email.from_email,
                email.to_email,
                email.subject,
                email.message,
                datetime.fromtimestamp(int(email.received_date) / 1000)
            )
            for email in emails
        ]
        with self.conn.cursor() as cursor:
            psycopg2.extras.execute_values(cursor, insert_sql, data, template=None, page_size=100)
        self.conn.commit()

    def fetch_emails(self):
        select_sql = "SELECT * FROM emails;"
        with self.conn.cursor() as cursor:
            cursor.execute(select_sql)
            rows = cursor.fetchall()
        emails = [Email(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]
        return emails

