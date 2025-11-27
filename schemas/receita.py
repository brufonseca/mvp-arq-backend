from pydantic import BaseModel
from typing import List, Dict, Any

class ReceitaBuscaSchema(BaseModel):
   """
    Define como representar uma busca. A busca sera feita pela lista de ingredientes
    """
   ingredients: str = "egg, banana"
   excludeIngredients: str = "salt, suggar"

class ReceitaViewSchema(BaseModel):
    """ 
    Define como um registro do diario sera retornado:  data + refeicoes
    """
    receitas: List[str]

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