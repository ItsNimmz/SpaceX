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
        # cur = mysql.connection.cursor()
        
        # Get yearly success rates
        cur.execute("""
            SELECT * 
            FROM rockets
        """)
        rockets_data = cur.fetchall()
    
        columns = [desc[0] for desc in cur.description]

        # Convert the result into a list of dictionaries (key-value pairs)
        rockets_list = [dict(zip(columns, row)) for row in rockets_data]
        
        cur.close()
        
        return jsonify({
            'rockets': rockets_list
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)