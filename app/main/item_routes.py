from flask import Blueprint, request, jsonify
from ..models.item import Item 
from ..models.user import User
from flask import render_template,Blueprint, request, jsonify, abort
from app import db
from app.models.db_storage import DBStorage

item_bp = Blueprint('item_bp', __name__)
storage = DBStorage(db)


@item_bp.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = Item(
            description=data['description'],
            category=data['category'],
            status=data['status'],
            date_reported=data.get('date_reported'),
            user_id=data['user_id'])
    db.session.add(new_item)
    db.session.commit()
    #fix check if user exists
    return jsonify({
        'message': 'Item created successfully',
        'item': {
            'id': new_item.id,
            'description': new_item.description,
            'category': new_item.category,
            'status': new_item.status,
            'date_reported': new_item.date_reported.isoformat(),
            'user_id': new_item.user_id
        }
    }), 201

@item_bp.route('/items', methods=['GET'])
def search_items():
    status = request.args.get('status')
    category = request.args.get('category')
    keyword = request.args.get('keyword')

    query = Item.query
    if status:
        query = query.filter(Item.status == status)
    if category:
        query = query.filter(Item.category == category)
    if keyword:
        query = query.filter(Item.description.contains(keyword))

    items = query.all()
    return jsonify([{'id': item.id, 'description': item.description, 'category': item.category,
        'status': item.status, 'date_reported': item.date_reported.isoformat(),
        'User': {
            'id': item.user.id,
            'username': item.user.username
        } if item.user else 'NO-user'# fix
        }for item in items])
