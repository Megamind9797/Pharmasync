

#/////

# import sqlite3

# conn = sqlite3.connect("database.db")
# cur = conn.cursor()

# with open("setup.sql", "r") as f:
#     cur.executescript(f.read())

# conn.commit()
# conn.close()

# print("DB ready 🚀")

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from flask import send_from_directory
import sqlite3
import datetime

import os
import google.generativeai as genai



app = Flask(__name__)
CORS(app)

# ================= DB CONNECT =================
def connect_db():

    
    # he dogh line add kelya ahe for testing
    db_path = os.path.abspath("database.db")

    

    return sqlite3.connect(
        db_path,
        timeout=30,
        check_same_thread=False
        )


# ================= CREATE TABLES =================
conn = connect_db()
cur = conn.cursor()

# cur.execute("PRAGMA table_info(orders)")
# print(cur.fetchall())

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS pharmacies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    latitude REAL,
    longitude REAL,
    owner_id INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    price INTEGER,
    stock INTEGER,
    pharmacy_id INTEGER,
    expiry_date TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    medicine_id INTEGER,
    quantity INTEGER,
    status TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS prescriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    image_name TEXT,
    status TEXT
)
""")
# ================= CREATE TABLES =================



cur.execute("""
    CREATE TABLE IF NOT EXISTS notifications(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        message TEXT
        
        is_read INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

conn.commit()
conn.close()


# ================= HOME =================
@app.route("/")
def home():
    return "Backend Running 🚀"


# ================= REGISTER =================
# ================= REGISTER =================
@app.route("/customer-register", methods=["POST"])
def customer_register():

    data = request.json

    name = data["name"]
    email = data["email"]
    password = data["password"]
    role = data["role"]

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    pharmacy_name = data.get("pharmacy_name")

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO customers(name,email,password,role)
    VALUES(?,?,?,?)
    """, (name,email,password,role))

    user_id = cur.lastrowid

    if role == "Pharmacy Owner":

        cur.execute("""
        INSERT INTO pharmacies
        (name, latitude, longitude, owner_id)
        VALUES (?, ?, ?, ?)
        """,
        (
            pharmacy_name,
            latitude,
            longitude,
            user_id
        ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Registration Successful"
    })

# ================= LOGIN =================
@app.route("/customer-login", methods=["POST"])
def customer_login():

    data = request.json

    email = data["email"]
    password = data["password"]

    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM customers
        WHERE email=? AND password=?
        """,
        (email,password)
    )

    user = cur.fetchone()

    conn.close()

    if user:

        return jsonify({
            "message":"Login Successful",
            "id":user[0],
            "role":user[4]
        })

    return jsonify({
        "message":"Invalid Email or Password"
    })


# ================= ADD PHARMACY =================
@app.route("/add-pharmacy", methods=["POST"])
def add_pharmacy():

    data = request.json

    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO pharmacies
        (name, latitude, longitude, owner_id)
        VALUES (?,?,?,?)
        """,
        (
            data["name"],
            data["latitude"],
            data["longitude"],
            data["owner_id"]
        )
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Pharmacy Added Successfully"})


# ================= ADD MEDICINE =================
@app.route("/add-medicine", methods=["POST"])
def add_medicine():

    data = request.json
    
    print(data)

    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO medicines
        (name,description,price,stock,pharmacy_id,expiry_date)
        VALUES (?,?,?,?,?,?)
        """,
        (
            data["name"],
            data["description"],
            data["price"],
            data["stock"],
            data["pharmacy_id"],
            data["expiry_date"]
        )
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Medicine Added Successfully"})


# ================= UPDATE STOCK =================
@app.route("/update-stock", methods=["POST"])
def update_stock():

    data = request.json

    medicine_id = data.get("medicine_id")
    stock = data.get("stock")

    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE medicines SET stock=? WHERE id=?",
        (stock, medicine_id)
    )

    if int(stock) <= 5:

        cur.execute(
            "SELECT name FROM medicines WHERE id=?",
            (medicine_id,)
        )

        medicine = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO notifications(message)
            VALUES(?)
            """,
            (f"⚠ Low stock alert for {medicine}",)
        )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Stock Updated Successfully"
    })


# ================= UPDATE PRICE =================
@app.route("/update-price", methods=["POST"])
def update_price():

    data = request.json

    medicine_id = data.get("medicine_id")
    price = data.get("price")

    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE medicines SET price=? WHERE id=?",
        (price, medicine_id)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Price Updated Successfully"
    })


# ================= OWNER MEDICINES =================
@app.route("/owner-medicines/<int:owner_id>")
def owner_medicines(owner_id):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT medicines.id,
               medicines.name,
               medicines.description,
               medicines.price,
               medicines.stock,
               medicines.expiry_date
        FROM medicines
        JOIN pharmacies
        ON medicines.pharmacy_id = pharmacies.id
        WHERE pharmacies.owner_id = ?
    """, (owner_id,))

    medicines = cur.fetchall()

    conn.close()

    result = []

    for med in medicines:

        result.append({
            "id": med[0],
            "name": med[1],
            "description": med[2],
            "price": med[3],
            "stock": med[4],
            "expiry_date": med[5]
        })

    return jsonify(result)


