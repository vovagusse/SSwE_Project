from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Payment(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    status = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    card_number = db.Column(db.String(16))
    
    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'amount': self.amount,
            'card_number': self.card_number
        }

@app.route('/payment/init', methods=['POST'])
def init_payment():
    amount = float(request.json['amount'])
    payment_id = str(random.randint(100000, 999999))
    
    payment = Payment(
        id=payment_id,
        status='pending',
        amount=amount
    )
    db.session.add(payment)
    db.session.commit()
    
    return {'payment_id': payment_id}

@app.route('/payment/process/<string:payment_id>', methods=['POST'])
def process_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        return {'error': 'Payment not found'}, 404
    
    card_number = request.json['card_number']
    if len(card_number) != 16 or not card_number.isdigit():
        return {'status': 'error', 'message': 'Invalid card number'}
    
    payment.status = 'success'
    payment.card_number = card_number
    db.session.commit()
    
    return {'status': 'success'}

@app.route('/payment/status/<string:payment_id>')
def get_status(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        return {'error': 'Payment not found'}, 404
        
    return payment.to_dict()
