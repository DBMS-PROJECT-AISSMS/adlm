from app import db
from app.models import Beneficiary
from datetime import datetime

def add_beneficiary(user_id, name, relationship, email):
    """Add a new beneficiary."""
    new_beneficiary = Beneficiary(
        user_id=user_id,
        name=name,
        relationship=relationship,
        email=email,
        created_at=datetime.now()
    )
    db.session.add(new_beneficiary)
    db.session.commit()
    return new_beneficiary

def modify_beneficiary(beneficiary_id, name=None, relationship=None, email=None):
    """Modify an existing beneficiary."""
    beneficiary = db.session.query(Beneficiary).filter_by(beneficiary_id=beneficiary_id).first()
    if beneficiary:
        if name:
            beneficiary.name = name
        if relationship:
            beneficiary.relationship = relationship
        if email:
            beneficiary.email = email
        db.session.commit()
        return beneficiary
    return None

def delete_beneficiary(beneficiary_id):
    """Delete a beneficiary."""
    beneficiary = db.session.query(Beneficiary).filter_by(beneficiary_id=beneficiary_id).first()
    if beneficiary:
        db.session.delete(beneficiary)
        db.session.commit()
        return True
    return False

def view_beneficiaries(user_id):
    """View all beneficiaries of a user."""
    return db.session.query(Beneficiary).filter_by(user_id=user_id).all()