# ================= OWNER ORDERS =================
@app.route("/owner-orders/<int:owner_id>")
def owner_orders(owner_id):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT orders.id,
               medicines.name,
               orders.quantity,
               orders.status
        FROM orders
        JOIN medicines
        ON orders.medicine_id = medicines.id
        JOIN pharmacies
        ON medicines.pharmacy_id = pharmacies.id
        WHERE pharmacies.owner_id = ?
    """, (owner_id,))

    orders = cur.fetchall()

    conn.close()

    result = []

    for order in orders:

        result.append({
            "order_id": order[0],
            "medicine": order[1],
            "quantity": order[2],
            "status": order[3]
        })

    return jsonify(result)


# ================= SEARCH =================
@app.route("/search", methods=["GET"])
def search():

    name = request.args.get("name")

    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM medicines WHERE name LIKE ?",
        ('%' + name + '%',)
    )

    medicines = cur.fetchall()

    conn.close()

    result = []

    for m in medicines:

        result.append({
            "id": m[0],
            "name": m[1],
            "description": m[2],
            "price": m[3],
            "stock": m[4],
            "pharmacy_id": m[5],
            "expiry_date": m[6]
        })

    return jsonify(result)


# ================= ORDER =================
@app.route("/order", methods=["POST"])
def place_order():

    cart = request.json

    print(cart)

    conn = connect_db()
    cur = conn.cursor()

    for item in cart:

        medicine_name = item["name"]
        quantity = item["quantity"]
        user_id=item["user_id"]

        # medicine find
        
        pharmacy_id=item["pharmacy_id"]
        cur.execute("""
        SELECT id, stock
        FROM medicines
        WHERE name=?
        AND pharmacy_id=?
        """, (medicine_name,
              pharmacy_id))

        result = cur.fetchone()

        if result is None:
            continue

        medicine_id = result[0]
        stock = result[1]

        # owner id nikal
        cur.execute("""
        SELECT pharmacies.owner_id
        FROM medicines
        JOIN pharmacies
        ON medicines.pharmacy_id = pharmacies.id
        WHERE medicines.id=?
        """, (medicine_id,))

        owner = cur.fetchone()

        if owner:
            owner_id = owner[0]

            cur.execute("""
            INSERT INTO notifications(user_id, message)
            VALUES (?, ?)
            """, (
                owner_id,
                f"New Order For {medicine_name}"
            ))

        # stock check
        if stock < quantity:
            continue

        
        # save order
        cur.execute("""
        INSERT INTO orders
        (user_id, medicine_id, quantity, status)
        VALUES (?, ?, ?, ?)
        """, (
            user_id,
            medicine_id,
            quantity,
            "Placed"
        ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Order Placed Successfully"
    })

    # new order notification
    notification = f"New order placed for {medicine_name}"

    cur.execute(
        """
        INSERT INTO notifications (message)
        VALUES (?)
        """,
        (notification,)
    )

    # low stock notification
    if new_stock <= 5:

        low_stock_msg = f"Low stock alert for {medicine_name}"

        cur.execute(
            """
            INSERT INTO notifications (message)
            VALUES (?)
            """,
            (low_stock_msg,)
        )

    conn.commit()
    conn.close()

    # low stock alert response
    if new_stock <= 5:

        return jsonify({

            "message": "Order Placed Successfully",

            "medicine": medicine_name,

            "remaining_stock": new_stock,

            "warning": "Low Stock Alert"

        })

    # normal success
    return jsonify({

        "message": "Order Placed Successfully",

        "medicine": medicine_name,

        "remaining_stock": new_stock

    })


# ================= EXPIRY ALERT =================
@app.route("/expiry-alert")
def expiry_alert():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT name, expiry_date FROM medicines"
    )

    medicines = cur.fetchall()

    conn.close()

    result = []

    for med in medicines:

        result.append({
            "medicine": med[0],
            "expiry_date": med[1]
        })

    return jsonify(result)


# ================= PRESCRIPTION UPLOAD =================
@app.route("/upload-prescription", methods=["POST"])
def upload_prescription():

    # uploads folder auto create
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    # user id
    user_id = request.form.get("user_id")

    # file check
    if "image" not in request.files:
        return jsonify({
            "message": "No image selected"
        })

    image = request.files["image"]

    # empty filename check
    if image.filename == "":
        return jsonify({
            "message": "No file chosen"
        })

    # save image
    image_path = os.path.join("uploads", image.filename)

    image.save(image_path)

    # database save
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO prescriptions
        (user_id,image_name,status)
        VALUES (?,?,?)
        """,
        (
            user_id,
            image.filename,
            "Pending"
        )
    )

    # notification
    notification = f"New prescription uploaded by user {user_id}"

    cur.execute(
        """
        INSERT INTO notifications (message)
        VALUES (?)
        """,
        (notification,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Prescription Uploaded Successfully",
        "file": image.filename
    })



