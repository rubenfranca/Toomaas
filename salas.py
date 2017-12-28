# coding=utf-8
from configs import *
app = Flask(__name__)

@app.route('/salas', methods=['GET'])
def lista_salas():    
    engine = create_engine(NOME_BASE_DADOS, echo=True)
    query = engine.execute("select * from salas") 
    #Query the result and get cursor.Dumping that data to a JSON is looked by extension
    result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
    return json.dumps(result)

@app.route('/salas/<sala_id>/reservas', methods=['GET'])
def lista_reservas_sala(sala_id):
    reservas_de_salas = requests.get(ENDERECO+":4001/reservas/sala/{}".format(sala_id)) 
    reservas = reservas_de_salas.json()
    return json.dumps(reservas)
    

@app.route('/salas', methods=['POST'])
def criar_sala():
    POST_NOME = str(request.form['nome_sala'])
    POST_PRECO = int(request.form['preco_sala'])
    POST_CAPACIDADE = int(request.form['capacidade_sala'])
    proxy = xmlrpclib.ServerProxy("http://localhost:8000/")
    if proxy.criar_sala(POST_NOME, POST_PRECO, POST_CAPACIDADE):
        return "sala criada"
    else:
        return "erro ao criar sala"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)
        

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4002)