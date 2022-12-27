from flask import Flask,render_template,url_for,request,session,redirect,flash,jsonify,Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,UserMixin,logout_user
app = Flask(__name__)

# Create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///e-commerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class customer(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Integer, nullable=False)
    Address = db.Column(db.String(100), nullable=False)
    Pin = db.Column(db.Integer)

    def __repr__(self):
        return self.username

@app.route('/customer_login', methods=['POST'])
def customer_login():
    username = 'Aksaini'
    user = customer.query.filter_by(username=username).first()
    print(user)
    return 'succesfully run'

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)