# ================= VIEW PRESCRIPTIONS =================
@app.route("/prescriptions")
def prescriptions():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM prescriptions"
    )

    data = cur.fetchall()

    conn.close()

    result = []

    for p in data:

        result.append({
            "id": p[0],
            "user_id": p[1],
            "image": p[2],
            "status": p[3]
        })

    return jsonify(result)


# ================= NEAREST =================
@app.route("/nearest", methods=["GET"])
def nearest_pharmacy():

    user_lat = float(request.args.get("lat"))
    user_lon = float(request.args.get("lon"))

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.id, p.name, p.latitude, p.longitude,
               m.name, m.price, m.stock
        FROM pharmacies p
        JOIN medicines m
        ON p.id = m.pharmacy_id
    """)

    data = cur.fetchall()

    conn.close()

    result = []

    for row in data:

        p_id, p_name, lat, lon, med_name, price, stock = row

        distance = (
            (lat - user_lat)**2 +
            (lon - user_lon)**2
        ) ** 0.5

        result.append({
            "pharmacy": p_name,
            "medicine": med_name,
            "price": price,
            "stock": stock,
            "distance": round(distance, 3)
        })

    result.sort(key=lambda x: x["distance"])

    return jsonify(result)


# ================= QR INFO SYSTEM =================

@app.route("/scan/<code>")
def scan_qr(code):

    qr_data = {

        "Calpol": {
            "name": "Calpol",
            "purpose": "Reduces fever and relieves mild pain like headache and toothache",
            "uses": "Used for fever and body pain",
            "precautions": "Do not exceed recommended dose; take with or after food",
            "video": "/static/videos/calpol.mp4"
        },

        "Saradon": {
            "name": "Saradon",
            "purpose": "Relieves headache, migraine, toothache, and muscle pain",
            "uses": "Used for pain relief",
            "precautions": "Avoid excess caffeine intake; take after meals",
            "video": "/static/videos/saradon.mp4"
        },

        "Coldact": {
            "name": "Coldact",
            "purpose": "Relieves cold, nasal congestion, fever, and body ache",
            "uses": "Used for cold and fever",
            "precautions": "Do not exceed prescribed dose; avoid alcohol",
            "video": "/static/videos/coldact.mp4"
        },

        "Chestoncold": {
            "name": "Chestoncold",
            "purpose": "Relieves cold, cough, nasal congestion, and fever",
            "uses": "Used for cough and cold relief",
            "precautions": "Avoid alcohol and driving due to drowsiness",
            "video": "/static/videos/chestoncold.mp4"
        },

        "Azee 500": {
            "name": "Azee 500",
            "purpose": "Treats bacterial infections of throat, lungs, ears, and skin",
            "uses": "Used for bacterial infections",
            "precautions": "Complete full antibiotic course",
            "video": "/static/videos/azee500.mp4"
        },

        "Campicillin": {
            "name": "Campicillin",
            "purpose": "Treats respiratory, urinary, and gastrointestinal infections",
            "uses": "Used for bacterial infections",
            "precautions": "Complete full course; take before or after food as directed",
            "video": "/static/videos/campicillin.mp4"
        },

        "Thyrox": {
            "name": "Thyrox",
            "purpose": "Treats hypothyroidism and maintains thyroid hormone levels",
            "uses": "Used for thyroid hormone replacement",
            "precautions": "Take on empty stomach at same time daily",
            "video": "/static/videos/thyrox.mp4"
        },

        "Okamet 500": {
            "name": "Okamet 500",
            "purpose": "Controls blood sugar in type 2 diabetes",
            "uses": "Used for diabetes management",
            "precautions": "Take regularly with meals and monitor sugar levels",
            "video": "/static/videos/okamet500.mp4"
        },

        "D-Rise 60K": {
            "name": "D-Rise 60K",
            "purpose": "Treats Vitamin D deficiency and strengthens bones",
            "uses": "Used for Vitamin D deficiency",
            "precautions": "Do not overdose; take with food or milk",
            "video": "/static/videos/drise60k.mp4"
        },

        "Pan-D": {
            "name": "Pan-D",
            "purpose": "Reduces acidity, reflux, and indigestion",
            "uses": "Used for acidity and stomach issues",
            "precautions": "Take before breakfast; do not crush capsule",
            "video": "/static/videos/pand.mp4"
        },

        "Cetzine": {
            "name": "Cetzine",
            "purpose": "Relieves allergy symptoms like sneezing and runny nose",
            "uses": "Used for allergies",
            "precautions": "May cause drowsiness",
            "video": "/static/videos/cetzine.mp4"
        },

        "Avil 25": {
            "name": "Avil 25",
            "purpose": "Relieves allergy, itching, and hay fever",
            "uses": "Used for allergy relief",
            "precautions": "Avoid driving due to drowsiness",
            "video": "/static/videos/avil25.mp4"
        },

        "Dolo 650": {
            "name": "Dolo 650",
            "purpose": "Reduces fever and relieves pain",
            "uses": "Used for fever and pain",
            "precautions": "Do not exceed recommended dose",
            "video": "/static/videos/dolo650.mp4"
        },

        "Allegra": {
            "name": "Allegra",
            "purpose": "Relieves allergy symptoms and sneezing",
            "uses": "Used for allergies",
            "precautions": "Avoid fruit juice before taking medicine",
            "video": "/static/videos/allegra.mp4"
        },

        "Albenza": {
            "name": "Albenza",
            "purpose": "Treats worm infections",
            "uses": "Used for deworming",
            "precautions": "Avoid during pregnancy",
            "video": "/static/videos/albenza.mp4"
        },

        "Brufen": {
            "name": "Brufen",
            "purpose": "Relieves pain, inflammation, and fever",
            "uses": "Used for pain and swelling",
            "precautions": "Take with food or milk",
            "video": "/static/videos/brufen.mp4"
        },

        "Dentinox": {
            "name": "Dentinox",
            "purpose": "Relieves infant colic and gas problems",
            "uses": "Used for gas relief in infants",
            "precautions": "Shake well before use",
            "video": "/static/videos/dentinox.mp4"
        },

        "Vermox": {
            "name": "Vermox",
            "purpose": "Treats pinworm and roundworm infections",
            "uses": "Used for worm infections",
            "precautions": "Treat all family members in pinworm infection",
            "video": "/static/videos/vermox.mp4"
        },

        "Sedofan": {
            "name": "Sedofan",
            "purpose": "Relieves cold and allergy symptoms",
            "uses": "Used for cold and allergy relief",
            "precautions": "Avoid in hypertension",
            "video": "/static/videos/sedofan.mp4"
        },

        "Digene": {
            "name": "Digene",
            "purpose": "Relieves acidity, indigestion, and bloating",
            "uses": "Used for acidity and gas",
            "precautions": "Do not exceed recommended dose",
            "video": "/static/videos/digene.mp4"
        }

    }

    # ================= SMART SEARCH =================

    normalised_code = code.strip().lower().replace(" ", "")

    medicine = None

    for key, value in qr_data.items():

        if key.lower().replace(" ", "") == normalised_code:
            medicine = value
            break

    if not medicine:
        return "<h1>Medicine Not Found</h1>"

    # ================= UI =================

    html = f"""

