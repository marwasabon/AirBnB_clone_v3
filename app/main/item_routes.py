from flask import Blueprint, request, jsonify, send_from_directory

from app.models.claim import Claim
from ..models.item import Item 
from ..models.user import User
from flask import render_template,Blueprint, request, jsonify, abort
from app import db
from app.models.db_storage import DBStorage
from flask_wtf.csrf import generate_csrf

item_bp = Blueprint('item_bp', __name__)
storage = DBStorage(db)

import os
from flask import Blueprint, request, redirect, url_for, flash, render_template, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from ..models.item import Item
from ..utils.forms import ItemUploadForm
from app import db

#item_bp = Blueprint('item_bp', __name__)

 
@item_bp.route('/upload_item', methods=['GET', 'POST'])
@login_required
def upload_item():
    form = ItemUploadForm()
    if form.validate_on_submit():
        file = form.image.data
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            new_item = Item(
                name=form.name.data,
                description=form.description.data,
                category=form.category.data,
                status=form.status.data,
                image_url=file_path,
                user_id=current_user.id
            )
            storage.new(new_item)
            storage.save()
            flash('Item uploaded successfully!', 'success')
            return redirect(url_for('item_bp.list_items'))
    return render_template('upload_item.html', form=form)

@item_bp.route('/items', methods=['GET'])
def list_items():
    items = Item.query.all()
    return render_template('list_items.html', items=items)

@item_bp.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = Item(
            description=data['description'],
            category=data['category'],
            status=data['status'],
            name=data['name'],
            date_reported=data.get('date_reported'),
            user_id=data['user_id'])
    storage.new(new_item)
    storage.save()
    #fix check if user exists -- done 
    return jsonify({
        'message': 'Item created successfully',
        'item': {
            'id': new_item.id,
            'name': new_item.name,
            'description': new_item.description,
            'category': new_item.category,
            'status': new_item.status,
            'date_reported': new_item.date_reported.isoformat(),
            'user_id': new_item.user_id
        }
    }), 201
#@csrf_exempt   
@item_bp.route('/items/claim', methods=['POST'])
@login_required
def claim_item():
    item_id = request.form.get('item_id')
    item = Item.query.get_or_404(item_id)
    new_claim = Claim(item_id=item.id, user_id=current_user.id, status='pending', additional_information=request.form.get('additional_information'))
    db.session.add(new_claim)
    db.session.commit()
    flash('Item claimed successfully', 'success')
    return redirect(url_for('item_bp.list_items'))

@item_bp.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

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
        'name': item.name,
        'User': {
            'id': item.user.id,
            'username': item.user.username
            } if item.user else 'NO-user'# fix
        }for item in items])

@item_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify({'id': item.id, 'name': item.name, 'description': item.description})

@item_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json()
    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    storage.save()
    return jsonify({'id': item.id, 'name': item.name, 'description': item.description})

@item_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    storage.delete(item)
    storage.save()
    return jsonify({'message': 'Item deleted'})

@item_bp.route('/upload', methods=['POST'])
def upload_file():
    """ routes when uploading images that is saved in the folder images"""
    None
