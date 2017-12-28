# coding=utf-8
NOME_BASE_DADOS = 'sqlite:///tutorial.db'
ENDERECO = 'http://127.0.0.1'
from flask import Flask,jsonify
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask import Flask, make_response, flash, redirect, render_template, request, session, abort
import os
from tabledef import *
import xmlrpclib
from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Float, Time, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from SimpleXMLRPCServer import SimpleXMLRPCServer
import sqlalchemy as sa
from sqlalchemy.ext.automap import automap_base
import requests
import json
#from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
from sqlalchemy import func, update
import csv
from flask_bootstrap import Bootstrap
#from flask_login import current_user
