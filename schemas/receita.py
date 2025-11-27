from pydantic import BaseModel
from typing import List

class ReceitaBuscaSchema(BaseModel):
   """
    Define como representar uma busca. A busca sera feita pela lista de ingredientes
    """
   ingredientes: str = "eggs"

class ReceitaViewSchema(BaseModel):
    """ 
    Define como um registro do diario sera retornado:  data + refeicoes
    """
    receitas: List[str]