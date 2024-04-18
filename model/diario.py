from sqlalchemy import Column, Date
from sqlalchemy.orm import relationship

from  model import Base, Refeicao

class Diario(Base):
    """
    Classe que representa um registro do diario de introducao alimentar

    Atributos
    ---------
    data_registro : date
        data do registro
        codigo unico identificador do registro
        campo obrigatorio
    
    refeicoes : list[Refeicao]
        lista das refeicoes ofertadas
        relacao implicita, sera construida pelo SQLAlchemy

    """
    __tablename__ = 'diario'

    data_registro = Column(Date, primary_key = True, unique = True)

    refeicoes = relationship("Refeicao")

    def __init__(self,data_registro):
        """
        Cria um novo registro do diário

        Argumentos:
            data_registro : data do registro


        """
        self.data_registro = data_registro

    
    def adiciona_refeicao(self,refeicao:Refeicao):
        """ 
        Adiciona nova refeicao ao registro do diario 
        
        Argumentos:
            refeicao: refeicao oferecida
            
        """
        self.refeicoes.append(refeicao)


        