<!DOCTYPE html>

<html>

<head>

    <title>{medicine['name']}</title>

    <style>

        body{{
            font-family:'Segoe UI',sans-serif;
            background:linear-gradient(135deg,#f0fdf9,#eaf6ff);
            padding:40px;
            text-align:center;
        }}

        .card{{
            background:white;
            padding:40px;
            border-radius:25px;
            max-width:900px;
            margin:auto;
            box-shadow:0 10px 30px rgba(0,0,0,0.15);
        }}

        .top-banner{{
            background:linear-gradient(135deg,#00b894,#0984e3);
            color:white;
            padding:25px;
            border-radius:20px;
            margin-bottom:30px;
        }}

        .top-banner h2{{
            font-size:34px;
            margin-bottom:10px;
        }}

        .top-banner p{{
            color:white;
            font-size:18px;
        }}

        .back-button{{
            display:inline-block;
            margin-bottom:25px;
            text-decoration:none;
            background:#00b894;
            color:white;
            padding:12px 25px;
            border-radius:12px;
            font-weight:bold;
            font-size:18px;
            transition:.3s;
        }}

        .back-button:hover{{
            background:#019874;
        }}

        #medicine-name{{
            color:#222;
            font-size:50px;
            margin-bottom:30px;
            font-weight:700;
        }}

        h1{{
            color:#00b894;
            font-size:38px;
            margin-top:30px;
            margin-bottom:15px;
        }}

        p{{
            color:#444;
            font-size:24px;
            line-height:1.8;
            margin-bottom:20px;
        }}

        .info-box{{
            background:#f8fbff;
            border-left:6px solid #00b894;
            padding:20px;
            margin-top:15px;
            border-radius:12px;
        }}

        video{{
            width:100%;
            max-width:700px;
            margin-top:25px;
            border-radius:15px;
            box-shadow:0 5px 15px rgba(0,0,0,0.15);
        }}

    </style>

</head>

