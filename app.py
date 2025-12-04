import os
import json
import requests

from sqlite3 import IntegrityError
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request


from model import Session, Diario, Refeicao
from logger import logger

from schemas.diario import (
    DiarioSchema, DiarioViewSchema, DiarioListaSchema,
    DiarioRemocaoSchema, DiarioBuscaSchema,
    retorna_diario, retorna_lista_diarios
)

from schemas.receita import (ReceitaBuscaSchema, ReceitaViewSchema, retorna_lista_receitas, organiza_estrutura_receita)

from schemas.traducao import (TraducaoRequisicaoSchema, TraducaoViewSchema)

from schemas.error import ErrorSchema
from flask_cors import CORS

from dotenv import load_dotenv


load_dotenv()

info = Info(title="Diário Introdução Alimentar API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


#definindo api keys

SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY')
GOOGLE_TRANSLATE_API_KEY = os.getenv('GOOGLE_TRANSLATE_API_KEY')

if not SPOONACULAR_API_KEY:
    raise RuntimeError("SPOONACULAR_API_KEY não encontrada nas variáveis de ambiente")

# definindo tags
home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
diario_tag = Tag(
    name="Diário", description="Adição, visualização e remoção de registros do diário de introdução alimentar")

receita_tag = Tag(name="Receitas", description="Busca de receitas usando a API Spoonacular")

traducao_tag = Tag(name="Tradução", description="Tradução de textos usando a API Google Translate")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentacao.
    """
    return redirect('/openapi')


@app.post('/inserir_diario', tags=[diario_tag],
          responses={"200": DiarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def insert_entrada_diario(body:DiarioSchema):
    """Adiciona um novo registro do diario de introducao alimentar

    Retorna uma representação do registro e das refeicoes associadas
    
    """
    data_registro = body.data_registro

    diario = Diario(data_registro)

    lista_refeicoes_brutas = body.refeicoes

    for refeicao_bruta in lista_refeicoes_brutas:
        refeicao = Refeicao(
            refeicao_bruta.tipo,
            refeicao_bruta.metodo,
            refeicao_bruta.avaliacao,
            refeicao_bruta.aceitacao,
            refeicao_bruta.comentarios
        )
        diario.adiciona_refeicao(refeicao)

    logger.debug("Adicionando entrada para a data: %s", diario.data_registro)
    try:
        # criando conexao com o bd
        session = Session()
        # adicionando instancia de diario
        session.add(diario)
        # realizando o commit da transacao
        session.commit()
        logger.debug("Adicionando entrada para a data: %s",
                     diario.data_registro)
        return retorna_diario(diario), 200

    except IntegrityError as e:
        # considerando que duplicidade de data e a causa do IntegrityError
        error_msg = "Registro com mesma data ja salvo na base :/"
        logger.warning(
            "Erro ao adicionar registro para a data %s, %s", diario.data_registro, {e})
        return {"message": error_msg}, 409
    except Exception as e:
        # tratando erros que nao sejam do tipo IntegrityError
        error_msg = "Nao foi possivel salvar novo registro :/"
        logger.warning(
            "Erro ao adicionar registro para a data %s, %s", diario.data_registro, {e})
        return {"message": error_msg}, 400


@app.get('/listar_diarios', tags=[diario_tag],
         responses={"200": DiarioListaSchema, "404": ErrorSchema})
def get_entradas_diario():
    """Retorna todos os registros do diario presentes no bd

    Retorna uma representacao da listagem de registros.
    """
    logger.debug("Buscando entradas de diário ")
    # criando conexao com o bd
    session = Session()
    # fazendo a busca
    entradas_diario = session.query(Diario).all()

    if not entradas_diario:
        # se nao ha registros cadastrados
        return {"diarios": []}, 200
    else:
        logger.debug("%s entradas de diario encontradas", len(entradas_diario))
        # retorna a representacao de um registro
        return retorna_lista_diarios(entradas_diario), 200


@app.get('/buscar_diario', tags=[diario_tag],
         responses={"200": DiarioViewSchema, "404": ErrorSchema})
def get_entrada_diario(query: DiarioBuscaSchema):
    """Faz a busca de um registro a partir da data informada

    Retorna uma representação do registro do diario de introducao alimentar e refeicoes associadas.
    """
    data_registro = query.data_registro
    logger.debug("Buscando entrada de diário para a data %s ", data_registro)
    # criando conexao com o bd
    session = Session()
    # fazendo a busca
    diario = session.query(Diario).filter(
        Diario.data_registro == data_registro).first()

    if not diario:
        # se o registro nao foi encontrado
        error_msg = "Entrada de diario não encontrada na base :/"
        logger.warning(
            "Erro ao buscar entrada de diário para a data %s , %s", data_registro, error_msg)
        return {"message": error_msg}, 404
    logger.debug("Entrada econtrada : %s", {diario.data_registro})
    # retorna a entrada encontrada
    return retorna_diario(diario), 200


@app.delete('/deletar_diario', tags=[diario_tag],
            responses={"200": DiarioRemocaoSchema, "404": ErrorSchema})
def del_produto(query: DiarioBuscaSchema):
    """Deleta um registro do diário a partir da data informada

    Retorna uma mensagem de confirmacao da remocao.
    """
    data_registro = query.data_registro
    logger.debug("Deletando entrada de diário para a data %s", data_registro)
    # criando conexao com o bd
    session = Session()
    # fazendo a remocao
    
    diario =  session.query(Diario).filter(
        Diario.data_registro == data_registro).first()
    
    
    for refeicao in diario.refeicoes:
        session.query(Refeicao).filter(
        Refeicao.id == refeicao.id).delete()
    
    count = session.query(Diario).filter(
        Diario.data_registro == data_registro).delete()
    session.commit()

    if count:
        # retorna a representacao da mensagem de confirmacao
        logger.debug("Deletado entrada para a data %s", data_registro)
        return {"message": "Entrada de diário removida", "data_registro": data_registro}

    error_msg = "Entrada de diário não encontrada na base :/"
    logger.warning("Erro ao deletar entrada de diário %s %s",
                   data_registro, error_msg)
    return {"message": error_msg}, 404


@app.post('/editar_diario', tags=[diario_tag],
          responses={"200": DiarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def edit_entrada_diario(body:DiarioSchema):
    """Edita um registro do diario de introducao alimentar

    Apenas as refeicoes podem ser editadas

    Retorna uma representacao do diario e refeicoes apos edicao
    """


    data_registro = body.data_registro

    try:
        # criando conexao com o bd
        session = Session()
        # fazendo a busca
        diario = session.query(Diario).filter(
            Diario.data_registro == data_registro).first()

        logger.debug(
            "Buscando entrada de diário para a data %s ", data_registro)

        if not diario:
            # se o registro nao for encontrado
            error_msg = "Entrada de diário não encontrada na base :/"
            logger.warning(
                "Erro ao buscar entrada de diário para a data %s , %s", data_registro, error_msg)
            return {"message": error_msg}, 404

        refeicoes = diario.refeicoes
        for refeicao in refeicoes:
            session.query(Refeicao).filter(
                Refeicao.id == refeicao.id).delete()
            session.commit()

        lista_refeicoes_brutas = body.refeicoes
        for refeicao_bruta in lista_refeicoes_brutas:
            refeicao = Refeicao(
                refeicao_bruta.tipo,
                refeicao_bruta.metodo,
                refeicao_bruta.avaliacao,
                refeicao_bruta.aceitacao,
                refeicao_bruta.comentarios
            )
            diario.adiciona_refeicao(refeicao)

        logger.debug("Editando entrada para a data: %s",
                     diario.data_registro)

        session.commit()
        return retorna_diario(diario), 200

    except Exception as e:
        # tratando erros nao previstos
        error_msg = "Não foi possível editar o registro :/"
        logger.warning(
            "Erro ao adicionar registro para a data %s, %s", diario.data_registro, {e})
        return {"message": error_msg}, 400

@app.get('/buscar_receita', tags=[receita_tag],
 responses={"200": ReceitaViewSchema,  "400": ErrorSchema})
def buscar_receita(query: ReceitaBuscaSchema):
        try:

            ingredientes = query.ingredients
            excluir_ingredientes = query.excludeIngredients
            max_results = 1

            ingredientes_traduzidos,ing_status_code = realizar_traducao(ingredientes, "pt-BR", "en")
            excluir_ingredientes_traduzidos,exc_ing_status_code  = realizar_traducao(excluir_ingredientes, "pt-BR", "en")

            if ing_status_code == 400 or exc_ing_status_code == 400 :
                error_msg = "Não foi possível traduzir os ingredientes"
                logger.warning(
                "Erro ao buscar receitas", error_msg)
                return {"message": error_msg}, 404
            
            url = "https://api.spoonacular.com/recipes/complexSearch"

            params = {
                "apiKey": SPOONACULAR_API_KEY,
                "includeIngredients": ingredientes_traduzidos,
                "excludeIngredients": excluir_ingredientes_traduzidos,
                "number": max_results,
                "addRecipeInformation": True,  
                "fillIngredients": True,
                "addRecipeInstructions": True,
            }
            
            
            logger.debug("Requisitando receitas")
            resposta = requests.get(url, params=params)

            if resposta.status_code == 200:

                dados = resposta.json()
                receitas = dados.get("results")

                receita = retorna_lista_receitas(receitas)[0]

                titulo = receita.get("titulo")
                instrucoes = receita.get("instrucoes")
                ingredientes = receita.get("ingredientes")

                texto_ingredientes = ""

                for ingrediente in ingredientes:
                    texto_ingredientes =  texto_ingredientes + str(ingrediente.get("quantidade"))+" "+ ingrediente.get("unidade") + ingrediente.get("nome") + "$$$"


                texto_a_traduzir = titulo + "&&&"+instrucoes+ "&&&"+texto_ingredientes

                texto_traduzido, status_code = realizar_traducao(texto_a_traduzir, "en", "pt-BR")

                if(status_code == 200):
                    texto_traduzido = organiza_estrutura_receita(texto_traduzido)

                return texto_traduzido, status_code

                # //return retorna_lista_receitas(receitas), 200
            else:
                error_msg = "Não foi possível realizar a requisição :/"
                logger.warning(
                    "Erro ao realizar a requisição",{e})
                return {"message": error_msg}, 400
        except Exception as e:
            # tratando erros nao previstos
            error_msg = "Não foi possível realizar a requisição :/"
            logger.warning(
                        "Erro ao realizar a requisição",{e})
            return {"message": error_msg}, 400


@app.get('/traduzir_texto', tags=[traducao_tag],
 responses={"200": TraducaoViewSchema,  "400": ErrorSchema})
def traduzir_texto(query: TraducaoRequisicaoSchema):
    try:

        texto = query.texto
        idioma_origem = query.idioma_origem
        idioma_destino = query.idioma_destino

        traducao, status_code = realizar_traducao(texto, idioma_origem, idioma_destino)

        if status_code == 200:
            return traducao, 200
        else:
            error_msg = "Não foi possível realizar a requisição :/"
            logger.warning(
                "Erro ao realizar a requisição",{error_msg})
            return {"message": error_msg}, 400

        
    except Exception as e:
        # tratando erros nao previstos
        error_msg = "Não foi possível realizar a requisição :/"
        logger.warning(
                    "Erro ao realizar a requisição",{e})
        return {"message": error_msg}, 400


def realizar_traducao(texto:str,idioma_origem:str, idioma_destino:str): 
    try:          
        if not texto:
            error_msg = "Texto a ser traduzido não enviado"
            logger.warning(
            "Erro ao traduzir texto", error_msg)
            return {"message": error_msg}, 404
        
        url = "https://translation.googleapis.com/language/translate/v2?key="+GOOGLE_TRANSLATE_API_KEY

        params = {
            "q": texto,
            "source": idioma_origem,
            "target": idioma_destino,
            "format": "text"
        }

        
        logger.debug("Requisitando tradução")

        resposta = requests.post(url, data=params)

        status_code = resposta.status_code

        if(status_code == 200):
            dados = resposta.json()

            resultado = dados.get("data")
            traduzido = resultado.get("translations")[0].get("translatedText")

            return traduzido,200
        else :
            return "", 400

        
    except Exception as e:
        # tratando erros nao previstos
        error_msg = "Não foi possível realizar a requisição :/"
        logger.warning(
                    "Erro ao realizar a requisição",{e})
        return {"message": error_msg}, 400