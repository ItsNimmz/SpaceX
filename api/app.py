from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import database as db

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route('/api/launches/stats', methods=['GET'])
def get_launch_stats():
    try:
        # Fetch data using the query functions
        yearly_stats = db.fetch_yearly_stats()
        rocket_stats = db.fetch_rocket_stats()

        return jsonify({
            'yearly_stats': yearly_stats,
            'rocket_stats': rocket_stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/metrix', methods=['GET'])
def get_metrix():
    try:
        # Fetch data using the query functions
        payload_contribution = db.fetch_payload_contribution_by_rocket()
        launch_frequencies = db.fetch_launch_frequencies()

        total_launches = sum(item['total_launches'] for item in launch_frequencies)
        
        return jsonify({
            'payload_contribution': payload_contribution,
            'launch_frequencies': launch_frequencies,
            'total_launches': total_launches
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500    

@app.route('/api/test', methods=['GET'])
def deployment_test():
    return jsonify({'message': 'Deployment successful! The Flask app is running.>>>'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
