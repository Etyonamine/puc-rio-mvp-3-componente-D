from pydantic import BaseModel
from model.modelo import Modelo
from model.veiculo import Veiculo
from model.marca import Marca
from typing import List
from model import Base

from schemas import ModeloViewSchema, MarcaViewSchema


class VeiculoSchema(BaseModel):
    """Define como um novo veiculo deve ser inserido """    
    placa: str = "ABC-1234"
    codigo_modelo: int = 1
   
class VeiculoViewSchema(BaseModel):
    """ Define como uma veículo deverá retornado: modelo
    """
    codigo: int = 1
    placa: str = "ABC-1234"   
    codigo_modelo: int = 30
    modelo: ModeloViewSchema


class VeiculoEditSchema(BaseModel):
    """Define como será recebido os dados para a edição """
    codigo: int = 1
    placa: str = 'ABC-1235'    
    modelo_id: int = 30


class VeiculoBuscaDelSchema(BaseModel):
    """ Define como a estrutura que representa a busca de delete.Que será
        feita apenas com o codigo do  .

    """
    codigo: int = 1


class VeiculoBuscaPorModelo(BaseModel):
    """ Define como a estrutura que representa a busca de veiculos fará a
        a busca através do código do modelo            

    """
    codigo_modelo: int = 1


class ListaVeiculosSchema(BaseModel):
    """ Define como retorna a lista de veiculos.
    """
    veiculos: List[VeiculoViewSchema]


def apresenta_veiculo(veiculo: Veiculo):
    """ Retorna uma representação de um veiculo seguindo o schema definido em
       VeiculoViewSchema.
    """
    return {
        "codigo": veiculo.cod_veiculo,
        "nome": veiculo.des_placa,
        "codigo_modelo": veiculo.cod_modelo,
        "modelo": [{"codigo": veiculo.modelo.cod_modelo, 
                    "nome":  veiculo.modelo.nom_modelo,
                    "codigo_marca": veiculo.modelo.cod_marca,
                     "marca": [{"codigo": veiculo.modelo.marca.cod_marca,"nome": veiculo.modelo.marca.nom_marca}]
                  }]
    }



def apresenta_lista_veiculo(lista: List[Veiculo]):
    """ Retorna uma representação de veiculos seguindo o schema definido em
        VeiculoViewSchema.

    """
    result = []
    for item in lista:
       
        result.append({
            "codigo": item.cod_veiculo,
            "placa": item.des_placa,
            "codigo_modelo": item.cod_modelo,
            "modelo": [{"codigo": item.modelo.cod_modelo, 
                                "nome":  item.modelo.nom_modelo,
                                "codigo_marca": item.modelo.cod_marca,
                                "marca": [{"codigo": item.modelo.marca.cod_marca,"nome": item.modelo.marca.nom_marca}]
                  }]
        })

    return {"lista": result}    


