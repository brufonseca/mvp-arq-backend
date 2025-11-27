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

from schemas.receita import (ReceitaBuscaSchema, ReceitaViewSchema)

from schemas.error import ErrorSchema
from flask_cors import CORS

info = Info(title="Diário Introdução Alimentar API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
diario_tag = Tag(
    name="Diário", description="Adição, visualização e remoção de registros do diário de introdução alimentar")

receita_tag = Tag(name="Receitas", description="Busca de receitas usando a API Spoonacular")

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

@app.post('/buscar_receita', tags=[receita_tag],
 responses={"200": ReceitaViewSchema,  "400": ErrorSchema})
def buscar_receita(query: ReceitaBuscaSchema):
        try:
            dados = request.get_json()

            ingredientes = dados.get("ingredientes")
            max_results = dados.get("maxResults", 3)

            if not ingredientes:
                error_msg = "Lista de ingredientes não enviada"
                logger.warning(
                "Erro ao buscar receitas", error_msg)
                return {"message": error_msg}, 404
            
            url = "https://api.spoonacular.com/recipes/complexSearch"

            params = {
                "apiKey": "0f0ef747b6754511b84b68db4d23b893",
                "includeIngredients": ingredientes_query,
               
                "number": max_results,
                "addRecipeInformation": True,  # traz mais dados da receita
                "fillIngredients": True,
                "addRecipeInstructions": True,
            }

            resposta = requests.get(url, params=params)
            resposta.raise_for_status()

            resultados = resposta.json()

            logger.warning(resultados)
        except requests.exceptions.RequestException as e:
            return jsonify({"erro_api": str(e)}), 502

        except Exception as e:
            return jsonify({"erro": str(e)}), 500

            
