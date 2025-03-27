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
        DROP TABLE IF EXISTS launches CASCADE;
        """,
        """
        DROP TABLE IF EXISTS rockets CASCADE;
        """,
        """
        DROP TABLE IF EXISTS payloads CASCADE;
        """,
        """
        CREATE TABLE IF NOT EXISTS rockets (
            rocket_id VARCHAR(500) PRIMARY KEY,
            name VARCHAR(255),
            type VARCHAR(255),
            company VARCHAR(255),
            description VARCHAR(500),
            first_flight TIMESTAMP,
            cost_per_launch INT,
            diameter_meters FLOAT,
            mass_kg FLOAT,
            height_meters FLOAT,
            success_rate_percentage INT,
            country VARCHAR(255),
            active BOOLEAN
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS launches (
            mission_id VARCHAR(500) PRIMARY KEY,
            mission_name VARCHAR(255),
            launch_date_utc TIMESTAMP,
            launch_year INT,
            details VARCHAR(2000),
            rocket_id VARCHAR(500),
            FOREIGN KEY (rocket_id) REFERENCES rockets(rocket_id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS payloads (
            payload_id VARCHAR(500) PRIMARY KEY,                 
            name VARCHAR(255),        
            kg FLOAT,
            mission_id VARCHAR(500),  
            rocket_id VARCHAR(500),   
            FOREIGN KEY (mission_id) REFERENCES launches(mission_id) ON DELETE CASCADE,
            FOREIGN KEY (rocket_id) REFERENCES rockets(rocket_id) ON DELETE CASCADE
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
        with engine.connect() as conn:
            result = conn.execute(text(f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = '{table_name}';
            """))
            table_columns = [row[0] for row in result]

    # Filter the DataFrame to include only columns that exist in the table
        df = df[[col for col in df.columns if col in table_columns]]

        df.to_sql(table_name, con=engine, if_exists="append", index=False)
        print("Data inserted successfully into the table.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Remove later
    print('\n')
    print('\n')
    print('\n')
    print('------------------------table_name----------------------',table_name)
    with engine.begin() as conn:
        test = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        rows = test.fetchall()
        for row in rows:
            print(row)
    return True

def load_payload(cleaned_data):
    payload_data = []
    for index, row in cleaned_data.iterrows():
        if isinstance(row['payload_data'], list):  # Ensure payload_data is a list
            for payload in row['payload_data']:
                payload_data.append({
                    "payload_id": payload.get("id"),
                    "kg": payload.get("kg"),
                    "name": payload.get("name"),
                    "mission_id": row["mission_id"],  
                    "rocket_id": row["rocket_id"]
                })

    # Create a DataFrame for payload data
    payload_df = pd.DataFrame(payload_data)
    payload_df = payload_df.drop_duplicates(subset=["payload_id"])
    insert_to_database(payload_df,'payloads')
        


   
