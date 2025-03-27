from sqlalchemy import create_engine, text  
import pandas as pd
import os
import psycopg2
current_dir = os.path.dirname(__file__)
folder_path = os.path.join(current_dir, 'data')

HOST = "postgresql://space_x_v1_user:HnphvMLlpStdnaghN8TuOtNOGz6PVX0s@dpg-cvhpqhggph6c73ce9of0-a.oregon-postgres.render.com/space_x_v1"  # Change if your database is hosted remotely

# Create MySQL database connection using SQLAlchemy
engine = create_engine(HOST)

def create_tables():
    queries = [
        """
        CREATE TABLE IF NOT EXISTS rockets (
            id SERIAL PRIMARY KEY,
            rocket_id VARCHAR(500),
            name VARCHAR(255),
            rocket_type VARCHAR(255),
            company VARCHAR(255),
            description VARCHAR(500),
            first_flight TIMESTAMP,
            cost_per_launch INT,
            diameter FLOAT,
            mass FLOAT,
            height FLOAT,
            success_rate_percentage INT,
            country VARCHAR(255),
            active BOOLEAN
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS launches (
            id SERIAL PRIMARY KEY,
            mission_name VARCHAR(255),
            launch_date_utc TIMESTAMP,
            launch_success BOOLEAN,
            launch_year INT,
            FOREIGN KEY (rocket_id) REFERENCES rockets(id) ON DELETE CASCADE
        );
        """
        ]
    try:
        # Establish the connection to PostgreSQL
        conn = psycopg2.connect(HOST)
        cur = conn.cursor()
        
        # Execute each query
        for query in queries:
            cur.execute(query)  # Execute the SQL statement
            print("Query executed successfully.")
        
        # Commit the changes and close the connection
        conn.commit()
        cur.close()
        conn.close()
    
    except Exception as e:
        print(f"An error occurred: {e}")

def insert_to_database(df, table_name):

    try:
        df.to_sql(table_name, con=engine, if_exists="replace", index=False)
        print("Data inserted successfully into the table.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Remove later
    with engine.begin() as conn:
        test = conn.execute(text(f"SELECT * FROM {table_name}"))
        rows = test.fetchall()
        for row in rows:
            print(row)
        
   
