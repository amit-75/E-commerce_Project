from flask import Flask,render_template,url_for,request,session,redirect,flash,jsonify,Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,UserMixin,logout_user
from werkzeug.utils import secure_filename
import uuid
import json

app = Flask(__name__)
app.secret_key = 'ksdjf45'

login_manager = LoginManager()
login_manager.init_app(app)

UPLOAD_FOLDER = 'static/product_images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///e-commerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# create a model/table in database
class customer(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Integer, nullable=False)
    Address = db.Column(db.String(100), nullable=False)
    Pin = db.Column(db.Integer)

    def __repr__(self):
        return self.username

class seller(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Integer, nullable=False)
    store_name = db.Column(db.String(100),unique=True, nullable=False)
    Address = db.Column(db.String(100), nullable=False)
    pin = db.Column(db.Integer)

    def __repr__(self):
        return self.username

class Products(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Product_name = db.Column(db.String(100), nullable=False)
    Price = db.Column(db.Integer, nullable=False)
    Product_image = db.Column(db.String(10000), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.Product_name

class order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(100),nullable=False)
    mob_no = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    seller_email = db.Column(db.String(100),nullable=False)
    customer_email = db.Column(db.String(100),nullable=False)
    address = db.Column(db.String(100),nullable=False)


@login_manager.user_loader
def load_user(id):
    return customer.query.get(int(id))

@app.route('/')
def index():
    return "Jay Shree Shyam || Jay Shree Radhe || Om Shree Shivaye Namastubhyam || Jay Shree Ram || Jay Shree Ram Jay Hanuman"

# API For customer_signup
@app.route('/customer_signup',methods=['POST'])
def customer_signup():
    res = request.get_json()
    username = res['username']
    email = res['email']
    password = res['password']
    address = res['address']
    pin = res['pin']

    new = customer(
        username=username,
        email = email,
        password=password,
        Address=address,
        Pin = pin
               )
    db.session.add(new)
    db.session.commit()
    return username + " has been register succesfully"

# API For seller_signup
@app.route('/seller_signup',methods=['POST'])
def seller_signup():
    res = request.get_json()
    username = res['username']
    email = res['email']
    password = res['password']
    store_name = res['store_name']
    address = res['address']
    pin = res['pin']

    new = seller(
        username=username,
        email = email,
        password=password,
        store_name = store_name,
        Address=address,
        pin = pin
               )
    db.session.add(new)
    db.session.commit()
    return username + " has been register succesfully"

# API For Customer_Login
@app.route('/customer_login', methods=['POST'])
def customer_login():
    res = request.get_json()
    username = res['username']
    password = res['password']

    user = customer.query.filter_by(username=username).first()
    if user and password==user.password:
        login_user(user)
        products = Products.query.all()        
        t_products=[]
        for i in products:
            t_products.append(str(i))
        return jsonify({"products":t_products})
    else:
        return "Incorrect username or password!!"

# API For Seller_Login
@app.route('/seller_login', methods=['POST'])
def seller_login():
    res = request.get_json()
    username = res['username']
    password = res['password']
    user = seller.query.filter_by(username=username).first()
    if user and password==user.password:
        login_user(user)
        return "Hii "+username+"! succesfully logged_in"
    else:
        return "Incorrect username or password!!"

@app.route('/show_products',methods=['POST','GET'])
def show_products():
    products = Products.query.all()
    return render_template('show_products.html',products=products)


@app.route('/place_order',methods=['POST'])
def place_order():
    p_id = request.form.get('p_id')
    quantity = request.form.get('quantity')
    customer_email = request.form.get('customer_email')
    mob_no = request.form.get('mob_no')
    address = request.form.get('address')
    price = request.form.get('price')
    seller_email = request.form.get('seller_email')

    new_order = order(p_id=p_id,quantity=quantity,customer_email=customer_email,mob_no=mob_no,address=address,price=price,seller_email=seller_email)
    db.session.add(new_order)
    db.session.commit()
    return 'Order placed'


# API For Upload Products
@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method=='POST':
        file = request.files['file']
        p_price = request.form.get('Price')
        p_stock = request.form.get('stock')

        if not file and p_stock and p_price:
            return redirect(url_for('upload'))

        filename = secure_filename(file.filename)
        mimetype = file.mimetype

        new_p = Products(Product_image=file.read(),Product_name=filename,Price=p_price,stock=p_stock,)
        db.session.add(new_p)
        db.session.commit()
        flash("Product has been uploaded succesfully..............")
        return render_template('upload.html')
    return render_template('upload.html')



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)