from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itens = db.Column(db.String(255))
    total = db.Column(db.Float)
    status = db.Column(db.String(50))