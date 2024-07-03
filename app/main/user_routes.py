#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users """
from flask import Blueprint, request, jsonify
from ..models.user import User
from flask import render_template,Blueprint, request, jsonify, abort
from app import db
from app.models.db_storage import DBStorage
# usecase for when username already exist
user_bp = Blueprint('user_bp', __name__)
storage = DBStorage(db)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(username=data['username'], email=data['email'],password=data['password'])
    db.session.add(user)
    db.session.save()
    return jsonify({ 'message': 'User created successfully','id': user.id, 'username': user.username, 'password': user.password,'email': user.email}), 201

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email,  'password': user.password,} for user in users])

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.password = data.get('password', user.password)
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    db.session.save()
    return jsonify({'message': 'User Updated successfully','id': user.id, 'username': user.username, 'email': user.email})

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.save()
    return jsonify({'message': 'User deleted'})
