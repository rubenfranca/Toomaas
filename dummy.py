import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time
from datetime import datetime
from tabledef import *
from sqlalchemy import Column, Date, Integer, String, Float, Time, Boolean
import sqlite3

engine = create_engine('sqlite:///tutorial.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
user = User("admin","password", "emailad", "291")
session.add(user)
 
user = User("python","python", "emailp", "292")
session.add(user)
 
user = User("jumpiness","python", "emailjump", "293")
session.add(user)

t = datetime.now()
reserva = Reserva(t.strftime('21/%m/%Y'),1,1)
session.add(reserva)
 
# commit the record the database
session.commit()
 
session.commit()
