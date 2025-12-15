from pydantic import BaseModel
from typing import List, Dict, Any

class ReceitaBuscaSchema(BaseModel):
   """
    Define como representar uma busca. A busca sera feita pela lista de ingredientes
    """
   ingredients: str = "ovo, banana"
   excludeIngredients: str = "sal, açúcar"
   dishType: str = "breakfast"

class ReceitaViewSchema(BaseModel):
    """ 
    Define como uma receita será retornada
    """
    receita: Dict[str, Any]

def retorna_lista_receitas(receitas: List[Dict[str, Any]]):
    list_receitas = []
    for receita in receitas:
        
        instrucoes = ""

        ingredientes = []

        for info_ingrediente in receita.get("extendedIngredients"):
            ingrediente = {
                "nome": info_ingrediente.get("name"),
                "quantidade": info_ingrediente.get("measures").get("metric").get("amount"),
                "unidade":info_ingrediente.get("measures").get("metric").get("unitLong")
            }

            ingredientes.append(ingrediente)


        for instrucao in receita.get("analyzedInstructions"):
            passos = instrucao.get("steps")
            for passo in passos:
                instrucoes+=passo.get("step") + "<br>"

        
        
        nova_receita = {
            "titulo": receita.get("title"),
            "instrucoes": instrucoes,
            "ingredientes": ingredientes
        }

        list_receitas.append(nova_receita)

    return list_receitas

def organiza_estrutura_receita(texto_receita:str):

    """ 
    Estrutura uma receita
    """

    titulo, instrucoes, texto_ingredientes = texto_receita.split("<§§§>")
    ingredientes = texto_ingredientes.split("<<|>>")

    receita = {
        "titulo": titulo,
        "instrucoes": instrucoes,
        "ingredientes": ingredientes
    }

    return receita

