# coding=utf-8
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

@app.route("/reservas")
def reservas():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        r = requests.get("http://localhost:4001/reservas")
        html ="<table>"\
               "</table><table><tr><td>id</td><td>dia_hora</td><td>data_pagamento</td></tr>"
        a =r.json()
        max = len(a['data'])
        for i in range(0,max):
            html += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" %(a['data'][i]['id'],a['data'][i]['dia_hora'],a['data'][i]['data_pagamento'])   
        html+= "</table>"
        return render_template('reservas.html', dados=html)

@app.route("/criarReserva", methods=['GET'])
def criar_reserva():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        r = requests.get("http://localhost:4002/salas")
        tabela_sala ="<table class='table table-dark table-hover'>"\
               "<thead><tr><td>nome</td><td>preco</td><td>capacidade</td></tr></thead><tbody>"
        a =r.json()
        max = len(a['data'])
        for i in range(0,max):
            tabela_sala += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" %(a['data'][i]['nome'],a['data'][i]['preco'],a['data'][i]['capacidade'])   
        tabela_sala+= "</tbody></table>"
        
        dropdown_sala = "<select class='form-control' name='sala_id'>"
        for i in range(0,max):
            dropdown_sala += "<option value=%s>%s</option>" %(a['data'][i]['id'],a['data'][i]['nome'])
        dropdown_sala += "</select>"    
        
        return render_template('criarReserva.html', tabela_salas=tabela_sala, dropdown_salas=dropdown_sala)

@app.route("/criarReserva", methods=['POST'])
def criar_reserva_post():
    POST_SALA_ID = int(request.form['sala_id'])
    POST_DIA = str(request.form['dia'])
    POST_HORA = str(request.form['hora'])
    POST_DIA_HORA = POST_HORA+" "+POST_DIA
    r = requests.post("http://localhost:4001/reservas", data= {'sala_id':POST_SALA_ID,'dia_hora':POST_DIA_HORA, 'user_id':session['user_id']})
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4003)