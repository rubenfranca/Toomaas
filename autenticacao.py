from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

def autenticar(user,pw):
    engine = create_engine('sqlite:///tutorial.db', echo=True)
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([user]), User.password.in_([pw]) )
    result = query.first()
    if result:
        return True
    else:
        return False

server = SimpleXMLRPCServer(("localhost", 8000))
server.register_function(autenticar, "autenticar")
server.serve_forever()