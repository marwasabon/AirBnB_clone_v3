from flask import render_template,Blueprint, request, jsonify, abort
from app import db
from app.models.contact import Contact
from app.models.db_storage import DBStorage, db

main = Blueprint('main', __name__)
storage = DBStorage(db)
@main.route('/')
def home():
    return render_template('index.html')

@main.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = storage.query(Contact)
    contacts_list = [{'id': contact.id, 'name': contact.name, 'created_at': contact.created_at,'updated_at': contact.updated_at,'address': contact.address} for contact in contacts]
    return jsonify(contacts_list)

@main.route('/contacts', methods=['POST'])
def create_contact():
    data = request.get_json()
    new_contact = Contact(name=data['name'], address=data['address'])
    storage.new(new_contact)
    storage.save()
    return jsonify({'message': 'Contact created', 'contact': str(new_contact)}), 201

@main.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    contact = storage.get(Contact, id)
    if contact is None:
        return jsonify({'message': 'Contact not found'}), 404
    return jsonify({'contact': str(contact)})

@main.route('/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    contact = storage.get(Contact, id)
    if contact is None:
        return jsonify({'message': 'Contact not found'}), 404
    data = request.get_json()
    contact.name = data.get('name', contact.name)
    contact.address = data.get('address', contact.address)
    storage.save()
    return jsonify({'message': 'Contact updated', 'contact': str(contact)})

@main.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = storage.get(Contact, id)
    if contact is None:
        return jsonify({'message': 'Contact not found'}), 404
    storage.delete(contact)
    storage.save()
    return jsonify({'message': 'Contact deleted'})
