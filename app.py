from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename
import requests
from flask import send_file,Response
import DB

conn = sqlite3.connect('database.db')

app = Flask(__name__)
app.secret_key = 'asdf@1234'
UPLOAD_FOLDER = 'static/product_images'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return "Jay Shree Shyam || Jay Shree Radhe || Om Shree Shivaye Namastubhyam || Jay Shree Ram || Jay Shree Ram Jay Hanuman"

@app.route('/search',methods=['POST'])
def search():
    search = request.form['search']
    conn = sqlite3.connect('database.db')
    try:
        cur = conn.cursor()
        data = cur.execute("SELECT * FROM products").fetchall()
        conn.close()
        s_products = []

        if search == "":
            return data

        for i in data:
            if search in i[1]:
                s_products.append(i)
        if s_products == []:
            return "No Result"
    except:
        msg = "Error Occur"
        return msg
    return s_products     


# API For customer_signup
@app.route('/customer_signup',methods=['POST'])
def customer_signup():
    if request.method == 'POST':
        res = request.get_json()
        try:
            password = res['password']
            email = res['email']
            first_name = res['firstName']
            last_name = res['lastName']
            address = res['address']
            city = res['city']
            state = res['state']
            country = res['country']
            phone = res['phone']
        except KeyError:
            return "Error: missing fields in request"

        try:
            with sqlite3.connect('database.db') as conn:
                cur = conn.cursor()
                emails = cur.execute("SELECT email FROM customer WHERE email IS NOT NULL").fetchall()
                if email in emails:
                    return "Error: email already registered"
                cur.execute("INSERT INTO customer (password, email, firstName, lastName, address, city, state, country, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (hashlib.md5(password.encode()).hexdigest(), email, first_name, last_name, address, city, state, country, phone))
                conn.commit()
                return "Success: customer registered"
        except sqlite3.Error as e:
            return f"Error: {e}"


# API For seller_signup
@app.route('/seller_signup',methods=['POST'])
def seller_signup():
    if request.method == 'POST':
        res = request.get_json()
        try:
            password = res['password']
            Email = res['email']
            first_name = res['firstName']
            last_name = res['lastName']
            store_name = res['store_name']
            address = res['address']
            city = res['city']
            state = res['state']
            country = res['country']
            phone = res['phone']
        except KeyError:
            return "Error: missing fields in request"

        try:
            with sqlite3.connect('database.db') as conn:
                cur = conn.cursor()
                emails = cur.execute("SELECT email FROM seller WHERE email IS NOT NULL").fetchall()
                if Email in emails:
                    return "Error: email already registered"
                cur.execute("INSERT INTO seller (password, email, firstName, lastName,store_name, address, city, state, country, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (hashlib.md5(password.encode()).hexdigest(), Email, first_name, last_name,store_name, address, city, state, country, phone))
                conn.commit()
                return "Success: Seller registered"
        except sqlite3.Error as e:
            return f"Error: {e}"

# API For show_products
@app.route('/show_products',methods=['POST','GET'])
def show_products():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM products')
        products = cur.fetchall()
        return products


def is_valid_customer(email, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM customer')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False

def is_valid_seller(email, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM seller')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def getLoginDetails_customer():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    if 'email' not in session:
        customerId = ""
        firstName = ""
        email = ""
        loggedIn = False
    else:
        cur.execute("SELECT customerId, firstName,email FROM customer WHERE email = '" + session['email'] + "'")
        result = cur.fetchone()
        if result:
            customerId, firstName, email = result
            loggedIn = True
        else:
            customerId = ""
            firstName = ""
            email = ""
            loggedIn = False
    conn.close()
    return (customerId, firstName, email, loggedIn)

def getLoginDetails_seller():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    if 'email' not in session:
        sellerId = ""
        firstName = ""
        email = ""
        loggedIn = False
    else:
        cur.execute("SELECT seller_Id, firstName,email FROM seller WHERE email = '" + session['email'] + "'")
        result = cur.fetchone()
        if result:
            sellerId, firstName, email = result
            loggedIn = True
        else:
            sellerId = ""
            firstName = ""
            email = ""
            loggedIn = False
    conn.close()
    return (sellerId, firstName, email, loggedIn)


# API For Customer_Login
@app.route('/customer_login', methods=['POST'])
def customer_login():
    email = request.form['email']
    password = request.form['password']

    if is_valid_customer(email, password):
        session['email'] = email
        return redirect(url_for('show_products'))
    else:
        error = 'Invalid email / Password'
        return error

# API For Seller_Login
@app.route('/seller_login', methods=['POST'])
def seller_login():
    email = request.form['email']
    password = request.form['password']

    if is_valid_seller(email, password):
        session['email'] = email
        return redirect(url_for('show_products'))
    else:
        error = 'Invalid email / Password'
        return error

@app.route('/profile',methods=['POST','GET'])
def profile():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    customerId,firstName,email,loggedIn = getLoginDetails_customer()

    if customerId == "":
        sellerId,firstName,email,loggedIn = getLoginDetails_seller()
        cur.execute("SELECT * FROM seller WHERE seller_Id='"+ str(sellerId) +"' ")
        data = cur.fetchall()
    else:
        cur.execute("SELECT * FROM customer WHERE customerId='"+ str(customerId) +"' ")
        data = cur.fetchall()
    conn.close()
    return data

@app.route('/your_order')
def your_order():
    customerId,firstName,email,loggedIn = getLoginDetails_customer()
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT productId FROM Orders WHERE customerId='"+ str(customerId) +"' ")
    data = cur.fetchall()

    if data == []:
        return "No orders"

    productIds = []
    for row in data:
        productIds.append(row[0])

    order_products = []
    for productId in productIds:
        p = cur.execute("SELECT * FROM products WHERE productId='"+ str(productId) +"' ").fetchall()
        order_products.append(p[0])

    conn.close()
    return order_products

@app.route('/your_products')
def your_products():
    sellerId,firstName,email,loggedIn = getLoginDetails_seller()
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE seller_email='"+ email +"' ")
    data = cur.fetchall()
    conn.close()
    return data

#### NO DATA INSERT INTO ORDER TABLE 
@app.route('/place_order',methods=['POST'])
def place_order():
    customerId,firstName,customer_email,loggedIn = getLoginDetails_customer()
    if loggedIn == False:
        return "You are not logged in!"

    productId = request.args.get('productId')
    customerId = customerId

    conn = sqlite3.connect('database.db')
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO Orders (productId,customerId) VALUES (?,?) ",(productId,customerId))
        conn.commit()
        msg = "Order placed"
    except sqlite3.OperationalError as e:
        msg = f"Error occurred: {e}"
        conn.rollback()
    finally:
        conn.close()
        return msg

# API For Upload Products
@app.route('/add_product', methods=['POST'])
def upload():
    name = request.form['name']
    price = request.form['price']
    stock = request.form['stock']
    description = request.form['description']
    file = request.files['file']
    # Validate the form data
    if not name or not description or not price:
        msg = 'Please enter all required fields'
        return msg
    if file and not allowed_file(file.filename):
        msg = 'Invalid file extension'
        return msg

    # If the data is valid, insert a new row into the database
    with sqlite3.connect('database.db') as conn:
        try:
            c = conn.cursor()
            c.execute("INSERT INTO products (name, description, price, image, stock) VALUES (?, ?, ?, ?, ?)",(name, description, price, file.filename, stock))
            conn.commit()
            # Save the image file
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            msg = "Successfully Uploaded"
        except:
            conn.rollback()
            msg = 'Error Occur'
    conn.close()
    return msg

@app.route("/logout")
def logout():
    session.pop('email', None)
    return "You LoggedOut!!!!!!!!!!"

if __name__ == "__main__":
    DB.database()
    app.run(debug = True)
