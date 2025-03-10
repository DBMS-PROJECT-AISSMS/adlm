from app import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")  # "user" or "beneficiary"
    is_deceased = db.Column(db.Boolean, default=False)  # Death verification

class DigitalAsset(db.Model):
    asset_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    asset_name = db.Column(db.String(255), nullable=False)
    asset_type = db.Column(db.String(100), nullable=False)
    asset_url = db.Column(db.Text, nullable=False)
    is_encrypted = db.Column(db.Boolean, default=False)

class Beneficiary(db.Model):
    beneficiary_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    relationship = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class AssetTransfer(db.Model):
    transfer_id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey("digital_asset.asset_id"), nullable=False)
    beneficiary_id = db.Column(db.Integer, db.ForeignKey("beneficiary.beneficiary_id"), nullable=False)
    transferred = db.Column(db.Boolean, default=False)
