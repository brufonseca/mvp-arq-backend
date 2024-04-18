from sqlalchemy import Column, String, Integer, ForeignKey, Date
from model import Base


class Refeicao(Base):

    """
    Classe que representa uma refeicao

    ...

    Atributos
    ---------
    id : int
        codigo unico identificador da refeicao

    tipo : str
        tipo de refeicao oferecida 

    metodo : str
        metodo usado para oferecer os alimentos 

    avaliacao : str
        avaliacao de como foi a refeicao 

    aceitacao : str
        aceitacao da refeicao oferecida

    comentarios : str
        comentarios sobre a refeicao 

    diario : date
        data do registro
        chave estrangeira que relaciona a refeicao com o registro do diario


    """
    __tablename__ = 'refeicao'

    id = Column(Integer, primary_key=True)
    tipo = Column(String(30))
    metodo = Column(String(30))
    avaliacao = Column(String(30))
    aceitacao = Column(String(30))
    comentarios = Column(String(4000))

    diario = Column(Date, ForeignKey("diario.data_registro"), nullable=False)

    def __init__(self, tipo: str, metodo: str, avaliacao: str, aceitacao: str, comentarios: str):
        """
        Cria uma nova refeicao

        Argumentos:
            tipo : tipo de refeicao oferecida
            metodo: metodo usado para oferecer os alimentos
            avaliacao: avaliacao de como foi a refeicao 
            aceitacao: aceitacao da refeicao oferecida
            comentarios:comentarios sobre a refeicao 


        """

        self.tipo = tipo
        self.metodo = metodo
        self.avaliacao = avaliacao
        self.aceitacao = aceitacao
        self.comentarios = comentarios
