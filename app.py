from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    img = request.files['fileUpload']
    option = request.form['option']
    
    img_name = img.filename
    
    # Process the image based on the selected option
    # For demonstration, let's assume we're just echoing back the option and image name
    result = f"Option selected: {option}\nImage name: {img_name}"
    return result

if __name__ == '__main__':
    app.run(debug=True)
