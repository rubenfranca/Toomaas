from configs import *
from tabledef import Reserva
app = Flask(__name__)

@app.route('/reservas', methods=['GET'])
def lista_reservas():
    engine = create_engine('sqlite:///tutorial.db', echo=True)
    Session = sessionmaker(bind=engine)
    s = Session()
    b = s.query(User)
    query = engine.execute("select * from users") 
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
    result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        
    return json.dumps(result)#[ row.username for row in b ])

@app.route('/reservas', methods=['POST'])
def criar_reserva():
    POST_SALA_ID = int(request.form['sala_id'])
    POST_CLIENTE_ID = int(request.form['cliente_id'])
    POST_DIA_HORA = str(request.form['dia_hora'])
    proxy = xmlrpclib.ServerProxy("http://localhost:8000/")
    if proxy.criar_reserva(POST_SALA_ID,POST_CLIENTE_ID,POST_DIA_HORA):
        return "reserva feita"
    else:
        return "erro na reserva"

@app.route('/reservas/update', methods=['POST'])
def pagamento_reserva():
    POST_RESERVA_ID = str(request.form['id'])
    proxy = xmlrpclib.ServerProxy("http://localhost:8000/")
    if proxy.pagamento_reserva(POST_RESERVA_ID):
        return "pagamento de reserva feita"
    else:
        return "erro no pagamento da reserva"

@app.route('/reservas/<int:id>', methods=['GET'])
def get_reserva(id):
    engine = create_engine('sqlite:///tutorial.db', echo=True)
    Session = sessionmaker(bind=engine)
    s = Session()
    b = s.query(Reserva).filter(Reserva.id.in_([id]))
    return json.dumps([ row._asdict() for row in b ])
    #for item in result:
     #  return jsonify({'id':item})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4001)