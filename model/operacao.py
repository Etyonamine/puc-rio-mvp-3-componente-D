from datetime import datetime
from typing import Union
from sqlalchemy import Column, String, Integer, DateTime,ForeignKey
from model import Base
from sqlalchemy.orm import relationship
class Operacao(Base):
    __tablename__ = 'operacao'
    codigo = Column("id_operacao", Integer, primary_key=True)    
    codigo_veiculo = Column("id_veiculo",Integer)
    codigo_tipo_operacao = Column("id_operacao_tip", Integer,\
                             ForeignKey("tipo_operacao.id_operacao_tip"),
                             nullable=False)     
    data_entrada = Column("dt_entrada",DateTime, default = datetime.now())                            
    observacao = Column("ds_observacao", String(300))    
    data_saida = Column("dt_saida",DateTime)    
    
    tipo_operacao = relationship("TipoOperacao", back_populates="operacoes")

    ## criar a operacao    
    def __init__(self, codigo_veiculo: Integer,
                codigo_tipo_operacao: Integer, 
                observacao: String,
                data_entrada:Union[DateTime, None] = None):
        """
        Cria uma operacao

        Argumentos:
            codigo_veiculo: codigo do veiculo estacionado
            codigo_tipo_operacao: codigo do tipo de operacao Mensal, Avulsa
            observacao : alguma observacao
            data_insercao quando a operacao foi feito ou inserido
                           à base
        """
        self.data_entrada = data_entrada
        self.codigo_veiculo = codigo_veiculo
        self.codigo_tipo_operacao = codigo_tipo_operacao
        self.observacao = observacao