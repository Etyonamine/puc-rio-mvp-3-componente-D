from pydantic import BaseModel
from typing import Optional, List
from model import Base
from model.operacao import Operacao
from schemas.tipo_operacao import TipoOperacaoViewSchema


class OperacaoSchema(BaseModel):
    """Define como um novo registro que será inserido """        
    placa_veiculo: str = "ABC1234"   
    codigo_tipo_operacao: int = 1
    observacao: str  = ""


class OperacaoViewSchema(BaseModel):
    """ Define como deverá retornado
    """
    codigo: int = 1
    data_entrada: str = "2023/01/01 22:00:00"
    data_saida: str = "2023/01/01 22:00:00"
    codigo_tipo_operacao: int = 1
    placa_veiculo: str = "ABC1234"
    tipo_operacao: TipoOperacaoViewSchema


class OperacaoBuscaPorVeiculoSchema(BaseModel):
    """ Define como será recebido os dados para a pesquisa """
    placa_veiculo: str = "ABC1234"

    
class OperacaoEditSchema(BaseModel):
    """Define como será recebido os dados para a edição """
    codigo: int = 1
    codigo_tipo_operacao: int = 1
    observacao: str = ""


class OperacaoBuscaDelSchema(BaseModel):
    """ Define como a estrutura que representa a busca de delete.Que será
        feita apenas com o codigo da Operacao.

    """
    codigo: int = 1


class ListaOperacaosSchema(BaseModel):
    """ Define como retorna a lista de Operacaos de operacao.
    """
    Operacaos: List[OperacaoViewSchema]


def apresenta_operacao(operacao: Operacao):
    """ Retorna uma representação de um Operacao seguindo o schema definido em
        OperacaoViewSchema.
    """
    return {
        "codigo": operacao.codigo,
        "codigo_tipo_operacao": operacao.codigo_tipo_operacao,
        "placa_veiculo": operacao.placa_veiculo,
        "observacao": operacao.observacao,
        "data_entrada": operacao.data_entrada,
        "data_saida": operacao.data_saida,
        "tipo_operacao": [{"codigo": operacao.codigo_tipo_operacao ,
                           "sigla": operacao.tipo_operacao.sigla,
                           "descricao": operacao.tipo_operacao.descricao
                           }]
        
    }


def apresenta_lista_operacao(lista: List[Operacao]):
    """ Retorna uma representação da lista de operacoes seguindo o schema definido em
        OperacaoViewSchema.

    """
    result = []
    for item in lista:
       
        result.append({
            "codigo": item.codigo,
            "codigo_tipo_operacao": item.codigo_tipo_operacao,
            "placa_veiculo": item.placa_veiculo,
            "data_entrada": item.data_entrada,
            "data_saida": item.data_saida,
            "observacao": item.observacao,
            "tipo_operacao": [{"codigo": item.codigo_tipo_operacao ,
                            "sigla": item.tipo_operacao.sigla,
                            "descricao": item.tipo_operacao.descricao
                            }]
        })

    return {"lista": result}    