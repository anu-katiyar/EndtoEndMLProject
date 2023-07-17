from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to home page"

@app.route('/home', methods=['GET', 'POST'])
def home():
    return rendertemplate('home.html')


if __name__ == '__main__': 
    app.run('0.0.0.0', port =80, debug=True)