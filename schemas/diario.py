from datetime import date
from typing import List
from pydantic import BaseModel

from model.diario import Diario


from schemas import RefeicaoSchema


class DiarioSchema(BaseModel):
    """    
    Define como exibir um registro do diario de introducao alimentar
    """
    data_registro: date
    refeicoes: List[RefeicaoSchema]


class DiarioViewSchema(BaseModel):
    """ 
    Define como um registro do diario sera retornado:  data + refeicoes
    """
    data_registro: date = date.today()
    refeicoes: List[RefeicaoSchema]


class DiarioListaSchema(BaseModel):
    """
    Define como retornar uma lista de registros do diario de introducao alimentar
    """
    diarios: List[DiarioSchema]


class DiarioBuscaSchema(BaseModel):
    """
    Define como representar uma busca. A busca sera feita pela data
    """
    data_registro: date = date.today()


class DiarioRemocaoSchema(BaseModel):
    """ 
    Define a estrutura do retorno de uma requisicao de remocao
    """

    mensagem: str


def retorna_lista_diarios(diarios: List[Diario]):
    """ Retorna uma lista de diarios seguindo o schema definido em
        DiarioViewSchema.
    """
    lista_diarios = []
    for diario in diarios:
        diario_resposta = {
            "data_registro": diario.data_registro,
            "refeicoes": []
        }

        for refeicao in diario.refeicoes:
            diario_resposta["refeicoes"].append(
                {
                    "tipo": refeicao.tipo, 
                    "aceitacao": refeicao.aceitacao, 
                    "metodo": refeicao.metodo, 
                    "avaliacao": refeicao.avaliacao, 
                    "comentarios":refeicao.comentarios
                })

        lista_diarios.append(diario_resposta)

    return {
        "diarios": lista_diarios
    }


def retorna_diario(diario: Diario):
    """ Retorna uma representacao de registro do diario de introducao alimentar
    """
    return {
        "data_registro": diario.data_registro,
        "refeicoes": [{"tipo": r.tipo, "aceitacao": r.aceitacao, "metodo": r.metodo, "avaliacao": r.avaliacao, "comentarios":r.comentarios} for r in diario.refeicoes]
    }
