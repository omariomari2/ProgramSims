import sqlite3
import datetime
from flask import Flask, jsonify, request, render_template, send_from_directory

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('kudos.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT id, username, full_name FROM users').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in users])

@app.route('/api/kudos', methods=['GET'])
def get_kudos():
    conn = get_db_connection()
    query = '''
        SELECT k.id, k.message, k.timestamp, 
               s.full_name as sender, r.full_name as receiver
        FROM kudos k
        JOIN users s ON k.sender_id = s.id
        JOIN users r ON k.receiver_id = r.id
        WHERE k.is_visible = 1
        ORDER BY k.timestamp DESC
    '''
    kudos = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in kudos])

@app.route('/api/kudos', methods=['POST'])
def create_kudos():
    data = request.get_json()
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    message = data.get('message')
    
    if not all([sender_id, receiver_id, message]):
        return jsonify({'error': 'Missing required fields'}), 400
        
    conn = get_db_connection()
    conn.execute('INSERT INTO kudos (sender_id, receiver_id, message) VALUES (?, ?, ?)',
                 (sender_id, receiver_id, message))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Kudos sent successfully'}), 201

@app.route('/api/kudos/admin', methods=['GET'])
def get_all_kudos_admin():
    conn = get_db_connection()
    query = '''
        SELECT k.id, k.message, k.timestamp, k.is_visible,
               s.full_name as sender, r.full_name as receiver
        FROM kudos k
        JOIN users s ON k.sender_id = s.id
        JOIN users r ON k.receiver_id = r.id
        ORDER BY k.timestamp DESC
    '''
    kudos = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in kudos])

@app.route('/api/kudos/<int:kudos_id>/moderate', methods=['PUT'])
def moderate_kudos(kudos_id):
    data = request.get_json()
    is_visible = data.get('is_visible')
    
    if is_visible is None:
        return jsonify({'error': 'Missing is_visible field'}), 400
        
    conn = get_db_connection()
    conn.execute('UPDATE kudos SET is_visible = ? WHERE id = ?', (is_visible, kudos_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Kudos visibility updated'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
