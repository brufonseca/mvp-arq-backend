from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# importando os elementos definidos no modelo
from model.base import Base
from model.refeicao import Refeicao
from model.diario import Diario


db_path = "database/"

if not os.path.exists(db_path):
   os.makedirs(db_path)


# string de acesso ao bd
db_url = 'sqlite:///%s/database.sqlite3' % db_path

# criacao de um engine de conexao com o bd
engine = create_engine(db_url)

# criacao de uma sessao do bd
Session = sessionmaker(engine)

# cria o bd, caso não exista
if not database_exists(engine.url):
    create_database(engine.url) 

# cria as tabelas do bd, caso não existam
Base.metadata.create_all(engine)