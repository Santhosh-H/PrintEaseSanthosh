from flask import *  
import os 
import qrcode
import uuid

app = Flask(__name__) 


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
        print(color, side, quantity)
        result.save(result.filename)
        #os.remove(result.filename)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",use_reloader=False)

    
def QR_Gen():
    # Create a unique identifier
    unique_id = str(uuid.uuid4())

    # Create the data to be encoded in the QR code, including the unique identifier
    data = "https://www.example.com?id=" + unique_id

    # Create the QR code instance
    qr = qrcode.QRCode(version=1, box_size=10, border=5)

    # Add the data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image
    img.save("qr_code_with_id.png")
