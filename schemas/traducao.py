from pydantic import BaseModel
from typing import List, Dict, Any

class TraducaoRequisicaoSchema(BaseModel):
   """
    Define como representar uma tradução. 
    """
   texto: str = "sal, açúcar, ovo"
   idioma_origem: str = "pt-BR"
   idioma_destino: str = "en"

class TraducaoViewSchema(BaseModel):
    """ 
    Define como um texto traduzido sera retornado
    """
    texto_traduzido: str