<body>

    <div class="card">

        <a href="javascript:history.back()" class="back-button">
            ⬅ Back
        </a>

        <div class="top-banner">

            <h2>Medicine Information Portal</h2>

            <p>
                Learn about uses, precautions and medicine awareness
            </p>

        </div>

        <h1 id="medicine-name">
            💊 {medicine['name']}
        </h1>

        <h1>Purpose</h1>

        <div class="info-box">
            <p>{medicine['purpose']}</p>
        </div>

        <h1>Uses</h1>

        <div class="info-box">
            <p>{medicine['uses']}</p>
        </div>

        <h1>Precautions</h1>

        <div class="info-box">
            <p>⚠ {medicine['precautions']}</p>
        </div>

        <h1>Medicine Awareness Video</h1>

        <video controls>
            <source src="{medicine['video']}" type="video/mp4">
        </video>

    </div>

</body>

</html>

"""

    return render_template_string(html)

# ================= NOTIFICATIONS =================

print("noti")
@app.route("/notifications")
def notifications():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM notifications"
    )

    data = cur.fetchall()
    print("NOTIFICATIONS:",repr(data))

    conn.close()

    result = []

    for n in data:

        result.append({
            "id": n[0],
            "owner_id": n[1],
            "message": n[2],
            
        })

    return jsonify(result)





# ================= ORDER HISTORY =================
@app.route("/order-history/<int:user_id>")
def order_history(user_id):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT orders.id,
               medicines.name,
               orders.quantity,
               orders.status
        FROM orders
        JOIN medicines
        ON orders.medicine_id = medicines.id
        WHERE orders.user_id = ?
    """, (user_id,))

    data = cur.fetchall()

    conn.close()

    result = []

    for order in data:

        result.append({
            "order_id": order[0],
            "medicine": order[1],
            "quantity": order[2],
            "status": order[3]
        })

    return jsonify(result)


# ================= CANCEL ORDER =================
# @app.route("/cancel-order/<int:order_id>", methods=["POST"])
# def cancel_order(order_id):

#     conn = connect_db()
#     cur = conn.cursor()

#     # get order
#     cur.execute("""
#         SELECT medicine_id, quantity, status
#         FROM orders
#         WHERE id=?
#     """, (order_id,))

#     order = cur.fetchone()

#     if not order:

#         conn.close()

#         return jsonify({
#             "message": "Order not found"
#         })

#     medicine_id = order[0]
#     quantity = order[1]
#     status = order[2]

#     # already cancelled
#     if status == "Cancelled":

#         conn.close()

#         return jsonify({
#             "message": "Order already cancelled"
#         })

#     # restore stock
#     cur.execute("""
#         SELECT stock
#         FROM medicines
#         WHERE id=?
#     """, (medicine_id,))

#     stock = cur.fetchone()[0]

#     new_stock = stock + quantity

#     cur.execute("""
#         UPDATE medicines
#         SET stock=?
#         WHERE id=?
#     """, (new_stock, medicine_id))

#     # update order status
#     cur.execute("""
#         UPDATE orders
#         SET status=?
#         WHERE id=?
#     """, ("Cancelled", order_id))

#     conn.commit()
#     conn.close()

#     return jsonify({
#         "message": "Order Cancelled Successfully",
#         "restored_stock": new_stock
#     })


# ================= EDIT MEDICINE =================
@app.route("/edit-medicine/<int:medicine_id>", methods=["POST"])
def edit_medicine(medicine_id):

    data = request.json

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE medicines
        SET name=?,
            description=?,
            price=?,
            stock=?,
            expiry_date=?
        WHERE id=?
    """,
    (
        data["name"],
        data["description"],
        data["price"],
        data["stock"],
        data["expiry_date"],
        medicine_id
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Medicine Updated Successfully"
    })


# ================= DELETE MEDICINE =================
@app.route("/delete-medicine/<int:medicine_id>", methods=["DELETE"])
def delete_medicine(medicine_id):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM medicines
        WHERE id=?
    """, (medicine_id,))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Medicine Deleted Successfully"
    })


# ================= ADMIN USERS =================
@app.route("/admin/users")
def admin_users():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, email, role
        FROM users
    """)

    users = cur.fetchall()

    conn.close()

    result = []

    for user in users:

        result.append({
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "role": user[3]
        })

    return jsonify(result)


# ================= ADMIN PHARMACIES =================
@app.route("/admin/pharmacies")
def admin_pharmacies():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM pharmacies
    """)

    pharmacies = cur.fetchall()

    conn.close()

    result = []

    for p in pharmacies:

        result.append({
            "id": p[0],
            "name": p[1],
            "latitude": p[2],
            "longitude": p[3],
            "owner_id": p[4]
        })

    return jsonify(result)


# ================= ADMIN ORDERS =================
@app.route("/admin/orders")
def admin_orders():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM orders
    """)

    orders = cur.fetchall()

    conn.close()

    result = []

    for order in orders:

        result.append({
            "id": order[0],
            "user_id": order[1],
            "medicine_id": order[2],
            "quantity": order[3],
            "status": order[4]
        })

    return jsonify(result)


# ================= EXPIRY WARNING =================
# @app.route("/expiry-warning")
# def expiry_warning():

#     conn = connect_db()
#     cur = conn.cursor()

#     cur.execute("""
#         SELECT name, expiry_date
#         FROM medicines
#     """)

