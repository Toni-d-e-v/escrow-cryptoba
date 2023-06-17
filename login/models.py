from flask_login import UserMixin
from login import db
import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    tron_address = db.Column(db.String(120), unique=False, nullable=False)
    bep20_address = db.Column(db.String(120), unique=False, nullable=False)
    telegram_username = db.Column(db.String(120), unique=False, nullable=False)
    admin = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    def __repr__(self) -> str:
        return f"User {self.username}"

# THis is escrow app]

# created_by_user: str
# created_by_user_id: int
# buyer_user_id: int
# status: str
# amount: float
# description: str
# created_at: datetime


class Escrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_by_user = db.Column(db.String(80), unique=False, nullable=False)
    created_by_user_id = db.Column(db.Integer, unique=False, nullable=False)
    buyer_user_id = db.Column(db.Integer, unique=False, nullable=False)
    status = db.Column(db.String(80), unique=False, nullable=False)
    amount = db.Column(db.Float, unique=False, nullable=False)
    description = db.Column(db.String(80), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, unique=False, nullable=False)
    verified = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    def __repr__(self) -> str:
        return f"Escrow {self.id}"



def add_escrow(created_by_user: str, created_by_user_id: int, buyer_user_id: int, status: str, amount: float, description: str) -> None:
    created_at = datetime.datetime.now()


    db.session.add(Escrow(created_by_user=created_by_user, created_by_user_id=created_by_user_id, buyer_user_id=buyer_user_id, status=status, amount=amount, description=description, created_at=created_at, verified=False))
    db.session.commit()
    return "Escrow is created"

def get_escrow(id: int) -> Escrow:
    return Escrow.query.get(int(id))

def get_escrows() -> list:
    escorws = []
    for escrow in Escrow.query.all():

        escorws.append(escrow)
    return escorws


def get_escrows_by_user_id(user_id: int) -> list:
    return Escrow.query.filter_by(buyer_user_id=user_id).all()

def get_escrows_by_created_by_user_id(user_id: int) -> list:
    return Escrow.query.filter_by(created_by_user_id=user_id).all()

def get_escrows_by_status(status: str) -> list:
    return Escrow.query.filter_by(status=status).all()

def close_escrow(id: int) -> None:
    escrow = get_escrow(id)
    escrow.status = "closed"
    db.session.commit()

def getUser(id: str) -> User:
    return User.query.filter_by(id=id).first()



def verify_escrow(id: int) -> None:
    escrow = get_escrow(id)
    escrow.verified = True
    db.session.commit()

def get_users() -> list:
    return User.query.all()

def change_password(id: int, password: str) -> None:
    user = getUser(id)
    user.password = password
    db.session.commit()

def change_email(id: int, email: str) -> None:
    user = getUser(id)
    user.email = email
    db.session.commit()

def change_telegram_username(id: int, telegram_username: str) -> None:
    user = getUser(id)
    user.telegram_username = telegram_username
    db.session.commit()

def change_tron_address(id: int, tron_address: str) -> None:
    user = getUser(id)
    user.tron_address = tron_address
    db.session.commit()

def change_bep20_address(id: int, bep20_address: str) -> None:
    user = getUser(id)
    user.bep20_address = bep20_address
    db.session.commit()

def remove_escrow(id: int) -> None:
    escrow = get_escrow(id)
    db.session.delete(escrow)
    db.session.commit()
    