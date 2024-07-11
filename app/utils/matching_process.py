from flask import Blueprint, request, jsonify
from ..models.claim import Claim
from ..models.item import Item 
from ..models.match import Match
from app import db
from app.models.db_storage import DBStorage
storage = DBStorage(db)

def find_potential_matches(new_claim):
    items = Item.query.filter_by(status='Found').all()
    print(f"Items found with status 'Found': {[item.id for item in items]}")
    potential_matches = []
    
    for item in items:
        print(f"Checking item: {item.id}")
        if (item.category == new_claim.item.category and
            item.description == new_claim.item.description and
            new_claim.additional_information in item.description):
            print(f"Item {item.id} matches the claim {new_claim.id}")
            potential_matches.append(item)
        else:
            print(f"Item {item.id} does not match the claim {new_claim.id}") 
    
    for item in potential_matches:
        match = Match(
            claim_id=new_claim.id,
            item_id=item.id,
            potential_owner_user_id=item.user_id,# this part 
            status='pending'
        )
        storage.new(match)
    
    storage.save()
    
    return potential_matches