#     medicines = cur.fetchall()

#     conn.close()

#     result = []

#     for med in medicines:

#         result.append({
#             "medicine": med[0],
#             "expiry_date": med[1],
#             "warning": "Check expiry manually"
#         })

#     return jsonify(result)


# ================= INVOICE =================
@app.route("/invoice/<int:order_id>")
def invoice(order_id):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT orders.id,
               medicines.name,
               medicines.price,
               orders.quantity,
               orders.status
        FROM orders
        JOIN medicines
        ON orders.medicine_id = medicines.id
        WHERE orders.id=?
    """, (order_id,))

    order = cur.fetchone()

    conn.close()

    if not order:

        return jsonify({
            "message": "Order not found"
        })

    total = order[2] * order[3]

    return jsonify({

        "invoice_id": order[0],

        "medicine": order[1],

        "price": order[2],

        "quantity": order[3],

        "total_amount": total,

        "status": order[4]

    })




# ================= SHOW UPLOADS =================
@app.route('/uploads/<filename>')
def uploaded_file(filename):

    return send_from_directory(
        'uploads',
        filename
    )
# ================= DELETE MEDICINE =================
# @app.route("/delete-medicine/<int:medicine_id>",
# methods=["DELETE"])

# def delete_medicine(medicine_id):

#     conn = connect_db()

#     cur = conn.cursor()

#     cur.execute(

#         "DELETE FROM medicines WHERE id=?",

#         (medicine_id,)
#     )

#     conn.commit()

#     conn.close()

#     return jsonify({

#         "message":"Medicine Deleted Successfully"

#     })

# ================= ALL ORDERS =================
# @app.route("/all-orders")
# def all_orders():

#     conn = connect_db()

#     cur = conn.cursor()

#     cur.execute("""

#         SELECT orders.id,
#                medicines.name,
#                orders.quantity,
#                orders.status

#         FROM orders

#         JOIN medicines
#         ON orders.medicine_id = medicines.id

#     """)

#     orders = cur.fetchall()

#     conn.close()

#     result = []

#     for order in orders:

#         result.append({

#             "id": order[0],
#             "medicine": order[1],
#             "quantity": order[2],
#             "status": order[3]

#         })

#     return jsonify(result)

# ================= ALL PHARMACIES =================
@app.route("/all-pharmacies")
def all_pharmacies():

    conn = connect_db()

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM pharmacies"
    )

    pharmacies = cur.fetchall()

    conn.close()

    result = []

    for p in pharmacies:

        result.append({

            "id": p[0],
            "name": p[1],
            "latitude": p[2],
            "longitude": p[3],
            "owner_id": p[4]

        })

    return jsonify(result)


# ================= ALL USERS =================
@app.route("/all-users")
def all_users():

    conn = connect_db()

    cur = conn.cursor()

    cur.execute(
        "SELECT id,name,email,role FROM users"
    )

    users = cur.fetchall()

    conn.close()

    result = []

    for user in users:

        result.append({

            "id": user[0],
            "name": user[1],
            "email": user[2],
            "role": user[3]

        })

    return jsonify(result)



# accept order
@app.route("/accept-order/<int:order_id>", methods=["POST"])
def accept_order(order_id):

    conn = connect_db()
    cur = conn.cursor()

    # user id nikal
    cur.execute("""
    SELECT user_id
    FROM orders
    WHERE id=?
    """, (order_id,))

    user_id = cur.fetchone()[0]

    # order accept
    cur.execute("""
    UPDATE orders
    SET status='Accepted'
    WHERE id=?
    """, (order_id,))

    # notification save
    cur.execute("""
    INSERT INTO notifications(user_id,message)
    VALUES (?,?)
    """,
    (
        user_id,
        "Your order has been accepted ✅"
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message":"Order Accepted"
    })
    
# Reject order
@app.route("/reject-order/<int:order_id>", methods=["POST"])
def reject_order(order_id):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE orders
        SET status='Rejected'
        WHERE id=?
    """, (order_id,))

    conn.commit()
    conn.close()

    return jsonify({
        "message":"Order Rejected"
    })   
    
    
     
@app.route("/profile/<int:user_id>")
def profile(user_id):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
        id,
        name,
        email,
        role,
        phone,
        address
        FROM users
        WHERE id=?
        """,
        (user_id,)
    )

    user = cur.fetchone()

    conn.close()

    if not user:
        return jsonify({
            "message":"User not found"
        })

    return jsonify({

        "id": user[0],
        "name": user[1],
        "email": user[2],
        "role": user[3],
        "phone": user[4],
        "address": user[5]

    })
    
