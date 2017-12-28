from configs import *
engine = create_engine('sqlite:///tutorial.db', echo=True)
 
app = Flask(__name__)
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html')
 
@app.route('/login', methods=['POST'])
def do_admin_login():
 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    
    proxy = xmlrpclib.ServerProxy("http://localhost:8000/")
    
    session['logged_in'] = proxy.autenticar(POST_USERNAME, POST_PASSWORD)
    session['user_id'] = proxy.get_user_id(POST_USERNAME) 
    return home()
 
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()
 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)

