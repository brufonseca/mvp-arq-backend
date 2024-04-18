from typing import List
from pydantic import BaseModel

from model.refeicao import Refeicao


class RefeicaoSchema(BaseModel):
    """    
    Define como exibir uma refeicao
    """
    tipo: str = "LANCHE_MANHA"
    metodo: str = "BLW"
    avaliacao: str = "SUCESSO"
    aceitacao: str = "OTIMO"
    comentarios: str = ""


class RefeicaoViewSchema(BaseModel):
    """ 
    Define como uma refeicao será retornada:  data + refeicao
    """
    tipo: str = "LANCHE_MANHA"
    metodo: str = "BLW"
    avaliacao: str = "SUCESSO"
    aceitacao: str = "OTIMO"
    comentarios: str


class RefeicaoListaSchema(BaseModel):
    """
    Define como retornar uma lista de refeicoes
    """
    refeicoes: List[RefeicaoSchema]


class RefeicaoRemocaoSchema(BaseModel):
    """ 
    Define a estrutura do retorno de uma requisicao de remocao
    """
    mensagem: str


def retorna_lista_refeicoes(refeicoes: List[Refeicao]):
    """ Retorna uma lista de refeicoes seguindo o schema definido em
        RefeicaoViewSchema.
    """
    lista_refeicoes = []
    for refeicao in refeicoes:
        lista_refeicoes.append({
            "tipo": refeicao.tipo,
            "metodo": refeicao.metodo,
            "avaliacao": refeicao.avaliacao,
            "aceitacao": refeicao.aceitacao,
            "comentarios": refeicao.comentarios
        })

    return {
        "refeicoes": lista_refeicoes
    }


def retorna_refeicao(refeicao: Refeicao):
    """ Retorna uma representação de refeicao seguindo o schema definido em
        RefeicaoViewSchema.
    """
    return {
        "metodo": refeicao.metodo,
        "avaliacao": refeicao.avaliacao,
        "aceitacao": refeicao.aceitacao,
        "comentarios": refeicao.comentarios
    }