@app.route("/update-profile/<int:user_id>", methods=["POST"])
def update_profile(user_id):

    data = request.json

    conn = connect_db()
    cur = conn.cursor()
    

    print("DATA RECEIVED:", data)

    cur.execute("PRAGMA table_info(users)")
    print(cur.fetchall())
    
    cur.execute("""
    UPDATE users
    SET name=?,
        email=?,
        phone=?,
        address=?
        WHERE id=?
""", (
    data.get("name"),
    data.get("email"),
    data.get("phone"),
    data.get("address"),
    
    user_id
))
    

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Profile Updated Successfully"
    })
    

@app.route("/analytics/<int:owner_id>")
def analytics(owner_id):

    conn = connect_db()
    cur = conn.cursor()

    # Orders

    cur.execute("""
SELECT COUNT(*)
FROM orders
JOIN medicines
ON orders.medicine_id = medicines.id
JOIN pharmacies
ON medicines.pharmacy_id = pharmacies.id
WHERE pharmacies.owner_id=?
AND orders.status='Delivered'
""",(owner_id,))

    total_orders = cur.fetchone()[0]

    # Low Stock

    cur.execute("""
    SELECT COUNT(*)
    FROM medicines
    JOIN pharmacies
    ON medicines.pharmacy_id = pharmacies.id
    WHERE pharmacies.owner_id=?
    AND medicines.stock <= 5
    """,(owner_id,))

    low_stock = cur.fetchone()[0]

    # Revenue

    cur.execute("""
SELECT medicines.price, orders.quantity
FROM orders
JOIN medicines
ON orders.medicine_id = medicines.id
JOIN pharmacies
ON medicines.pharmacy_id = pharmacies.id
WHERE pharmacies.owner_id=?
AND orders.status='Delivered'
""",(owner_id,))

    revenue_data = cur.fetchall()

    total_revenue = 0

    for row in revenue_data:

        total_revenue += row[0] * row[1]

    conn.close()

    return jsonify({

        "total_orders": total_orders,

        "low_stock": low_stock,

        "total_revenue": total_revenue

    })   
    
@app.route("/top-medicines/<int:owner_id>")
def top_medicines(owner_id):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT medicines.name,
           COUNT(orders.id) as total_sales
    FROM orders
    JOIN medicines
    ON orders.medicine_id = medicines.id
    JOIN pharmacies
    ON medicines.pharmacy_id = pharmacies.id
    WHERE pharmacies.owner_id=?
    AND orders.status='Delivered'
    GROUP BY medicines.id
    ORDER BY total_sales DESC
    LIMIT 5
    """,(owner_id,))

    data = cur.fetchall()

    conn.close()

    medicines = []
    sales = []

    for row in data:
        medicines.append(row[0])
        sales.append(row[1])

    return jsonify({
        "medicines": medicines,
        "sales": sales
    })
    
    
@app.route("/sales-analytics/<int:owner_id>")
def sales_analytics(owner_id):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT medicines.name,
           SUM(medicines.price * orders.quantity)
    FROM orders
    JOIN medicines
    ON orders.medicine_id = medicines.id
    JOIN pharmacies
    ON medicines.pharmacy_id = pharmacies.id
    WHERE pharmacies.owner_id=?
    AND orders.status=`Delivered`
    GROUP BY medicines.id
    """,(owner_id,))

    data = cur.fetchall()

    conn.close()

    labels = []
    revenue = []

    for row in data:
        labels.append(row[0])
        revenue.append(row[1] if row[1] else 0)

    return jsonify({
        "labels": labels,
        "revenue": revenue
    })    
    

 
 
@app.route("/clear-notifications", methods=["DELETE"])
def clear_notifications():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM notifications")

    conn.commit()
    conn.close()

    return jsonify({
        "message":"All Notifications Deleted"
    }) 
    

    
@app.route("/expiry-alerts/<int:owner_id>")
def expiry_alerts(owner_id):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT medicines.name,
           medicines.expiry_date
    FROM medicines
    JOIN pharmacies
    ON medicines.pharmacy_id = pharmacies.id
    WHERE pharmacies.owner_id=?
    """, (owner_id,))

    medicines = cur.fetchall()

    alerts = []

    from datetime import datetime

    today = datetime.now().date()

    for med in medicines:

        name = med[0]

        try:
            expiry = datetime.strptime(
                med[1],
                "%Y-%m-%d"
            ).date()

        except:
            expiry = datetime.strptime(
                med[1],
                "%d-%m-%Y"
            ).date()

        days_left = (expiry - today).days

        if days_left <= 30:

            alerts.append({

                "medicine": name,

                "days_left": days_left

            })

    conn.close()

    return jsonify(alerts)
       
@app.route("/medicine-options/<medicine_name>")
def medicine_options(medicine_name):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT
        pharmacies.id,
        pharmacies.name,
        medicines.price,
        medicines.stock

    FROM medicines

    JOIN pharmacies
    ON medicines.pharmacy_id = pharmacies.id

    WHERE medicines.name = ?
    """,(medicine_name,))

    rows = cur.fetchall()

    conn.close()

    result = []

    for row in rows:

        result.append({

            "pharmacy_id": row[0],
            "pharmacy_name": row[1],
            "price": row[2],
            "stock": row[3]

        })

    return jsonify(result)    
    
