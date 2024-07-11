import unittest
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user
from flask_testing import TestCase
from app import create_app, db
from app.models import User, Claim
from app.routes import claim_bp

class TestClaims(TestCase):
    def create_app(self):
        app = create_app()
        app.config.from_object('config.TestingConfig')
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()
        self.client = self.app.test_client()
        
        # Create a test user and log in
        self.user = User(username='testuser', email='test@example.com', password='testpassword')
        db.session.add(self.user)
        db.session.commit()
        login_user(self.user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_claim(self):
        response = self.client.post('/claims', json={
            'item_id': 1
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Claim created successfully')
        self.assertIn('claim_id', data)

    def test_get_claims(self):
        # Create a claim directly in the database
        claim = Claim(item_id=1, claimant_user_id=self.user.id, status='pending')
        db.session.add(claim)
        db.session.commit()
        
        response = self.client.get('/claims')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['item_id'], 1)
        self.assertEqual(data[0]['claimant_user_id'], self.user.id)
        self.assertEqual(data[0]['status'], 'pending')

if __name__ == '__main__':
    unittest.main()

