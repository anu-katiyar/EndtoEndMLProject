from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to home page"

@app.route('/home', methods=['GET', 'POST'])
def home():
    if method == 'GET':
        return render_template('home.html')
    else:  
        return render_template('home.html')



if __name__ == '__main__': 
    main()
    #app.run('0.0.0.0', port =80, debug=True)