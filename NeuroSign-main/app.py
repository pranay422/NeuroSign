from flask import Flask, render_template
from flask_cors import CORS
from dyslexia_app import dyslexia_bp
from sign_language_app import sign_language_bp



app = Flask(__name__)

CORS(app)
CORS(dyslexia_bp)  

app.register_blueprint(dyslexia_bp)
app.register_blueprint(sign_language_bp)

@app.route('/')
def home():
    return render_template('mainpage.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
