from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import psycopg2

load_dotenv()

app = Flask(__name__)
CORS(app)


# test
def get_db_connection():
    DB_URL = "postgresql://space_x_v1_user:HnphvMLlpStdnaghN8TuOtNOGz6PVX0s@dpg-cvhpqhggph6c73ce9of0-a.oregon-postgres.render.com/space_x_v1"
    conn = psycopg2.connect(DB_URL)
    return conn
# test

@app.route('/api/launches/stats', methods=['GET'])
def get_launch_stats():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Query 1: Yearly stats (total launches per year)
        cur.execute("""
            SELECT 
                l.launch_year AS year,
                COUNT(*) AS total_launches
            FROM launches l
            GROUP BY l.launch_year
            ORDER BY l.launch_year;
        """)
        yearly_data = cur.fetchall()
        yearly_columns = [desc[0] for desc in cur.description]
        yearly_stats = [dict(zip(yearly_columns, row)) for row in yearly_data]

        # Query 2: Payload stats (average payload weight by rocket)
        cur.execute("""
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
        """)
        rocket_data = cur.fetchall()
        rocket_columns = [desc[0] for desc in cur.description]
        rocket_stats = [dict(zip(rocket_columns, row)) for row in rocket_data]

        cur.close()
        conn.close()

        # Return both datasets in a single JSON response
        return jsonify({
            'yearly_stats': yearly_stats,
            'rocket_stats': rocket_stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/api/test', methods=['GET'])
def deployment_test():
    return jsonify({'message': 'Deployment successful! The Flask app is running.'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
