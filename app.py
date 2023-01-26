from flask import *  
import os 
import qrcode
import uuid
from flask import Flask, render_template,request,flash,redirect,url_for,session
import sqlite3

app = Flask(__name__)
app.secret_key="123"
qr_codes={}

con=sqlite3.connect("database.db")
con.execute("create table if not exists work(pid integer primary key,name text,password text,contact integer,mail text)")
con.close()

@app.route('/')
def index1():
    return render_template('index1.html')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from work where name=? and password=?",(name,password))
        data=cur.fetchone()

        if data:
            session["name"]=data["name"]
            session["password"]=data["password"]
            return redirect("customer")
        else:
            flash("Username and Password Mismatch","danger")
    return redirect(url_for("index"))


@app.route('/customer',methods=["GET","POST"])
def customer():
    return render_template("map.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            name=request.form['name']
            password=request.form['password']
            contact=request.form['contact']
            mail=request.form['mail']
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("insert into work(name,password,contact,mail)values(?,?,?,?)",(name,password,contact,mail))
            con.commit()
            flash("Record Added  Successfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return redirect(url_for("index"))
            con.close()

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload',methods=["POST","GET"])
def getData():
    if request.method == 'POST':
        result = request.files['file']
        color = request.form.get('color')
        side = request.form.get('side')
        quantity = request.form.get('quantity')
        #print(color, side, quantity)
        result.save(result.filename)
        #os.remove(result.filename)
        # Create a unique identifier
        unique_id = str(uuid.uuid4())

        # Create the data to be encoded in the QR code, including the unique identifier
        #data = color + side + quantity + " data recieved + unique code next " + unique_id
        # Create the QR code instance
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        data="http://192.168.28.59:5000/scan/" + unique_id
        # Add the data to the QR code
        qr.add_data(data)
        qr.make(fit=True)

        # Create an image from the QR code instance
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image
        img.save("static/qr.png")   
        # Add the identifier to the qr_codes dictionary
        qr_codes[unique_id] = True

    return render_template('payment.html', qr_code_id=unique_id, data=data)

@app.route("/scan/<qr_code_id>")
def scan_qr_code(qr_code_id):
    # Check if the scanned QR code's identifier exists in the qr_codes dictionary
    if qr_codes.get(qr_code_id):
        # remove the scanned qr code from the dictionary
        qr_codes.pop(qr_code_id)
        data="http://192.168.1.15:5000/completed.html"
        return render_template("completed.html", url=data)
    else:
        return render_template("scanned.html")

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",use_reloader=False)
