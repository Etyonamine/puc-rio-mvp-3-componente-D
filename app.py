from datetime import datetime
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, TipoOperacao, Operacao
from logger import logger
from schemas import *
from flask_cors import CORS


info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger,\
                             Redoc ou RapiDoc")

tipo_operacao_Tag = Tag(name="TipoOperacao", 
                        description="Adição, visualização,\
                                    edição e remoção de tipo_operacaos de veiculos à base")

operacao_Tag = Tag(name="Operacao", 
                        description="Adição, visualização,\
                                    edição e remoção de tipo_operacaos de veiculos à base")
 
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite\
       a escolha do estilo de documentação.
    """
    return redirect('/openapi')


# ***************************************************  Metodos do tipo de operacao ***************************************
# Novo registro na tabela tipo_operacao do veiculo
@app.post('/tipo_operacao', tags=[tipo_operacao_Tag],
          responses={"201": TipoOperacaoViewSchema,
                     "404": ErrorSchema,
                     "500": ErrorSchema})
def add_tipo_operacao(form: TipoOperacaoSchema):
    """ Adicionar a tipo_operacao de operacao """
    tipo_operacao = TipoOperacao(      
      sigla = form.sigla,
      descricao = form.descricao
    )

    logger.debug(f"Adicionando o tipo_operacao de operacao com a sigla {tipo_operacao.sigla}\
                     descricao { tipo_operacao.descricao }")
    
    try:
        # criando conexão com a base
        session = Session()
        # adicionando  
        session.add(tipo_operacao)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado o tipo_operacao de operacao com a sigla {tipo_operacao.sigla}\
                      descricao{tipo_operacao.descricao}")
        return apresenta_tipo_operacao(tipo_operacao), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = f"O tipo de operacao com a sigla {tipo_operacao.sigla} já foi salvo anteriormente na base :/"
        logger.warning(
            f"Erro ao adicionar a tipo_operacao do operacao com nome ={tipo_operacao.descricao}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar um novo tipo_operacao de operacao, {error_msg}")
        return {"message": error_msg}, 400


# Edicao registro na tabela tipo_operacao do veiculo
@app.put('/tipo_operacao', tags=[tipo_operacao_Tag],
         responses={"204": None,
                    "404": ErrorSchema,
                    "500": ErrorSchema})
def upd_tipo_operacao(form: TipoOperacaoEditSchema):
    """Editar uma tipo_operacao de veiculojá cadastrado na base """
    codigo = form.codigo
    sigla = form.sigla
    descricao = form.descricao

    logger.debug(f"Editando a tipo_operacao de operacao #{codigo}")
    try:

        # criando conexão com a base
        session = Session()
        # Consulta se ja existe a descricao com outro codigo
        tipo_operacao = session.query(TipoOperacao)\
                             .filter(TipoOperacao.sigla ==  sigla
                                and TipoOperacao.codigo != codigo
                             ).first()

        if tipo_operacao:
            # se foi encontrado retorna sem dar o commit
            error_msg = "Existe outro registro com\
                         a mesma sigla!"
            logger.warning(
                f"Erro ao editar a tipo_operacao com o codigo #{codigo} {error_msg}")
            return {"message": error_msg}, 400
        else:            
            count = session.query(TipoOperacao).filter(
                TipoOperacao.codigo == codigo)\
                            .update({"descricao": descricao,
                                    "sigla": sigla})
            session.commit()
            if count:
                # retorna sem representação com apenas o codigo http 204
                logger.debug(f"Editado a tipo_operacao com a sigla {sigla}")
                return '', 204
            else:
                error_msg = f"O tipo_operacao com a sigla {sigla} não foi encontrado na base"
                logger.warning(
                    f"Erro ao editar o tipo_operacao com a sigla {sigla} , {error_msg}")
                return '', 404
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível editar a tipo_operacao :/{e.__str__}"
        logger.warning(
            f"Erro ao editar o tipo_operacao com a sigla  #'{sigla}', {error_msg}")
        return {"message": error_msg}, 500


# Remoção de um registro de tipo_operacao de veiculo
@app.delete('/tipo_operacao', tags=[tipo_operacao_Tag],
            responses={"204": None, "404": ErrorSchema, "500": ErrorSchema})
def del_tipo_operacao(form: TipoOperacaoBuscaDelSchema):
    """Exclui uma tipo_operacao da base de dados através do atributo codigo

    Retorna uma mensagem de exclusão com sucesso.
    """
    codigo = form.codigo
    logger.debug(f"Excluindo a tipo_operacaoID #{codigo}")
    try:
        # criando conexão com a base
        session = Session()
        # validar se está sendo utilizado no operacao  
        """ operacao = session.query(Operacao)\
                             .filter(Operacao.id_operacao_tip == codigo).first()

        if operacao:
            # se há   cadastrado
            error_msg = "Não é possível excluir! O Tipo de Operacao está associado há um ou mais operações."
            logger.warning(f"Erro ao buscar a tipo_operacao de operacao , {error_msg}")
            return {"message": error_msg}, 400                """

        # fazendo a remoção
        count = session.query(TipoOperacao).filter(
            TipoOperacao.codigo == codigo).delete()
        session.commit()

        if count:
            # retorna sem representação com apenas o codigo http 204
            logger.debug(f"Excluindo o tipo_operacao com o codigo #{codigo}")
            return '', 204
        else:
            # se o   não foi encontrado retorno o codigo http 404
            error_msg = "O tipo_operacao de operacao não foi encontrado na base"
            logger.warning(
                f"Erro ao excluir o tipo_operacao com o \
                 codigo #'{codigo}', {error_msg}")
            return '', 404
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível excluir tipo_operacao  :/"
        logger.warning(
            f"Erro ao excluir a tipo_operacao com\
            o codigo #'{codigo}', {error_msg}")
        return {"message": error_msg}, 500


# Consulta de todos as tipo_operacaos
@app.get('/tipo_operacoes', tags=[tipo_operacao_Tag],
         responses={"200": ListaTipoOperacaosSchema, "500": ErrorSchema})
def get_tipo_operacaos():
    """Consulta as tipo_operacoes 

    Retorna uma listagem de representações dos tipo_operacoes
    """
    logger.debug(f"Consultando as tipo_operacoes   ")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        lista = session.query(TipoOperacao).all()

        if not lista:
            # se não há tipo_operacaos cadastrados
            return {"tipo_operacoes": []}, 200
        else:
            logger.debug(f"%d tipo_operacoes encontrados" %
                         len(lista))
            # retorna a representação de tipo_operacaos
            return apresenta_lista_tipo_operacao(lista), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar os tipo_operacoes de listas :/{str(e)}"
        logger.warning(
            f"Erro ao consultar tipo_operacoes, {error_msg}")
        return {"message": error_msg}, 500


# Consulta por código de tipo_operacao
@app.get('/tipo_operacao_id', tags=[tipo_operacao_Tag],
         responses={"200": TipoOperacaoViewSchema, "404": ErrorSchema,
                    "500": ErrorSchema})
def get_tipo_operacao_id(query: TipoOperacaoBuscaDelSchema):
    """Consulta um tipo_operacao pelo codigo

    Retorna uma representação da tipo_operacao  
    """

    codigo = query.codigo

    logger.debug(
        f"Consultando a tipo_operacao por codigo = #{codigo} ")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        tipo_operacao = session.query(TipoOperacao)\
                             .filter(TipoOperacao.codigo == codigo).first()

        if not tipo_operacao:
            # se não há   cadastrado
            error_msg = "Tipo Operacao não encontrado na base :/"
            logger.warning(f"Erro ao buscar a tipo_operacao de operacao , {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(
                f"Tipo Operacao #{codigo} encontrado")
            # retorna a representação de  s
            return apresenta_tipo_operacao(tipo_operacao), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar a tipo_operacao:/{str(e)}"
        logger.warning(
            f"Erro ao consultar a tipo_operacao do operacao, {error_msg}")
        return {"message": error_msg}, 500



# ***************************************************  Metodos do tipo de operacao ***************************************
# Novo registro na tabela tipo_operacao do veiculo
@app.post('/tipo_operacao', tags=[tipo_operacao_Tag],
          responses={"201": TipoOperacaoViewSchema,
                     "404": ErrorSchema,
                     "500": ErrorSchema})
def add_tipo_operacao(form: TipoOperacaoSchema):
    """ Adicionar a tipo_operacao de operacao """
    tipo_operacao = TipoOperacao(      
      sigla = form.sigla,
      descricao = form.descricao
    )

    logger.debug(f"Adicionando o tipo_operacao de operacao com a sigla {tipo_operacao.sigla}\
                     descricao { tipo_operacao.descricao }")
    
    try:
        # criando conexão com a base
        session = Session()
        # adicionando  
        session.add(tipo_operacao)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado o tipo_operacao de operacao com a sigla {tipo_operacao.sigla}\
                      descricao{tipo_operacao.descricao}")
        return apresenta_tipo_operacao(tipo_operacao), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = f"O tipo de operacao com a sigla {tipo_operacao.sigla} já foi salvo anteriormente na base :/"
        logger.warning(
            f"Erro ao adicionar a tipo_operacao do operacao com nome ={tipo_operacao.descricao}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar um novo tipo_operacao de operacao, {error_msg}")
        return {"message": error_msg}, 400
