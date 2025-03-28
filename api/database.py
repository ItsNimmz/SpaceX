import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_db_connection():
    DB_URL = os.getenv('DATABASE_URL') 
    conn = psycopg2.connect(DB_URL)
    return conn

def run_query(query):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        yearly_stats = cur.fetchall()
        cur.close()
        conn.close()
        return yearly_stats
    except Exception as e:
        raise Exception(f"Error fetching yearly stats: {e}")

def fetch_yearly_stats():
    query = """
        SELECT 
            l.launch_year AS year,
            COUNT(*) AS total_launches
        FROM launches l
        GROUP BY l.launch_year
        ORDER BY l.launch_year;
    """

    data = run_query(query)
    return data

def fetch_rocket_stats():
    query = """
        SELECT 
            r.name AS rocket_name,
            COUNT(l.mission_id) AS total_launches,
            SUM(p.kg) AS total_payload_weight,
            ROUND(CAST(AVG(p.kg) AS NUMERIC), 2) AS avg_payload_weight,
            r.success_rate_percentage AS success_rate,
            r.company AS rocket_company
        FROM 
            rockets r
        LEFT JOIN 
            launches l ON r.rocket_id = l.rocket_id
        LEFT JOIN 
            payloads p ON l.mission_id = p.mission_id
        GROUP BY 
            r.name, r.success_rate_percentage, r.company
        ORDER BY 
            total_launches DESC, total_payload_weight DESC;
    """
    data = run_query(query)
    return data

def fetch_payload_contribution_by_rocket():
    query = """
        SELECT 
            r.name AS rocket_name,
            SUM(p.kg) AS total_payload_weight,
            ROUND(CAST((SUM(p.kg) * 100.0) / (SELECT SUM(kg) FROM payloads) AS NUMERIC), 2) AS payload_contribution_percentage
        FROM 
            rockets r
        LEFT JOIN 
            payloads p ON r.rocket_id = p.rocket_id
        GROUP BY 
            r.name
        ORDER BY 
            payload_contribution_percentage DESC;
    """
    data = run_query(query)
    return data

def fetch_overall_success_rate():
    query = """
        SELECT 
            COUNT(*) AS total_launches,
            SUM(CASE WHEN l.launch_success THEN 1 ELSE 0 END) AS successful_launches,
            ROUND(CAST((SUM(CASE WHEN l.success THEN 1 ELSE 0 END) * 100.0) / COUNT(*) AS NUMERIC), 2) AS overall_success_rate
        FROM 
            launches l;
    """
    data = run_query(query)
    return data

def fetch_launch_frequencies():
    query = """
        SELECT 
            l.launch_year AS year,
            COUNT(*) AS total_launches
        FROM 
            launches l
        GROUP BY 
            l.launch_year
        ORDER BY 
            l.launch_year;
    """
    data = run_query(query)
    return data

def fetch_rockets():
    query = """
        SELECT 
            name AS rocket_name,
            active
        FROM 
            rockets
        ORDER BY 
            name;
    """
    data = run_query(query)
    return data