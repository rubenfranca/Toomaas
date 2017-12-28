from flask import Flask, jsonify
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, update
from tabledef import *
import xmlrpclib
import json
from SimpleXMLRPCServer import SimpleXMLRPCServer
from configs import *

engine = create_engine('sqlite:///tutorial.db', echo=True)
Session = sessionmaker(bind=engine)
s = Session()

def autenticar(user,pw):
    query = s.query(User).filter(User.username.in_([user]), User.password.in_([pw]) )
    result = query.first()
    if result:
        return True
    else:
        return False

def get_user_id(user):
    query = s.query(User).filter(User.username.in_([user]))
    result = query.first()
    if result:
        return result.id
    else:
        return 0
    
    
def get_reservas():
    b = s.query(Reserva.id, Reserva.dia_hora, Reserva.data_pagamento)
    a = []
    for row in b:
        a.append(row.id) 
    return a

def get_reserva(id):
    b = s.query(Reserva).filter(Reserva.id.in_([id]))
    result = b.first()
    a = []
    a.append(result.id)
    a.append(result.dia_hora)
    a.append(result.data_pagamento)
    return a

def criar_reserva(sala_id,cliente_id,dia_hora):
    reserva = Reserva(dia_hora, sala_id, cliente_id)
    s.add(reserva)
    failed=False
    try:
        s.commit()
    except Exception as e:
        failed=True
    if not failed:
        return True
    else:
        return False

def pagamento_reserva(id_reserva):
    data_agora = datetime.now()
    data_agora_str = data_agora.strftime('%d/%m/%Y')
    #s.query().filter(Reserva.id == id_reserva).update({"pagamento_feito": 1})
    #s.query(Reserva).filter_by(id=id_reserva).update({"pagamento_feito": 1, "data_pagamento": data_agora_str})
    #updt = update(reservas).where(reservas.c.id==id_reserva).values(pagamento_feito=1)
    conn = sqlite3.connect("tutorial.db")
    c = conn.cursor()
    c.execute("UPDATE reservas SET pagamento_feito = 1 WHERE id =%s" % id_reserva)
    failed=False
    try:
        conn.commit()
    except Exception as e:
        failed=True
    if not failed:
        return True
    else:
        return False

def criar_sala(nome_sala,preco_sala,capacidade_sala):
    sala = Sala(nome_sala, preco_sala, capacidade_sala)
    s.add(sala)
    failed=False
    try:
        s.commit()
    except Exception as e:
        failed=True
    if not failed:
        return True
    else:
        return False
    

server = SimpleXMLRPCServer(("localhost", 8000), allow_none=true)
server.register_function(autenticar, "autenticar")
server.register_function(get_reservas, "get_reservas")
server.register_function(get_reserva, "get_reserva")
server.register_function(criar_reserva, "criar_reserva")
server.register_function(pagamento_reserva, "pagamento_reserva")
server.register_function(get_user_id, "get_user_id")
server.register_function(criar_sala, "criar_sala")
server.serve_forever()