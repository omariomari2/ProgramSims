import unittest
import json
from app import app, get_db_connection

class kudosTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        

        conn = get_db_connection()
        with open('schema.sql') as f:
            conn.executescript(f.read())
        
        conn.execute("INSERT INTO users (username, full_name, is_admin) VALUES (?, ?, ?)", ('alice', 'Alice', 0))
        conn.execute("INSERT INTO users (username, full_name, is_admin) VALUES (?, ?, ?)", ('bob', 'Bob', 0))
        conn.commit()
        conn.close()

    def test_get_users(self):
        rv = self.app.get('/api/users')
        data = json.loads(rv.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['username'], 'alice')

    def test_create_and_get_kudos(self):

        rv = self.app.post('/api/kudos', json={
            'sender_id': 1,
            'receiver_id': 2,
            'message': 'Good job!'
        })
        self.assertEqual(rv.status_code, 201)
        

        rv = self.app.get('/api/kudos')
        data = json.loads(rv.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['message'], 'Good job!')
        
    def test_moderation(self):

        self.app.post('/api/kudos', json={'sender_id': 1, 'receiver_id': 2, 'message': 'To be hidden'})
        

        rv = self.app.get('/api/kudos')
        data = json.loads(rv.data)
        self.assertEqual(len(data), 1)
        kudos_id = data[0]['id']
        

        rv = self.app.put(f'/api/kudos/{kudos_id}/moderate', json={'is_visible': 0})
        self.assertEqual(rv.status_code, 200)
        

        rv = self.app.get('/api/kudos')
        data = json.loads(rv.data)
        self.assertEqual(len(data), 0)

if __name__ == '__main__':
    unittest.main()