@app.route("/check-medicines")
def check_medicines():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM medicines")

    rows = cur.fetchall()

    conn.close()

    return jsonify(rows)

@app.route("/check-pharmacy")
def check_pharmacy():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM pharmacies")

    rows = cur.fetchall()

    conn.close()

    return jsonify(rows)

 
@app.route("/check-added")
def check_added():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT
    name,
    pharmacy_id,
    stock,
    price
    FROM medicines
    ORDER BY id DESC
    LIMIT 10
    """)

    data = cur.fetchall()

    conn.close()

    return jsonify(data)

@app.route("/all-medicines")
def all_medicines():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT name, price, stock
        FROM medicines
    """)

    rows = cur.fetchall()

    conn.close()

    return jsonify(rows)

@app.route("/all-orders")
def all_orders():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM orders")

    rows = cur.fetchall()

    conn.close()

    return jsonify(rows)

@app.route("/user-orders/<int:user_id>")
def user_orders(user_id):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT
        orders.id,
        medicines.name,
        orders.quantity,
        orders.status
    FROM orders
    JOIN medicines
    ON medicines.id = orders.medicine_id
    WHERE orders.user_id = ?
    AND orders.customer_deleted=0
    """, (user_id,))

    rows = cur.fetchall()

    conn.close()

    return jsonify(rows)

@app.route("/cancel-order/<int:order_id>",
methods=["POST"])
def cancel_order(order_id):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    UPDATE orders
    SET status='Cancelled'
    WHERE id=?
    """,(order_id,))

    conn.commit()
    conn.close()

    return jsonify({
        "message":"Order Cancelled"
    })


# Assign Delivery
@app.route("/assign-delivery/<int:order_id>", methods=["POST"])
def assign_delivery(order_id):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE orders
        SET status='Assigned'
        WHERE id=?
    """, (order_id,))

    conn.commit()
    conn.close()

    return jsonify({"message":"Assigned To Delivery"})



# Out For Delivery
@app.route("/out-for-delivery/<int:order_id>", methods=["POST"])
def out_for_delivery(order_id):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE orders
        SET status='Out For Delivery'
        WHERE id=?
    """, (order_id,))

    conn.commit()
    conn.close()

    return jsonify({"message":"Out For Delivery"})



# Delivered
@app.route("/deliver-order/<int:order_id>", methods=["POST"])
def deliver_order(order_id):

    conn = connect_db()
    cur = conn.cursor()
    
    
    
    cur.execute("""
    SELECT medicine_id, quantity
    FROM orders
    WHERE id=?
    """, (order_id,))

    order = cur.fetchone()

    medicine_id = order[0]
    quantity = order[1]

    cur.execute("""
    SELECT stock
    FROM medicines
    WHERE id=?
    """, (medicine_id,))

    stock = cur.fetchone()[0]

    new_stock = stock - quantity
    
    # order=cur.fetchone()
    # if not order:
    #     return jsonify({
    #         "message":"Order not Found"
    #     })

    cur.execute("""
    UPDATE medicines
    SET stock=?
    WHERE id=?
    """, (new_stock, medicine_id))

    cur.execute("""
        UPDATE orders
        SET status='Delivered'
        WHERE id=?
    """, (order_id,))

    conn.commit()
    conn.close()

    return jsonify({"message":"Order Delivered"})


@app.route("/notifications/<int:user_id>")
def get_notifications(user_id):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT message
    FROM notifications
    WHERE owner_id=?
    ORDER BY id DESC
    """,(user_id,))

    rows = cur.fetchall()

    conn.close()

    return jsonify(rows)

@app.route("/delete-order/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE orders
        SET customer_deleted=1
        WHERE id=?
    """, (order_id,))

    conn.commit()
    conn.close()

    return jsonify({
        "message":"Order Deleted"
    })
@app.route("/check-customers")
def check_customers():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM customers")

    rows = cur.fetchall()

    conn.close()

    return jsonify(rows)    
    
@app.route("/check-users")
def check_users():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")

    data = cur.fetchall()

    conn.close()

    return jsonify(data)

@app.route("/owner-pharmacy/<int:owner_id>")
def owner_pharmacy(owner_id):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM pharmacies WHERE owner_id=?",
        (owner_id,)
    )

    pharmacy = cur.fetchone()

    conn.close()

    if pharmacy:
        return jsonify({
            "pharmacy_id": pharmacy[0]
        })

    return jsonify({
        "message":"No pharmacy found"
    })

  
    
if __name__ == "__main__":
    app.run(debug=True)   







