from flask import Flask, render_template, send_from_directory
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)

app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['Access-Control-Allow-Credentials'] = True

@app.route("/")
def hello():
    return render_template('index.html')


@app.route('/static/files/<path:path>')
def send_files(path):
    return send_from_directory('static/files', path)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port),debug=True)